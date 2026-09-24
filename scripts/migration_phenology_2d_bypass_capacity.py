#!/usr/bin/env python3
"""Compute the 2D temporal-bypass velocity capacity diagnostic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.moving_climate_landscape_2d import (
    MovingLandscape2DScenario,
    phenology_only_capacity_velocity_ceiling,
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
        "--phenology-limits",
        type=parse_float_list,
        default=parse_float_list("0,2,4"),
    )
    parser.add_argument(
        "--phenology-rates",
        type=parse_float_list,
        default=parse_float_list("0,0.16666666666666666,0.3333333333333333"),
    )
    parser.add_argument("--width", type=int, default=31)
    parser.add_argument("--height", type=int, default=15)
    parser.add_argument("--barrier-x-offset", type=int, default=3)
    parser.add_argument("--spatial-gradient", type=float, default=0.20)
    parser.add_argument("--phenology-scale", type=float, default=1.0)
    parser.add_argument("--baseline-growth", type=float, default=0.30)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--phenology-cost", type=float, default=0.03)
    parser.add_argument("--migration-cost", type=float, default=0.03)
    parser.add_argument("--steps", type=int, default=100)
    args = parser.parse_args()

    if len(args.phenology_limits) != len(args.phenology_rates):
        raise SystemExit(
            "--phenology-limits and --phenology-rates must have equal length"
        )
    if args.width % 2 == 0 or args.height % 2 == 0:
        raise SystemExit("--width and --height must be odd")

    barrier_x = args.width // 2 + args.barrier_x_offset
    if not 1 <= barrier_x < args.width:
        raise SystemExit("barrier column must leave accessible habitat to its west")

    parameters = SpeciesTrackingParameters(
        abiotic_strength=args.abiotic_strength,
        interaction_strength=0.0,
        migration_cost=args.migration_cost,
        phenology_cost=args.phenology_cost,
        baseline_growth=args.baseline_growth,
    )

    for limit, rate in zip(
        args.phenology_limits,
        args.phenology_rates,
    ):
        scenario = MovingLandscape2DScenario(
            width=args.width,
            height=args.height,
            spatial_gradient=args.spatial_gradient,
            climate_velocity=0.0,
            phenology_scale=args.phenology_scale,
            max_abs_phenology_shift=limit,
            steps=args.steps,
            burn_in=0,
            species_a=parameters,
            species_b=parameters,
        )
        accessible = tuple(
            scenario.index(x_index, y_index)
            for x_index in range(barrier_x)
            for y_index in range(args.height)
        )
        ceiling = phenology_only_capacity_velocity_ceiling(
            scenario,
            accessible,
            phenology_rate=rate,
            parameters=parameters,
        )
        print(
            "bypass_capacity "
            f"phenology_limit={limit} "
            f"phenology_rate={rate} "
            f"velocity_ceiling={ceiling:.12g}"
        )


if __name__ == "__main__":
    main()
