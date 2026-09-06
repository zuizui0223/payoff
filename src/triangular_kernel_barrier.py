"""Exact shared-resident barrier geometry for the triangular interaction kernel.

For resident architecture 0 and negative frequency feedback ``gamma<0``, write
``G=-gamma>0``.  Inside the triangular interaction support ``0<=r<=epsilon``:

    p(r) = alpha r - (kappa/2) r^2 + G r^2 (1-r/epsilon)

and outside the support ``p(r)=alpha r-(kappa/2)r^2``.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt


@dataclass(frozen=True)
class TriangularBarrierReceipt:
    alpha: float
    kappa: float
    gamma: float
    epsilon: float
    length: float
    feedback_strength: float
    intrinsic_optimum: float
    derivative_inside_at_boundary: float
    derivative_outside_at_boundary: float
    local_max_location: float | None
    local_max_payoff: float | None
    boundary_payoff: float
    barrier_depth: float | None
    outside_optimum_payoff: float
    ridge_and_dip_exist: bool
    outside_global_better: bool
    global_better_across_barrier: bool


def _intrinsic_payoff(r: float, alpha: float, kappa: float) -> float:
    return alpha * r - 0.5 * kappa * r * r


def _inside_payoff(r: float, alpha: float, kappa: float, G: float, epsilon: float) -> float:
    return _intrinsic_payoff(r, alpha, kappa) + G * r * r * (1.0 - r / epsilon)


def triangular_barrier_receipt(
    *,
    alpha: float,
    kappa: float,
    gamma: float,
    epsilon: float,
    length: float = 1.0,
    tolerance: float = 1e-12,
) -> TriangularBarrierReceipt:
    """Return exact local-ridge and across-valley global-better diagnostics.

    ``ridge_and_dip_exist`` means the payoff rises from the resident, turns down
    before ``epsilon``, and turns up again immediately outside the compact
    support.  ``global_better_across_barrier`` additionally requires the best
    intrinsic architecture outside the support to exceed the local ridge.
    """
    a = float(alpha)
    k = float(kappa)
    g = float(gamma)
    e = float(epsilon)
    L = float(length)
    if not all(isfinite(x) for x in (a, k, g, e, L)):
        raise ValueError("parameters must be finite")
    if a <= 0.0:
        raise ValueError("alpha must be positive for the registered shared-resident theorem")
    if k <= 0.0:
        raise ValueError("kappa must be positive")
    if g >= 0.0:
        raise ValueError("gamma must be negative")
    if e <= 0.0 or L <= 0.0 or e >= L:
        raise ValueError("require 0 < epsilon < length")
    if tolerance < 0.0:
        raise ValueError("tolerance must be non-negative")

    G = -g
    r_star = min(L, a / k)
    inside_boundary_derivative = a - (G + k) * e
    outside_boundary_derivative = a - k * e

    ridge_and_dip = (
        outside_boundary_derivative > tolerance
        and inside_boundary_derivative < -tolerance
    )

    r_max = None
    p_max = None
    depth = None
    if ridge_and_dip:
        discriminant = (2.0 * G - k) ** 2 + 12.0 * G * a / e
        r_candidate = e * ((2.0 * G - k) + sqrt(discriminant)) / (6.0 * G)
        if not (0.0 < r_candidate < e):
            raise RuntimeError("derivative sign conditions did not yield an interior local maximum")
        r_max = r_candidate
        p_max = _inside_payoff(r_max, a, k, G, e)

    p_boundary = _intrinsic_payoff(e, a, k)  # triangular weight is zero at epsilon
    if p_max is not None:
        depth = p_max - p_boundary

    p_outside_best = _intrinsic_payoff(r_star, a, k)
    outside_better = (
        r_star > e + tolerance
        and p_max is not None
        and p_outside_best > p_max + tolerance
    )

    return TriangularBarrierReceipt(
        alpha=a,
        kappa=k,
        gamma=g,
        epsilon=e,
        length=L,
        feedback_strength=G,
        intrinsic_optimum=r_star,
        derivative_inside_at_boundary=inside_boundary_derivative,
        derivative_outside_at_boundary=outside_boundary_derivative,
        local_max_location=r_max,
        local_max_payoff=p_max,
        boundary_payoff=p_boundary,
        barrier_depth=depth,
        outside_optimum_payoff=p_outside_best,
        ridge_and_dip_exist=ridge_and_dip,
        outside_global_better=outside_better,
        global_better_across_barrier=ridge_and_dip and outside_better,
    )
