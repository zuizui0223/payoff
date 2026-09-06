"""Potential-game diagnostics for the two-architecture PAYOFF model."""

from __future__ import annotations

from typing import Optional, Tuple

from .payoff_game import interior_equilibrium, payoff_gap


def mean_game_payoff(p: float, phi: float, eta: float) -> float:
    """Return V(p)=q^T A q for q=(1-p,p) and the symmetric PAYOFF matrix."""

    _validate_frequency(p)
    return 2.0 * (phi - eta) * p + 2.0 * eta * p * p


def potential_slope(p: float, phi: float, eta: float) -> float:
    """Return dV/dp, which equals 2*Delta(p)."""

    _validate_frequency(p)
    return 2.0 * payoff_gap(p, phi, eta)


def potential_rate(p: float, phi: float, eta: float) -> float:
    """Return dV/dt along replicator dynamics.

    For the declared game this is exactly 2 p(1-p) Delta(p)^2 and is
    therefore non-negative.
    """

    _validate_frequency(p)
    delta = payoff_gap(p, phi, eta)
    return 2.0 * p * (1.0 - p) * delta * delta


def coordination_basin_sizes(
    phi: float, eta: float, tol: float = 1e-12
) -> Optional[Tuple[float, float]]:
    """Return (S_basin, D_basin) inside the strict coordination wedge."""

    if eta <= tol:
        return None
    p_star = interior_equilibrium(phi, eta, tol=tol)
    if p_star is None:
        return None
    return p_star, 1.0 - p_star


def risk_dominant_architecture(
    phi: float, eta: float, tol: float = 1e-12
) -> Optional[str]:
    """Return S, D, or tie inside the strict coordination wedge.

    Returns None outside that wedge, where deterministic basin-size risk
    dominance between two locally stable pure states is not the relevant
    classification.
    """

    basins = coordination_basin_sizes(phi, eta, tol=tol)
    if basins is None:
        return None
    s_basin, d_basin = basins
    if d_basin > s_basin + tol:
        return "D"
    if s_basin > d_basin + tol:
        return "S"
    return "tie"


def coexistence_frequency(
    phi: float, eta: float, tol: float = 1e-12
) -> Optional[float]:
    """Return stable D frequency inside the strict negative-feedback wedge."""

    if eta >= -tol:
        return None
    return interior_equilibrium(phi, eta, tol=tol)


def _validate_frequency(p: float) -> None:
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must lie in [0,1]")
