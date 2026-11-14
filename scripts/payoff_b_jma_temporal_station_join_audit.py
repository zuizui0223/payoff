"""Audit all original JMA event dates against official historical station records."""
from __future__ import annotations
import argparse
import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.japan_phenology_panel import parse_wide_jma_csv
from src.japan_phenology_smaster_temporal import parse_smaster, audit_event_coverage
from scripts.payoff_b_japan_phenology_source_census import URL as EVENT_URL, INDEX_URL, parse_index_labels
from scripts.payoff_b_jma_station_metadata_source_probe import URL as STATION_URL


def audit_original_sources(event_zip: bytes, station_zip: bytes, labels: dict) -> dict:
    events = []
    with zipfile.ZipFile(io.BytesIO(event_zip)) as z:
        for name in z.namelist():
            if not name.lower().endswith(".csv"):
                continue
            basename = name.rsplit("/", 1)[-1]
            rows, _ = parse_wide_jma_csv(z.read(name), source_file=basename,
                                         event_label=labels.get(basename, basename))
            events.extend(rows)
    metadata = parse_smaster(station_zip)
    return audit_event_coverage(events, metadata)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    def get(url, limit=30_000_000):
        req = urllib.request.Request(url, headers={"User-Agent": "PAYOFF-B-JMA-temporal-audit/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read(limit + 1)
        if len(raw) > limit:
            raise ValueError("Source exceeds registered byte limit")
        return raw
    labels = parse_index_labels(get(INDEX_URL, 500_000).decode("utf-8"))
    receipt = audit_original_sources(get(EVENT_URL), get(STATION_URL), labels)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
