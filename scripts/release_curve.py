#!/usr/bin/env python3
"""Generate fixation probability rho_i across initial architecture counts."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.finite_population import (
    finite_zero_gap_count,
    minimum_initial_d_for_fixation_probability,
    moran_fixation_probability_from_i,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=100)
    parser.add_argument("--phi", type=float, default=0.2)
    parser.add_argument("--eta", type=float, default=1.0)
    parser.add_argument("--beta", type=float, default=1.0)
    parser.add_argument(
        "--output", type=Path, default=Path("outputs/release_curve.csv")
    )
    args = parser.parse_args()

    if args.n < 2:
        raise SystemExit("--n must be at least 2")
    if args.beta < 0:
        raise SystemExit("--beta must be non-negative")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    zero_gap = ""
    if args.eta != 0:
        zero_gap = f"{finite_zero_gap_count(args.n, args.phi, args.eta):.12g}"

    m50 = minimum_initial_d_for_fixation_probability(
        args.n, args.phi, args.eta, args.beta, target=0.5
    )
    m90 = minimum_initial_d_for_fixation_probability(
        args.n, args.phi, args.eta, args.beta, target=0.9
    )

    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "initial_d",
                "initial_frequency",
                "fixation_probability_d",
                "n",
                "phi",
                "eta",
                "beta",
                "finite_zero_gap_count",
                "m50",
                "m90",
            ],
        )
        writer.writeheader()
        for i in range(args.n + 1):
            rho = moran_fixation_probability_from_i(
                i, args.n, args.phi, args.eta, args.beta
            )
            writer.writerow(
                {
                    "initial_d": i,
                    "initial_frequency": f"{i / args.n:.12g}",
                    "fixation_probability_d": f"{rho:.12g}",
                    "n": args.n,
                    "phi": f"{args.phi:.12g}",
                    "eta": f"{args.eta:.12g}",
                    "beta": f"{args.beta:.12g}",
                    "finite_zero_gap_count": zero_gap,
                    "m50": m50,
                    "m90": m90,
                }
            )

    print(args.output)
    print(f"m50={m50} m90={m90} zero_gap_count={zero_gap or 'NA'}")


if __name__ == "__main__":
    main()
