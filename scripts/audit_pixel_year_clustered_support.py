#!/usr/bin/env python3
"""Run pixel-year clustered support sensitivity on frozen Aikens targets."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.fixed_interval_gps_targets import FixedIntervalGPSTarget
from src.fixed_target_clustered_coverage import (
    simulate_pixel_year_clustered_support,
)


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(
        value.strip().replace("Z", "+00:00")
    )


def parse_probability_list(value: str) -> list[float]:
    values = [
        float(token.strip())
        for token in value.split(",")
        if token.strip()
    ]
    if not values:
        raise argparse.ArgumentTypeError(
            "expected at least one comma-separated probability"
        )
    if any(p < 0.0 or p > 1.0 for p in values):
        raise argparse.ArgumentTypeError(
            "probabilities must lie in [0,1]"
        )
    return values


def read_targets(path: Path) -> list[FixedIntervalGPSTarget]:
    rows: list[FixedIntervalGPSTarget] = []
    with path.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        reader = csv.DictReader(handle)
        required = {
            "animal_id",
            "animal_year",
            "group",
            "target_index",
            "target_timestamp",
            "observation_id",
            "observed_timestamp",
            "deviation_seconds",
            "pixel_id",
        }
        if reader.fieldnames is None:
            raise SystemExit("targets CSV has no header row")
        missing = required.difference(reader.fieldnames)
        if missing:
            raise SystemExit(
                "targets CSV missing required columns: "
                + ", ".join(sorted(missing))
            )
        for row_number, row in enumerate(reader, start=2):
            try:
                rows.append(
                    FixedIntervalGPSTarget(
                        animal_id=str(row["animal_id"]),
                        animal_year=str(row["animal_year"]),
                        group=str(row["group"]),
                        target_index=int(row["target_index"]),
                        target_timestamp=parse_time(
                            str(row["target_timestamp"])
                        ),
                        observation_id=str(
                            row["observation_id"]
                        ),
                        observed_timestamp=parse_time(
                            str(row["observed_timestamp"])
                        ),
                        deviation_seconds=float(
                            row["deviation_seconds"]
                        ),
                        pixel_id=str(row["pixel_id"]),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid target row {row_number}: {exc}"
                ) from exc
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("targets_csv", type=Path)
    parser.add_argument(
        "--probabilities",
        type=parse_probability_list,
        default=parse_probability_list(
            "0.32,0.33,0.335,0.34,0.345,0.35"
        ),
    )
    parser.add_argument("--replicates", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260922)
    parser.add_argument(
        "--min-animals-per-group",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--min-pairs-per-group",
        type=int,
        default=100,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/aikens_pixel_year_clustered_support.json"
        ),
    )
    args = parser.parse_args()

    targets = read_targets(args.targets_csv)

    rows = []
    for index, p in enumerate(args.probabilities):
        result = simulate_pixel_year_clustered_support(
            targets,
            target_validity_probability=p,
            replicates=args.replicates,
            seed=args.seed + index * 1_000_003,
            min_animals_per_group=args.min_animals_per_group,
            min_pairs_per_group=args.min_pairs_per_group,
        )
        rows.append(result)

    payload = {
        "status": "PIXEL_YEAR_CLUSTERED_SUPPORT_SENSITIVITY",
        "source_targets": str(args.targets_csv),
        "targets": len(targets),
        "replicates_per_probability": args.replicates,
        "base_seed": args.seed,
        "cluster_definition": "pixel_id x target_timestamp.year",
        "results": [
            asdict(row)
            for row in rows
        ],
        "lambda_outcome_opened": False,
        "claim_boundary": (
            "fixed-seed Monte Carlo under independent pixel-year validity; "
            "real environmental missingness can have broader spatial, temporal "
            "and population-level dependence"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    for row in rows:
        print(
            "pixel_year_clustered_support "
            f"p={row.target_validity_probability:.6g} "
            f"joint={row.joint_probability_all_groups_pass:.6g} "
            f"ci95=[{row.joint_wilson_low_95:.6g},"
            f"{row.joint_wilson_high_95:.6g}] "
            f"clusters={row.unique_pixel_years}"
        )
        for group in row.groups:
            print(
                "pixel_year_clustered_group "
                f"p={row.target_validity_probability:.6g} "
                f"group={group.group} "
                f"support={group.probability_support_gate_passes:.6g} "
                f"mean_pairs={group.mean_valid_adjacent_pairs:.6g} "
                f"mean_animals={group.mean_animals_with_valid_pairs:.6g}"
            )


if __name__ == "__main__":
    main()
