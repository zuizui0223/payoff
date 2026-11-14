"""Audit phenology 3-digit station IDs against official JMA smaster.index IDs.

A numeric-ID match is evidence for a candidate crosswalk, NOT sufficient proof
of station history, coordinates, or temporal validity.
"""
from __future__ import annotations
import argparse
import csv
import io
import json
import re
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.payoff_b_japan_phenology_source_census import URL as PHENO_URL
from scripts.payoff_b_jma_station_metadata_source_probe import URL as META_URL

def compare_station_ids(pheno_archive: bytes, metadata_archive: bytes) -> dict:
    p_ids = set()
    p_names = {}
    with zipfile.ZipFile(io.BytesIO(pheno_archive)) as z:
        for name in z.namelist():
            if not name.lower().endswith(".csv"):
                continue
            rows = list(csv.reader(io.StringIO(z.read(name).decode("cp932"))))
            if len(rows) < 3 or rows[1][:2] != ["番号", "地点名"]:
                raise ValueError("Unexpected original phenology table schema")
            for row in rows[2:]:
                if row and re.fullmatch(r"\d{3}", row[0].strip()):
                    sid = row[0].strip()
                    p_ids.add(sid)
                    p_names.setdefault(sid, set()).add(row[1].strip())
    meta_ids = set()
    meta_name_samples = {}
    malformed = 0
    with zipfile.ZipFile(io.BytesIO(metadata_archive)) as z:
        members = [x for x in z.namelist() if x.endswith("smaster.index")]
        if len(members) != 1:
            raise ValueError("Expected one original smaster.index")
        lines = z.read(members[0]).decode("cp932").splitlines()
        for line in lines:
            if len(line) < 40 or not re.fullmatch(r"\d{3}", line[:3]):
                malformed += 1
                continue
            sid = line[:3]
            meta_ids.add(sid)
            # Extract a limited diagnostic only; full station history
            # and coordinate positions require official format spec.
            meta_name_samples.setdefault(sid, line[15:35].strip())
    overlap = p_ids & meta_ids
    return {
        "status": "NUMERIC_ID_CANDIDATE_OVERLAP_ONLY",
        "phenology_station_ids": len(p_ids),
        "metadata_station_ids": len(meta_ids),
        "overlap_station_ids": len(overlap),
        "phenology_unmatched_ids": sorted(p_ids - meta_ids),
        "metadata_malformed_lines": malformed,
        "overlap_examples": [{"id": sid, "phenology_names": sorted(p_names[sid]),
                              "metadata_name_fragment": meta_name_samples[sid]}
                             for sid in sorted(overlap)[:12]],
        "source_temporal_location_crosswalk_certified": False,
        "coordinates_certified": False,
        "environmental_join_admitted": False,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    def fetch(url):
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"PAYOFF-B-station-overlap-audit/1.0"}), timeout=60) as r:
            return r.read(30_000_001)
    result = compare_station_ids(fetch(PHENO_URL), fetch(META_URL))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
