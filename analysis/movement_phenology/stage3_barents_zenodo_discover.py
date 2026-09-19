#!/usr/bin/env python3
"""Discover and inventory the public Zenodo processed Barnacle Goose tracking release.

Source dataset:
Boom & Kissling (2024), Data from: Making better use of tracking data...
Zenodo record 10214988 / Dryad 10.5061/dryad.zw3r228fd.

The processed file was produced from public Movebank sources with movepub and
subsampled to the first record per hour. We use it as a reproducible fallback
for Barents/Svalbard source acquisition, not as a claim of byte-identical
recovery of the original Movebank export.
"""

from __future__ import annotations

import json
from pathlib import Path
import requests
import pandas as pd

API = "https://zenodo.org/api/records/10214988"
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = {
    "barents": "10.5441/001/1.ps244r11",
    "svalbard": "10.5441/001/1.5k6b1364",
}


def main():
    r = requests.get(API, timeout=60)
    r.raise_for_status()
    rec = r.json()
    files = rec.get("files", [])
    if not files:
        raise SystemExit("Zenodo record contains no files")

    discovery = {
        "record": rec.get("id"),
        "doi": rec.get("doi"),
        "title": rec.get("metadata", {}).get("title"),
        "files": [
            {
                "key": f.get("key"),
                "size": f.get("size"),
                "checksum": f.get("checksum"),
                "download": (f.get("links") or {}).get("self"),
            }
            for f in files
        ],
    }
    (OUT / "stage3_barents_zenodo_discovery.json").write_text(
        json.dumps(discovery, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(discovery, indent=2))


if __name__ == "__main__":
    main()
