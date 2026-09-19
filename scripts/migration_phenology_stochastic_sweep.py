#!/usr/bin/env python3
"""Run a reproducible shard of the stochastic PAYOFF-B tracking sweep."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.spatiotemporal_tracking import TrackingScenario
from src.stochastic_tracking_sweep import (
    StochasticSweepRanges,
    draw_stochastic_sweep_point,
    optimize_stochastic_strategy,
    planned_tracking_steps,
    shard_sample_indices,
    stochastic_sweep_row,
)


FIELDNAMES = [
    "sample_index",
    "climate_velocity",
    "partner_spatial_share",
    "interaction_strength",
    "migration_cost",
    "phenology_cost",
    "climate_increment_sd",
    "partner_spatial_share_sd",
    "partner_demand_noise_sd",
    "replicates",
    "strategy_points",
    "best_migration_rate",
    "best_phenology_rate",
    "best_migration_share",
    "mean_log_growth",
    "sd_log_growth",
    "mean_abiotic_only_log_growth",
    "viability_fraction",
    "interaction_failure_fraction",
    "mean_rms_abiotic_mismatch",
    "mean_rms_interaction_mismatch",
    "outcome",
]


def _existing_indices(path: Path) -> set[int]:
    if not path.exists():
        return set()
    with path.open(newline="", encoding="utf-8") as handle:
        return {
            int(row["sample_index"])
            for row in csv.DictReader(handle)
            if row.get("sample_index")
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=16)
    parser.add_argument("--replicates", type=int, default=8)
    parser.add_argument("--strategy-points", type=int, default=7)
    parser.add_argument("--max-rate", type=float, default=1.2)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--burn-in", type=int, default=30)
    parser.add_argument("--baseline-growth", type=float, default=0.3)
    parser.add_argument("--seed", type=int, default=20260919)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/migration_phenology_stochastic_sweep.csv"
        ),
    )
    args = parser.parse_args()

    if args.steps <= 0:
        raise SystemExit("--steps must be positive")
    if not 0 <= args.burn_in < args.steps:
        raise SystemExit(
            "--burn-in must satisfy 0 <= burn-in < steps"
        )

    indices = shard_sample_indices(
        args.samples,
        args.shard_index,
        args.shard_count,
    )
    workload = planned_tracking_steps(
        len(indices),
        args.strategy_points,
        args.replicates,
        args.steps,
    )
    if args.dry_run:
        print(
            f"shard_samples={len(indices)} "
            f"planned_ecological_updates={workload}"
        )
        return

    base = TrackingScenario(
        baseline_growth=args.baseline_growth,
        steps=args.steps,
        burn_in=args.burn_in,
    )
    ranges = StochasticSweepRanges()

    completed = (
        _existing_indices(args.output)
        if args.resume
        else set()
    )
    rows = []
    for sample_index in indices:
        if sample_index in completed:
            continue
        point = draw_stochastic_sweep_point(
            sample_index,
            seed=args.seed,
            base_scenario=base,
            ranges=ranges,
        )
        optimum = optimize_stochastic_strategy(
            point.scenario,
            point.forcing,
            replicates=args.replicates,
            seed=args.seed + sample_index * 10_000_019,
            max_rate=args.max_rate,
            points=args.strategy_points,
        )
        rows.append(
            stochastic_sweep_row(
                point,
                optimum,
                replicates=args.replicates,
                strategy_points=args.strategy_points,
            )
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    append = args.resume and args.output.exists()
    with args.output.open(
        "a" if append else "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=FIELDNAMES,
        )
        if not append:
            writer.writeheader()
        writer.writerows(rows)

    print(
        f"{args.output} rows_written={len(rows)} "
        f"planned_ecological_updates={workload}"
    )


if __name__ == "__main__":
    main()
