#!/usr/bin/env python3
"""Generate the recurrent-mutation stationary architecture profile."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.mutation_stationary import (
    rare_mutation_boundary_probability_d,
    stationary_distribution,
    stationary_modes,
    stationary_summary,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=50)
    parser.add_argument("--phi", type=float, default=0.0)
    parser.add_argument("--eta", type=float, default=1.0)
    parser.add_argument("--beta", type=float, default=0.5)
    parser.add_argument("--u-sd", type=float, default=0.001)
    parser.add_argument("--u-ds", type=float, default=0.001)
    parser.add_argument("--output", type=Path, default=Path("outputs/stationary_profile.csv"))
    args = parser.parse_args()

    probs = stationary_distribution(
        n=args.n,
        phi=args.phi,
        eta=args.eta,
        beta=args.beta,
        u_sd=args.u_sd,
        u_ds=args.u_ds,
    )
    summary = stationary_summary(probs)
    modes = stationary_modes(probs)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["i", "d_frequency", "stationary_probability"])
        writer.writeheader()
        for i, probability in enumerate(probs):
            writer.writerow(
                {
                    "i": i,
                    "d_frequency": f"{i / args.n:.12g}",
                    "stationary_probability": f"{probability:.16g}",
                }
            )

    rare_d = rare_mutation_boundary_probability_d(
        args.n, args.phi, args.beta, args.u_sd, args.u_ds
    )

    print(args.output)
    print(f"modes={','.join(str(i) for i in modes)}")
    for key, value in summary.items():
        print(f"{key}={value:.12g}")
    print(f"rare_mutation_boundary_probability_d={rare_d:.12g}")


if __name__ == "__main__":
    main()
