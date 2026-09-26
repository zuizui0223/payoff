#!/usr/bin/env python3
"""Generate the canonical PAYOFF-B hidden-state coordination receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.partial_information_coordination import (
    ALWAYS_ADVANCE,
    ALWAYS_BASELINE,
    FOLLOW_CUE,
    REVERSE_CUE,
    HiddenStateGame,
    SpeciesCueParameters,
    focal_threshold_diagnostic,
    information_deficit_diagnostic,
    oracle_action_profile,
    pure_bayesian_nash_equilibria,
    realized_growths,
)


POLICY_NAMES = {
    ALWAYS_BASELINE: "always_baseline",
    FOLLOW_CUE: "follow_cue",
    REVERSE_CUE: "reverse_cue",
    ALWAYS_ADVANCE: "always_advance",
}


def canonical_game(migrant_accuracy: float) -> HiddenStateGame:
    local = SpeciesCueParameters(
        name="local_responder",
        cue_accuracy=1.0,
        baseline_growth=0.30,
        abiotic_mismatch_cost=0.60,
        interaction_mismatch_cost=0.20,
        advance_cost=0.05,
    )
    migrant = SpeciesCueParameters(
        name="migrant",
        cue_accuracy=migrant_accuracy,
        baseline_growth=0.40,
        abiotic_mismatch_cost=0.50,
        interaction_mismatch_cost=0.40,
        advance_cost=0.30,
    )
    return HiddenStateGame(
        species=(local, local, migrant),
        prior_advanced=0.5,
    )


def policy_names(profile):
    return [POLICY_NAMES[policy] for policy in profile]


def build_receipt() -> dict:
    game = canonical_game(0.60)
    threshold = focal_threshold_diagnostic(game, 2)
    diagnostic = information_deficit_diagnostic(game)
    equilibrium = diagnostic.selected_partial_equilibrium

    sweep = []
    for index in range(51):
        accuracy = 0.50 + index * 0.01
        row_game = canonical_game(accuracy)
        equilibria = pure_bayesian_nash_equilibria(row_game)
        selected = max(
            equilibria,
            key=lambda row: row.mean_expected_growth,
        )
        row_diagnostic = information_deficit_diagnostic(row_game)
        sweep.append(
            {
                "migrant_cue_accuracy": round(accuracy, 10),
                "n_pure_bayesian_equilibria": len(equilibria),
                "selected_policy_profile": policy_names(selected.policies),
                "migrant_policy": POLICY_NAMES[selected.policies[2]],
                "migrant_expected_growth": selected.expected_growths[2],
                "mean_expected_growth": selected.mean_expected_growth,
                "information_deficit": row_diagnostic.information_deficit,
            }
        )

    early_oracle = oracle_action_profile(game, 1)
    early_partial_actions = (
        equilibrium.policies[0][1],
        equilibrium.policies[1][1],
        equilibrium.policies[2][1],
    )

    return {
        "receipt_id": "payoff_b_hidden_state_game_canonical_20260926",
        "status": "synthetic_analytic_game_witness",
        "formal_interpretation": (
            "hidden-state Bayesian coordination game; not a quantum model"
        ),
        "canonical_design": {
            "prior_advanced": game.prior_advanced,
            "local_cue_accuracy": 1.0,
            "migrant_cue_accuracy": 0.60,
            "migrant_advance_cost": 0.30,
            "migrant_abiotic_mismatch_cost": 0.50,
            "migrant_interaction_mismatch_cost": 0.40,
        },
        "exact_threshold": {
            "critical_posterior_advanced": (
                threshold.critical_posterior_advanced
            ),
            "critical_positive_cue_accuracy": (
                threshold.critical_positive_cue_accuracy
            ),
            "posterior_after_positive_cue_at_accuracy_0_60": (
                threshold.posterior_after_advanced_cue
            ),
            "best_response_policy_at_accuracy_0_60": (
                POLICY_NAMES[threshold.best_response_policy]
            ),
        },
        "perfect_information": {
            "baseline_state_oracle_actions": list(
                oracle_action_profile(game, 0)
            ),
            "advanced_state_oracle_actions": list(early_oracle),
            "advanced_state_oracle_growths": list(
                realized_growths(game, 1, early_oracle)
            ),
            "expected_mean_growth": (
                diagnostic.oracle_expected_mean_growth
            ),
        },
        "partial_information": {
            "n_pure_bayesian_equilibria": len(
                diagnostic.partial_equilibria
            ),
            "selected_policy_profile": policy_names(
                equilibrium.policies
            ),
            "expected_growths": list(equilibrium.expected_growths),
            "expected_mean_growth": equilibrium.mean_expected_growth,
            "advanced_state_actions_after_positive_cues": list(
                early_partial_actions
            ),
            "advanced_state_growths_after_positive_cues": list(
                realized_growths(game, 1, early_partial_actions)
            ),
        },
        "deficit_decomposition": {
            "coordination_deficit": diagnostic.coordination_deficit,
            "information_deficit": diagnostic.information_deficit,
            "total_deficit": diagnostic.total_deficit,
            "information_only_trap": diagnostic.information_only_trap,
        },
        "cue_accuracy_sweep": sweep,
        "claim_boundary": [
            "the model is a synthetic hidden-state game",
            "cue accuracy is not yet estimated for a named migration system",
            "the canonical 2/3 threshold is parameter-specific, not universal",
            "the general result is existence of a reliability threshold when advancing is costly",
            "the information deficit is distinct from the existing unilateral coordination-accessibility barrier",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_hidden_state_game_canonical_20260926.json"
        ),
    )
    args = parser.parse_args()
    receipt = build_receipt()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
