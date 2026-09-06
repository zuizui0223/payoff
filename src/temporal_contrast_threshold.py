"""Exact critical seasonal contrast for anti-phase temporal coordination inversion.

The exact anti-phase dimensionless premium is F(u,v), with u=m*tau and
v=|x|tau. Let M(v)=max_u F(u,v). For v>0, M(v) is strictly increasing from 0
to infinity. Therefore every positive dimensionless barrier B has one unique
critical contrast v_c satisfying M(v_c)=B.
"""

from __future__ import annotations

from typing import Dict

from src.anti_phase_temporal import (
    dimensionless_premium,
    exact_optimal_dimensionless_migration,
)


def exact_max_dimensionless_premium(v: float) -> float:
    """Return M(v)=max_u F(u,v), including M(0)=0."""

    if v < 0.0:
        raise ValueError("v must be non-negative")
    if v == 0.0:
        return 0.0
    u_star = exact_optimal_dimensionless_migration(v)
    return dimensionless_premium(u_star, v)


def critical_dimensionless_contrast(
    dimensionless_barrier: float,
    tol: float = 1e-12,
) -> float:
    """Return unique v_c with M(v_c)=dimensionless_barrier.

    For temporal coordination inversion at phi_bar=0,
        dimensionless_barrier=eta*tau.
    For reciprocal invasion at nonzero mean static gap,
        dimensionless_barrier=(eta+|phi_bar|)*tau.
    """

    if dimensionless_barrier < 0.0:
        raise ValueError("dimensionless_barrier must be non-negative")
    if tol <= 0.0:
        raise ValueError("tol must be positive")
    if dimensionless_barrier == 0.0:
        return 0.0

    lower = 0.0
    upper = max(1.0, dimensionless_barrier + 1.0)
    while exact_max_dimensionless_premium(upper) < dimensionless_barrier:
        upper *= 2.0
        if upper > 300.0:
            raise RuntimeError("failed to bracket critical seasonal contrast")

    while upper - lower > tol * max(1.0, upper):
        mid = 0.5 * (lower + upper)
        if exact_max_dimensionless_premium(mid) < dimensionless_barrier:
            lower = mid
        else:
            upper = mid
    return 0.5 * (lower + upper)


def critical_contrast_half_amplitude(
    eta: float,
    mean_static_gap: float,
    season_duration: float,
) -> float:
    """Return exact |x| threshold for existence of reciprocal invasion.

    The target premium is eta+|phi_bar|, so the dimensionless barrier is
        B=(eta+|phi_bar|)tau.
    """

    if eta < 0.0:
        raise ValueError("eta must be non-negative")
    if season_duration <= 0.0:
        raise ValueError("season_duration must be positive")
    barrier = (eta + abs(mean_static_gap)) * season_duration
    return critical_dimensionless_contrast(barrier) / season_duration


def weak_barrier_critical_contrast_approx(dimensionless_barrier: float) -> float:
    """Return v_c ~= sqrt(B/H*) for small B."""

    if dimensionless_barrier < 0.0:
        raise ValueError("dimensionless_barrier must be non-negative")
    if dimensionless_barrier == 0.0:
        return 0.0
    h_star = 0.1324875394468274
    return (dimensionless_barrier / h_star) ** 0.5


def strong_barrier_critical_contrast_approx(dimensionless_barrier: float) -> float:
    """Large-B first approximation v_c ~= B+log(B)+1.

    The exact strong-contrast maximum obeys
        M(v)=v-log(v)-1+O(1/v).
    This approximation is intended only for dimensionless_barrier >> 1.
    """

    from math import log

    if dimensionless_barrier <= 0.0:
        raise ValueError("strong-barrier approximation requires positive barrier")
    return dimensionless_barrier + log(dimensionless_barrier) + 1.0


def contrast_threshold_summary(
    eta: float,
    mean_static_gap: float,
    season_duration: float,
) -> Dict[str, float]:
    """Return exact and asymptotic contrast thresholds."""

    if eta < 0.0:
        raise ValueError("eta must be non-negative")
    if season_duration <= 0.0:
        raise ValueError("season_duration must be positive")
    barrier = (eta + abs(mean_static_gap)) * season_duration
    v_critical = critical_dimensionless_contrast(barrier)
    return {
        "dimensionless_barrier": barrier,
        "critical_dimensionless_contrast": v_critical,
        "critical_contrast_half_amplitude": v_critical / season_duration,
        "weak_barrier_approximation": weak_barrier_critical_contrast_approx(barrier),
        "strong_barrier_approximation": (
            strong_barrier_critical_contrast_approx(barrier)
            if barrier > 0.0
            else 0.0
        ),
    }
