#!/usr/bin/env python3
"""Evaluate cross-system lambda reliability from the frozen registry."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.cross_system_lambda_reliability import (
    evaluate_cross_system_lambda_reliability,
    systems_from_registry,
)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--registry-json",
        type=Path,
        default=Path(
            "data/payoff_b_lambda_recovery_taxon_registry_20260922.json"
        ),
    )
    p.add_argument(
        "--minimum-taxa-for-coordinate",
        type=int,
        default=3,
    )
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_cross_system_lambda_reliability_gate.json"
        ),
    )
    args = p.parse_args()

    registry = json.loads(
        args.registry_json.read_text(encoding="utf-8")
    )
    gate = evaluate_cross_system_lambda_reliability(
        systems_from_registry(registry),
        minimum_taxa_for_coordinate=args.minimum_taxa_for_coordinate,
    )

    payload = {
        "status": "cross_system_lambda_reliability_gate_evaluated",
        "registry_source": str(args.registry_json),
        "gate": asdict(gate),
        "claim_boundary": {
            "coordinate_claim": (
                "licensed"
                if gate.estimator_scale_coordinate_licensed
                else "hold"
            ),
            "latent_magnitude_comparison": (
                "licensed"
                if gate.latent_magnitude_comparison_licensed
                else "hold"
            ),
            "rule": (
                "assumption-conditional sensitivity does not count as "
                "source-specific measurement-error identification"
            ),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "cross_system_lambda_reliability "
        f"taxa={gate.unique_taxa} "
        f"coordinate={int(gate.estimator_scale_coordinate_licensed)} "
        f"latent_magnitude={int(gate.latent_magnitude_comparison_licensed)} "
        f"identified_taxa={gate.taxa_with_source_specific_error_identification}"
    )


if __name__ == "__main__":
    main()
