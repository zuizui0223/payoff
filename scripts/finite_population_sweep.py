#!/usr/bin/env python3
"""Generate a finite-population fixation grid for the PAYOFF Moran model."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.finite_population import (
    classify_weak_selection_mutant_advantage,
    moran_fixation_probability_d,
    moran_fixation_probability_s,
)


def frange(start: float, stop: float, step: float):
    x = start
    while x <= stop + abs(step) * 1e-9:
        yield x
        x += step


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=50)
    parser.add_argument("--beta", type=float, default=0.1)
    parser.add_argument("--phi-min", type=float, default=-1.0)
    parser.add_argument("--phi-max", type=float, default=1.0)
    parser.add_argument("--eta-min", type=float, default=-1.0)
    parser.add_argument("--eta-max", type=float, default=1.0)
    parser.add_argument("--step", type=float, default=0.1)
    parser.add_argument(
        "--output", type=Path, default=Path("outputs/finite_population_grid.csv")
    )
    args = parser.parse_args()

    if args.n < 2:
        raise SystemExit("--n must be at least 2")
    if args.beta < 0:
        raise SystemExit("--beta must be non-negative")
    if args.step <= 0:
        raise SystemExit("--step must be positive")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    neutral = 1.0 / args.n

    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "n",
                "beta",
                "phi",
                "eta",
                "rho_d",
                "rho_s",
                "neutral",
                "rho_d_over_neutral",
                "rho_s_over_neutral",
                "weak_selection_class",
            ],
        )
        writer.writeheader()

        for eta in frange(args.eta_min, args.eta_max, args.step):
            for phi in frange(args.phi_min, args.phi_max, args.step):
                rho_d = moran_fixation_probability_d(args.n, phi, eta, args.beta)
                rho_s = moran_fixation_probability_s(args.n, phi, eta, args.beta)
                writer.writerow(
                    {
                        "n": args.n,
                        "beta": f"{args.beta:.12g}",
                        "phi": f"{phi:.12g}",
                        "eta": f"{eta:.12g}",
                        "rho_d": f"{rho_d:.12g}",
                        "rho_s": f"{rho_s:.12g}",
                        "neutral": f"{neutral:.12g}",
                        "rho_d_over_neutral": f"{rho_d / neutral:.12g}",
                        "rho_s_over_neutral": f"{rho_s / neutral:.12g}",
                        "weak_selection_class": classify_weak_selection_mutant_advantage(phi, eta),
                    }
                )

    print(args.output)


if __name__ == "__main__":
    main()
