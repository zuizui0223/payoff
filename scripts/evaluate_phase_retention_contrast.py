#!/usr/bin/env python3
"""Evaluate a preregistered within-system contrast in phase retention."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.phase_retention_contrast import (
    PhaseRetentionContrastObservation,
    PhaseRetentionContrastRegistration,
    evaluate_phase_retention_contrast,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registration-json", type=Path, required=True)
    parser.add_argument("--observation-json", type=Path, required=True)
    parser.add_argument("--fail-on-gate-failure", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_phase_retention_contrast_gate.json"
        ),
    )
    args = parser.parse_args()

    registration = PhaseRetentionContrastRegistration(
        **json.loads(
            args.registration_json.read_text(encoding="utf-8")
        )
    )
    observation = PhaseRetentionContrastObservation(
        **json.loads(
            args.observation_json.read_text(encoding="utf-8")
        )
    )
    gate = evaluate_phase_retention_contrast(
        registration,
        observation,
    )

    receipt = {
        "status": (
            "phase_retention_contrast_gate_pass"
            if gate.passed
            else "phase_retention_contrast_gate_fail"
        ),
        "registration_source": str(args.registration_json),
        "observation_source": str(args.observation_json),
        "prospective_contract_satisfied": True,
        "gate": asdict(gate),
        "claim_boundary": (
            "within-system forcing contrast on lambda; this is not an "
            "additional taxon and should not be counted as an independent "
            "cross-taxon replication"
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "phase_retention_contrast_gate "
        f"system={registration.system_name} "
        f"group_a={registration.group_a} "
        f"group_b={registration.group_b} "
        f"delta_lambda={gate.lambda_difference_b_minus_a:.12g} "
        f"direction_passed={int(gate.direction_passed)} "
        f"support_passed={int(gate.support_passed)} "
        f"passed={int(gate.passed)}"
    )

    if args.fail_on_gate_failure and not gate.passed:
        raise SystemExit(
            "preregistered phase-retention contrast gate failed"
        )


if __name__ == "__main__":
    main()
