#!/usr/bin/env python3
"""Audit pre-environment support ceiling from frozen fixed GPS targets."""

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
from src.fixed_target_support_ceiling import (
    audit_fixed_target_support_ceiling,
)


def parse_time(value: str) -> datetime:
    token = value.strip().replace("Z", "+00:00")
    return datetime.fromisoformat(token)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("targets_csv", type=Path)
    parser.add_argument("--min-animals-per-group", type=int, default=10)
    parser.add_argument("--min-pairs-per-group", type=int, default=100)
    parser.add_argument(
        "--fail-if-necessarily-not-estimable",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/aikens_fixed_target_support_ceiling.json"
        ),
    )
    args = parser.parse_args()

    targets: list[FixedIntervalGPSTarget] = []
    with args.targets_csv.open(
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
                targets.append(
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

    audit = audit_fixed_target_support_ceiling(
        targets,
        min_animals_per_group=args.min_animals_per_group,
        min_pairs_per_group=args.min_pairs_per_group,
    )

    payload = {
        "status": (
            "PRE_ENV_SUPPORT_CEILING_PASSES"
            if audit.all_groups_support_possible
            else "PRE_ENV_SUPPORT_CEILING_IMPOSSIBLE"
        ),
        "source_targets": str(args.targets_csv),
        "min_animals_per_group": audit.min_animals_per_group,
        "min_pairs_per_group": audit.min_pairs_per_group,
        "groups": [
            asdict(row)
            for row in audit.groups
        ],
        "all_groups_support_possible": (
            audit.all_groups_support_possible
        ),
        "necessarily_not_estimable": (
            audit.necessarily_not_estimable
        ),
        "interpretation": (
            "pass means the registered final support gate remains possible "
            "before environmental filtering; it does not guarantee final "
            "estimability. failure means the registered contrast is necessarily "
            "NOT ESTIMABLE regardless of environmental coverage."
        ),
        "lambda_outcome_opened": False,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    for row in audit.groups:
        print(
            "pre_env_support_ceiling "
            f"group={row.group} "
            f"animals_with_possible_pairs="
            f"{row.animals_with_possible_pairs} "
            f"max_possible_adjacent_pairs="
            f"{row.max_possible_adjacent_pairs} "
            f"support_possible={int(row.final_support_possible)}"
        )

    if (
        args.fail_if_necessarily_not_estimable
        and audit.necessarily_not_estimable
    ):
        raise SystemExit(
            "registered contrast is necessarily NOT ESTIMABLE "
            "under the pre-environment support ceiling"
        )


if __name__ == "__main__":
    main()
