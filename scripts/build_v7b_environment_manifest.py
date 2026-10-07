#!/usr/bin/env python3
"""Build the frozen V7B fixed-region AppEEARS manifest from its source receipt."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.v7b_environment_manifest import (
    FeedbackRegion,
    build_feedback_appeears_manifest,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--source",
        type=Path,
        default=Path("data/payoff_b_v7b_environment_manifest_20261007.json"),
    )
    p.add_argument("--output", type=Path, required=True)
    return p.parse_args()


def main():
    args = parse_args()
    source = json.loads(args.source.read_text(encoding="utf-8"))
    regions = [
        FeedbackRegion(
            flyway=str(row["flyway"]),
            region_id=str(row["region_id"]),
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
        )
        for row in source["regions"]
    ]
    out = build_feedback_appeears_manifest(
        regions,
        years=[int(year) for year in source["years"]],
    )
    if out["expected_region_years"] != int(source["expected_region_years"]):
        raise SystemExit("source receipt and generated region-year count disagree")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.output)


if __name__ == "__main__":
    main()
