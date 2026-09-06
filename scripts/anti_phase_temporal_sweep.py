#!/usr/bin/env python3
"""Sweep migration for the exact anti-phase seasonal rescue model."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.anti_phase_temporal import (
    anti_phase_floquet_exponent,
    anti_phase_temporal_premium,
    fast_switching_premium,
    small_migration_slope,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mean-margin", type=float, default=-0.08)
    parser.add_argument("--contrast-half-amplitude", type=float, default=1.5)
    parser.add_argument("--season-duration", type=float, default=1.0)
    parser.add_argument("--m-min", type=float, default=0.0)
    parser.add_argument("--m-max", type=float, default=5.0)
    parser.add_argument("--step", type=float, default=0.05)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def grid(start: float, stop: float, step: float) -> list[float]:
    if step <= 0.0:
        raise ValueError("step must be positive")
    if start < 0.0 or stop < start:
        raise ValueError("migration range must satisfy 0<=min<=max")
    values = []
    value = start
    while value <= stop + step * 1e-9:
        values.append(value)
        value += step
    return values


def main() -> None:
    args = parse_args()
    if args.season_duration <= 0.0:
        raise ValueError("season-duration must be positive")

    slope0 = small_migration_slope(
        args.contrast_half_amplitude, args.season_duration
    )
    rows = []
    for migration_rate in grid(args.m_min, args.m_max, args.step):
        floquet = anti_phase_floquet_exponent(
            args.mean_margin,
            args.contrast_half_amplitude,
            migration_rate,
            args.season_duration,
        )
        premium = anti_phase_temporal_premium(
            args.contrast_half_amplitude,
            migration_rate,
            args.season_duration,
        )
        rows.append(
            {
                "migration_rate": migration_rate,
                "mean_margin": args.mean_margin,
                "contrast_half_amplitude": args.contrast_half_amplitude,
                "season_duration": args.season_duration,
                "time_averaged_exponent": args.mean_margin,
                "floquet_exponent": floquet,
                "temporal_premium": premium,
                "rescued": int(args.mean_margin < 0.0 < floquet),
                "small_migration_slope": slope0,
                "fast_switching_premium": fast_switching_premium(
                    args.contrast_half_amplitude,
                    migration_rate,
                    args.season_duration,
                ),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    best = max(rows, key=lambda row: row["temporal_premium"])
    rescue_rows = [row for row in rows if row["rescued"]]
    print(f"wrote {len(rows)} rows to {args.output}")
    print(
        "sampled premium maximum: "
        f"m={best['migration_rate']:.6g}, premium={best['temporal_premium']:.6g}"
    )
    if rescue_rows:
        print(
            "sampled rescue interval: "
            f"[{rescue_rows[0]['migration_rate']:.6g}, {rescue_rows[-1]['migration_rate']:.6g}]"
        )
    else:
        print("no sampled migration value rescued the negative mean margin")


if __name__ == "__main__":
    main()
