#!/usr/bin/env python3
"""Evaluate the cross-system PAYOFF-B phase-retention gate."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.phase_retention_gate import (
    PhaseRetentionPrediction,
    estimate_phase_retention,
    evaluate_phase_retention_gate,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument(
        "--before-column",
        default="phase_before",
    )
    parser.add_argument(
        "--after-column",
        default="phase_after",
    )
    parser.add_argument("--lambda-low", type=float, required=True)
    parser.add_argument("--lambda-high", type=float, required=True)
    parser.add_argument("--min-pairs", type=int, default=3)
    parser.add_argument(
        "--require-retention-class",
        choices=(
            "sign_reversing",
            "restoring",
            "neutral_retention",
            "amplifying",
        ),
    )
    parser.add_argument(
        "--fail-on-gate-failure",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_phase_retention_gate.json"
        ),
    )
    args = parser.parse_args()

    pairs = []
    with args.csv_path.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit("CSV has no header row")
        missing = [
            column
            for column in (
                args.before_column,
                args.after_column,
            )
            if column not in reader.fieldnames
        ]
        if missing:
            raise SystemExit(
                "missing phase-retention columns: "
                + ", ".join(missing)
            )
        for row_number, row in enumerate(reader, start=2):
            try:
                pairs.append(
                    (
                        float(row[args.before_column]),
                        float(row[args.after_column]),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid row {row_number}: {exc}"
                ) from exc

    estimate = estimate_phase_retention(pairs)
    prediction = PhaseRetentionPrediction(
        lambda_low=args.lambda_low,
        lambda_high=args.lambda_high,
        min_pairs=args.min_pairs,
        require_retention_class=args.require_retention_class,
    )
    gate = evaluate_phase_retention_gate(
        estimate,
        prediction,
    )

    receipt = {
        "status": (
            "phase_retention_gate_pass"
            if gate.passed
            else "phase_retention_gate_fail"
        ),
        "source_file": str(args.csv_path),
        "gate": asdict(gate),
        "common_coordinate": (
            "e_out = residual_forcing + lambda * e_in"
        ),
        "actuator_layer": (
            "not evaluated here; speed, stopover, route reset and other "
            "mechanisms belong to separate system-specific prospective gates"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(
        "phase_retention_gate "
        f"passed={int(gate.passed)} "
        f"lambda={estimate.lambda_retention:.12g} "
        f"forcing={estimate.residual_forcing:.12g} "
        f"class={estimate.retention_class} "
        f"r2={estimate.r_squared}"
    )

    if args.fail_on_gate_failure and not gate.passed:
        raise SystemExit("phase-retention gate failed")


if __name__ == "__main__":
    main()
