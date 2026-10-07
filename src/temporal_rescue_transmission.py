"""Temporal rescue transmission utilities for PAYOFF-B."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class TemporalTransmission:
    prebreed_vs_migration_slope: float
    transmission: float
    regime: str


def temporal_rescue_transmission(
    prebreed_vs_migration_slope: float,
) -> TemporalTransmission:
    """Return tau = 1 + beta and a transparent regime label."""

    beta = float(prebreed_vs_migration_slope)
    if not isfinite(beta):
        raise ValueError("slope must be finite")

    tau = 1.0 + beta
    if tau < 0.0:
        regime = "REVERSAL"
    elif abs(tau) <= 1e-12:
        regime = "FULL_DEBT_TRANSFER"
    elif tau < 1.0:
        regime = "PARTIAL_TRANSMISSION"
    elif abs(tau - 1.0) <= 1e-12:
        regime = "FULL_TRANSMISSION"
    else:
        regime = "AMPLIFIED_OR_CONFOUNDED"

    return TemporalTransmission(
        prebreed_vs_migration_slope=beta,
        transmission=tau,
        regime=regime,
    )


def linear_state_debt_transmission(
    marginal_debt_per_day_corrected: float,
    recovery_rate: float,
) -> float:
    """Return tau = 1 - D'(u)/rho for a local linear debt witness."""

    debt = float(marginal_debt_per_day_corrected)
    rho = float(recovery_rate)
    if not isfinite(debt) or debt < 0.0:
        raise ValueError("marginal debt must be finite and non-negative")
    if not isfinite(rho) or rho <= 0.0:
        raise ValueError("recovery_rate must be finite and positive")
    return 1.0 - debt / rho


def environmental_response_transmission(
    downstream_timing_slope: float,
    upstream_timing_slope: float,
) -> float:
    """Ratio of downstream to upstream response to the same forcing."""

    downstream = float(downstream_timing_slope)
    upstream = float(upstream_timing_slope)
    if not isfinite(downstream) or not isfinite(upstream):
        raise ValueError("slopes must be finite")
    if abs(upstream) <= 1e-12:
        raise ValueError("upstream timing slope must be non-zero")
    return downstream / upstream
