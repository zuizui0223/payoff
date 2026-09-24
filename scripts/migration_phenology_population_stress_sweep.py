#!/usr/bin/env python3
"""Stress-test demographic expression of coordination barriers.

This preserves the full ecological barrier grid while crossing it with two
predeclared demographic stress axes:

1. low-density baseline growth, and
2. carrying capacity.

Density regulation is set equal to baseline growth by default, so a perfectly
matched zero-cost strategy retains deterministic equilibrium near K. This keeps
the abundance scale interpretable while changing recovery buffer and finite-N
demographic noise.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tracking_coevolution import (
    CoevolutionScenario,
    SpeciesTrackingParameters,
)
from src.tracking_coevolution_population import (
    coordination_barrier_population_consequence,
)
from src.tracking_population import PopulationDynamics
from src.stochastic_tracking_sweep import shard_sample_indices


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
        "--interaction-strengths",
        type=parse_float_list,
        default=parse_float_list("0,0.1,0.3,0.6,1.0"),
    )
    parser.add_argument(
        "--cost-biases",
        type=parse_float_list,
        default=parse_float_list("-0.08,-0.04,0,0.04,0.08"),
    )
    parser.add_argument(
        "--climate-velocities",
        type=parse_float_list,
        default=parse_float_list("0.02,0.04,0.06"),
    )
    parser.add_argument(
        "--baseline-growths",
        type=parse_float_list,
        default=parse_float_list("0.04,0.08,0.12"),
    )
    parser.add_argument(
        "--carrying-capacities",
        type=parse_float_list,
        default=parse_float_list("30,100,300"),
    )
    parser.add_argument("--initial-fraction", type=float, default=0.5)
    parser.add_argument("--base-cost", type=float, default=0.08)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--joint-cost", type=float, default=0.0)
    parser.add_argument("--steps", type=int, default=160)
    parser.add_argument("--burn-in", type=int, default=20)
    parser.add_argument("--mutation-step", type=float, default=0.1)
    parser.add_argument("--max-rate", type=float, default=1.0)
    parser.add_argument("--max-cycles", type=int, default=40)
    parser.add_argument("--replicates", type=int, default=32)
    parser.add_argument("--extinction-threshold", type=int, default=0)
    parser.add_argument(
        "--persistence-gain-threshold",
        type=float,
        default=0.10,
    )
    parser.add_argument("--seed", type=int, default=20260920)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_population_stress.csv"
        ),
    )
    args = parser.parse_args()

    if not 0.0 < args.initial_fraction <= 1.0:
        raise SystemExit("--initial-fraction must lie in (0,1]")
    if any(value <= 0.0 for value in args.baseline_growths):
        raise SystemExit("baseline growths must be positive")
    if any(value <= 0.0 for value in args.carrying_capacities):
        raise SystemExit("carrying capacities must be positive")

    cells = [
        (
            interaction,
            bias,
            velocity,
            baseline_growth,
            carrying_capacity,
        )
        for interaction in args.interaction_strengths
        for bias in args.cost_biases
        for velocity in args.climate_velocities
        for baseline_growth in args.baseline_growths
        for carrying_capacity in args.carrying_capacities
    ]
    selected = shard_sample_indices(
        len(cells),
        args.shard_index,
        args.shard_count,
    )

    rows = []
    for cell_index in selected:
        (
            interaction_strength,
            bias,
            climate_velocity,
            baseline_growth,
            carrying_capacity,
        ) = cells[cell_index]

        migration_cost = args.base_cost - 0.5 * bias
        phenology_cost = args.base_cost + 0.5 * bias
        if migration_cost < 0.0 or phenology_cost < 0.0:
            raise SystemExit(
                "cost bias creates a negative architecture cost"
            )

        parameters = SpeciesTrackingParameters(
            abiotic_strength=args.abiotic_strength,
            interaction_strength=interaction_strength,
            migration_cost=migration_cost,
            phenology_cost=phenology_cost,
            joint_cost=args.joint_cost,
            baseline_growth=baseline_growth,
        )
        scenario = CoevolutionScenario(
            climate_velocity=climate_velocity,
            steps=args.steps,
            burn_in=args.burn_in,
            species_a=parameters,
            species_b=parameters,
        )
        initial_population = max(
            1,
            int(round(args.initial_fraction * carrying_capacity)),
        )
        population = PopulationDynamics(
            initial_population=initial_population,
            carrying_capacity=carrying_capacity,
            density_coefficient=baseline_growth,
            extinction_threshold=args.extinction_threshold,
        )

        consequence = coordination_barrier_population_consequence(
            scenario,
            population,
            population,
            replicates=args.replicates,
            seed=args.seed + cell_index * 10_000_019,
            mutation_step=args.mutation_step,
            max_rate=args.max_rate,
            max_cycles=args.max_cycles,
        )
        local = consequence.local_population.summary()
        matched = consequence.matched_population.summary()
        local_persistence = float(
            local["joint_persistence_fraction"]
        )
        matched_persistence = float(
            matched["joint_persistence_fraction"]
        )
        gain = matched_persistence - local_persistence

        rows.append(
            {
                "cell_index": cell_index,
                "interaction_strength": interaction_strength,
                "cost_bias": bias,
                "climate_velocity": climate_velocity,
                "baseline_growth": baseline_growth,
                "carrying_capacity": carrying_capacity,
                "initial_population": initial_population,
                "barrier": int(consequence.barrier),
                "accessibility_gap": consequence.accessibility_gap,
                "local_joint_persistence": local_persistence,
                "matched_joint_persistence": matched_persistence,
                "persistence_gain": gain,
                "persistence_cost_ge_threshold": int(
                    consequence.barrier
                    and gain >= args.persistence_gain_threshold
                ),
                "local_a_migration": (
                    consequence.local_endpoint.strategy_a.migration_rate
                ),
                "local_a_phenology": (
                    consequence.local_endpoint.strategy_a.phenology_rate
                ),
                "matched_migration": (
                    consequence.matched_optimum.strategy_a.migration_rate
                ),
                "matched_phenology": (
                    consequence.matched_optimum.strategy_a.phenology_rate
                ),
                "replicates": args.replicates,
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

    barrier_rows = [row for row in rows if row["barrier"]]
    costly_rows = [
        row
        for row in barrier_rows
        if row["persistence_cost_ge_threshold"]
    ]
    print(
        f"{args.output} cells={len(rows)} "
        f"barriers={len(barrier_rows)} "
        f"barriers_with_persistence_cost={len(costly_rows)}"
    )

    if barrier_rows:
        max_row = max(
            barrier_rows,
            key=lambda row: float(row["persistence_gain"]),
        )
        print(
            "max_persistence_gain="
            f"{float(max_row['persistence_gain']):.12g} "
            f"local={max_row['local_joint_persistence']} "
            f"matched={max_row['matched_joint_persistence']} "
            f"interaction={max_row['interaction_strength']} "
            f"cost_bias={max_row['cost_bias']} "
            f"velocity={max_row['climate_velocity']} "
            f"baseline_growth={max_row['baseline_growth']} "
            f"K={max_row['carrying_capacity']}"
        )

        for carrying_capacity in args.carrying_capacities:
            subset = [
                row
                for row in barrier_rows
                if row["carrying_capacity"] == carrying_capacity
            ]
            if subset:
                print(
                    "barrier_summary_by_K "
                    f"K={carrying_capacity} "
                    f"n={len(subset)} "
                    f"mean_persistence_gain="
                    f"{mean(float(row['persistence_gain']) for row in subset):.12g} "
                    f"costly_fraction="
                    f"{mean(float(row['persistence_cost_ge_threshold']) for row in subset):.12g}"
                )

        for baseline_growth in args.baseline_growths:
            subset = [
                row
                for row in barrier_rows
                if row["baseline_growth"] == baseline_growth
            ]
            if subset:
                print(
                    "barrier_summary_by_growth "
                    f"g0={baseline_growth} "
                    f"n={len(subset)} "
                    f"mean_persistence_gain="
                    f"{mean(float(row['persistence_gain']) for row in subset):.12g} "
                    f"costly_fraction="
                    f"{mean(float(row['persistence_cost_ge_threshold']) for row in subset):.12g}"
                )

        for baseline_growth in args.baseline_growths:
            for carrying_capacity in args.carrying_capacities:
                subset = [
                    row
                    for row in barrier_rows
                    if row["baseline_growth"] == baseline_growth
                    and row["carrying_capacity"] == carrying_capacity
                ]
                if subset:
                    print(
                        "barrier_summary_by_growth_K "
                        f"g0={baseline_growth} "
                        f"K={carrying_capacity} "
                        f"n={len(subset)} "
                        f"mean_local_persistence="
                        f"{mean(float(row['local_joint_persistence']) for row in subset):.12g} "
                        f"mean_matched_persistence="
                        f"{mean(float(row['matched_joint_persistence']) for row in subset):.12g} "
                        f"mean_persistence_gain="
                        f"{mean(float(row['persistence_gain']) for row in subset):.12g} "
                        f"positive_gain_fraction="
                        f"{mean(float(row['persistence_gain'] > 0.0) for row in subset):.12g} "
                        f"costly_fraction="
                        f"{mean(float(row['persistence_cost_ge_threshold']) for row in subset):.12g}"
                    )


if __name__ == "__main__":
    main()
