#!/usr/bin/env python3
"""Map coevolutionary coordination barriers across 2D route geometries."""

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
    landscape_2d_coordination_barrier_diagnostic,
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
        "--interaction-strengths",
        type=parse_float_list,
        default=parse_float_list("0,0.5,1.0"),
    )
    parser.add_argument(
        "--climate-velocities",
        type=parse_float_list,
        default=parse_float_list("0.04,0.05,0.06"),
    )
    parser.add_argument(
        "--phenology-limits",
        type=parse_float_list,
        default=parse_float_list("2,4"),
    )
    parser.add_argument("--width", type=int, default=31)
    parser.add_argument("--height", type=int, default=15)
    parser.add_argument("--first-wall-offset", type=int, default=3)
    parser.add_argument("--second-wall-offset", type=int, default=7)
    parser.add_argument("--detour-offset", type=int, default=5)
    parser.add_argument("--gap-width", type=int, default=1)
    parser.add_argument("--base-cost", type=float, default=0.06)
    parser.add_argument(
        "--cost-bias",
        type=float,
        default=-0.08,
        help=(
            "phenology_cost - migration_cost; negative means phenology is cheaper"
        ),
    )
    parser.add_argument("--baseline-growth", type=float, default=0.35)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--initial-total-abundance", type=float, default=400.0)
    parser.add_argument("--local-carrying-capacity", type=float, default=80.0)
    parser.add_argument("--density-coefficient", type=float, default=0.35)
    parser.add_argument("--extinction-threshold", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--burn-in", type=int, default=20)
    parser.add_argument("--mutation-step", type=float, default=0.2)
    parser.add_argument("--max-migration-rate", type=float, default=1.0)
    parser.add_argument("--max-phenology-rate", type=float, default=1.0)
    parser.add_argument("--max-cycles", type=int, default=40)
    parser.add_argument("--gap-tolerance", type=float, default=1e-8)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_2d_coevolution.csv"
        ),
    )
    args = parser.parse_args()

    if args.width % 2 == 0 or args.height % 2 == 0:
        raise SystemExit("--width and --height must be odd")

    center_x = args.width // 2
    center_y = args.height // 2
    first_x = center_x + args.first_wall_offset
    second_x = center_x + args.second_wall_offset
    if not (0 <= first_x < second_x < args.width):
        raise SystemExit("wall offsets must define two ordered walls")
    if abs(args.detour_offset) >= center_y:
        raise SystemExit("--detour-offset is too large")

    migration_cost = args.base_cost - 0.5 * args.cost_bias
    phenology_cost = args.base_cost + 0.5 * args.cost_bias
    if migration_cost < 0.0 or phenology_cost < 0.0:
        raise SystemExit("cost bias creates a negative cost")

    geometry_barriers = {
        "open": (),
        "straight": (
            (first_x, args.gap_width, center_y),
            (second_x, args.gap_width, center_y),
        ),
        "zigzag": (
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
    }

    rows = []
    for interaction_strength in args.interaction_strengths:
        parameters = SpeciesTrackingParameters(
            abiotic_strength=args.abiotic_strength,
            interaction_strength=interaction_strength,
            migration_cost=migration_cost,
            phenology_cost=phenology_cost,
            baseline_growth=args.baseline_growth,
        )
        for geometry_name, barriers in geometry_barriers.items():
            if geometry_name == "open":
                habitat = (1.0,) * (args.width * args.height)
            else:
                habitat = multiple_vertical_barriers_habitat(
                    args.width,
                    args.height,
                    barriers=barriers,
                )

            for velocity in args.climate_velocities:
                for phenology_limit in args.phenology_limits:
                    scenario = MovingLandscape2DScenario(
                        width=args.width,
                        height=args.height,
                        climate_velocity=velocity,
                        max_abs_phenology_shift=phenology_limit,
                        initial_total_abundance=args.initial_total_abundance,
                        local_carrying_capacity=args.local_carrying_capacity,
                        density_coefficient=args.density_coefficient,
                        extinction_threshold=args.extinction_threshold,
                        habitat_quality=habitat,
                        steps=args.steps,
                        burn_in=args.burn_in,
                        species_a=parameters,
                        species_b=parameters,
                    )
                    diagnostic = (
                        landscape_2d_coordination_barrier_diagnostic(
                            scenario,
                            mutation_step=args.mutation_step,
                            max_migration_rate=args.max_migration_rate,
                            max_phenology_rate=args.max_phenology_rate,
                            max_cycles=args.max_cycles,
                            gap_tolerance=args.gap_tolerance,
                        )
                    )
                    local = diagnostic.local.final
                    matched = diagnostic.matched_optimum
                    rows.append(
                        {
                            "interaction_strength": interaction_strength,
                            "geometry": geometry_name,
                            "climate_velocity": velocity,
                            "phenology_limit": phenology_limit,
                            "migration_cost": migration_cost,
                            "phenology_cost": phenology_cost,
                            "barrier": int(diagnostic.barrier),
                            "persistence_rescue": int(
                                diagnostic.persistence_rescue
                            ),
                            "accessibility_gap": (
                                diagnostic.accessibility_gap
                            ),
                            "local_a_migration": (
                                local.strategy_a.migration_rate
                            ),
                            "local_a_phenology": (
                                local.strategy_a.phenology_rate
                            ),
                            "local_b_migration": (
                                local.strategy_b.migration_rate
                            ),
                            "local_b_phenology": (
                                local.strategy_b.phenology_rate
                            ),
                            "matched_migration": (
                                matched.strategy_a.migration_rate
                            ),
                            "matched_phenology": (
                                matched.strategy_a.phenology_rate
                            ),
                            "local_joint_growth": (
                                local.mean_joint_growth
                            ),
                            "matched_joint_growth": (
                                matched.mean_joint_growth
                            ),
                            "local_joint_persisted": int(
                                local.joint_persisted
                            ),
                            "matched_joint_persisted": int(
                                matched.joint_persisted
                            ),
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
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"{args.output} cells={len(rows)}")
    for interaction_strength in args.interaction_strengths:
        for geometry_name in ("open", "straight", "zigzag"):
            subset = [
                row
                for row in rows
                if float(row["interaction_strength"])
                == interaction_strength
                and row["geometry"] == geometry_name
            ]
            barriers = sum(int(row["barrier"]) for row in subset)
            rescues = sum(
                int(row["persistence_rescue"])
                for row in subset
            )
            print(
                "coevolution_summary "
                f"interaction={interaction_strength} "
                f"geometry={geometry_name} "
                f"barriers={barriers}/{len(subset)} "
                f"rescues={rescues}/{len(subset)}"
            )

    barrier_rows = [row for row in rows if row["barrier"]]
    if barrier_rows:
        strongest = max(
            barrier_rows,
            key=lambda row: float(row["accessibility_gap"]),
        )
        print(
            "strongest_barrier "
            f"interaction={strongest['interaction_strength']} "
            f"geometry={strongest['geometry']} "
            f"velocity={strongest['climate_velocity']} "
            f"phenology_limit={strongest['phenology_limit']} "
            f"gap={strongest['accessibility_gap']:.12g} "
            f"rescue={strongest['persistence_rescue']}"
        )


if __name__ == "__main__":
    main()
