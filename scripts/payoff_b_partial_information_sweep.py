#!/usr/bin/env python3
"""Sweep remote-cue reliability in the PAYOFF-B partial-information game."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from src.partial_information_coordination import (
    PartialInformationTimingGame,
    evaluate_partial_information_game,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prior-early", type=float, default=0.55)
    parser.add_argument("--accuracy-min", type=float, default=0.50)
    parser.add_argument("--accuracy-max", type=float, default=1.00)
    parser.add_argument("--accuracy-step", type=float, default=0.01)
    parser.add_argument("--false-early-cost", type=float, default=2.0)
    parser.add_argument("--missed-early-cost", type=float, default=1.0)
    parser.add_argument(
        "--migrant-interaction-cost",
        type=float,
        default=0.5,
    )
    parser.add_argument(
        "--resident-interaction-cost",
        type=float,
        default=1.0,
    )
    parser.add_argument("--resident-partners", type=int, default=2)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/payoff_b_partial_information_sweep.csv"),
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=Path("outputs/payoff_b_partial_information_summary.json"),
    )
    return parser.parse_args()


def accuracy_grid(start: float, stop: float, step: float) -> list[float]:
    if step <= 0.0:
        raise ValueError("accuracy-step must be positive")
    if start < 0.5 or stop > 1.0 or start > stop:
        raise ValueError("accuracy range must satisfy 0.5 <= min <= max <= 1")
    values: list[float] = []
    value = start
    while value <= stop + 1e-12:
        values.append(round(value, 12))
        value += step
    return values


def main() -> None:
    args = parse_args()
    rows: list[dict[str, object]] = []

    for accuracy in accuracy_grid(
        args.accuracy_min,
        args.accuracy_max,
        args.accuracy_step,
    ):
        game = PartialInformationTimingGame(
            prior_early=args.prior_early,
            cue_accuracy=accuracy,
            false_early_cost=args.false_early_cost,
            missed_early_cost=args.missed_early_cost,
            migrant_interaction_mismatch_cost=args.migrant_interaction_cost,
            resident_interaction_mismatch_cost_per_partner=(
                args.resident_interaction_cost
            ),
            resident_partners=args.resident_partners,
        )
        diagnostic = evaluate_partial_information_game(game)
        rows.append(
            {
                "cue_accuracy": accuracy,
                "posterior_early_after_early_cue": (
                    diagnostic.posterior_early_after_early_cue
                ),
                "private_threshold": diagnostic.private_threshold,
                "joint_threshold": diagnostic.joint_threshold,
                "private_critical_accuracy": (
                    diagnostic.private_critical_accuracy
                ),
                "joint_critical_accuracy": (
                    diagnostic.joint_critical_accuracy
                ),
                "private_action_after_early_cue": (
                    diagnostic.early_cue_private_action
                ),
                "joint_action_after_early_cue": (
                    diagnostic.early_cue_joint_action
                ),
                "regime": diagnostic.early_cue_regime,
                "information_deficit": diagnostic.information_deficit,
                "coordination_deficit": diagnostic.coordination_deficit,
                "total_adaptation_deficit": (
                    diagnostic.total_adaptation_deficit
                ),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    reference = PartialInformationTimingGame(
        prior_early=args.prior_early,
        cue_accuracy=0.55,
        false_early_cost=args.false_early_cost,
        missed_early_cost=args.missed_early_cost,
        migrant_interaction_mismatch_cost=args.migrant_interaction_cost,
        resident_interaction_mismatch_cost_per_partner=(
            args.resident_interaction_cost
        ),
        resident_partners=args.resident_partners,
    )
    diagnostic = evaluate_partial_information_game(reference)
    summary = {
        "model": "payoff_b_partial_information_coordination_v1",
        "interpretation": (
            "destination residents observe realized spring state; migrant "
            "commits using a noisy remote cue"
        ),
        "private_critical_accuracy": diagnostic.private_critical_accuracy,
        "joint_critical_accuracy": diagnostic.joint_critical_accuracy,
        "accuracy_wedge_width": diagnostic.accuracy_wedge_width,
        "reference_accuracy": 0.55,
        "reference_regime": diagnostic.early_cue_regime,
        "reference_private_action_after_early_cue": (
            diagnostic.early_cue_private_action
        ),
        "reference_joint_action_after_early_cue": (
            diagnostic.early_cue_joint_action
        ),
        "reference_information_deficit": diagnostic.information_deficit,
        "reference_coordination_deficit": diagnostic.coordination_deficit,
        "claim_boundary": [
            "binary hidden-state mechanism model, not a calibrated bird system",
            "cue accuracy is a model parameter, not an empirical teleconnection estimate",
            "resident partners are assumed to observe destination state before acting",
            "capacity deficit is fixed to zero in this minimal model",
        ],
    }
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
