#!/usr/bin/env python3
"""Test coordination-barrier robustness to landscape boundary leakage."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.moving_climate_landscape import MovingLandscapeScenario
from src.moving_landscape_coevolution import (
    landscape_coordination_barrier_diagnostic,
)
from src.tracking_coevolution import SpeciesTrackingParameters
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
        "--boundary-retentions",
        type=parse_float_list,
        default=parse_float_list("0,0.5,1"),
    )
    parser.add_argument(
        "--interaction-strengths",
        type=parse_float_list,
        default=parse_float_list("0.2,0.5,1.0"),
    )
    parser.add_argument(
        "--cost-biases",
        type=parse_float_list,
        default=parse_float_list("-0.08,0,0.08"),
    )
    parser.add_argument(
        "--climate-velocities",
        type=parse_float_list,
        default=parse_float_list("0.04,0.05"),
    )
    parser.add_argument(
        "--phenology-limits",
        type=parse_float_list,
        default=parse_float_list("2,4"),
    )
    parser.add_argument("--base-cost", type=float, default=0.06)
    parser.add_argument("--baseline-growth", type=float, default=0.30)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--joint-cost", type=float, default=0.0)
    parser.add_argument("--patches", type=int, default=31)
    parser.add_argument("--patch-spacing", type=float, default=1.0)
    parser.add_argument("--spatial-gradient", type=float, default=0.20)
    parser.add_argument("--carrying-capacity", type=float, default=800.0)
    parser.add_argument("--density-coefficient", type=float, default=0.30)
    parser.add_argument("--extinction-threshold", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--burn-in", type=int, default=30)
    parser.add_argument("--mutation-step", type=float, default=0.1)
    parser.add_argument("--max-migration-rate", type=float, default=1.0)
    parser.add_argument("--max-phenology-rate", type=float, default=1.0)
    parser.add_argument("--max-cycles", type=int, default=80)
    parser.add_argument("--gap-tolerance", type=float, default=1e-8)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_boundary_robustness.csv"
        ),
    )
    args = parser.parse_args()

    if any(
        not 0.0 <= value <= 1.0
        for value in args.boundary_retentions
    ):
        raise SystemExit(
            "boundary retentions must lie in [0,1]"
        )

    cells = [
        (
            boundary_retention,
            interaction_strength,
            cost_bias,
            climate_velocity,
            phenology_limit,
        )
        for boundary_retention in args.boundary_retentions
        for interaction_strength in args.interaction_strengths
        for cost_bias in args.cost_biases
        for climate_velocity in args.climate_velocities
        for phenology_limit in args.phenology_limits
    ]
    selected = shard_sample_indices(
        len(cells),
        args.shard_index,
        args.shard_count,
    )

    rows = []
    for cell_index in selected:
        (
            boundary_retention,
            interaction_strength,
            cost_bias,
            climate_velocity,
            phenology_limit,
        ) = cells[cell_index]

        migration_cost = args.base_cost - 0.5 * cost_bias
        phenology_cost = args.base_cost + 0.5 * cost_bias
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
        scenario = MovingLandscapeScenario(
            patches=args.patches,
            patch_spacing=args.patch_spacing,
            spatial_gradient=args.spatial_gradient,
            climate_velocity=climate_velocity,
            max_abs_phenology_shift=phenology_limit,
            carrying_capacity=args.carrying_capacity,
            density_coefficient=args.density_coefficient,
            extinction_threshold=args.extinction_threshold,
            boundary_retention=boundary_retention,
            steps=args.steps,
            burn_in=args.burn_in,
            species_a=parameters,
            species_b=parameters,
        )
        diagnostic = landscape_coordination_barrier_diagnostic(
            scenario,
            mutation_step=args.mutation_step,
            max_migration_rate=args.max_migration_rate,
            max_phenology_rate=args.max_phenology_rate,
            max_cycles=args.max_cycles,
            gap_tolerance=args.gap_tolerance,
        )

        local = diagnostic.local.final
        matched = diagnostic.matched_optimum
        rescue = (
            not local.joint_persisted
            and matched.joint_persisted
        )

        rows.append(
            {
                "cell_index": cell_index,
                "boundary_retention": boundary_retention,
                "interaction_strength": interaction_strength,
                "cost_bias": cost_bias,
                "climate_velocity": climate_velocity,
                "phenology_limit": phenology_limit,
                "barrier": int(diagnostic.barrier),
                "accessibility_gap": diagnostic.accessibility_gap,
                "persistence_rescue": int(rescue),
                "local_joint_persisted": int(local.joint_persisted),
                "matched_joint_persisted": int(matched.joint_persisted),
                "local_joint_growth": local.mean_joint_growth,
                "matched_joint_growth": matched.mean_joint_growth,
                "local_migration": local.strategy_a.migration_rate,
                "local_phenology": local.strategy_a.phenology_rate,
                "matched_migration": matched.strategy_a.migration_rate,
                "matched_phenology": matched.strategy_a.phenology_rate,
                "local_edge_mass": 0.5
                * (
                    local.right_edge_mass_fraction_a
                    + local.right_edge_mass_fraction_b
                ),
                "matched_edge_mass": 0.5
                * (
                    matched.right_edge_mass_fraction_a
                    + matched.right_edge_mass_fraction_b
                ),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with args.output.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"{args.output} cells={len(rows)}")
    for retention in args.boundary_retentions:
        subset = [
            row
            for row in rows
            if row["boundary_retention"] == retention
        ]
        if not subset:
            continue
        print(
            "boundary_summary "
            f"retention={retention} "
            f"n={len(subset)} "
            f"barriers={sum(int(row['barrier']) for row in subset)} "
            f"rescues={sum(int(row['persistence_rescue']) for row in subset)} "
            f"mean_gap="
            f"{mean(float(row['accessibility_gap']) for row in subset):.12g} "
            f"mean_local_edge_mass="
            f"{mean(float(row['local_edge_mass']) for row in subset):.12g}"
        )

    if rows:
        strongest = max(
            rows,
            key=lambda row: float(row["accessibility_gap"]),
        )
        print(
            "max_gap "
            f"retention={strongest['boundary_retention']} "
            f"gap={strongest['accessibility_gap']:.12g} "
            f"interaction={strongest['interaction_strength']} "
            f"cost_bias={strongest['cost_bias']} "
            f"velocity={strongest['climate_velocity']} "
            f"phenology_limit={strongest['phenology_limit']} "
            f"rescue={strongest['persistence_rescue']}"
        )


if __name__ == "__main__":
    main()
