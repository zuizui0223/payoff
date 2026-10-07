#!/usr/bin/env python3
"""Calibrate fixed public racing TM scores into win probabilities.

Expected long-format CSV columns:
    split          train or test
    race_id
    horse_id
    tm_score       fixed public TM score; higher is better
    winner         1 for winner, 0 otherwise

The softmax scale is fitted on training races only.  Test winner labels are
carried through to facilitate later scoring but are never used to fit the
calibration scale.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from src.racing_public_score_calibration import (
    PublicScoreRace,
    fit_public_score_scale,
    standardized_score_probabilities,
)


REQUIRED = {"split", "race_id", "horse_id", "tm_score", "winner"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("csv_path")
    p.add_argument("--output-csv", required=True)
    p.add_argument("--receipt-json", required=True)
    p.add_argument("--max-scale", type=float, default=5.0)
    p.add_argument("--grid-points", type=int, default=501)
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


def group_races(rows: list[dict[str, str]]):
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    split_races = {"train": set(), "test": set()}
    for row in rows:
        split = row["split"].strip().lower()
        if split not in {"train", "test"}:
            raise ValueError("split must be train or test")
        race = str(row["race_id"])
        grouped[(split, race)].append(row)
        split_races[split].add(race)

    overlap = split_races["train"] & split_races["test"]
    if overlap:
        raise ValueError("train/test race_id overlap is not allowed")

    races: dict[str, list[PublicScoreRace]] = {"train": [], "test": []}
    raw_by_key: dict[tuple[str, str], dict[str, float]] = {}

    for (split, race), race_rows in grouped.items():
        scores: dict[str, float] = {}
        winners: list[str] = []
        for row in race_rows:
            horse = str(row["horse_id"])
            if horse in scores:
                raise ValueError(f"duplicate horse row for race {race}: {horse}")
            scores[horse] = float(row["tm_score"])
            flag = int(row["winner"])
            if flag not in {0, 1}:
                raise ValueError("winner must be 0 or 1")
            if flag == 1:
                winners.append(horse)
        if len(winners) != 1:
            raise ValueError(f"race {race} must have exactly one winner")
        races[split].append(
            PublicScoreRace(
                race_id=race,
                winner_id=winners[0],
                scores=scores,
            )
        )
        raw_by_key[(split, race)] = scores

    if not races["train"] or not races["test"]:
        raise ValueError("both train and test races are required")
    return races, raw_by_key


def main() -> int:
    args = parse_args()
    rows = load_rows(Path(args.csv_path))
    races, raw_by_key = group_races(rows)

    calibration = fit_public_score_scale(
        races["train"],
        max_scale=args.max_scale,
        grid_points=args.grid_points,
    )

    probs_by_key: dict[tuple[str, str], dict[str, float]] = {}
    for key, scores in raw_by_key.items():
        probs_by_key[key] = standardized_score_probabilities(
            scores,
            scale=calibration.scale,
        )

    output = Path(args.output_csv)
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "split",
        "race_id",
        "horse_id",
        "tm_score",
        "form_probability",
        "winner",
    ]
    with output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            split = row["split"].strip().lower()
            race = str(row["race_id"])
            horse = str(row["horse_id"])
            writer.writerow(
                {
                    "split": split,
                    "race_id": race,
                    "horse_id": horse,
                    "tm_score": row["tm_score"],
                    "form_probability": (
                        f"{probs_by_key[(split, race)][horse]:.17g}"
                    ),
                    "winner": row["winner"],
                }
            )

    receipt = {
        "schema": "payoff_b_racing_public_score_calibration_v1",
        "scale": calibration.scale,
        "training_log_loss": calibration.training_log_loss,
        "training_races": calibration.races,
        "test_races": len(races["test"]),
        "max_scale": args.max_scale,
        "grid_points": args.grid_points,
        "fit_scope": "train_only",
        "intended_source": (
            "retrospective primary: JRA-VAN TM category 7 accumulated score "
            "corresponding to final pre-race forecast"
        ),
        "prospective_extension": (
            "archive realtime TM category 1 previous-day score before overwrite"
        ),
    }
    receipt_path = Path(args.receipt_json)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
