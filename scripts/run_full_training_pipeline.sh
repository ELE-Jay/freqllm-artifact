#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARTIFACT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CODE_ROOT=""
CHECKPOINTS_DIR="$ARTIFACT_ROOT/checkpoints"
PYTHON_BIN="${PYTHON_BIN:-python}"
VARIANTS="small,medium,large"
RUN_SMALL_ABLATIONS="yes"

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
    --skip-small-ablations)
      RUN_SMALL_ABLATIONS="no"
      shift
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

mkdir -p "$CHECKPOINTS_DIR"
IFS=',' read -r -a VARIANT_LIST <<< "$VARIANTS"

for variant in "${VARIANT_LIST[@]}"; do
  echo "[full-train] baseline $variant"
  "$PYTHON_BIN" "$CODE_ROOT/train_gpt2_baseline_variant.py" \
    --variant "$variant" \
    --save-path "$CHECKPOINTS_DIR/gpt2_baseline_kd_${variant}.pth"

  echo "[full-train] freqgpt $variant"
  "$PYTHON_BIN" "$CODE_ROOT/train_freqgpt_variant_polynorm.py" \
    --variant "$variant" \
    --save-path "$CHECKPOINTS_DIR/freqgpt_polynorm_kd_${variant}_calibrated.pth"

  echo "[full-train] polytransformer P-stage $variant"
  "$PYTHON_BIN" "$CODE_ROOT/train_polytransformer_gpt2_variant.py" \
    --variant "$variant" \
    --stage p \
    --save-path "$CHECKPOINTS_DIR/polytransformer_paper_${variant}_p.pth"

  echo "[full-train] polytransformer RM-stage $variant"
  "$PYTHON_BIN" "$CODE_ROOT/train_polytransformer_gpt2_variant.py" \
    --variant "$variant" \
    --stage rm \
    --init-weights "$CHECKPOINTS_DIR/polytransformer_paper_${variant}_p.pth" \
    --save-path "$CHECKPOINTS_DIR/polytransformer_paper_${variant}.pth"
done

if [[ "$RUN_SMALL_ABLATIONS" == "yes" ]]; then
  echo "[full-train] small KD ablations"
  "$PYTHON_BIN" "$CODE_ROOT/train_freqgpt_kd_ablation.py" \
    --variant small \
    --mode full_kd \
    --seq-len 256 \
    --batch-size 4 \
    --epochs 1 \
    --lr 1e-5 \
    --temperature 2.0 \
    --alpha 0.5 \
    --beta-calib 0.02 \
    --max-train-batches 300 \
    --max-samples 5000 \
    --warmup-steps 50 \
    --save-path "$CHECKPOINTS_DIR/freqgpt_ablation_formal_full_kd_small.pth"

  "$PYTHON_BIN" "$CODE_ROOT/train_freqgpt_kd_ablation.py" \
    --variant small \
    --mode no_kd \
    --seq-len 256 \
    --batch-size 4 \
    --epochs 1 \
    --lr 1e-5 \
    --temperature 2.0 \
    --alpha 0.5 \
    --beta-calib 0.02 \
    --max-train-batches 300 \
    --max-samples 5000 \
    --warmup-steps 50 \
    --save-path "$CHECKPOINTS_DIR/freqgpt_ablation_formal_no_kd_small.pth"

  "$PYTHON_BIN" "$CODE_ROOT/train_freqgpt_kd_ablation.py" \
    --variant small \
    --mode from_scratch \
    --seq-len 256 \
    --batch-size 4 \
    --epochs 1 \
    --lr 1e-5 \
    --temperature 2.0 \
    --alpha 0.5 \
    --beta-calib 0.02 \
    --max-train-batches 300 \
    --max-samples 5000 \
    --warmup-steps 50 \
    --save-path "$CHECKPOINTS_DIR/freqgpt_ablation_formal_from_scratch_small.pth"
fi

echo "[full-train] invoking checkpoint-level rerun"
bash "$SCRIPT_DIR/run_checkpoint_repro.sh" \
  --code-root "$CODE_ROOT" \
  --checkpoints-root "$CHECKPOINTS_DIR" \
  --python "$PYTHON_BIN" \
  --variants "$VARIANTS"

echo "[full-train] completed"
