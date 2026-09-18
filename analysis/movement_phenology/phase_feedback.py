"""Phase-error feedback dynamics for movement–phenology tracking."""

from __future__ import annotations

import math


def exponential_relative_speed(
    phase_error_days: float,
    u0: float,
    kappa_per_day: float,
) -> float:
    """u(E)=u0*exp(kappa*E)."""
    e = float(phase_error_days)
    u0 = float(u0)
    k = float(kappa_per_day)
    if not all(math.isfinite(z) for z in (e, u0, k)):
        raise ValueError("arguments must be finite")
    if u0 <= 0:
        raise ValueError("u0 must be positive")
    return u0 * math.exp(k * e)


def equilibrium_phase_error_days(u0: float, kappa_per_day: float) -> float:
    """Phase offset E* where the exponential controller has u(E*)=1."""
    u0 = float(u0)
    k = float(kappa_per_day)
    if not math.isfinite(u0) or not math.isfinite(k):
        raise ValueError("arguments must be finite")
    if u0 <= 0:
        raise ValueError("u0 must be positive")
    if k == 0:
        raise ValueError("kappa must be nonzero")
    return -math.log(u0) / k


def phase_error_spatial_derivative(
    phase_error_days: float,
    environment_speed_km_day: float,
    u0: float,
    kappa_per_day: float,
) -> float:
    """dE/ds in days/km under exponential error feedback."""
    ce = float(environment_speed_km_day)
    if not math.isfinite(ce) or ce <= 0:
        raise ValueError("environment speed must be positive and finite")
    u = exponential_relative_speed(phase_error_days, u0, kappa_per_day)
    return (1.0 / u - 1.0) / ce


def local_relaxation_distance_km(
    environment_speed_km_day: float,
    kappa_per_day: float,
) -> float:
    """Local e-folding distance ce/kappa for a stabilizing kappa>0 controller."""
    ce = float(environment_speed_km_day)
    k = float(kappa_per_day)
    if not math.isfinite(ce) or not math.isfinite(k):
        raise ValueError("arguments must be finite")
    if ce <= 0:
        raise ValueError("environment speed must be positive")
    if k <= 0:
        raise ValueError("kappa must be positive for stabilizing relaxation")
    return ce / k


def local_half_distance_km(
    environment_speed_km_day: float,
    kappa_per_day: float,
) -> float:
    """Distance for small phase perturbations to halve."""
    return math.log(2.0) * local_relaxation_distance_km(
        environment_speed_km_day, kappa_per_day
    )
