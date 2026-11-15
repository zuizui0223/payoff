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
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.japan_phenology_panel import parse_wide_jma_csv

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
    """Exact source event-name prefix taxonomy; avoid いちょう/ちょう collision.

    All 65 official event labels are audited; unmatched labels remain
    unclassified, never silently assigned to plants.
    """
    animal = {
        "amphibian": ("とのさまがえる", "にほんあまがえる"),
        "bird": ("ひばり", "うぐいす", "つばめ", "もず", "かっこう", "さしば"),
        "insect": ("もんしろちょう", "きあげは", "しおからとんぼ",
                   "ほたる", "あぶらぜみ", "ひぐらし", "あきあかね",
                   "えんまこおろぎ", "くさぜみ", "くまぜみ",
                   "つくつくほうし", "にいにいぜみ", "はるぜみ", "みんみんぜみ"),
        "reptile": ("とかげ",),
    }
    for group, prefixes in animal.items():
        if name.startswith(prefixes):
            return group
    plant_stages = ("開花", "満開", "発芽", "紅葉", "黄葉", "落葉")
    if any(name.endswith(stage) for stage in plant_stages):
        return "plant"
    return "unclassified"


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
            # JMA historical tables are wide: event-title row, station/year
            # header with year,rm pairs, then one station per row.
            # Retain rm flags without interpreting their code semantics.
            annual_coverage = None
            if len(nonempty) >= 3 and len(nonempty[1]) >= 4 and nonempty[1][0] == "番号":
                header = nonempty[1]
                # Read contiguous YEAR,rm pairs from column 2 only.
                # Trailing summary columns may also contain four-digit years.
                yearcols = []
                i = 2
                while (i + 1 < len(header)
                       and re.fullmatch(r"(?:19|20)\d{2}", header[i].strip())
                       and header[i + 1].strip().lower() == "rm"):
                    yearcols.append((i, int(header[i])))
                    i += 2
                if yearcols:
                    per_year = {}
                    station_ids = set()
                    rm_counts = Counter()
                    nondate_value_counts = Counter()
                    for row in nonempty[2:]:
                        if not row or not row[0].strip().isdigit():
                            continue
                        station_ids.add(row[0].strip())
                        for i, year in yearcols:
                            value = row[i].strip() if i < len(row) else ""
                            rm = row[i + 1].strip() if i + 1 < len(row) else ""
                            rm_counts[rm] += 1
                            # No biological event is inferred from 0, blanks,
                            # or unknown special codes; valid MMDD only.
                            if not value.isdigit() or not (1 <= int(value) <= 1231):
                                nondate_value_counts[value] += 1
                                continue
                            mmdd = value.zfill(4)
                            month, day = int(mmdd[:2]), int(mmdd[2:])
                            import datetime
                            try:
                                datetime.date(year, month, day)
                            except ValueError:
                                nondate_value_counts["INVALID_CALENDAR_DATE"] += 1
                                continue
                            per_year[year] = per_year.get(year, 0) + 1
                    annual_coverage = {
                        "year_min": min(y for _, y in yearcols),
                        "year_max": max(y for _, y in yearcols),
                        "year_column_count": len(yearcols),
                        "station_count": len(station_ids),
                        "valid_mmdd_cells": sum(per_year.values()),
                        "valid_mmdd_by_year": {str(y): per_year.get(y, 0) for _, y in yearcols},
                        "rm_flags_retained_not_interpreted": True,
                        "rm_code_frequencies_all_station_year_cells": dict(rm_counts),
                        "nondate_value_frequencies": dict(nondate_value_counts.most_common(20)),
                        "valid_mmdd_is_not_validated_biological_record": True,
                    }
            # Diagnose every rejected file without guessing its schema.
            # Distinguish no year header from a different header position.
            header_candidates = []
            for header_idx, candidate in enumerate(nonempty[:12]):
                years = [(i, int(v)) for i, v in enumerate(candidate)
                         if re.fullmatch(r"(?:19|20)\d{2}", v.strip())]
                if years:
                    header_candidates.append({
                        "row_index": header_idx,
                        "year_column_count": len(years),
                        "first_year": years[0][1],
                        "last_year": years[-1][1],
                        "next_column_is_rm_for_all": all(
                            i + 1 < len(candidate) and
                            candidate[i + 1].strip().lower() == "rm"
                            for i, _ in years),
                        "header_first_8_cells": candidate[:8],
                    })
            basename = member.filename.rsplit("/", 1)[-1]
            label = (labels or {}).get(basename)
            panel, panel_receipt = parse_wide_jma_csv(
                payload, source_file=basename, event_label=label or basename
            )
            if annual_coverage is None:
                raise ValueError(f"Unrecognized annual schema for {basename}")
            if len(panel) != annual_coverage["valid_mmdd_cells"]:
                raise ValueError(f"Independent panel count mismatch for {basename}")
            results.append({
                "filename": member.filename,
                "official_event_label": label,
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "encoding": encoding,
                "annual_coverage": annual_coverage,
                "panel_receipt": panel_receipt,
                "header_candidates": header_candidates,
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
        "files_with_wide_year_rm_schema": sum(x["annual_coverage"] is not None for x in results),
        "independent_panel_event_count": sum(x["panel_receipt"]["event_rows_calendar_valid_not_rm_screened"] for x in results),
        "valid_mmdd_cells_total_not_unique_observations": sum(x["annual_coverage"]["valid_mmdd_cells"] for x in results if x["annual_coverage"]),
        "source_taxon_filename_class_counts": dict(Counter(x["source_taxon_guess"] for x in results)),
        "unrecognized_files": [{
            "filename": x["filename"],
            "official_event_label": x["official_event_label"],
            "row_count": x["row_count_including_headers"],
            "first_three_rows_first_12_cells": x["first_three_rows_first_12_cells"],
            "header_candidates": x["header_candidates"],
        } for x in results if x["annual_coverage"] is None],
        "rm_codes_on_valid_event_dates": dict(sum((Counter(x["panel_receipt"]["valid_event_rm_codes"]) for x in results), Counter())),
        "rm_code_frequencies_all_wide_tables": dict(sum(
            (Counter(x["annual_coverage"]["rm_code_frequencies_all_station_year_cells"])
             for x in results if x["annual_coverage"] is not None), Counter())),
        "by_taxon_provisional": {
            taxon: {
                "files": sum(x["source_taxon_guess"] == taxon for x in results),
                "wide_year_files": sum(x["source_taxon_guess"] == taxon and x["annual_coverage"] is not None for x in results),
                "calendar_valid_cells_not_quality_screened": sum(
                    x["annual_coverage"]["valid_mmdd_cells"]
                    for x in results if x["source_taxon_guess"] == taxon and x["annual_coverage"] is not None),
            }
            for taxon in ("amphibian", "bird", "insect", "plant_or_unclassified")
        },
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
    print(json.dumps({"csv_file_count": result["csv_file_count"], "files_with_official_event_labels": result["files_with_official_event_labels"], "files_with_wide_year_rm_schema": result["files_with_wide_year_rm_schema"], "valid_mmdd_cells_total_not_unique_observations": result["valid_mmdd_cells_total_not_unique_observations"], "independent_panel_event_count": result["independent_panel_event_count"], "rm_codes_on_valid_event_dates": result["rm_codes_on_valid_event_dates"], "first_file_schema": result["files"][0]["first_three_rows_first_12_cells"] if result["files"] else [], "archive_sha256": result["archive_sha256"], "source_taxon_filename_class_counts": result["source_taxon_filename_class_counts"], "by_taxon_provisional": result["by_taxon_provisional"], "unrecognized_files": result["unrecognized_files"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
