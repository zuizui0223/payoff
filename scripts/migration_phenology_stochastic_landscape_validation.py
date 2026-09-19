#!/usr/bin/env python3
"""Validate spatial coordination rescue under local demographic noise."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.moving_climate_landscape import MovingLandscapeScenario
from src.moving_landscape_coevolution import (
    landscape_coordination_barrier_diagnostic,
)
from src.stochastic_moving_landscape import (
    stochastic_moving_landscape_ensemble,
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
        "--boundary-retentions",
        type=parse_float_list,
        default=parse_float_list("0,0.5,1"),
    )
    parser.add_argument("--interaction-strength", type=float, default=0.5)
    parser.add_argument("--cost-bias", type=float, default=-0.08)
    parser.add_argument("--base-cost", type=float, default=0.06)
    parser.add_argument("--climate-velocity", type=float, default=0.05)
    parser.add_argument("--phenology-limit", type=float, default=4.0)
    parser.add_argument("--baseline-growth", type=float, default=0.30)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--patches", type=int, default=31)
    parser.add_argument("--spatial-gradient", type=float, default=0.20)
    parser.add_argument("--carrying-capacity", type=float, default=800.0)
    parser.add_argument("--density-coefficient", type=float, default=0.30)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--burn-in", type=int, default=30)
    parser.add_argument("--mutation-step", type=float, default=0.1)
    parser.add_argument("--max-rate", type=float, default=1.0)
    parser.add_argument("--max-cycles", type=int, default=80)
    parser.add_argument("--replicates", type=int, default=128)
    parser.add_argument("--seed", type=int, default=20260920)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_stochastic_landscape_validation.csv"
        ),
    )
    args = parser.parse_args()

    migration_cost = args.base_cost - 0.5 * args.cost_bias
    phenology_cost = args.base_cost + 0.5 * args.cost_bias
    if migration_cost < 0.0 or phenology_cost < 0.0:
        raise SystemExit("cost bias creates a negative architecture cost")

    rows = []
    for index, retention in enumerate(args.boundary_retentions):
        if not 0.0 <= retention <= 1.0:
            raise SystemExit("boundary retention must lie in [0,1]")

        parameters = SpeciesTrackingParameters(
            abiotic_strength=args.abiotic_strength,
            interaction_strength=args.interaction_strength,
            migration_cost=migration_cost,
            phenology_cost=phenology_cost,
            baseline_growth=args.baseline_growth,
        )
        scenario = MovingLandscapeScenario(
            patches=args.patches,
            spatial_gradient=args.spatial_gradient,
            climate_velocity=args.climate_velocity,
            max_abs_phenology_shift=args.phenology_limit,
            carrying_capacity=args.carrying_capacity,
            density_coefficient=args.density_coefficient,
            boundary_retention=retention,
            steps=args.steps,
            burn_in=args.burn_in,
            species_a=parameters,
            species_b=parameters,
        )
        diagnostic = landscape_coordination_barrier_diagnostic(
            scenario,
            mutation_step=args.mutation_step,
            max_migration_rate=args.max_rate,
            max_phenology_rate=args.max_rate,
            max_cycles=args.max_cycles,
        )
        local = diagnostic.local.final
        matched = diagnostic.matched_optimum

        replicate_seed = args.seed + index * 10_000_019
        local_ensemble = stochastic_moving_landscape_ensemble(
            local.strategy_a,
            local.strategy_b,
            scenario,
            replicates=args.replicates,
            seed=replicate_seed,
        ).summary()
        matched_ensemble = stochastic_moving_landscape_ensemble(
            matched.strategy_a,
            matched.strategy_b,
            scenario,
            replicates=args.replicates,
            seed=replicate_seed,
        ).summary()

        rows.append(
            {
                "boundary_retention": retention,
                "barrier": int(diagnostic.barrier),
                "accessibility_gap": diagnostic.accessibility_gap,
                "local_migration": local.strategy_a.migration_rate,
                "local_phenology": local.strategy_a.phenology_rate,
                "matched_migration": matched.strategy_a.migration_rate,
                "matched_phenology": matched.strategy_a.phenology_rate,
                "local_deterministic_growth": local.mean_joint_growth,
                "matched_deterministic_growth": matched.mean_joint_growth,
                "local_deterministic_persisted": int(
                    local.joint_persisted
                ),
                "matched_deterministic_persisted": int(
                    matched.joint_persisted
                ),
                "local_stochastic_persistence": float(
                    local_ensemble["joint_persistence_fraction"]
                ),
                "matched_stochastic_persistence": float(
                    matched_ensemble["joint_persistence_fraction"]
                ),
                "stochastic_persistence_gain": (
                    float(
                        matched_ensemble["joint_persistence_fraction"]
                    )
                    - float(
                        local_ensemble["joint_persistence_fraction"]
                    )
                ),
                "local_mean_final_abundance_a": float(
                    local_ensemble["mean_final_abundance_a"]
                ),
                "matched_mean_final_abundance_a": float(
                    matched_ensemble["mean_final_abundance_a"]
                ),
                "local_mean_extinction_step": local_ensemble[
                    "mean_extinction_step_conditional"
                ],
                "matched_mean_extinction_step": matched_ensemble[
                    "mean_extinction_step_conditional"
                ],
                "replicates": args.replicates,
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

    print(f"{args.output} rows={len(rows)}")
    for row in rows:
        print(
            "stochastic_boundary "
            f"retention={row['boundary_retention']} "
            f"barrier={row['barrier']} "
            f"gap={row['accessibility_gap']:.12g} "
            f"local_p={row['local_stochastic_persistence']:.12g} "
            f"matched_p={row['matched_stochastic_persistence']:.12g} "
            f"gain={row['stochastic_persistence_gain']:.12g} "
            f"local=({row['local_migration']},{row['local_phenology']}) "
            f"matched=({row['matched_migration']},{row['matched_phenology']})"
        )


if __name__ == "__main__":
    main()
