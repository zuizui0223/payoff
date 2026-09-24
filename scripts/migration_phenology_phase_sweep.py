#!/usr/bin/env python3
"""Generate a migration x phenology tracking phase sweep."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.spatiotemporal_tracking import (
    TrackingScenario,
    tracking_phase_diagram,
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
        "--climate-velocities",
        type=parse_float_list,
        default=parse_float_list("0.01,0.02,0.04,0.06,0.08"),
    )
    parser.add_argument(
        "--partner-spatial-shares",
        type=parse_float_list,
        default=parse_float_list("0,0.25,0.5,0.75,1"),
    )
    parser.add_argument("--partner-tracking-fraction", type=float, default=1.0)
    parser.add_argument("--partner-lag", type=float, default=0.0)
    parser.add_argument("--phenology-scale", type=float, default=1.0)
    parser.add_argument("--abiotic-strength", type=float, default=1.0)
    parser.add_argument("--interaction-strength", type=float, default=0.25)
    parser.add_argument("--migration-cost", type=float, default=0.05)
    parser.add_argument("--phenology-cost", type=float, default=0.05)
    parser.add_argument("--joint-cost", type=float, default=0.0)
    parser.add_argument("--baseline-growth", type=float, default=0.2)
    parser.add_argument("--steps", type=int, default=240)
    parser.add_argument("--burn-in", type=int, default=60)
    parser.add_argument("--max-rate", type=float, default=1.5)
    parser.add_argument("--grid-points", type=int, default=31)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_phase_sweep.csv"
        ),
    )
    args = parser.parse_args()

    scenario = TrackingScenario(
        partner_tracking_fraction=args.partner_tracking_fraction,
        partner_lag=args.partner_lag,
        phenology_scale=args.phenology_scale,
        abiotic_strength=args.abiotic_strength,
        interaction_strength=args.interaction_strength,
        migration_cost=args.migration_cost,
        phenology_cost=args.phenology_cost,
        joint_cost=args.joint_cost,
        baseline_growth=args.baseline_growth,
        steps=args.steps,
        burn_in=args.burn_in,
    )
    rows = tracking_phase_diagram(
        scenario,
        args.climate_velocities,
        args.partner_spatial_shares,
        max_rate=args.max_rate,
        points=args.grid_points,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "climate_velocity",
        "partner_spatial_share",
        "migration_rate",
        "phenology_rate",
        "migration_share",
        "mean_log_growth",
        "abiotic_only_mean_log_growth",
        "rms_abiotic_mismatch",
        "rms_interaction_mismatch",
        "outcome",
    ]
    with args.output.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(rows)

    counts: dict[str, int] = {}
    for row in rows:
        outcome = str(row["outcome"])
        counts[outcome] = counts.get(outcome, 0) + 1

    print(args.output)
    print(
        "outcomes="
        + ",".join(
            f"{name}:{counts[name]}"
            for name in sorted(counts)
        )
    )


if __name__ == "__main__":
    main()
