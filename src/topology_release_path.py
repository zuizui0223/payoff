"""Sequential edge-release path for edgewise PAYOFF modularization.

Under linear decoupling cost, recovery is convex in each decoupling direction.
Therefore, if an unreleased edge currently has

    pressure_e=(x_i*-x_j*)^2 > k_e,

then releasing that edge all the way to its allowed endpoint strictly improves
net architecture gain relative to the current state. This module repeatedly
applies that sufficient local rule, re-optimizing phenotype after every release.

The resulting path is an accessibility diagnostic, not a general proof that the
greedy path reaches the global optimum for every graph.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from src.edgewise_modularity import (
    edge_pressures,
    net_gain_linear_cost,
    optimized_loss,
    optimized_phenotype,
    recovery_from_decoupling,
)

Edge = Tuple[int, int]


def connected_components(
    node_count: int,
    edges: Sequence[Edge],
    couplings: Sequence[float],
    tol: float = 1e-12,
) -> Tuple[Tuple[int, ...], ...]:
    """Return connected modules induced by edges with positive coupling."""

    if node_count <= 0:
        raise ValueError("node_count must be positive")
    if len(edges) != len(couplings):
        raise ValueError("edges and couplings must have same length")
    adjacency = [set() for _ in range(node_count)]
    for (i, j), coupling in zip(edges, couplings):
        if coupling < -tol:
            raise ValueError("couplings must be non-negative")
        if coupling > tol:
            adjacency[i].add(j)
            adjacency[j].add(i)

    seen = set()
    components: List[Tuple[int, ...]] = []
    for root in range(node_count):
        if root in seen:
            continue
        stack = [root]
        component = []
        seen.add(root)
        while stack:
            node = stack.pop()
            component.append(node)
            for neighbor in sorted(adjacency[node], reverse=True):
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        components.append(tuple(sorted(component)))
    return tuple(sorted(components))


def greedy_positive_pressure_path(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    reference_couplings: Sequence[float],
    linear_costs: Sequence[float],
    tol: float = 1e-12,
) -> List[Dict[str, object]]:
    """Release one currently profitable edge at a time.

    At each state, among still-retained edges choose the largest positive
        pressure_e - k_e.
    The selected edge is fully released. Phenotype and all edge pressures are
    then recomputed before the next step.

    Returns the initial state plus every post-release state.
    """

    if not optima or len(optima) != len(trait_weights):
        raise ValueError("optima and trait_weights must have same non-zero length")
    if not (len(edges) == len(reference_couplings) == len(linear_costs)):
        raise ValueError("one coupling and one linear cost are required per edge")
    if any(c < 0.0 for c in reference_couplings):
        raise ValueError("reference couplings must be non-negative")
    if any(k < 0.0 for k in linear_costs):
        raise ValueError("linear costs must be non-negative")

    decouplings = [0.0 for _ in edges]
    path: List[Dict[str, object]] = []

    while True:
        current = [
            max(0.0, reference - release)
            for reference, release in zip(reference_couplings, decouplings)
        ]
        phenotype = optimized_phenotype(
            optima, trait_weights, edges, current
        )
        pressures = edge_pressures(
            optima, trait_weights, edges, current
        )
        margins = [
            pressure - cost
            if decouplings[index] < reference_couplings[index] - tol
            else float("-inf")
            for index, (pressure, cost) in enumerate(zip(pressures, linear_costs))
        ]
        candidate = max(range(len(edges)), key=lambda index: margins[index]) if edges else None
        chosen = candidate if candidate is not None and margins[candidate] > tol else None

        path.append(
            {
                "step": len(path),
                "released": tuple(
                    decouplings[index] >= reference_couplings[index] - tol
                    for index in range(len(edges))
                ),
                "decouplings": tuple(decouplings),
                "couplings": tuple(current),
                "components": connected_components(len(optima), edges, current, tol),
                "phenotype": tuple(phenotype),
                "optimized_loss": optimized_loss(
                    optima, trait_weights, edges, current
                ),
                "recovery": recovery_from_decoupling(
                    optima,
                    trait_weights,
                    edges,
                    reference_couplings,
                    decouplings,
                ),
                "net_gain": net_gain_linear_cost(
                    optima,
                    trait_weights,
                    edges,
                    reference_couplings,
                    decouplings,
                    linear_costs,
                ),
                "pressures": tuple(pressures),
                "margins": tuple(margins),
                "next_edge_index": chosen,
            }
        )

        if chosen is None:
            break
        decouplings[chosen] = float(reference_couplings[chosen])

    return path
