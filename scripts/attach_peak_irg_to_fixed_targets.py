#!/usr/bin/env python3
"""Attach peak IRG to already selected fixed-interval GPS targets."""

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

from src.fixed_interval_gps_targets import FixedIntervalGPSTarget
from src.fixed_target_phase import attach_phase_to_fixed_targets
from src.phase_environment_join import PeakIRGRecord


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "t", "yes", "y"}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("targets_csv", type=Path)
    p.add_argument("peak_irg_csv", type=Path)
    p.add_argument(
        "--required-modis-product",
        choices=("MOD09Q1.006", "MOD09Q1.061"),
    )
    p.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/aikens_fixed_targets_with_phase.csv"),
    )
    p.add_argument(
        "--receipt-output",
        type=Path,
        default=Path("outputs/aikens_fixed_targets_phase_receipt.json"),
    )
    args = p.parse_args()

    targets = []
    with args.targets_csv.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {
            "animal_id",
            "animal_year",
            "group",
            "target_index",
            "target_timestamp",
            "observation_id",
            "observed_timestamp",
            "deviation_seconds",
            "pixel_id",
        }
        if reader.fieldnames is None:
            raise SystemExit("targets CSV has no header")
        missing = required.difference(reader.fieldnames)
        if missing:
            raise SystemExit(
                "targets CSV missing required columns: "
                + ", ".join(sorted(missing))
            )
        for number, row in enumerate(reader, start=2):
            try:
                targets.append(
                    FixedIntervalGPSTarget(
                        animal_id=str(row["animal_id"]),
                        animal_year=str(row["animal_year"]),
                        group=str(row["group"]),
                        target_index=int(row["target_index"]),
                        target_timestamp=parse_time(row["target_timestamp"]),
                        observation_id=str(row["observation_id"]),
                        observed_timestamp=parse_time(row["observed_timestamp"]),
                        deviation_seconds=float(row["deviation_seconds"]),
                        pixel_id=str(row["pixel_id"]),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid target row {number}: {exc}"
                ) from exc

    peaks = []
    with args.peak_irg_csv.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {
            "pixel_id",
            "year",
            "modis_product",
            "reconstruction_lane",
            "peak_irg_date",
        }
        if reader.fieldnames is None:
            raise SystemExit("peak IRG CSV has no header")
        missing = required.difference(reader.fieldnames)
        if missing:
            raise SystemExit(
                "peak IRG CSV missing required columns: "
                + ", ".join(sorted(missing))
            )
        for number, row in enumerate(reader, start=2):
            try:
                peaks.append(
                    PeakIRGRecord(
                        pixel_id=str(row["pixel_id"]),
                        year=int(row["year"]),
                        modis_product=str(row["modis_product"]),
                        reconstruction_lane=str(row["reconstruction_lane"]),
                        peak_irg_date=str(row["peak_irg_date"]),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid peak IRG row {number}: {exc}"
                ) from exc

    audit = attach_phase_to_fixed_targets(
        targets,
        peaks,
        required_modis_product=args.required_modis_product,
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
            "phase_valid",
            "local_peak_irg_timestamp",
            "phase_error_days",
            "modis_product",
            "reconstruction_lane",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in audit.targets:
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
                    "phase_valid": str(row.phase_valid).lower(),
                    "local_peak_irg_timestamp": (
                        ""
                        if row.local_peak_irg_timestamp is None
                        else row.local_peak_irg_timestamp.isoformat()
                    ),
                    "phase_error_days": (
                        ""
                        if row.phase_error_days is None
                        else row.phase_error_days
                    ),
                    "modis_product": row.modis_product or "",
                    "reconstruction_lane": row.reconstruction_lane or "",
                }
            )

    receipt = {
        "status": "fixed_target_environmental_phase_audit_complete",
        "targets_source": str(args.targets_csv),
        "peak_irg_source": str(args.peak_irg_csv),
        "required_modis_product": args.required_modis_product,
        "total_targets": audit.total_targets,
        "valid_targets": audit.valid_targets,
        "invalid_targets": audit.invalid_targets,
        "valid_fraction": (
            audit.valid_targets / audit.total_targets
            if audit.total_targets
            else 0.0
        ),
        "valid_by_group": dict(audit.valid_by_group),
        "invalid_by_group": dict(audit.invalid_by_group),
        "products": list(audit.products),
        "reconstruction_lanes": list(audit.reconstruction_lanes),
        "output": str(args.output),
        "target_selection_changed_by_environment": False,
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
