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

from math import asinh, sinh, sqrt
from typing import Dict


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
    return mean_margin - m + asinh((m / delta) * sinh(delta * tau)) / tau


def anti_phase_temporal_premium(
    contrast_half_amplitude: float,
    migration_rate: float,
    season_duration: float,
) -> float:
    """Return exact periodic minus time-averaged invasion exponent."""

    return anti_phase_floquet_exponent(
        0.0, contrast_half_amplitude, migration_rate, season_duration
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
    return {
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
        "rescued": float(mean_margin < 0.0 < floquet),
    }


def _validate(migration_rate: float, season_duration: float) -> None:
    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    if season_duration <= 0.0:
        raise ValueError("season_duration must be positive")
