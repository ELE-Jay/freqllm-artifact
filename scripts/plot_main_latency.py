from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np

from plot_utils import COLORS, FIGURES_DIR, HATCHES, RESULTS_DIR, ensure_output_dirs, set_paper_style


VARIANTS = ["small", "medium", "large"]
BUCKETS = [
    (32, "32 tok\nSST2/WiC"),
    (64, "64 tok\nARC/SIQA/MNLI"),
    (128, "128 tok\nPIQA/HS/ANLI"),
]


def load_data() -> dict:
    path = RESULTS_DIR / "gpt2_gpu_latency_summary.json"
    return json.loads(path.read_text(encoding="utf-8"))


def bucket_value(variant_data: dict, seq_len: int, method: str) -> float:
    for task_data in variant_data.values():
        if task_data["seq_len"] == seq_len:
            return task_data[method]
    raise KeyError(seq_len)


def main() -> None:
    ensure_output_dirs()
    set_paper_style(font_size=10.5, legend_size=10.0)
    data = load_data()

    fig, axes = plt.subplots(1, 3, figsize=(14.4, 4.6), sharey=True)
    width = 0.25

    for ax, variant in zip(axes, VARIANTS):
        variant_data = data["fhe_task_bucket"][variant]
        x = np.arange(len(BUCKETS))
        encrypted = [bucket_value(variant_data, seq_len, "encryptedllm") for seq_len, _ in BUCKETS]
        poly = [bucket_value(variant_data, seq_len, "polytransformer") for seq_len, _ in BUCKETS]
        ours = [bucket_value(variant_data, seq_len, "freqgpt") for seq_len, _ in BUCKETS]

        ax.bar(
            x - width,
            encrypted,
            width,
            label="EncryptedLLM",
            color=COLORS["encryptedllm"],
            edgecolor="black",
            linewidth=0.9,
            hatch=HATCHES["encryptedllm"],
            zorder=3,
        )
        ax.bar(
            x,
            poly,
            width,
            label="PolyTransformer",
            color=COLORS["polytransformer"],
            edgecolor="black",
            linewidth=0.9,
            hatch=HATCHES["polytransformer"],
            zorder=3,
        )
        ax.bar(
            x + width,
            ours,
            width,
            label="FreqGPT",
            color=COLORS["freqgpt"],
            edgecolor="black",
            linewidth=0.9,
            hatch=HATCHES["freqgpt"],
            zorder=3,
        )

        ax.set_title(f"GPT-2 {variant.capitalize()}")
        ax.set_xticks(x)
        ax.set_xticklabels([label for _, label in BUCKETS])
        ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[0].set_ylabel("FHE Latency (s)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncols=3, frameon=True, edgecolor="black", bbox_to_anchor=(0.5, 1.04))
    fig.tight_layout(rect=(0, 0, 1, 0.95))

    pdf_path = FIGURES_DIR / "gpt2_fhe_task_bucket_latency_small_medium_large.pdf"
    png_path = FIGURES_DIR / "gpt2_fhe_task_bucket_latency_small_medium_large.png"
    fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {pdf_path}")


if __name__ == "__main__":
    main()
