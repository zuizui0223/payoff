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


@dataclass(frozen=True)
class TriangularFeedbackWindow:
    alpha: float
    kappa: float
    epsilon: float
    length: float
    dimensionless_range: float
    ridge_onset_G: float
    upper_contact_location: float
    global_better_upper_G: float
    gamma_window_lower: float
    gamma_window_upper: float
    outside_optimum_payoff: float


def _intrinsic_payoff(r: float, alpha: float, kappa: float) -> float:
    return alpha * r - 0.5 * kappa * r * r


def _inside_payoff(r: float, alpha: float, kappa: float, G: float, epsilon: float) -> float:
    return _intrinsic_payoff(r, alpha, kappa) + G * r * r * (1.0 - r / epsilon)


def _local_max_geometry(alpha: float, kappa: float, G: float, epsilon: float) -> tuple[float, float]:
    discriminant = (2.0 * G - kappa) ** 2 + 12.0 * G * alpha / epsilon
    r_max = epsilon * ((2.0 * G - kappa) + sqrt(discriminant)) / (6.0 * G)
    return r_max, _inside_payoff(r_max, alpha, kappa, G, epsilon)


def triangular_barrier_receipt(
    *,
    alpha: float,
    kappa: float,
    gamma: float,
    epsilon: float,
    length: float = 1.0,
    tolerance: float = 1e-12,
) -> TriangularBarrierReceipt:
    """Return exact local-ridge and across-valley global-better diagnostics."""
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
        r_candidate, p_candidate = _local_max_geometry(a, k, G, e)
        if not (0.0 < r_candidate < e):
            raise RuntimeError("derivative sign conditions did not yield an interior local maximum")
        r_max = r_candidate
        p_max = p_candidate

    p_boundary = _intrinsic_payoff(e, a, k)
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


def triangular_feedback_window(
    *,
    alpha: float,
    kappa: float,
    epsilon: float,
    length: float = 1.0,
) -> TriangularFeedbackWindow:
    """Return the exact finite ``G`` interval with a ridge and better outside optimum.

    This closed form assumes the unconstrained quadratic intrinsic optimum
    ``r*=alpha/kappa`` lies inside the feasible architecture interval and that
    ``0 < epsilon < r*``.

    Let

        E = epsilon/r* = kappa epsilon / alpha  in (0,1),
        x = r_m/r*.

    At the upper feedback boundary the local ridge is stationary and has the
    same payoff as the outside optimum.  Eliminating ``G`` between those two
    equations gives

        x^2 - 3x + 2E = 0,

    so the relevant root is

        x_hi = (3 - sqrt(9-8E))/2.

    Substitution into the equal-payoff equation gives the exact upper feedback
    strength

        G_hi/kappa
        = (1-x_hi)^2 / [2 x_hi^2 (1-x_hi/E)].

    The ridge onset is ``G_on=alpha/epsilon-kappa``.  Hence the exact
    global-better-across-barrier window is ``G_on < G < G_hi``.
    """
    a = float(alpha)
    k = float(kappa)
    e = float(epsilon)
    L = float(length)
    if not all(isfinite(v) for v in (a, k, e, L)):
        raise ValueError("parameters must be finite")
    if a <= 0.0 or k <= 0.0 or e <= 0.0 or L <= 0.0:
        raise ValueError("alpha, kappa, epsilon and length must be positive")

    r_star = a / k
    if r_star > L + 1e-12:
        raise ValueError("closed-form feedback window requires alpha/kappa <= length")
    if not e < r_star:
        raise ValueError("feedback window requires epsilon < alpha/kappa")

    E = e / r_star
    x_hi = (3.0 - sqrt(9.0 - 8.0 * E)) / 2.0
    if not (0.0 < x_hi < E < 1.0):
        raise RuntimeError("closed-form upper contact root left the admissible branch")

    G_on = a / e - k
    g_hi = (1.0 - x_hi) ** 2 / (2.0 * x_hi**2 * (1.0 - x_hi / E))
    G_hi = k * g_hi
    r_contact = r_star * x_hi
    outside = _intrinsic_payoff(r_star, a, k)

    # Exact-form internal consistency checks guard the algebraic branch.
    _, ridge_payoff = _local_max_geometry(a, k, G_hi, e)
    if abs(ridge_payoff - outside) > 1e-9 * max(1.0, abs(outside)):
        raise RuntimeError("closed-form upper boundary failed equal-payoff check")

    return TriangularFeedbackWindow(
        alpha=a,
        kappa=k,
        epsilon=e,
        length=L,
        dimensionless_range=E,
        ridge_onset_G=G_on,
        upper_contact_location=r_contact,
        global_better_upper_G=G_hi,
        gamma_window_lower=-G_hi,
        gamma_window_upper=-G_on,
        outside_optimum_payoff=outside,
    )
