"""Exact anti-phase two-patch seasonal source-switching specialization.

Two equal-length seasons of duration tau swap patch quality:
    season A: (rbar+x, rbar-x)
    season B: (rbar-x, rbar+x)
with symmetric migration rate m.

The time-averaged operator has principal exponent rbar. The exact periodic
Floquet exponent is
    rbar-m + asinh[(m/d)sinh(d tau)]/tau,
where d=sqrt(m^2+x^2).
The difference from rbar is the temporal rescue premium.
"""

from __future__ import annotations

from math import asinh, cosh, exp, log, log1p, sinh, sqrt, tanh
from typing import Dict


def _asinh_ratio_sinh(numerator: float, denominator: float, argument: float) -> float:
    """Return asinh((numerator/denominator)*sinh(argument)) stably.

    All arguments used here are non-negative.  Evaluating ``sinh(argument)``
    directly overflows near 710 even when the final asinh value is finite.
    Work on the log scale and only exponentiate while the scaled sinh itself
    remains representable.
    """

    if numerator == 0.0 or argument == 0.0:
        return 0.0
    if argument < 20.0:
        log_sinh = log(sinh(argument))
    else:
        log_sinh = argument - log(2.0) + log1p(-exp(-2.0 * argument))
    log_scaled_sinh = log(numerator) - log(denominator) + log_sinh
    if log_scaled_sinh > 700.0:
        return log_scaled_sinh + log(2.0)
    return asinh(exp(log_scaled_sinh))


def anti_phase_floquet_exponent(
    mean_margin: float,
    contrast_half_amplitude: float,
    migration_rate: float,
    season_duration: float,
) -> float:
    """Return the exact Floquet exponent for symmetric anti-phase switching."""

    _validate(migration_rate, season_duration)
    x = abs(contrast_half_amplitude)
    m = migration_rate
    tau = season_duration
    if m == 0.0:
        return mean_margin
    delta = sqrt(m * m + x * x)
    growth_term = _asinh_ratio_sinh(m, delta, delta * tau)
    return mean_margin - m + growth_term / tau


def anti_phase_temporal_premium(
    contrast_half_amplitude: float,
    migration_rate: float,
    season_duration: float,
) -> float:
    """Return exact periodic minus time-averaged invasion exponent."""

    return anti_phase_floquet_exponent(
        0.0, contrast_half_amplitude, migration_rate, season_duration
    )


def dimensionless_premium(u: float, v: float) -> float:
    """Return F(u,v)=tau*P with u=m*tau and v=|x|*tau."""

    if u < 0.0 or v < 0.0:
        raise ValueError("u and v must be non-negative")
    if u == 0.0 or v == 0.0:
        return 0.0
    d = sqrt(u * u + v * v)
    return -u + _asinh_ratio_sinh(u, d, d)


def dimensionless_premium_derivative(u: float, v: float) -> float:
    """Return partial F/partial u for u>0,v>0."""

    if u <= 0.0 or v <= 0.0:
        raise ValueError("derivative formula requires u>0 and v>0")
    d = sqrt(u * u + v * v)
    s = sinh(d)
    c = cosh(d)
    y_prime = v * v * s / (d**3) + u * u * c / (d**2)
    root = sqrt(1.0 + (u * s / d) ** 2)
    return -1.0 + y_prime / root


def exact_optimal_dimensionless_migration(v: float, tol: float = 1e-13) -> float:
    """Return the unique exact maximizer u*=m*tau for fixed v=|x|tau>0.

    The proof of uniqueness is in theory/ANTI_PHASE_SEASONAL_RESCUE.md.
    Numerical solution uses the monotone crossing
        1-v^2/d^2 = R(d),
    where d=sqrt(u^2+v^2) and
        R(d)=(sinh(d)^2-d^2)/(d cosh(d)-sinh(d))^2.
    """

    if v <= 0.0:
        raise ValueError("v must be positive")
    if tol <= 0.0:
        raise ValueError("tol must be positive")

    def crossing(u: float) -> float:
        d = sqrt(u * u + v * v)
        left = u * u / (d * d)
        denom = d * cosh(d) - sinh(d)
        right = (sinh(d) ** 2 - d * d) / (denom * denom)
        return left - right

    lower = 0.0
    upper = max(1.0, v)
    while crossing(upper) < 0.0:
        upper *= 2.0
        if upper > 700.0:
            raise RuntimeError("failed to bracket exact anti-phase optimum")
    while upper - lower > tol * max(1.0, upper):
        mid = 0.5 * (lower + upper)
        if crossing(mid) < 0.0:
            lower = mid
        else:
            upper = mid
    return 0.5 * (lower + upper)


def exact_optimal_migration(
    contrast_half_amplitude: float,
    season_duration: float,
    tol: float = 1e-13,
) -> float:
    """Return the unique exact premium-maximizing migration rate."""

    if season_duration <= 0.0:
        raise ValueError("season_duration must be positive")
    v = abs(contrast_half_amplitude) * season_duration
    if v == 0.0:
        raise ValueError("nonzero contrast is required for an interior optimum")
    return exact_optimal_dimensionless_migration(v, tol) / season_duration


def exact_max_premium(
    contrast_half_amplitude: float,
    season_duration: float,
    tol: float = 1e-13,
) -> float:
    """Return the exact maximum temporal premium over migration."""

    m_star = exact_optimal_migration(
        contrast_half_amplitude, season_duration, tol
    )
    return anti_phase_temporal_premium(
        contrast_half_amplitude, m_star, season_duration
    )


def small_migration_slope(contrast_half_amplitude: float, season_duration: float) -> float:
    """Return d(premium)/dm at m=0+.

    With z=|x|tau,
        premium = m[sinh(z)/z - 1] + O(m^3).
    The z=0 limit is zero.
    """

    if season_duration <= 0.0:
        raise ValueError("season_duration must be positive")
    x = abs(contrast_half_amplitude)
    if x == 0.0:
        return 0.0
    z = x * season_duration
    return sinh(z) / z - 1.0


def fast_switching_premium(
    contrast_half_amplitude: float,
    migration_rate: float,
    season_duration: float,
) -> float:
    """Leading rapid-switching approximation to the exact temporal premium.

    For equal season durations tau,
        premium = m*x^2*tau^2/6 + O(tau^4),
    where x is half the between-patch margin contrast in each season.
    """

    _validate(migration_rate, season_duration)
    x = abs(contrast_half_amplitude)
    return migration_rate * x * x * season_duration * season_duration / 6.0


def strong_migration_premium_asymptotic(
    contrast_half_amplitude: float,
    migration_rate: float,
    season_duration: float,
) -> float:
    """Two-term large-m approximation to the temporal premium.

    premium
    = x^2/(2m) - x^2/(2m^2 tau) + O(m^-3)
    up to exponentially small terms for fixed positive tau.
    """

    _validate(migration_rate, season_duration)
    if migration_rate == 0.0:
        raise ValueError("large-m asymptotic requires positive migration")
    x2 = contrast_half_amplitude * contrast_half_amplitude
    m = migration_rate
    tau = season_duration
    return x2 / (2.0 * m) - x2 / (2.0 * m * m * tau)


def weak_contrast_shape(dimensionless_migration: float) -> float:
    """Universal O((x tau)^2) premium shape for weak seasonal contrast.

    With
        u=m tau,
        v=x tau,
    the dimensionless premium obeys
        tau*P = v^2 H(u) + O(v^4),
    where
        H(u)=(u-tanh u)/(2u^2).
    The continuous u=0 limit is zero.
    """

    u = dimensionless_migration
    if u < 0.0:
        raise ValueError("dimensionless_migration must be non-negative")
    if u == 0.0:
        return 0.0
    return (u - tanh(u)) / (2.0 * u * u)


def weak_contrast_optimal_dimensionless_migration(tol: float = 1e-14) -> float:
    """Return the unique positive maximizer u*=m*tau of the weak-contrast shape.

    u* is the unique positive root of
        u tanh(u)^2 - 2u + 2 tanh(u)=0,
    numerically about 1.6061152988.
    """

    if tol <= 0.0:
        raise ValueError("tol must be positive")

    def score(u: float) -> float:
        t = tanh(u)
        return u * t * t - 2.0 * u + 2.0 * t

    lower = 1.0
    upper = 2.0
    if not (score(lower) > 0.0 and score(upper) < 0.0):
        raise RuntimeError("failed to bracket weak-contrast optimum")
    while upper - lower > tol:
        mid = 0.5 * (lower + upper)
        if score(mid) > 0.0:
            lower = mid
        else:
            upper = mid
    return 0.5 * (lower + upper)


def weak_contrast_optimal_migration(season_duration: float) -> float:
    """Approximate optimal migration m*=u*/tau for |x|tau << 1."""

    if season_duration <= 0.0:
        raise ValueError("season_duration must be positive")
    return weak_contrast_optimal_dimensionless_migration() / season_duration


def weak_contrast_max_premium_approx(
    contrast_half_amplitude: float, season_duration: float
) -> float:
    """Approximate maximum temporal premium for |x|tau << 1.

    max P ~= H(u*) x^2 tau,
    where H(u*) ~= 0.1324875394.
    """

    if season_duration <= 0.0:
        raise ValueError("season_duration must be positive")
    u_star = weak_contrast_optimal_dimensionless_migration()
    return (
        weak_contrast_shape(u_star)
        * contrast_half_amplitude
        * contrast_half_amplitude
        * season_duration
    )


def rescue_condition(
    mean_margin: float,
    contrast_half_amplitude: float,
    migration_rate: float,
    season_duration: float,
) -> bool:
    """Return whether periodic switching makes the rare architecture invade."""

    return (
        anti_phase_floquet_exponent(
            mean_margin,
            contrast_half_amplitude,
            migration_rate,
            season_duration,
        )
        > 0.0
    )


def anti_phase_summary(
    mean_margin: float,
    contrast_half_amplitude: float,
    migration_rate: float,
    season_duration: float,
) -> Dict[str, float]:
    """Return exact and asymptotic anti-phase diagnostics."""

    floquet = anti_phase_floquet_exponent(
        mean_margin,
        contrast_half_amplitude,
        migration_rate,
        season_duration,
    )
    premium = floquet - mean_margin
    u_star_weak = weak_contrast_optimal_dimensionless_migration()
    summary: Dict[str, float] = {
        "mean_margin": mean_margin,
        "contrast_half_amplitude": contrast_half_amplitude,
        "migration_rate": migration_rate,
        "season_duration": season_duration,
        "time_averaged_exponent": mean_margin,
        "floquet_exponent": floquet,
        "temporal_premium": premium,
        "small_migration_slope": small_migration_slope(
            contrast_half_amplitude, season_duration
        ),
        "fast_switching_premium": fast_switching_premium(
            contrast_half_amplitude, migration_rate, season_duration
        ),
        "weak_contrast_u_star": u_star_weak,
        "weak_contrast_shape_max": weak_contrast_shape(u_star_weak),
        "weak_contrast_optimal_migration": u_star_weak / season_duration,
        "weak_contrast_max_premium": weak_contrast_max_premium_approx(
            contrast_half_amplitude, season_duration
        ),
        "rescued": float(mean_margin < 0.0 < floquet),
    }
    if contrast_half_amplitude != 0.0:
        exact_m = exact_optimal_migration(
            contrast_half_amplitude, season_duration
        )
        summary["exact_optimal_migration"] = exact_m
        summary["exact_optimal_dimensionless_migration"] = exact_m * season_duration
        summary["exact_max_premium"] = anti_phase_temporal_premium(
            contrast_half_amplitude, exact_m, season_duration
        )
    return summary


def _validate(migration_rate: float, season_duration: float) -> None:
    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    if season_duration <= 0.0:
        raise ValueError("season_duration must be positive")
