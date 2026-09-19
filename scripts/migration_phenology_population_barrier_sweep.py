#!/usr/bin/env python3
"""Map coordination barriers and their demographic persistence consequences."""

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
        help=(
            "phenology_cost - migration_cost; positive means migration is cheaper"
        ),
    )
    parser.add_argument(
        "--climate-velocities",
        type=parse_float_list,
        default=parse_float_list("0.02,0.04,0.06"),
    )
    parser.add_argument("--base-cost", type=float, default=0.08)
    parser.add_argument("--baseline-growth", type=float, default=0.12)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--joint-cost", type=float, default=0.0)
    parser.add_argument("--steps", type=int, default=140)
    parser.add_argument("--burn-in", type=int, default=20)
    parser.add_argument("--mutation-step", type=float, default=0.1)
    parser.add_argument("--max-rate", type=float, default=1.0)
    parser.add_argument("--max-cycles", type=int, default=40)
    parser.add_argument("--replicates", type=int, default=32)
    parser.add_argument("--initial-population", type=int, default=50)
    parser.add_argument("--carrying-capacity", type=float, default=100.0)
    parser.add_argument(
        "--density-coefficient",
        type=float,
        default=0.12,
    )
    parser.add_argument(
        "--extinction-threshold",
        type=int,
        default=2,
    )
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
            "outputs/migration_phenology_population_barriers.csv"
        ),
    )
    args = parser.parse_args()

    cells = [
        (interaction, bias, velocity)
        for interaction in args.interaction_strengths
        for bias in args.cost_biases
        for velocity in args.climate_velocities
    ]
    selected = shard_sample_indices(
        len(cells),
        args.shard_index,
        args.shard_count,
    )

    population = PopulationDynamics(
        initial_population=args.initial_population,
        carrying_capacity=args.carrying_capacity,
        density_coefficient=args.density_coefficient,
        extinction_threshold=args.extinction_threshold,
    )

    rows = []
    for cell_index in selected:
        interaction_strength, bias, climate_velocity = cells[cell_index]
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
            baseline_growth=args.baseline_growth,
        )
        scenario = CoevolutionScenario(
            climate_velocity=climate_velocity,
            steps=args.steps,
            burn_in=args.burn_in,
            species_a=parameters,
            species_b=parameters,
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

        local = consequence.local_endpoint
        matched = consequence.matched_optimum
        local_population = consequence.local_population.summary()
        matched_population = consequence.matched_population.summary()
        local_persistence = float(
            local_population["joint_persistence_fraction"]
        )
        matched_persistence = float(
            matched_population["joint_persistence_fraction"]
        )
        persistence_gain = matched_persistence - local_persistence

        if not consequence.barrier:
            demographic_class = "no_coordination_barrier"
        elif persistence_gain >= args.persistence_gain_threshold:
            demographic_class = "barrier_with_persistence_cost"
        elif local_persistence == 0.0 and matched_persistence == 0.0:
            demographic_class = "barrier_both_fail"
        elif local_persistence == 1.0 and matched_persistence == 1.0:
            demographic_class = "barrier_cryptic_both_persist"
        else:
            demographic_class = "barrier_small_persistence_effect"

        rows.append(
            {
                "cell_index": cell_index,
                "interaction_strength": interaction_strength,
                "cost_bias": bias,
                "climate_velocity": climate_velocity,
                "migration_cost": migration_cost,
                "phenology_cost": phenology_cost,
                "barrier": int(consequence.barrier),
                "accessibility_gap": consequence.accessibility_gap,
                "local_a_migration": local.strategy_a.migration_rate,
                "local_a_phenology": local.strategy_a.phenology_rate,
                "local_b_migration": local.strategy_b.migration_rate,
                "local_b_phenology": local.strategy_b.phenology_rate,
                "matched_migration": matched.strategy_a.migration_rate,
                "matched_phenology": matched.strategy_a.phenology_rate,
                "local_mean_growth": 0.5
                * (
                    local.mean_log_growth_a
                    + local.mean_log_growth_b
                ),
                "matched_mean_growth": 0.5
                * (
                    matched.mean_log_growth_a
                    + matched.mean_log_growth_b
                ),
                "local_joint_persistence": local_persistence,
                "matched_joint_persistence": matched_persistence,
                "persistence_gain": persistence_gain,
                "local_mean_first_extinction_step": local_population[
                    "mean_first_extinction_step_conditional"
                ],
                "matched_mean_first_extinction_step": matched_population[
                    "mean_first_extinction_step_conditional"
                ],
                "demographic_class": demographic_class,
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

    barriers = sum(int(row["barrier"]) for row in rows)
    costly = sum(
        row["demographic_class"]
        == "barrier_with_persistence_cost"
        for row in rows
    )
    if rows:
        max_gap_row = max(
            rows,
            key=lambda row: float(row["accessibility_gap"]),
        )
        max_persistence_row = max(
            rows,
            key=lambda row: float(row["persistence_gain"]),
        )
        print(
            f"{args.output} cells={len(rows)} "
            f"barriers={barriers} "
            f"barriers_with_persistence_cost={costly}"
        )
        print(
            "max_accessibility_gap="
            f"{float(max_gap_row['accessibility_gap']):.12g} "
            f"at_interaction={max_gap_row['interaction_strength']} "
            f"cost_bias={max_gap_row['cost_bias']} "
            f"climate_velocity={max_gap_row['climate_velocity']}"
        )
        print(
            "max_persistence_gain="
            f"{float(max_persistence_row['persistence_gain']):.12g} "
            f"local={max_persistence_row['local_joint_persistence']} "
            f"matched={max_persistence_row['matched_joint_persistence']} "
            f"at_interaction={max_persistence_row['interaction_strength']} "
            f"cost_bias={max_persistence_row['cost_bias']} "
            f"climate_velocity={max_persistence_row['climate_velocity']}"
        )
    else:
        print(f"{args.output} cells=0")


if __name__ == "__main__":
    main()
