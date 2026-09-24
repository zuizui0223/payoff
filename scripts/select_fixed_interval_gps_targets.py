#!/usr/bin/env python3
"""Select frozen fixed-interval GPS targets before environmental joining."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.fixed_interval_gps_targets import (
    GPSObservation,
    select_fixed_interval_gps_targets,
)


def parse_time(value: str) -> datetime:
    token = value.strip().replace("Z", "+00:00")
    return datetime.fromisoformat(token)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("input_csv", type=Path)
    p.add_argument("--target-interval-hours", type=float, default=24.0)
    p.add_argument("--max-target-deviation-hours", type=float, default=3.0)
    p.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/aikens_fixed_gps_targets.csv"),
    )
    p.add_argument(
        "--receipt-output",
        type=Path,
        default=Path("outputs/aikens_fixed_gps_targets_receipt.json"),
    )
    args = p.parse_args()

    observations = []
    with args.input_csv.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {
            "observation_id",
            "animal_id",
            "animal_year",
            "group",
            "timestamp",
            "pixel_id",
        }
        if reader.fieldnames is None:
            raise SystemExit("input CSV has no header")
        missing = required.difference(reader.fieldnames)
        if missing:
            raise SystemExit(
                "input CSV missing required columns: "
                + ", ".join(sorted(missing))
            )
        for number, row in enumerate(reader, start=2):
            try:
                observations.append(
                    GPSObservation(
                        observation_id=str(row["observation_id"]),
                        animal_id=str(row["animal_id"]),
                        animal_year=str(row["animal_year"]),
                        group=str(row["group"]),
                        timestamp=parse_time(str(row["timestamp"])),
                        pixel_id=str(row["pixel_id"]),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid input row {number}: {exc}"
                ) from exc

    result = select_fixed_interval_gps_targets(
        observations,
        target_interval_seconds=args.target_interval_hours * 3600.0,
        max_target_deviation_seconds=args.max_target_deviation_hours * 3600.0,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "animal_id",
            "animal_year",
            "group",
            "target_index",
            "target_timestamp",
            "observation_id",
            "observed_timestamp",
            "deviation_seconds",
            "pixel_id",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in result.selected_targets:
            writer.writerow(
                {
                    "animal_id": row.animal_id,
                    "animal_year": row.animal_year,
                    "group": row.group,
                    "target_index": row.target_index,
                    "target_timestamp": row.target_timestamp.isoformat(),
                    "observation_id": row.observation_id,
                    "observed_timestamp": row.observed_timestamp.isoformat(),
                    "deviation_seconds": row.deviation_seconds,
                    "pixel_id": row.pixel_id,
                }
            )

    by_group: dict[str, int] = {}
    for row in result.selected_targets:
        by_group[row.group] = by_group.get(row.group, 0) + 1

    receipt = {
        "status": "fixed_interval_gps_targets_selected",
        "source_file": str(args.input_csv),
        "target_interval_hours": result.target_interval_seconds / 3600.0,
        "max_target_deviation_hours": (
            result.max_target_deviation_seconds / 3600.0
        ),
        "anchor_rule": "earliest_raw_spring_migration_observation_per_animal_year",
        "raw_observations": result.raw_observations,
        "animal_years_seen": result.animal_years_seen,
        "animal_years_with_targets": result.animal_years_with_targets,
        "selected_targets": len(result.selected_targets),
        "selected_targets_by_group": {
            key: by_group[key] for key in sorted(by_group)
        },
        "output": str(args.output),
        "environment_used_for_selection": False,
        "lambda_outcome_opened": False,
    }
    args.receipt_output.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(args.receipt_output)


if __name__ == "__main__":
    main()
