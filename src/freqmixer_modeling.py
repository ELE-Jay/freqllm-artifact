from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


DEFAULT_POLY_COEFFS = (1.875, -1.25, 0.375)


class ResidualScale(nn.Module):
    def __init__(self, init_value: float) -> None:
        super().__init__()
        self.gain = nn.Parameter(torch.tensor(float(init_value), dtype=torch.float32))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x * self.gain.to(dtype=x.dtype, device=x.device)


class DistributionCalibratedPolyNorm(nn.Module):
    """Constant-depth normalization calibrated to observed variance statistics."""

    def __init__(
        self,
        d_model: int,
        momentum: float = 0.05,
        clamp_min: float = 0.1,
        clamp_max: float = 10.0,
        range_limit: float = 2.5,
    ) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.ones(d_model))
        self.bias = nn.Parameter(torch.zeros(d_model))
        self.poly_coeffs = nn.Parameter(torch.tensor(DEFAULT_POLY_COEFFS, dtype=torch.float32), requires_grad=False)
        self.register_buffer("running_var_mean", torch.tensor(1.0))
        self.register_buffer("running_var_std", torch.tensor(0.25))
        self.register_buffer("last_var_mean", torch.tensor(1.0))
        self.register_buffer("last_var_std", torch.tensor(0.25))
        self.momentum = momentum
        self.clamp_min = clamp_min
        self.clamp_max = clamp_max
        self.range_limit = range_limit
        self._cached_scaled_var = None

    def _update_running_stats(self, var: torch.Tensor) -> None:
        var_detached = var.detach()
        batch_mean = var_detached.mean()
        batch_std = var_detached.std(unbiased=False).clamp_min(1e-4)
        self.running_var_mean.mul_(1.0 - self.momentum).add_(self.momentum * batch_mean)
        self.running_var_std.mul_(1.0 - self.momentum).add_(self.momentum * batch_std)
        self.last_var_mean.copy_(batch_mean)
        self.last_var_std.copy_(batch_std)

    def _scaled_variance(self, var: torch.Tensor) -> torch.Tensor:
        if self.training:
            self._update_running_stats(var)
        ref = self.running_var_mean.clamp_min(1e-4)
        return var / ref

    def calibration_regularizer(self) -> torch.Tensor:
        if self._cached_scaled_var is None:
            return self.weight.new_zeros(())
        overflow = torch.relu((self._cached_scaled_var - 1.0).abs() - self.range_limit)
        return overflow.square().mean()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        mu = x.mean(dim=-1, keepdim=True)
        centered = x - mu
        var = centered.square().mean(dim=-1, keepdim=True)
        scaled_var = self._scaled_variance(var)
        self._cached_scaled_var = scaled_var

        coeffs = self.poly_coeffs.to(dtype=x.dtype, device=x.device)
        ref_inv_std = self.running_var_mean.clamp_min(1e-4).rsqrt().to(dtype=x.dtype, device=x.device)
        inv_std_approx = ref_inv_std * (
            coeffs[0] + coeffs[1] * scaled_var + coeffs[2] * scaled_var.square()
        )
        if self.training:
            inv_std_approx = torch.clamp(inv_std_approx, min=self.clamp_min, max=self.clamp_max)

        x_norm = centered * inv_std_approx
        return x_norm * self.weight + self.bias


class CausalFreqMixer(nn.Module):
    """Frequency-domain causal mixer with fixed-order gating."""

    def __init__(self, d_model: int, max_length: int, order: int = 2) -> None:
        super().__init__()
        self.d_model = d_model
        self.max_length = max_length
        self.order = order
        self.proj = nn.Linear(d_model, d_model * (order + 1))
        self.filter_time = nn.Parameter(torch.randn(order, 1, max_length, d_model) / (max_length ** 0.5))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, seq_len, _ = x.shape
        projected = self.proj(x).view(batch, seq_len, self.order + 1, self.d_model).transpose(1, 2)
        value_stream = projected[:, 0]
        gate_streams = projected[:, 1:]

        fft_size = 2 * self.max_length
        padded_value = F.pad(value_stream, (0, 0, 0, self.max_length))

        for stage in range(self.order):
            padded_filter = F.pad(self.filter_time[stage], (0, 0, 0, self.max_length))
            value_fft = torch.fft.fft(padded_value, n=fft_size, dim=1)
            filter_fft = torch.fft.fft(padded_filter, n=fft_size, dim=1)
            convolved = torch.fft.ifft(value_fft * filter_fft, n=fft_size, dim=1).real
            value_stream = convolved[:, :seq_len, :] * gate_streams[:, stage]
            padded_value = F.pad(value_stream, (0, 0, 0, self.max_length))

        return value_stream


class FreqGPTModel(nn.Module):
    """Reference public model snippet using PolyNorm + FreqMixer blocks."""

    def __init__(
        self,
        vocab_size: int = 50257,
        d_model: int = 768,
        max_length: int = 256,
        n_layers: int = 12,
        mixer_order: int = 2,
    ) -> None:
        super().__init__()
        residual_init = 1.0 / (2.0 * n_layers) ** 0.5
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.blocks = nn.ModuleList(
            [
                nn.ModuleDict(
                    {
                        "ln1": DistributionCalibratedPolyNorm(d_model),
                        "freqmixer": CausalFreqMixer(d_model, max_length, order=mixer_order),
                        "freqmixer_scale": ResidualScale(residual_init),
                        "ln2": DistributionCalibratedPolyNorm(d_model),
                        "mlp": nn.Sequential(
                            nn.Linear(d_model, 4 * d_model),
                            nn.GELU(),
                            nn.Linear(4 * d_model, d_model),
                        ),
                        "mlp_scale": ResidualScale(residual_init),
                    }
                )
                for _ in range(n_layers)
            ]
        )
        self.lm_head = nn.Linear(d_model, vocab_size)
        self._init_weights()

    def _init_weights(self) -> None:
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.Embedding):
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
            elif isinstance(module, CausalFreqMixer):
                nn.init.normal_(module.filter_time, mean=0.0, std=0.01)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        x = self.embedding(input_ids)
        for block in self.blocks:
            x = x + block["freqmixer_scale"](block["freqmixer"](block["ln1"](x)))
            x = x + block["mlp_scale"](block["mlp"](block["ln2"](x)))
        return self.lm_head(x)

    def calibration_regularizer(self) -> torch.Tensor:
        reg = self.embedding.weight.new_zeros(())
        for block in self.blocks:
            reg = reg + block["ln1"].calibration_regularizer()
            reg = reg + block["ln2"].calibration_regularizer()
        return reg
