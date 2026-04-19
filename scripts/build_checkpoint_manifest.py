from __future__ import annotations

import hashlib
import json
from pathlib import Path


ARTIFACT_ROOT = Path(__file__).resolve().parents[1]
CHECKPOINTS_DIR = ARTIFACT_ROOT / "checkpoints"

CHECKPOINTS = [
    "gpt2_baseline_kd_small.pth",
    "gpt2_baseline_kd_medium.pth",
    "gpt2_baseline_kd_large.pth",
    "freqgpt_polynorm_kd_small_calibrated.pth",
    "freqgpt_polynorm_kd_medium_calibrated.pth",
    "freqgpt_polynorm_kd_large_calibrated.pth",
    "polytransformer_paper_small.pth",
    "polytransformer_paper_medium.pth",
    "polytransformer_paper_large.pth",
    "freqgpt_ablation_formal_full_kd_small.pth",
    "freqgpt_ablation_formal_no_kd_small.pth",
    "freqgpt_ablation_formal_from_scratch_small.pth",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def human_size(num_bytes: int) -> str:
    gib = num_bytes / (1024 ** 3)
    mib = num_bytes / (1024 ** 2)
    if gib >= 1.0:
        return f"{gib:.2f} GiB"
    return f"{mib:.0f} MiB"


def main() -> None:
    manifest = {}
    md_lines = [
        "# Generated Checkpoint Manifest",
        "",
        "| File | Size | SHA-256 |",
        "|---|---:|---|",
    ]
    for filename in CHECKPOINTS:
        path = CHECKPOINTS_DIR / filename
        if not path.exists():
            print(f"[missing] {path}")
            continue
        size_bytes = path.stat().st_size
        sha256 = sha256_file(path)
        manifest[filename] = {
            "size_bytes": size_bytes,
            "size_human": human_size(size_bytes),
            "sha256": sha256,
            "path": str(path),
        }
        md_lines.append(f"| `{filename}` | {human_size(size_bytes)} | `{sha256}` |")
        print(f"[ok] {filename} {human_size(size_bytes)}")

    json_path = CHECKPOINTS_DIR / "checkpoint_manifest.generated.json"
    md_path = CHECKPOINTS_DIR / "checkpoint_manifest.generated.md"
    json_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"[saved] {json_path}")
    print(f"[saved] {md_path}")


if __name__ == "__main__":
    main()
