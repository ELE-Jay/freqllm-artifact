from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np

from plot_utils import COLORS, FIGURES_DIR, HATCHES, RESULTS_DIR, ensure_output_dirs, set_paper_style


METHODS = [
    ("encryptedllm", "EncryptedLLM", "encryptedllm"),
    ("polytransformer", "PolyTransformer", "polytransformer"),
    ("thor", "THOR", "thor"),
    ("freqllm", "FreqLLM", "freqgpt"),
]


def load_data() -> dict:
    path = RESULTS_DIR / "security_level_latency_results.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["results"]


def plot_security_level_latency(results: dict, bucket_label: str = "128 tok") -> None:
    set_paper_style(font_size=10.0, legend_size=8.0)

    variants = ["small", "medium", "large"]
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.65), sharey=False)
    width = 0.19

    for ax, variant in zip(axes, variants):
        bucket_rows = results[variant][bucket_label]["latency_by_security_level"]
        lambdas = [int(value) for value in bucket_rows.keys()]
        x = np.arange(len(lambdas))
        offsets = np.linspace(-1.5 * width, 1.5 * width, len(METHODS))

        for offset, (method_key, label, style_key) in zip(offsets, METHODS):
            values = [bucket_rows[str(lambda_bits)][method_key] for lambda_bits in lambdas]
            ax.bar(
                x + offset,
                values,
                width=width,
                label=label,
                color=COLORS[style_key],
                edgecolor="black",
                linewidth=0.9,
                hatch=HATCHES[style_key],
                zorder=3,
            )

        y_max = max(
            bucket_rows[str(lambda_bits)][method_key]
            for lambda_bits in lambdas
            for method_key, _, _ in METHODS
        )
        ax.set_ylim(0, y_max * 1.18)
        ax.set_title(f"GPT-2 {variant.capitalize()}")
        ax.set_xlabel(r"Security level $\lambda$")
        ax.set_xticks(x)
        ax.set_xticklabels([str(lambda_bits) for lambda_bits in lambdas])
        ax.grid(axis="y", linestyle="--", linewidth=0.45, alpha=0.45, zorder=0)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[0].set_ylabel("Encrypted latency (s)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.05),
        ncols=4,
        frameon=True,
        edgecolor="black",
        handlelength=1.35,
        columnspacing=0.9,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.9), w_pad=1.0)

    pdf_path = FIGURES_DIR / "security_level_latency_gpt2_128tok.pdf"
    png_path = FIGURES_DIR / "security_level_latency_gpt2_128tok.png"
    fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {pdf_path}")
    print(f"Saved: {png_path}")


def main() -> None:
    ensure_output_dirs()
    plot_security_level_latency(load_data())


if __name__ == "__main__":
    main()
