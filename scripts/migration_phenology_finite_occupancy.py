#!/usr/bin/env python3
"""Map exact finite-N weak-mutation tracking occupancy."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.spatiotemporal_tracking import TrackingScenario
from src.tracking_finite_evolution import (
    finite_stationary_tracking_summary,
)
from src.tracking_mutation_selection import StrategyLattice


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


def parse_int_list(value: str) -> list[int]:
    values = [
        int(item.strip())
        for item in value.split(",")
        if item.strip()
    ]
    if not values:
        raise argparse.ArgumentTypeError(
            "expected at least one comma-separated integer"
        )
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--population-sizes",
        type=parse_int_list,
        default=parse_int_list("10,30,100,300"),
    )
    parser.add_argument(
        "--selection-strengths",
        type=parse_float_list,
        default=parse_float_list("1,5,20"),
    )
    parser.add_argument(
        "--partner-spatial-shares",
        type=parse_float_list,
        default=parse_float_list("0,0.5,1"),
    )
    parser.add_argument("--climate-velocity", type=float, default=0.04)
    parser.add_argument("--interaction-strength", type=float, default=0.3)
    parser.add_argument("--migration-cost", type=float, default=0.03)
    parser.add_argument("--phenology-cost", type=float, default=0.03)
    parser.add_argument("--baseline-growth", type=float, default=0.3)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--burn-in", type=int, default=20)
    parser.add_argument("--max-rate", type=float, default=1.0)
    parser.add_argument("--grid-points", type=int, default=11)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_finite_occupancy.csv"
        ),
    )
    args = parser.parse_args()

    lattice = StrategyLattice(
        max_rate=args.max_rate,
        points=args.grid_points,
    )
    rows = []
    for partner_share in args.partner_spatial_shares:
        scenario = TrackingScenario(
            climate_velocity=args.climate_velocity,
            partner_spatial_share=partner_share,
            interaction_strength=args.interaction_strength,
            migration_cost=args.migration_cost,
            phenology_cost=args.phenology_cost,
            baseline_growth=args.baseline_growth,
            steps=args.steps,
            burn_in=args.burn_in,
        )
        for population_size in args.population_sizes:
            for selection_strength in args.selection_strengths:
                summary = finite_stationary_tracking_summary(
                    scenario,
                    lattice,
                    population_size=population_size,
                    selection_strength=selection_strength,
                )
                rows.append(
                    {
                        "partner_spatial_share": partner_share,
                        **summary,
                    }
                )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with args.output.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(rows)

    if rows:
        most_diffuse = max(
            rows,
            key=lambda row: float(
                row["effective_strategy_count"]
            ),
        )
        most_concentrated = max(
            rows,
            key=lambda row: float(row["top_probability"]),
        )
        print(
            f"{args.output} cells={len(rows)} "
            f"max_effective_strategies="
            f"{most_diffuse['effective_strategy_count']:.12g} "
            f"max_top_probability="
            f"{most_concentrated['top_probability']:.12g}"
        )
    else:
        print(f"{args.output} cells=0")


if __name__ == "__main__":
    main()
