"""Exact temporal baseline for common additive environmental forcing.

If every patch's rare-D margin receives the same scalar shift q(t), then
    A_D(t)=A_D0+q(t)I.
The scalar identity term commutes with A_D0 at all times, so finite-time and
long-run growth separate exactly into baseline spatial growth plus the time
average of q. Rare-S receives the opposite shift.
"""

from __future__ import annotations

from typing import Dict, Sequence, Tuple


def mean_shift(shifts: Sequence[float], durations: Sequence[float] | None = None) -> float:
    """Return time-weighted mean scalar environmental shift."""

    if not shifts:
        raise ValueError("shifts cannot be empty")
    if durations is None:
        return sum(shifts) / len(shifts)
    if len(shifts) != len(durations):
        raise ValueError("shifts and durations must have the same length")
    if any(duration <= 0.0 for duration in durations):
        raise ValueError("durations must be positive")
    total = sum(durations)
    return sum(shift * duration for shift, duration in zip(shifts, durations)) / total


def temporal_invasion_exponents(
    lambda_d_baseline: float,
    lambda_s_baseline: float,
    shifts: Sequence[float],
    durations: Sequence[float] | None = None,
) -> Tuple[float, float]:
    """Return long-run rare-D and rare-S exponents under common shifts."""

    q_bar = mean_shift(shifts, durations)
    return lambda_d_baseline + q_bar, lambda_s_baseline - q_bar


def linear_environment_shifts(
    environments: Sequence[float], reference_environment: float, slope: float
) -> list[float]:
    """Return q(t)=alpha[e(t)-e0] for sampled/seasonal environments."""

    if not environments:
        raise ValueError("environments cannot be empty")
    return [slope * (environment - reference_environment) for environment in environments]


def linear_environment_temporal_exponents(
    lambda_d_baseline: float,
    lambda_s_baseline: float,
    environments: Sequence[float],
    reference_environment: float,
    slope: float,
    durations: Sequence[float] | None = None,
) -> Tuple[float, float]:
    """Return exact exponents under common linear environmental forcing."""

    shifts = linear_environment_shifts(environments, reference_environment, slope)
    return temporal_invasion_exponents(
        lambda_d_baseline, lambda_s_baseline, shifts, durations
    )


def finite_time_log_multiplier(
    baseline_exponent: float,
    shifts: Sequence[float],
    durations: Sequence[float],
) -> float:
    """Return log growth multiplier along a baseline eigenmode over all seasons.

    If the baseline eigenmode has growth exponent lambda0, then
        log M = lambda0*T + sum q_l*tau_l.
    """

    if len(shifts) != len(durations) or not shifts:
        raise ValueError("shifts and durations must have the same non-zero length")
    if any(duration <= 0.0 for duration in durations):
        raise ValueError("durations must be positive")
    return baseline_exponent * sum(durations) + sum(
        shift * duration for shift, duration in zip(shifts, durations)
    )


def zero_mean_fluctuation_residual(
    lambda_baseline: float,
    shifts: Sequence[float],
    durations: Sequence[float] | None = None,
) -> float:
    """Return temporal exponent minus baseline; zero for mean-zero forcing."""

    return lambda_baseline + mean_shift(shifts, durations) - lambda_baseline


def temporal_environment_summary(
    lambda_d_baseline: float,
    lambda_s_baseline: float,
    environments: Sequence[float],
    reference_environment: float,
    slope: float,
    durations: Sequence[float] | None = None,
) -> Dict[str, float]:
    """Summarize mean environment shift and reciprocal temporal exponents."""

    shifts = linear_environment_shifts(environments, reference_environment, slope)
    q_bar = mean_shift(shifts, durations)
    lambda_d, lambda_s = temporal_invasion_exponents(
        lambda_d_baseline, lambda_s_baseline, shifts, durations
    )
    return {
        "mean_environment_shift": q_bar,
        "lambda_d_temporal": lambda_d,
        "lambda_s_temporal": lambda_s,
        "signed_reciprocal_exponent_sum": lambda_d + lambda_s,
    }
