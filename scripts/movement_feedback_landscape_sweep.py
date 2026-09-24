#!/usr/bin/env python3
"""Sweep state-dependent movement feedback on an explicit 2D landscape."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.movement_feedback_landscape import (
    MovementRateFeedbackController,
    simulate_controlled_moving_landscape_2d,
)
from src.moving_climate_landscape_2d import MovingLandscape2DScenario
from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import SpeciesTrackingParameters


def parse_float_list(value: str) -> list[float]:
    values = [
        float(item.strip())
        for item in value.split(",")
        if item.strip()
    ]
    if not values:
        raise argparse.ArgumentTypeError(
            "expected at least one comma-separated number"
        )
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--climate-velocities",
        type=parse_float_list,
        default=parse_float_list("0.02,0.03,0.04,0.05"),
    )
    parser.add_argument(
        "--controller-gains",
        type=parse_float_list,
        default=parse_float_list("0,0.1,0.25,0.5,1"),
    )
    parser.add_argument(
        "--phenology-rates",
        type=parse_float_list,
        default=parse_float_list("0,0.25,0.5"),
    )
    parser.add_argument("--baseline-migration-rate", type=float, default=0.1)
    parser.add_argument("--max-migration-rate", type=float, default=1.5)
    parser.add_argument("--width", type=int, default=31)
    parser.add_argument("--height", type=int, default=15)
    parser.add_argument("--spatial-gradient", type=float, default=0.20)
    parser.add_argument("--phenology-limit", type=float, default=4.0)
    parser.add_argument("--initial-total-abundance", type=float, default=400.0)
    parser.add_argument("--local-carrying-capacity", type=float, default=80.0)
    parser.add_argument("--density-coefficient", type=float, default=0.35)
    parser.add_argument("--baseline-growth", type=float, default=0.35)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--migration-cost", type=float, default=0.05)
    parser.add_argument("--phenology-cost", type=float, default=0.03)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--burn-in", type=int, default=20)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/movement_feedback_landscape_sweep.csv"
        ),
    )
    args = parser.parse_args()

    if args.max_migration_rate < args.baseline_migration_rate:
        raise SystemExit(
            "--max-migration-rate must be >= baseline migration rate"
        )

    parameters = SpeciesTrackingParameters(
        abiotic_strength=args.abiotic_strength,
        interaction_strength=0.0,
        migration_cost=args.migration_cost,
        phenology_cost=args.phenology_cost,
        joint_cost=0.0,
        baseline_growth=args.baseline_growth,
    )

    rows = []
    for velocity in args.climate_velocities:
        scenario = MovingLandscape2DScenario(
            width=args.width,
            height=args.height,
            climate_velocity=velocity,
            spatial_gradient=args.spatial_gradient,
            max_abs_phenology_shift=args.phenology_limit,
            initial_total_abundance=args.initial_total_abundance,
            local_carrying_capacity=args.local_carrying_capacity,
            density_coefficient=args.density_coefficient,
            dispersal_x_weight=1.0,
            dispersal_y_weight=0.0,
            dispersal_x_bias=1.0,
            dispersal_y_bias=0.0,
            steps=args.steps,
            burn_in=args.burn_in,
            species_a=parameters,
            species_b=parameters,
        )
        for phenology_rate in args.phenology_rates:
            strategy = TrackingStrategy(
                args.baseline_migration_rate,
                phenology_rate,
            )
            for gain in args.controller_gains:
                controller = MovementRateFeedbackController(
                    gain=gain,
                    min_migration_rate=0.0,
                    max_migration_rate=args.max_migration_rate,
                )
                result = simulate_controlled_moving_landscape_2d(
                    strategy,
                    scenario,
                    controller,
                )
                rows.append(
                    {
                        "climate_velocity": velocity,
                        "baseline_migration_rate": (
                            args.baseline_migration_rate
                        ),
                        "phenology_rate": phenology_rate,
                        "controller_gain": gain,
                        "max_migration_rate": (
                            args.max_migration_rate
                        ),
                        "mean_effective_migration_rate": (
                            result.mean_effective_migration_rate
                        ),
                        "minimum_effective_migration_rate": (
                            result.minimum_effective_migration_rate
                        ),
                        "maximum_effective_migration_rate": (
                            result.maximum_effective_migration_rate
                        ),
                        "controller_floor_fraction": (
                            result.controller_floor_fraction
                        ),
                        "controller_ceiling_fraction": (
                            result.controller_ceiling_fraction
                        ),
                        "mean_precontrol_mismatch": (
                            result.mean_precontrol_mismatch
                        ),
                        "rms_abiotic_mismatch": (
                            result.rms_abiotic_mismatch
                        ),
                        "mean_low_density_growth": (
                            result.mean_low_density_growth
                        ),
                        "mean_realized_growth": (
                            result.mean_realized_growth
                        ),
                        "final_abundance": result.final_abundance,
                        "final_climate_centroid": (
                            result.final_climate_centroid
                        ),
                        "final_phenology_shift": (
                            result.final_phenology_shift
                        ),
                        "phenology_limit_fraction": (
                            result.phenology_limit_fraction
                        ),
                        "persisted": int(result.persisted),
                    }
                )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]) if rows else [],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"{args.output} cells={len(rows)}")
    for velocity in args.climate_velocities:
        for phenology_rate in args.phenology_rates:
            subset = [
                row
                for row in rows
                if float(row["climate_velocity"]) == velocity
                and float(row["phenology_rate"]) == phenology_rate
            ]
            best = max(
                subset,
                key=lambda row: float(
                    row["mean_low_density_growth"]
                ),
            )
            fixed = next(
                row
                for row in subset
                if float(row["controller_gain"]) == 0.0
            )
            print(
                "movement_feedback_summary "
                f"velocity={velocity} "
                f"phenology_rate={phenology_rate} "
                f"best_gain={best['controller_gain']} "
                f"best_growth={best['mean_low_density_growth']:.12g} "
                f"fixed_growth={fixed['mean_low_density_growth']:.12g} "
                f"best_mismatch={best['rms_abiotic_mismatch']:.12g} "
                f"fixed_mismatch={fixed['rms_abiotic_mismatch']:.12g} "
                f"best_mean_m={best['mean_effective_migration_rate']:.12g} "
                f"ceiling_fraction={best['controller_ceiling_fraction']:.12g}"
            )


if __name__ == "__main__":
    main()
