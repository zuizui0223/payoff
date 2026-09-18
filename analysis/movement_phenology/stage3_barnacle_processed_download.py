#!/usr/bin/env python3
"""Download the public processed tracking release used as a reproducible
fallback for Greenland/Barents barnacle-goose reconstruction.
"""

from __future__ import annotations

import json
from pathlib import Path

import requests


API = "https://zenodo.org/api/records/10214988"
OUT = Path("external/barnacle_processed")
RECEIPT = Path("outputs/movement_phenology/stage3_barnacle_processed_download.json")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)

    r = requests.get(API, timeout=60)
    r.raise_for_status()
    rec = r.json()
    files = rec.get("files", [])
    candidates = [
        f for f in files
        if "ProcessedTrackingData" in str(f.get("key", ""))
        and str(f.get("key", "")).lower().endswith(".csv")
    ]
    if not candidates:
        raise SystemExit(
            "No ProcessedTrackingData CSV found. "
            f"Files={[f.get('key') for f in files]}"
        )
    if len(candidates) > 1:
        candidates.sort(key=lambda f: int(f.get("size", 0)), reverse=True)

    f = candidates[0]
    url = (f.get("links") or {}).get("self")
    if not url:
        raise SystemExit(f"Selected Zenodo file has no download URL: {f}")

    target = OUT / "ProcessedTrackingData_MakingBeterUseOfTrackingData_2023.csv"
    with requests.get(url, timeout=300, stream=True) as rr:
        rr.raise_for_status()
        with target.open("wb") as h:
            for chunk in rr.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    h.write(chunk)

    if target.stat().st_size == 0:
        raise SystemExit("Downloaded processed tracking file is empty")

    receipt = {
        "zenodo_record": rec.get("id"),
        "zenodo_doi": rec.get("doi"),
        "selected_key": f.get("key"),
        "selected_size": f.get("size"),
        "selected_checksum": f.get("checksum"),
        "downloaded_bytes": target.stat().st_size,
        "target": str(target),
        "claim_ceiling": (
            "Processed public tracking release used as a source-acquisition "
            "fallback; direct-controller results remain conditional on "
            "stopover and environmental reconstruction audits."
        ),
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
