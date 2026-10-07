"""Behavior-independent local phase-readability metrics for PAYOFF-B V7B.

These helpers transform an already-fitted annual vegetation curve into
predeclared local phase-readability proxies. They do not use animal movement or
behavioral outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from src.irg_reconstruction import PeakIRGFit


@dataclass(frozen=True)
class LocalPhaseReadability:
    peak_irg: float
    inverse_spring_scale: float
    peak_irg_over_rmse: float | None


def local_phase_readability(fit: PeakIRGFit) -> LocalPhaseReadability:
    """Return the frozen V7B primary and sensitivity coordinates."""

    peak = float(fit.peak_irg_value)
    scale = float(fit.spring_scale_days)
    rmse = float(fit.fit_rmse)

    if not isfinite(peak) or peak <= 0.0:
        raise ValueError("peak IRG must be finite and positive")
    if not isfinite(scale) or scale <= 0.0:
        raise ValueError("spring scale must be finite and positive")
    if not isfinite(rmse) or rmse < 0.0:
        raise ValueError("fit RMSE must be finite and non-negative")

    snr = None if rmse == 0.0 else peak / rmse
    return LocalPhaseReadability(
        peak_irg=peak,
        inverse_spring_scale=1.0 / scale,
        peak_irg_over_rmse=snr,
    )
