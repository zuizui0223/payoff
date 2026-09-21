#!/usr/bin/env python3
"""Build preregistered fixed-interval phase pairs from phase-annotated GPS."""

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

from src.fixed_interval_phase_pairs import (
    PhaseLocation,
    reconstruct_fixed_interval_phase_pairs,
)


def parse_time(value: str) -> datetime:
    value = value.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(
            f"timestamp is not ISO-8601 compatible: {value!r}"
        ) from exc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--animal-id-column", default="animal_id")
    parser.add_argument("--animal-year-column", default="animal_year")
    parser.add_argument("--group-column", default="group")
    parser.add_argument("--timestamp-column", default="timestamp")
    parser.add_argument(
        "--local-peak-column",
        default="local_peak_irg_timestamp",
    )
    parser.add_argument(
        "--target-interval-hours",
        type=float,
        default=24.0,
    )
    parser.add_argument(
        "--max-target-deviation-hours",
        type=float,
        default=3.0,
    )
    parser.add_argument(
        "--pairs-output",
        type=Path,
        default=Path(
            "outputs/payoff_b_fixed_interval_phase_pairs.csv"
        ),
    )
    parser.add_argument(
        "--receipt-output",
        type=Path,
        default=Path(
            "outputs/payoff_b_fixed_interval_phase_pairs_receipt.json"
        ),
    )
    args = parser.parse_args()

    required = (
        args.animal_id_column,
        args.animal_year_column,
        args.group_column,
        args.timestamp_column,
        args.local_peak_column,
    )
    observations = []

    with args.input_csv.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit("input CSV has no header row")
        missing = [
            column
            for column in required
            if column not in reader.fieldnames
        ]
        if missing:
            raise SystemExit(
                "missing required columns: "
                + ", ".join(missing)
            )

        for row_number, row in enumerate(reader, start=2):
            try:
                observations.append(
                    PhaseLocation(
                        animal_id=str(
                            row[args.animal_id_column]
                        ),
                        animal_year=str(
                            row[args.animal_year_column]
                        ),
                        group=str(row[args.group_column]),
                        timestamp=parse_time(
                            row[args.timestamp_column]
                        ),
                        local_peak_timestamp=parse_time(
                            row[args.local_peak_column]
                        ),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid input row {row_number}: {exc}"
                ) from exc

    result = reconstruct_fixed_interval_phase_pairs(
        observations,
        target_interval_seconds=(
            args.target_interval_hours * 3600.0
        ),
        max_target_deviation_seconds=(
            args.max_target_deviation_hours * 3600.0
        ),
    )

    args.pairs_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with args.pairs_output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        fieldnames = [
            "animal_id",
            "animal_year",
            "group",
            "start_target_index",
            "start_timestamp",
            "end_timestamp",
            "phase_before",
            "phase_after",
        ]
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        for pair in result.phase_pairs:
            row = asdict(pair)
            row["start_timestamp"] = (
                pair.start_timestamp.isoformat()
            )
            row["end_timestamp"] = (
                pair.end_timestamp.isoformat()
            )
            writer.writerow(row)

    group_counts: dict[str, dict[str, int]] = {}
    for pair in result.phase_pairs:
        group = group_counts.setdefault(
            pair.group,
            {
                "pairs": 0,
                "animal_years": 0,
                "animals": 0,
            },
        )
        group["pairs"] += 1

    for group_name, group in group_counts.items():
        group_pairs = [
            pair
            for pair in result.phase_pairs
            if pair.group == group_name
        ]
        group["animal_years"] = len(
            {pair.animal_year for pair in group_pairs}
        )
        group["animals"] = len(
            {pair.animal_id for pair in group_pairs}
        )

    receipt = {
        "status": "fixed_interval_phase_pairs_reconstructed",
        "source_file": str(args.input_csv),
        "target_interval_hours": (
            result.target_interval_seconds / 3600.0
        ),
        "max_target_deviation_hours": (
            result.max_target_deviation_seconds / 3600.0
        ),
        "animal_years_seen": result.animal_years_seen,
        "animal_years_with_pairs": (
            result.animal_years_with_pairs
        ),
        "matched_phase_points": result.matched_phase_points,
        "phase_pairs": len(result.phase_pairs),
        "groups": group_counts,
        "pairs_output": str(args.pairs_output),
        "claim_boundary": (
            "reconstruction only; no lambda estimate or forcing contrast is "
            "evaluated in this step"
        ),
    }
    args.receipt_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.pairs_output)
    print(args.receipt_output)
    print(
        "fixed_interval_phase_pairs "
        f"animal_years={result.animal_years_with_pairs} "
        f"pairs={len(result.phase_pairs)} "
        f"groups={','.join(result.groups)}"
    )


if __name__ == "__main__":
    main()
