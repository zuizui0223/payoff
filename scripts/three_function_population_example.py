#!/usr/bin/env python3
"""Transport the three-function topology landscape into population-game receipts."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.three_function_example import TWO_MODULE, intrinsic_topology_payoffs
from src.topology_game import (
    classify_pairwise_topology_game,
    pairwise_payoff_parameters,
    reciprocal_fixation_probabilities,
    reciprocal_invasion_margins,
    topology_distance,
)
from src.topology_mutation import symmetric_mutation_stationary_distribution


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--edge-cost", type=float, default=0.4)
    parser.add_argument("--gamma", type=float, default=-0.25)
    parser.add_argument("--population-size", type=int, default=20)
    parser.add_argument("--beta", type=float, default=0.4)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/three_function_population.csv"),
    )
    return parser.parse_args()


def label(topology) -> str:
    return "".join(str(int(value)) for value in topology)


def main() -> None:
    args = parse_args()
    if args.edge_cost < 0.0:
        raise ValueError("edge cost must be non-negative")
    if args.population_size < 2:
        raise ValueError("population-size must be at least 2")
    if args.beta < 0.0:
        raise ValueError("beta must be non-negative")

    payoffs = intrinsic_topology_payoffs(args.edge_cost)
    if TWO_MODULE not in payoffs:
        raise RuntimeError("registered best-module topology is missing")
    stationary = symmetric_mutation_stationary_distribution(
        payoffs, args.population_size, args.beta
    )

    rows = []
    for topology, payoff in sorted(payoffs.items(), key=lambda item: item[1], reverse=True):
        if topology == TWO_MODULE:
            rows.append(
                {
                    "topology": label(topology),
                    "intrinsic_payoff": payoff,
                    "distance_from_module": 0.0,
                    "phi_vs_module": 0.0,
                    "eta_vs_module": 0.0,
                    "mutant_into_module_margin": 0.0,
                    "module_into_mutant_margin": 0.0,
                    "pair_class": "reference_module",
                    "rho_mutant_into_module": "",
                    "rho_module_into_mutant": "",
                    "stationary_probability": stationary[topology],
                }
            )
            continue

        q = topology_distance(TWO_MODULE, topology)
        phi, eta = pairwise_payoff_parameters(
            payoffs[TWO_MODULE],
            payoff,
            TWO_MODULE,
            topology,
            args.gamma,
        )
        into_module, module_into = reciprocal_invasion_margins(
            payoffs[TWO_MODULE],
            payoff,
            TWO_MODULE,
            topology,
            args.gamma,
        )
        rho_into, rho_reverse = reciprocal_fixation_probabilities(
            args.population_size,
            args.beta,
            payoffs[TWO_MODULE],
            payoff,
            TWO_MODULE,
            topology,
            args.gamma,
        )
        rows.append(
            {
                "topology": label(topology),
                "intrinsic_payoff": payoff,
                "distance_from_module": q,
                "phi_vs_module": phi,
                "eta_vs_module": eta,
                "mutant_into_module_margin": into_module,
                "module_into_mutant_margin": module_into,
                "pair_class": classify_pairwise_topology_game(
                    payoffs[TWO_MODULE],
                    payoff,
                    TWO_MODULE,
                    topology,
                    args.gamma,
                ),
                "rho_mutant_into_module": rho_into,
                "rho_module_into_mutant": rho_reverse,
                "stationary_probability": stationary[topology],
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    full = next(row for row in rows if row["topology"] == "111")
    phi = float(full["phi_vs_module"])
    eta = float(full["eta_vs_module"])
    p_full = 0.5 * (1.0 - phi / eta)
    print(args.output)
    print(f"module-vs-full equilibrium full-release frequency={p_full:.12g}")
    print(
        "stationary module/full="
        f"{stationary[TWO_MODULE]:.12g}/"
        f"{stationary[(1, 1, 1)]:.12g}"
    )


if __name__ == "__main__":
    main()
