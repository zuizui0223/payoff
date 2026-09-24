#!/usr/bin/env python3
"""Synthesize PAYOFF-B phase-retention gates across independent systems.

Manifest schema:

{
  "systems": [
    {
      "system_name": "system_A",
      "independent_test_id": "A_heldout",
      "forcing_regime": "moderate",
      "phase_coordinate_id": "signed_resource_phase_error",
      "segment_scale_id": "standardized_tracking_segment_v1",
      "phase_gate_json": "outputs/A_phase_gate.json",
      "actuator_gate_json": "outputs/A_actuator_gate.json"
    }
  ]
}

The phase-gate receipt paths must be unique. Actuator receipts are optional and
remain system-specific in the output.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.cross_system_phase_synthesis import (
    CrossSystemEvidence,
    synthesize_cross_system_phase,
)
from src.phase_retention_gate import (
    ActuatorGate,
    ActuatorPredictionResult,
    PhaseRetentionEstimate,
    PhaseRetentionGate,
    PhaseRetentionPrediction,
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def phase_gate_from_receipt(
    path: Path,
    *,
    require_prospective: bool,
) -> PhaseRetentionGate:
    receipt = load_json(path)
    if require_prospective and not bool(
        receipt.get("prospective_contract_satisfied", False)
    ):
        raise SystemExit(
            "prospective phase evidence requires a prospectively registered "
            f"evaluation receipt: {path}"
        )
    payload = receipt.get("gate")
    if payload is None:
        raise SystemExit(
            f"phase-gate receipt has no gate payload: {path}"
        )

    estimate_payload = dict(payload["estimate"])
    prediction_payload = dict(payload["prediction"])
    return PhaseRetentionGate(
        passed=bool(payload["passed"]),
        estimate=PhaseRetentionEstimate(
            **estimate_payload
        ),
        prediction=PhaseRetentionPrediction(
            **prediction_payload
        ),
        interval_passed=bool(payload["interval_passed"]),
        class_passed=bool(payload["class_passed"]),
        reasons=tuple(payload.get("reasons", ())),
    )


def actuator_gate_from_receipt(
    path: Path,
    *,
    require_prospective: bool,
) -> ActuatorGate:
    receipt = load_json(path)
    if require_prospective and not bool(
        receipt.get("prospective_contract_satisfied", False)
    ):
        raise SystemExit(
            "prospective actuator evidence requires a prospectively "
            f"registered evaluation receipt: {path}"
        )
    payload = receipt.get("gate")
    if payload is None:
        raise SystemExit(
            f"actuator-gate receipt has no gate payload: {path}"
        )
    predictions = tuple(
        ActuatorPredictionResult(**row)
        for row in payload.get("predictions", [])
    )
    return ActuatorGate(
        system_name=str(payload["system_name"]),
        predictions=predictions,
        prospective_predictions=int(
            payload["prospective_predictions"]
        ),
        passed_predictions=int(payload["passed_predictions"]),
        failed_predictions=int(payload["failed_predictions"]),
        all_prospective_passed=bool(
            payload["all_prospective_passed"]
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest_json", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_cross_system_phase_synthesis.json"
        ),
    )
    args = parser.parse_args()

    manifest = load_json(args.manifest_json)
    system_rows = manifest.get("systems")
    if not isinstance(system_rows, list) or not system_rows:
        raise SystemExit(
            "manifest requires a non-empty systems list"
        )

    phase_paths: list[str] = []
    evidence: list[CrossSystemEvidence] = []

    for index, row in enumerate(system_rows, start=1):
        try:
            system_name = str(row["system_name"])
            test_id = str(row["independent_test_id"])
            forcing_regime = str(row["forcing_regime"])
            phase_coordinate_id = str(row["phase_coordinate_id"])
            segment_scale_id = str(row["segment_scale_id"])
            evidence_tier = str(
                row.get("evidence_tier", "prospective")
            )
            phase_path = Path(row["phase_gate_json"])
        except (KeyError, TypeError) as exc:
            raise SystemExit(
                f"invalid system row {index}: {exc}"
            ) from exc

        phase_key = str(phase_path.resolve())
        if phase_key in phase_paths:
            raise SystemExit(
                "the same phase-gate receipt cannot be reused as "
                "independent cross-system evidence"
            )
        phase_paths.append(phase_key)

        actuator_path_value = row.get("actuator_gate_json")
        actuator = (
            None
            if actuator_path_value in (None, "")
            else actuator_gate_from_receipt(
                Path(actuator_path_value),
                require_prospective=(
                    evidence_tier == "prospective"
                ),
            )
        )

        evidence.append(
            CrossSystemEvidence(
                system_name=system_name,
                independent_test_id=test_id,
                forcing_regime=forcing_regime,
                phase_coordinate_id=phase_coordinate_id,
                segment_scale_id=segment_scale_id,
                phase_gate=phase_gate_from_receipt(
                    phase_path,
                    require_prospective=(
                        evidence_tier == "prospective"
                    ),
                ),
                evidence_tier=evidence_tier,
                actuator_gate=actuator,
            )
        )

    synthesis = synthesize_cross_system_phase(evidence)
    output = {
        "status": "cross_system_phase_retention_synthesis",
        "common_coordinate": (
            "e_out = residual_forcing + lambda * e_in"
        ),
        "phase_coordinate_id": synthesis.phase_coordinate_id,
        "segment_scale_id": synthesis.segment_scale_id,
        "synthesis": asdict(synthesis),
        "cross_system_claim_target": "prospectively registered lambda",
        "actuator_policy": (
            "system-specific prospective results only; "
            "no pooled actuator score"
        ),
        "no_combined_score": True,
        "claim_boundary": (
            "lambda synthesis is refused unless all independent tests share "
            "the same predeclared phase_coordinate_id and segment_scale_id; "
            "actuator failures do not invalidate passing lambda gates"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "cross_system_phase_synthesis "
        f"independent_lambda_tests={synthesis.independent_lambda_tests} "
        f"lambda_passed={synthesis.lambda_passed} "
        f"lambda_failed={synthesis.lambda_failed} "
        f"lambda_median={synthesis.lambda_median:.12g} "
        f"lambda_pass_actuator_fail="
        f"{len(synthesis.lambda_pass_actuator_fail_systems)}"
    )


if __name__ == "__main__":
    main()
