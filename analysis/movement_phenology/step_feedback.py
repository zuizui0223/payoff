"""Discrete movement–phenology STEP-controller utilities."""

from __future__ import annotations

import math


def phase_transfer_slope_from_stopover_gain(
    stopover_gain: float,
    travel_time_gain: float = 0.0,
) -> float:
    """Return lambda = 1 - g_stop - g_travel.

    Gains are defined as positive when a later phase error shortens elapsed time.
    """
    gs = float(stopover_gain)
    gf = float(travel_time_gain)
    if not math.isfinite(gs) or not math.isfinite(gf):
        raise ValueError("controller gains must be finite")
    return 1.0 - gs - gf


def stopover_gain_from_slope(stopover_slope_days_per_phase_day: float) -> float:
    """Convert d(stopover)/dE to positive correction gain."""
    slope = float(stopover_slope_days_per_phase_day)
    if not math.isfinite(slope):
        raise ValueError("stopover slope must be finite")
    return -slope


def is_locally_contracting(phase_transfer_slope: float) -> bool:
    """Whether a one-step phase map is locally contracting."""
    lam = float(phase_transfer_slope)
    if not math.isfinite(lam):
        raise ValueError("phase-transfer slope must be finite")
    return abs(lam) < 1.0


def correction_fraction(phase_transfer_slope: float) -> float:
    """Signed fraction of phase error removed in one local linear step.

    lambda=1 -> zero correction
    lambda=0 -> full first-order reset
    0<lambda<1 -> partial correction
    lambda<0 -> overshoot after more than full correction
    """
    lam = float(phase_transfer_slope)
    if not math.isfinite(lam):
        raise ValueError("phase-transfer slope must be finite")
    return 1.0 - lam
