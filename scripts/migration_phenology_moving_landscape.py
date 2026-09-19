#!/usr/bin/env python3
"""Sweep explicit moving-climate landscapes over climate speed and phenology limit."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.moving_climate_landscape import (
    MovingLandscapeScenario,
    landscape_strategy_sweep,
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
        "--climate-velocities",
        type=parse_float_list,
        default=parse_float_list("0.01,0.03,0.05,0.08"),
    )
    parser.add_argument(
        "--phenology-limits",
        type=parse_float_list,
        default=parse_float_list("0,1,2,4"),
    )
    parser.add_argument("--patches", type=int, default=41)
    parser.add_argument("--patch-spacing", type=float, default=1.0)
    parser.add_argument("--spatial-gradient", type=float, default=0.20)
    parser.add_argument("--phenology-scale", type=float, default=1.0)
    parser.add_argument("--initial-distribution-sd", type=float, default=2.0)
    parser.add_argument("--carrying-capacity", type=float, default=1000.0)
    parser.add_argument("--density-coefficient", type=float, default=0.30)
    parser.add_argument("--extinction-threshold", type=float, default=1.0)
    parser.add_argument("--baseline-growth", type=float, default=0.30)
    parser.add_argument("--interaction-strength", type=float, default=0.25)
    parser.add_argument("--migration-cost", type=float, default=0.03)
    parser.add_argument("--phenology-cost", type=float, default=0.03)
    parser.add_argument("--joint-cost", type=float, default=0.0)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=160)
    parser.add_argument("--burn-in", type=int, default=40)
    parser.add_argument("--max-migration-rate", type=float, default=1.0)
    parser.add_argument("--max-phenology-rate", type=float, default=1.0)
    parser.add_argument("--migration-points", type=int, default=9)
    parser.add_argument("--phenology-points", type=int, default=9)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_moving_landscape.csv"
        ),
    )
    args = parser.parse_args()

    parameters = SpeciesTrackingParameters(
        abiotic_strength=args.abiotic_strength,
        interaction_strength=args.interaction_strength,
        migration_cost=args.migration_cost,
        phenology_cost=args.phenology_cost,
        joint_cost=args.joint_cost,
        baseline_growth=args.baseline_growth,
    )
    scenario = MovingLandscapeScenario(
        patches=args.patches,
        patch_spacing=args.patch_spacing,
        spatial_gradient=args.spatial_gradient,
        climate_velocity=0.0,
        phenology_scale=args.phenology_scale,
        max_abs_phenology_shift=0.0,
        initial_distribution_sd=args.initial_distribution_sd,
        carrying_capacity=args.carrying_capacity,
        density_coefficient=args.density_coefficient,
        extinction_threshold=args.extinction_threshold,
        steps=args.steps,
        burn_in=args.burn_in,
        species_a=parameters,
        species_b=parameters,
    )

    rows = landscape_strategy_sweep(
        scenario,
        args.climate_velocities,
        args.phenology_limits,
        max_migration_rate=args.max_migration_rate,
        max_phenology_rate=args.max_phenology_rate,
        migration_points=args.migration_points,
        phenology_points=args.phenology_points,
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

    counts: dict[str, int] = {}
    for row in rows:
        outcome = str(row["outcome"])
        counts[outcome] = counts.get(outcome, 0) + 1

    edge_cell = max(
        rows,
        key=lambda row: float(row["right_edge_mass_fraction"]),
    )
    mismatch_cell = max(
        rows,
        key=lambda row: float(row["rms_abiotic_mismatch"]),
    )
    print(
        f"{args.output} cells={len(rows)} "
        + " ".join(
            f"{name}={counts[name]}"
            for name in sorted(counts)
        )
    )
    print(
        "max_edge_mass="
        f"{edge_cell['right_edge_mass_fraction']:.12g} "
        f"velocity={edge_cell['climate_velocity']} "
        f"phenology_limit={edge_cell['phenology_limit']} "
        f"outcome={edge_cell['outcome']}"
    )
    print(
        "max_abiotic_mismatch="
        f"{mismatch_cell['rms_abiotic_mismatch']:.12g} "
        f"velocity={mismatch_cell['climate_velocity']} "
        f"phenology_limit={mismatch_cell['phenology_limit']} "
        f"outcome={mismatch_cell['outcome']}"
    )


if __name__ == "__main__":
    main()
