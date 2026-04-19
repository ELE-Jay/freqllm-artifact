# Reproducibility Tiers

This artifact supports three reproducibility tiers.

## Tier 1: Snapshot-Level Artifact Reproduction

Goal:

- deterministically regenerate the paper figures and tables
- avoid heavy OpenFHE/GPU reruns during artifact evaluation

Entry point:

```bash
bash scripts/reproduce_all.sh
```

Inputs:

- validated JSON result snapshots in `results/`

Outputs:

- regenerated PDFs/PNGs in `figures/`
- regenerated `.tex`/`.md` tables in `tables/`

## Tier 2: Checkpoint-Level Reproducibility

Goal:

- start from trained checkpoints
- rerun evaluation and latency measurement
- regenerate the JSON results and the paper figures/tables

Requirements:

- the full codebase checkout containing the original training and evaluation scripts
- an OpenFHE/GPU-capable environment, typically the `encryptedllm` conda environment
- local GPT-2 resources, local datasets, and the trained checkpoint files

Entry point:

```bash
bash scripts/run_checkpoint_repro.sh --code-root /path/to/EncryptedLLM-repro-kit/python
```

What it does:

1. Symlinks checkpoints from `checkpoints/` into the full codebase at the filenames expected by the evaluation scripts.
2. Reruns:
   - 8-task accuracy for small/medium/large
   - task-bucket latency for small/medium/large
   - small sequence-length scalability
   - small architecture-side ablation latency
   - small KD ablation evaluation
3. Copies the regenerated JSON outputs back into `results/`.
4. Reruns `bash scripts/reproduce_all.sh` to redraw the figures and tables from the regenerated outputs.

## Tier 3: Full Training Reproducibility

Goal:

- start from training scripts and datasets
- regenerate checkpoints
- rerun evaluation
- redraw the published figures and tables

Requirements:

- everything required by Tier 2
- local OpenWebText parquet shards
- local Wikitext-103 parquet shards
- local GPT-2 tokenizer/config/model resources
- sufficient GPU memory and runtime budget

Entry point:

```bash
bash scripts/run_full_training_pipeline.sh --code-root /path/to/EncryptedLLM-repro-kit/python
```

What it does:

1. Trains:
   - GPT-2 baseline checkpoints
   - FreqGPT checkpoints
   - paper-style PolyTransformer checkpoints
   - small KD ablation checkpoints
2. Writes checkpoints into `checkpoints/`.
3. Calls `scripts/run_checkpoint_repro.sh` to produce the evaluation outputs and redraw the paper artifacts.

## Distribution of Checkpoints

The checkpoint files are too large for normal Git history and several are also too large for a single GitHub release asset. The practical recommendation is:

- store the manifest and reproduction scripts in GitHub
- distribute small checkpoints via GitHub Releases if desired
- distribute medium/large checkpoints via Zenodo, Hugging Face, or another large-object host
- place the downloaded files into `checkpoints/` using the exact filenames in `checkpoints/checkpoint_manifest.md`

See `checkpoints/README.md` for the expected filenames.
