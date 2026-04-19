from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


ARTIFACT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ARTIFACT_ROOT / "results"
FIGURES_DIR = ARTIFACT_ROOT / "figures"
TABLES_DIR = ARTIFACT_ROOT / "tables"

COLORS = {
    "encryptedllm": "#9BBBE1",
    "polytransformer": "#B7B7EB",
    "freqgpt": "#F09BA0",
}

HATCHES = {
    "encryptedllm": "\\\\\\",
    "polytransformer": "xx",
    "freqgpt": "...",
}


def set_paper_style(font_size: float = 11.0, legend_size: float = 9.0) -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": font_size,
            "axes.labelsize": font_size + 1.0,
            "axes.titlesize": font_size + 1.5,
            "legend.fontsize": legend_size,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def ensure_output_dirs() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    TABLES_DIR.mkdir(exist_ok=True)
