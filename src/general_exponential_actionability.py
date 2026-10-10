"""Generalized exponential information-actionability timing, with exact boundary.

This module corrects a scope omission in the V4 integration manuscript.
The previously frozen canonical result
  t*=log(1+alpha/beta)/alpha
REMAINS valid for the deliberately specified q(0)=B/S case. It is NOT
general across different initial cue accuracy. No new theorem or field result
is claimed: this is elementary optimal timing calculus and an audit guard.

Assumptions: 0.5<=q_start<1 (invertible symmetric binary cue),
cue_gain>0, q_start+cue_gain<=1,
alpha,beta>0, value scale S>0, threshold B/S in [0.5,1],
retained actionability exp(-beta*t), zero direct waiting cost,
actor may opt out if information never becomes usable.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, expm1, isfinite, log, log1p


@dataclass(frozen=True)
class ExponentialTiming:
    status: str
    cue_start: float
    cue_limit: float
    cue_action_threshold: float
    threshold_crossing_time: float | None
    optimal_time: float | None
    optimal_cue_accuracy: float | None
    maximal_actionable_value: float


def _finite(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def gross_actionable_value(
    t: float, *,
    q_start: float, cue_gain: float, alpha: float,
    beta: float, scale: float, base_loss: float,
) -> float:
    """Actionable positive information value at t >= 0, with opt-out."""
    t = _finite("t", t)
    if t < 0:
        raise ValueError("time must be nonnegative")
    q = q_start - cue_gain * expm1(-alpha*t)
    return exp(-beta*t)*max(0.0, scale*q-base_loss)


def general_exponential_timing(
    *, q_start: float, cue_gain: float,
    alpha: float, beta: float,
    scale: float, base_loss: float,
) -> ExponentialTiming:
    """Exact max of exp(-beta*t)*max(0,S*q(t)-B) over t>=0.

    With q(t)=q_start+cue_gain*(1-exp(-alpha*t)), define
    H=S*cue_gain > 0, A=S*(q_start+cue_gain)-B.
    In the positive-value region:
       N'(t)=exp(-beta*t)[-beta*A+(alpha+beta)*H*exp(-alpha*t)].
    If A<=0, q(t) never becomes strictly profitable.
    If A>0, the candidate is:
       tcrit=[log(H/A)+log(1+alpha/beta)]/alpha,
    clipped to the feasible time interval [0,infinity).
    The old canonical t*=log(1+alpha/beta)/alpha follows only
    when q_start=B/S (then A=H).

    This is a one-shot deterministic expectation proxy, not an observed
    biological belief, instantaneous forecast or demographic fitness.
    """
    q0 = _finite("q_start", q_start)
    gain = _finite("cue_gain", cue_gain)
    a = _finite("alpha", alpha)
    b = _finite("beta", beta)
    s = _finite("scale", scale)
    base = _finite("base_loss", base_loss)
    if not (0.5 <= q0 < 1 and 0 < gain <= 1-q0 and
            a > 0 and b > 0 and s > 0 and 0.5*s <= base <= s):
        raise ValueError("invalid invertible binary cue reliability, rates or threshold")

    qmax = q0 + gain
    threshold = base/s
    h = s*gain
    asymptotic_information_value = s*qmax-base
    if asymptotic_information_value <= 0:
        return ExponentialTiming(
            status="NEVER_ACTIONABLE",
            cue_start=q0, cue_limit=qmax, cue_action_threshold=threshold,
            threshold_crossing_time=None,
            optimal_time=None, optimal_cue_accuracy=None,
            maximal_actionable_value=0.0,
        )
    A = asymptotic_information_value
    crossing = 0.0 if q0 >= threshold else log(h/A)/a
    candidate = (log(h/A) + log1p(a/b)) / a
    tstar = max(0.0, candidate)
    opt_q = q0 - gain*expm1(-a*tstar)
    maximum = exp(-b*tstar)*max(0.0,s*opt_q-base)
    return ExponentialTiming(
        status="IMMEDIATE_USE" if tstar==0 else "INTERIOR_MAXIMUM",
        cue_start=q0, cue_limit=qmax, cue_action_threshold=threshold,
        threshold_crossing_time=crossing,
        optimal_time=tstar, optimal_cue_accuracy=opt_q,
        maximal_actionable_value=maximum,
    )
