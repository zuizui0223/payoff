#!/usr/bin/env python3
"""Audit linkage of the published stork GPS archive to annual breeding records.

PUBLIC-SOURCE QC ONLY; does not estimate arrival effects, behavior or fitness.
The 273MB GPS is checksum-verified and processed locally in the GitHub job.
Do not include individual IDs, raw animal locations, or track files in artifacts.

Data: Rotics et al. 2018, Movebank DOI 10.5441/001/1.v8d24552 (CC0).
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

from scripts.qc_public_movebank_stork_breeding_2018 import (
    DOI, FILES as SMALL_FILES, ARCHIVE, download_cc0, UNKNOWN,
)

GPS_UUID = "ed3529e6-ce20-4237-8875-9d35fdbf9a0f"
GPS_EXPECTED_MD5 = "bda2ebd2441316b2e2fd9e9578d7d0b4"
GPS_EXPECTED_BYTES = 273153305
GPS_LIMIT_BYTES = GPS_EXPECTED_BYTES + 16384

# Calendar-month COVERAGE screens only, never a claim about actual residence.
COVERAGE_MONTHS = {
    "winter_JanFeb": {1, 2},
    "spring_MarApr": {3, 4},
    "late_spring_MayJun": {5, 6},
}
MIN_DAYS_WINTER = 5
MIN_DAYS_SPRING = 10
MIN_DAYS_LATE = 7
MAX_ID_SAMPLE = 50000

JOIN_SPECS = (
    ("deployment-id", "deployment-id"),
    ("individual-local-identifier", "animal-id"),
    ("tag-local-identifier", "tag-id"),
)
REQUIRED_GPS = {"timestamp", "location-lat", "location-long"}


def download_gps(path):
    request = urllib.request.Request(
        ARCHIVE + GPS_UUID + "/content",
        headers={"User-Agent": "PAYOFF-B-public-CC0-GPS-join-QC/0.1"}
    )
    digest, size = hashlib.md5(), 0
    with urllib.request.urlopen(request, timeout=150) as response, Path(path).open("wb") as out:
        if not response.geturl().startswith("https://datarepository.movebank.org/"):
            raise ValueError("GPS download redirected off original repository")
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > GPS_LIMIT_BYTES:
                raise ValueError("GPS download exceeds preverified byte limit")
            digest.update(chunk)
            out.write(chunk)
    if size != GPS_EXPECTED_BYTES or digest.hexdigest() != GPS_EXPECTED_MD5:
        raise ValueError(
            f"GPS original integrity failure: size={size} "
            f"expected={GPS_EXPECTED_BYTES} md5={digest.hexdigest()} "
            f"expected={GPS_EXPECTED_MD5}"
        )
    return {"verified": True, "bytes": size, "md5": digest.hexdigest(),
            "bitstream_uuid": GPS_UUID}


def load_reference_and_breeding(refpath, birthpath):
    with Path(refpath).open(encoding="utf-8-sig", errors="replace", newline="") as f:
        ref_reader = csv.DictReader(f)
        refs = list(ref_reader)
    with Path(birthpath).open(encoding="utf-8-sig", errors="replace", newline="") as f:
        bird_reader = csv.DictReader(f)
        breeding = list(bird_reader)
    for required in ("deployment-id", "animal-id", "tag-id"):
        if required not in (ref_reader.fieldnames or []):
            raise ValueError("reference missing key column: " + required)
    for required in ("id", "Year", "Fledglings"):
        if required not in (bird_reader.fieldnames or []):
            raise ValueError("breeding missing key column: " + required)
    deployments = {str(r["deployment-id"]).strip() for r in refs}
    if len(deployments) != len(refs) or "" in deployments:
        raise ValueError("reference deployment keys are duplicated/blank")
    years = set()
    numeric_birth_pairs = set()
    for row in breeding:
        ident, year = str(row["id"]).strip(), str(row["Year"]).strip()
        if ident not in deployments or not year.isdecimal():
            raise ValueError("breeding ID/year mismatched against reference")
        pair = (ident, int(year))
        if pair in years:
            raise ValueError("duplicate breeding animal-year")
        years.add(pair)
        if (row["Fledglings"] or "").strip().upper() not in UNKNOWN:
            numeric_birth_pairs.add(pair)
    return refs, years, numeric_birth_pairs


def identifier_mappings(refs):
    mappings = {}
    ambiguous = {}
    for gpsfield, reffield in JOIN_SPECS:
        mapping, conflicts = {}, set()
        for row in refs:
            key, deploy = str(row.get(reffield) or "").strip(), str(row["deployment-id"]).strip()
            if not key:
                continue
            if key in mapping and mapping[key] != deploy:
                conflicts.add(key)
            else:
                mapping[key] = deploy
        for k in conflicts:
            mapping.pop(k, None)
        mappings[gpsfield] = mapping
        ambiguous[gpsfield] = len(conflicts)
    return mappings, ambiguous


def choose_gps_identifier(gpspath, mappings):
    with Path(gpspath).open(encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        if not REQUIRED_GPS.issubset(set(fields)):
            raise ValueError("GPS essential columns missing: " + ",".join(sorted(REQUIRED_GPS-set(fields))))
        methods = [k for k, _ in JOIN_SPECS if k in fields]
        if not methods:
            raise ValueError("GPS has no matching deployment/animal/tag identity column")
        matches = Counter()
        sampled = 0
        for row in reader:
            sampled += 1
            for method in methods:
                if str(row.get(method) or "").strip() in mappings[method]:
                    matches[method] += 1
            if sampled >= MAX_ID_SAMPLE:
                break
    # Selection uses only independent reference identifiers; no breeding success
    # or route response data are involved.
    method = max(methods, key=lambda k: (matches[k], -methods.index(k)))
    if matches[method] == 0:
        raise ValueError("No GPS identifiers match the independent reference file")
    return {
        "gps_columns": fields,
        "identity_method": method,
        "sample_rows_for_identity_mapping": sampled,
        "sample_matches_by_available_method": dict(matches),
    }


def parse_time(value):
    s = (value or "").strip()
    if not s:
        raise ValueError("blank timestamp")
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def gps_breeding_join_summary(gpspath, refs, breeding_pairs, numeric_pairs):
    mappings, ambiguous = identifier_mappings(refs)
    preflight = choose_gps_identifier(gpspath, mappings)
    method = preflight["identity_method"]
    mapping = mappings[method]
    obs = Counter()
    months = defaultdict(set)
    total = 0
    unmatched = no_id = invalid_time = invalid_position = 0
    matched = 0
    gps_pairs = set()
    spring_pairs = set()
    seen_pair_time = set()
    duplicate_matched_timestamps = 0
    speed_nonmissing = 0
    raw_years = Counter()
    matched_years = Counter()
    with Path(gpspath).open(encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            ident = str(row.get(method) or "").strip()
            if not ident:
                no_id += 1
                continue
            dep = mapping.get(ident)
            if dep is None:
                unmatched += 1
                continue
            try:
                dt = parse_time(row.get("timestamp"))
            except ValueError:
                invalid_time += 1
                continue
            try:
                lat = float(row.get("location-lat") or "")
                lon = float(row.get("location-long") or "")
                if not math.isfinite(lat) or not math.isfinite(lon):
                    raise ValueError("non-finite GPS coordinate")
                if not -90 <= lat <= 90 or not -180 <= lon <= 180:
                    raise ValueError("GPS outside geographic range")
            except ValueError:
                invalid_position += 1
                continue
            if "ground-speed" in (preflight["gps_columns"]):
                speed = (row.get("ground-speed") or "").strip()
                if speed:
                    try:
                        if math.isfinite(float(speed)):
                            speed_nonmissing += 1
                    except ValueError:
                        pass
            matched += 1
            raw_years[dt.year] += 1
            pair = dep, dt.year
            gps_pairs.add(pair)
            if pair in breeding_pairs:
                matched_years[dt.year] += 1
                key = (dep, dt.isoformat())
                if key in seen_pair_time:
                    duplicate_matched_timestamps += 1
                else:
                    seen_pair_time.add(key)
                obs[pair] += 1
                day = dt.date().isoformat()
                for season, values in COVERAGE_MONTHS.items():
                    if dt.month in values:
                        months[(pair, season)].add(day)
    sufficient_winter = {
        pair for pair in breeding_pairs
        if len(months[(pair, "winter_JanFeb")]) >= MIN_DAYS_WINTER
    }
    sufficient_spring = {
        pair for pair in breeding_pairs
        if len(months[(pair, "spring_MarApr")]) >= MIN_DAYS_SPRING
    }
    sufficient_late = {
        pair for pair in breeding_pairs
        if len(months[(pair, "late_spring_MayJun")]) >= MIN_DAYS_LATE
    }
    all_three = sufficient_winter & sufficient_spring & sufficient_late
    two_window = sufficient_spring & sufficient_late
    matched_pairs = gps_pairs & breeding_pairs
    repeat_ids = Counter(pair[0] for pair in matched_pairs)
    # Do not export animal IDs or locations; report coverage and fixed gates.
    return {
        **preflight,
        "ambiguous_reference_keys_by_method": ambiguous,
        "source_gps_total_rows": total,
        "source_gps_rows_matched_and_geovalid": matched,
        "source_gps_unmatched_identity_rows": unmatched,
        "source_gps_blank_identity_rows": no_id,
        "source_gps_invalid_timestamp_rows": invalid_time,
        "source_gps_invalid_geocoordinate_rows": invalid_position,
        "matched_duplicate_individual_timestamp_rows": duplicate_matched_timestamps,
        "ground_speed_nonmissing_matched_events": speed_nonmissing,
        "matched_gps_rows_by_year": {str(k):v for k,v in sorted(raw_years.items())},
        "matched_breeding_gps_rows_by_year": {str(k):v for k,v in sorted(matched_years.items())},
        "breeding_total_animal_years": len(breeding_pairs),
        "breeding_numeric_fledgling_animal_years": len(numeric_pairs),
        "breeding_animal_years_with_any_valid_gps": len(matched_pairs),
        "breeding_animal_years_with_any_gps_and_numeric_fledglings": len(matched_pairs & numeric_pairs),
        "gps_matched_breeding_individuals": len(repeat_ids),
        "gps_breeding_individuals_repeated_over_years": sum(n>1 for n in repeat_ids.values()),
        "coverage_calendar_windows": {
            "winter_JanFeb_min5dates": len(sufficient_winter),
            "spring_MarApr_min10dates": len(sufficient_spring),
            "late_spring_MayJun_min7dates": len(sufficient_late),
            "spring_and_late_windows": len(two_window),
            "winter_spring_late_all": len(all_three),
            "winter_spring_late_all_numeric_fledglings": len(all_three & numeric_pairs),
            "spring_and_late_numeric_fledglings": len(two_window & numeric_pairs),
        },
        "coverage_gate_constants": {
            "min_unique_days_JanFeb": MIN_DAYS_WINTER,
            "min_unique_days_MarApr": MIN_DAYS_SPRING,
            "min_unique_days_MayJun": MIN_DAYS_LATE,
        },
        "calendar_windows_are_actual_migration_stages": False,
        "migration_start_end_derived": False,
        "stopover_actuators_derived": False,
        "cue_availability_verified": False,
        "individual_correction_effect_estimated": False,
        "fitness_association_estimated": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path("outputs/payoff_b_stork_gps_breeding_join_qc.json"))
    args = parser.parse_args()
    result = {
        "source_doi": DOI,
        "classification": "VERIFIED_SOURCE_COVERAGE_ONLY",
        "source_checksum_verified": False,
        "biological_hypothesis_tested": False,
        "status": "NOT_STARTED",
    }
    with tempfile.TemporaryDirectory() as tmp:
        working = Path(tmp)
        small = {}
        try:
            for name in SMALL_FILES:
                small[name] = working / (
                    name + (".txt" if name == "readme" else ".csv")
                )
                download_cc0(name, small[name])
            refs, breeding, numeric = load_reference_and_breeding(
                small["reference"], small["breeding"]
            )
            gps = working / "gps.csv"
            result["gps_source_integrity"] = download_gps(gps)
            result["source_checksum_verified"] = True
            result["join_audit"] = gps_breeding_join_summary(gps, refs, breeding, numeric)
            result["status"] = "VERIFIED_GPS_BREEDING_COVERAGE"
        except (OSError, ValueError, urllib.error.URLError) as e:
            result["status"] = "FAILED_SOURCE_OR_SCHEMA_GATE"
            result["error"] = type(e).__name__ + ": " + str(e)[:550]
    result["raw_gps_or_animal_ids_exported"] = False
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "VERIFIED_GPS_BREEDING_COVERAGE":
        raise SystemExit("GPS-to-breeding source admission failed")


if __name__ == "__main__":
    main()
