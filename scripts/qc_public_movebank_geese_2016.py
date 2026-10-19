#!/usr/bin/env python3
"""Public archived Movebank source QC (no raw GPS output or biological test).

Kölzsch et al. 2016, 10.5441/001/1.31c2v92f (CC0). This dataset might
share an underlying animal cohort with PAYOFF's already opened goose systems.
The QC below is NOT an independent test of the PAYOFF-B hypothesis.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import tempfile
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = "https://datarepository.movebank.org/server/api/core/bitstreams/"
DOI = "10.5441/001/1.31c2v92f"
FILES = {
    "gps": ("0a262590-49e2-4e47-a290-dbfd6649579f",
            "0e0abd1126c53f4924907c3fb6a72d02", 16806763),
    "reference": ("8f978822-d8a0-482e-9ada-d931ee4f3a0c",
                  "b94f00cf565810e27e8c658260cae58a", 7827),
    "readme": ("5e59bf05-e763-4da9-9629-0c5aae4226cc",
               "00a2bd756f2b78eda10223860d38c833", 10567),
}
MAX_EXTRA_BYTES = 512 * 1024


def download_public_bitstream(name, dest):
    uuid, expected_md5, expected_size = FILES[name]
    url = ROOT + uuid + "/content"
    request = urllib.request.Request(url, headers={
        "User-Agent": "PAYOFF-B-public-source-QC/0.1",
        "Accept": "text/plain,text/csv,application/octet-stream",
    })
    checksum = hashlib.md5()
    count = 0
    with urllib.request.urlopen(request, timeout=120) as response, Path(dest).open("wb") as f:
        if not response.geturl().startswith("https://datarepository.movebank.org/"):
            raise ValueError("unexpected redirect outside publisher's archive")
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            count += len(chunk)
            if count > expected_size + MAX_EXTRA_BYTES:
                raise ValueError(f"{name}: exceeds pinned size bound")
            checksum.update(chunk)
            f.write(chunk)
    if count != expected_size or checksum.hexdigest() != expected_md5:
        raise ValueError(
            f"{name}: pinned MD5/size mismatch; "
            f"actual_bytes={count} expected_bytes={expected_size}; "
            f"actual_md5={checksum.hexdigest()} expected_md5={expected_md5}"
        )
    return {"size_bytes": count, "md5": checksum.hexdigest(),
            "bitstream_uuid": uuid, "bitstream_url": url}


def event_coverage(path):
    """Aggregate event coverage without outputting individual IDs or coordinates."""
    with Path(path).open(newline="", encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        required = {"timestamp", "individual-local-identifier",
                    "location-lat", "location-long"}
        if not required.issubset(set(fields)):
            return {"status": "REQUIRED_FIELDS_MISSING",
                    "available_columns": fields, "required_columns": sorted(required)}
        n = badtime = missingid = badcoords = duplicate = 0
        animals, animal_years = Counter(), defaultdict(set)
        years, months, yearmonths, seen = Counter(), Counter(), set(), set()
        first = last = None
        for row in reader:
            n += 1
            individual = (row.get("individual-local-identifier") or "").strip()
            if not individual:
                missingid += 1
                continue
            raw = (row.get("timestamp") or "").strip()
            try:
                dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            except ValueError:
                badtime += 1
                continue
            try:
                lat = float(row.get("location-lat", ""))
                lon = float(row.get("location-long", ""))
                if not (math.isfinite(lat) and math.isfinite(lon)
                        and -90 <= lat <= 90 and -180 <= lon <= 180):
                    raise ValueError("range")
            except (ValueError, TypeError):
                badcoords += 1
                continue
            key = (individual, raw)
            if key in seen:
                duplicate += 1
            else:
                seen.add(key)
            animals[individual] += 1
            animal_years[individual].add(dt.year)
            years[dt.year] += 1
            months[dt.month] += 1
            yearmonths.add((dt.year, dt.month))
            day = dt.date().isoformat()
            first = day if first is None or day < first else first
            last = day if last is None or day > last else last
    counts = sorted(animals.values())
    def quantile(q):
        return counts[round(q * (len(counts)-1))] if counts else None
    return {
        "status": "TIMESTAMP_AND_COORDINATE_COLUMNS_PRESENT",
        "total_input_rows": n,
        "valid_location_timestamp_identity_rows": sum(animals.values()),
        "missing_individual_rows": missingid,
        "invalid_timestamp_rows": badtime,
        "invalid_coordinate_rows": badcoords,
        "duplicate_individual_timestamp_rows": duplicate,
        "unique_individual_identifiers": len(animals),
        "identifiers_present_in_multiple_calendar_years": sum(
            len(y) > 1 for y in animal_years.values()),
        "date_range": [first, last] if first else [],
        "calendar_years_with_valid_events": len(years),
        "calendar_year_counts": {str(k):v for k,v in sorted(years.items())},
        "month_event_counts": {str(k):v for k,v in sorted(months.items())},
        "year_months_with_events": len(yearmonths),
        "individual_event_count_quantiles": {
            "min": quantile(0), "median": quantile(0.5),
            "p90": quantile(0.9), "max": quantile(1)},
        "has_required_event_columns": True,
        "has_true_migration_segmentation": False,
        "cue_chronology_verified": False,
        "behavioral_correction_verified": False,
        "fitness_outcome_verified": False,
        "unique_migration_seasons_verified": False,
    }


def reference_coverage(path):
    with Path(path).open(newline="", encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)
        return {"columns": reader.fieldnames or [], "n_rows": sum(1 for _ in reader)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path,
        default=Path("outputs/payoff_b_public_geese_qc_2016.json"))
    args = ap.parse_args()
    result = {
        "source_doi": DOI, "source_article_doi": "10.1111/oik.03121",
        "license_metadata": "CC0 1.0 Universal",
        "published_individual_count_reference": 65,
        "reuse_is_confirmatory_independent": "NOT_VERIFIED_POSSIBLE_COHORT_OVERLAP",
        "status": "PENDING_SOURCE_READ", "access_issue": None,
    }
    with tempfile.TemporaryDirectory() as d:
        paths = {
            key: Path(d) / (key + (".txt" if key == "readme" else ".csv"))
            for key in FILES
        }
        try:
            result["files"] = {
                key: download_public_bitstream(key, paths[key]) for key in FILES
            }
            result["gps_coverage"] = event_coverage(paths["gps"])
            result["reference_coverage"] = reference_coverage(paths["reference"])
            result["readme_pinned"] = True
            result["status"] = "PUBLIC_SOURCE_CHECKED_AGGREGATE_QC_ONLY"
        except (urllib.error.HTTPError, urllib.error.URLError, OSError, ValueError) as e:
            result["status"] = "NOT_ADMITTED_SOURCE_OR_DOWNLOAD_ERROR"
            result["access_issue"] = type(e).__name__ + " " + str(e)[:400]
    result["raw_tracking_file_uploaded"] = False
    result["causal_information_actionability_test"] = "NOT_RUN"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "PUBLIC_SOURCE_CHECKED_AGGREGATE_QC_ONLY":
        raise SystemExit("Published archive source integrity/availability gate failed")


if __name__ == "__main__":
    main()
