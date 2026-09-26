#!/usr/bin/env python3
"""Trace cue-loss and cue-recovery hysteresis in the 3-player Bayesian game."""

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--accuracy-min", type=float, default=0.50)
    parser.add_argument("--accuracy-max", type=float, default=1.00)
    parser.add_argument("--accuracy-step", type=float, default=0.01)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/payoff_b_bayesian_hysteresis.csv"),
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=Path("outputs/payoff_b_bayesian_hysteresis_summary.json"),
    )
    return parser.parse_args()


def grid(start: float, stop: float, step: float) -> list[float]:
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


def profile_text(profile) -> str:
    return "|".join(policy_label(policy) for policy in profile)


def run_direction(
    accuracies: list[float],
    initial_profile,
    direction: str,
):
    rows: list[dict[str, object]] = []
    profile = tuple(initial_profile)

    for accuracy in accuracies:
        game = canonical_three_player_game(accuracy)
        dynamics = sequential_best_response(game, profile)
        profile = dynamics.final.profile
        equilibria = pure_bayesian_nash_equilibria(game)
        best_equilibrium = equilibria[0]

        rows.append(
            {
                "direction": direction,
                "migrant_cue_accuracy": accuracy,
                "historical_profile": profile_text(profile),
                "historical_joint_payoff": dynamics.final.joint_payoff,
                "best_equilibrium_profile": profile_text(
                    best_equilibrium.profile
                ),
                "best_equilibrium_joint_payoff": (
                    best_equilibrium.joint_payoff
                ),
                "history_lock_loss": (
                    best_equilibrium.joint_payoff
                    - dynamics.final.joint_payoff
                ),
                "pure_bne_count": len(equilibria),
            }
        )
    return rows, profile


def main() -> None:
    args = parse_args()
    ascending = grid(
        args.accuracy_min,
        args.accuracy_max,
        args.accuracy_step,
    )
    descending = list(reversed(ascending))

    follow_all = (FOLLOW_CUE, FOLLOW_CUE, FOLLOW_CUE)
    down_rows, low_profile = run_direction(
        descending,
        follow_all,
        "degrading",
    )
    up_rows, recovered_profile = run_direction(
        ascending,
        low_profile,
        "recovering",
    )
    rows = down_rows + up_rows

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    collapse_row = next(
        (
            row
            for row in down_rows
            if row["historical_profile"]
            == "always_late|always_late|always_late"
        ),
        None,
    )
    full_recovery = up_rows[-1]

    summary = {
        "model": "payoff_b_three_player_bayesian_timing_game_v1",
        "status": "synthetic mechanism witness",
        "degradation_collapse_accuracy": (
            None if collapse_row is None
            else collapse_row["migrant_cue_accuracy"]
        ),
        "full_recovery_historical_profile": (
            full_recovery["historical_profile"]
        ),
        "full_recovery_best_equilibrium_profile": (
            full_recovery["best_equilibrium_profile"]
        ),
        "full_recovery_history_lock_loss": (
            full_recovery["history_lock_loss"]
        ),
        "final_recovered_profile": profile_text(recovered_profile),
        "claim_boundary": [
            "synthetic Bayesian coordination game, not a calibrated food web",
            "best-response update order is a declared accessibility rule",
            "hysteresis is shown for the canonical parameter witness, not claimed universal",
            "cue accuracy is not yet estimated for a named migrant system",
        ],
    }
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
