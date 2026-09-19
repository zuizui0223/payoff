#!/usr/bin/env python3
"""Map coevolutionary coordination barriers across interaction and cost bias."""

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
    coordination_barrier_diagnostic,
)


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
    parser.add_argument("--base-cost", type=float, default=0.08)
    parser.add_argument("--climate-velocity", type=float, default=0.04)
    parser.add_argument("--baseline-growth", type=float, default=0.35)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--joint-cost", type=float, default=0.0)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--burn-in", type=int, default=20)
    parser.add_argument("--mutation-step", type=float, default=0.1)
    parser.add_argument("--max-rate", type=float, default=1.0)
    parser.add_argument("--max-cycles", type=int, default=40)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_coordination_barriers.csv"
        ),
    )
    args = parser.parse_args()

    rows = []
    for interaction_strength in args.interaction_strengths:
        if interaction_strength < 0.0:
            raise SystemExit(
                "interaction strengths must be non-negative"
            )
        for bias in args.cost_biases:
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
                climate_velocity=args.climate_velocity,
                steps=args.steps,
                burn_in=args.burn_in,
                species_a=parameters,
                species_b=parameters,
            )
            diagnostic = coordination_barrier_diagnostic(
                scenario,
                mutation_step=args.mutation_step,
                max_rate=args.max_rate,
                max_cycles=args.max_cycles,
            )
            local = diagnostic.local.final
            matched = diagnostic.matched_optimum
            local_score = 0.5 * (
                local.mean_log_growth_a
                + local.mean_log_growth_b
            )
            matched_score = 0.5 * (
                matched.mean_log_growth_a
                + matched.mean_log_growth_b
            )
            rows.append(
                {
                    "interaction_strength": interaction_strength,
                    "cost_bias": bias,
                    "migration_cost": migration_cost,
                    "phenology_cost": phenology_cost,
                    "local_a_migration": local.strategy_a.migration_rate,
                    "local_a_phenology": local.strategy_a.phenology_rate,
                    "local_b_migration": local.strategy_b.migration_rate,
                    "local_b_phenology": local.strategy_b.phenology_rate,
                    "matched_migration": (
                        matched.strategy_a.migration_rate
                    ),
                    "matched_phenology": (
                        matched.strategy_a.phenology_rate
                    ),
                    "local_mean_growth": local_score,
                    "matched_mean_growth": matched_score,
                    "accessibility_gap": (
                        diagnostic.accessibility_gap
                    ),
                    "barrier": int(diagnostic.barrier),
                    "local_interaction_mismatch": (
                        local.rms_interaction_mismatch
                    ),
                    "converged": int(
                        diagnostic.local.converged
                    ),
                    "cycles": diagnostic.local.cycles,
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
    print(
        f"{args.output} cells={len(rows)} "
        f"barriers={barriers}"
    )


if __name__ == "__main__":
    main()
