"""Continuous architecture recovery game for PAYOFF.

Architecture state is recovery r in [0,L], where L is the fully shared
conflict load and r is the pre-cost loss recovered by partial dimensional
release. Intrinsic relative payoff is

    b(r)=alpha*r-(kappa/2)*r^2,

with alpha=1-c1 for linear architecture-cost slope c1 and kappa>0.
Pairwise ecological feedback is

    H(r,q)=-gamma*(r-q)^2.

The exact branching threshold is gamma=-kappa/2 for an interior intrinsic
optimum. Stronger dissimilarity reward (gamma<-kappa/2) yields a protected
endpoint polymorphism in the declared quadratic potential game.
"""

from __future__ import annotations

from math import inf
from typing import Dict, Iterable, Optional, Sequence, Tuple


def net_linear_benefit(linear_cost_slope: float) -> float:
    """Return alpha=1-c1 for architecture cost C=c1*r+kappa*r^2/2."""

    return 1.0 - linear_cost_slope


def architecture_cost(
    recovery: float,
    linear_cost_slope: float,
    curvature: float,
) -> float:
    """Return C(r)=c1*r+(kappa/2)r^2."""

    _validate_nonnegative_recovery(recovery)
    _validate_curvature(curvature)
    return linear_cost_slope * recovery + 0.5 * curvature * recovery * recovery


def intrinsic_payoff(
    recovery: float,
    linear_cost_slope: float,
    curvature: float,
) -> float:
    """Return relative intrinsic payoff b(r)=r-C(r)."""

    alpha = net_linear_benefit(linear_cost_slope)
    _validate_nonnegative_recovery(recovery)
    _validate_curvature(curvature)
    return alpha * recovery - 0.5 * curvature * recovery * recovery


def no_feedback_optimum(
    max_recovery: float,
    linear_cost_slope: float,
    curvature: float,
) -> float:
    """Return unique static optimum r0=clip(alpha/kappa,0,L)."""

    _validate_max_recovery(max_recovery)
    _validate_curvature(curvature)
    alpha = net_linear_benefit(linear_cost_slope)
    return _clip(alpha / curvature, 0.0, max_recovery)


def no_feedback_regime(
    max_recovery: float,
    linear_cost_slope: float,
    curvature: float,
    tol: float = 1e-12,
) -> str:
    """Classify shared / partial / full recovery optimum."""

    optimum = no_feedback_optimum(max_recovery, linear_cost_slope, curvature)
    if optimum <= tol:
        return "shared"
    if optimum >= max_recovery - tol:
        return "full_differentiation"
    return "partial_modularity"


def mismatch_feedback(recovery_a: float, recovery_b: float, gamma: float) -> float:
    """Return H(a,b)=-gamma(a-b)^2."""

    _validate_nonnegative_recovery(recovery_a)
    _validate_nonnegative_recovery(recovery_b)
    diff = recovery_a - recovery_b
    return -gamma * diff * diff


def mutant_invasion_fitness(
    mutant_recovery: float,
    resident_recovery: float,
    linear_cost_slope: float,
    curvature: float,
    gamma: float,
) -> float:
    """Return mutant-minus-resident payoff in a monomorphic resident."""

    return (
        intrinsic_payoff(mutant_recovery, linear_cost_slope, curvature)
        - intrinsic_payoff(resident_recovery, linear_cost_slope, curvature)
        + mismatch_feedback(mutant_recovery, resident_recovery, gamma)
    )


def monomorphic_selection_gradient(
    resident_recovery: float,
    linear_cost_slope: float,
    curvature: float,
) -> float:
    """Return d/dy f(y,x)|y=x = alpha-kappa*x.

    Symmetric quadratic mismatch feedback does not enter the first derivative.
    """

    _validate_nonnegative_recovery(resident_recovery)
    _validate_curvature(curvature)
    return net_linear_benefit(linear_cost_slope) - curvature * resident_recovery


def interior_singular_recovery(
    max_recovery: float,
    linear_cost_slope: float,
    curvature: float,
) -> Optional[float]:
    """Return interior singular recovery alpha/kappa, or None if boundary."""

    optimum = no_feedback_optimum(max_recovery, linear_cost_slope, curvature)
    if 0.0 < optimum < max_recovery:
        return optimum
    return None


def singular_invasion_curvature(curvature: float, gamma: float) -> float:
    """Return d^2 f/dy^2 at the singular resident: -kappa-2gamma."""

    _validate_curvature(curvature)
    return -curvature - 2.0 * gamma


def branching_regime(curvature: float, gamma: float, tol: float = 1e-12) -> str:
    """Classify singular architecture ESS / neutral / branching-compatible."""

    value = curvature + 2.0 * gamma
    if value > tol:
        return "monomorphic_ess"
    if value < -tol:
        return "branching_compatible"
    return "neutral_variance_threshold"


def singular_mutant_fitness_exact(
    mutant_recovery: float,
    singular_recovery: float,
    curvature: float,
    gamma: float,
) -> float:
    """Return exact f(y,r0)=-(kappa/2+gamma)(y-r0)^2.

    Caller is responsible for supplying an actual interior singular recovery.
    """

    _validate_nonnegative_recovery(mutant_recovery)
    _validate_nonnegative_recovery(singular_recovery)
    _validate_curvature(curvature)
    diff = mutant_recovery - singular_recovery
    return -(0.5 * curvature + gamma) * diff * diff


def mean_game_payoff_from_moments(
    mean_recovery: float,
    variance_recovery: float,
    linear_cost_slope: float,
    curvature: float,
    gamma: float,
) -> float:
    """Return V=2alpha*mu-kappa*mu^2-(kappa+2gamma)*variance."""

    _validate_nonnegative_recovery(mean_recovery)
    if variance_recovery < 0.0:
        raise ValueError("variance_recovery must be non-negative")
    _validate_curvature(curvature)
    alpha = net_linear_benefit(linear_cost_slope)
    return (
        2.0 * alpha * mean_recovery
        - curvature * mean_recovery * mean_recovery
        - (curvature + 2.0 * gamma) * variance_recovery
    )


def direct_mean_game_payoff(
    recoveries: Sequence[float],
    frequencies: Sequence[float],
    linear_cost_slope: float,
    curvature: float,
    gamma: float,
) -> float:
    """Direct finite-distribution mean payoff for verification and discrete games."""

    if not recoveries or len(recoveries) != len(frequencies):
        raise ValueError("recoveries and frequencies must have same non-zero length")
    if any(r < 0.0 for r in recoveries):
        raise ValueError("recoveries must be non-negative")
    if any(p < 0.0 for p in frequencies):
        raise ValueError("frequencies must be non-negative")
    total = sum(frequencies)
    if abs(total - 1.0) > 1e-10:
        raise ValueError("frequencies must sum to one")

    result = 0.0
    for i, (ri, pi) in enumerate(zip(recoveries, frequencies)):
        for rj, pj in zip(recoveries, frequencies):
            kernel = (
                intrinsic_payoff(ri, linear_cost_slope, curvature)
                + intrinsic_payoff(rj, linear_cost_slope, curvature)
                + mismatch_feedback(ri, rj, gamma)
            )
            result += pi * pj * kernel
    return result


def distribution_moments(
    recoveries: Sequence[float], frequencies: Sequence[float]
) -> Tuple[float, float]:
    """Return (mean, population variance) for a discrete architecture distribution."""

    if not recoveries or len(recoveries) != len(frequencies):
        raise ValueError("recoveries and frequencies must have same non-zero length")
    if any(r < 0.0 for r in recoveries):
        raise ValueError("recoveries must be non-negative")
    if any(p < 0.0 for p in frequencies):
        raise ValueError("frequencies must be non-negative")
    if abs(sum(frequencies) - 1.0) > 1e-10:
        raise ValueError("frequencies must sum to one")
    mean = sum(p * r for p, r in zip(frequencies, recoveries))
    variance = sum(p * (r - mean) ** 2 for p, r in zip(frequencies, recoveries))
    return mean, variance


def endpoint_mixture_frequency(
    max_recovery: float,
    linear_cost_slope: float,
    curvature: float,
    gamma: float,
) -> float:
    """Return globally optimal endpoint D frequency when kappa+2gamma<0.

    Formula is clipped to [0,1] so it also covers parameter choices outside the
    interior-intrinsic-optimum theorem.
    """

    _validate_max_recovery(max_recovery)
    _validate_curvature(curvature)
    if curvature + 2.0 * gamma >= 0.0:
        raise ValueError("endpoint-mixture theorem requires curvature+2gamma<0")
    alpha = net_linear_benefit(linear_cost_slope)
    numerator = 2.0 * alpha - (curvature + 2.0 * gamma) * max_recovery
    denominator = -4.0 * gamma * max_recovery
    return _clip(numerator / denominator, 0.0, 1.0)


def global_potential_optimum(
    max_recovery: float,
    linear_cost_slope: float,
    curvature: float,
    gamma: float,
    tol: float = 1e-12,
) -> Dict[str, float | str]:
    """Return exact global-potential optimizer for the quadratic continuous game."""

    _validate_max_recovery(max_recovery)
    _validate_curvature(curvature)
    coefficient = curvature + 2.0 * gamma
    r0 = no_feedback_optimum(max_recovery, linear_cost_slope, curvature)

    if coefficient > tol:
        return {
            "regime": "monomorphic",
            "mean_recovery": r0,
            "variance_recovery": 0.0,
            "endpoint_d_frequency": float(r0 >= max_recovery - tol),
            "potential": mean_game_payoff_from_moments(
                r0, 0.0, linear_cost_slope, curvature, gamma
            ),
        }

    if coefficient >= -tol:
        return {
            "regime": "neutral_variance_manifold",
            "mean_recovery": r0,
            "variance_recovery": float("nan"),
            "endpoint_d_frequency": float("nan"),
            "potential": mean_game_payoff_from_moments(
                r0, 0.0, linear_cost_slope, curvature, gamma
            ),
        }

    p = endpoint_mixture_frequency(
        max_recovery, linear_cost_slope, curvature, gamma
    )
    mean = p * max_recovery
    variance = p * (1.0 - p) * max_recovery * max_recovery
    return {
        "regime": "endpoint_polymorphism" if 0.0 < p < 1.0 else "endpoint_monomorphism",
        "mean_recovery": mean,
        "variance_recovery": variance,
        "endpoint_d_frequency": p,
        "potential": mean_game_payoff_from_moments(
            mean, variance, linear_cost_slope, curvature, gamma
        ),
    }


def endpoint_subgame_parameters(
    max_recovery: float,
    linear_cost_slope: float,
    curvature: float,
    gamma: float,
) -> Tuple[float, float]:
    """Return (phi_endpoint,eta_endpoint) for endpoints r=0 and r=L."""

    _validate_max_recovery(max_recovery)
    phi = intrinsic_payoff(max_recovery, linear_cost_slope, curvature)
    eta = gamma * max_recovery * max_recovery
    return phi, eta


def endpoint_subgame_coexistence_frequency(
    max_recovery: float,
    linear_cost_slope: float,
    curvature: float,
    gamma: float,
) -> Optional[float]:
    """Return strict interior D frequency of endpoint two-strategy game, if any."""

    phi, eta = endpoint_subgame_parameters(
        max_recovery, linear_cost_slope, curvature, gamma
    )
    if eta == 0.0:
        return None
    p = 0.5 * (1.0 - phi / eta)
    if 0.0 < p < 1.0:
        return p
    return None


def endpoint_mixture_mutant_relative_payoff(
    mutant_recovery: float,
    max_recovery: float,
    endpoint_d_frequency: float,
    linear_cost_slope: float,
    curvature: float,
    gamma: float,
) -> float:
    """Return mutant payoff minus endpoint-S payoff against an endpoint mixture."""

    _validate_nonnegative_recovery(mutant_recovery)
    _validate_max_recovery(max_recovery)
    if mutant_recovery > max_recovery:
        raise ValueError("mutant_recovery cannot exceed max_recovery")
    if not 0.0 <= endpoint_d_frequency <= 1.0:
        raise ValueError("endpoint_d_frequency must lie in [0,1]")

    p = endpoint_d_frequency
    mutant = intrinsic_payoff(mutant_recovery, linear_cost_slope, curvature) + (
        (1.0 - p) * mismatch_feedback(mutant_recovery, 0.0, gamma)
        + p * mismatch_feedback(mutant_recovery, max_recovery, gamma)
    )
    endpoint_s = 0.0 + p * mismatch_feedback(0.0, max_recovery, gamma)
    return mutant - endpoint_s


def two_function_coupling_for_recovery(
    a: float,
    b: float,
    conflict_load: float,
    recovery: float,
) -> float:
    """Invert exact two-function R(lambda) to residual coupling lambda.

    R(lambda)=L*ab/[ab+lambda(a+b)].
    Returns +inf at recovery=0 and 0 at recovery=L.
    """

    if a <= 0.0 or b <= 0.0:
        raise ValueError("a and b must be positive")
    if conflict_load <= 0.0:
        raise ValueError("conflict_load must be positive")
    if recovery < 0.0 or recovery > conflict_load:
        raise ValueError("recovery must lie in [0,conflict_load]")
    if recovery == 0.0:
        return inf
    if recovery == conflict_load:
        return 0.0
    return a * b * (conflict_load - recovery) / (
        recovery * (a + b)
    )


def two_function_recovery_from_coupling(
    a: float,
    b: float,
    conflict_load: float,
    coupling: float,
) -> float:
    """Return exact two-function recovery R(lambda)."""

    if a <= 0.0 or b <= 0.0:
        raise ValueError("a and b must be positive")
    if conflict_load <= 0.0:
        raise ValueError("conflict_load must be positive")
    if coupling < 0.0:
        raise ValueError("coupling must be non-negative")
    return conflict_load * a * b / (a * b + coupling * (a + b))


def _validate_nonnegative_recovery(recovery: float) -> None:
    if recovery < 0.0:
        raise ValueError("recovery must be non-negative")


def _validate_max_recovery(max_recovery: float) -> None:
    if max_recovery <= 0.0:
        raise ValueError("max_recovery must be positive")


def _validate_curvature(curvature: float) -> None:
    if curvature <= 0.0:
        raise ValueError("curvature must be positive")


def _clip(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))
