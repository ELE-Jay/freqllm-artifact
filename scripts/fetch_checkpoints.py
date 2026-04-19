from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import urllib.request
from pathlib import Path


ARTIFACT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ARTIFACT_ROOT / "checkpoints" / "checkpoint_urls.json"
DEFAULT_TEMPLATE = ARTIFACT_ROOT / "checkpoints" / "checkpoint_urls.template.json"
DEFAULT_OUTPUT = ARTIFACT_ROOT / "checkpoints"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download and verify trained checkpoints.")
    parser.add_argument("--manifest", type=str, default=str(DEFAULT_MANIFEST))
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT))
    parser.add_argument("--only", nargs="*", default=[])
    parser.add_argument("--skip-existing", action="store_true")
    return parser.parse_args()


def resolve_manifest(path_str: str) -> Path:
    path = Path(path_str)
    if path.exists():
        return path
    if path == DEFAULT_MANIFEST and DEFAULT_TEMPLATE.exists():
        raise FileNotFoundError(
            f"Missing {DEFAULT_MANIFEST.name}. Copy {DEFAULT_TEMPLATE.name} to checkpoint_urls.json and fill the real URLs first."
        )
    raise FileNotFoundError(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, target: Path) -> None:
    with urllib.request.urlopen(url) as response, target.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def main() -> None:
    args = parse_args()
    manifest_path = resolve_manifest(args.manifest)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    selected = set(args.only) if args.only else set(payload.keys())
    for filename, meta in payload.items():
        if filename not in selected:
            continue
        target = output_dir / filename
        if args.skip_existing and target.exists():
            print(f"[skip-existing] {target}")
            continue

        print(f"[download] {filename}")
        download(meta["url"], target)

        if meta.get("size_bytes"):
            actual_size = target.stat().st_size
            if actual_size != int(meta["size_bytes"]):
                raise RuntimeError(f"Size mismatch for {filename}: expected {meta['size_bytes']}, got {actual_size}")

        if meta.get("sha256"):
            actual_sha = sha256_file(target)
            if actual_sha != meta["sha256"]:
                raise RuntimeError(f"SHA-256 mismatch for {filename}: expected {meta['sha256']}, got {actual_sha}")
        print(f"[ok] {target}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[error] {exc}", file=sys.stderr)
        sys.exit(1)
