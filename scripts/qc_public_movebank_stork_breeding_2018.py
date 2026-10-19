#!/usr/bin/env python3
"""Read-only published CC0 stork reproduction/source-data admission audit.

The 273 MB GPS and 1 GB accelerometer files are NOT downloaded here.
No animal IDs or locations are published; only source-level aggregates.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import tempfile
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

ARCHIVE = "https://datarepository.movebank.org/server/api/core/bitstreams/"
DOI = "10.5441/001/1.v8d24552"
PAPER = "10.1111/1365-2656.12898"
FILES = {
    "breeding": ("d5a51c3d-d726-41de-968c-eceb40871e9b",
                 "127aac0293bea33bb9329f2624aacbfb", 2150),
    "reference": ("7011637a-dc59-4c24-86e3-5ff0d46fb320",
                  "1c9f7c976ebb094e8b1b9c37965c5717", 14115),
    "readme": ("45e1c70b-d7af-4a40-802f-c302ae483efa",
               "900cd4505d84037f470540bf33e21aec", 15286),
}
UNKNOWN = {"NA", "UNKNOWN", "NAN", "NONE", ""}


def download_cc0(name, dest):
    uuid, expected, size = FILES[name]
    req = urllib.request.Request(ARCHIVE + uuid + "/content",
                                 headers={"User-Agent": "PAYOFF-B-public-source-QC/0.1"})
    md5, n = hashlib.md5(), 0
    with urllib.request.urlopen(req, timeout=45) as response, Path(dest).open("wb") as out:
        if not response.geturl().startswith("https://datarepository.movebank.org/"):
            raise ValueError("redirect outside repository")
        while True:
            block = response.read(65536)
            if not block:
                break
            n += len(block)
            if n > size + 32768:
                raise ValueError("published source size cap exceeded")
            md5.update(block)
            out.write(block)
    if md5.hexdigest() != expected or n != size:
        raise ValueError(f"{name}: pinned source checksum/size mismatch")
    return {"bitstream_uuid": uuid, "md5": expected, "size_bytes": n}


def read_stork_breeding(breeding_csv, reference_csv):
    with Path(reference_csv).open(encoding="utf-8-sig", newline="", errors="replace") as f:
        reader = csv.DictReader(f)
        if not {"deployment-id", "animal-taxon"}.issubset(set(reader.fieldnames or [])):
            raise ValueError("required reference fields missing")
        refs = list(reader)
    ids = {str(r["deployment-id"]).strip() for r in refs if r.get("deployment-id")}
    taxa = sorted({r["animal-taxon"] for r in refs if r.get("animal-taxon")})
    with Path(breeding_csv).open(encoding="utf-8-sig", newline="", errors="replace") as f:
        reader = csv.DictReader(f)
        if not {"id", "Year", "Sex", "Fledglings", "Breeding attempt"}.issubset(
            set(reader.fieldnames or [])
        ):
            raise ValueError("breeding fields missing")
        records = list(reader)
    years, animals, attempts = Counter(), Counter(), Counter()
    matched_rows, matched_ids = 0, set()
    known, missing = [], 0
    for row in records:
        identifier, year = str(row["id"]).strip(), str(row["Year"]).strip()
        if not identifier or not year.isdigit():
            raise ValueError("missing ID or nonnumeric year")
        animals[identifier] += 1
        years[year] += 1
        attempts[str(row["Breeding attempt"]).strip().lower()] += 1
        if identifier in ids:
            matched_rows += 1
            matched_ids.add(identifier)
        fledged = str(row["Fledglings"]).strip()
        if fledged.upper() in UNKNOWN:
            missing += 1
        else:
            try:
                number = float(fledged)
            except ValueError:
                raise ValueError("unexpected fledgling count")
            if number < 0 or not number.is_integer():
                raise ValueError("invalid fledgling count")
            known.append(int(number))
    return {
        "reference_rows": len(refs),
        "reference_unique_deployments": len(ids),
        "reference_taxa": taxa,
        "breeding_individual_year_rows": len(records),
        "breeding_distinct_individual_ids": len(animals),
        "breeding_individuals_repeated_over_years": sum(n > 1 for n in animals.values()),
        "breeding_year_counts": dict(sorted(years.items())),
        "breeding_attempt_counts": dict(sorted(attempts.items())),
        "fledgling_count_numeric_rows": len(known),
        "fledgling_missing_or_unknown_rows": missing,
        "mean_fledglings_among_numeric_rows": (
            sum(known) / len(known) if known else None
        ),
        "breeding_rows_with_reference_deployment_match": matched_rows,
        "breeding_individuals_with_reference_deployment_match": len(matched_ids),
        "breeding_rows_without_reference_match": len(records) - matched_rows,
        "breeding_unique_ids_without_reference_match": len(set(animals) - ids),
        "has_independently_observed_breeding_outcome_file": bool(known),
        "movement_events_joined": False,
        "migration_stage_actions_measured": False,
        "decision_time_cue_measured": False,
        "causal_test_run": False,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path,
                    default=Path("outputs/payoff_b_white_stork_breeding_qc.json"))
    args = ap.parse_args()
    result = {
        "source_doi": DOI, "paper_doi": PAPER,
        "rights": "CC0 1.0 Universal", "status": "NOT_OPENED",
        "source_files": {}, "source_validation_error": None,
    }
    with tempfile.TemporaryDirectory() as temp:
        files = {name: Path(temp) / (name + (".txt" if name == "readme" else ".csv"))
                 for name in FILES}
        try:
            for name in FILES:
                result["source_files"][name] = download_cc0(name, files[name])
            result["source_coverage"] = read_stork_breeding(
                files["breeding"], files["reference"]
            )
            result["status"] = "VERIFIED_BREEDING_SOURCE_METADATA_ONLY"
        except (urllib.error.HTTPError, urllib.error.URLError, OSError, ValueError) as e:
            result["status"] = "SOURCE_ACCESS_OR_JOIN_BLOCKED"
            result["source_validation_error"] = type(e).__name__ + " " + str(e)[:250]
    result["gps_source_size_declared_bytes"] = 273153305
    result["acc_source_size_declared_bytes"] = 1058090908
    result["gps_and_acc_not_downloaded"] = True
    result["individual_identifiers_not_uploaded"] = True
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] != "VERIFIED_BREEDING_SOURCE_METADATA_ONLY":
        raise SystemExit("source admission failed")


if __name__ == "__main__":
    main()
