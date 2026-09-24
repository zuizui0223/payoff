#!/usr/bin/env python3
"""Evaluate system-specific prospective actuator predictions independently."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.phase_retention_gate import (
    ActuatorPrediction,
    evaluate_actuator_gate,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("prediction_json", type=Path)
    parser.add_argument(
        "--fail-on-gate-failure",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_actuator_gate.json"
        ),
    )
    args = parser.parse_args()

    payload = json.loads(
        args.prediction_json.read_text(encoding="utf-8")
    )
    system_name = payload.get("system_name")
    if not system_name:
        raise SystemExit("prediction JSON requires system_name")

    predictions = []
    for index, row in enumerate(
        payload.get("predictions", []),
        start=1,
    ):
        try:
            predictions.append(
                ActuatorPrediction(
                    name=row["name"],
                    expected_direction=row["expected_direction"],
                    observed_effect=float(row["observed_effect"]),
                    zero_tolerance=float(
                        row.get("zero_tolerance", 0.0)
                    ),
                    observed_p_value=(
                        None
                        if row.get("p_value") is None
                        else float(row["p_value"])
                    ),
                    max_p_value=(
                        None
                        if row.get("max_p_value") is None
                        else float(row["max_p_value"])
                    ),
                    prospective=bool(
                        row.get("prospective", True)
                    ),
                )
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise SystemExit(
                f"invalid actuator prediction {index}: {exc}"
            ) from exc

    gate = evaluate_actuator_gate(
        str(system_name),
        predictions,
    )
    receipt = {
        "status": (
            "actuator_gate_pass"
            if gate.all_prospective_passed
            else "actuator_gate_fail"
        ),
        "gate": asdict(gate),
        "claim_boundary": (
            "system-specific prospective actuator test; failure does not "
            "invalidate a separately passing phase-retention lambda gate"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(
        "actuator_gate "
        f"system={gate.system_name} "
        f"prospective={gate.prospective_predictions} "
        f"passed={gate.passed_predictions} "
        f"failed={gate.failed_predictions} "
        f"all_passed={int(gate.all_prospective_passed)}"
    )

    if (
        args.fail_on_gate_failure
        and not gate.all_prospective_passed
    ):
        raise SystemExit("system-specific actuator gate failed")


if __name__ == "__main__":
    main()
