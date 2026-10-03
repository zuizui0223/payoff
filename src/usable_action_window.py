"""Exact overlap window for readiness opening and opportunity expiry."""

from __future__ import annotations
from dataclasses import dataclass
from math import exp, log, isfinite

@dataclass(frozen=True)
class UsableWindowPeak:
    readiness_rate: float
    expiry_rate: float
    peak_time: float
    readiness_at_peak: float
    opportunity_at_peak: float
    usable_gate_at_peak: float

@dataclass(frozen=True)
class MultiPrerequisitePeak:
    opening_rate: float
    expiry_rate: float
    prerequisite_count: int
    peak_time: float
    opening_level_at_peak: float
    objective_at_peak: float

def _positive(name: str, value: float) -> float:
    x=float(value)
    if not isfinite(x) or x <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return x

def readiness_opening(time: float, *, rate: float) -> float:
    t=max(0.0,float(time))
    a=_positive("rate",rate)
    return 1.0-exp(-a*t)

def opportunity_survival(time: float, *, rate: float) -> float:
    t=max(0.0,float(time))
    b=_positive("rate",rate)
    return exp(-b*t)

def usable_action_gate(time: float, *, readiness_rate: float, expiry_rate: float) -> float:
    return readiness_opening(time,rate=readiness_rate)*opportunity_survival(
        time,rate=expiry_rate
    )

def usable_window_peak(*, readiness_rate: float, expiry_rate: float) -> UsableWindowPeak:
    """Peak of U(t)=(1-exp(-gamma t))*exp(-beta t).

    t* = log(1+gamma/beta)/gamma.
    """
    gamma=_positive("readiness_rate",readiness_rate)
    beta=_positive("expiry_rate",expiry_rate)
    t=log(1.0+gamma/beta)/gamma
    G=readiness_opening(t,rate=gamma)
    O=opportunity_survival(t,rate=beta)
    return UsableWindowPeak(
        readiness_rate=gamma,
        expiry_rate=beta,
        peak_time=t,
        readiness_at_peak=G,
        opportunity_at_peak=O,
        usable_gate_at_peak=G*O,
    )

def multi_prerequisite_value(
    time: float,
    *,
    opening_rate: float,
    expiry_rate: float,
    prerequisite_count: int,
) -> float:
    """Witness value (1-exp(-alpha t))^n exp(-beta t)."""
    alpha=_positive("opening_rate",opening_rate)
    beta=_positive("expiry_rate",expiry_rate)
    n=int(prerequisite_count)
    if n < 1:
        raise ValueError("prerequisite_count must be >=1")
    t=max(0.0,float(time))
    return (1.0-exp(-alpha*t))**n * exp(-beta*t)

def multi_prerequisite_peak(
    *,
    opening_rate: float,
    expiry_rate: float,
    prerequisite_count: int,
) -> MultiPrerequisitePeak:
    """Exact peak for n equal-rate opening prerequisites plus expiry.

    If

        F_n(t)=(1-exp(-alpha t))^n exp(-beta t),

    then

        t* = log(1+n alpha/beta)/alpha,

    and the common opening level at the optimum is

        n alpha/(beta+n alpha).

    n=1 is the readiness-opportunity window.
    n=2 can represent a witness in which readiness and normalized information
    surplus mature at the same rate before opportunity expires.
    """
    alpha=_positive("opening_rate",opening_rate)
    beta=_positive("expiry_rate",expiry_rate)
    n=int(prerequisite_count)
    if n < 1:
        raise ValueError("prerequisite_count must be >=1")
    t=log(1.0+n*alpha/beta)/alpha
    q=1.0-exp(-alpha*t)
    val=multi_prerequisite_value(
        t,opening_rate=alpha,expiry_rate=beta,prerequisite_count=n
    )
    return MultiPrerequisitePeak(
        opening_rate=alpha,
        expiry_rate=beta,
        prerequisite_count=n,
        peak_time=t,
        opening_level_at_peak=q,
        objective_at_peak=val,
    )
