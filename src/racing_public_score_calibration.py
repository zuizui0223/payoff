"""Calibration of a fixed public racing score into within-race probabilities.

The intended first PAYOFF-B racing use is the JRA-VAN *previous-day*
head-to-head data-mining score (TM record, data category 1).  The public score
is fixed before the within-day odds path evaluated by the mechanism-separation
test.

Scores are standardized within race, then mapped through one global softmax
scale lambda:

    p_i(lambda) proportional to exp(lambda * z_i).

Lambda is fitted only on training races by multinomial log loss and then frozen.
This produces a probabilistic fixed-information forecast without using
contemporaneous odds.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log, sqrt
from typing import Mapping, Sequence


_EPS = 1e-15
_TOL = 1e-12


@dataclass(frozen=True)
class PublicScoreRace:
    race_id: str
    winner_id: str
    scores: Mapping[str, float]


@dataclass(frozen=True)
class PublicScoreCalibration:
    scale: float
    training_log_loss: float
    races: int


def standardized_score_probabilities(
    scores: Mapping[str, float],
    *,
    scale: float,
) -> dict[str, float]:
    """Convert higher-is-better scores into a within-race probability vector."""

    lam = float(scale)
    if not isfinite(lam) or lam < 0.0:
        raise ValueError("scale must be finite and non-negative")
    if not scores:
        raise ValueError("scores must contain at least one runner")

    values: dict[str, float] = {}
    for runner, raw in scores.items():
        x = float(raw)
        if not isfinite(x):
            raise ValueError("scores must be finite")
        values[str(runner)] = x

    n = len(values)
    mean = sum(values.values()) / n
    variance = sum((x - mean) ** 2 for x in values.values()) / n
    sd = sqrt(variance)

    if sd <= _TOL or lam <= _TOL:
        uniform = 1.0 / n
        return {runner: uniform for runner in values}

    logits = {
        runner: lam * (x - mean) / sd
        for runner, x in values.items()
    }
    max_logit = max(logits.values())
    unnorm = {
        runner: exp(v - max_logit)
        for runner, v in logits.items()
    }
    total = sum(unnorm.values())
    return {runner: value / total for runner, value in unnorm.items()}


def public_score_log_loss(
    races: Sequence[PublicScoreRace],
    *,
    scale: float,
) -> float:
    if not races:
        raise ValueError("at least one race is required")
    losses: list[float] = []
    for race in races:
        probs = standardized_score_probabilities(race.scores, scale=scale)
        winner = str(race.winner_id)
        if winner not in probs:
            raise ValueError("winner_id must be present in scores")
        losses.append(-log(max(probs[winner], _EPS)))
    return sum(losses) / len(losses)


def fit_public_score_scale(
    races: Sequence[PublicScoreRace],
    *,
    max_scale: float = 5.0,
    grid_points: int = 501,
) -> PublicScoreCalibration:
    """Fit a global softmax scale on training races only.

    The grid includes zero and max_scale.  Ties are resolved toward the smaller
    scale, avoiding unnecessary overconfidence.
    """

    if not races:
        raise ValueError("at least one race is required")
    upper = float(max_scale)
    if not isfinite(upper) or upper <= 0.0:
        raise ValueError("max_scale must be finite and positive")
    if grid_points < 2:
        raise ValueError("grid_points must be at least two")

    best_scale = 0.0
    best_loss = float("inf")
    for i in range(grid_points):
        scale = upper * i / (grid_points - 1)
        loss = public_score_log_loss(races, scale=scale)
        if loss < best_loss - _TOL:
            best_scale = scale
            best_loss = loss

    return PublicScoreCalibration(
        scale=best_scale,
        training_log_loss=best_loss,
        races=len(races),
    )
