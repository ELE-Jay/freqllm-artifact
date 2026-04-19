# Checkpoints

This directory is intentionally empty in Git history.

## Why

The trained checkpoints are large:

- small checkpoints are hundreds of MiB
- medium checkpoints are around 1.4--1.5 GiB
- large checkpoints are around 2.9--3.0 GiB

So they should not be committed into normal Git history. Instead, publish them as release assets or via an external large-file host, then place or symlink them into this directory with the exact filenames listed in `checkpoint_manifest.md`.

## How to Use

If you already have a local codebase with the trained checkpoints, you can populate this directory automatically:

```bash
bash scripts/register_local_checkpoints.sh --source-python-dir /path/to/EncryptedLLM-repro-kit/python
```

Then you can run checkpoint-level reproducibility:

```bash
bash scripts/run_checkpoint_repro.sh --code-root /path/to/EncryptedLLM-repro-kit/python
```

For full training reproducibility, use:

```bash
bash scripts/run_full_training_pipeline.sh --code-root /path/to/EncryptedLLM-repro-kit/python
```
