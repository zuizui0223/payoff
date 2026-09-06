"""Robustness diagnostics for discrete edge-release architectures.

Two reserves are deliberately separated:

1. global vertex reserve
       best intrinsic payoff - second-best intrinsic payoff;
2. local vertex reserve
       minimum KKT-direction margin across all edge boundaries.

A topology can be locally resistant to infinitesimal edge changes while having
only a small global payoff advantage over another distant topology.
"""

from __future__ import annotations

from typing import Dict, Sequence, Tuple

from src.edgewise_modularity import (
    edge_pressures,
    enumerate_vertex_topologies,
)

Edge = Tuple[int, int]


def global_vertex_reserve(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    reference_couplings: Sequence[float],
    linear_costs: Sequence[float],
) -> Dict[str, object]:
    """Return best/runner-up vertex topologies and intrinsic payoff gap."""

    rows = enumerate_vertex_topologies(
        optima, trait_weights, edges, reference_couplings, linear_costs
    )
    ordered = sorted(rows, key=lambda row: float(row["net_gain"]), reverse=True)
    if len(ordered) < 2:
        raise ValueError("at least one edge is required to define a runner-up topology")
    best = ordered[0]
    second = ordered[1]
    return {
        "best_released": best["released"],
        "best_net_gain": float(best["net_gain"]),
        "second_released": second["released"],
        "second_net_gain": float(second["net_gain"]),
        "global_reserve": float(best["net_gain"]) - float(second["net_gain"]),
    }


def vertex_boundary_margins(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    reference_couplings: Sequence[float],
    linear_costs: Sequence[float],
    released: Sequence[bool],
) -> Tuple[float, ...]:
    """Return positive-sense local KKT margins at one binary topology.

    For a retained edge (d_e=0), local stability against release requires
        pressure_e <= k_e,
    so margin is
        k_e-pressure_e.

    For a fully released edge (d_e=c_e^0), local stability against recoupling
    requires
        pressure_e >= k_e,
    so margin is
        pressure_e-k_e.
    """

    if not (
        len(edges)
        == len(reference_couplings)
        == len(linear_costs)
        == len(released)
    ):
        raise ValueError("one coupling, cost, and release state are required per edge")
    current = [
        0.0 if bool(flag) else float(reference)
        for flag, reference in zip(released, reference_couplings)
    ]
    pressures = edge_pressures(optima, trait_weights, edges, current)
    margins = []
    for flag, pressure, cost in zip(released, pressures, linear_costs):
        if cost < 0.0:
            raise ValueError("linear costs must be non-negative")
        margins.append(pressure - cost if flag else cost - pressure)
    return tuple(margins)


def local_vertex_reserve(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    reference_couplings: Sequence[float],
    linear_costs: Sequence[float],
    released: Sequence[bool],
) -> float:
    """Return minimum local boundary margin; positive means strict local stability."""

    margins = vertex_boundary_margins(
        optima,
        trait_weights,
        edges,
        reference_couplings,
        linear_costs,
        released,
    )
    if not margins:
        raise ValueError("at least one edge is required")
    return min(margins)


def topology_robustness_summary(
    optima: Sequence[float],
    trait_weights: Sequence[float],
    edges: Sequence[Edge],
    reference_couplings: Sequence[float],
    linear_costs: Sequence[float],
) -> Dict[str, object]:
    """Return global and local reserves for the best vertex architecture."""

    global_receipt = global_vertex_reserve(
        optima, trait_weights, edges, reference_couplings, linear_costs
    )
    released = global_receipt["best_released"]
    margins = vertex_boundary_margins(
        optima,
        trait_weights,
        edges,
        reference_couplings,
        linear_costs,
        released,
    )
    return {
        **global_receipt,
        "edge_boundary_margins": margins,
        "local_reserve": min(margins),
        "strict_local_vertex_stability": min(margins) > 0.0,
    }
