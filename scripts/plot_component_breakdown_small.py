from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np

from plot_utils import FIGURES_DIR, RESULTS_DIR, ensure_output_dirs, set_paper_style


METHODS = [
    ("baseline", "EncryptedLLM", "#9BBBE1", "\\\\\\"),
    ("polytransformer", "PolyTransformer", "#B7B7EB", "xx"),
    ("freqgpt", "FreqGPT", "#F09BA0", "..."),
]

COMPONENTS = [
    ("norm", "Norm", "#F6E2C1", ""),
    ("attention", "Attention", "#F3DBC1", "//"),
    ("dense", "Dense", "#D6E2E2", "\\\\"),
    ("gelu", "GeLU", "#B2B6C1", "xx"),
    ("bootstrap", "Bootstrap", "#F0EFED", ".."),
]


def load_variant_data() -> dict:
    path = RESULTS_DIR / "icml25_fig2_breakdown_data.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["small"]


def plot_component_grouped(ax, variant_result: dict) -> None:
    x = np.arange(len(COMPONENTS))
    width = 0.24
    for idx, (method_key, method_name, color, hatch) in enumerate(METHODS):
        values = [variant_result[method_key][comp_key] for comp_key, *_ in COMPONENTS]
        ax.bar(
            x + (idx - 1) * width,
            values,
            width=width,
            color=color,
            edgecolor="black",
            linewidth=0.9,
            hatch=hatch,
            label=method_name,
            zorder=3,
        )
    ax.set_xticks(x)
    ax.set_xticklabels([label for _, label, _, _ in COMPONENTS], rotation=20)
    ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)
    ax.set_axisbelow(True)


def plot_total_stacked(ax, variant_result: dict) -> None:
    x = np.arange(len(METHODS))
    bottoms = np.zeros(len(METHODS))
    for comp_key, comp_label, color, hatch in COMPONENTS:
        values = np.array([variant_result[method_key][comp_key] for method_key, *_ in METHODS])
        ax.bar(
            x,
            values,
            bottom=bottoms,
            width=0.62,
            color=color,
            edgecolor="black",
            linewidth=0.9,
            hatch=hatch,
            label=comp_label,
            zorder=3,
        )
        bottoms += values
    ax.set_xticks(x)
    ax.set_xticklabels([name for _, name, _, _ in METHODS], rotation=10)
    ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)
    ax.set_axisbelow(True)


def main() -> None:
    ensure_output_dirs()
    set_paper_style(font_size=11.0, legend_size=9.0)
    variant_data = load_variant_data()

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.3), gridspec_kw={"width_ratios": [1.45, 1.0]})
    plot_component_grouped(axes[0], variant_data)
    plot_total_stacked(axes[1], variant_data)
    axes[0].set_ylabel("Latency per Transformer Block (s)")
    axes[0].legend(loc="upper right", frameon=True, edgecolor="black", title="Methods")
    axes[1].legend(loc="upper right", frameon=True, edgecolor="black", title="Components")
    fig.tight_layout()

    pdf_path = FIGURES_DIR / "icml25_fig2_ours_component_breakdown_small.pdf"
    png_path = FIGURES_DIR / "icml25_fig2_ours_component_breakdown_small.png"
    fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {pdf_path}")


if __name__ == "__main__":
    main()
