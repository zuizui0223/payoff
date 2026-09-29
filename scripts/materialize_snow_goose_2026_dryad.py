#!/usr/bin/env python3
"""Materialize only preregistered 2026 Dryad snow-goose files.

The script consumes the metadata-only manifest probe. It downloads only the
three frozen source files needed for the fed-only J-mechanism lane and writes
them outside the PAYOFF-B git checkout. It does not parse table rows.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "data_exp_Feb2025.txt",
    "cond2009_July2024.txt",
    "CortFitness_April2025_clean2.R",
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    return p.parse_args()


def ensure_outside_repo(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(REPO_ROOT.resolve())
    except ValueError:
        return resolved
    raise ValueError("output directory must be outside the PAYOFF-B repository")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def select_required_files(manifest: dict) -> list[dict]:
    if manifest.get("classification") != "PUBLIC_J_MECHANISM_SOURCE_READY":
        raise ValueError("manifest is not PUBLIC_J_MECHANISM_SOURCE_READY")
    rows = manifest.get("files")
    if not isinstance(rows, list):
        raise ValueError("manifest files must be a list")

    by_name = {
        str(row.get("path")): row
        for row in rows
        if isinstance(row, dict) and row.get("path") is not None
    }
    missing = sorted(REQUIRED - set(by_name))
    if missing:
        raise ValueError("required Dryad files missing: " + ",".join(missing))

    selected = [by_name[name] for name in sorted(REQUIRED)]
    for row in selected:
        if not row.get("download_href"):
            raise ValueError(f"missing download_href for {row.get('path')}")
    return selected


def main():
    args = parse_args()
    try:
        import requests
    except ImportError as exc:
        raise RuntimeError("install requests before materializing Dryad data") from exc

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    selected = select_required_files(manifest)
    output = ensure_outside_repo(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    receipt = {
        "materialization_id": "payoff_b_snow_goose_2026_dryad_j_source_v1",
        "source_probe_id": manifest.get("probe_id"),
        "rows_opened": False,
        "files": [],
    }

    session = requests.Session()
    session.headers.update({
        "User-Agent": "PAYOFF-B-2026-Dryad-materializer/1.0",
    })

    for row in selected:
        response = session.get(row["download_href"], timeout=120)
        response.raise_for_status()
        data = response.content
        path = output / Path(str(row["path"])).name
        path.write_bytes(data)
        receipt["files"].append({
            "name": path.name,
            "bytes": len(data),
            "sha256": sha256_bytes(data),
            "dryad_digest": row.get("digest"),
            "dryad_digest_type": row.get("digestType"),
        })

    receipt_path = output / "payoff_b_snow_goose_2026_dryad_receipt.json"
    receipt_path.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
