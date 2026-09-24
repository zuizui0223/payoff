#!/usr/bin/env python3
"""Validate a frozen PAYOFF-B landscape projection on held-out outcomes."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tracking_empirical_outcome import (
    LandscapeOutcomeObservation,
    OutcomeValidationThresholds,
    evaluate_outcome_validation_gate,
    validate_landscape_outcome,
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prediction-json",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--observed-outcome-json",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--max-abs-final-abundance-relative-error",
        type=float,
    )
    parser.add_argument(
        "--max-abs-climate-centroid-error",
        type=float,
    )
    parser.add_argument(
        "--max-abs-phenology-shift-error",
        type=float,
    )
    parser.add_argument(
        "--max-abs-rms-mismatch-error",
        type=float,
    )
    parser.add_argument(
        "--max-abs-low-density-growth-error",
        type=float,
    )
    parser.add_argument(
        "--require-persistence-match",
        action="store_true",
    )
    parser.add_argument(
        "--fail-on-gate-failure",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_ecological_outcome_validation.json"
        ),
    )
    args = parser.parse_args()

    prediction_receipt = load_json(args.prediction_json)
    prediction = prediction_receipt.get("prediction")
    if prediction is None:
        raise SystemExit(
            "prediction JSON has no prediction payload"
        )

    observed_receipt = load_json(args.observed_outcome_json)
    observed_payload = observed_receipt.get(
        "observed_outcome",
        observed_receipt,
    )
    observed = LandscapeOutcomeObservation(
        final_abundance=observed_payload.get(
            "final_abundance"
        ),
        final_climate_centroid=observed_payload.get(
            "final_climate_centroid"
        ),
        final_phenology_shift=observed_payload.get(
            "final_phenology_shift"
        ),
        rms_abiotic_mismatch=observed_payload.get(
            "rms_abiotic_mismatch"
        ),
        mean_low_density_growth=observed_payload.get(
            "mean_low_density_growth"
        ),
        persisted=observed_payload.get("persisted"),
    )
    validation = validate_landscape_outcome(
        prediction,
        observed,
    )

    criteria_declared = any(
        value is not None
        for value in (
            args.max_abs_final_abundance_relative_error,
            args.max_abs_climate_centroid_error,
            args.max_abs_phenology_shift_error,
            args.max_abs_rms_mismatch_error,
            args.max_abs_low_density_growth_error,
        )
    ) or args.require_persistence_match

    if criteria_declared:
        thresholds = OutcomeValidationThresholds(
            max_abs_final_abundance_relative_error=(
                args.max_abs_final_abundance_relative_error
            ),
            max_abs_climate_centroid_error=(
                args.max_abs_climate_centroid_error
            ),
            max_abs_phenology_shift_error=(
                args.max_abs_phenology_shift_error
            ),
            max_abs_rms_mismatch_error=(
                args.max_abs_rms_mismatch_error
            ),
            max_abs_low_density_growth_error=(
                args.max_abs_low_density_growth_error
            ),
            require_persistence_match=(
                args.require_persistence_match
            ),
        )
        gate = evaluate_outcome_validation_gate(
            validation,
            thresholds,
        )
        gate_payload = asdict(gate)
        status = (
            "held_out_ecological_outcome_gate_pass"
            if gate.passed
            else "held_out_ecological_outcome_gate_fail"
        )
    else:
        gate = None
        gate_payload = None
        status = "held_out_ecological_outcome_errors_only"

    receipt = {
        "status": status,
        "prediction_source": str(args.prediction_json),
        "observed_outcome_source": str(
            args.observed_outcome_json
        ),
        "validation": asdict(validation),
        "gate": gate_payload,
        "claim_boundary": (
            "ecological outcome validation is downstream of tracking-control "
            "validation and uses independently held-out outcome data; "
            "tolerances are predeclared rather than fitted to errors"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "ecological_outcome_validation "
        f"status={status} "
        f"metrics={validation.compared_metrics} "
        f"abundance_rel_error="
        f"{validation.final_abundance_relative_error} "
        f"centroid_error="
        f"{validation.final_climate_centroid_error} "
        f"phenology_error="
        f"{validation.final_phenology_shift_error} "
        f"mismatch_error="
        f"{validation.rms_abiotic_mismatch_error} "
        f"growth_error="
        f"{validation.mean_low_density_growth_error} "
        f"persistence_match={validation.persistence_match}"
    )

    if (
        args.fail_on_gate_failure
        and gate is not None
        and not gate.passed
    ):
        raise SystemExit(
            "predeclared ecological outcome validation gate failed"
        )


if __name__ == "__main__":
    main()
