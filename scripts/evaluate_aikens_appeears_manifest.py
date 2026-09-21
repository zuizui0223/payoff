#!/usr/bin/env python3
"""Evaluate canonical Aikens source coverage for an AppEEARS manifest."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.appeears_manifest_gate import (
    AppEEARSCoverageExpectation,
    canonical_aikens_coverage_expectation,
    evaluate_appeears_manifest_coverage,
)


def parse_int_list(value: str) -> tuple[int, ...]:
    return tuple(
        int(item.strip())
        for item in value.split(",")
        if item.strip()
    )


def parse_str_list(value: str) -> tuple[str, ...]:
    return tuple(
        item.strip()
        for item in value.split(",")
        if item.strip()
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest_json", type=Path)
    parser.add_argument(
        "--canonical-aikens",
        action="store_true",
        help="use the frozen 64,539-point Aikens source identity",
    )
    parser.add_argument("--expected-gps-observations", type=int)
    parser.add_argument("--required-years", type=parse_int_list)
    parser.add_argument("--required-groups", type=parse_str_list)
    parser.add_argument("--exact-year-set", action="store_true")
    parser.add_argument("--min-unique-cells", type=int, default=1)
    parser.add_argument(
        "--min-unique-cell-years",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--fail-on-gate-failure",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/aikens_appeears_manifest_coverage_gate.json"
        ),
    )
    args = parser.parse_args()

    manifest = json.loads(
        args.manifest_json.read_text(encoding="utf-8")
    )

    if args.canonical_aikens:
        custom_fields = (
            args.expected_gps_observations,
            args.required_years,
            args.required_groups,
        )
        if any(value is not None for value in custom_fields):
            raise SystemExit(
                "--canonical-aikens cannot be combined with custom "
                "expected count/year/group arguments"
            )
        expectation = canonical_aikens_coverage_expectation()
    else:
        expectation = AppEEARSCoverageExpectation(
            expected_gps_observations=(
                args.expected_gps_observations
            ),
            required_years=args.required_years or (),
            required_groups=args.required_groups or (),
            exact_year_set=args.exact_year_set,
            min_unique_cells=args.min_unique_cells,
            min_unique_cell_years=args.min_unique_cell_years,
        )

    gate = evaluate_appeears_manifest_coverage(
        manifest,
        expectation,
    )
    receipt = {
        "status": (
            "appeears_manifest_coverage_gate_pass"
            if gate.passed
            else "appeears_manifest_coverage_gate_fail"
        ),
        "manifest_source": str(args.manifest_json),
        "expectation": asdict(expectation),
        "gate": asdict(gate),
        "lambda_outcome_opened": False,
        "claim_boundary": (
            "source-identity and coverage gate only; does not authenticate, "
            "submit, or download an AppEEARS task"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "appeears_manifest_coverage_gate "
        f"passed={int(gate.passed)} "
        f"gps={gate.observed_gps_observations} "
        f"cells={gate.observed_unique_cells} "
        f"cell_years={gate.observed_unique_cell_years} "
        f"years={','.join(str(v) for v in gate.observed_years)} "
        f"groups={','.join(gate.observed_groups)} "
        f"reasons={';'.join(gate.reasons) if gate.reasons else 'none'}"
    )

    if args.fail_on_gate_failure and not gate.passed:
        raise SystemExit("AppEEARS source-coverage gate failed")


if __name__ == "__main__":
    main()
