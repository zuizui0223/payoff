"""End-to-end retrospective PAYOFF-B racing analysis on normalized JV-Link tables.

This module composes the already frozen source, timing, split, calibration and
proper-score components.  It deliberately reports predictive information
absorption only; it does not construct or evaluate a betting strategy.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Iterable, Mapping, Sequence

from src.racing_chronological_split import chronological_date_split
from src.racing_information_absorption import (
    RaceForecast,
    evaluate_time_slice,
    market_probabilities_from_decimal_odds,
)
from src.racing_jvlink_contract import validate_normalized_handoff
from src.racing_public_score_calibration import (
    PublicScoreRace,
    fit_public_score_scale,
    standardized_score_probabilities,
)
from src.racing_time_slices import OddsSnapshot, select_primary_time_slices


@dataclass(frozen=True)
class RacingPrimaryAnalysis:
    source_audit: dict[str, int]
    split: dict[str, object]
    calibration: dict[str, float | int | str]
    exclusions: dict[str, int]
    time_slices: tuple[dict[str, float | int | str], ...]
    primary_contrasts: dict[str, float | bool]


def _as_rows(values: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    return [dict(row) for row in values]


def analyze_normalized_handoff(
    races: Iterable[Mapping[str, object]],
    results: Iterable[Mapping[str, object]],
    tm: Iterable[Mapping[str, object]],
    odds: Iterable[Mapping[str, object]],
    *,
    train_fraction: float = 0.70,
    targets_minutes: Sequence[float] = (30, 15, 10, 5),
    max_staleness_minutes: float = 10.0,
    score_max_scale: float = 5.0,
    score_grid_points: int = 501,
    pool_grid_points: int = 101,
) -> RacingPrimaryAnalysis:
    """Run the frozen retrospective category-7 mechanism-separation analysis."""

    race_rows = _as_rows(races)
    result_rows = _as_rows(results)
    tm_rows = _as_rows(tm)
    odds_rows = _as_rows(odds)

    audit = validate_normalized_handoff(
        race_rows,
        result_rows,
        tm_rows,
        odds_rows,
    )

    race_meta: dict[str, tuple[object, datetime]] = {}
    race_dates = []
    for row in race_rows:
        race_id = str(row["race_id"])
        race_day = datetime.fromisoformat(str(row["post_time"])).date()
        post = datetime.fromisoformat(str(row["post_time"]))
        race_meta[race_id] = (race_day, post)
        race_dates.append(race_day)

    split = chronological_date_split(
        race_dates,
        train_fraction=train_fraction,
    )

    valid_starters: dict[str, set[str]] = defaultdict(set)
    winner_by_race: dict[str, str] = {}
    for row in result_rows:
        race_id = str(row["race_id"])
        horse_id = str(row["horse_id"])
        if int(str(row["valid_starter"])) == 1:
            valid_starters[race_id].add(horse_id)
        if int(str(row["winner"])) == 1:
            winner_by_race[race_id] = horse_id

    scores_by_race: dict[str, dict[str, float]] = defaultdict(dict)
    for row in tm_rows:
        race_id = str(row["race_id"])
        horse_id = str(row["horse_id"])
        scores_by_race[race_id][horse_id] = float(row["tm_score"])

    odds_by_race_time: dict[str, dict[datetime, dict[str, float]]] = defaultdict(
        lambda: defaultdict(dict)
    )
    for row in odds_rows:
        race_id = str(row["race_id"])
        horse_id = str(row["horse_id"])
        when = datetime.fromisoformat(str(row["snapshot_time"]))
        odds_by_race_time[race_id][when][horse_id] = float(row["decimal_odds"])

    exclusions = {
        "tm_runner_set_mismatch": 0,
        "incomplete_time_panel": 0,
        "selected_snapshot_runner_set_mismatch": 0,
    }
    selected_by_race: dict[str, dict[str, object]] = {}

    for race_id, (race_day, post) in race_meta.items():
        valid = valid_starters[race_id]
        if set(scores_by_race.get(race_id, {})) != valid:
            exclusions["tm_runner_set_mismatch"] += 1
            continue

        snapshots = [
            OddsSnapshot(observed_at=when, decimal_odds=runner_odds)
            for when, runner_odds in odds_by_race_time.get(race_id, {}).items()
        ]
        if not snapshots:
            exclusions["incomplete_time_panel"] += 1
            continue

        selected = select_primary_time_slices(
            post_time=post,
            snapshots=snapshots,
            targets_minutes=targets_minutes,
            max_staleness_minutes=max_staleness_minutes,
        )
        if selected is None:
            exclusions["incomplete_time_panel"] += 1
            continue

        if any(set(s.decimal_odds) != valid for s in selected.values()):
            exclusions["selected_snapshot_runner_set_mismatch"] += 1
            continue

        selected_by_race[race_id] = selected

    eligible = sorted(selected_by_race)
    train_race_ids = [
        race_id
        for race_id in eligible
        if split.assignment[race_meta[race_id][0]] == "train"
    ]
    test_race_ids = [
        race_id
        for race_id in eligible
        if split.assignment[race_meta[race_id][0]] == "test"
    ]
    if not train_race_ids or not test_race_ids:
        raise ValueError(
            "eligible races must leave at least one training and one test race"
        )

    training_scores = [
        PublicScoreRace(
            race_id=race_id,
            winner_id=winner_by_race[race_id],
            scores=scores_by_race[race_id],
        )
        for race_id in train_race_ids
    ]
    calibration = fit_public_score_scale(
        training_scores,
        max_scale=score_max_scale,
        grid_points=score_grid_points,
    )

    form_by_race = {
        race_id: standardized_score_probabilities(
            scores_by_race[race_id],
            scale=calibration.scale,
        )
        for race_id in eligible
    }

    labels = [f"T-{float(m):g}" for m in targets_minutes] + ["LAST"]
    rows_by_time_split: dict[
        str, dict[str, list[RaceForecast]]
    ] = {
        label: {"train": [], "test": []}
        for label in labels
    }

    for race_id in eligible:
        split_name = split.assignment[race_meta[race_id][0]]
        winner = winner_by_race[race_id]
        form = form_by_race[race_id]
        for label in labels:
            selected = selected_by_race[race_id][label]
            market = market_probabilities_from_decimal_odds(
                selected.decimal_odds
            )
            rows_by_time_split[label][split_name].append(
                RaceForecast(
                    race_id=race_id,
                    winner_id=winner,
                    form_probabilities=form,
                    market_probabilities=market,
                )
            )

    evaluations = []
    for label in labels:
        ev = evaluate_time_slice(
            label,
            rows_by_time_split[label]["train"],
            rows_by_time_split[label]["test"],
            grid_points=pool_grid_points,
        )
        evaluations.append(asdict(ev))

    by_label = {str(row["time_slice"]): row for row in evaluations}
    first = labels[0]
    last = "LAST"
    contrasts = {
        "market_log_loss_improvement_first_to_last": (
            float(by_label[first]["test_market_log_loss"])
            - float(by_label[last]["test_market_log_loss"])
        ),
        "form_weight_decline_first_to_last": (
            float(by_label[first]["fitted_form_weight"])
            - float(by_label[last]["fitted_form_weight"])
        ),
        "incremental_form_value_decline_first_to_last": (
            float(by_label[first]["incremental_form_value_over_market"])
            - float(by_label[last]["incremental_form_value_over_market"])
        ),
    }
    contrasts.update(
        {
            "P1_market_improves": (
                contrasts["market_log_loss_improvement_first_to_last"] > 0.0
            ),
            "P2_form_weight_declines": (
                contrasts["form_weight_decline_first_to_last"] > 0.0
            ),
            "P3_incremental_form_value_declines": (
                contrasts["incremental_form_value_decline_first_to_last"] > 0.0
            ),
        }
    )

    return RacingPrimaryAnalysis(
        source_audit=asdict(audit),
        split={
            "train_fraction": split.train_fraction,
            "train_dates": [d.isoformat() for d in split.train_dates],
            "test_dates": [d.isoformat() for d in split.test_dates],
            "eligible_train_races": len(train_race_ids),
            "eligible_test_races": len(test_race_ids),
        },
        calibration={
            "tm_score_scale": calibration.scale,
            "training_log_loss": calibration.training_log_loss,
            "training_races": calibration.races,
            "tm_data_category": 7,
        },
        exclusions=exclusions,
        time_slices=tuple(evaluations),
        primary_contrasts=contrasts,
    )
