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
from src.tracking_empirical_bridge import (
    controls_from_interval_audit,
)
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
    parser.add_argument(
        "--latent-substeps",
        type=int,
        default=1,
        help=(
            "number of iid model steps represented by one retained observation "
            "interval"
        ),
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
    parser.add_argument("--spatial-gradient", type=float)
    parser.add_argument(
        "--wave-speed",
        type=float,
        help="environmental-wave displacement per model step",
    )
    parser.add_argument(
        "--wave-displacement-per-observation-interval",
        type=float,
        help=(
            "alternative to --wave-speed; divided by latent_substeps to obtain "
            "environmental-wave displacement per model step"
        ),
    )
    parser.add_argument("--phenology-scale", type=float)
    parser.add_argument("--max-abs-phenology-shift", type=float)
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
        latent_substeps=args.latent_substeps,
    )

    if (
        args.wave_speed is not None
        and args.wave_displacement_per_observation_interval is not None
    ):
        raise SystemExit(
            "supply only one of --wave-speed or "
            "--wave-displacement-per-observation-interval"
        )
    model_wave_speed = args.wave_speed
    if args.wave_displacement_per_observation_interval is not None:
        if args.latent_substeps <= 0:
            raise SystemExit("--latent-substeps must be positive")
        model_wave_speed = (
            args.wave_displacement_per_observation_interval
            / args.latent_substeps
        )

    control_args = (
        args.spatial_gradient,
        model_wave_speed,
        args.phenology_scale,
        args.max_abs_phenology_shift,
    )
    supplied = [value is not None for value in control_args]
    if any(supplied) and not all(supplied):
        raise SystemExit(
            "to build tracking controls, supply --spatial-gradient, one wave "
            "displacement option, --phenology-scale, and "
            "--max-abs-phenology-shift"
        )

    controls = None
    if all(supplied):
        try:
            controls = controls_from_interval_audit(
                audit,
                spatial_gradient=args.spatial_gradient,
                wave_speed=model_wave_speed,
                phenology_scale=args.phenology_scale,
                max_abs_phenology_shift=args.max_abs_phenology_shift,
            )
        except ValueError as exc:
            raise SystemExit(
                "tracking controls not licensed: " + str(exc)
            ) from exc

    receipt = {
        "source_file": str(args.csv_path),
        "rows": len(rows),
        "resolved_columns": resolved,
        "audit": asdict(audit),
        "tracking_controls": (
            None if controls is None else asdict(controls)
        ),
        "full_tracking_controls_ready": (
            False if controls is None else controls.full_tracking_controls_ready
        ),
        "movement_parameter_status": (
            "symmetric_kernel_licensed"
            if audit.movement.direct_inverse_licensed
            else (
                "directional_kernel_licensed"
                if audit.movement.directional_inverse_licensed
                else "not_licensed"
            )
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
            "movement inversion requires projected fixed-interval steps and "
            "compatibility with either the symmetric or directional declared "
            "one-step kernel; phase compression is not PAYOFF-B h unless the "
            "timing axis is independently isolated"
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
        f"latent_substeps={audit.latent_substeps} "
        f"model_step_seconds={audit.model_step_seconds:.12g} "
        f"symmetric_movement_licensed="
        f"{int(audit.movement.direct_inverse_licensed)} "
        f"directional_movement_licensed="
        f"{int(audit.movement.directional_inverse_licensed)} "
        f"kernel_symmetric={int(audit.movement.symmetric_kernel_compatible)} "
        f"phase_intervals={audit.phase.intervals_with_phase} "
        f"h_licensed={int(audit.phase.phenology_rate_licensed)}"
    )
    if audit.movement.inverse_failure:
        print(
            "symmetric_movement_inverse_failure="
            + audit.movement.inverse_failure
        )
    if audit.movement.directional_inverse_failure:
        print(
            "directional_movement_inverse_failure="
            + audit.movement.directional_inverse_failure
        )
    if audit.phase.mean_log_compression is not None:
        print(
            "phase_mean_log_compression="
            f"{audit.phase.mean_log_compression:.12g}"
        )
    if controls is not None:
        print(
            "tracking_controls "
            f"kernel={controls.movement_kernel_kind} "
            f"migration_rate={controls.migration_rate:.12g} "
            f"x_weight={controls.dispersal_x_weight:.12g} "
            f"y_weight={controls.dispersal_y_weight:.12g} "
            f"x_bias={controls.dispersal_x_bias:.12g} "
            f"y_bias={controls.dispersal_y_bias:.12g} "
            f"climate_velocity={controls.climate_velocity:.12g} "
            f"phenology_rate={controls.phenology_rate} "
            f"full_ready={int(controls.full_tracking_controls_ready)}"
        )


if __name__ == "__main__":
    main()
