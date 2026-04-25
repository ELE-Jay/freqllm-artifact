from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
PLOTS_DIR = SCRIPT_DIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from fhe_latency_common import (  # noqa: E402
    SLOT_CAPACITY,
    measure_baseline_block_latency,
    measure_freqgpt_block_latency,
    measure_polytransformer_block_latency,
    measure_thor_block_latency,
)
from gpt2_variant_utils import get_variant_spec  # noqa: E402
from refresh_thor_results_from_cached_primitives import fit_primitive_latencies  # noqa: E402


SECURITY_CONFIGS = {
    128: {"ring_dim": 1 << 16},
    192: {"ring_dim": 1 << 17},
    256: {"ring_dim": 1 << 18},
}

METHODS = [
    ("encryptedllm", "EncryptedLLM", "#9BBBE1", "\\\\\\"),
    ("polytransformer", "PolyTransformer", "#B7B7EB", "xx"),
    ("thor", "THOR", "#D8C4A3", "//"),
    ("freqllm", "FreqLLM", "#F09BA0", "..."),
]

TASK_BUCKETS = [
    ("32 tok", 32),
    ("64 tok", 64),
    ("128 tok", 128),
]


def _ntt_factor(ring_dim: int, base_ring_dim: int) -> float:
    return (ring_dim * math.log2(ring_dim)) / (base_ring_dim * math.log2(base_ring_dim))


def _linear_factor(ring_dim: int, base_ring_dim: int) -> float:
    return ring_dim / base_ring_dim


def scale_primitive_latencies(
    base_latencies: dict[str, float],
    ring_dim: int,
    base_ring_dim: int = 1 << 16,
) -> dict[str, float]:
    """Scale primitive prices for a larger CKKS ring.

    Rotations, ciphertext multiplications, plaintext multiplications, and
    bootstrapping are NTT-heavy, so we scale them with N log N. Ciphertext
    addition is mostly coefficient-wise and is scaled linearly with N.
    """

    ntt = _ntt_factor(ring_dim, base_ring_dim)
    linear = _linear_factor(ring_dim, base_ring_dim)
    return {
        "rotate": base_latencies["rotate"] * ntt,
        "add": base_latencies["add"] * linear,
        "mul_cc": base_latencies["mul_cc"] * ntt,
        "mul_cp": base_latencies["mul_cp"] * ntt,
        "bootstrap": base_latencies["bootstrap"] * ntt,
        "light_bootstrap": base_latencies.get("light_bootstrap", 0.0) * ntt,
    }


def measure_method(
    method: str,
    seq_len: int,
    hidden_size: int,
    num_heads: int,
    n_layers: int,
    primitive_latencies: dict[str, float],
    slot_capacity: int,
) -> float:
    if method == "encryptedllm":
        per_block = measure_baseline_block_latency(
            None,
            None,
            seq_len,
            hidden_size,
            num_heads,
            slot_capacity=slot_capacity,
            primitive_latencies=primitive_latencies,
        )
    elif method == "polytransformer":
        per_block = measure_polytransformer_block_latency(
            None,
            None,
            seq_len,
            hidden_size,
            num_heads,
            slot_capacity=slot_capacity,
            primitive_latencies=primitive_latencies,
        )
    elif method == "thor":
        per_block = measure_thor_block_latency(
            None,
            None,
            seq_len,
            hidden_size,
            num_heads,
            slot_capacity=slot_capacity,
            primitive_latencies=primitive_latencies,
        )
    elif method == "freqllm":
        per_block = measure_freqgpt_block_latency(
            None,
            None,
            seq_len,
            hidden_size,
            slot_capacity=slot_capacity,
            primitive_latencies=primitive_latencies,
        )
    else:
        raise ValueError(f"Unknown method: {method}")
    return per_block * n_layers


def build_results(args: argparse.Namespace) -> dict:
    base_primitive_latencies = fit_primitive_latencies()
    variants = [x.strip() for x in args.variants.split(",") if x.strip()]
    security_levels = [int(x.strip()) for x in args.security_levels.split(",") if x.strip()]

    results = {
        "metadata": {
            "experiment": "security_level_latency_sensitivity",
            "backend": "OpenFHE-GPU primitive-calibrated latency model",
            "scheme": "CKKS",
            "secret_key_distribution": "GAUSSIAN",
            "standard_deviation": 3.2,
            "multiplicative_depth": 24,
            "scaling_modulus_size": 50,
            "first_modulus_size": 60,
            "base_ring_dim": 1 << 16,
            "logical_slot_capacity": args.slot_capacity,
            "security_configs": SECURITY_CONFIGS,
            "primitive_scaling": {
                "rotate": "N log N",
                "add": "N",
                "mul_cc": "N log N",
                "mul_cp": "N log N",
                "bootstrap": "N log N",
                "light_bootstrap": "N log N",
            },
            "packing_policy": "fixed logical packing across security levels",
            "note": (
                "We vary the CKKS security level by conservatively increasing "
                "the ring dimension and scaling primitive latency. The logical "
                "packing budget is held fixed so higher lambda does not obtain "
                "extra packing capacity as a confounder."
            ),
            "base_primitive_latencies": base_primitive_latencies,
        },
        "results": {},
    }

    for variant in variants:
        spec = get_variant_spec(variant)
        results["results"][variant] = {}
        for bucket_label, seq_len in TASK_BUCKETS:
            if seq_len not in args.seq_lens:
                continue
            bucket_rows = {}
            for lambda_bits in security_levels:
                if lambda_bits not in SECURITY_CONFIGS:
                    raise ValueError(f"Unsupported security level: {lambda_bits}")
                ring_dim = SECURITY_CONFIGS[lambda_bits]["ring_dim"]
                primitive_latencies = scale_primitive_latencies(base_primitive_latencies, ring_dim)
                row = {
                    "lambda": lambda_bits,
                    "ring_dim": ring_dim,
                    "slot_capacity": args.slot_capacity,
                }
                for method_key, _, _, _ in METHODS:
                    row[method_key] = measure_method(
                        method=method_key,
                        seq_len=seq_len,
                        hidden_size=spec["d_model"],
                        num_heads=spec["n_heads"],
                        n_layers=spec["n_layers"],
                        primitive_latencies=primitive_latencies,
                        slot_capacity=args.slot_capacity,
                    )
                row["freqllm_speedup_vs_thor"] = row["thor"] / row["freqllm"]
                row["freqllm_speedup_vs_encryptedllm"] = row["encryptedllm"] / row["freqllm"]
                bucket_rows[str(lambda_bits)] = row
            results["results"][variant][bucket_label] = {
                "seq_len": seq_len,
                "latency_by_security_level": bucket_rows,
            }
    return results


def write_markdown(results: dict, output_path: Path) -> None:
    lines = [
        "# Security-Level Latency Sensitivity",
        "",
        "Latency is in seconds. Lower is better.",
        "",
        "Parameters: CKKS, multiplicative depth = 24, scaling modulus size = 50, first modulus size = 60, logical slot capacity = 32768.",
        "Security levels use conservative ring dimensions: λ=128 -> N=65536, λ=192 -> N=131072, λ=256 -> N=262144.",
        "Primitive scaling: additions scale with N; rotations, multiplications, and bootstrapping scale with N log N.",
        "",
    ]
    for variant, variant_rows in results["results"].items():
        lines.append(f"## GPT-2 {variant.capitalize()}")
        for bucket_label, bucket_data in variant_rows.items():
            lines.append("")
            lines.append(f"### {bucket_label}")
            lines.append(
                "| λ | Ring dim | EncryptedLLM | PolyTransformer | THOR | FreqLLM | FreqLLM speedup vs THOR |"
            )
            lines.append("|---:|---:|---:|---:|---:|---:|---:|")
            for lambda_bits, row in bucket_data["latency_by_security_level"].items():
                lines.append(
                    f"| {lambda_bits} | {row['ring_dim']} | "
                    f"{row['encryptedllm']:.1f} | {row['polytransformer']:.1f} | "
                    f"{row['thor']:.1f} | {row['freqllm']:.1f} | "
                    f"{row['freqllm_speedup_vs_thor']:.2f}x |"
                )
        lines.append("")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_results(results: dict, output_prefix: Path, bucket_label: str = "128 tok") -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 10,
            "axes.labelsize": 10,
            "axes.titlesize": 10,
            "legend.fontsize": 8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    variants = list(results["results"].keys())
    fig, axes = plt.subplots(1, len(variants), figsize=(3.2 * len(variants), 2.55), sharey=False)
    if len(variants) == 1:
        axes = [axes]

    for ax, variant in zip(axes, variants):
        bucket_data = results["results"][variant][bucket_label]["latency_by_security_level"]
        lambdas = [int(x) for x in bucket_data.keys()]
        x = np.arange(len(lambdas))
        width = 0.19
        offsets = np.linspace(-1.5 * width, 1.5 * width, len(METHODS))

        for offset, (method_key, method_label, color, hatch) in zip(offsets, METHODS):
            values = [bucket_data[str(lambda_bits)][method_key] for lambda_bits in lambdas]
            ax.bar(
                x + offset,
                values,
                width=width,
                label=method_label,
                color=color,
                edgecolor="black",
                linewidth=0.9,
                hatch=hatch,
                )

        ax.set_title(f"GPT-2 {variant.capitalize()}")
        ax.set_xlabel(r"Security level $\lambda$")
        ax.set_xticks(x)
        ax.set_xticklabels([str(v) for v in lambdas])
        ax.grid(axis="y", linestyle="--", linewidth=0.45, alpha=0.45)
        ax.set_axisbelow(True)
        y_max = max(
            bucket_data[str(lambda_bits)][method_key]
            for lambda_bits in lambdas
            for method_key, _, _, _ in METHODS
        )
        ax.set_ylim(0, y_max * 1.18)

    axes[0].set_ylabel("Encrypted latency (s)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.03),
        ncol=4,
        frameon=True,
        edgecolor="black",
        columnspacing=0.9,
        handlelength=1.4,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.91), w_pad=1.0)

    pdf_path = output_prefix.with_suffix(".pdf")
    png_path = output_prefix.with_suffix(".png")
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[Saved] {pdf_path}")
    print(f"[Saved] {png_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variants", default="small,medium,large")
    parser.add_argument("--security-levels", default="128,192,256")
    parser.add_argument("--seq-lens", type=lambda s: {int(x) for x in s.split(",")}, default={32, 64, 128})
    parser.add_argument("--slot-capacity", type=int, default=SLOT_CAPACITY)
    parser.add_argument(
        "--output-json",
        type=Path,
        default=SCRIPT_DIR / "security_level_latency_results.json",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=SCRIPT_DIR / "security_level_latency_results.md",
    )
    parser.add_argument(
        "--plot-output-prefix",
        type=Path,
        default=PLOTS_DIR / "security_level_latency_gpt2_128tok",
    )
    parser.add_argument("--plot-bucket", default="128 tok")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = build_results(args)
    args.output_json.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    write_markdown(results, args.output_md)
    plot_results(results, args.plot_output_prefix, bucket_label=args.plot_bucket)
    print(f"[Saved] {args.output_json}")
    print(f"[Saved] {args.output_md}")


if __name__ == "__main__":
    main()
