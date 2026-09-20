#!/usr/bin/env python3
"""Inspect a candidate mule-deer source CSV for PAYOFF-B calibration readiness.

This tool does not guess model parameters. It inspects file grain, column
availability, and whether the table can support the declared direct tracking
inverse.

A row-per-animal-year summary can support descriptive or route-level audits,
but not the exact step-variance movement inverse or fixed-interval residual
transition inverse.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ALIASES = {
    "animal_id": (
        "animal_id",
        "animalid",
        "id",
        "deer_id",
        "deerid",
        "individual",
        "individual_id",
    ),
    "year": (
        "year",
        "migration_year",
    ),
    "timestamp": (
        "timestamp",
        "datetime",
        "date_time",
        "gps_time",
        "time",
        "date",
    ),
    "x": (
        "x",
        "easting",
        "longitude",
        "lon",
        "utm_x",
    ),
    "y": (
        "y",
        "northing",
        "latitude",
        "lat",
        "utm_y",
    ),
    "days_from_peak": (
        "days_from_peak",
        "daysfrompeak",
        "days_from_peak_irg",
        "dfp",
    ),
    "movement_rate": (
        "movement_rate",
        "movementrate",
        "move_rate",
        "speed",
        "migration_speed",
    ),
    "stopover": (
        "stopover",
        "stopover_use",
        "stopover_days",
        "stopover_time",
    ),
    "migration_distance": (
        "migration_distance",
        "migrationdistance",
        "distance_km",
        "migration_km",
    ),
    "start_days_from_peak": (
        "start_days_from_peak",
        "start_dfp",
        "dfp_start",
    ),
    "end_days_from_peak": (
        "end_days_from_peak",
        "end_dfp",
        "dfp_end",
    ),
}


def normalize_header(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def resolve_aliases(headers: list[str]) -> dict[str, str | None]:
    normalized = {
        normalize_header(header): header
        for header in headers
    }
    resolved: dict[str, str | None] = {}
    for role, aliases in ALIASES.items():
        match = None
        for alias in aliases:
            if alias in normalized:
                match = normalized[alias]
                break
        resolved[role] = match
    return resolved


def infer_grain(
    rows: list[dict[str, str]],
    resolved: dict[str, str | None],
) -> dict[str, object]:
    n_rows = len(rows)
    animal_col = resolved["animal_id"]
    year_col = resolved["year"]
    time_col = resolved["timestamp"]

    unique_animals = None
    unique_animal_years = None
    unique_times = None

    if animal_col is not None:
        unique_animals = len(
            {
                row.get(animal_col, "").strip()
                for row in rows
                if row.get(animal_col, "").strip()
            }
        )

    if animal_col is not None and year_col is not None:
        unique_animal_years = len(
            {
                (
                    row.get(animal_col, "").strip(),
                    row.get(year_col, "").strip(),
                )
                for row in rows
                if row.get(animal_col, "").strip()
                and row.get(year_col, "").strip()
            }
        )

    if time_col is not None:
        unique_times = len(
            {
                row.get(time_col, "").strip()
                for row in rows
                if row.get(time_col, "").strip()
            }
        )

    if time_col is not None and n_rows >= 2:
        if unique_animal_years and n_rows > 3 * unique_animal_years:
            label = "candidate_interval_or_gps_level"
        elif unique_animals and n_rows > 10 * unique_animals:
            label = "candidate_interval_or_gps_level"
        else:
            label = "timestamp_present_but_grain_uncertain"
    elif unique_animal_years is not None and unique_animal_years > 0:
        ratio = n_rows / unique_animal_years
        if 0.8 <= ratio <= 1.2:
            label = "animal_year_summary"
        else:
            label = "multirow_animal_year_without_timestamp"
    else:
        label = "summary_or_unknown"

    return {
        "label": label,
        "rows": n_rows,
        "unique_animals": unique_animals,
        "unique_animal_years": unique_animal_years,
        "unique_timestamps": unique_times,
    }


def calibration_readiness(
    resolved: dict[str, str | None],
    grain: dict[str, object],
) -> dict[str, object]:
    interval_like = grain["label"] == "candidate_interval_or_gps_level"

    movement_ready = (
        interval_like
        and resolved["animal_id"] is not None
        and resolved["timestamp"] is not None
        and resolved["x"] is not None
        and resolved["y"] is not None
    )

    phenology_ready = (
        interval_like
        and resolved["animal_id"] is not None
        and resolved["timestamp"] is not None
        and resolved["days_from_peak"] is not None
    )

    route_summary_ready = (
        resolved["animal_id"] is not None
        and (
            resolved["movement_rate"] is not None
            or resolved["migration_distance"] is not None
            or resolved["start_days_from_peak"] is not None
            or resolved["end_days_from_peak"] is not None
        )
    )

    blockers: list[str] = []
    if not interval_like:
        blockers.append(
            "table is not identified as fixed-interval/GPS-level data"
        )
    if resolved["timestamp"] is None:
        blockers.append("no timestamp column identified")
    if resolved["x"] is None or resolved["y"] is None:
        blockers.append(
            "no 2D position pair identified for component step variances"
        )
    if resolved["days_from_peak"] is None:
        blockers.append(
            "no interval-level Days-From-Peak residual column identified"
        )

    return {
        "movement_kernel_direct_inverse_ready": movement_ready,
        "phenology_step_inverse_ready": phenology_ready,
        "route_summary_analysis_ready": route_summary_ready,
        "full_direct_tracking_inverse_ready": (
            movement_ready and phenology_ready
        ),
        "blockers": blockers,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_mule_deer_source_ingest_audit.json"
        ),
    )
    args = parser.parse_args()

    with args.csv_path.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit("CSV has no header row")
        headers = list(reader.fieldnames)
        rows = list(reader)

    resolved = resolve_aliases(headers)
    grain = infer_grain(rows, resolved)
    readiness = calibration_readiness(
        resolved,
        grain,
    )

    receipt = {
        "source_file": str(args.csv_path),
        "headers": headers,
        "resolved_columns": resolved,
        "grain": grain,
        "readiness": readiness,
        "claim_boundary": (
            "column/grain audit only; does not estimate tracking parameters "
            "unless the declared fixed-interval inputs are present"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "source_ingest "
        f"grain={grain['label']} "
        f"rows={grain['rows']} "
        f"movement_ready={int(readiness['movement_kernel_direct_inverse_ready'])} "
        f"phenology_ready={int(readiness['phenology_step_inverse_ready'])} "
        f"full_ready={int(readiness['full_direct_tracking_inverse_ready'])}"
    )


if __name__ == "__main__":
    main()
