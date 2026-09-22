"""Phase-uncertainty propagation under separate feedback and environmental innovation."""

from __future__ import annotations

import math
from collections.abc import Iterable


def next_phase_variance(
    current_variance_days2: float,
    phase_retention_lambda: float,
    innovation_sd_days: float,
) -> float:
    """V_next = lambda^2 V + sigma_innovation^2."""
    v = float(current_variance_days2)
    lam = float(phase_retention_lambda)
    sd = float(innovation_sd_days)
    if not all(math.isfinite(x) for x in (v, lam, sd)):
        raise ValueError("arguments must be finite")
    if v < 0:
        raise ValueError("variance must be non-negative")
    if sd < 0:
        raise ValueError("innovation SD must be non-negative")
    return lam * lam * v + sd * sd


def stationary_phase_variance(
    phase_retention_lambda: float,
    innovation_sd_days: float,
) -> float:
    """Stationary variance sigma^2/(1-lambda^2), requiring |lambda|<1."""
    lam = float(phase_retention_lambda)
    sd = float(innovation_sd_days)
    if not math.isfinite(lam) or not math.isfinite(sd):
        raise ValueError("arguments must be finite")
    if abs(lam) >= 1:
        raise ValueError("stationary variance requires |lambda| < 1")
    if sd < 0:
        raise ValueError("innovation SD must be non-negative")
    return sd * sd / (1.0 - lam * lam)


def stationary_phase_sd(
    phase_retention_lambda: float,
    innovation_sd_days: float,
) -> float:
    return math.sqrt(
        stationary_phase_variance(
            phase_retention_lambda,
            innovation_sd_days,
        )
    )


def constant_route_variance_after_steps(
    initial_variance_days2: float,
    phase_retention_lambda: float,
    innovation_sd_days: float,
    steps: int,
) -> float:
    """Closed-form finite-n variance for a constant controller/environment."""
    if isinstance(steps, bool) or int(steps) != steps or steps < 0:
        raise ValueError("steps must be a non-negative integer")
    n = int(steps)
    v0 = float(initial_variance_days2)
    lam = float(phase_retention_lambda)
    sd = float(innovation_sd_days)
    if not all(math.isfinite(x) for x in (v0, lam, sd)):
        raise ValueError("arguments must be finite")
    if v0 < 0 or sd < 0:
        raise ValueError("variance and innovation SD must be non-negative")
    if n == 0:
        return v0
    if abs(lam) == 1:
        return v0 + n * sd * sd
    return (
        (lam ** (2 * n)) * v0
        + sd * sd * (1.0 - lam ** (2 * n)) / (1.0 - lam * lam)
    )


def propagate_route_variance(
    initial_variance_days2: float,
    phase_retention_lambdas: Iterable[float],
    innovation_sds_days: Iterable[float],
) -> list[float]:
    """Return [V0,V1,...] for a route with stage-specific lambda and innovation."""
    lambdas = list(phase_retention_lambdas)
    sds = list(innovation_sds_days)
    if len(lambdas) != len(sds):
        raise ValueError("lambda and innovation sequences must have equal length")
    v = float(initial_variance_days2)
    if not math.isfinite(v) or v < 0:
        raise ValueError("initial variance must be finite and non-negative")
    out = [v]
    for lam, sd in zip(lambdas, sds):
        v = next_phase_variance(v, lam, sd)
        out.append(v)
    return out
