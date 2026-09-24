#!/usr/bin/env python3
"""Build phase pairs only from adjacent preselected targets with valid phase."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.fixed_target_phase import (
    AnnotatedFixedTarget,
    build_adjacent_phase_pairs,
)


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "t", "yes", "y"}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("input_csv", type=Path)
    p.add_argument(
        "--pairs-output",
        type=Path,
        default=Path("outputs/aikens_fixed_24h_phase_pairs.csv"),
    )
    p.add_argument(
        "--receipt-output",
        type=Path,
        default=Path("outputs/aikens_fixed_24h_phase_pairs_receipt.json"),
    )
    args = p.parse_args()

    rows = []
    with args.input_csv.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit("input CSV has no header")
        for number, row in enumerate(reader, start=2):
            try:
                valid = parse_bool(row["phase_valid"])
                peak = (
                    None
                    if not row["local_peak_irg_timestamp"].strip()
                    else parse_time(row["local_peak_irg_timestamp"])
                )
                phase = (
                    None
                    if not row["phase_error_days"].strip()
                    else float(row["phase_error_days"])
                )
                rows.append(
                    AnnotatedFixedTarget(
                        animal_id=str(row["animal_id"]),
                        animal_year=str(row["animal_year"]),
                        group=str(row["group"]),
                        target_index=int(row["target_index"]),
                        target_timestamp=parse_time(row["target_timestamp"]),
                        observation_id=str(row["observation_id"]),
                        observed_timestamp=parse_time(row["observed_timestamp"]),
                        deviation_seconds=float(row["deviation_seconds"]),
                        pixel_id=str(row["pixel_id"]),
                        phase_valid=valid,
                        local_peak_irg_timestamp=peak,
                        phase_error_days=phase,
                        modis_product=(
                            str(row["modis_product"]) or None
                        ),
                        reconstruction_lane=(
                            str(row["reconstruction_lane"]) or None
                        ),
                    )
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid fixed-target phase row {number}: {exc}"
                ) from exc

    pairs = build_adjacent_phase_pairs(rows)

    args.pairs_output.parent.mkdir(parents=True, exist_ok=True)
    with args.pairs_output.open("w", newline="", encoding="utf-8") as handle:
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
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for pair in pairs:
            writer.writerow(
                {
                    "animal_id": pair.animal_id,
                    "animal_year": pair.animal_year,
                    "group": pair.group,
                    "start_target_index": pair.start_target_index,
                    "start_timestamp": pair.start_timestamp.isoformat(),
                    "end_timestamp": pair.end_timestamp.isoformat(),
                    "phase_before": pair.phase_before,
                    "phase_after": pair.phase_after,
                }
            )

    groups: dict[str, dict[str, object]] = {}
    for pair in pairs:
        row = groups.setdefault(
            pair.group,
            {"pairs": 0, "animals": set(), "animal_years": set()},
        )
        row["pairs"] = int(row["pairs"]) + 1
        row["animals"].add(pair.animal_id)
        row["animal_years"].add(pair.animal_year)

    group_summary = {
        group: {
            "pairs": int(values["pairs"]),
            "animals": len(values["animals"]),
            "animal_years": len(values["animal_years"]),
        }
        for group, values in sorted(groups.items())
    }

    receipt = {
        "status": "adjacent_fixed_target_phase_pairs_reconstructed",
        "source_file": str(args.input_csv),
        "phase_pairs": len(pairs),
        "groups": group_summary,
        "pairing_rule": "adjacent_target_indices_only",
        "missing_or_invalid_environment_breaks_chain": True,
        "target_selection_repeated_after_environment": False,
        "pairs_output": str(args.pairs_output),
        "lambda_outcome_opened": False,
    }
    args.receipt_output.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.pairs_output)
    print(args.receipt_output)


if __name__ == "__main__":
    main()
