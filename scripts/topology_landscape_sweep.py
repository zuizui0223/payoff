#!/usr/bin/env python3
"""End-to-end edgewise PAYOFF topology landscape and rare-mutation sweep."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.edgewise_modularity import enumerate_vertex_topologies
from src.topology_game import (
    classify_pairwise_topology_game,
    pairwise_payoff_parameters,
    topology_distance,
)
from src.topology_mutation import (
    intrinsic_valley_depth,
    is_single_edge_local_optimum,
    symmetric_mutation_stationary_distribution,
    symmetric_single_edge_generator,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gamma", type=float, default=-0.5)
    parser.add_argument("--population-size", type=int, default=30)
    parser.add_argument("--beta", type=float, default=0.5)
    parser.add_argument("--mutation-rate", type=float, default=0.01)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Registered small demonstration landscape. The script is an audit harness,
    # not a claim that these numbers represent one empirical system.
    optima = [0.0, 1.2, 3.0]
    trait_weights = [1.0, 2.0, 1.5]
    edges = [(0, 1), (1, 2), (0, 2)]
    reference_couplings = [1.2, 0.8, 0.5]
    linear_costs = [0.10, 0.18, 0.25]
    edge_weights = [1.0, 1.0, 1.0]

    vertices = enumerate_vertex_topologies(
        optima,
        trait_weights,
        edges,
        reference_couplings,
        linear_costs,
    )
    intrinsic = {
        tuple(int(flag) for flag in row["released"]): float(row["net_gain"])
        for row in vertices
    }
    stationary = symmetric_mutation_stationary_distribution(
        intrinsic, args.population_size, args.beta
    )
    states, generator = symmetric_single_edge_generator(
        intrinsic,
        args.mutation_rate,
        args.population_size,
        args.beta,
        args.gamma,
        edge_weights,
    )
    state_index = {state: i for i, state in enumerate(states)}
    global_best = max(intrinsic, key=intrinsic.get)

    rows = []
    for state in states:
        if state == global_best:
            valley = 0.0
            distance = 0.0
            phi = 0.0
            eta = 0.0
            pair_class = "global_best"
        else:
            valley = intrinsic_valley_depth(state, global_best, intrinsic)
            distance = topology_distance(state, global_best, edge_weights)
            phi, eta = pairwise_payoff_parameters(
                intrinsic[state],
                intrinsic[global_best],
                state,
                global_best,
                args.gamma,
                edge_weights,
            )
            pair_class = classify_pairwise_topology_game(
                intrinsic[state],
                intrinsic[global_best],
                state,
                global_best,
                args.gamma,
                edge_weights,
            )

        index = state_index[state]
        rows.append(
            {
                "topology": "".join(str(bit) for bit in state),
                "intrinsic_payoff": intrinsic[state],
                "stationary_probability": stationary[state],
                "single_edge_local_optimum": int(
                    is_single_edge_local_optimum(state, intrinsic)
                ),
                "global_best": int(state == global_best),
                "valley_depth_to_global_best": valley,
                "distance_to_global_best": distance,
                "pair_phi_to_global_best": phi,
                "pair_eta_to_global_best": eta,
                "pair_class_to_global_best": pair_class,
                "total_substitution_rate_out": -generator[index][index],
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} topologies to {args.output}")
    print("global_best=" + "".join(str(bit) for bit in global_best))
    print(f"global_best_payoff={intrinsic[global_best]:.12g}")
    print(f"global_best_stationary={stationary[global_best]:.12g}")


if __name__ == "__main__":
    main()
