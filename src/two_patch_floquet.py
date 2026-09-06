"""Exact two-patch Floquet extension for temporally varying local margins.

For one rare architecture, season l has local linear margins r1_l,r2_l and
constant symmetric migration m. The seasonal operator is
    A_l=[[r1_l-m, m], [m, r2_l-m]].
Each 2x2 symmetric matrix exponential is available in closed form. The product
over a period gives the exact principal Floquet exponent.
"""

from __future__ import annotations

from math import cosh, exp, log, sqrt
from typing import Dict, Sequence, Tuple

from src.environment_mosaic import two_patch_invasion_exponent

Season = Tuple[float, float, float]
Matrix2 = Tuple[Tuple[float, float], Tuple[float, float]]


def seasonal_operator(r1: float, r2: float, migration_rate: float) -> Matrix2:
    """Return the symmetric two-patch rare-type operator for one season."""

    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    return (
        (r1 - migration_rate, migration_rate),
        (migration_rate, r2 - migration_rate),
    )


def seasonal_matrix_exponential(
    r1: float, r2: float, migration_rate: float, duration: float
) -> Matrix2:
    """Return exp(A*tau) in closed form for one symmetric two-patch season."""

    if duration < 0.0:
        raise ValueError("duration must be non-negative")
    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")

    a = r1 - migration_rate
    d = r2 - migration_rate
    b = migration_rate
    center = 0.5 * (a + d)
    contrast = 0.5 * (a - d)
    delta = sqrt(contrast * contrast + b * b)
    scale = exp(center * duration)
    if delta == 0.0:
        return ((scale, 0.0), (0.0, scale))

    c = cosh(delta * duration)
    # sinh(x) computed from exponentials to avoid another import and to keep
    # the formula explicit.
    x = delta * duration
    s_over_delta = 0.5 * (exp(x) - exp(-x)) / delta
    return (
        (
            scale * (c + s_over_delta * contrast),
            scale * s_over_delta * b,
        ),
        (
            scale * s_over_delta * b,
            scale * (c - s_over_delta * contrast),
        ),
    )


def commutator_scalar(
    season_a: Sequence[float], season_b: Sequence[float], migration_rate: float
) -> float:
    """Return c where [A_a,A_b]=[[0,c],[-c,0]].

    The two seasonal operators commute iff this scalar is zero:
        c=m[(r1_a-r2_a)-(r1_b-r2_b)].
    Durations, if included as third entries, do not affect the commutator gate.
    """

    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    if len(season_a) < 2 or len(season_b) < 2:
        raise ValueError("each season must contain at least r1 and r2")
    contrast_a = season_a[0] - season_a[1]
    contrast_b = season_b[0] - season_b[1]
    return migration_rate * (contrast_a - contrast_b)


def period_matrix(seasons: Sequence[Season], migration_rate: float) -> Matrix2:
    """Return the chronological one-period propagator E_M...E_2 E_1."""

    _validate_seasons(seasons)
    product: Matrix2 = ((1.0, 0.0), (0.0, 1.0))
    for r1, r2, duration in seasons:
        seasonal = seasonal_matrix_exponential(r1, r2, migration_rate, duration)
        product = _matmul(seasonal, product)
    return product


def floquet_exponent(seasons: Sequence[Season], migration_rate: float) -> float:
    """Return the exact principal Floquet exponent per unit time."""

    _validate_seasons(seasons)
    propagator = period_matrix(seasons, migration_rate)
    radius = _spectral_radius_positive_2x2(propagator)
    total_time = sum(duration for _, _, duration in seasons)
    return log(radius) / total_time


def time_averaged_operator_exponent(
    seasons: Sequence[Season], migration_rate: float
) -> float:
    """Principal exponent of the operator built from time-averaged margins."""

    _validate_seasons(seasons)
    total_time = sum(duration for _, _, duration in seasons)
    mean_r1 = sum(r1 * duration for r1, _, duration in seasons) / total_time
    mean_r2 = sum(r2 * duration for _, r2, duration in seasons) / total_time
    return two_patch_invasion_exponent(mean_r1, mean_r2, migration_rate)


def temporal_noncommutativity_effect(
    seasons: Sequence[Season], migration_rate: float
) -> float:
    """Return Floquet exponent minus exponent of the time-averaged operator."""

    return floquet_exponent(seasons, migration_rate) - time_averaged_operator_exponent(
        seasons, migration_rate
    )


def floquet_summary(seasons: Sequence[Season], migration_rate: float) -> Dict[str, float]:
    """Summarize exact periodic and time-averaged growth predictions."""

    floquet = floquet_exponent(seasons, migration_rate)
    averaged = time_averaged_operator_exponent(seasons, migration_rate)
    max_commutator = 0.0
    for i in range(len(seasons)):
        for j in range(i + 1, len(seasons)):
            max_commutator = max(
                max_commutator,
                abs(commutator_scalar(seasons[i], seasons[j], migration_rate)),
            )
    return {
        "floquet_exponent": floquet,
        "time_averaged_operator_exponent": averaged,
        "temporal_effect": floquet - averaged,
        "max_pairwise_commutator_scalar": max_commutator,
    }


def _matmul(a: Matrix2, b: Matrix2) -> Matrix2:
    return (
        (
            a[0][0] * b[0][0] + a[0][1] * b[1][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1],
        ),
        (
            a[1][0] * b[0][0] + a[1][1] * b[1][0],
            a[1][0] * b[0][1] + a[1][1] * b[1][1],
        ),
    )


def _spectral_radius_positive_2x2(matrix: Matrix2) -> float:
    a, b = matrix[0]
    c, d = matrix[1]
    trace = a + d
    determinant = a * d - b * c
    discriminant = (a - d) ** 2 + 4.0 * b * c
    if discriminant < 0.0 and discriminant > -1e-12:
        discriminant = 0.0
    if discriminant < 0.0:
        raise ValueError("period matrix has non-real eigenvalues")
    lambda_plus = 0.5 * (trace + sqrt(discriminant))
    if lambda_plus <= 0.0:
        raise ValueError("principal period multiplier must be positive")
    return lambda_plus


def _validate_seasons(seasons: Sequence[Season]) -> None:
    if not seasons:
        raise ValueError("seasons cannot be empty")
    if any(len(season) != 3 for season in seasons):
        raise ValueError("each season must be (r1,r2,duration)")
    if any(duration <= 0.0 for _, _, duration in seasons):
        raise ValueError("season durations must be positive")
