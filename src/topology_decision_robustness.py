"""Perturbation robustness for topology decisions.

The module separates two finite-margin guarantees:

1. first-edge decision robustness from edge release margins
       m_e=(x_i-x_j)^2-k_e;
2. global-best topology robustness from best-minus-runner-up payoff reserve.

The bounds are deterministic sufficient conditions under uniform additive
perturbations of the corresponding decision scores.
"""

from __future__ import annotations

from typing import Dict, Sequence


def first_edge_decision_radius(margins: Sequence[float]) -> Dict[str, float | int]:
    """Return a sufficient sup-norm perturbation radius for first-edge identity.

    Let e* be the unique largest margin m*>0 and m2 the second-largest margin.
    If every margin is perturbed by at most epsilon, then e* remains positive
    and remains the unique largest margin whenever

        epsilon < min(m*, (m*-m2)/2).

    The function requires at least two edges and a strict positive leader.
    """

    if len(margins) < 2:
        raise ValueError("at least two edge margins are required")
    ordered = sorted(enumerate(float(value) for value in margins), key=lambda item: item[1], reverse=True)
    best_index, best = ordered[0]
    _, second = ordered[1]
    if best <= 0.0:
        raise ValueError("first-edge robustness requires a positive leading margin")
    if best <= second:
        raise ValueError("first-edge robustness requires a unique leading margin")
    ranking_gap = best - second
    radius = min(best, 0.5 * ranking_gap)
    return {
        "best_edge_index": best_index,
        "best_margin": best,
        "second_margin": second,
        "ranking_gap": ranking_gap,
        "uniform_margin_perturbation_radius": radius,
    }


def global_best_decision_radius(global_reserve: float) -> float:
    """Return reserve/2 for uniform additive perturbations of topology payoffs.

    If the best topology exceeds the runner-up by rho>0 and every topology
    payoff is perturbed by at most epsilon, the best topology remains strictly
    best whenever epsilon<rho/2.
    """

    reserve = float(global_reserve)
    if reserve <= 0.0:
        raise ValueError("global_reserve must be strictly positive")
    return 0.5 * reserve


def decision_robustness_summary(
    edge_margins: Sequence[float], global_reserve: float
) -> Dict[str, float | int]:
    """Return first-edge and global-topology perturbation receipts together."""

    edge = first_edge_decision_radius(edge_margins)
    global_radius = global_best_decision_radius(global_reserve)
    return {
        **edge,
        "global_reserve": float(global_reserve),
        "uniform_topology_payoff_perturbation_radius": global_radius,
    }
