#!/usr/bin/env python3
"""Audit a single coordination gate on a 2D moving landscape."""

from __future__ import annotations

import argparse
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
)
from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import SpeciesTrackingParameters


def main() -> None:
    parser = argparse.ArgumentParser()
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
    parser.add_argument("--resident-migration", type=float, default=0.2)
    parser.add_argument("--resident-phenology", type=float, default=0.0)
    parser.add_argument("--neighbor-migration", type=float, default=0.2)
    parser.add_argument("--neighbor-phenology", type=float, default=0.2)
    args = parser.parse_args()

    center_x = args.width // 2
    center_y = args.height // 2
    first_x = center_x + args.first_wall_offset
    second_x = center_x + args.second_wall_offset
    habitat = multiple_vertical_barriers_habitat(
        args.width,
        args.height,
        barriers=(
            (
                first_x,
                args.gap_width,
                center_y + args.detour_offset,
            ),
            (
                second_x,
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
    scenario = MovingLandscape2DScenario(
        width=args.width,
        height=args.height,
        climate_velocity=args.climate_velocity,
        max_abs_phenology_shift=args.phenology_limit,
        initial_total_abundance=args.initial_total_abundance,
        local_carrying_capacity=args.local_carrying_capacity,
        density_coefficient=args.density_coefficient,
        habitat_quality=habitat,
        steps=args.steps,
        burn_in=args.burn_in,
        species_a=parameters,
        species_b=parameters,
    )
    resident = TrackingStrategy(
        args.resident_migration,
        args.resident_phenology,
    )
    neighbor = TrackingStrategy(
        args.neighbor_migration,
        args.neighbor_phenology,
    )
    audit = audit_landscape_2d_coordination_gate(
        scenario,
        resident,
        neighbor,
    )

    print(
        "resident "
        f"strategy=({resident.migration_rate},{resident.phenology_rate}) "
        f"joint_growth={audit.resident.mean_joint_growth:.12g} "
        f"persisted={int(audit.resident.joint_persisted)}"
    )
    print(
        "coordinated "
        f"strategy=({neighbor.migration_rate},{neighbor.phenology_rate}) "
        f"joint_growth={audit.coordinated.mean_joint_growth:.12g} "
        f"persisted={int(audit.coordinated.joint_persisted)} "
        f"joint_gain={audit.coordinated_joint_gain:.12g}"
    )
    print(
        "unilateral_a "
        f"growth={audit.unilateral_a.mean_log_growth_a:.12g} "
        f"gain={audit.unilateral_gain_a:.12g} "
        f"interaction_mismatch="
        f"{audit.unilateral_a.rms_interaction_mismatch:.12g}"
    )
    print(
        "unilateral_b "
        f"growth={audit.unilateral_b.mean_log_growth_b:.12g} "
        f"gain={audit.unilateral_gain_b:.12g} "
        f"interaction_mismatch="
        f"{audit.unilateral_b.rms_interaction_mismatch:.12g}"
    )
    print(
        f"coordination_gate={int(audit.coordination_gate)}"
    )
    if not audit.coordination_gate:
        raise SystemExit(
            "declared 2D coordination-gate audit did not satisfy the gate"
        )


if __name__ == "__main__":
    main()
