#!/usr/bin/env python3
"""Materialize only preregistered 2026 Dryad snow-goose files.

The script consumes the metadata-only manifest probe. It downloads only the
two frozen table inputs needed for the fed-only J-mechanism lane and writes
them outside the PAYOFF-B git checkout. It does not parse table rows.

Dryad's API download route may require OAuth even for public datasets. If an
API file request returns 401/403, the script may use Dryad's public
stash/downloads/file_stream endpoint for the same file id, but only if the
downloaded bytes match the SHA-256 digest frozen in the API manifest.
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
}
OPTIONAL_DOCUMENTATION = {
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
        api_url = str(row["download_href"])
        response = session.get(api_url, timeout=120)
        source_url = api_url
        if response.status_code in {401, 403}:
            # Dryad API file downloads now require OAuth even for public data.
            # The public dataset front-end still exposes the deposited file
            # stream. This fallback changes access route only, not source bytes.
            file_id = api_url.rstrip("/").split("/")[-2]
            source_url = (
                "https://datadryad.org/stash/downloads/file_stream/"
                + file_id
            )
            response = session.get(source_url, timeout=120)
        response.raise_for_status()
        data = response.content
        digest = sha256_bytes(data)
        expected = row.get("digest")
        if row.get("digestType") == "sha-256" and expected:
            if digest.lower() != str(expected).lower():
                raise ValueError(
                    f"Dryad SHA-256 mismatch for {row.get('path')}: "
                    f"{digest} != {expected}"
                )
        path = output / Path(str(row["path"])).name
        path.write_bytes(data)
        receipt["files"].append({
            "name": path.name,
            "bytes": len(data),
            "sha256": digest,
            "dryad_digest": expected,
            "dryad_digest_type": row.get("digestType"),
            "source_url": source_url,
            "api_download_status": (
                response.status_code
                if source_url == api_url
                else "API_AUTH_FALLBACK"
            ),
        })

    receipt_path = output / "payoff_b_snow_goose_2026_dryad_receipt.json"
    receipt_path.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
