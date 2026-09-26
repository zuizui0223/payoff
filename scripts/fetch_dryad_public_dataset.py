#!/usr/bin/env python3
"""Fetch one public Dryad dataset through the documented v2 API."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import urllib.parse
import zipfile
from pathlib import Path

import requests


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--doi", required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--summary-output", type=Path, required=True)
    return p.parse_args()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)

    identifier = args.doi
    if not identifier.startswith("doi:"):
        identifier = "doi:" + identifier
    encoded = urllib.parse.quote(identifier, safe="")
    url = f"https://datadryad.org/api/v2/datasets/{encoded}/download"

    response = requests.get(
        url,
        timeout=120,
        allow_redirects=True,
        headers={
            "Accept": "application/zip, application/octet-stream",
            "User-Agent": "PAYOFF-B-public-dryad-fetch/1.0",
        },
    )
    response.raise_for_status()

    zip_path = args.output_dir / "dataset.zip"
    zip_path.write_bytes(response.content)
    if not zipfile.is_zipfile(zip_path):
        raise RuntimeError(
            f"Dryad download is not a zip archive: {response.headers.get('content-type')}"
        )

    extracted = args.output_dir / "extracted"
    if extracted.exists():
        shutil.rmtree(extracted)
    extracted.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(extracted)

    files = []
    for path in sorted(p for p in extracted.rglob("*") if p.is_file()):
        relative = path.relative_to(extracted).as_posix()
        files.append(
            {
                "path": relative,
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    result = {
        "doi": identifier,
        "download_url": url,
        "archive_sha256": sha256(zip_path),
        "archive_size_bytes": zip_path.stat().st_size,
        "files": files,
    }
    args.summary_output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
