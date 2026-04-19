from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np

from plot_utils import FIGURES_DIR, RESULTS_DIR, ensure_output_dirs, set_paper_style


METHODS = [
    ("full_kd", "Full KD", "#EF8B67", "///"),
    ("no_kd", "No KD", "#F0C284", "\\\\\\"),
    ("from_scratch", "Scratch", "#F5EBAE", "..."),
]

TASKS = [
    ("social_iqa", "Social IQA\n64 tok"),
    ("piqa", "PIQA\n128 tok"),
]

INPUTS = {
    "full_kd": RESULTS_DIR / "kd_ablation_small_formal_full.json",
    "no_kd": RESULTS_DIR / "kd_ablation_small_formal_nokd.json",
    "from_scratch": RESULTS_DIR / "kd_ablation_small_formal_scratch.json",
}


def load_results() -> dict:
    data = {}
    for key, path in INPUTS.items():
        payload = json.loads(path.read_text(encoding="utf-8"))
        data[key] = payload["tasks"]
    return data


def main() -> None:
    ensure_output_dirs()
    set_paper_style(font_size=11.5, legend_size=8.8)
    data = load_results()

    x = np.arange(len(TASKS))
    width = 0.23
    center = (len(METHODS) - 1) / 2.0

    fig, ax = plt.subplots(figsize=(3.35, 1.68))

    for idx, (method_key, label, color, hatch) in enumerate(METHODS):
        offsets = x + (idx - center) * width
        values = np.array([data[method_key][task_key] for task_key, _ in TASKS])
        ax.bar(
            offsets,
            values,
            width=width,
            label=label,
            color=color,
            edgecolor="black",
            linewidth=0.9,
            hatch=hatch,
            zorder=3,
        )

    ax.set_ylabel("Accuracy")
    ax.set_xticks(x)
    ax.set_xticklabels([label for _, label in TASKS])
    max_val = max(data[method_key][task_key] for method_key, *_ in METHODS for task_key, _ in TASKS)
    ax.set_ylim(0.30, max_val + 0.07)
    ax.set_xlim(-0.5, len(TASKS) - 0.5)
    ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(
        loc="upper center",
        ncol=3,
        frameon=True,
        edgecolor="black",
        bbox_to_anchor=(0.5, 0.985),
        borderpad=0.22,
        handlelength=1.0,
        columnspacing=0.45,
        labelspacing=0.2,
    )

    fig.tight_layout(pad=0.08)
    pdf_path = FIGURES_DIR / "freqgpt_ablation_small_kd_accuracy.pdf"
    png_path = FIGURES_DIR / "freqgpt_ablation_small_kd_accuracy.png"
    fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {pdf_path}")


if __name__ == "__main__":
    main()
