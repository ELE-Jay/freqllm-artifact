# Checkpoint Distribution Plan

This document describes a practical publication strategy for the trained checkpoints.

## Recommended Hosting Split

The checkpoint sizes motivate a mixed strategy:

### GitHub Repository

Keep only:

- manifests
- download metadata
- reproduction scripts
- documentation

Do **not** commit the raw `.pth` files into Git history.

### GitHub Releases

Good fit for:

- small checkpoints
- possibly medium checkpoints

Reason:

- GitHub release assets support files under 2 GiB each
- small checkpoints are comfortably below this limit
- medium checkpoints are around 1.4--1.5 GiB and still fit

Suggested assets:

- `gpt2_baseline_kd_small.pth`
- `freqgpt_polynorm_kd_small_calibrated.pth`
- `polytransformer_paper_small.pth`
- `freqgpt_ablation_formal_full_kd_small.pth`
- `freqgpt_ablation_formal_no_kd_small.pth`
- `freqgpt_ablation_formal_from_scratch_small.pth`
- optionally the medium checkpoints

### External Large-File Host

Recommended for:

- large checkpoints
- any medium checkpoints if you prefer a single hosting backend

Practical options:

- Zenodo
- Hugging Face model/dataset repository

Reason:

- several large checkpoints are around 2.9--3.0 GiB
- these exceed the 2 GiB per-release-asset limit on GitHub releases

## Publishing Workflow

1. Place the local checkpoints in `checkpoints/` or symlink them there with:

```bash
bash scripts/register_local_checkpoints.sh --source-python-dir /path/to/EncryptedLLM-repro-kit/python
```

2. Build a verified manifest with size and SHA-256:

```bash
python scripts/build_checkpoint_manifest.py
```

This writes:

- `checkpoints/checkpoint_manifest.generated.json`
- `checkpoints/checkpoint_manifest.generated.md`

3. Upload the files to the chosen host(s).

4. Fill the real URLs into:

- `checkpoints/checkpoint_urls.json`

5. Reviewers can then download and verify checkpoints with:

```bash
python scripts/fetch_checkpoints.py --manifest checkpoints/checkpoint_urls.json
```

## Suggested Release Layout

### Release `checkpoints-small-v1`

- baseline small
- FreqGPT small
- PolyTransformer small
- three small KD ablation checkpoints

### Release `checkpoints-medium-v1`

- baseline medium
- FreqGPT medium
- PolyTransformer medium

### External host collection `checkpoints-large-v1`

- baseline large
- FreqGPT large
- PolyTransformer large

## Notes

- If you use Hugging Face, point `checkpoint_urls.json` at the direct download URLs.
- If you use Zenodo, use the stable record URL or the direct file URL.
- Keep the filenames unchanged so the existing wrapper scripts can link them into the full codebase without extra renaming.
