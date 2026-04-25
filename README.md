# FreqLLM CCS'26 Artifact

This repository packages the result snapshots, plotting scripts, table-generation scripts, checkpoint manifests, reference implementation, and wrapper pipelines needed to reproduce the paper artifacts for our FHE-friendly LLM study at multiple reproducibility tiers. The main comparison includes EncryptedLLM, PolyTransformer, THOR, and FreqLLM under a unified secure evaluation setting, with GPT-2 as the primary backbone and BERT-base as a supplementary encoder-side validation.

For CCS double-blind review, distribute this artifact through an anonymous host such as `https://anonymous.4open.science`. Do not submit a personal GitHub, Google Drive, self-managed website, or other trackable/non-anonymous URL.

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
- `docs/CHECKPOINT_DISTRIBUTION.md`
- `checkpoints/README.md`
- `scripts/run_checkpoint_repro.sh`
- `scripts/run_full_training_pipeline.sh`
- `scripts/make_review_archive.sh`

## Snapshot-Level Artifact Reproduction

Running the reproduction pipeline regenerates:

- `figures/gpt2_fhe_task_bucket_latency_small_medium_large.pdf`
- `figures/icml25_fig2_ours_component_breakdown_small.pdf`
- `figures/sequence_length_scalability_comparison_small.pdf`
- `figures/security_level_latency_gpt2_128tok.pdf`
- `figures/freqgpt_ablation_small_arch_latency.pdf`
- `figures/freqgpt_ablation_small_kd_accuracy.pdf`
- `figures/bert_base_fhe_task_bucket_latency.pdf`
- `figures/bert_base_component_breakdown.pdf`
- `figures/sequence_length_scalability_comparison_bert_base.pdf`
- `tables/main_accuracy.tex`
- `tables/freqllm_approx_params.tex`
- `tables/freqllm_depth_cts_small.tex`

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

- `results/`: validated experiment snapshots in JSON form, including GPT-2 main results, security-level sensitivity, and BERT-base supplementary results
- `checkpoints/`: checkpoint manifest and placement instructions
- `scripts/`: figure and table reproduction scripts
- `src/`: public reference implementation snippets with packing-aware FFT terminology
- `code/`: copied experiment scripts for checkpoint-level and full-training reproduction
- `docs/`: Open Science URL template and artifact notes
- `figures/`: regenerated paper figures
- `tables/`: regenerated paper tables

## Notes

- The public artifact uses the name `FreqLLM` for the model and `packing-aware FFT mixer` for the frequency-domain bottleneck gate operator.
- The scripts here are intentionally self-contained and rely only on `numpy` and `matplotlib`.
- Heavy OpenFHE/GPU reruns are not required for the snapshot-level artifact path. The security-level sensitivity figure is redrawn from `results/security_level_latency_results.json`; the original OpenFHE-calibrated experiment script is included as `code/security_level_latency_experiment.py`.
- Checkpoint-level and full-training reproducibility require the full OpenFHE/GPU codebase, datasets, and large checkpoint files described in `docs/REPRODUCIBILITY_TIERS.md`.
- The repository includes `scripts/fetch_checkpoints.py` and `checkpoints/checkpoint_urls.template.json` to support reproducible checkpoint distribution once anonymous checkpoint URLs are filled in.

## CCS Submission

Create a sanitized archive without `.git/` history and upload it to an anonymous CCS-allowed artifact host. Use the same anonymous URL in the paper's Open Science appendix and in the HotCRP artifact field. See `docs/OPEN_SCIENCE.md` and `docs/OPEN_SCIENCE_APPENDIX.tex`.

```bash
bash scripts/check_review_sanitization.sh
bash scripts/make_review_archive.sh
```

The archive intentionally excludes local logs, checkpoint symlinks, real `.pth`
files, and Git history. Checkpoint binaries should be uploaded separately to an
anonymous large-file host and referenced through
`checkpoints/checkpoint_urls.json`.

To stage local checkpoint files for that separate upload:

```bash
bash scripts/stage_checkpoint_uploads.sh
```

After uploading the checkpoint shards to an anonymous large-file host, finalize
the URL manifest and rebuild the anonymous archive with:

```bash
bash scripts/finalize_review_artifact.sh \
  --checkpoint-base-url <ANON_CHECKPOINT_BASE_URL>
```

See `docs/FINAL_SUBMISSION_STEPS.md` for the final submission checklist.
