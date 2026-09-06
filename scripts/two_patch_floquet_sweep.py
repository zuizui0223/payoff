#!/usr/bin/env python3
"""Sweep migration for a two-season two-patch PAYOFF Floquet example."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.two_patch_floquet import floquet_summary


def frange(start: float, stop: float, step: float):
    x = start
    while x <= stop + abs(step) * 1e-9:
        yield x
        x += step


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r1-a", type=float, default=-2.5)
    parser.add_argument("--r2-a", type=float, default=1.0)
    parser.add_argument("--r1-b", type=float, default=2.0)
    parser.add_argument("--r2-b", type=float, default=-1.0)
    parser.add_argument("--tau-a", type=float, default=1.0)
    parser.add_argument("--tau-b", type=float, default=1.0)
    parser.add_argument("--m-min", type=float, default=0.0)
    parser.add_argument("--m-max", type=float, default=1.0)
    parser.add_argument("--step", type=float, default=0.05)
    parser.add_argument("--output", type=Path, default=Path("outputs/two_patch_floquet_sweep.csv"))
    args = parser.parse_args()

    if args.tau_a <= 0.0 or args.tau_b <= 0.0:
        raise SystemExit("season durations must be positive")
    if args.step <= 0.0:
        raise SystemExit("--step must be positive")

    seasons = [
        (args.r1_a, args.r2_a, args.tau_a),
        (args.r1_b, args.r2_b, args.tau_b),
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "migration_rate",
                "floquet_exponent",
                "time_averaged_operator_exponent",
                "temporal_effect",
                "max_pairwise_commutator_scalar",
                "floquet_can_invade",
                "average_model_can_invade",
            ],
        )
        writer.writeheader()
        for migration in frange(args.m_min, args.m_max, args.step):
            summary = floquet_summary(seasons, migration)
            writer.writerow(
                {
                    "migration_rate": f"{migration:.12g}",
                    **{key: f"{value:.12g}" for key, value in summary.items()},
                    "floquet_can_invade": int(summary["floquet_exponent"] > 0.0),
                    "average_model_can_invade": int(
                        summary["time_averaged_operator_exponent"] > 0.0
                    ),
                }
            )

    print(args.output)


if __name__ == "__main__":
    main()
