#!/usr/bin/env python3
"""Evaluate time-sliced racing information absorption for PAYOFF-B.

Input CSV is long format with one row per race x horse x time slice.

Required columns:
    split            train or test
    race_id
    horse_id
    time_slice
    decimal_odds
    form_probability
    winner           1 for winner, 0 otherwise

The same frozen form_probability for a horse/race should be repeated across
time slices.  The script does not enforce temporal feature provenance; that is
a data-generation responsibility covered by the prospective protocol.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from src.racing_information_absorption import (
    RaceForecast,
    evaluate_time_slice,
    market_probabilities_from_decimal_odds,
)


REQUIRED = {
    "split",
    "race_id",
    "horse_id",
    "time_slice",
    "decimal_odds",
    "form_probability",
    "winner",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("csv_path")
    p.add_argument("--output", required=True)
    p.add_argument("--grid-points", type=int, default=101)
    return p.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing required columns: {sorted(missing)}")
        rows = [dict(row) for row in reader]
    if not rows:
        raise ValueError("input CSV has no data rows")
    return rows


def build_forecasts(
    rows: list[dict[str, str]],
) -> dict[str, dict[str, list[RaceForecast]]]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        split = row["split"].strip().lower()
        if split not in {"train", "test"}:
            raise ValueError("split must be train or test")
        grouped[(split, row["time_slice"], row["race_id"])].append(row)

    out: dict[str, dict[str, list[RaceForecast]]] = {
        "train": defaultdict(list),
        "test": defaultdict(list),
    }

    for (split, time_slice, race_id), race_rows in grouped.items():
        odds: dict[str, float] = {}
        form: dict[str, float] = {}
        winners: list[str] = []
        for row in race_rows:
            horse = str(row["horse_id"])
            if horse in odds:
                raise ValueError(
                    f"duplicate horse row for split={split}, time={time_slice}, "
                    f"race={race_id}, horse={horse}"
                )
            odds[horse] = float(row["decimal_odds"])
            form[horse] = float(row["form_probability"])
            winner_flag = int(row["winner"])
            if winner_flag not in {0, 1}:
                raise ValueError("winner must be 0 or 1")
            if winner_flag == 1:
                winners.append(horse)

        if len(winners) != 1:
            raise ValueError(
                f"race {race_id} at {time_slice} must have exactly one winner"
            )
        market = market_probabilities_from_decimal_odds(odds)
        out[split][time_slice].append(
            RaceForecast(
                race_id=race_id,
                winner_id=winners[0],
                form_probabilities=form,
                market_probabilities=market,
            )
        )

    return {
        split: dict(by_time)
        for split, by_time in out.items()
    }


def main() -> int:
    args = parse_args()
    rows = load_rows(Path(args.csv_path))
    forecasts = build_forecasts(rows)

    train_times = set(forecasts["train"])
    test_times = set(forecasts["test"])
    common = sorted(train_times & test_times)
    if not common:
        raise ValueError("no time slices are shared by train and test data")

    results = []
    for time_slice in common:
        ev = evaluate_time_slice(
            time_slice,
            forecasts["train"][time_slice],
            forecasts["test"][time_slice],
            grid_points=args.grid_points,
        )
        results.append(
            {
                "time_slice": ev.time_slice,
                "fitted_form_weight": ev.fitted_form_weight,
                "training_log_loss": ev.training_log_loss,
                "test_market_log_loss": ev.test_market_log_loss,
                "test_form_log_loss": ev.test_form_log_loss,
                "test_hybrid_log_loss": ev.test_hybrid_log_loss,
                "incremental_form_value_over_market": (
                    ev.incremental_form_value_over_market
                ),
                "test_races": ev.test_races,
            }
        )

    payload = {
        "schema": "payoff_b_racing_information_absorption_v1",
        "grid_points": args.grid_points,
        "time_slices": results,
        "notes": [
            "Proper-score analysis only; no betting strategy is evaluated.",
            "Weights are trained on train races and reported on held-out test races.",
            "fitted_form_weight is a proxy, not a structural market-efficiency parameter.",
        ],
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
