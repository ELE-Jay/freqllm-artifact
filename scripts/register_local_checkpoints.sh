#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARTIFACT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CHECKPOINTS_DIR="$ARTIFACT_ROOT/checkpoints"
SOURCE_PYTHON_DIR="/root/FHE/EncryptedLLM/EncryptedLLM-repro-kit/python"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source-python-dir)
      SOURCE_PYTHON_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

mkdir -p "$CHECKPOINTS_DIR"

FILES=(
  gpt2_baseline_kd_small.pth
  gpt2_baseline_kd_medium.pth
  gpt2_baseline_kd_large.pth
  freqgpt_polynorm_kd_small_calibrated.pth
  freqgpt_polynorm_kd_medium_calibrated.pth
  freqgpt_polynorm_kd_large_calibrated.pth
  polytransformer_paper_small.pth
  polytransformer_paper_medium.pth
  polytransformer_paper_large.pth
  freqgpt_ablation_formal_full_kd_small.pth
  freqgpt_ablation_formal_no_kd_small.pth
  freqgpt_ablation_formal_from_scratch_small.pth
)

for file in "${FILES[@]}"; do
  src="$SOURCE_PYTHON_DIR/$file"
  dst="$CHECKPOINTS_DIR/$file"
  if [[ -e "$src" ]]; then
    ln -sfn "$src" "$dst"
    echo "[linked] $dst -> $src"
  else
    echo "[missing] $src" >&2
  fi
done
