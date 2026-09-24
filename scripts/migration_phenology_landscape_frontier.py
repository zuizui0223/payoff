#!/usr/bin/env python3
"""Resolve the finite-horizon persistence frontier on a moving landscape."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.moving_climate_landscape import (
    MovingLandscapeScenario,
    landscape_persistence_frontier,
    landscape_strategy_sweep,
    terminal_nonnegative_growth_velocity_ceiling,
    zero_mismatch_velocity_ceiling,
)
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
        default=parse_float_list(
            "0.01,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08"
        ),
    )
    parser.add_argument(
        "--phenology-limits",
        type=parse_float_list,
        default=parse_float_list("0,1,2,3,4,5"),
    )
    parser.add_argument("--patches", type=int, default=41)
    parser.add_argument("--patch-spacing", type=float, default=1.0)
    parser.add_argument("--spatial-gradient", type=float, default=0.20)
    parser.add_argument("--phenology-scale", type=float, default=1.0)
    parser.add_argument("--initial-distribution-sd", type=float, default=2.0)
    parser.add_argument("--carrying-capacity", type=float, default=1000.0)
    parser.add_argument("--density-coefficient", type=float, default=0.30)
    parser.add_argument("--extinction-threshold", type=float, default=1.0)
    parser.add_argument("--boundary-retention", type=float, default=1.0)
    parser.add_argument("--baseline-growth", type=float, default=0.30)
    parser.add_argument("--interaction-strength", type=float, default=0.25)
    parser.add_argument("--migration-cost", type=float, default=0.03)
    parser.add_argument("--phenology-cost", type=float, default=0.03)
    parser.add_argument("--joint-cost", type=float, default=0.0)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=160)
    parser.add_argument("--burn-in", type=int, default=40)
    parser.add_argument("--max-migration-rate", type=float, default=1.0)
    parser.add_argument("--max-phenology-rate", type=float, default=1.0)
    parser.add_argument("--migration-points", type=int, default=7)
    parser.add_argument("--phenology-points", type=int, default=7)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_landscape_frontier_grid.csv"
        ),
    )
    parser.add_argument(
        "--frontier-output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_landscape_frontier_summary.csv"
        ),
    )
    args = parser.parse_args()

    parameters = SpeciesTrackingParameters(
        abiotic_strength=args.abiotic_strength,
        interaction_strength=args.interaction_strength,
        migration_cost=args.migration_cost,
        phenology_cost=args.phenology_cost,
        joint_cost=args.joint_cost,
        baseline_growth=args.baseline_growth,
    )
    scenario = MovingLandscapeScenario(
        patches=args.patches,
        patch_spacing=args.patch_spacing,
        spatial_gradient=args.spatial_gradient,
        climate_velocity=0.0,
        phenology_scale=args.phenology_scale,
        max_abs_phenology_shift=0.0,
        initial_distribution_sd=args.initial_distribution_sd,
        carrying_capacity=args.carrying_capacity,
        density_coefficient=args.density_coefficient,
        extinction_threshold=args.extinction_threshold,
        boundary_retention=args.boundary_retention,
        steps=args.steps,
        burn_in=args.burn_in,
        species_a=parameters,
        species_b=parameters,
    )

    rows = landscape_strategy_sweep(
        scenario,
        args.climate_velocities,
        args.phenology_limits,
        max_migration_rate=args.max_migration_rate,
        max_phenology_rate=args.max_phenology_rate,
        migration_points=args.migration_points,
        phenology_points=args.phenology_points,
    )
    frontier = landscape_persistence_frontier(rows)

    for row in frontier:
        limit = float(row["phenology_limit"])
        limit_scenario = MovingLandscapeScenario(
            patches=scenario.patches,
            patch_spacing=scenario.patch_spacing,
            spatial_gradient=scenario.spatial_gradient,
            climate_velocity=0.0,
            phenology_scale=scenario.phenology_scale,
            max_abs_phenology_shift=limit,
            initial_distribution_sd=scenario.initial_distribution_sd,
            carrying_capacity=scenario.carrying_capacity,
            density_coefficient=scenario.density_coefficient,
            extinction_threshold=scenario.extinction_threshold,
            steps=scenario.steps,
            burn_in=scenario.burn_in,
            species_a=scenario.species_a,
            species_b=scenario.species_b,
        )
        zero_ceiling = zero_mismatch_velocity_ceiling(
            limit_scenario
        )
        row["zero_mismatch_velocity_ceiling"] = zero_ceiling

        migration = row["migration_rate_at_frontier"]
        phenology = row["phenology_rate_at_frontier"]
        max_velocity = row["max_persisted_velocity"]
        if (
            migration is not None
            and phenology is not None
            and max_velocity is not None
        ):
            strategy = TrackingStrategy(
                float(migration),
                float(phenology),
            )
            terminal_ceiling = (
                terminal_nonnegative_growth_velocity_ceiling(
                    limit_scenario,
                    strategy,
                    parameters,
                )
            )
            row["terminal_growth_velocity_ceiling"] = (
                terminal_ceiling
            )
            row["frontier_minus_zero_ceiling"] = (
                float(max_velocity) - zero_ceiling
            )
            row["frontier_minus_terminal_ceiling"] = (
                None
                if terminal_ceiling is None
                else float(max_velocity) - terminal_ceiling
            )
        else:
            row["terminal_growth_velocity_ceiling"] = None
            row["frontier_minus_zero_ceiling"] = None
            row["frontier_minus_terminal_ceiling"] = None

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

    args.frontier_output.parent.mkdir(parents=True, exist_ok=True)
    with args.frontier_output.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(frontier[0]) if frontier else [],
        )
        writer.writeheader()
        writer.writerows(frontier)

    print(
        f"{args.output} cells={len(rows)} "
        f"{args.frontier_output} limits={len(frontier)}"
    )
    for row in frontier:
        print(
            "frontier "
            f"phenology_limit={row['phenology_limit']} "
            f"max_persisted_velocity={row['max_persisted_velocity']} "
            f"first_failed_velocity={row['first_failed_velocity_above']} "
            f"monotone={row['monotone_persistence']} "
            f"outcome={row['outcome_at_frontier']} "
            f"migration={row['migration_rate_at_frontier']} "
            f"phenology={row['phenology_rate_at_frontier']} "
            f"edge_mass={row['right_edge_mass_at_frontier']} "
            f"limit_fraction={row['phenology_limit_fraction_at_frontier']} "
            f"zero_ceiling={row['zero_mismatch_velocity_ceiling']} "
            f"terminal_ceiling={row['terminal_growth_velocity_ceiling']} "
            f"frontier_minus_terminal={row['frontier_minus_terminal_ceiling']}"
        )


if __name__ == "__main__":
    main()
