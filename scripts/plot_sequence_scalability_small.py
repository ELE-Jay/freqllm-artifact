from __future__ import annotations

import json

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from plot_utils import COLORS, FIGURES_DIR, RESULTS_DIR, ensure_output_dirs, set_paper_style


METHOD_STYLES = {
    "encryptedllm": {
        "label": "EncryptedLLM",
        "color": COLORS["encryptedllm"],
        "marker": "o",
    },
    "polytransformer": {
        "label": "PolyTransformer",
        "color": COLORS["polytransformer"],
        "marker": "^",
    },
    "freqgpt": {
        "label": "FreqGPT",
        "color": COLORS["freqgpt"],
        "marker": "s",
    },
}


def load_results() -> dict:
    path = RESULTS_DIR / "sequence_length_scalability_small.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    ensure_output_dirs()
    set_paper_style(font_size=11.0, legend_size=10.0)
    payload = load_results()
    seq_lens = payload["sequence_lengths"]

    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    for key in ("encryptedllm", "polytransformer", "freqgpt"):
        style = METHOD_STYLES[key]
        values = payload[key]
        ax.fill_between(seq_lens, values, 0, color=style["color"], alpha=0.18, linewidth=0, zorder=1)
        ax.plot(
            seq_lens,
            values,
            label=style["label"],
            color=style["color"],
            linewidth=2.4,
            marker=style["marker"],
            markersize=6.5,
            markeredgecolor="black",
            markeredgewidth=0.7,
            zorder=3,
        )
        ax.annotate(
            f"{values[-1]:.0f}",
            (seq_lens[-1], values[-1]),
            textcoords="offset points",
            xytext=(6, -2 if key == "freqgpt" else 6),
            ha="left",
            va="center",
            fontsize=9.5,
            color=style["color"],
        )

    ax.set_xlabel("Sequence Length (Tokens)")
    ax.set_ylabel("FHE Latency (s)")
    ax.set_xticks(seq_lens)
    ax.set_xlim(min(seq_lens), max(seq_lens))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.grid(axis="y", linestyle="--", linewidth=0.8, alpha=0.28)
    ax.grid(axis="x", visible=False)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    legend = ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="black")
    legend.get_frame().set_linewidth(0.9)

    fig.tight_layout()
    pdf_path = FIGURES_DIR / "sequence_length_scalability_comparison_small.pdf"
    png_path = FIGURES_DIR / "sequence_length_scalability_comparison_small.png"
    fig.savefig(pdf_path, format="pdf", bbox_inches="tight", dpi=300)
    fig.savefig(png_path, format="png", bbox_inches="tight", dpi=300)
    print(f"Saved: {pdf_path}")


if __name__ == "__main__":
    main()
