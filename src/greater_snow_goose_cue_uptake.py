"""Fail-closed helpers for the prospective greater-snow-goose GPS cue-use lane."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


FROZEN_Q_GRID = (
    0.500, 0.525, 0.550, 0.575, 0.600,
    0.625, 0.650, 0.675, 0.700,
)


@dataclass(frozen=True)
class CueUptakeEstimability:
    estimable: bool
    reasons: tuple[str, ...]
    individuals: int
    years: int
    contexts: int
    departure_events: int
    predictive_connectivity_sd: float


def evaluate_estimability(
    *,
    individuals: int,
    years: int,
    contexts: int,
    departure_events: int,
    predictive_connectivity_sd: float,
) -> CueUptakeEstimability:
    """Apply the preregistered estimability gate exactly."""

    sd = float(predictive_connectivity_sd)
    if not isfinite(sd) or sd < 0.0:
        raise ValueError("predictive_connectivity_sd must be finite and non-negative")

    reasons = []
    if int(individuals) < 30:
        reasons.append("FEWER_THAN_30_INDIVIDUALS")
    if int(years) < 4:
        reasons.append("FEWER_THAN_4_YEARS")
    if int(contexts) < 3:
        reasons.append("FEWER_THAN_3_CONTEXTS")
    if int(departure_events) < 100:
        reasons.append("FEWER_THAN_100_DEPARTURES")
    if sd < 0.03:
        reasons.append("PREDICTIVE_CONNECTIVITY_SD_BELOW_0_03")

    return CueUptakeEstimability(
        estimable=not reasons,
        reasons=tuple(reasons),
        individuals=int(individuals),
        years=int(years),
        contexts=int(contexts),
        departure_events=int(departure_events),
        predictive_connectivity_sd=sd,
    )


def gaussian_binary_q(rho: float) -> float:
    """Secondary Gaussian sign-agreement bridge q=0.5+asin(rho)/pi."""

    from math import asin, pi

    r = float(rho)
    if not isfinite(r) or not -1.0 <= r <= 1.0:
        raise ValueError("rho must lie in [-1, 1]")
    return 0.5 + asin(r) / pi


def threshold_active(q: float, threshold: float) -> bool:
    """Frozen secondary threshold indicator."""

    value = float(q)
    cut = float(threshold)
    if not all(isfinite(x) for x in (value, cut)):
        raise ValueError("q and threshold must be finite")
    if cut not in FROZEN_Q_GRID:
        raise ValueError("threshold is not on the frozen q grid")
    return value >= cut


def preoutcome_training_valid(
    *,
    focal_year: int,
    training_end_year: int,
    training_years: int,
) -> bool:
    """Historical predictive-connectivity data must end before focal year."""

    return int(training_end_year) <= int(focal_year) - 1 and int(training_years) >= 15
