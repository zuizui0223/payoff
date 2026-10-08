"""Post-outcome kinematic identity for migration phase-transfer slopes.

For a transition between sites j and k, define:
    e_j = A_j - S_j
    e_k = A_k - S_k
    A_k = A_j + stopover + transit.

Then exactly:
    e_k = e_j + stopover + transit + (S_j - S_k)

and therefore the OLS slope of e_k on e_j with an intercept is:
    lambda = 1 + slope(stopover|e_j) + slope(transit|e_j)
               + slope(S_j-S_k|e_j).

The components are covariance decompositions, NOT causal effects.
In particular, negative stopover slope can arise from a fixed departure date
without cue-driven reactive correction.

The present analysis is a labelled post-outcome DIAGNOSTIC. It never changes
the frozen V7R primary outcome, transition selection, or hypothesis.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence

_TOL = 1e-9


@dataclass(frozen=True)
class PhaseTransition:
    origin_arrival_doy: float
    destination_arrival_doy: float
    origin_phase: float
    destination_phase: float
    origin_stopover_days: float
    transit_days: float


@dataclass(frozen=True)
class PhaseIdentity:
    n: int
    lambda_observed: float
    b_stopover: float
    b_transit: float
    b_interregional_season: float
    lambda_reconstructed: float
    maximum_row_identity_error: float
    slope_identity_error: float


def _slope(predictor: Sequence[float], response: Sequence[float]) -> float:
    n = len(predictor)
    mx = sum(predictor) / n
    my = sum(response) / n
    ssx = sum((x-mx)**2 for x in predictor)
    if ssx <= 1e-12:
        raise ValueError("origin phase lacks variation; slope is unidentified")
    return sum((x-mx)*(y-my) for x,y in zip(predictor,response)) / ssx


def decompose_phase_transfer(rows: Sequence[PhaseTransition]) -> PhaseIdentity:
    """Verify per-row identities, then exactly decompose an OLS phase slope."""

    data = list(rows)
    if len(data) < 2:
        raise ValueError("at least two transition observations required")

    for row in data:
        if not all(isfinite(float(value)) for value in (
            row.origin_arrival_doy, row.destination_arrival_doy,
            row.origin_phase, row.destination_phase,
            row.origin_stopover_days, row.transit_days,
        )):
            raise ValueError("all phase-transition values must be finite")

    phase = [float(r.origin_phase) for r in data]
    next_phase = [float(r.destination_phase) for r in data]
    stop = [float(r.origin_stopover_days) for r in data]
    transit = [float(r.transit_days) for r in data]
    season = [
        (float(r.origin_arrival_doy)-float(r.origin_phase))
        - (float(r.destination_arrival_doy)-float(r.destination_phase))
        for r in data
    ]

    max_error = max(
        abs(
            float(r.destination_arrival_doy)
            - float(r.origin_arrival_doy)
            - float(r.origin_stopover_days)
            - float(r.transit_days)
        )
        for r in data
    )
    if max_error > _TOL:
        raise ValueError("movement chronology does not match stopover + transit")

    max_phase_error = max(
        abs(next_phase[i] - phase[i] - stop[i] - transit[i] - season[i])
        for i in range(len(data))
    )
    max_error=max(max_error,max_phase_error)
    if max_error > _TOL:
        raise ValueError("phase identity fails at individual-transition level")

    lam = _slope(phase,next_phase)
    bs = _slope(phase,stop)
    bt = _slope(phase,transit)
    bc = _slope(phase,season)
    predicted = 1.0+bs+bt+bc
    error = abs(lam-predicted)
    if error > _TOL:
        raise ValueError("phase-transfer slope identity failed")

    return PhaseIdentity(
        n=len(data),
        lambda_observed=lam,
        b_stopover=bs,
        b_transit=bt,
        b_interregional_season=bc,
        lambda_reconstructed=predicted,
        maximum_row_identity_error=max_error,
        slope_identity_error=error,
    )
