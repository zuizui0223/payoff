#!/usr/bin/env python3
"""Sweep migration and report exact spatial environmental invasion thresholds."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.spatial_environment_gradient import spatial_environment_summary


def frange(start: float, stop: float, step: float):
    x = start
    while x <= stop + abs(step) * 1e-9:
        yield x
        x += step


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phi-source", type=float, default=0.6)
    parser.add_argument("--phi-sink", type=float, default=-1.0)
    parser.add_argument("--eta-source", type=float, default=0.0)
    parser.add_argument("--eta-sink", type=float, default=0.0)
    parser.add_argument("--e0", type=float, default=0.0)
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--m-min", type=float, default=0.0)
    parser.add_argument("--m-max", type=float, default=2.0)
    parser.add_argument("--step", type=float, default=0.1)
    parser.add_argument("--output", type=Path, default=Path("outputs/spatial_environment_thresholds.csv"))
    args = parser.parse_args()

    if args.alpha == 0.0:
        raise SystemExit("--alpha must be non-zero")
    if args.step <= 0.0:
        raise SystemExit("--step must be positive")

    base_phis = [args.phi_source, args.phi_sink]
    etas = [args.eta_source, args.eta_sink]
    adjacency = [[0.0, 1.0], [1.0, 0.0]]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "migration_rate",
                "lambda_d_reference",
                "lambda_s_reference",
                "environment_d_neutral",
                "environment_s_neutral",
                "signed_reciprocal_width",
            ],
        )
        writer.writeheader()
        for migration in frange(args.m_min, args.m_max, args.step):
            summary = spatial_environment_summary(
                base_phis,
                etas,
                adjacency,
                migration,
                args.e0,
                args.alpha,
            )
            writer.writerow(
                {
                    "migration_rate": f"{migration:.12g}",
                    **{key: f"{value:.12g}" for key, value in summary.items()},
                }
            )

    print(args.output)


if __name__ == "__main__":
    main()
