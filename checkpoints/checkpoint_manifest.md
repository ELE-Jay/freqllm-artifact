# Checkpoint Manifest

Place the following files in `checkpoints/` with exactly these names.

## Main Model Checkpoints

| File name | Role | Approx. size |
|---|---|---:|
| `gpt2_baseline_kd_small.pth` | Plaintext GPT-2 baseline, small | 473 MiB |
| `gpt2_baseline_kd_medium.pth` | Plaintext GPT-2 baseline, medium | 1.4 GiB |
| `gpt2_baseline_kd_large.pth` | Plaintext GPT-2 baseline, large | 2.9 GiB |
| `freqgpt_polynorm_kd_small_calibrated.pth` | FreqGPT, small | 611 MiB |
| `freqgpt_polynorm_kd_medium_calibrated.pth` | FreqGPT, medium | 1.5 GiB |
| `freqgpt_polynorm_kd_large_calibrated.pth` | FreqGPT, large | 3.0 GiB |
| `polytransformer_paper_small.pth` | PolyTransformer, small | 474 MiB |
| `polytransformer_paper_medium.pth` | PolyTransformer, medium | 1.4 GiB |
| `polytransformer_paper_large.pth` | PolyTransformer, large | 2.9 GiB |

## Small Ablation Checkpoints

| File name | Role | Approx. size |
|---|---|---:|
| `freqgpt_ablation_formal_full_kd_small.pth` | FreqGPT small KD ablation: full KD | 611 MiB |
| `freqgpt_ablation_formal_no_kd_small.pth` | FreqGPT small KD ablation: no KD | 611 MiB |
| `freqgpt_ablation_formal_from_scratch_small.pth` | FreqGPT small KD ablation: from scratch | 611 MiB |

## Notes

- The reproduction scripts expect these exact filenames.
- If you already have the local training repo checkout, `scripts/register_local_checkpoints.sh` can symlink these files into this directory automatically.
