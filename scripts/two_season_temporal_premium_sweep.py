#!/usr/bin/env python3
"""Generate a period x migration grid for the exact two-season temporal premium."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from src.two_patch_floquet import (
    fast_switching_premium_coefficient,
    time_averaged_operator_exponent,
    two_season_closed_form,
    two_season_temporal_premium,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r1-a", type=float, default=-2.5)
    parser.add_argument("--r2-a", type=float, default=1.0)
    parser.add_argument("--r1-b", type=float, default=2.0)
    parser.add_argument("--r2-b", type=float, default=-1.0)
    parser.add_argument("--season-a-fraction", type=float, default=0.5)
    parser.add_argument("--m-min", type=float, default=0.0)
    parser.add_argument("--m-max", type=float, default=0.8)
    parser.add_argument("--m-step", type=float, default=0.1)
    parser.add_argument("--period-min", type=float, default=0.1)
    parser.add_argument("--period-max", type=float, default=2.0)
    parser.add_argument("--period-step", type=float, default=0.1)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def inclusive_grid(start: float, stop: float, step: float) -> list[float]:
    if step <= 0.0:
        raise ValueError("grid step must be positive")
    if stop < start:
        raise ValueError("grid stop must be >= start")
    values = []
    value = start
    while value <= stop + step * 1e-9:
        values.append(value)
        value += step
    return values


def main() -> None:
    args = parse_args()
    w = args.season_a_fraction
    if not 0.0 < w < 1.0:
        raise ValueError("season-a-fraction must lie strictly between 0 and 1")
    if args.m_min < 0.0:
        raise ValueError("migration rates must be non-negative")
    if args.period_min <= 0.0:
        raise ValueError("periods must be positive")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for migration_rate in inclusive_grid(args.m_min, args.m_max, args.m_step):
        coefficient = fast_switching_premium_coefficient(
            (args.r1_a, args.r2_a),
            (args.r1_b, args.r2_b),
            migration_rate,
            w,
        )
        for period in inclusive_grid(args.period_min, args.period_max, args.period_step):
            seasons = [
                (args.r1_a, args.r2_a, w * period),
                (args.r1_b, args.r2_b, (1.0 - w) * period),
            ]
            floquet = two_season_closed_form(seasons, migration_rate)
            averaged = time_averaged_operator_exponent(seasons, migration_rate)
            premium = two_season_temporal_premium(seasons, migration_rate)
            quadratic_prediction = coefficient * period * period
            rows.append(
                {
                    "migration_rate": migration_rate,
                    "period": period,
                    "floquet_exponent": floquet,
                    "averaged_exponent": averaged,
                    "temporal_premium": premium,
                    "fast_switching_coefficient": coefficient,
                    "quadratic_premium_prediction": quadratic_prediction,
                    "premium_over_period_squared": premium / (period * period),
                    "rescue_vs_average": int(averaged < 0.0 < floquet),
                }
            )

    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
