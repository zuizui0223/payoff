#!/usr/bin/env python3
"""Map robustness of information cascades and hysteresis in PAYOFF-B."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from src.bayesian_timing_coordination import (
    FOLLOW_CUE,
    canonical_three_player_game,
    policy_label,
    pure_bayesian_nash_equilibria,
    sequential_best_response,
)


FOLLOW_ALL = (FOLLOW_CUE, FOLLOW_CUE, FOLLOW_CUE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prior-early", type=float, default=0.40)
    parser.add_argument("--local-accuracy-min", type=float, default=0.75)
    parser.add_argument("--local-accuracy-max", type=float, default=1.00)
    parser.add_argument("--local-accuracy-step", type=float, default=0.025)
    parser.add_argument("--interaction-min", type=float, default=0.00)
    parser.add_argument("--interaction-max", type=float, default=1.00)
    parser.add_argument("--interaction-step", type=float, default=0.025)
    parser.add_argument("--migrant-accuracy-min", type=float, default=0.50)
    parser.add_argument("--migrant-accuracy-max", type=float, default=1.00)
    parser.add_argument("--migrant-accuracy-step", type=float, default=0.01)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/payoff_b_bayesian_phase_diagram.csv"),
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=Path("outputs/payoff_b_bayesian_phase_diagram_summary.json"),
    )
    return parser.parse_args()


def grid(start: float, stop: float, step: float) -> list[float]:
    if step <= 0.0:
        raise ValueError("grid step must be positive")
    if start > stop:
        raise ValueError("grid start must be <= stop")
    values: list[float] = []
    value = start
    while value <= stop + 1e-12:
        values.append(round(value, 12))
        value += step
    return values


def profile_text(profile) -> str:
    return "|".join(policy_label(policy) for policy in profile)


def run_historical_path(
    local_accuracy: float,
    interaction_strength: float,
    migrant_accuracies: list[float],
    prior_early: float = 0.40,
) -> dict[str, object]:
    descending = list(reversed(migrant_accuracies))
    baseline_game = canonical_three_player_game(
        descending[0],
        interaction_strength=interaction_strength,
        local_accuracy=local_accuracy,
    )
    baseline = sequential_best_response(
        baseline_game,
        FOLLOW_ALL,
    ).final
    baseline_profile = baseline.profile
    eligible = baseline_profile == FOLLOW_ALL

    profile = baseline_profile
    collapse_accuracy: float | None = None
    for migrant_accuracy in descending:
        game = canonical_three_player_game(
            migrant_accuracy,
            interaction_strength=interaction_strength,
            local_accuracy=local_accuracy,
            prior_early=prior_early,
        )
        result = sequential_best_response(game, profile)
        profile = result.final.profile
        if (
            collapse_accuracy is None
            and eligible
            and (
                profile[0] != FOLLOW_CUE
                or profile[1] != FOLLOW_CUE
            )
        ):
            collapse_accuracy = migrant_accuracy

    low_information_profile = profile

    for migrant_accuracy in migrant_accuracies:
        game = canonical_three_player_game(
            migrant_accuracy,
            interaction_strength=interaction_strength,
            local_accuracy=local_accuracy,
            prior_early=prior_early,
        )
        result = sequential_best_response(game, profile)
        profile = result.final.profile

    recovered_profile = profile
    recovered_game = canonical_three_player_game(
        migrant_accuracies[-1],
        interaction_strength=interaction_strength,
        local_accuracy=local_accuracy,
    )
    recovered_evaluation = sequential_best_response(
        recovered_game,
        recovered_profile,
    ).final
    equilibria = pure_bayesian_nash_equilibria(recovered_game)
    best_equilibrium = equilibria[0]
    history_lock_loss = (
        best_equilibrium.joint_payoff
        - recovered_evaluation.joint_payoff
    )

    cascade = eligible and collapse_accuracy is not None
    hysteresis = eligible and recovered_profile != baseline_profile
    inefficient_hysteresis = (
        cascade
        and hysteresis
        and history_lock_loss > 1e-12
    )

    if not eligible:
        phase = "baseline_not_following"
    elif not cascade:
        phase = "no_resident_cascade"
    elif not hysteresis:
        phase = "reversible_cascade"
    elif inefficient_hysteresis:
        phase = "inefficient_information_hysteresis"
    else:
        phase = "history_dependence_without_joint_loss"

    return {
        "prior_early": prior_early,
        "local_cue_accuracy": local_accuracy,
        "interaction_strength": interaction_strength,
        "baseline_profile": profile_text(baseline_profile),
        "baseline_joint_payoff": baseline.joint_payoff,
        "resident_cascade": cascade,
        "collapse_migrant_accuracy": collapse_accuracy,
        "low_information_profile": profile_text(low_information_profile),
        "recovered_profile": profile_text(recovered_profile),
        "best_recovered_equilibrium": profile_text(best_equilibrium.profile),
        "recovered_joint_payoff": recovered_evaluation.joint_payoff,
        "best_recovered_joint_payoff": best_equilibrium.joint_payoff,
        "history_lock_loss": history_lock_loss,
        "hysteresis": hysteresis,
        "inefficient_hysteresis": inefficient_hysteresis,
        "phase": phase,
        "recovered_pure_bne_count": len(equilibria),
    }


def main() -> None:
    args = parse_args()
    local_accuracies = grid(
        args.local_accuracy_min,
        args.local_accuracy_max,
        args.local_accuracy_step,
    )
    interactions = grid(
        args.interaction_min,
        args.interaction_max,
        args.interaction_step,
    )
    migrant_accuracies = grid(
        args.migrant_accuracy_min,
        args.migrant_accuracy_max,
        args.migrant_accuracy_step,
    )
    if migrant_accuracies[0] < 0.5 or migrant_accuracies[-1] > 1.0:
        raise ValueError("migrant cue accuracy must stay in [0.5, 1]")
    if local_accuracies[0] < 0.5 or local_accuracies[-1] > 1.0:
        raise ValueError("local cue accuracy must stay in [0.5, 1]")
    if interactions[0] < 0.0:
        raise ValueError("interaction strength must be non-negative")

    rows = [
        run_historical_path(
            local_accuracy,
            interaction,
            migrant_accuracies,
            prior_early=args.prior_early,
        )
        for local_accuracy in local_accuracies
        for interaction in interactions
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    eligible = [row for row in rows if row["baseline_profile"] == "follow_cue|follow_cue|follow_cue"]
    cascade = [row for row in eligible if row["resident_cascade"]]
    hysteresis = [row for row in eligible if row["hysteresis"]]
    inefficient = [row for row in eligible if row["inefficient_hysteresis"]]

    phase_counts: dict[str, int] = {}
    for row in rows:
        phase = str(row["phase"])
        phase_counts[phase] = phase_counts.get(phase, 0) + 1

    summary = {
        "model": "payoff_b_three_player_bayesian_phase_diagram_v1",
        "status": "synthetic robustness map",
        "grid": {
            "prior_early": args.prior_early,
            "local_accuracy_values": len(local_accuracies),
            "interaction_values": len(interactions),
            "migrant_accuracy_values_per_path": len(migrant_accuracies),
            "cells": len(rows),
        },
        "eligible_high_information_cells": len(eligible),
        "resident_cascade_cells": len(cascade),
        "hysteresis_cells": len(hysteresis),
        "inefficient_information_hysteresis_cells": len(inefficient),
        "phase_counts": phase_counts,
        "claim_rule": (
            "promote only cells that start in all-following coordination, "
            "show resident cascade under migrant information loss, fail to "
            "return after information recovery, and retain a higher-joint-payoff "
            "pure equilibrium at full recovered information"
        ),
        "claim_boundary": [
            "synthetic finite Bayesian game, not a calibrated natural network",
            "sequential best response is the declared historical accessibility rule",
            "grid prevalence is design prevalence, not a natural frequency",
            "cue accuracy is a mechanistic information parameter",
        ],
    }
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
