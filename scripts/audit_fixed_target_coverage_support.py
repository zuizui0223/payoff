#!/usr/bin/env python3
"""Quantify Aikens support robustness under IID target-level environment validity."""

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
from src.fixed_target_coverage_support import (
    exact_iid_target_coverage_support,
    find_minimum_iid_target_validity,
)


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(
        value.strip().replace("Z", "+00:00")
    )


def parse_probability_list(value: str) -> list[float]:
    result = [
        float(token.strip())
        for token in value.split(",")
        if token.strip()
    ]
    if not result:
        raise argparse.ArgumentTypeError(
            "expected at least one comma-separated probability"
        )
    if any(p < 0.0 or p > 1.0 for p in result):
        raise argparse.ArgumentTypeError(
            "probabilities must lie in [0,1]"
        )
    return result


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
            "0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1"
        ),
    )
    parser.add_argument(
        "--target-joint-support-probability",
        type=float,
        default=0.95,
    )
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
        "--threshold-tolerance",
        type=float,
        default=1e-4,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/aikens_iid_target_coverage_support.json"
        ),
    )
    args = parser.parse_args()

    targets = read_targets(args.targets_csv)
    grid = [
        exact_iid_target_coverage_support(
            targets,
            target_validity_probability=p,
            min_animals_per_group=args.min_animals_per_group,
            min_pairs_per_group=args.min_pairs_per_group,
        )
        for p in args.probabilities
    ]
    threshold = find_minimum_iid_target_validity(
        targets,
        target_joint_support_probability=(
            args.target_joint_support_probability
        ),
        min_animals_per_group=args.min_animals_per_group,
        min_pairs_per_group=args.min_pairs_per_group,
        tolerance=args.threshold_tolerance,
    )

    payload = {
        "status": "IID_TARGET_VALIDITY_SUPPORT_ENVELOPE",
        "source_targets": str(args.targets_csv),
        "targets": len(targets),
        "assumption": (
            "each frozen target independently has valid environmental phase "
            "with common probability p"
        ),
        "grid": [
            {
                "target_validity_probability": row.target_validity_probability,
                "joint_probability_all_groups_pass": (
                    row.joint_probability_all_groups_pass
                ),
                "groups": [
                    asdict(group)
                    for group in row.groups
                ],
            }
            for row in grid
        ],
        "threshold": asdict(threshold),
        "lambda_outcome_opened": False,
        "claim_boundary": (
            "exact under IID target-level validity only; real MODIS/IRG "
            "failures can be correlated by pixel-year, date, geography, "
            "snow/quality state, or population, so this is a synthetic "
            "support-robustness envelope rather than a guarantee"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    if threshold.minimum_target_validity_probability is None:
        print(
            "iid_target_coverage_threshold "
            "minimum_p=NONE "
            f"joint_support={threshold.achieved_joint_support_probability:.12g}"
        )
    else:
        print(
            "iid_target_coverage_threshold "
            f"target_joint={threshold.target_joint_support_probability:.12g} "
            f"minimum_p={threshold.minimum_target_validity_probability:.12g} "
            f"achieved_joint={threshold.achieved_joint_support_probability:.12g}"
        )
        for group in threshold.groups:
            print(
                "iid_target_coverage_group "
                f"group={group.group} "
                f"support_probability="
                f"{group.probability_support_gate_passes:.12g} "
                f"expected_pairs="
                f"{group.expected_valid_adjacent_pairs:.12g} "
                f"expected_animals="
                f"{group.expected_animals_with_valid_pairs:.12g}"
            )


if __name__ == "__main__":
    main()
