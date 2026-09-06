"""Ohtsuki-Nowak regular-graph pair-approximation bridge for PAYOFF.

This module does not rederive evolutionary graph theory. It substitutes the
PAYOFF 2x2 architecture matrix into the transformed-payoff formulas of
Ohtsuki & Nowak (2006) for weak selection on large degree-k regular graphs.

Rows/columns are ordered (S,D):
    [[0,       phi-eta],
     [phi-eta, 2phi   ]]

For this special symmetric matrix, the graph correction H is identical for
BD, pairwise-comparison, DB, and imitation updating:
    H=-2phi/(k-2).
Consequently the transformed replicator gap remains affine with
    phi_k = k*phi/(k-2),
    eta_k = eta.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple


_UPDATE_RULES = {"bd", "pc", "db", "im"}


def payoff_matrix(phi: float, eta: float) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Return the PAYOFF architecture matrix ordered (S,D)."""

    return ((0.0, phi - eta), (phi - eta, 2.0 * phi))


def ohtsuki_h(phi: float, eta: float, degree: int, update_rule: str) -> float:
    """Return the Ohtsuki-Nowak off-diagonal graph correction H.

    Formulas are the regular-graph weak-selection pair-approximation formulas
    for k>=3. The special PAYOFF matrix makes all supported rules simplify to
    the same H, but the rule-specific expressions are evaluated explicitly so
    that the cancellation remains auditable.
    """

    k = _validate_degree(degree)
    rule = update_rule.lower()
    if rule not in _UPDATE_RULES:
        raise ValueError(f"update_rule must be one of {sorted(_UPDATE_RULES)}")

    matrix = payoff_matrix(phi, eta)
    a11, a12 = matrix[0]
    a21, a22 = matrix[1]

    if rule in {"bd", "pc"}:
        return (a11 + a12 - a21 - a22) / (k - 2.0)
    if rule == "db":
        return (
            (k + 1.0) * a11 + a12 - a21 - (k + 1.0) * a22
        ) / ((k + 1.0) * (k - 2.0))
    return (
        (k + 3.0) * a11 + 3.0 * a12 - 3.0 * a21 - (k + 3.0) * a22
    ) / ((k + 3.0) * (k - 2.0))


def transformed_matrix(
    phi: float, eta: float, degree: int, update_rule: str
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Return the regular-graph transformed payoff matrix ordered (S,D)."""

    base = payoff_matrix(phi, eta)
    h = ohtsuki_h(phi, eta, degree, update_rule)
    return (
        (base[0][0], base[0][1] + h),
        (base[1][0] - h, base[1][1]),
    )


def transformed_parameters(phi: float, eta: float, degree: int) -> Tuple[float, float]:
    """Return (phi_k,eta_k) for the transformed PAYOFF replicator gap."""

    k = _validate_degree(degree)
    return (k / (k - 2.0)) * phi, eta


def graph_payoff_gap(p: float, phi: float, eta: float, degree: int) -> float:
    """Return transformed weak-selection regular-graph gap at D frequency p."""

    if not 0.0 <= p <= 1.0:
        raise ValueError("p must lie in [0,1]")
    phi_k, eta_k = transformed_parameters(phi, eta, degree)
    return phi_k + eta_k * (2.0 * p - 1.0)


def graph_interior_equilibrium(
    phi: float, eta: float, degree: int, tol: float = 1e-12
) -> Optional[float]:
    """Return the strict transformed interior equilibrium/threshold, if any."""

    phi_k, eta_k = transformed_parameters(phi, eta, degree)
    if abs(eta_k) <= tol:
        return None
    p_star = 0.5 * (1.0 - phi_k / eta_k)
    if tol < p_star < 1.0 - tol:
        return p_star
    return None


def graph_phi_boundaries(eta: float, degree: int) -> Tuple[float, float]:
    """Return ordered phi boundaries enclosing the graph middle region.

    The transformed game has an interior region when |phi_k|<|eta|, so
        |phi| < |eta|(k-2)/k.
    """

    k = _validate_degree(degree)
    half_width = abs(eta) * (k - 2.0) / k
    return -half_width, half_width


def graph_cost_boundaries(recovery: float, eta: float, degree: int) -> Tuple[float, float]:
    """Return ordered K boundaries around R for the graph middle region."""

    if recovery < 0.0:
        raise ValueError("recovery must be non-negative")
    lower_phi, upper_phi = graph_phi_boundaries(eta, degree)
    # phi=R-K, so the ordered K interval reverses the phi interval.
    return recovery - upper_phi, recovery - lower_phi


def graph_bridge_summary(phi: float, eta: float, degree: int) -> Dict[str, float]:
    """Return the core PAYOFF regular-graph scaling diagnostics."""

    k = _validate_degree(degree)
    phi_k, eta_k = transformed_parameters(phi, eta, k)
    lower, upper = graph_phi_boundaries(eta, k)
    return {
        "degree": float(k),
        "phi": phi,
        "eta": eta,
        "phi_graph": phi_k,
        "eta_graph": eta_k,
        "phi_amplification": k / (k - 2.0),
        "middle_phi_lower": lower,
        "middle_phi_upper": upper,
        "middle_phi_width": upper - lower,
    }


def _validate_degree(degree: int) -> int:
    if isinstance(degree, bool) or int(degree) != degree or degree < 3:
        raise ValueError("degree must be an integer >=3")
    return int(degree)
