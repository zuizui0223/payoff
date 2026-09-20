#!/usr/bin/env python3
"""Sensitivity of the canonical 2D coordination gate to distributional overlap."""

from __future__ import annotations

import argparse
import csv
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
    audit_landscape_2d_coordination_gate,
    landscape_2d_coordination_barrier_diagnostic,
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
        "--overlap-scales",
        type=parse_float_list,
        default=parse_float_list("0,0.5,1,2"),
    )
    parser.add_argument("--interaction-strength", type=float, default=1.0)
    parser.add_argument("--climate-velocity", type=float, default=0.06)
    parser.add_argument("--phenology-limit", type=float, default=4.0)
    parser.add_argument("--width", type=int, default=31)
    parser.add_argument("--height", type=int, default=15)
    parser.add_argument("--first-wall-offset", type=int, default=3)
    parser.add_argument("--second-wall-offset", type=int, default=7)
    parser.add_argument("--detour-offset", type=int, default=5)
    parser.add_argument("--gap-width", type=int, default=1)
    parser.add_argument("--migration-cost", type=float, default=0.10)
    parser.add_argument("--phenology-cost", type=float, default=0.02)
    parser.add_argument("--baseline-growth", type=float, default=0.35)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--initial-total-abundance", type=float, default=400.0)
    parser.add_argument("--local-carrying-capacity", type=float, default=80.0)
    parser.add_argument("--density-coefficient", type=float, default=0.35)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--burn-in", type=int, default=20)
    parser.add_argument("--mutation-step", type=float, default=0.2)
    parser.add_argument("--max-rate", type=float, default=1.0)
    parser.add_argument("--max-cycles", type=int, default=60)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_2d_overlap_sensitivity.csv"
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
    parameters = SpeciesTrackingParameters(
        abiotic_strength=args.abiotic_strength,
        interaction_strength=args.interaction_strength,
        migration_cost=args.migration_cost,
        phenology_cost=args.phenology_cost,
        baseline_growth=args.baseline_growth,
    )
    resident = TrackingStrategy(0.2, 0.0)
    neighbor = TrackingStrategy(0.2, 0.2)

    rows = []
    for overlap_scale in args.overlap_scales:
        scenario = MovingLandscape2DScenario(
            width=args.width,
            height=args.height,
            climate_velocity=args.climate_velocity,
            max_abs_phenology_shift=args.phenology_limit,
            initial_total_abundance=args.initial_total_abundance,
            local_carrying_capacity=args.local_carrying_capacity,
            density_coefficient=args.density_coefficient,
            distribution_overlap_scale=overlap_scale,
            habitat_quality=habitat,
            steps=args.steps,
            burn_in=args.burn_in,
            species_a=parameters,
            species_b=parameters,
        )
        diagnostic = landscape_2d_coordination_barrier_diagnostic(
            scenario,
            mutation_step=args.mutation_step,
            max_migration_rate=args.max_rate,
            max_phenology_rate=args.max_rate,
            max_cycles=args.max_cycles,
        )
        audit = audit_landscape_2d_coordination_gate(
            scenario,
            resident,
            neighbor,
        )
        local = diagnostic.local.final
        matched = diagnostic.matched_optimum

        rows.append(
            {
                "distribution_overlap_scale": overlap_scale,
                "barrier": int(diagnostic.barrier),
                "persistence_rescue": int(
                    diagnostic.persistence_rescue
                ),
                "accessibility_gap": diagnostic.accessibility_gap,
                "local_a_migration": local.strategy_a.migration_rate,
                "local_a_phenology": local.strategy_a.phenology_rate,
                "local_b_migration": local.strategy_b.migration_rate,
                "local_b_phenology": local.strategy_b.phenology_rate,
                "matched_migration": matched.strategy_a.migration_rate,
                "matched_phenology": matched.strategy_a.phenology_rate,
                "local_joint_growth": local.mean_joint_growth,
                "matched_joint_growth": matched.mean_joint_growth,
                "local_mean_distribution_overlap": (
                    local.mean_distribution_overlap
                ),
                "matched_mean_distribution_overlap": (
                    matched.mean_distribution_overlap
                ),
                "fixed_gate": int(audit.coordination_gate),
                "fixed_coordinated_gain": (
                    audit.coordinated_joint_gain
                ),
                "fixed_unilateral_gain_a": (
                    audit.unilateral_gain_a
                ),
                "fixed_unilateral_gain_b": (
                    audit.unilateral_gain_b
                ),
                "fixed_unilateral_overlap_a": (
                    audit.unilateral_a.mean_distribution_overlap
                ),
                "fixed_unilateral_overlap_b": (
                    audit.unilateral_b.mean_distribution_overlap
                ),
                "fixed_unilateral_mismatch_a": (
                    audit.unilateral_a.rms_interaction_mismatch
                ),
                "fixed_unilateral_mismatch_b": (
                    audit.unilateral_b.rms_interaction_mismatch
                ),
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
    for row in rows:
        print(
            "overlap_sensitivity "
            f"scale={row['distribution_overlap_scale']} "
            f"barrier={row['barrier']} "
            f"rescue={row['persistence_rescue']} "
            f"gap={row['accessibility_gap']:.12g} "
            f"fixed_gate={row['fixed_gate']} "
            f"coordinated_gain={row['fixed_coordinated_gain']:.12g} "
            f"unilateral_gain={row['fixed_unilateral_gain_a']:.12g} "
            f"unilateral_overlap={row['fixed_unilateral_overlap_a']:.12g} "
            f"unilateral_mismatch={row['fixed_unilateral_mismatch_a']:.12g}"
        )


if __name__ == "__main__":
    main()
