#!/usr/bin/env python3
"""Validate frozen PAYOFF-B tracking controls on held-out interval data."""

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
from src.tracking_empirical_bridge import EmpiricalTrackingControls
from src.tracking_empirical_validation import validate_tracking_controls
from src.tracking_interval_calibration import (
    IntervalObservation,
    build_fixed_intervals,
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
        "--tracking-controls-json",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--interval-tolerance-fraction",
        type=float,
        default=0.10,
    )
    parser.add_argument(
        "--timing-axis-isolated",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_held_out_tracking_validation.json"
        ),
    )
    args = parser.parse_args()

    controls_receipt = json.loads(
        args.tracking_controls_json.read_text(encoding="utf-8")
    )
    payload = controls_receipt.get("tracking_controls")
    if payload is None:
        raise SystemExit(
            "tracking-controls JSON has no tracking_controls payload"
        )
    controls = EmpiricalTrackingControls(**payload)

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
        role
        for role in required
        if resolved.get(role) is None
    ]
    if missing:
        raise SystemExit(
            "held-out CSV is missing required metric interval columns: "
            + ", ".join(missing)
        )

    phase_col = resolved.get("days_from_peak")
    observations: list[IntervalObservation] = []
    for row_number, row in enumerate(rows, start=2):
        try:
            animal_id = row[resolved["animal_id"]].strip()
            if not animal_id:
                raise ValueError("animal_id is empty")
            observations.append(
                IntervalObservation(
                    animal_id=animal_id,
                    timestamp=parse_timestamp(
                        row[resolved["timestamp"]]
                    ),
                    x_metric=float(row[resolved["x_metric"]]),
                    y_metric=float(row[resolved["y_metric"]]),
                    phase_residual=(
                        _parse_optional_float(row.get(phase_col))
                        if phase_col is not None
                        else None
                    ),
                )
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise SystemExit(
                f"invalid row {row_number}: {exc}"
            ) from exc

    steps = build_fixed_intervals(
        observations,
        target_interval_seconds=(
            controls.observation_interval_seconds
        ),
        interval_tolerance_fraction=(
            args.interval_tolerance_fraction
        ),
        climate_axis_angle_degrees=(
            controls.climate_axis_angle_degrees
        ),
    )
    validation = validate_tracking_controls(
        steps,
        controls,
        timing_axis_isolated=args.timing_axis_isolated,
    )

    receipt = {
        "status": "held_out_tracking_control_validation",
        "held_out_source": str(args.csv_path),
        "tracking_controls_source": (
            str(args.tracking_controls_json)
        ),
        "observation_interval_seconds": (
            controls.observation_interval_seconds
        ),
        "latent_substeps": controls.latent_substeps,
        "decision_interval_seconds": (
            controls.decision_interval_seconds
        ),
        "retained_intervals": len(steps),
        "validation": asdict(validation),
        "claim_boundary": (
            "no parameter refitting is performed on held-out intervals; "
            "movement validation tests frozen one-step moments, and phase "
            "validation is licensed only for an independently isolated timing "
            "axis"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "held_out_tracking_validation "
        f"intervals={len(steps)} "
        f"movement_rmse="
        f"{validation.movement.dimensionless_moment_rmse:.12g} "
        f"phase_validation_licensed="
        f"{int(validation.phase.validation_licensed)} "
        f"phase_mean_error="
        f"{validation.phase.mean_log_compression_error}"
    )


if __name__ == "__main__":
    main()
