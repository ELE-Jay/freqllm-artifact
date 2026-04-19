from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np

from plot_utils import FIGURES_DIR, RESULTS_DIR, ensure_output_dirs, set_paper_style


METHODS = [
    ("full", "FreqGPT", "#7895C1", "///"),
    ("wout_polynorm", "w/o PolyNorm", "#A8CBDF", "\\\\\\"),
    ("wout_freqmixer_fft", "w/o FreqMixer/FFT", "#D6EFF4", "xx"),
    ("wout_fftlinear", "w/o FFT-Linear", "#F2FAFC", "..."),
]
SEQ_LENS = ["64", "128"]


def load_results() -> dict:
    path = RESULTS_DIR / "freqgpt_ablation_latency_formal_small_64_128.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    ensure_output_dirs()
    set_paper_style(font_size=11.5, legend_size=8.8)
    data = load_results()

    x = np.arange(len(SEQ_LENS))
    width = 0.18
    center = (len(METHODS) - 1) / 2.0

    fig, ax = plt.subplots(figsize=(3.35, 1.72))

    for idx, (method_key, label, color, hatch) in enumerate(METHODS):
        offsets = x + (idx - center) * width
        values = np.array([data["seq_lens"][seq_len]["ablations"][method_key]["latency"] for seq_len in SEQ_LENS])
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

    ax.set_ylabel("Latency (s)")
    ax.set_xticks(x)
    ax.set_xticklabels([f"Len {seq_len}" for seq_len in SEQ_LENS])
    ax.set_xlim(-0.5, len(SEQ_LENS) - 0.5)
    max_val = max(
        data["seq_lens"][seq_len]["ablations"][method_key]["latency"]
        for seq_len in SEQ_LENS
        for method_key, *_ in METHODS
    )
    ax.set_ylim(0, max_val * 1.22)
    ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(
        loc="upper center",
        ncol=2,
        frameon=True,
        edgecolor="black",
        bbox_to_anchor=(0.5, 0.985),
        borderpad=0.22,
        handlelength=1.0,
        columnspacing=0.45,
        labelspacing=0.2,
    )

    fig.tight_layout(pad=0.08)
    pdf_path = FIGURES_DIR / "freqgpt_ablation_small_arch_latency.pdf"
    png_path = FIGURES_DIR / "freqgpt_ablation_small_arch_latency.png"
    fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {pdf_path}")


if __name__ == "__main__":
    main()
