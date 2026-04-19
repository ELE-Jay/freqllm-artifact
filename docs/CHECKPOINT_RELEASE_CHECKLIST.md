# Checkpoint Release Checklist

This checklist is organized by target host.

## Before Uploading

1. Make sure the local checkpoint symlinks or files exist:

```bash
bash scripts/register_local_checkpoints.sh --source-python-dir /path/to/EncryptedLLM-repro-kit/python
```

2. Regenerate the verified manifest:

```bash
/opt/conda/bin/python scripts/build_checkpoint_manifest.py
```

3. Keep these files nearby while publishing:

- `checkpoints/checkpoint_manifest.generated.md`
- `checkpoints/checkpoint_manifest.generated.json`
- `checkpoints/checkpoint_urls.json`

## GitHub Release: `checkpoints-small-v1`

Upload these files to the GitHub release tag `checkpoints-small-v1`.

| File | Size |
|---|---:|
| `gpt2_baseline_kd_small.pth` | 473 MiB |
| `freqgpt_polynorm_kd_small_calibrated.pth` | 610 MiB |
| `polytransformer_paper_small.pth` | 473 MiB |
| `freqgpt_ablation_formal_full_kd_small.pth` | 610 MiB |
| `freqgpt_ablation_formal_no_kd_small.pth` | 610 MiB |
| `freqgpt_ablation_formal_from_scratch_small.pth` | 610 MiB |

After uploading, verify that these URLs work:

- `https://github.com/ELE-Jay/freqllm-artifact/releases/download/checkpoints-small-v1/gpt2_baseline_kd_small.pth`
- `https://github.com/ELE-Jay/freqllm-artifact/releases/download/checkpoints-small-v1/freqgpt_polynorm_kd_small_calibrated.pth`
- `https://github.com/ELE-Jay/freqllm-artifact/releases/download/checkpoints-small-v1/polytransformer_paper_small.pth`
- `https://github.com/ELE-Jay/freqllm-artifact/releases/download/checkpoints-small-v1/freqgpt_ablation_formal_full_kd_small.pth`
- `https://github.com/ELE-Jay/freqllm-artifact/releases/download/checkpoints-small-v1/freqgpt_ablation_formal_no_kd_small.pth`
- `https://github.com/ELE-Jay/freqllm-artifact/releases/download/checkpoints-small-v1/freqgpt_ablation_formal_from_scratch_small.pth`

## GitHub Release: `checkpoints-medium-v1`

Upload these files to the GitHub release tag `checkpoints-medium-v1`.

| File | Size |
|---|---:|
| `gpt2_baseline_kd_medium.pth` | 1.32 GiB |
| `freqgpt_polynorm_kd_medium_calibrated.pth` | 1.46 GiB |
| `polytransformer_paper_medium.pth` | 1.32 GiB |

After uploading, verify that these URLs work:

- `https://github.com/ELE-Jay/freqllm-artifact/releases/download/checkpoints-medium-v1/gpt2_baseline_kd_medium.pth`
- `https://github.com/ELE-Jay/freqllm-artifact/releases/download/checkpoints-medium-v1/freqgpt_polynorm_kd_medium_calibrated.pth`
- `https://github.com/ELE-Jay/freqllm-artifact/releases/download/checkpoints-medium-v1/polytransformer_paper_medium.pth`

## Hugging Face or Zenodo: Large Checkpoints

Recommended repository name:

- `ELE-Jay/freqllm-checkpoints`

Recommended files:

| File | Size |
|---|---:|
| `gpt2_baseline_kd_large.pth` | 2.88 GiB |
| `freqgpt_polynorm_kd_large_calibrated.pth` | 2.99 GiB |
| `polytransformer_paper_large.pth` | 2.88 GiB |

If you use Hugging Face, the target URLs should look like:

- `https://huggingface.co/ELE-Jay/freqllm-checkpoints/resolve/main/gpt2_baseline_kd_large.pth`
- `https://huggingface.co/ELE-Jay/freqllm-checkpoints/resolve/main/freqgpt_polynorm_kd_large_calibrated.pth`
- `https://huggingface.co/ELE-Jay/freqllm-checkpoints/resolve/main/polytransformer_paper_large.pth`

## After Uploading

1. Open and edit:

- `checkpoints/checkpoint_urls.json`

2. Replace any placeholder URL with the actual published URL.

3. Test a small download:

```bash
python scripts/fetch_checkpoints.py \
  --manifest checkpoints/checkpoint_urls.json \
  --only gpt2_baseline_kd_small.pth \
  --skip-existing
```

4. Test one medium or large download in the same way.

5. Commit and push the updated `checkpoints/checkpoint_urls.json`.

## Reviewer-Facing Sanity Check

After the URLs are final, this command should work end to end:

```bash
python scripts/fetch_checkpoints.py --manifest checkpoints/checkpoint_urls.json
```

Then checkpoint-level reproducibility can start with:

```bash
bash scripts/run_checkpoint_repro.sh --code-root /path/to/EncryptedLLM-repro-kit/python
```
