#!/usr/bin/env python3
"""Compare straight, shifted, and zigzag 2D migration corridors."""

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
    optimize_matched_2d_strategy,
    multiple_vertical_barriers_habitat,
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


def parse_int_list(value: str) -> list[int]:
    values = [
        int(item.strip())
        for item in value.split(",")
        if item.strip()
    ]
    if not values:
        raise argparse.ArgumentTypeError(
            "expected at least one comma-separated integer"
        )
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--climate-velocities",
        type=parse_float_list,
        default=parse_float_list("0.04,0.05,0.06,0.07"),
    )
    parser.add_argument(
        "--phenology-limits",
        type=parse_float_list,
        default=parse_float_list("0,2,4"),
    )
    parser.add_argument(
        "--gap-widths",
        type=parse_int_list,
        default=parse_int_list("1,3"),
    )
    parser.add_argument("--width", type=int, default=31)
    parser.add_argument("--height", type=int, default=15)
    parser.add_argument("--first-wall-offset", type=int, default=3)
    parser.add_argument("--second-wall-offset", type=int, default=7)
    parser.add_argument("--detour-offset", type=int, default=5)
    parser.add_argument("--patch-spacing", type=float, default=1.0)
    parser.add_argument("--spatial-gradient", type=float, default=0.20)
    parser.add_argument("--initial-distribution-sd", type=float, default=2.0)
    parser.add_argument("--initial-total-abundance", type=float, default=400.0)
    parser.add_argument("--local-carrying-capacity", type=float, default=80.0)
    parser.add_argument("--density-coefficient", type=float, default=0.30)
    parser.add_argument("--extinction-threshold", type=float, default=1.0)
    parser.add_argument("--baseline-growth", type=float, default=0.30)
    parser.add_argument("--interaction-strength", type=float, default=0.25)
    parser.add_argument("--migration-cost", type=float, default=0.03)
    parser.add_argument("--phenology-cost", type=float, default=0.03)
    parser.add_argument("--joint-cost", type=float, default=0.0)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--burn-in", type=int, default=20)
    parser.add_argument("--max-migration-rate", type=float, default=1.0)
    parser.add_argument("--max-phenology-rate", type=float, default=1.0)
    parser.add_argument("--migration-points", type=int, default=5)
    parser.add_argument("--phenology-points", type=int, default=5)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_2d_zigzag.csv"
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
        raise SystemExit("wall offsets must define two ordered in-landscape walls")
    if abs(args.detour_offset) >= center_y:
        raise SystemExit("--detour-offset is too large for the landscape")

    second_wall_position = (
        second_x - center_x
    ) * args.patch_spacing

    parameters = SpeciesTrackingParameters(
        abiotic_strength=args.abiotic_strength,
        interaction_strength=args.interaction_strength,
        migration_cost=args.migration_cost,
        phenology_cost=args.phenology_cost,
        joint_cost=args.joint_cost,
        baseline_growth=args.baseline_growth,
    )

    geometries = {
        "open": (),
        "straight": None,
        "shifted": None,
        "zigzag": None,
    }

    rows = []
    for gap_width in args.gap_widths:
        geometries["straight"] = (
            (first_x, gap_width, center_y),
            (second_x, gap_width, center_y),
        )
        geometries["shifted"] = (
            (
                first_x,
                gap_width,
                center_y + args.detour_offset,
            ),
            (
                second_x,
                gap_width,
                center_y + args.detour_offset,
            ),
        )
        geometries["zigzag"] = (
            (
                first_x,
                gap_width,
                center_y + args.detour_offset,
            ),
            (
                second_x,
                gap_width,
                center_y - args.detour_offset,
            ),
        )

        for geometry_name, barriers in geometries.items():
            if geometry_name == "open":
                habitat = (1.0,) * (args.width * args.height)
            else:
                assert barriers is not None
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
                        patch_spacing=args.patch_spacing,
                        spatial_gradient=args.spatial_gradient,
                        climate_velocity=velocity,
                        max_abs_phenology_shift=phenology_limit,
                        initial_distribution_sd=args.initial_distribution_sd,
                        initial_total_abundance=args.initial_total_abundance,
                        local_carrying_capacity=args.local_carrying_capacity,
                        density_coefficient=args.density_coefficient,
                        extinction_threshold=args.extinction_threshold,
                        monitor_climate_coordinate=second_wall_position,
                        habitat_quality=habitat,
                        steps=args.steps,
                        burn_in=args.burn_in,
                        species_a=parameters,
                        species_b=parameters,
                    )
                    best = optimize_matched_2d_strategy(
                        scenario,
                        max_migration_rate=args.max_migration_rate,
                        max_phenology_rate=args.max_phenology_rate,
                        migration_points=args.migration_points,
                        phenology_points=args.phenology_points,
                    )
                    migration = best.strategy_a.migration_rate
                    phenology = best.strategy_a.phenology_rate
                    total_rate = migration + phenology
                    migration_share = (
                        migration / total_rate
                        if total_rate > 0.0
                        else 0.5
                    )
                    if not best.joint_persisted:
                        outcome = "failure"
                    elif migration_share >= 2.0 / 3.0:
                        outcome = "migration"
                    elif migration_share <= 1.0 / 3.0:
                        outcome = "phenology"
                    else:
                        outcome = "mixed"

                    rows.append(
                        {
                            "geometry": geometry_name,
                            "gap_width": gap_width,
                            "climate_velocity": velocity,
                            "phenology_limit": phenology_limit,
                            "migration_rate": migration,
                            "phenology_rate": phenology,
                            "migration_share": migration_share,
                            "outcome": outcome,
                            "joint_persisted": int(
                                best.joint_persisted
                            ),
                            "mean_joint_low_density_growth": (
                                best.mean_joint_growth
                            ),
                            "mean_realized_growth": 0.5
                            * (
                                best.mean_realized_log_growth_a
                                + best.mean_realized_log_growth_b
                            ),
                            "final_total_abundance": 0.5
                            * (
                                best.final_abundance_a
                                + best.final_abundance_b
                            ),
                            "rms_abiotic_mismatch": 0.5
                            * (
                                best.rms_abiotic_mismatch_a
                                + best.rms_abiotic_mismatch_b
                            ),
                            "phenology_limit_fraction": 0.5
                            * (
                                best.phenology_limit_fraction_a
                                + best.phenology_limit_fraction_b
                            ),
                            "mean_fraction_beyond_second_wall": 0.5
                            * (
                                best.mean_monitor_fraction_a
                                + best.mean_monitor_fraction_b
                            ),
                            "final_fraction_beyond_second_wall": 0.5
                            * (
                                best.final_monitor_fraction_a
                                + best.final_monitor_fraction_b
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
    for geometry_name in ("open", "straight", "shifted", "zigzag"):
        subset = [
            row
            for row in rows
            if row["geometry"] == geometry_name
        ]
        persisted = sum(
            int(row["joint_persisted"])
            for row in subset
        )
        mean_growth = sum(
            float(row["mean_joint_low_density_growth"])
            for row in subset
        ) / len(subset)
        mean_crossing = sum(
            float(row["mean_fraction_beyond_second_wall"])
            for row in subset
        ) / len(subset)
        print(
            "geometry_summary "
            f"geometry={geometry_name} "
            f"persisted={persisted}/{len(subset)} "
            f"mean_growth={mean_growth:.12g} "
            f"mean_crossing={mean_crossing:.12g}"
        )

    for phenology_limit in args.phenology_limits:
        open_rows = {
            (
                int(row["gap_width"]),
                float(row["climate_velocity"]),
            ): row
            for row in rows
            if row["geometry"] == "open"
            and float(row["phenology_limit"]) == phenology_limit
        }
        zigzag_rows = {
            (
                int(row["gap_width"]),
                float(row["climate_velocity"]),
            ): row
            for row in rows
            if row["geometry"] == "zigzag"
            and float(row["phenology_limit"]) == phenology_limit
        }
        common = sorted(set(open_rows) & set(zigzag_rows))
        if common:
            mean_penalty = sum(
                float(
                    zigzag_rows[key][
                        "mean_joint_low_density_growth"
                    ]
                )
                - float(
                    open_rows[key][
                        "mean_joint_low_density_growth"
                    ]
                )
                for key in common
            ) / len(common)
            rescue_loss = sum(
                int(open_rows[key]["joint_persisted"])
                - int(zigzag_rows[key]["joint_persisted"])
                for key in common
            )
            print(
                "zigzag_penalty_by_phenology "
                f"phenology_limit={phenology_limit} "
                f"mean_growth_penalty={mean_penalty:.12g} "
                f"open_minus_zigzag_persistence={rescue_loss}"
            )


if __name__ == "__main__":
    main()
