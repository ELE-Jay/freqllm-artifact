# FreqLLM CCS'26 Artifact

This repository packages the result snapshots, plotting scripts, table-generation scripts, checkpoint manifests, and wrapper pipelines needed to reproduce the core paper artifacts for our FHE-friendly GPT-2 study at multiple reproducibility tiers.

## Reproducibility Tiers

This repository now supports three levels of reproducibility:

1. Snapshot-level artifact reproduction
   Regenerate the published figures and tables from validated JSON result snapshots.
2. Checkpoint-level reproducibility
   Provide trained checkpoints, relink them into the full codebase, rerun evaluation, regenerate JSON outputs, and then redraw the paper figures and tables.
3. Full training reproducibility
   Start from the training scripts, produce checkpoints, rerun evaluation, and regenerate the paper artifacts.

See:

- `docs/REPRODUCIBILITY_TIERS.md`
- `checkpoints/README.md`
- `scripts/run_checkpoint_repro.sh`
- `scripts/run_full_training_pipeline.sh`

## Snapshot-Level Artifact Reproduction

Running the reproduction pipeline regenerates:

- `figures/gpt2_fhe_task_bucket_latency_small_medium_large.pdf`
- `figures/icml25_fig2_ours_component_breakdown_small.pdf`
- `figures/sequence_length_scalability_comparison_small.pdf`
- `figures/freqgpt_ablation_small_arch_latency.pdf`
- `figures/freqgpt_ablation_small_kd_accuracy.pdf`
- `tables/main_accuracy.tex`
- `tables/freqgpt_approx_params.tex`
- `tables/freqgpt_depth_cts_small.tex`

The generated figures and tables are rebuilt from validated result snapshots exported from the formal experiment runs. This keeps snapshot-level artifact reproduction lightweight and deterministic for reviewers.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash scripts/reproduce_all.sh
```

All outputs will be written to `figures/` and `tables/`.

## Directory Layout

- `results/`: validated experiment snapshots in JSON form
- `checkpoints/`: checkpoint manifest and placement instructions
- `scripts/`: figure and table reproduction scripts
- `src/`: public reference implementation snippets with sanitized `FreqMixer` terminology
- `docs/`: Open Science URL template and artifact notes
- `figures/`: regenerated paper figures
- `tables/`: regenerated paper tables

## Notes

- The public artifact uses the name `FreqMixer` consistently for our frequency-domain mixer operator and related ablations.
- The scripts here are intentionally self-contained and rely only on `numpy` and `matplotlib`.
- Heavy OpenFHE/GPU reruns are not required for the snapshot-level artifact path.
- Checkpoint-level and full-training reproducibility require the full OpenFHE/GPU codebase, datasets, and large checkpoint files described in `docs/REPRODUCIBILITY_TIERS.md`.

## Publishing

This directory is ready to be initialized as a Git repository and pushed to GitHub. The only missing step is GitHub authentication for the final `git push`.
