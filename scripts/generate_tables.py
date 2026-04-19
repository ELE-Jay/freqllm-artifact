from __future__ import annotations

import json

from plot_utils import RESULTS_DIR, TABLES_DIR, ensure_output_dirs


TASK_ORDER = [
    ("sst2", "SST2"),
    ("wic", "WiC"),
    ("piqa", "PIQA"),
    ("arc_easy", "ARC-E"),
    ("social_iqa", "SIQA"),
    ("mnli", "MNLI"),
    ("hellaswag", "HellaSwag"),
    ("anli_r1", "ANLI-R1"),
]

METHOD_LABELS = {
    "baseline": "Plaintext GPT-2",
    "polytransformer": "PolyTransformer",
    "encryptedllm": "EncryptedLLM",
    "freqgpt": "FreqGPT",
}

APPROX_PARAMS = {
    "Small": [
        ("EncryptedLLM", "LN Newton = 16, exp $r$ = 7, Goldschmidt = 14"),
        ("PolyTransformer", "InvSqrt deg. = 7, Sigma / GeLU deg. = 7 / 7"),
        ("FreqGPT", "PolyNorm deg. = 2, FreqMixer order = 2, FFT-Linear = yes, Softmax / Division = removed"),
    ],
    "Medium": [
        ("EncryptedLLM", "LN Newton = 18, exp $r$ = 7, Goldschmidt = 18"),
        ("PolyTransformer", "InvSqrt deg. = 7, Sigma / GeLU deg. = 7 / 7"),
        ("FreqGPT", "PolyNorm deg. = 2, FreqMixer order = 2, FFT-Linear = yes, Softmax / Division = removed"),
    ],
    "Large": [
        ("EncryptedLLM", "LN Newton = 18, exp $r$ = 7, Goldschmidt = 22"),
        ("PolyTransformer", "InvSqrt deg. = 7, Sigma / GeLU deg. = 7 / 7"),
        ("FreqGPT", "PolyNorm deg. = 2, FreqMixer order = 2, FFT-Linear = yes, Softmax / Division = removed"),
    ],
}

OPERATOR_PROFILE_SMALL = [
    ("EncryptedLLM", "depth", [13, 22, 0, 17]),
    ("EncryptedLLM", "\\# of cts", [3, 6, 12, 12]),
    ("PolyTransformer", "depth", [9, 9, 0, 7]),
    ("PolyTransformer", "\\# of cts", [3, 6, 12, 12]),
    ("FreqGPT", "depth", [3, 2, 0, 3]),
    ("FreqGPT", "\\# of cts", [3, 3, 3, 3]),
]


def load_accuracy(variant: str) -> dict:
    path = RESULTS_DIR / f"gpt2_gpu_8task_compare_{variant}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def fmt_score(value: float) -> str:
    return f"{value:.3f}"


def maybe_bold(text: str, enabled: bool) -> str:
    return rf"\textbf{{{text}}}" if enabled else text


def write_text(path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    print(f"Saved: {path}")


def generate_main_accuracy() -> None:
    ensure_output_dirs()
    variants = [("small", "Small"), ("medium", "Medium"), ("large", "Large")]
    tex_lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Eight-task utility under the unified GPT-2/GPU evaluation setting. Higher is better. Plaintext GPT-2 is included only as a utility reference; the secure comparisons are among EncryptedLLM, PolyTransformer, and FreqGPT.}",
        r"\label{tab:main-accuracy}",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{l l c c c c c c c c c}",
        r"\toprule",
        r"Scale & Method & SST2 & WiC & PIQA & ARC-E & SIQA & MNLI & HellaSwag & ANLI-R1 & Avg. \\",
        r"\midrule",
    ]
    md_lines = [
        "# Main Accuracy Table",
        "",
        "| Scale | Method | SST2 | WiC | PIQA | ARC-E | SIQA | MNLI | HellaSwag | ANLI-R1 | Avg. |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    methods = ["baseline", "polytransformer", "encryptedllm", "freqgpt"]
    for variant_key, variant_label in variants:
        data = load_accuracy(variant_key)
        best_by_column = {}
        for task_key, _ in TASK_ORDER:
            best_by_column[task_key] = max(data[method][task_key] for method in methods)
        best_by_column["average"] = max(data[method]["average"] for method in methods)
        for idx, method in enumerate(methods):
            scores = [
                maybe_bold(fmt_score(data[method][task_key]), data[method][task_key] == best_by_column[task_key])
                for task_key, _ in TASK_ORDER
            ]
            avg = maybe_bold(fmt_score(data[method]["average"]), data[method]["average"] == best_by_column["average"])
            row_scale = variant_label if idx == 0 else ""
            row_method = METHOD_LABELS[method]
            tex_lines.append(
                f"{row_scale} & {row_method} & " + " & ".join(scores + [avg]) + r" \\"
            )
            md_lines.append(
                f"| {row_scale or ' '} | {row_method} | " + " | ".join(scores + [avg]) + " |"
            )
        tex_lines.append(r"\midrule")

    tex_lines.pop()
    tex_lines.extend([r"\bottomrule", r"\end{tabular}%", r"}", r"\end{table*}"])
    write_text(TABLES_DIR / "main_accuracy.tex", "\n".join(tex_lines) + "\n")
    write_text(TABLES_DIR / "main_accuracy.md", "\n".join(md_lines) + "\n")


def generate_approx_params() -> None:
    tex_lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{ICML'25-style approximation parameters adapted to our setting. We explicitly separate the approximation recipe of each secure baseline so that the reader can distinguish which parameters belong to EncryptedLLM, PolyTransformer, and FreqGPT. We omit plaintext GPT-2 because these parameters are specific to encrypted approximation circuits.}",
        r"\label{tab:freqgpt-approx-params}",
        r"\resizebox{\columnwidth}{!}{%",
        r"\begin{tabular}{l l p{7.2cm}}",
        r"\toprule",
        r"Scale & Method & Approximation / architectural parameters \\",
        r"\midrule",
    ]
    md_lines = [
        "# Approximation Parameter Table",
        "",
        "| Scale | Method | Approximation / architectural parameters |",
        "|---|---|---|",
    ]
    for scale, rows in APPROX_PARAMS.items():
        for method, text in rows:
            tex_lines.append(f"{scale} & {method} & {text} \\\\")
            md_lines.append(f"| {scale} | {method} | {text.replace('$', '')} |")
        tex_lines.append(r"\midrule")
    tex_lines.pop()
    tex_lines.extend([r"\bottomrule", r"\end{tabular}%", r"}", r"\end{table}"])
    write_text(TABLES_DIR / "freqgpt_approx_params.tex", "\n".join(tex_lines) + "\n")
    write_text(TABLES_DIR / "freqgpt_approx_params.md", "\n".join(md_lines) + "\n")


def generate_operator_profile_small() -> None:
    headers = ["Normalization", "Attention / Mixer", "Dense / MLP", "Activation"]
    tex_lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{ICML'25-style operator profile for GPT-2 Small at token position 128. For each method, the first row reports multiplicative depth and the second row reports the number of working ciphertexts under our current OpenFHE-GPU slot configuration ($n=32768$ slots).}",
        r"\label{tab:freqgpt-depth-cts-small}",
        r"\resizebox{\columnwidth}{!}{%",
        r"\begin{tabular}{l l c c c c}",
        r"\toprule",
        "Method & Statistic & " + " & ".join(headers) + r" \\",
        r"\midrule",
    ]
    md_lines = [
        "# Operator Profile Table (Small, Token 128)",
        "",
        "| Method | Statistic | " + " | ".join(headers) + " |",
        "|---|---|" + "---:|" * len(headers),
    ]
    for method, statistic, values in OPERATOR_PROFILE_SMALL:
        tex_lines.append(f"{method} & {statistic} & " + " & ".join(str(v) for v in values) + r" \\")
        md_lines.append(f"| {method} | {statistic.replace('\\\\#', '#')} | " + " | ".join(str(v) for v in values) + " |")
        if statistic == "\\# of cts" and method != "FreqGPT":
            tex_lines.append(r"\midrule")
    tex_lines.extend([r"\bottomrule", r"\end{tabular}%", r"}", r"\end{table}"])
    write_text(TABLES_DIR / "freqgpt_depth_cts_small.tex", "\n".join(tex_lines) + "\n")
    write_text(TABLES_DIR / "freqgpt_depth_cts_small.md", "\n".join(md_lines) + "\n")


def main() -> None:
    generate_main_accuracy()
    generate_approx_params()
    generate_operator_profile_small()


if __name__ == "__main__":
    main()
