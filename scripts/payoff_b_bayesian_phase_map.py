#!/usr/bin/env python3
"""Map information-triggered coordination hysteresis across a declared grid.

This is a synthetic robustness map. Cell counts are design frequencies, not
estimates of natural prevalence.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.bayesian_timing_coordination import (
    ALWAYS_LATE,
    FOLLOW_CUE,
    BayesianTimingGame,
    TimingPlayer,
    policy_label,
    pure_bayesian_nash_equilibria,
    sequential_best_response,
)


FOLLOW_ALL = (FOLLOW_CUE, FOLLOW_CUE, FOLLOW_CUE)
LATE_ALL = (ALWAYS_LATE, ALWAYS_LATE, ALWAYS_LATE)


def parse_float_list(text: str) -> list[float]:
    return [float(value.strip()) for value in text.split(",") if value.strip()]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--priors", default="0.30,0.40,0.50")
    p.add_argument(
        "--resident-accuracies",
        default="0.80,0.90,0.95",
    )
    p.add_argument(
        "--interaction-strengths",
        default="0,0.25,0.50,0.75,1.00",
    )
    p.add_argument(
        "--migrant-false-early-costs",
        default="1.0,2.0,3.0",
    )
    p.add_argument("--migrant-missed-early-cost", type=float, default=1.0)
    p.add_argument("--accuracy-step", type=float, default=0.01)
    p.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/payoff_b_bayesian_phase_map.csv"),
    )
    p.add_argument(
        "--summary-output",
        type=Path,
        default=Path("outputs/payoff_b_bayesian_phase_map_summary.json"),
    )
    return p.parse_args()


def q_grid(step: float) -> list[float]:
    if step <= 0.0 or step > 0.5:
        raise ValueError("accuracy-step must lie in (0,0.5]")
    values = []
    q = 1.0
    while q >= 0.5 - 1e-12:
        values.append(round(q, 12))
        q -= step
    if values[-1] != 0.5:
        values.append(0.5)
    return values


def build_game(
    *,
    prior: float,
    resident_accuracy: float,
    migrant_accuracy: float,
    interaction_strength: float,
    migrant_false_early_cost: float,
    migrant_missed_early_cost: float,
) -> BayesianTimingGame:
    return BayesianTimingGame(
        prior_early=prior,
        players=(
            TimingPlayer(
                name="flower",
                cue_accuracy=resident_accuracy,
                false_early_cost=1.0,
                missed_early_cost=0.25,
                interaction_strength=interaction_strength,
            ),
            TimingPlayer(
                name="local_pollinator",
                cue_accuracy=resident_accuracy,
                false_early_cost=1.0,
                missed_early_cost=0.25,
                interaction_strength=interaction_strength,
            ),
            TimingPlayer(
                name="migrant",
                cue_accuracy=migrant_accuracy,
                false_early_cost=migrant_false_early_cost,
                missed_early_cost=migrant_missed_early_cost,
                interaction_strength=interaction_strength,
            ),
        ),
    )


def profile_text(profile) -> str:
    return "|".join(policy_label(policy) for policy in profile)


def run_cell(
    *,
    prior: float,
    resident_accuracy: float,
    interaction_strength: float,
    migrant_false_early_cost: float,
    migrant_missed_early_cost: float,
    accuracies: list[float],
) -> dict[str, object]:
    profile = FOLLOW_ALL
    baseline_follow_stable = None
    first_resident_departure_q = None
    collapse_q = None

    for q_index, q in enumerate(accuracies):
        game = build_game(
            prior=prior,
            resident_accuracy=resident_accuracy,
            migrant_accuracy=q,
            interaction_strength=interaction_strength,
            migrant_false_early_cost=migrant_false_early_cost,
            migrant_missed_early_cost=migrant_missed_early_cost,
        )
        dynamics = sequential_best_response(game, profile)
        profile = dynamics.final.profile

        if q_index == 0:
            baseline_follow_stable = profile == FOLLOW_ALL
            continue

        if baseline_follow_stable and (
            first_resident_departure_q is None
            and (
                profile[0] != FOLLOW_CUE
                or profile[1] != FOLLOW_CUE
            )
        ):
            first_resident_departure_q = q

        if (
            baseline_follow_stable
            and collapse_q is None
            and profile == LATE_ALL
        ):
            collapse_q = q

    low_profile = profile

    for q in reversed(accuracies):
        game = build_game(
            prior=prior,
            resident_accuracy=resident_accuracy,
            migrant_accuracy=q,
            interaction_strength=interaction_strength,
            migrant_false_early_cost=migrant_false_early_cost,
            migrant_missed_early_cost=migrant_missed_early_cost,
        )
        dynamics = sequential_best_response(game, profile)
        profile = dynamics.final.profile

    recovered_profile = profile
    full_game = build_game(
        prior=prior,
        resident_accuracy=resident_accuracy,
        migrant_accuracy=1.0,
        interaction_strength=interaction_strength,
        migrant_false_early_cost=migrant_false_early_cost,
        migrant_missed_early_cost=migrant_missed_early_cost,
    )
    equilibria = pure_bayesian_nash_equilibria(full_game)
    equilibrium_profiles = {row.profile for row in equilibria}
    follow_eval = next(
        (
            row
            for row in equilibria
            if row.profile == FOLLOW_ALL
        ),
        None,
    )
    recovered_eval = next(
        (
            row
            for row in equilibria
            if row.profile == recovered_profile
        ),
        None,
    )

    if recovered_eval is None:
        recovered_eval = sequential_best_response(
            full_game,
            recovered_profile,
        ).final

    payoff_gap = (
        None
        if follow_eval is None
        else follow_eval.joint_payoff - recovered_eval.joint_payoff
    )
    hysteresis = bool(
        baseline_follow_stable
        and recovered_profile != FOLLOW_ALL
        and FOLLOW_ALL in equilibrium_profiles
        and recovered_profile in equilibrium_profiles
        and payoff_gap is not None
        and payoff_gap > 1e-12
    )

    return {
        "prior_early": prior,
        "resident_accuracy": resident_accuracy,
        "interaction_strength": interaction_strength,
        "migrant_false_early_cost": migrant_false_early_cost,
        "migrant_missed_early_cost": migrant_missed_early_cost,
        "baseline_follow_stable_q1": bool(baseline_follow_stable),
        "first_resident_departure_q": first_resident_departure_q,
        "all_late_collapse_q": collapse_q,
        "collective_all_late_cascade": collapse_q is not None,
        "resident_cascade": first_resident_departure_q is not None,
        "low_information_profile": profile_text(low_profile),
        "recovered_profile_q1": profile_text(recovered_profile),
        "follow_all_is_bne_q1": FOLLOW_ALL in equilibrium_profiles,
        "recovered_is_bne_q1": recovered_profile in equilibrium_profiles,
        "follow_minus_recovered_joint_payoff_q1": payoff_gap,
        "hysteresis_with_better_original_equilibrium": hysteresis,
        "pure_bne_count_q1": len(equilibria),
    }


def main() -> None:
    args = parse_args()
    priors = parse_float_list(args.priors)
    resident_accuracies = parse_float_list(args.resident_accuracies)
    interactions = parse_float_list(args.interaction_strengths)
    false_costs = parse_float_list(args.migrant_false_early_costs)
    accuracies = q_grid(args.accuracy_step)

    rows = []
    for prior in priors:
        for resident_accuracy in resident_accuracies:
            for interaction_strength in interactions:
                for false_cost in false_costs:
                    rows.append(
                        run_cell(
                            prior=prior,
                            resident_accuracy=resident_accuracy,
                            interaction_strength=interaction_strength,
                            migrant_false_early_cost=false_cost,
                            migrant_missed_early_cost=(
                                args.migrant_missed_early_cost
                            ),
                            accuracies=accuracies,
                        )
                    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    positive_interaction = [
        row for row in rows
        if row["interaction_strength"] > 0.0
        and row["baseline_follow_stable_q1"]
    ]
    zero_interaction = [
        row for row in rows
        if row["interaction_strength"] == 0.0
        and row["baseline_follow_stable_q1"]
    ]
    cascade_rows = [
        row for row in positive_interaction
        if row["collective_all_late_cascade"]
    ]
    hysteresis_rows = [
        row for row in positive_interaction
        if row["hysteresis_with_better_original_equilibrium"]
    ]

    by_interaction = {}
    for interaction in interactions:
        eligible = [
            row for row in rows
            if row["interaction_strength"] == interaction
            and row["baseline_follow_stable_q1"]
        ]
        cascades = [
            row for row in eligible
            if row["collective_all_late_cascade"]
        ]
        hysteresis = [
            row for row in eligible
            if row["hysteresis_with_better_original_equilibrium"]
        ]
        by_interaction[str(interaction)] = {
            "baseline_eligible_cells": len(eligible),
            "collective_cascade_cells": len(cascades),
            "hysteresis_cells": len(hysteresis),
            "collapse_q_min": (
                min(
                    float(row["all_late_collapse_q"])
                    for row in cascades
                )
                if cascades else None
            ),
            "collapse_q_max": (
                max(
                    float(row["all_late_collapse_q"])
                    for row in cascades
                )
                if cascades else None
            ),
        }

    summary = {
        "design": {
            "priors": priors,
            "resident_accuracies": resident_accuracies,
            "interaction_strengths": interactions,
            "migrant_false_early_costs": false_costs,
            "migrant_missed_early_cost": args.migrant_missed_early_cost,
            "migrant_accuracy_grid": accuracies,
            "n_cells": len(rows),
            "n_positive_interaction_baseline_eligible_cells": len(positive_interaction),
            "n_zero_interaction_baseline_eligible_cells": len(zero_interaction),
        },
        "readout": {
            "positive_interaction_collective_cascade_cells": len(cascade_rows),
            "positive_interaction_hysteresis_cells": len(hysteresis_rows),
            "zero_interaction_information_triggered_resident_cascade_cells": sum(
                bool(row["resident_cascade"])
                for row in zero_interaction
            ),
            "zero_interaction_information_triggered_collective_cascade_cells": sum(
                bool(row["collective_all_late_cascade"])
                for row in zero_interaction
            ),
            "cascade_interaction_strengths": sorted(
                {
                    row["interaction_strength"]
                    for row in cascade_rows
                }
            ),
            "hysteresis_interaction_strengths": sorted(
                {
                    row["interaction_strength"]
                    for row in hysteresis_rows
                }
            ),
            "collapse_q_min": (
                min(
                    float(row["all_late_collapse_q"])
                    for row in cascade_rows
                    if row["all_late_collapse_q"] is not None
                )
                if cascade_rows else None
            ),
            "collapse_q_max": (
                max(
                    float(row["all_late_collapse_q"])
                    for row in cascade_rows
                    if row["all_late_collapse_q"] is not None
                )
                if cascade_rows else None
            ),
            "by_interaction_strength": by_interaction,
        },
        "claim_boundary": [
            "information-triggered counts require all-follow to be stable at q=1 before cue degradation",
            "cell counts are frequencies in a declared synthetic grid, not natural prevalence",
            "parameter ranges are mechanism probes rather than fitted ecological values",
            "hysteresis uses sequential best response as a declared accessibility rule",
            "information and interaction effects should be tested against the zero-interaction control",
        ],
    }

    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
