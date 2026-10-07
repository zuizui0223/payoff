#!/usr/bin/env python3
"""Validate normalized JV-Link racing handoff CSVs and write an audit receipt."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import argparse
import csv
import json
from pathlib import Path

from src.racing_jvlink_contract import validate_normalized_handoff


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
    audit = validate_normalized_handoff(
        load(args.races, "races"),
        load(args.results, "results"),
        load(args.tm, "tm"),
        load(args.odds, "odds"),
    )
    payload = {
        "schema": "payoff_b_racing_jvlink_handoff_audit_v1",
        "races": audit.races,
        "result_rows": audit.result_rows,
        "tm_rows": audit.tm_rows,
        "odds_rows": audit.odds_rows,
        "candidate_races": audit.candidate_races,
        "status": "PASS",
        "primary_tm_category": 7,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
