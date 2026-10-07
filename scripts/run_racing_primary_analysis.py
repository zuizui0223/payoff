#!/usr/bin/env python3
"""Run the frozen retrospective PAYOFF-B racing analysis from four CSV tables."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

from src.racing_primary_analysis import analyze_normalized_handoff


REQUIRED = {
    "races": {"race_id", "race_date", "post_time"},
    "results": {"race_id", "horse_id", "horse_number", "winner", "valid_starter"},
    "tm": {"race_id", "horse_id", "horse_number", "tm_score", "tm_data_category"},
    "odds": {"race_id", "horse_id", "horse_number", "snapshot_time", "decimal_odds"},
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--races", required=True)
    p.add_argument("--results", required=True)
    p.add_argument("--tm", required=True)
    p.add_argument("--odds", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--train-fraction", type=float, default=0.70)
    p.add_argument("--max-staleness-minutes", type=float, default=10.0)
    p.add_argument("--score-max-scale", type=float, default=5.0)
    p.add_argument("--score-grid-points", type=int, default=501)
    p.add_argument("--pool-grid-points", type=int, default=101)
    return p.parse_args()


def load(path: str, kind: str):
    with Path(path).open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = REQUIRED[kind] - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{kind} missing columns: {sorted(missing)}")
        return [dict(row) for row in reader]


def main() -> int:
    args = parse_args()
    out = analyze_normalized_handoff(
        load(args.races, "races"),
        load(args.results, "results"),
        load(args.tm, "tm"),
        load(args.odds, "odds"),
        train_fraction=args.train_fraction,
        max_staleness_minutes=args.max_staleness_minutes,
        score_max_scale=args.score_max_scale,
        score_grid_points=args.score_grid_points,
        pool_grid_points=args.pool_grid_points,
    )
    payload = {
        "schema": "payoff_b_racing_retrospective_primary_v1",
        **asdict(out),
        "claim_boundary": (
            "proper-score mechanism-separation analysis; no betting strategy "
            "or market-microstructure novelty claim"
        ),
    }
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
