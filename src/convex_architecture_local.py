"""Local continuous-architecture receipts for a general smooth convex cost.

The architecture coordinate is recovered conflict loss r, so intrinsic payoff is
    b(r)=r-C(r).
For symmetric mismatch feedback H(r,q)=-gamma(r-q)^2, the monomorphic
selection gradient and local branching threshold depend only on derivatives of
C at the resident/singular recovery.
"""

from __future__ import annotations

from .numerical_tolerance import DEFAULT_RELATIVE_TOL, relative_band


def selection_gradient_from_cost_slope(cost_slope: float) -> float:
    """Return g=1-C'(r)."""

    return 1.0 - cost_slope


def singular_condition_residual(cost_slope: float) -> float:
    """Return C'(r*)-1; zero identifies an interior singular recovery."""

    return cost_slope - 1.0


def convergence_rate_from_cost_curvature(cost_curvature: float) -> float:
    """Return derivative of the monomorphic selection gradient: -C''(r*)."""

    if cost_curvature <= 0.0:
        raise ValueError("cost_curvature must be positive for local convexity")
    return -cost_curvature


def branching_threshold_gamma(cost_curvature: float) -> float:
    """Return gamma_c=-C''(r*)/2."""

    if cost_curvature <= 0.0:
        raise ValueError("cost_curvature must be positive")
    return -0.5 * cost_curvature


def mutant_fitness_curvature(cost_curvature: float, gamma: float) -> float:
    """Return local mutant curvature -C''(r*)-2gamma."""

    if cost_curvature <= 0.0:
        raise ValueError("cost_curvature must be positive")
    return -cost_curvature - 2.0 * gamma


def local_branching_regime(
    cost_curvature: float,
    gamma: float,
    tol: float = DEFAULT_RELATIVE_TOL,
) -> str:
    """Classify local singular strategy as ESS / neutral / branching-compatible.

    ``tol`` is dimensionless. Numerical neutrality is judged relative to the
    two curvature terms whose cancellation defines the exact branching line.
    """

    curvature = mutant_fitness_curvature(cost_curvature, gamma)
    band = relative_band((cost_curvature, 2.0 * gamma), tol)
    if curvature < -band:
        return "local_ess"
    if curvature > band:
        return "branching_compatible"
    return "second_order_neutral"
