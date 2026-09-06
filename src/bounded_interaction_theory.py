"""Exact local formulas for the hard bounded architecture-interaction kernel."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt


def local_mutant_curvature(kappa: float, gamma: float) -> float:
    """Return d2 f/dy2 at a monomorphic interior singular architecture."""
    k = float(kappa)
    g = float(gamma)
    if not isfinite(k) or not isfinite(g) or k < 0.0:
        raise ValueError("kappa must be finite and non-negative; gamma must be finite")
    return -k - 2.0 * g


def locally_branching_compatible(kappa: float, gamma: float) -> bool:
    """Strict local disruptive-curvature criterion for epsilon > 0."""
    return local_mutant_curvature(kappa, gamma) > 0.0


def hard_cutoff_interface_jump(gamma: float, epsilon: float) -> float:
    """One-sided payoff jump: outside minus inside at |y-x|=epsilon."""
    g = float(gamma)
    e = float(epsilon)
    if not isfinite(g) or not isfinite(e) or e < 0.0:
        raise ValueError("gamma must be finite and epsilon finite/non-negative")
    return g * e * e


def shared_resident_inside_payoff(
    r: float, *, alpha: float, kappa: float, gamma: float
) -> float:
    """Mutant payoff at r within a hard interaction radius around resident 0."""
    x = float(r)
    return float(alpha) * x - (0.5 * float(kappa) + float(gamma)) * x * x


def shared_resident_outside_payoff(r: float, *, alpha: float, kappa: float) -> float:
    """Mutant payoff outside the resident-0 interaction neighbourhood."""
    x = float(r)
    return float(alpha) * x - 0.5 * float(kappa) * x * x


@dataclass(frozen=True)
class NegativeFeedbackEscape:
    alpha: float
    kappa: float
    gamma: float
    epsilon: float
    inside_boundary_payoff: float
    outside_boundary_payoff: float
    interface_jump: float
    equal_payoff_origin_side: float
    escape_jump_infimum: float


def negative_feedback_interface_escape_infimum(
    *, alpha: float, kappa: float, gamma: float, epsilon: float
) -> NegativeFeedbackEscape:
    """Exact continuous escape-jump infimum for a shared resident.

    Assumptions checked here:

    - alpha > 0, kappa >= 0, gamma < 0, epsilon > 0;
    - the inside payoff is strictly increasing on [0, epsilon];
    - the outside payoff immediately beyond epsilon is positive.

    Let p_in(r)=alpha*r-(kappa/2+gamma)r^2 and
    p_out(r)=alpha*r-(kappa/2)r^2. Because gamma<0, crossing the hard
    interaction boundary produces a downward jump. There is a unique x* in
    [0,epsilon) satisfying

        p_in(x*) = p_out(epsilon).

    Every x<x* is reachable from 0 by arbitrarily small uphill steps, and a
    jump from x to just beyond epsilon is uphill when x is sufficiently close
    to x*. Hence

        delta_escape = epsilon - x*

    is the infimum jump size needed to bypass the interface while preserving a
    strictly uphill path. Equality itself is neutral; strict accessibility in
    the continuum requires a jump strictly larger than the infimum.
    """
    a = float(alpha)
    k = float(kappa)
    g = float(gamma)
    e = float(epsilon)
    if any(not isfinite(v) for v in (a, k, g, e)):
        raise ValueError("parameters must be finite")
    if a <= 0.0 or k < 0.0 or g >= 0.0 or e <= 0.0:
        raise ValueError("requires alpha>0, kappa>=0, gamma<0, epsilon>0")

    slope_at_zero = a
    slope_at_epsilon = a - (k + 2.0 * g) * e
    if min(slope_at_zero, slope_at_epsilon) <= 0.0:
        raise ValueError("inside payoff must be strictly increasing on [0, epsilon]")

    outside = shared_resident_outside_payoff(e, alpha=a, kappa=k)
    inside = shared_resident_inside_payoff(e, alpha=a, kappa=k, gamma=g)
    if outside <= 0.0:
        raise ValueError("outside boundary payoff must be positive")
    if not outside < inside:
        raise RuntimeError("negative gamma should create a downward boundary jump")

    quadratic = 0.5 * k + g
    if abs(quadratic) < 1e-14:
        x_equal = outside / a
    else:
        discriminant = a * a - 4.0 * quadratic * outside
        if discriminant < 0.0 and abs(discriminant) < 1e-12:
            discriminant = 0.0
        if discriminant < 0.0:
            raise RuntimeError("equal-payoff root is not real under declared assumptions")
        x_equal = (a - sqrt(discriminant)) / (2.0 * quadratic)

    if not 0.0 <= x_equal < e:
        raise RuntimeError("equal-payoff root did not fall inside the interaction interval")

    return NegativeFeedbackEscape(
        alpha=a,
        kappa=k,
        gamma=g,
        epsilon=e,
        inside_boundary_payoff=inside,
        outside_boundary_payoff=outside,
        interface_jump=hard_cutoff_interface_jump(g, e),
        equal_payoff_origin_side=x_equal,
        escape_jump_infimum=e - x_equal,
    )
