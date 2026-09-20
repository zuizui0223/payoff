#!/usr/bin/env python3
"""Evaluate predeclared held-out validation criteria for PAYOFF-B controls."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.tracking_empirical_gate import (
    TrackingValidationThresholds,
    evaluate_tracking_validation_gate,
)
from src.tracking_empirical_validation import (
    HeldOutMovementValidation,
    HeldOutPhaseValidation,
    HeldOutTrackingValidation,
)


def _validation_payload(receipt: dict) -> dict:
    if "validation" in receipt:
        return receipt["validation"]
    if "held_out_validation" in receipt:
        return receipt["held_out_validation"]
    raise SystemExit(
        "validation JSON must contain validation or held_out_validation"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--validation-json",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--max-movement-moment-rmse",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--min-held-out-intervals",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--require-phase-validation",
        action="store_true",
    )
    parser.add_argument(
        "--max-abs-phase-log-error",
        type=float,
    )
    parser.add_argument(
        "--min-phase-intervals",
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
            "outputs/payoff_b_tracking_validation_gate.json"
        ),
    )
    args = parser.parse_args()

    receipt = json.loads(
        args.validation_json.read_text(encoding="utf-8")
    )
    payload = _validation_payload(receipt)
    validation = HeldOutTrackingValidation(
        movement=HeldOutMovementValidation(
            **payload["movement"]
        ),
        phase=HeldOutPhaseValidation(
            **payload["phase"]
        ),
    )
    thresholds = TrackingValidationThresholds(
        max_movement_moment_rmse=(
            args.max_movement_moment_rmse
        ),
        min_held_out_intervals=args.min_held_out_intervals,
        require_phase_validation=args.require_phase_validation,
        max_abs_phase_log_error=args.max_abs_phase_log_error,
        min_phase_intervals=args.min_phase_intervals,
    )
    gate = evaluate_tracking_validation_gate(
        validation,
        thresholds,
    )

    output = {
        "status": (
            "held_out_tracking_gate_pass"
            if gate.passed
            else "held_out_tracking_gate_fail"
        ),
        "validation_source": str(args.validation_json),
        "gate": asdict(gate),
        "claim_boundary": (
            "thresholds are predeclared analysis criteria and are not fitted "
            "to held-out validation performance"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "tracking_validation_gate "
        f"passed={int(gate.passed)} "
        f"movement_passed={int(gate.movement_passed)} "
        f"phase_passed={int(gate.phase_passed)} "
        f"movement_rmse={gate.movement_rmse:.12g} "
        f"phase_abs_error={gate.abs_phase_log_error} "
        f"reasons={';'.join(gate.reasons) if gate.reasons else 'none'}"
    )

    if args.fail_on_gate_failure and not gate.passed:
        raise SystemExit("predeclared held-out tracking validation gate failed")


if __name__ == "__main__":
    main()
