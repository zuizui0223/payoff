#!/usr/bin/env python3
"""Audit a one-step coordination gate on an explicit moving landscape."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.moving_climate_landscape import MovingLandscapeScenario
from src.moving_landscape_coevolution import (
    landscape_local_coordination_gate,
)
from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import SpeciesTrackingParameters


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interaction-strength", type=float, default=0.5)
    parser.add_argument("--migration-cost", type=float, default=0.10)
    parser.add_argument("--phenology-cost", type=float, default=0.02)
    parser.add_argument("--baseline-growth", type=float, default=0.30)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--climate-velocity", type=float, default=0.05)
    parser.add_argument("--phenology-limit", type=float, default=4.0)
    parser.add_argument("--patches", type=int, default=31)
    parser.add_argument("--spatial-gradient", type=float, default=0.20)
    parser.add_argument("--carrying-capacity", type=float, default=800.0)
    parser.add_argument("--density-coefficient", type=float, default=0.30)
    parser.add_argument("--boundary-retention", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--burn-in", type=int, default=30)
    parser.add_argument("--resident-migration", type=float, default=0.2)
    parser.add_argument("--resident-phenology", type=float, default=0.0)
    parser.add_argument("--mutation-step", type=float, default=0.2)
    parser.add_argument("--max-migration-rate", type=float, default=1.0)
    parser.add_argument("--max-phenology-rate", type=float, default=1.0)
    args = parser.parse_args()

    parameters = SpeciesTrackingParameters(
        abiotic_strength=args.abiotic_strength,
        interaction_strength=args.interaction_strength,
        migration_cost=args.migration_cost,
        phenology_cost=args.phenology_cost,
        baseline_growth=args.baseline_growth,
    )
    scenario = MovingLandscapeScenario(
        patches=args.patches,
        spatial_gradient=args.spatial_gradient,
        climate_velocity=args.climate_velocity,
        max_abs_phenology_shift=args.phenology_limit,
        carrying_capacity=args.carrying_capacity,
        density_coefficient=args.density_coefficient,
        boundary_retention=args.boundary_retention,
        steps=args.steps,
        burn_in=args.burn_in,
        species_a=parameters,
        species_b=parameters,
    )
    resident = TrackingStrategy(
        args.resident_migration,
        args.resident_phenology,
    )
    gate = landscape_local_coordination_gate(
        scenario,
        resident,
        mutation_step=args.mutation_step,
        max_migration_rate=args.max_migration_rate,
        max_phenology_rate=args.max_phenology_rate,
    )

    print(
        json.dumps(
            {
                "resident_migration": gate.resident.migration_rate,
                "resident_phenology": gate.resident.phenology_rate,
                "neighbor_migration": (
                    gate.coordinated_neighbor.migration_rate
                ),
                "neighbor_phenology": (
                    gate.coordinated_neighbor.phenology_rate
                ),
                "coordinated_gain": gate.coordinated_gain,
                "unilateral_gain_a": gate.unilateral_gain_a,
                "unilateral_gain_b": gate.unilateral_gain_b,
                "unilateral_mismatch_a": gate.unilateral_mismatch_a,
                "unilateral_mismatch_b": gate.unilateral_mismatch_b,
                "blocked": gate.blocked,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
