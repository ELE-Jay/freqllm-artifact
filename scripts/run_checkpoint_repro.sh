#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARTIFACT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CODE_ROOT=""
CHECKPOINTS_DIR="$ARTIFACT_ROOT/checkpoints"
PYTHON_BIN="${PYTHON_BIN:-python}"
VARIANTS="small,medium,large"
TASKS="sst2,wic,piqa,arc_easy,social_iqa,mnli,hellaswag,anli_r1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --code-root)
      CODE_ROOT="$2"
      shift 2
      ;;
    --checkpoints-root)
      CHECKPOINTS_DIR="$2"
      shift 2
      ;;
    --python)
      PYTHON_BIN="$2"
      shift 2
      ;;
    --variants)
      VARIANTS="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$CODE_ROOT" ]]; then
  echo "--code-root is required" >&2
  exit 1
fi

if [[ ! -f "$CODE_ROOT/compare_gpt2_gpu_methods.py" ]]; then
  echo "Invalid --code-root: $CODE_ROOT" >&2
  exit 1
fi

bash "$SCRIPT_DIR/link_checkpoints_into_codebase.sh" --code-root "$CODE_ROOT" --checkpoints-root "$CHECKPOINTS_DIR"

IFS=',' read -r -a VARIANT_LIST <<< "$VARIANTS"

for variant in "${VARIANT_LIST[@]}"; do
  echo "[checkpoint-repro] accuracy $variant"
  "$PYTHON_BIN" "$CODE_ROOT/compare_gpt2_gpu_methods.py" \
    --variant "$variant" \
    --tasks "$TASKS" \
    --output "$CODE_ROOT/gpt2_gpu_8task_compare_${variant}.json"

  echo "[checkpoint-repro] latency $variant"
  "$PYTHON_BIN" "$CODE_ROOT/latency_benchmark_alltasks.py" \
    --variant "$variant" \
    > "$CODE_ROOT/log_latency_benchmark_alltasks_${variant}_paper_polytransformer.txt"
done

echo "[checkpoint-repro] latency summary"
"$PYTHON_BIN" "$CODE_ROOT/build_gpt2_latency_summary_from_logs.py"

echo "[checkpoint-repro] small sequence scalability"
"$PYTHON_BIN" "$CODE_ROOT/plot_sequence_length_scalability.py" --variant small

echo "[checkpoint-repro] small architecture ablation latency"
"$PYTHON_BIN" "$CODE_ROOT/freqgpt_ablation_latency.py" \
  --variant small \
  --seq-lens 64 128 \
  --output-prefix freqgpt_ablation_latency_formal_small_64_128

echo "[checkpoint-repro] small KD ablation evaluation"
"$PYTHON_BIN" "$CODE_ROOT/evaluate_freqgpt_ablation.py" \
  --variant small \
  --weights "$CODE_ROOT/freqgpt_ablation_formal_full_kd_small.pth" \
  --output-json "$CODE_ROOT/kd_ablation_small_formal_full.json"
"$PYTHON_BIN" "$CODE_ROOT/evaluate_freqgpt_ablation.py" \
  --variant small \
  --weights "$CODE_ROOT/freqgpt_ablation_formal_no_kd_small.pth" \
  --output-json "$CODE_ROOT/kd_ablation_small_formal_nokd.json"
"$PYTHON_BIN" "$CODE_ROOT/evaluate_freqgpt_ablation.py" \
  --variant small \
  --weights "$CODE_ROOT/freqgpt_ablation_formal_from_scratch_small.pth" \
  --output-json "$CODE_ROOT/kd_ablation_small_formal_scratch.json"

mkdir -p "$ARTIFACT_ROOT/results"
cp "$CODE_ROOT/gpt2_gpu_8task_compare_small.json" "$ARTIFACT_ROOT/results/"
cp "$CODE_ROOT/gpt2_gpu_8task_compare_medium.json" "$ARTIFACT_ROOT/results/"
cp "$CODE_ROOT/gpt2_gpu_8task_compare_large.json" "$ARTIFACT_ROOT/results/"
cp "$CODE_ROOT/gpt2_gpu_latency_summary.json" "$ARTIFACT_ROOT/results/"
cp "$CODE_ROOT/kd_ablation_small_formal_full.json" "$ARTIFACT_ROOT/results/"
cp "$CODE_ROOT/kd_ablation_small_formal_nokd.json" "$ARTIFACT_ROOT/results/"
cp "$CODE_ROOT/kd_ablation_small_formal_scratch.json" "$ARTIFACT_ROOT/results/"
cp "$CODE_ROOT/freqgpt_ablation_latency_formal_small_64_128_small.json" "$ARTIFACT_ROOT/results/freqgpt_ablation_latency_formal_small_64_128.json"
cp "$CODE_ROOT/sequence_length_scalability_comparison_small.pdf" "$ARTIFACT_ROOT/figures/"
cp "$CODE_ROOT/sequence_length_scalability_comparison_small.png" "$ARTIFACT_ROOT/figures/"

echo "[checkpoint-repro] redraw artifact figures and tables"
bash "$SCRIPT_DIR/reproduce_all.sh"

echo "[checkpoint-repro] completed"
