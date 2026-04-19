# FreqLLM CCS'26 Artifact

This repository packages the result snapshots, plotting scripts, and table-generation scripts needed to reproduce the core paper artifacts for our FHE-friendly GPT-2 study.

## What This Artifact Reproduces

Running the reproduction pipeline regenerates:

- `figures/gpt2_fhe_task_bucket_latency_small_medium_large.pdf`
- `figures/icml25_fig2_ours_component_breakdown_small.pdf`
- `figures/sequence_length_scalability_comparison_small.pdf`
- `figures/freqgpt_ablation_small_arch_latency.pdf`
- `figures/freqgpt_ablation_small_kd_accuracy.pdf`
- `tables/main_accuracy.tex`
- `tables/freqgpt_approx_params.tex`
- `tables/freqgpt_depth_cts_small.tex`

The generated figures and tables are rebuilt from validated result snapshots exported from the formal experiment runs. This keeps artifact reproduction lightweight and deterministic for reviewers.

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
- `scripts/`: figure and table reproduction scripts
- `src/`: public reference implementation snippets with sanitized `FreqMixer` terminology
- `docs/`: Open Science URL template and artifact notes
- `figures/`: regenerated paper figures
- `tables/`: regenerated paper tables

## Notes

- The public artifact uses the name `FreqMixer` consistently for our frequency-domain mixer operator and related ablations.
- The scripts here are intentionally self-contained and rely only on `numpy` and `matplotlib`.
- Heavy OpenFHE/GPU reruns are not required for artifact evaluation; the goal of this package is deterministic reproduction of the paper figures and tables from validated result snapshots.

## Publishing

This directory is ready to be initialized as a Git repository and pushed to GitHub. The only missing step is GitHub authentication for the final `git push`.
