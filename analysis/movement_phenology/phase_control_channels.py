"""Feed-forward environmental prediction plus phase-feedback retention."""

from __future__ import annotations

import math


def stationary_phase_variance(
    environmental_innovation_variance: float,
    behavioral_noise_variance: float,
    phase_retention_lambda: float,
) -> float:
    """AR(1) phase variance benchmark: (sigma_env^2+sigma_beh^2)/(1-lambda^2)."""
    se = float(environmental_innovation_variance)
    sb = float(behavioral_noise_variance)
    lam = float(phase_retention_lambda)
    if not all(math.isfinite(x) for x in (se, sb, lam)):
        raise ValueError("arguments must be finite")
    if se < 0 or sb < 0:
        raise ValueError("variances must be non-negative")
    if abs(lam) >= 1:
        raise ValueError("stationary benchmark requires |lambda| < 1")
    return (se + sb) / (1.0 - lam * lam)


def correction_strength(phase_retention_lambda: float) -> float:
    """Net contraction score 1-|lambda|; positive only for stable contraction."""
    lam = float(phase_retention_lambda)
    if not math.isfinite(lam):
        raise ValueError("lambda must be finite")
    return 1.0 - abs(lam)


def environmental_predictability_r2(
    destination_variance: float,
    innovation_variance: float,
) -> float:
    """Fraction of destination environmental variance explained by a forecast."""
    vy = float(destination_variance)
    ve = float(innovation_variance)
    if not math.isfinite(vy) or not math.isfinite(ve):
        raise ValueError("variances must be finite")
    if vy <= 0 or ve < 0:
        raise ValueError("destination variance must be positive and innovation non-negative")
    return 1.0 - ve / vy
