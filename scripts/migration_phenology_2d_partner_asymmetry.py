#!/usr/bin/env python3
"""Explore asymmetric partner preferences for migration versus phenology in 2D."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.moving_climate_landscape_2d import (
    MovingLandscape2DScenario,
    multiple_vertical_barriers_habitat,
)
from src.moving_landscape_2d_coevolution import (
    coevolve_moving_landscape_2d_pair,
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


def axis_label(migration: float, phenology: float) -> str:
    if migration <= 1e-12 and phenology <= 1e-12:
        return "stasis"
    if migration > phenology + 1e-12:
        return "migration"
    if phenology > migration + 1e-12:
        return "phenology"
    return "balanced"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cost-biases",
        type=parse_float_list,
        default=parse_float_list("-0.08,0,0.08"),
        help=(
            "phenology_cost - migration_cost; positive means migration is cheaper"
        ),
    )
    parser.add_argument(
        "--interaction-strengths",
        type=parse_float_list,
        default=parse_float_list("0,0.5,1.0"),
    )
    parser.add_argument("--base-cost", type=float, default=0.06)
    parser.add_argument("--climate-velocity", type=float, default=0.06)
    parser.add_argument("--phenology-limit", type=float, default=4.0)
    parser.add_argument("--width", type=int, default=31)
    parser.add_argument("--height", type=int, default=15)
    parser.add_argument("--first-wall-offset", type=int, default=3)
    parser.add_argument("--second-wall-offset", type=int, default=7)
    parser.add_argument("--detour-offset", type=int, default=5)
    parser.add_argument("--gap-width", type=int, default=1)
    parser.add_argument("--baseline-growth", type=float, default=0.35)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--initial-total-abundance", type=float, default=400.0)
    parser.add_argument("--local-carrying-capacity", type=float, default=80.0)
    parser.add_argument("--density-coefficient", type=float, default=0.35)
    parser.add_argument("--distribution-overlap-scale", type=float, default=0.0)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--burn-in", type=int, default=20)
    parser.add_argument("--mutation-step", type=float, default=0.2)
    parser.add_argument("--max-rate", type=float, default=1.0)
    parser.add_argument("--max-cycles", type=int, default=60)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_2d_partner_asymmetry.csv"
        ),
    )
    args = parser.parse_args()

    center_x = args.width // 2
    center_y = args.height // 2
    habitat = multiple_vertical_barriers_habitat(
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

    rows = []
    for interaction_strength in args.interaction_strengths:
        for bias_a in args.cost_biases:
            for bias_b in args.cost_biases:
                migration_cost_a = args.base_cost - 0.5 * bias_a
                phenology_cost_a = args.base_cost + 0.5 * bias_a
                migration_cost_b = args.base_cost - 0.5 * bias_b
                phenology_cost_b = args.base_cost + 0.5 * bias_b
                if min(
                    migration_cost_a,
                    phenology_cost_a,
                    migration_cost_b,
                    phenology_cost_b,
                ) < 0.0:
                    raise SystemExit(
                        "cost bias creates a negative architecture cost"
                    )

                species_a = SpeciesTrackingParameters(
                    abiotic_strength=args.abiotic_strength,
                    interaction_strength=interaction_strength,
                    migration_cost=migration_cost_a,
                    phenology_cost=phenology_cost_a,
                    baseline_growth=args.baseline_growth,
                )
                species_b = SpeciesTrackingParameters(
                    abiotic_strength=args.abiotic_strength,
                    interaction_strength=interaction_strength,
                    migration_cost=migration_cost_b,
                    phenology_cost=phenology_cost_b,
                    baseline_growth=args.baseline_growth,
                )
                scenario = MovingLandscape2DScenario(
                    width=args.width,
                    height=args.height,
                    climate_velocity=args.climate_velocity,
                    max_abs_phenology_shift=args.phenology_limit,
                    initial_total_abundance=args.initial_total_abundance,
                    local_carrying_capacity=args.local_carrying_capacity,
                    density_coefficient=args.density_coefficient,
                    distribution_overlap_scale=(
                        args.distribution_overlap_scale
                    ),
                    habitat_quality=habitat,
                    steps=args.steps,
                    burn_in=args.burn_in,
                    species_a=species_a,
                    species_b=species_b,
                )
                result = coevolve_moving_landscape_2d_pair(
                    scenario,
                    mutation_step=args.mutation_step,
                    max_migration_rate=args.max_rate,
                    max_phenology_rate=args.max_rate,
                    max_cycles=args.max_cycles,
                )
                final = result.final
                axis_a = axis_label(
                    final.strategy_a.migration_rate,
                    final.strategy_a.phenology_rate,
                )
                axis_b = axis_label(
                    final.strategy_b.migration_rate,
                    final.strategy_b.phenology_rate,
                )
                distance = math.hypot(
                    final.strategy_a.migration_rate
                    - final.strategy_b.migration_rate,
                    final.strategy_a.phenology_rate
                    - final.strategy_b.phenology_rate,
                )
                rows.append(
                    {
                        "interaction_strength": interaction_strength,
                        "cost_bias_a": bias_a,
                        "cost_bias_b": bias_b,
                        "migration_cost_a": migration_cost_a,
                        "phenology_cost_a": phenology_cost_a,
                        "migration_cost_b": migration_cost_b,
                        "phenology_cost_b": phenology_cost_b,
                        "a_migration": (
                            final.strategy_a.migration_rate
                        ),
                        "a_phenology": (
                            final.strategy_a.phenology_rate
                        ),
                        "b_migration": (
                            final.strategy_b.migration_rate
                        ),
                        "b_phenology": (
                            final.strategy_b.phenology_rate
                        ),
                        "axis_a": axis_a,
                        "axis_b": axis_b,
                        "axis_aligned": int(axis_a == axis_b),
                        "strategy_distance": distance,
                        "interaction_mismatch": (
                            final.rms_interaction_mismatch
                        ),
                        "distribution_overlap": (
                            final.mean_distribution_overlap
                        ),
                        "joint_growth": final.mean_joint_growth,
                        "joint_persisted": int(
                            final.joint_persisted
                        ),
                        "converged": int(result.converged),
                        "cycles": result.cycles,
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
    for interaction_strength in args.interaction_strengths:
        subset = [
            row
            for row in rows
            if float(row["interaction_strength"])
            == interaction_strength
        ]
        aligned = sum(
            int(row["axis_aligned"]) for row in subset
        )
        persisted = sum(
            int(row["joint_persisted"]) for row in subset
        )
        mean_distance = sum(
            float(row["strategy_distance"])
            for row in subset
        ) / len(subset)
        mean_mismatch = sum(
            float(row["interaction_mismatch"])
            for row in subset
        ) / len(subset)
        print(
            "asymmetry_summary "
            f"interaction={interaction_strength} "
            f"axis_aligned={aligned}/{len(subset)} "
            f"persisted={persisted}/{len(subset)} "
            f"mean_strategy_distance={mean_distance:.12g} "
            f"mean_interaction_mismatch={mean_mismatch:.12g}"
        )

    opposed = [
        row
        for row in rows
        if float(row["cost_bias_a"])
        * float(row["cost_bias_b"]) < 0.0
    ]
    if opposed:
        for interaction_strength in args.interaction_strengths:
            subset = [
                row
                for row in opposed
                if float(row["interaction_strength"])
                == interaction_strength
            ]
            if subset:
                print(
                    "opposed_bias_summary "
                    f"interaction={interaction_strength} "
                    f"aligned={sum(int(row['axis_aligned']) for row in subset)}/{len(subset)} "
                    f"persisted={sum(int(row['joint_persisted']) for row in subset)}/{len(subset)} "
                    f"mean_distance="
                    f"{sum(float(row['strategy_distance']) for row in subset)/len(subset):.12g}"
                )


if __name__ == "__main__":
    main()
