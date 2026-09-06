#!/usr/bin/env python3
"""Sweep regular-graph degree for the weak-selection PAYOFF transform."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.regular_graph_pair_approx import graph_bridge_summary, graph_cost_boundaries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phi", type=float, default=0.2)
    parser.add_argument("--eta", type=float, default=1.0)
    parser.add_argument("--recovery", type=float, default=1.0)
    parser.add_argument("--k-min", type=int, default=3)
    parser.add_argument("--k-max", type=int, default=30)
    parser.add_argument("--output", type=Path, default=Path("outputs/regular_graph_degree.csv"))
    args = parser.parse_args()

    if args.k_min < 3 or args.k_max < args.k_min:
        raise SystemExit("require 3 <= k-min <= k-max")
    if args.recovery < 0:
        raise SystemExit("--recovery must be non-negative")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "degree",
        "phi",
        "eta",
        "phi_graph",
        "eta_graph",
        "phi_amplification",
        "middle_phi_width",
        "cost_lower",
        "cost_upper",
        "middle_cost_width",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for degree in range(args.k_min, args.k_max + 1):
            summary = graph_bridge_summary(args.phi, args.eta, degree)
            cost_lower, cost_upper = graph_cost_boundaries(args.recovery, args.eta, degree)
            writer.writerow(
                {
                    "degree": degree,
                    "phi": f"{args.phi:.12g}",
                    "eta": f"{args.eta:.12g}",
                    "phi_graph": f"{summary['phi_graph']:.12g}",
                    "eta_graph": f"{summary['eta_graph']:.12g}",
                    "phi_amplification": f"{summary['phi_amplification']:.12g}",
                    "middle_phi_width": f"{summary['middle_phi_width']:.12g}",
                    "cost_lower": f"{cost_lower:.12g}",
                    "cost_upper": f"{cost_upper:.12g}",
                    "middle_cost_width": f"{cost_upper-cost_lower:.12g}",
                }
            )

    print(args.output)


if __name__ == "__main__":
    main()
