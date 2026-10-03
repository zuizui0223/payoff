"""Stage-to-stage timing handoff identities for PAYOFF-B.

A later seasonal event can be written as

    T_next = T_entry + W,

where W is the interval between the two events.

For simple OLS with an intercept on the same observations,

    beta(next ~ entry) = 1 + beta(W ~ entry).

This identity is descriptive.  A negative interval slope indicates buffering of
upstream timing variation, but does not by itself prove strategic feedback.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class StageHandoff:
    interval_slope: float
    timing_retention: float
    compensation_fraction: float
    regime: str


def _finite(name: str, value: float) -> float:
    x=float(value)
    if not isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def handoff_from_interval_slope(interval_slope: float) -> StageHandoff:
    """Translate an interval-on-entry slope into downstream timing retention.

    If T_next = T_entry + W, then on the same sample and with simple OLS:

        eta = beta(T_next ~ T_entry)
            = 1 + beta(W ~ T_entry).

    Define compensation fraction c = -beta(W ~ T_entry) = 1-eta.

    Regimes:
      eta = 1      : no buffering;
      0 < eta < 1  : partial buffering;
      eta = 0      : complete buffering of upstream timing variation;
      eta < 0      : overcompensation / sign reversal;
      eta > 1      : amplification.
    """

    b=_finite("interval_slope",interval_slope)
    eta=1.0+b
    comp=-b

    tol=1e-12
    if abs(eta-1.0)<=tol:
        regime="no_buffering"
    elif abs(eta)<=tol:
        regime="complete_buffering"
    elif 0.0<eta<1.0:
        regime="partial_buffering"
    elif eta<0.0:
        regime="overcompensation"
    else:
        regime="amplification"

    return StageHandoff(
        interval_slope=b,
        timing_retention=eta,
        compensation_fraction=comp,
        regime=regime,
    )


def downstream_timing_slope(interval_slope: float) -> float:
    """Exact simple-regression handoff identity."""
    return 1.0+_finite("interval_slope",interval_slope)


def interval_slope_from_retention(timing_retention: float) -> float:
    """Inverse handoff identity."""
    eta=_finite("timing_retention",timing_retention)
    return eta-1.0
