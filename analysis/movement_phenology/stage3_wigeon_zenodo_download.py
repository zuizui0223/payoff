#!/usr/bin/env python3
"""Robustly download the public Zenodo hourly dabbling-duck release.

The human-facing /records/.../files/... URL can intermittently return 504 from
GitHub-hosted runners. This downloader resolves the file through the Zenodo
record API and streams the API-provided file link with retries.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import time

import requests


RECORD_API = "https://zenodo.org/api/records/16940654"
TARGET_KEY = "250823_LNU_dabbling_ducks_hourly.csv"
OUT = Path("external/wigeon") / TARGET_KEY
RECEIPT = Path("outputs/movement_phenology/stage3_wigeon_zenodo_download.json")
UA = {"User-Agent": "payoff-wigeon-reanalysis/1.0"}


def get_json(url: str, attempts: int = 5):
    last = None
    for i in range(attempts):
        try:
            r = requests.get(url, headers=UA, timeout=60)
            r.raise_for_status()
            return r.json()
        except Exception as exc:
            last = exc
            if i + 1 < attempts:
                time.sleep(2 ** i)
    raise RuntimeError(f"Zenodo metadata GET failed: {last}")


def stream_download(url: str, target: Path, attempts: int = 5):
    last = None
    for i in range(attempts):
        try:
            with requests.get(
                url,
                headers=UA,
                timeout=(30, 300),
                stream=True,
                allow_redirects=True,
            ) as r:
                r.raise_for_status()
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("wb") as h:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            h.write(chunk)
            if target.exists() and target.stat().st_size > 0:
                return
            raise RuntimeError("download completed but target is empty")
        except Exception as exc:
            last = exc
            try:
                target.unlink(missing_ok=True)
            except Exception:
                pass
            if i + 1 < attempts:
                time.sleep(3 * (i + 1))
    raise RuntimeError(f"Zenodo file download failed: {last}")


def main():
    metadata_error = None
    try:
        rec = get_json(RECORD_API)
    except Exception as exc:
        rec = {}
        metadata_error = f"{type(exc).__name__}: {exc}"

    files = rec.get("files", [])
    matches = [f for f in files if f.get("key") == TARGET_KEY]
    f = matches[0] if len(matches) == 1 else {}
    links = f.get("links") or {}

    # The record API can intermittently return 504 from GitHub runners even
    # while the file object itself remains available. Never make metadata a
    # single point of failure for a public, frozen file.
    candidates = [
        links.get("content"),
        links.get("self"),
        f"https://zenodo.org/api/records/16940654/files/{TARGET_KEY}/content",
        f"https://zenodo.org/records/16940654/files/{TARGET_KEY}?download=1",
    ]
    candidates = list(dict.fromkeys(x for x in candidates if x))

    errors = []
    for url in candidates:
        try:
            stream_download(url, OUT, attempts=3)
            chosen = url
            break
        except Exception as exc:
            errors.append(f"{url}: {type(exc).__name__}: {exc}")
    else:
        raise SystemExit("All Zenodo API download routes failed: " + " | ".join(errors))

    sha = hashlib.sha256()
    with OUT.open("rb") as h:
        for chunk in iter(lambda: h.read(1024 * 1024), b""):
            sha.update(chunk)

    receipt = {
        "record_id": rec.get("id", 16940654),
        "record_doi": rec.get("doi", "10.5281/zenodo.16940654"),
        "file_key": TARGET_KEY,
        "metadata_error_if_any": metadata_error,
        "metadata_match_count": len(matches),
        "declared_size": f.get("size"),
        "declared_checksum": f.get("checksum"),
        "downloaded_bytes": OUT.stat().st_size,
        "sha256": sha.hexdigest(),
        "chosen_url": chosen,
        "failed_routes": errors,
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
