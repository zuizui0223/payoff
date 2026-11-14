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
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

URL = "https://www.data.jma.go.jp/sakura/data/ruinenchi/ruinenchi_all.zip"
MAX_BYTES = 8_000_000
INDEX_URL = "https://www.data.jma.go.jp/sakura/data/download_ruinenchi.html"


class _JmaLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.href = None
        self.links = {}

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.href = dict(attrs).get("href")

    def handle_data(self, data):
        if self.href and self.href.endswith(".csv") and data.strip():
            self.links[urlparse(urljoin(INDEX_URL, self.href)).path.rsplit("/", 1)[-1]] = data.strip().lstrip("★")

    def handle_endtag(self, tag):
        if tag == "a":
            self.href = None


def parse_index_labels(html: str) -> dict:
    parser = _JmaLinkParser()
    parser.feed(html)
    return parser.links



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


def summarize_zip(raw: bytes, labels: dict | None = None) -> dict:
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
            basename = member.filename.rsplit("/", 1)[-1]
            label = (labels or {}).get(basename)
            results.append({
                "filename": member.filename,
                "official_event_label": label,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "encoding": encoding,
                "row_count_including_headers": len(rows),
                "first_three_rows_first_12_cells": [r[:12] for r in first],
                "source_taxon_guess": classify(label or member.filename),
                "header_only_no_biological_fit": True,
            })
    return {
        "source": URL,
        "archive_sha256": hashlib.sha256(raw).hexdigest(),
        "archive_bytes": len(raw),
        "csv_file_count": len(results),
        "files_with_official_event_labels": sum(bool(x["official_event_label"]) for x in results),
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
    try:
        with urllib.request.urlopen(urllib.request.Request(INDEX_URL, headers={"User-Agent": "PAYOFF-B-research-source-inventory/1.0"}), timeout=30) as resp:
            labels = parse_index_labels(resp.read(500_000).decode("utf-8"))
    except Exception as exc:
        labels = {}
        print(f"JMA HTML label fetch failed (nonfatal): {type(exc).__name__}")
    result = summarize_zip(raw, labels=labels)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"csv_file_count": result["csv_file_count"], "files_with_official_event_labels": result["files_with_official_event_labels"], "first_file_schema": result["files"][0]["first_three_rows_first_12_cells"] if result["files"] else [], "archive_sha256": result["archive_sha256"], "source_taxon_filename_class_counts": result["source_taxon_filename_class_counts"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
