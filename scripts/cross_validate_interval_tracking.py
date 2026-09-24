#!/usr/bin/env python3
"""Grouped cross-validation for interval-level PAYOFF-B tracking controls."""

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
from src.tracking_empirical_bridge import controls_from_interval_audit
from src.tracking_empirical_split import deterministic_group_split
from src.tracking_empirical_validation import validate_tracking_controls
from src.tracking_interval_calibration import (
    IntervalObservation,
    audit_interval_calibration,
    build_fixed_intervals,
    parse_timestamp,
)


def _optional_float(value: str | None) -> float | None:
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
        "--split-unit",
        choices=("animal", "animal_year"),
        default="animal",
    )
    parser.add_argument("--holdout-fraction", type=float, default=0.2)
    parser.add_argument("--split-seed", default="PAYOFF-B")
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
    parser.add_argument(
        "--latent-substeps",
        type=int,
        default=1,
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
    )
    parser.add_argument("--spatial-gradient", type=float, required=True)
    parser.add_argument(
        "--wave-speed",
        type=float,
        help="environmental-wave displacement per model step",
    )
    parser.add_argument(
        "--wave-displacement-per-observation-interval",
        type=float,
    )
    parser.add_argument("--phenology-scale", type=float, required=True)
    parser.add_argument(
        "--max-abs-phenology-shift",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_grouped_tracking_cross_validation.json"
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
        role for role in required if resolved.get(role) is None
    ]
    if missing:
        raise SystemExit(
            "missing required projected interval columns: "
            + ", ".join(missing)
        )
    if args.split_unit == "animal_year" and resolved.get("year") is None:
        raise SystemExit(
            "--split-unit animal_year requires a year column"
        )

    animal_col = resolved["animal_id"]
    year_col = resolved.get("year")
    phase_col = resolved.get("days_from_peak")

    parsed: list[tuple[str, IntervalObservation]] = []
    groups: list[str] = []
    for row_number, row in enumerate(rows, start=2):
        try:
            animal = row[animal_col].strip()
            if not animal:
                raise ValueError("animal_id is empty")
            if args.split_unit == "animal":
                group = animal
            else:
                year = row[year_col].strip()
                if not year:
                    raise ValueError("year is empty")
                group = f"{animal}::{year}"

            observation = IntervalObservation(
                animal_id=group,
                timestamp=parse_timestamp(
                    row[resolved["timestamp"]]
                ),
                x_metric=float(row[resolved["x_metric"]]),
                y_metric=float(row[resolved["y_metric"]]),
                phase_residual=(
                    _optional_float(row.get(phase_col))
                    if phase_col is not None
                    else None
                ),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise SystemExit(
                f"invalid row {row_number}: {exc}"
            ) from exc
        parsed.append((group, observation))
        groups.append(group)

    split = deterministic_group_split(
        groups,
        holdout_fraction=args.holdout_fraction,
        seed=args.split_seed,
    )
    training_set = set(split.training_groups)
    held_set = set(split.held_out_groups)

    training_observations = [
        observation
        for group, observation in parsed
        if group in training_set
    ]
    held_observations = [
        observation
        for group, observation in parsed
        if group in held_set
    ]

    target_seconds = args.target_interval_hours * 3600.0
    if (
        args.wave_speed is not None
        and args.wave_displacement_per_observation_interval is not None
    ):
        raise SystemExit(
            "supply only one wave displacement option"
        )
    if (
        args.wave_speed is None
        and args.wave_displacement_per_observation_interval is None
    ):
        raise SystemExit(
            "supply --wave-speed or "
            "--wave-displacement-per-observation-interval"
        )
    if args.latent_substeps <= 0:
        raise SystemExit("--latent-substeps must be positive")
    model_wave_speed = args.wave_speed
    if args.wave_displacement_per_observation_interval is not None:
        model_wave_speed = (
            args.wave_displacement_per_observation_interval
            / args.latent_substeps
        )

    calibration = audit_interval_calibration(
        training_observations,
        target_interval_seconds=target_seconds,
        patch_spacing=args.patch_spacing,
        interval_tolerance_fraction=(
            args.interval_tolerance_fraction
        ),
        climate_axis_angle_degrees=(
            args.climate_axis_angle_degrees
        ),
        symmetry_tolerance=args.symmetry_tolerance,
        timing_axis_isolated=args.timing_axis_isolated,
        latent_substeps=args.latent_substeps,
    )
    controls = controls_from_interval_audit(
        calibration,
        spatial_gradient=args.spatial_gradient,
        wave_speed=model_wave_speed,
        phenology_scale=args.phenology_scale,
        max_abs_phenology_shift=args.max_abs_phenology_shift,
    )

    held_steps = build_fixed_intervals(
        held_observations,
        target_interval_seconds=target_seconds,
        interval_tolerance_fraction=(
            args.interval_tolerance_fraction
        ),
        climate_axis_angle_degrees=(
            args.climate_axis_angle_degrees
        ),
    )
    if not held_steps:
        raise SystemExit(
            "held-out groups contain no intervals matching the declared "
            "decision interval"
        )

    validation = validate_tracking_controls(
        held_steps,
        controls,
        timing_axis_isolated=args.timing_axis_isolated,
    )

    receipt = {
        "status": "grouped_out_of_sample_tracking_validation",
        "source_file": str(args.csv_path),
        "split": asdict(split),
        "split_unit": args.split_unit,
        "split_seed": args.split_seed,
        "training_rows": len(training_observations),
        "held_out_rows": len(held_observations),
        "calibration": asdict(calibration),
        "tracking_controls": asdict(controls),
        "held_out_intervals": len(held_steps),
        "held_out_validation": asdict(validation),
        "claim_boundary": (
            "groups are split before parameter identification; held-out groups "
            "are used only for validation and never refit the tracking controls"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "grouped_tracking_cross_validation "
        f"split_unit={args.split_unit} "
        f"training_groups={len(split.training_groups)} "
        f"held_out_groups={len(split.held_out_groups)} "
        f"training_intervals={calibration.retained_intervals} "
        f"latent_substeps={calibration.latent_substeps} "
        f"held_out_intervals={len(held_steps)} "
        f"movement_rmse="
        f"{validation.movement.dimensionless_moment_rmse:.12g} "
        f"phase_validation_licensed="
        f"{int(validation.phase.validation_licensed)} "
        f"phase_mean_error="
        f"{validation.phase.mean_log_compression_error}"
    )


if __name__ == "__main__":
    main()
