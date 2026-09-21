#!/usr/bin/env python3
"""Evaluate a prospectively registered PAYOFF-B lambda prediction."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.prospective_tracking_evaluation import (
    PhaseObservationSet,
    ReportedPhaseObservation,
    evaluate_registered_phase,
    evaluate_registered_reported_phase,
)
from src.prospective_tracking_registry import (
    PhaseRetentionRegistration,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registration-json", type=Path, required=True)
    parser.add_argument("--observation-json", type=Path, required=True)
    parser.add_argument(
        "--fail-on-gate-failure",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_registered_phase_retention_evaluation.json"
        ),
    )
    args = parser.parse_args()

    registration_payload = json.loads(
        args.registration_json.read_text(encoding="utf-8")
    )
    observation_payload = json.loads(
        args.observation_json.read_text(encoding="utf-8")
    )

    registration = PhaseRetentionRegistration(
        **registration_payload
    )
    common = {
        "system_name": str(observation_payload["system_name"]),
        "independent_test_id": str(
            observation_payload["independent_test_id"]
        ),
        "phase_coordinate_id": str(
            observation_payload["phase_coordinate_id"]
        ),
        "segment_scale_id": str(
            observation_payload["segment_scale_id"]
        ),
    }

    if "reported_estimate" in observation_payload:
        reported = observation_payload["reported_estimate"]
        observations = ReportedPhaseObservation(
            **common,
            pairs=int(reported["pairs"]),
            lambda_retention=float(
                reported["lambda_retention"]
            ),
            lambda_se=(
                None
                if reported.get("lambda_se") is None
                else float(reported["lambda_se"])
            ),
            p_vs_no_correction=(
                None
                if reported.get("p_vs_no_correction") is None
                else float(reported["p_vs_no_correction"])
            ),
        )
        evaluation = evaluate_registered_reported_phase(
            registration,
            observations,
        )
        observation_mode = "reported_summary"
    else:
        pairs = tuple(
            (float(row[0]), float(row[1]))
            for row in observation_payload["pairs"]
        )
        observations = PhaseObservationSet(
            **common,
            pairs=pairs,
        )
        evaluation = evaluate_registered_phase(
            registration,
            observations,
        )
        observation_mode = "raw_pairs"

    receipt = {
        "status": (
            "prospective_phase_retention_gate_pass"
            if evaluation.gate.passed
            else "prospective_phase_retention_gate_fail"
        ),
        "registration_source": str(args.registration_json),
        "observation_source": str(args.observation_json),
        "system_name": evaluation.system_name,
        "independent_test_id": evaluation.independent_test_id,
        "forcing_regime": evaluation.forcing_regime,
        "phase_coordinate_id": evaluation.phase_coordinate_id,
        "segment_scale_id": evaluation.segment_scale_id,
        "prospective_contract_satisfied": True,
        "observation_mode": observation_mode,
        "gate": asdict(evaluation.gate),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "registered_phase_retention "
        f"system={evaluation.system_name} "
        f"passed={int(evaluation.gate.passed)} "
        f"lambda={evaluation.gate.estimate.lambda_retention:.12g} "
        f"class={evaluation.gate.estimate.retention_class}"
    )

    if args.fail_on_gate_failure and not evaluation.gate.passed:
        raise SystemExit("prospectively registered lambda gate failed")


if __name__ == "__main__":
    main()
