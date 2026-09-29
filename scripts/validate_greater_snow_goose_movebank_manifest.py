#!/usr/bin/env python3
"""Validate a nonraw Movebank materialization manifest for Greater Snow Goose."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from scripts.payoff_b_greater_snow_goose_movebank_materialize import (
    ATTRIBUTES,
    YEARS,
    sha256_file,
)


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def validate_manifest(payload: dict) -> dict:
    errors = []

    if payload.get("status") != "COMPLETE":
        errors.append("manifest_status_not_complete")
    if payload.get("study_id") != "1442516400":
        errors.append("unexpected_study_id")
    if str(payload.get("sensor_type_id")) != "653":
        errors.append("unexpected_sensor_type_id")
    if payload.get("event_data_opened") is not True:
        errors.append("event_data_opened_not_true")

    requested = tuple(payload.get("years_requested", []))
    if requested != YEARS:
        errors.append("years_requested_not_exactly_2019_2023")

    rows = payload.get("files")
    if not isinstance(rows, list):
        errors.append("files_not_a_list")
        rows = []

    by_year = {}
    for row in rows:
        year = row.get("year")
        if year in by_year:
            errors.append(f"duplicate_year:{year}")
            continue
        by_year[year] = row

    if tuple(sorted(by_year)) != YEARS:
        errors.append("file_years_not_exactly_2019_2023")

    for year in YEARS:
        row = by_year.get(year)
        if row is None:
            continue
        if row.get("status") != "MATERIALIZED":
            errors.append(f"year_status_not_materialized:{year}")
        if not isinstance(row.get("rows"), int) or row["rows"] <= 0:
            errors.append(f"nonpositive_row_count:{year}")
        if not isinstance(row.get("bytes"), int) or row["bytes"] <= 0:
            errors.append(f"nonpositive_byte_count:{year}")
        digest = str(row.get("sha256", ""))
        if not SHA256_RE.fullmatch(digest):
            errors.append(f"invalid_sha256:{year}")
        header = set(row.get("header") or [])
        missing = set(ATTRIBUTES) - header
        if missing:
            errors.append(
                f"missing_header_fields:{year}:"
                + ",".join(sorted(missing))
            )

    calculated_total_rows = sum(
        int(row.get("rows", 0))
        for row in rows
        if isinstance(row, dict)
    )
    if payload.get("total_rows") != calculated_total_rows:
        errors.append("total_rows_mismatch")

    calculated_total_bytes = sum(
        int(row.get("bytes", 0))
        for row in rows
        if isinstance(row, dict)
    )
    if payload.get("total_bytes") != calculated_total_bytes:
        errors.append("total_bytes_mismatch")

    return {
        "valid": not errors,
        "errors": errors,
        "years": list(YEARS),
        "total_rows": calculated_total_rows,
        "total_bytes": calculated_total_bytes,
    }


def verify_raw_files(payload: dict, raw_dir: Path) -> list[str]:
    errors = []
    for row in payload.get("files", []):
        path = raw_dir / str(row.get("path"))
        if not path.is_file():
            errors.append(f"raw_file_missing:{path.name}")
            continue
        observed = sha256_file(path)
        if observed != row.get("sha256"):
            errors.append(f"raw_sha256_mismatch:{path.name}")
    return errors


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument(
        "--raw-dir",
        type=Path,
        help="Optional protected local raw directory for SHA verification.",
    )
    p.add_argument("--output", type=Path)
    return p.parse_args()


def main():
    args = parse_args()
    payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = validate_manifest(payload)

    if args.raw_dir is not None:
        raw_errors = verify_raw_files(
            payload,
            args.raw_dir.expanduser().resolve(),
        )
        result["raw_sha_verified"] = not raw_errors
        result["errors"].extend(raw_errors)
        result["valid"] = not result["errors"]
    else:
        result["raw_sha_verified"] = None

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")

    if not result["valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
