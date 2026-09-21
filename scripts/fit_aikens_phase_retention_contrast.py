#!/usr/bin/env python3
"""Fit the frozen Aikens phase-retention contrast from fixed 24-hour pairs."""

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

from src.phase_retention_contrast_fit import (
    PhasePairRecord,
    fit_phase_retention_contrast,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pairs_csv", type=Path)
    parser.add_argument(
        "--registration-json",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--group-a-value",
        default="small",
        help="group value in phase-pair CSV corresponding to registered group A",
    )
    parser.add_argument(
        "--group-b-value",
        default="large",
        help="group value in phase-pair CSV corresponding to registered group B",
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
        "--fail-on-not-estimable",
        action="store_true",
    )
    parser.add_argument(
        "--fit-receipt-output",
        type=Path,
        default=Path(
            "outputs/aikens_phase_retention_contrast_fit_receipt.json"
        ),
    )
    parser.add_argument(
        "--observation-output",
        type=Path,
        default=Path(
            "outputs/aikens_phase_retention_contrast_observation.json"
        ),
    )
    args = parser.parse_args()

    registration = json.loads(
        args.registration_json.read_text(
            encoding="utf-8"
        )
    )

    required_columns = (
        "animal_id",
        "animal_year",
        "group",
        "phase_before",
        "phase_after",
    )
    records = []
    with args.pairs_csv.open(
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit("phase-pair CSV has no header row")
        missing = [
            column
            for column in required_columns
            if column not in reader.fieldnames
        ]
        if missing:
            raise SystemExit(
                "phase-pair CSV missing required columns: "
                + ", ".join(missing)
            )

        for row_number, row in enumerate(reader, start=2):
            try:
                records.append(
                    PhasePairRecord(
                        animal_id=str(row["animal_id"]),
                        animal_year=str(row["animal_year"]),
                        group=str(row["group"]),
                        phase_before=float(
                            row["phase_before"]
                        ),
                        phase_after=float(
                            row["phase_after"]
                        ),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise SystemExit(
                    f"invalid phase-pair row {row_number}: {exc}"
                ) from exc

    fit = fit_phase_retention_contrast(
        records,
        group_a_value=args.group_a_value,
        group_b_value=args.group_b_value,
        min_animals_per_group=args.min_animals_per_group,
        min_pairs_per_group=args.min_pairs_per_group,
    )

    receipt = {
        "status": (
            "phase_retention_contrast_estimable"
            if fit.estimable
            else "phase_retention_contrast_not_estimable"
        ),
        "source_pairs": str(args.pairs_csv),
        "registration_source": str(
            args.registration_json
        ),
        "group_value_map": {
            str(registration["group_a"]): (
                args.group_a_value
            ),
            str(registration["group_b"]): (
                args.group_b_value
            ),
        },
        "support_thresholds": {
            "min_animals_per_group": (
                args.min_animals_per_group
            ),
            "min_pairs_per_group": (
                args.min_pairs_per_group
            ),
        },
        "fit": asdict(fit),
        "observation_output": (
            str(args.observation_output)
            if fit.estimable
            else None
        ),
        "lambda_outcome_opened": bool(fit.estimable),
        "claim_boundary": (
            "registered pair-level regression with animal-year fixed effects "
            "and animal-clustered uncertainty; no threshold retuning allowed"
        ),
    }

    args.fit_receipt_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    args.fit_receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    if fit.estimable:
        observation = {
            "system_name": registration[
                "system_name"
            ],
            "independent_test_id": registration[
                "independent_test_id"
            ],
            "phase_coordinate_id": registration[
                "phase_coordinate_id"
            ],
            "segment_scale_id": registration[
                "segment_scale_id"
            ],
            "group_a": registration["group_a"],
            "group_b": registration["group_b"],
            "lambda_a": fit.lambda_a,
            "lambda_b": fit.lambda_b,
            "p_difference": fit.p_difference,
            "fit_provenance": {
                "source_pairs": str(args.pairs_csv),
                "fit_receipt": str(
                    args.fit_receipt_output
                ),
                "delta_lambda_b_minus_a": (
                    fit.delta_lambda_b_minus_a
                ),
                "delta_lambda_se": fit.delta_lambda_se,
                "lambda_a_se": fit.lambda_a_se,
                "lambda_b_se": fit.lambda_b_se,
                "total_pairs": fit.total_pairs,
                "total_animals": fit.total_animals,
                "total_animal_years": (
                    fit.total_animal_years
                ),
            },
        }
        args.observation_output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        args.observation_output.write_text(
            json.dumps(
                observation,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    print(args.fit_receipt_output)
    print(
        "aikens_phase_retention_fit "
        f"estimable={int(fit.estimable)} "
        f"pairs={fit.total_pairs} "
        f"animals={fit.total_animals} "
        f"lambda_a={fit.lambda_a} "
        f"lambda_b={fit.lambda_b} "
        f"delta={fit.delta_lambda_b_minus_a} "
        f"p={fit.p_difference} "
        f"reasons={';'.join(fit.reasons) if fit.reasons else 'none'}"
    )

    if args.fail_on_not_estimable and not fit.estimable:
        raise SystemExit(
            "frozen Aikens phase-retention contrast is not estimable"
        )


if __name__ == "__main__":
    main()
