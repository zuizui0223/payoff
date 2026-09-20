#!/usr/bin/env python3
"""Audit fixed-interval projected tracking data for PAYOFF-B calibration."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.inspect_mule_deer_source_csv import resolve_aliases
from src.tracking_interval_calibration import (
    IntervalObservation,
    audit_interval_calibration,
    parse_timestamp,
)


def _parse_optional_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    return float(text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument(
        "--target-interval-hours",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--interval-tolerance-fraction",
        type=float,
        default=0.10,
    )
    parser.add_argument("--patch-spacing", type=float, required=True)
    parser.add_argument(
        "--climate-axis-angle-degrees",
        type=float,
        default=0.0,
    )
    parser.add_argument(
        "--symmetry-tolerance",
        type=float,
        default=0.25,
    )
    parser.add_argument(
        "--timing-axis-isolated",
        action="store_true",
        help=(
            "license timing-axis h only when phase-residual transitions have "
            "already isolated timing from spatial movement and other pathways"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_interval_tracking_audit.json"
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
        resolved = resolve_aliases(list(reader.fieldnames))
        rows = list(reader)

    required = ("animal_id", "timestamp", "x_metric", "y_metric")
    missing = [
        role for role in required
        if resolved.get(role) is None
    ]
    if missing:
        if (
            resolved.get("longitude") is not None
            and resolved.get("latitude") is not None
            and (
                resolved.get("x_metric") is None
                or resolved.get("y_metric") is None
            )
        ):
            raise SystemExit(
                "CSV has geographic longitude/latitude but no metric projected "
                "x/y columns. Project coordinates first; degrees cannot be "
                "passed to the exact movement inverse."
            )
        raise SystemExit(
            "missing required interval columns: "
            + ", ".join(missing)
        )

    observations: list[IntervalObservation] = []
    phase_col = resolved.get("days_from_peak")
    for row_number, row in enumerate(rows, start=2):
        try:
            animal_id = row[resolved["animal_id"]].strip()
            if not animal_id:
                raise ValueError("animal_id is empty")
            timestamp = parse_timestamp(
                row[resolved["timestamp"]]
            )
            x_metric = float(row[resolved["x_metric"]])
            y_metric = float(row[resolved["y_metric"]])
            phase = (
                _parse_optional_float(row.get(phase_col))
                if phase_col is not None
                else None
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise SystemExit(
                f"invalid row {row_number}: {exc}"
            ) from exc

        observations.append(
            IntervalObservation(
                animal_id=animal_id,
                timestamp=timestamp,
                x_metric=x_metric,
                y_metric=y_metric,
                phase_residual=phase,
            )
        )

    audit = audit_interval_calibration(
        observations,
        target_interval_seconds=(
            args.target_interval_hours * 3600.0
        ),
        patch_spacing=args.patch_spacing,
        interval_tolerance_fraction=(
            args.interval_tolerance_fraction
        ),
        climate_axis_angle_degrees=(
            args.climate_axis_angle_degrees
        ),
        symmetry_tolerance=args.symmetry_tolerance,
        timing_axis_isolated=args.timing_axis_isolated,
    )

    receipt = {
        "source_file": str(args.csv_path),
        "rows": len(rows),
        "resolved_columns": resolved,
        "audit": asdict(audit),
        "movement_parameter_status": (
            "licensed"
            if audit.movement.direct_inverse_licensed
            else "not_licensed"
        ),
        "phenology_parameter_status": (
            "licensed_candidate"
            if audit.phase.phenology_rate_licensed
            else "not_licensed"
        ),
        "phase_controller_status": (
            "descriptive_interval_compression_available"
            if audit.phase.intervals_with_phase > 0
            else "no_interval_phase_residual"
        ),
        "claim_boundary": (
            "movement inverse is licensed only if projected fixed-interval "
            "steps are compatible with the declared symmetric one-step kernel; "
            "phase compression is not PAYOFF-B h unless the timing axis is "
            "independently isolated"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "interval_tracking_audit "
        f"retained_intervals={audit.retained_intervals} "
        f"movement_licensed={int(audit.movement.direct_inverse_licensed)} "
        f"kernel_symmetric={int(audit.movement.symmetric_kernel_compatible)} "
        f"phase_intervals={audit.phase.intervals_with_phase} "
        f"h_licensed={int(audit.phase.phenology_rate_licensed)}"
    )
    if audit.movement.inverse_failure:
        print(
            "movement_inverse_failure="
            + audit.movement.inverse_failure
        )
    if audit.phase.mean_log_compression is not None:
        print(
            "phase_mean_log_compression="
            f"{audit.phase.mean_log_compression:.12g}"
        )


if __name__ == "__main__":
    main()
