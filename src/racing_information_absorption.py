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



@dataclass(frozen=True)
class PairedTestBootstrap:
    """Paired race-level bootstrap for first-to-last held-out contrasts."""

    replicates: int
    seed: int
    races: int
    market_improvement_mean: float
    market_improvement_ci_low: float
    market_improvement_ci_high: float
    market_improvement_positive_fraction: float
    incremental_value_decline_mean: float
    incremental_value_decline_ci_low: float
    incremental_value_decline_ci_high: float
    incremental_value_decline_positive_fraction: float


def _percentile(sorted_values: Sequence[float], probability: float) -> float:
    if not sorted_values:
        raise ValueError("percentile requires at least one value")
    if probability <= 0.0:
        return float(sorted_values[0])
    if probability >= 1.0:
        return float(sorted_values[-1])
    position = probability * (len(sorted_values) - 1)
    lo = int(position)
    hi = min(lo + 1, len(sorted_values) - 1)
    weight = position - lo
    return float(
        sorted_values[lo] * (1.0 - weight)
        + sorted_values[hi] * weight
    )


def paired_test_bootstrap(
    first_test_races: Sequence[RaceForecast],
    last_test_races: Sequence[RaceForecast],
    *,
    first_form_weight: float,
    last_form_weight: float,
    replicates: int = 2000,
    seed: int = 20261007,
) -> PairedTestBootstrap:
    """Bootstrap P1/P3 by race, preserving within-race time pairing.

    The train-fitted form weights are held fixed.  This therefore quantifies
    held-out test-race uncertainty in:

    P1:
        L_market(first) - L_market(last)

    P3:
        [L_market(first)-L_hybrid(first)]
        -
        [L_market(last)-L_hybrid(last)].

    It does not claim to quantify uncertainty in the training-estimated
    weights themselves.
    """

    from random import Random

    n_rep = int(replicates)
    if n_rep < 1:
        raise ValueError("replicates must be positive")

    first = {str(r.race_id): r.validated() for r in first_test_races}
    last = {str(r.race_id): r.validated() for r in last_test_races}
    if set(first) != set(last):
        raise ValueError("first and last test slices must contain identical race ids")
    race_ids = sorted(first)
    if not race_ids:
        raise ValueError("at least one paired test race is required")

    market_contrib: list[float] = []
    value_contrib: list[float] = []

    for race_id in race_ids:
        one = first[race_id]
        two = last[race_id]

        market_first = race_log_loss(
            one.market_probabilities,
            one.winner_id,
        )
        market_last = race_log_loss(
            two.market_probabilities,
            two.winner_id,
        )

        hybrid_first = logarithmic_opinion_pool(
            one.form_probabilities,
            one.market_probabilities,
            first_form_weight,
        )
        hybrid_last = logarithmic_opinion_pool(
            two.form_probabilities,
            two.market_probabilities,
            last_form_weight,
        )
        hybrid_first_loss = race_log_loss(hybrid_first, one.winner_id)
        hybrid_last_loss = race_log_loss(hybrid_last, two.winner_id)

        market_contrib.append(market_first - market_last)
        value_contrib.append(
            (market_first - hybrid_first_loss)
            - (market_last - hybrid_last_loss)
        )

    market_mean = sum(market_contrib) / len(market_contrib)
    value_mean = sum(value_contrib) / len(value_contrib)

    rng = Random(int(seed))
    market_draws: list[float] = []
    value_draws: list[float] = []
    n = len(race_ids)
    for _ in range(n_rep):
        indexes = [rng.randrange(n) for _ in range(n)]
        market_draws.append(
            sum(market_contrib[i] for i in indexes) / n
        )
        value_draws.append(
            sum(value_contrib[i] for i in indexes) / n
        )

    market_draws.sort()
    value_draws.sort()
    return PairedTestBootstrap(
        replicates=n_rep,
        seed=int(seed),
        races=n,
        market_improvement_mean=market_mean,
        market_improvement_ci_low=_percentile(market_draws, 0.025),
        market_improvement_ci_high=_percentile(market_draws, 0.975),
        market_improvement_positive_fraction=(
            sum(value > 0.0 for value in market_draws) / n_rep
        ),
        incremental_value_decline_mean=value_mean,
        incremental_value_decline_ci_low=_percentile(value_draws, 0.025),
        incremental_value_decline_ci_high=_percentile(value_draws, 0.975),
        incremental_value_decline_positive_fraction=(
            sum(value > 0.0 for value in value_draws) / n_rep
        ),
    )
