"""Prospective horse-racing mechanism-separation utilities for PAYOFF-B.

This module does not implement a betting strategy.  It evaluates whether a
fixed non-market probabilistic forecast retains incremental predictive value
over a contemporaneous pari-mutuel market forecast as race time approaches.

For each race, the market forecast is obtained by normalizing reciprocal
decimal odds within the active field.  A frozen form-model forecast f and a
time-varying market forecast m are combined through a logarithmic opinion pool

    h_i(w) proportional to f_i**w * m_i**(1-w),

with w fitted on training races by multinomial log loss.

The fitted w is a descriptive/prospective proxy for the remaining incremental
value of the frozen form forecast.  It is not asserted to be a structural
market-efficiency parameter or the PAYOFF exclusivity state e(t).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log
from typing import Mapping, Sequence


_EPS = 1e-15
_TOL = 1e-12


def _validate_distribution(
    probs: Mapping[str, float],
    *,
    name: str,
) -> dict[str, float]:
    if not probs:
        raise ValueError(f"{name} must contain at least one runner")
    out: dict[str, float] = {}
    for runner, value in probs.items():
        p = float(value)
        if not isfinite(p) or p <= 0.0:
            raise ValueError(f"{name} probabilities must be finite and positive")
        out[str(runner)] = p
    total = sum(out.values())
    if total <= 0.0:
        raise ValueError(f"{name} must have positive total mass")
    return {runner: p / total for runner, p in out.items()}


def market_probabilities_from_decimal_odds(
    odds: Mapping[str, float],
) -> dict[str, float]:
    """Normalize reciprocal decimal odds to a within-race probability vector."""

    if not odds:
        raise ValueError("odds must contain at least one runner")
    reciprocal: dict[str, float] = {}
    for runner, value in odds.items():
        o = float(value)
        if not isfinite(o) or o <= 1.0:
            raise ValueError("decimal odds must be finite and greater than one")
        reciprocal[str(runner)] = 1.0 / o
    total = sum(reciprocal.values())
    return {runner: value / total for runner, value in reciprocal.items()}


def logarithmic_opinion_pool(
    form_probabilities: Mapping[str, float],
    market_probabilities: Mapping[str, float],
    form_weight: float,
) -> dict[str, float]:
    """Combine two probability vectors through a normalized log pool."""

    w = float(form_weight)
    if not isfinite(w) or not 0.0 <= w <= 1.0:
        raise ValueError("form_weight must lie in [0, 1]")

    form = _validate_distribution(form_probabilities, name="form")
    market = _validate_distribution(market_probabilities, name="market")
    if set(form) != set(market):
        raise ValueError("form and market distributions must share runner ids")

    log_scores = {
        runner: w * log(max(form[runner], _EPS))
        + (1.0 - w) * log(max(market[runner], _EPS))
        for runner in form
    }
    max_log = max(log_scores.values())
    unnorm = {
        runner: exp(score - max_log)
        for runner, score in log_scores.items()
    }
    total = sum(unnorm.values())
    return {runner: value / total for runner, value in unnorm.items()}


@dataclass(frozen=True)
class RaceForecast:
    """One race with a frozen form forecast and one contemporaneous market."""

    race_id: str
    winner_id: str
    form_probabilities: Mapping[str, float]
    market_probabilities: Mapping[str, float]

    def validated(self) -> "RaceForecast":
        form = _validate_distribution(self.form_probabilities, name="form")
        market = _validate_distribution(self.market_probabilities, name="market")
        if set(form) != set(market):
            raise ValueError("form and market distributions must share runner ids")
        winner = str(self.winner_id)
        if winner not in form:
            raise ValueError("winner_id must be present in the runner set")
        return RaceForecast(
            race_id=str(self.race_id),
            winner_id=winner,
            form_probabilities=form,
            market_probabilities=market,
        )


@dataclass(frozen=True)
class TimeSliceEvaluation:
    """Held-out proper-score summary for one pre-race time slice."""

    time_slice: str
    fitted_form_weight: float
    training_log_loss: float
    test_market_log_loss: float
    test_form_log_loss: float
    test_hybrid_log_loss: float
    incremental_form_value_over_market: float
    test_races: int


def race_log_loss(
    probabilities: Mapping[str, float],
    winner_id: str,
) -> float:
    probs = _validate_distribution(probabilities, name="probabilities")
    winner = str(winner_id)
    if winner not in probs:
        raise ValueError("winner_id must be present in probabilities")
    return -log(max(probs[winner], _EPS))


def mean_log_loss(
    races: Sequence[RaceForecast],
    *,
    source: str,
    form_weight: float | None = None,
) -> float:
    """Return mean multinomial log loss across races.

    source must be one of "form", "market", or "hybrid".
    """

    if not races:
        raise ValueError("at least one race is required")
    if source not in {"form", "market", "hybrid"}:
        raise ValueError("source must be form, market, or hybrid")
    if source == "hybrid" and form_weight is None:
        raise ValueError("hybrid source requires form_weight")

    losses: list[float] = []
    for raw in races:
        race = raw.validated()
        if source == "form":
            probs = race.form_probabilities
        elif source == "market":
            probs = race.market_probabilities
        else:
            probs = logarithmic_opinion_pool(
                race.form_probabilities,
                race.market_probabilities,
                float(form_weight),
            )
        losses.append(race_log_loss(probs, race.winner_id))
    return sum(losses) / len(losses)


def fit_form_weight(
    training_races: Sequence[RaceForecast],
    *,
    grid_points: int = 101,
) -> tuple[float, float]:
    """Fit log-pool form weight on training races only.

    A deterministic equally spaced grid on [0, 1] is used.  If multiple weights
    are tied within numerical tolerance, the smaller weight is chosen.  This is
    conservative about claiming incremental form-model value.
    """

    if grid_points < 2:
        raise ValueError("grid_points must be at least two")
    if not training_races:
        raise ValueError("at least one training race is required")

    best_w = 0.0
    best_loss = float("inf")
    for i in range(grid_points):
        w = i / (grid_points - 1)
        loss = mean_log_loss(
            training_races,
            source="hybrid",
            form_weight=w,
        )
        if loss < best_loss - _TOL:
            best_w = w
            best_loss = loss
    return best_w, best_loss


def evaluate_time_slice(
    time_slice: str,
    training_races: Sequence[RaceForecast],
    test_races: Sequence[RaceForecast],
    *,
    grid_points: int = 101,
) -> TimeSliceEvaluation:
    """Fit w on training races and evaluate market/form/hybrid on held-out races."""

    if not test_races:
        raise ValueError("at least one test race is required")
    weight, training_loss = fit_form_weight(
        training_races,
        grid_points=grid_points,
    )
    market_loss = mean_log_loss(test_races, source="market")
    form_loss = mean_log_loss(test_races, source="form")
    hybrid_loss = mean_log_loss(
        test_races,
        source="hybrid",
        form_weight=weight,
    )
    return TimeSliceEvaluation(
        time_slice=str(time_slice),
        fitted_form_weight=weight,
        training_log_loss=training_loss,
        test_market_log_loss=market_loss,
        test_form_log_loss=form_loss,
        test_hybrid_log_loss=hybrid_loss,
        incremental_form_value_over_market=market_loss - hybrid_loss,
        test_races=len(test_races),
    )
