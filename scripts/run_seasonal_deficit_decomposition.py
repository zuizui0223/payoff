"""Emit two completely synthetic PAYOFF-B deficit-allocation witnesses.

Usage:
    python scripts/run_seasonal_deficit_decomposition.py
"""
from __future__ import annotations

import json
from dataclasses import asdict

from src.seasonal_deficit_decomposition import decompose_seasonal_deficit


def build_receipt() -> dict:
    w1 = decompose_seasonal_deficit(
        prior_early=0.55,
        cue_accuracy=0.55,
        joint_losses={
            "late": (0.0, 3.5),
            "early": (4.5, 0.0),
            "buffer": (1.0, 1.0),
        },
        private_losses={
            "late": (0.0, 1.5),
            "early": (2.5, 0.0),
            "buffer": (1.0, 1.0),
        },
        limited_actions=("late", "early"),
        full_actions=("late", "early", "buffer"),
    )
    losses = {"late": (0.0, 1.0), "early": (2.0, 0.0)}
    w2 = decompose_seasonal_deficit(
        prior_early=0.40,
        cue_accuracy=0.80,
        joint_losses=losses,
        private_losses=losses,
        limited_actions=("late",),
        full_actions=("late", "early"),
    )
    return {
        "claim_status": "SYNTHETIC_COUNTERFACTUAL_IDENTITY_NOT_EMPIRICAL_MECHANISM",
        "source_data_used": False,
        "intervention_scope": "binary hidden state; binary symmetric cue; finite nested actions",
        "w1_robust_action_information_complement": asdict(w1),
        "w2_irreversible_action_information_substitute": asdict(w2),
    }


def main() -> None:
    print(json.dumps(build_receipt(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
