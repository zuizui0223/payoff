"""Inventory the original JMA all-taxon phenology CSV archive.

Source census only: no temperature/NDVI fit and no biological effect inferred.
The original archive is downloaded in CI, hashed and read in memory; the raw
data are not committed or uploaded. CSV schema is preserved as observed.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

URL = "https://www.data.jma.go.jp/sakura/data/ruinenchi/ruinenchi_all.zip"
MAX_BYTES = 8_000_000


def classify(name: str) -> str:
    # Source event labels, not species traits inferred from dates.
    amphibians = ("あまがえる", "アマガエル", "とのさまがえる", "トノサマガエル")
    birds = ("うぐいす", "かっこう", "さしば", "つばめ", "ひばり", "もず")
    insects = ("せみ", "ぜみ", "セミ", "ゼミ", "こおろぎ", "とんぼ", "ほたる", "ちょう", "チョウ", "あきあかね", "きあげは", "アブラ", "あぶら")
    if any(s in name for s in amphibians):
        return "amphibian"
    if any(s in name for s in birds):
        return "bird"
    if any(s in name for s in insects):
        return "insect"
    return "plant_or_unclassified"


def summarize_zip(raw: bytes) -> dict:
    if len(raw) > MAX_BYTES:
        raise ValueError("Archive exceeds safety bound")
    results = []
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        members = [x for x in z.infolist() if not x.is_dir()]
        if len(members) > 200:
            raise ValueError("Unexpected archive member count")
        for member in members:
            if member.file_size > 3_000_000 or member.file_size < 0:
                raise ValueError("Unexpected CSV member size")
            if not member.filename.lower().endswith(".csv"):
                continue
            payload = z.read(member)
            decoded = None
            encoding = None
            for enc in ("cp932", "utf-8-sig", "shift_jis"):
                try:
                    decoded = payload.decode(enc)
                    encoding = enc
                    break
                except UnicodeDecodeError:
                    continue
            if decoded is None:
                raise ValueError("Unknown CSV encoding")
            rows = list(csv.reader(io.StringIO(decoded)))
            nonempty = [r for r in rows if any(v.strip() for v in r)]
            first = nonempty[:3]
            results.append({
                "filename": member.filename,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "encoding": encoding,
                "row_count_including_headers": len(rows),
                "first_three_rows_first_12_cells": [r[:12] for r in first],
                "source_taxon_guess": classify(member.filename),
                "header_only_no_biological_fit": True,
            })
    return {
        "source": URL,
        "archive_sha256": hashlib.sha256(raw).hexdigest(),
        "archive_bytes": len(raw),
        "csv_file_count": len(results),
        "source_taxon_filename_class_counts": dict(Counter(x["source_taxon_guess"] for x in results)),
        "files": results,
        "note": "Counts are source-file inventory, not number of biological observations. Filename taxonomy is provisional. 2021 JMA animal observation cessation must be modelled as an observation-protocol change.",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    request = urllib.request.Request(URL, headers={"User-Agent": "PAYOFF-B-research-source-inventory/1.0"})
    with urllib.request.urlopen(request, timeout=60) as resp:
        raw = resp.read(MAX_BYTES + 1)
    result = summarize_zip(raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"csv_file_count": result["csv_file_count"], "archive_sha256": result["archive_sha256"], "source_taxon_filename_class_counts": result["source_taxon_filename_class_counts"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
