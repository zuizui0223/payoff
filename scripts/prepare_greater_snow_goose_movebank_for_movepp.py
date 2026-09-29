#!/usr/bin/env python3
"""Apply frozen Movebank GPS hygiene before the movepp pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.movebank_event_hygiene import clean_movebank_gps_events


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, nargs="+", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--audit-output", type=Path, required=True)
    return p.parse_args()


def main():
    args = parse_args()
    import pandas as pd

    frames = [pd.read_csv(path) for path in args.input]
    raw = pd.concat(frames, ignore_index=True)
    clean, audit = clean_movebank_gps_events(raw)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(args.output, index=False)

    payload = {
        "contract": (
            "data/payoff_b_greater_snow_goose_raw_gps_hygiene_contract_20260929.json"
        ),
        "status": "PASS",
        **asdict(audit),
        "output_rows": int(len(clean)),
        "output_columns": list(clean.columns),
        "claim_boundary": (
            "input hygiene only; no movement-state or cue-uptake outcome opened"
        ),
    }
    args.audit_output.parent.mkdir(parents=True, exist_ok=True)
    args.audit_output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
