#!/usr/bin/env python3
"""Attach local peak-IRG dates to GPS observations with explicit coverage audit."""

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

from src.phase_environment_join import (
    GPSPhaseKey,
    PeakIRGRecord,
    attach_peak_irg_to_gps,
)


def parse_time(value: str) -> datetime:
    token = value.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(token)
    except ValueError as exc:
        raise ValueError(
            f"timestamp is not ISO-8601 compatible: {value!r}"
        ) from exc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("gps_csv", type=Path)
    parser.add_argument("peak_irg_csv", type=Path)
    parser.add_argument(
        "--required-modis-product",
        choices=("MOD09Q1.006", "MOD09Q1.061"),
    )
    parser.add_argument(
        "--minimum-matched-fraction",
        type=float,
        default=0.0,
    )
    parser.add_argument(
        "--allow-below-minimum",
        action="store_true",
        help=(
            "write the coverage audit even when the predeclared matched "
            "fraction is not reached"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_phase_annotated_gps.csv"
        ),
    )
    parser.add_argument(
        "--receipt-output",
        type=Path,
        default=Path(
            "outputs/payoff_b_phase_environment_join_receipt.json"
        ),
    )
    args = parser.parse_args()

    gps_rows = []
    with args.gps_csv.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
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
            raise SystemExit("GPS CSV has no header row")
        missing = required.difference(
            reader.fieldnames
        )
        if missing:
            raise SystemExit(
                "GPS CSV missing required columns: "
                + ", ".join(sorted(missing))
            )
        for number, row in enumerate(reader, start=2):
            try:
                gps_rows.append(
                    GPSPhaseKey(
                        observation_id=str(
                            row["observation_id"]
                        ),
                        animal_id=str(row["animal_id"]),
                        animal_year=str(
                            row["animal_year"]
                        ),
                        group=str(row["group"]),
                        timestamp=parse_time(
                            row["timestamp"]
                        ),
                        pixel_id=str(row["pixel_id"]),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid GPS row {number}: {exc}"
                ) from exc

    irg_rows = []
    with args.peak_irg_csv.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        reader = csv.DictReader(handle)
        required = {
            "pixel_id",
            "year",
            "modis_product",
            "reconstruction_lane",
            "peak_irg_date",
        }
        if reader.fieldnames is None:
            raise SystemExit(
                "peak-IRG CSV has no header row"
            )
        missing = required.difference(
            reader.fieldnames
        )
        if missing:
            raise SystemExit(
                "peak-IRG CSV missing required columns: "
                + ", ".join(sorted(missing))
            )
        for number, row in enumerate(reader, start=2):
            try:
                irg_rows.append(
                    PeakIRGRecord(
                        pixel_id=str(row["pixel_id"]),
                        year=int(row["year"]),
                        modis_product=str(
                            row["modis_product"]
                        ),
                        reconstruction_lane=str(
                            row["reconstruction_lane"]
                        ),
                        peak_irg_date=str(
                            row["peak_irg_date"]
                        ),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid peak-IRG row {number}: {exc}"
                ) from exc

    try:
        audit = attach_peak_irg_to_gps(
            gps_rows,
            irg_rows,
            required_modis_product=(
                args.required_modis_product
            ),
            minimum_matched_fraction=(
                args.minimum_matched_fraction
            ),
            enforce_minimum=(
                not args.allow_below_minimum
            ),
        )
    except ValueError as exc:
        raise SystemExit(
            f"environmental join failed: {exc}"
        ) from exc

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with args.output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        fieldnames = [
            "observation_id",
            "animal_id",
            "animal_year",
            "group",
            "timestamp",
            "pixel_id",
            "local_peak_irg_timestamp",
            "modis_product",
            "reconstruction_lane",
        ]
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        for row in audit.annotated:
            writer.writerow(
                {
                    "observation_id": row.observation_id,
                    "animal_id": row.animal_id,
                    "animal_year": row.animal_year,
                    "group": row.group,
                    "timestamp": (
                        row.timestamp.isoformat()
                    ),
                    "pixel_id": row.pixel_id,
                    "local_peak_irg_timestamp": (
                        row.local_peak_irg_timestamp.isoformat()
                    ),
                    "modis_product": row.modis_product,
                    "reconstruction_lane": (
                        row.reconstruction_lane
                    ),
                }
            )

    coverage_gate_passed = (
        audit.matched_fraction
        >= args.minimum_matched_fraction
    )
    receipt = {
        "status": (
            "environmental_phase_join_complete"
            if coverage_gate_passed
            else "environmental_phase_join_below_required_coverage"
        ),
        "coverage_gate_passed": coverage_gate_passed,
        "gps_source": str(args.gps_csv),
        "peak_irg_source": str(args.peak_irg_csv),
        "required_modis_product": (
            args.required_modis_product
        ),
        "minimum_matched_fraction": (
            args.minimum_matched_fraction
        ),
        "gps_observations": audit.gps_observations,
        "matched_observations": (
            audit.matched_observations
        ),
        "missing_observations": (
            audit.missing_observations
        ),
        "matched_fraction": audit.matched_fraction,
        "matched_by_group": dict(
            audit.matched_by_group
        ),
        "missing_by_group": dict(
            audit.missing_by_group
        ),
        "products": list(audit.products),
        "reconstruction_lanes": list(
            audit.reconstruction_lanes
        ),
        "output": str(args.output),
        "claim_boundary": (
            "join and coverage audit only; no fixed-interval "
            "phase pair or lambda outcome is estimated here"
        ),
    }
    args.receipt_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(args.receipt_output)
    print(
        "phase_environment_join "
        f"matched={audit.matched_observations}/"
        f"{audit.gps_observations} "
        f"fraction={audit.matched_fraction:.6f}"
    )


if __name__ == "__main__":
    main()
