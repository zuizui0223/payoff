#!/usr/bin/env python3
"""Evaluate prospectively registered system-specific actuator predictions."""

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
    evaluate_registered_actuators,
)
from src.prospective_tracking_registry import (
    ActuatorObservation,
    ActuatorObservationSet,
    ActuatorPredictionSpec,
    ActuatorRegistration,
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
            "outputs/payoff_b_registered_actuator_evaluation.json"
        ),
    )
    args = parser.parse_args()

    registration_payload = json.loads(
        args.registration_json.read_text(encoding="utf-8")
    )
    observation_payload = json.loads(
        args.observation_json.read_text(encoding="utf-8")
    )

    predictions = tuple(
        ActuatorPredictionSpec(
            name=str(row["name"]),
            expected_direction=str(row["expected_direction"]),
            zero_tolerance=float(row.get("zero_tolerance", 0.0)),
        )
        for row in registration_payload["predictions"]
    )
    registration = ActuatorRegistration(
        system_name=str(registration_payload["system_name"]),
        independent_test_id=str(
            registration_payload["independent_test_id"]
        ),
        forcing_regime=str(registration_payload["forcing_regime"]),
        predictions=predictions,
    )
    observations = ActuatorObservationSet(
        system_name=str(observation_payload["system_name"]),
        independent_test_id=str(
            observation_payload["independent_test_id"]
        ),
        observations=tuple(
            ActuatorObservation(
                name=str(row["name"]),
                observed_effect=float(row["observed_effect"]),
            )
            for row in observation_payload["observations"]
        ),
    )
    evaluation = evaluate_registered_actuators(
        registration,
        observations,
    )

    receipt = {
        "status": (
            "prospective_actuator_gate_pass"
            if evaluation.gate.all_prospective_passed
            else "prospective_actuator_gate_fail"
        ),
        "registration_source": str(args.registration_json),
        "observation_source": str(args.observation_json),
        "system_name": evaluation.system_name,
        "independent_test_id": evaluation.independent_test_id,
        "forcing_regime": evaluation.forcing_regime,
        "prospective_contract_satisfied": True,
        "gate": asdict(evaluation.gate),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "registered_actuator_gate "
        f"system={evaluation.system_name} "
        f"passed={evaluation.gate.passed_predictions} "
        f"failed={evaluation.gate.failed_predictions} "
        f"all_passed={int(evaluation.gate.all_prospective_passed)}"
    )

    if (
        args.fail_on_gate_failure
        and not evaluation.gate.all_prospective_passed
    ):
        raise SystemExit(
            "prospectively registered actuator gate failed"
        )


if __name__ == "__main__":
    main()
