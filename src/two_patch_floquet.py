"""Exact two-patch Floquet extension for temporally varying local margins.

For one rare architecture, season l has local linear margins r1_l,r2_l and
constant symmetric migration m. The seasonal operator is
    A_l=[[r1_l-m, m], [m, r2_l-m]].
Each 2x2 symmetric matrix exponential is available in closed form. The product
over a period gives the exact principal Floquet exponent.

For exactly two seasons, the principal exponent has an additional scalar
closed form. Golden-Thompson then implies that the periodic Floquet exponent is
never below the principal eigenvalue of the time-averaged operator in this
specific two-season symmetric model. Equality holds when the seasonal
operators commute.
"""

from __future__ import annotations

from math import acosh, cosh, exp, log, sqrt
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


def two_season_closed_form(seasons: Sequence[Season], migration_rate: float) -> float:
    """Exact scalar Floquet formula for exactly two seasons.

    Write, for season l,
        a_l=(r1_l+r2_l)/2-m,
        x_l=(r1_l-r2_l)/2,
        d_l=sqrt(x_l^2+m^2),
        u_l=d_l*tau_l.

    If
        C=cosh(u1)cosh(u2)
          +[(x1*x2+m^2)/(d1*d2)]sinh(u1)sinh(u2),
    then
        Lambda_F=(a1*tau1+a2*tau2)/T + acosh(C)/T.
    """

    _validate_two_seasons(seasons)
    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")

    (r11, r21, tau1), (r12, r22, tau2) = seasons
    a1 = 0.5 * (r11 + r21) - migration_rate
    a2 = 0.5 * (r12 + r22) - migration_rate
    x1 = 0.5 * (r11 - r21)
    x2 = 0.5 * (r12 - r22)
    d1 = sqrt(x1 * x1 + migration_rate * migration_rate)
    d2 = sqrt(x2 * x2 + migration_rate * migration_rate)
    u1 = d1 * tau1
    u2 = d2 * tau2

    c1 = cosh(u1)
    c2 = cosh(u2)
    s1 = 0.5 * (exp(u1) - exp(-u1))
    s2 = 0.5 * (exp(u2) - exp(-u2))

    if d1 == 0.0 or d2 == 0.0:
        # A zero traceless part commutes with everything; direct exact routine
        # is simpler and avoids a 0/0 in the normalized dot product.
        return floquet_exponent(seasons, migration_rate)

    alignment = (x1 * x2 + migration_rate * migration_rate) / (d1 * d2)
    c_value = c1 * c2 + alignment * s1 * s2
    if c_value < 1.0 and c_value > 1.0 - 1e-12:
        c_value = 1.0
    if c_value < 1.0:
        raise ValueError("closed-form hyperbolic trace must be at least one")

    total_time = tau1 + tau2
    center_rate = (a1 * tau1 + a2 * tau2) / total_time
    return center_rate + acosh(c_value) / total_time


def two_season_temporal_premium(
    seasons: Sequence[Season], migration_rate: float
) -> float:
    """Floquet exponent minus time-averaged-operator exponent for two seasons.

    In the declared two-season symmetric model this value is non-negative.
    It is zero when the seasonal operators commute, including m=0 or unchanged
    patch contrast across seasons.
    """

    _validate_two_seasons(seasons)
    return two_season_closed_form(seasons, migration_rate) - time_averaged_operator_exponent(
        seasons, migration_rate
    )


def fast_switching_premium_coefficient(
    season_a: Sequence[float],
    season_b: Sequence[float],
    migration_rate: float,
    season_a_fraction: float,
) -> float:
    """Coefficient C2 in premium = C2*T^2 + O(T^4) for rapid switching.

    `season_a` and `season_b` provide at least (r1,r2). If the total period is
    T and season A occupies fraction w, then

        premium
        = T^2 * w^2(1-w)^2 * m^2 * (Delta_c)^2
          / [24 delta_bar]
          + O(T^4),

    where Delta_c is the change in patch contrast
        (r1-r2)_A-(r1-r2)_B,
    and
        delta_bar=sqrt(x_bar^2+m^2),
        x_bar=[w(r1-r2)_A+(1-w)(r1-r2)_B]/2.

    The coefficient is non-negative and vanishes exactly at the basic
    commutator gates m=0 or unchanged patch contrast (apart from the degenerate
    delta_bar=0 case, where the exact formula should be used).
    """

    if len(season_a) < 2 or len(season_b) < 2:
        raise ValueError("each season must contain at least r1 and r2")
    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    if not 0.0 < season_a_fraction < 1.0:
        raise ValueError("season_a_fraction must lie strictly between 0 and 1")

    w = season_a_fraction
    contrast_a = season_a[0] - season_a[1]
    contrast_b = season_b[0] - season_b[1]
    delta_contrast = contrast_a - contrast_b
    x_bar = 0.5 * (w * contrast_a + (1.0 - w) * contrast_b)
    delta_bar = sqrt(x_bar * x_bar + migration_rate * migration_rate)
    if delta_bar == 0.0:
        return 0.0
    return (
        w * w
        * (1.0 - w) ** 2
        * migration_rate**2
        * delta_contrast**2
        / (24.0 * delta_bar)
    )


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


def _validate_two_seasons(seasons: Sequence[Season]) -> None:
    _validate_seasons(seasons)
    if len(seasons) != 2:
        raise ValueError("exact two-season formula requires exactly two seasons")
