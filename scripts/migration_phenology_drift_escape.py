#!/usr/bin/env python3
"""Sweep finite population size for drift-assisted coordination escape."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tracking_coevolution import (
    CoevolutionScenario,
    SpeciesTrackingParameters,
)
from src.tracking_finite_coevolution import (
    build_pair_growth_landscape,
    finite_coevolution_escape_ensemble,
)
from src.tracking_mutation_selection import StrategyLattice


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
        "--population-sizes",
        type=parse_int_list,
        default=parse_int_list("10,30,100,300,1000"),
    )
    parser.add_argument(
        "--selection-strengths",
        type=parse_float_list,
        default=parse_float_list("5,20"),
    )
    parser.add_argument("--interaction-strength", type=float, default=0.3)
    parser.add_argument(
        "--cost-bias",
        type=float,
        default=0.08,
        help=(
            "phenology_cost - migration_cost; positive means migration is cheaper"
        ),
    )
    parser.add_argument("--base-cost", type=float, default=0.065)
    parser.add_argument("--climate-velocity", type=float, default=0.04)
    parser.add_argument("--baseline-growth", type=float, default=0.35)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--burn-in", type=int, default=20)
    parser.add_argument("--max-rate", type=float, default=1.0)
    parser.add_argument("--grid-points", type=int, default=11)
    parser.add_argument("--mutation-events", type=int, default=20000)
    parser.add_argument(
        "--evolutionary-burn-in",
        type=int,
        default=2000,
    )
    parser.add_argument("--replicates", type=int, default=32)
    parser.add_argument("--seed", type=int, default=20260920)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_drift_escape.csv"
        ),
    )
    args = parser.parse_args()

    migration_cost = args.base_cost - 0.5 * args.cost_bias
    phenology_cost = args.base_cost + 0.5 * args.cost_bias
    if migration_cost < 0.0 or phenology_cost < 0.0:
        raise SystemExit(
            "cost bias creates a negative architecture cost"
        )

    parameters = SpeciesTrackingParameters(
        abiotic_strength=args.abiotic_strength,
        interaction_strength=args.interaction_strength,
        migration_cost=migration_cost,
        phenology_cost=phenology_cost,
        baseline_growth=args.baseline_growth,
    )
    scenario = CoevolutionScenario(
        climate_velocity=args.climate_velocity,
        steps=args.steps,
        burn_in=args.burn_in,
        species_a=parameters,
        species_b=parameters,
    )
    lattice = StrategyLattice(
        max_rate=args.max_rate,
        points=args.grid_points,
    )
    landscape = build_pair_growth_landscape(
        scenario,
        lattice,
    )

    rows = []
    for selection_strength in args.selection_strengths:
        for population_size in args.population_sizes:
            ensemble = finite_coevolution_escape_ensemble(
                landscape,
                population_size=population_size,
                selection_strength=selection_strength,
                mutation_events=args.mutation_events,
                evolutionary_burn_in=args.evolutionary_burn_in,
                replicates=args.replicates,
                seed=(
                    args.seed
                    + population_size * 1009
                    + int(round(selection_strength * 1000))
                ),
            )
            rows.append(ensemble.summary())

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
        best = max(
            rows,
            key=lambda row: float(
                row["mean_high_payoff_fraction"]
            ),
        )
        print(
            f"{args.output} cells={len(rows)} "
            f"accessibility_gap={landscape.accessibility_gap:.12g}"
        )
        print(
            "best_drift_escape "
            f"N={best['population_size']} "
            f"beta={best['selection_strength']} "
            f"escape_replicate_fraction="
            f"{best['escape_replicate_fraction']:.12g} "
            f"mean_high_payoff_fraction="
            f"{best['mean_high_payoff_fraction']:.12g} "
            f"mean_joint_growth={best['mean_joint_growth']:.12g}"
        )
        print(
            "reference_states "
            f"local={landscape.local_state} "
            f"matched={landscape.matched_state} "
            f"local_growth={landscape.local_joint_growth:.12g} "
            f"matched_growth={landscape.matched_joint_growth:.12g}"
        )
    else:
        print(f"{args.output} cells=0")


if __name__ == "__main__":
    main()
