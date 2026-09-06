#!/usr/bin/env python3
"""Sweep migration across a heterogeneous two-patch PAYOFF landscape."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.environment_mosaic import (
    two_patch_invasion_exponent,
    two_patch_rescue_threshold,
)


def frange(start: float, stop: float, step: float):
    x = start
    while x <= stop + abs(step) * 1e-9:
        yield x
        x += step


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r-source", type=float, default=0.5)
    parser.add_argument("--r-sink", type=float, default=-1.5)
    parser.add_argument("--m-min", type=float, default=0.0)
    parser.add_argument("--m-max", type=float, default=1.5)
    parser.add_argument("--step", type=float, default=0.05)
    parser.add_argument("--output", type=Path, default=Path("outputs/environment_mosaic_two_patch.csv"))
    args = parser.parse_args()

    if args.r_source <= 0.0 or args.r_sink >= 0.0:
        raise SystemExit("--r-source must be positive and --r-sink negative")
    if args.r_source + args.r_sink >= 0.0:
        raise SystemExit("this sweep expects a source-sink pair with negative mean margin")
    if args.step <= 0.0:
        raise SystemExit("--step must be positive")

    mcrit = two_patch_rescue_threshold(args.r_source, args.r_sink)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["migration_rate", "invasion_exponent", "can_invade", "critical_migration"],
        )
        writer.writeheader()
        for migration in frange(args.m_min, args.m_max, args.step):
            exponent = two_patch_invasion_exponent(args.r_source, args.r_sink, migration)
            writer.writerow(
                {
                    "migration_rate": f"{migration:.12g}",
                    "invasion_exponent": f"{exponent:.12g}",
                    "can_invade": int(exponent > 0.0),
                    "critical_migration": f"{mcrit:.12g}",
                }
            )

    print(f"critical_migration={mcrit:.12g}")
    print(args.output)


if __name__ == "__main__":
    main()
