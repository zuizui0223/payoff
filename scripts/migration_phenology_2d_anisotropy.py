#!/usr/bin/env python3
"""Test anisotropic movement against 2D zigzag route costs."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.moving_climate_landscape_2d import (
    MovingLandscape2DScenario,
    multiple_vertical_barriers_habitat,
    optimize_matched_2d_strategy,
)
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
        "--y-weight-ratios",
        type=parse_float_list,
        default=parse_float_list("1,0.5,0.25,0.1"),
    )
    parser.add_argument(
        "--climate-velocities",
        type=parse_float_list,
        default=parse_float_list("0.05,0.06,0.07"),
    )
    parser.add_argument(
        "--phenology-limits",
        type=parse_float_list,
        default=parse_float_list("0,2,4"),
    )
    parser.add_argument("--width", type=int, default=31)
    parser.add_argument("--height", type=int, default=15)
    parser.add_argument("--first-wall-offset", type=int, default=3)
    parser.add_argument("--second-wall-offset", type=int, default=7)
    parser.add_argument("--detour-offset", type=int, default=5)
    parser.add_argument("--gap-width", type=int, default=1)
    parser.add_argument("--initial-total-abundance", type=float, default=400.0)
    parser.add_argument("--local-carrying-capacity", type=float, default=80.0)
    parser.add_argument("--density-coefficient", type=float, default=0.30)
    parser.add_argument("--baseline-growth", type=float, default=0.30)
    parser.add_argument("--interaction-strength", type=float, default=0.25)
    parser.add_argument("--migration-cost", type=float, default=0.03)
    parser.add_argument("--phenology-cost", type=float, default=0.03)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--burn-in", type=int, default=20)
    parser.add_argument("--max-migration-rate", type=float, default=1.0)
    parser.add_argument("--max-phenology-rate", type=float, default=1.0)
    parser.add_argument("--migration-points", type=int, default=7)
    parser.add_argument("--phenology-points", type=int, default=7)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_2d_anisotropy.csv"
        ),
    )
    args = parser.parse_args()

    if any(value < 0.0 for value in args.y_weight_ratios):
        raise SystemExit("y-weight ratios must be non-negative")

    center_x = args.width // 2
    center_y = args.height // 2
    zigzag_habitat = multiple_vertical_barriers_habitat(
        args.width,
        args.height,
        barriers=(
            (
                center_x + args.first_wall_offset,
                args.gap_width,
                center_y + args.detour_offset,
            ),
            (
                center_x + args.second_wall_offset,
                args.gap_width,
                center_y - args.detour_offset,
            ),
        ),
    )
    open_habitat = (1.0,) * (args.width * args.height)

    parameters = SpeciesTrackingParameters(
        abiotic_strength=args.abiotic_strength,
        interaction_strength=args.interaction_strength,
        migration_cost=args.migration_cost,
        phenology_cost=args.phenology_cost,
        baseline_growth=args.baseline_growth,
    )

    rows = []
    for y_ratio in args.y_weight_ratios:
        for velocity in args.climate_velocities:
            for phenology_limit in args.phenology_limits:
                results = {}
                for geometry_name, habitat in (
                    ("open", open_habitat),
                    ("zigzag", zigzag_habitat),
                ):
                    scenario = MovingLandscape2DScenario(
                        width=args.width,
                        height=args.height,
                        climate_velocity=velocity,
                        max_abs_phenology_shift=phenology_limit,
                        initial_total_abundance=args.initial_total_abundance,
                        local_carrying_capacity=args.local_carrying_capacity,
                        density_coefficient=args.density_coefficient,
                        dispersal_x_weight=1.0,
                        dispersal_y_weight=y_ratio,
                        habitat_quality=habitat,
                        steps=args.steps,
                        burn_in=args.burn_in,
                        species_a=parameters,
                        species_b=parameters,
                    )
                    results[geometry_name] = optimize_matched_2d_strategy(
                        scenario,
                        max_migration_rate=args.max_migration_rate,
                        max_phenology_rate=args.max_phenology_rate,
                        migration_points=args.migration_points,
                        phenology_points=args.phenology_points,
                    )

                open_result = results["open"]
                zigzag = results["zigzag"]
                rows.append(
                    {
                        "y_weight_ratio": y_ratio,
                        "climate_velocity": velocity,
                        "phenology_limit": phenology_limit,
                        "open_migration": (
                            open_result.strategy_a.migration_rate
                        ),
                        "open_phenology": (
                            open_result.strategy_a.phenology_rate
                        ),
                        "zigzag_migration": (
                            zigzag.strategy_a.migration_rate
                        ),
                        "zigzag_phenology": (
                            zigzag.strategy_a.phenology_rate
                        ),
                        "open_joint_growth": (
                            open_result.mean_joint_growth
                        ),
                        "zigzag_joint_growth": zigzag.mean_joint_growth,
                        "zigzag_growth_penalty": (
                            zigzag.mean_joint_growth
                            - open_result.mean_joint_growth
                        ),
                        "open_persisted": int(
                            open_result.joint_persisted
                        ),
                        "zigzag_persisted": int(
                            zigzag.joint_persisted
                        ),
                        "persistence_loss": int(
                            open_result.joint_persisted
                            and not zigzag.joint_persisted
                        ),
                        "zigzag_rms_abiotic_mismatch": 0.5
                        * (
                            zigzag.rms_abiotic_mismatch_a
                            + zigzag.rms_abiotic_mismatch_b
                        ),
                        "zigzag_phenology_limit_fraction": 0.5
                        * (
                            zigzag.phenology_limit_fraction_a
                            + zigzag.phenology_limit_fraction_b
                        ),
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
    for y_ratio in args.y_weight_ratios:
        for phenology_limit in args.phenology_limits:
            subset = [
                row
                for row in rows
                if float(row["y_weight_ratio"]) == y_ratio
                and float(row["phenology_limit"])
                == phenology_limit
            ]
            mean_penalty = sum(
                float(row["zigzag_growth_penalty"])
                for row in subset
            ) / len(subset)
            persistence_losses = sum(
                int(row["persistence_loss"])
                for row in subset
            )
            mean_migration = sum(
                float(row["zigzag_migration"])
                for row in subset
            ) / len(subset)
            mean_phenology = sum(
                float(row["zigzag_phenology"])
                for row in subset
            ) / len(subset)
            print(
                "anisotropy_summary "
                f"y_ratio={y_ratio} "
                f"phenology_limit={phenology_limit} "
                f"mean_zigzag_penalty={mean_penalty:.12g} "
                f"persistence_losses={persistence_losses}/{len(subset)} "
                f"mean_migration={mean_migration:.12g} "
                f"mean_phenology={mean_phenology:.12g}"
            )


if __name__ == "__main__":
    main()
