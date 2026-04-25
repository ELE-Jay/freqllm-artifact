#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python "$SCRIPT_DIR/plot_main_latency.py"
python "$SCRIPT_DIR/plot_component_breakdown_small.py"
python "$SCRIPT_DIR/plot_sequence_scalability_small.py"
python "$SCRIPT_DIR/plot_security_level_latency.py"
python "$SCRIPT_DIR/plot_ablation_arch.py"
python "$SCRIPT_DIR/plot_ablation_kd.py"
python "$SCRIPT_DIR/plot_bert_latency_suite.py"
python "$SCRIPT_DIR/generate_tables.py"

echo "Artifact reproduction completed."
