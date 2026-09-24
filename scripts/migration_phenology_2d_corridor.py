#!/usr/bin/env python3
"""Sweep 2D corridor bottlenecks under moving climate and phenology limits."""

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
    corridor_persistence_frontier,
    optimize_matched_2d_strategy,
    vertical_barrier_habitat,
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
        default=parse_float_list("0.02,0.03,0.04"),
    )
    parser.add_argument(
        "--phenology-limits",
        type=parse_float_list,
        default=parse_float_list("0,2,4"),
    )
    parser.add_argument(
        "--gap-widths",
        type=parse_int_list,
        default=parse_int_list("1,3,7,21"),
    )
    parser.add_argument("--width", type=int, default=41)
    parser.add_argument("--height", type=int, default=21)
    parser.add_argument(
        "--barrier-x-offset",
        type=int,
        default=5,
        help="barrier column offset east of the centered initial optimum",
    )
    parser.add_argument(
        "--gap-center-offset",
        type=int,
        default=0,
        help="corridor center offset in the transverse y direction",
    )
    parser.add_argument("--patch-spacing", type=float, default=1.0)
    parser.add_argument("--spatial-gradient", type=float, default=0.20)
    parser.add_argument("--initial-distribution-sd", type=float, default=2.0)
    parser.add_argument("--initial-total-abundance", type=float, default=500.0)
    parser.add_argument("--local-carrying-capacity", type=float, default=100.0)
    parser.add_argument("--density-coefficient", type=float, default=0.30)
    parser.add_argument("--extinction-threshold", type=float, default=1.0)
    parser.add_argument("--baseline-growth", type=float, default=0.30)
    parser.add_argument("--interaction-strength", type=float, default=0.25)
    parser.add_argument("--migration-cost", type=float, default=0.03)
    parser.add_argument("--phenology-cost", type=float, default=0.03)
    parser.add_argument("--joint-cost", type=float, default=0.0)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--burn-in", type=int, default=30)
    parser.add_argument("--max-migration-rate", type=float, default=1.0)
    parser.add_argument("--max-phenology-rate", type=float, default=1.0)
    parser.add_argument("--migration-points", type=int, default=7)
    parser.add_argument("--phenology-points", type=int, default=7)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_2d_corridor.csv"
        ),
    )
    parser.add_argument(
        "--frontier-output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_2d_corridor_frontier.csv"
        ),
    )
    args = parser.parse_args()

    if args.width % 2 == 0 or args.height % 2 == 0:
        raise SystemExit("--width and --height must be odd")
    barrier_x_index = args.width // 2 + args.barrier_x_offset
    if not 0 <= barrier_x_index < args.width:
        raise SystemExit("barrier column lies outside the landscape")
    barrier_x_position = (
        barrier_x_index - args.width // 2
    ) * args.patch_spacing
    gap_center_y_index = (
        args.height // 2 + args.gap_center_offset
    )
    if not 0 <= gap_center_y_index < args.height:
        raise SystemExit("gap center lies outside the landscape")

    parameters = SpeciesTrackingParameters(
        abiotic_strength=args.abiotic_strength,
        interaction_strength=args.interaction_strength,
        migration_cost=args.migration_cost,
        phenology_cost=args.phenology_cost,
        joint_cost=args.joint_cost,
        baseline_growth=args.baseline_growth,
    )

    rows = []
    for gap_width in args.gap_widths:
        habitat = vertical_barrier_habitat(
            args.width,
            args.height,
            barrier_x_index=barrier_x_index,
            gap_width=gap_width,
            gap_center_y_index=gap_center_y_index,
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
                    monitor_climate_coordinate=barrier_x_position,
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
                        "gap_width": gap_width,
                        "gap_center_offset": args.gap_center_offset,
                        "open_fraction": gap_width / args.height,
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
                        "final_fraction_beyond_barrier": 0.5
                        * (
                            best.final_monitor_fraction_a
                            + best.final_monitor_fraction_b
                        ),
                        "mean_fraction_beyond_barrier": 0.5
                        * (
                            best.mean_monitor_fraction_a
                            + best.mean_monitor_fraction_b
                        ),
                        "final_climate_centroid": 0.5
                        * (
                            best.final_climate_centroid_a
                            + best.final_climate_centroid_b
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

    frontier = corridor_persistence_frontier(rows)
    args.frontier_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with args.frontier_output.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(frontier[0]) if frontier else [],
        )
        writer.writeheader()
        writer.writerows(frontier)

    print(
        f"{args.output} cells={len(rows)} "
        f"{args.frontier_output} frontier_rows={len(frontier)}"
    )
    for gap_width in args.gap_widths:
        subset = [
            row for row in rows
            if int(row["gap_width"]) == gap_width
        ]
        persistence = sum(
            int(row["joint_persisted"])
            for row in subset
        )
        mean_crossing = sum(
            float(row["mean_fraction_beyond_barrier"])
            for row in subset
        ) / len(subset)
        print(
            "corridor_summary "
            f"gap_width={gap_width} "
            f"persisted={persistence}/{len(subset)} "
            f"mean_crossing={mean_crossing:.12g}"
        )

    rescue_candidates = [
        row
        for row in rows
        if int(row["joint_persisted"]) == 1
        and float(row["phenology_limit"]) > 0.0
    ]
    if rescue_candidates:
        strongest = max(
            rescue_candidates,
            key=lambda row: float(
                row["mean_joint_low_density_growth"]
            ),
        )
        print(
            "best_persisting_cell "
            f"gap_width={strongest['gap_width']} "
            f"velocity={strongest['climate_velocity']} "
            f"phenology_limit={strongest['phenology_limit']} "
            f"migration={strongest['migration_rate']} "
            f"phenology={strongest['phenology_rate']} "
            f"crossing={strongest['mean_fraction_beyond_barrier']:.12g}"
        )


if __name__ == "__main__":
    main()

