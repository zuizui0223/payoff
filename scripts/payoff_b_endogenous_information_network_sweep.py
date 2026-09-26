#!/usr/bin/env python3
"""Sweep information quality x interaction coupling in the unified PAYOFF-B game."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.endogenous_information_network import (
    all_commit_late_profile,
    all_wait_follow_profile,
    canonical_endogenous_information_network,
    evaluate_information_network,
    is_strict_information_network_equilibrium,
    profile_labels,
    sequential_information_network_best_response,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--topology",
        choices=("complete", "chain", "migrant_star"),
        default="complete",
    )
    p.add_argument("--interaction-min", type=float, default=0.0)
    p.add_argument("--interaction-max", type=float, default=1.0)
    p.add_argument("--interaction-step", type=float, default=0.01)
    p.add_argument("--cue-min", type=float, default=0.50)
    p.add_argument("--cue-max", type=float, default=1.00)
    p.add_argument("--cue-step", type=float, default=0.01)
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_endogenous_information_network_sweep.csv"
        ),
    )
    p.add_argument(
        "--summary-output",
        type=Path,
        default=Path(
            "outputs/payoff_b_endogenous_information_network_summary.json"
        ),
    )
    return p.parse_args()


def grid(start: float, stop: float, step: float) -> list[float]:
    if step <= 0.0:
        raise ValueError("step must be positive")
    values: list[float] = []
    value = start
    while value <= stop + 1e-12:
        values.append(round(value, 12))
        value += step
    return values


def main():
    args = parse_args()
    interaction_values = grid(
        args.interaction_min,
        args.interaction_max,
        args.interaction_step,
    )
    cue_values = grid(
        args.cue_min,
        args.cue_max,
        args.cue_step,
    )

    late = all_commit_late_profile()
    follow = all_wait_follow_profile()
    rows = []
    interaction_rows = []

    for interaction in interaction_values:
        upward_profile = late
        upward = []
        for cue in cue_values:
            game = canonical_endogenous_information_network(
                cue,
                interaction_strength=interaction,
                interaction_topology=args.topology,
            )
            result = sequential_information_network_best_response(
                game,
                upward_profile,
            )
            upward_profile = result.final.profile
            upward.append((cue, game, result.final))

        downward_profile = follow
        downward = []
        for cue in reversed(cue_values):
            game = canonical_endogenous_information_network(
                cue,
                interaction_strength=interaction,
                interaction_topology=args.topology,
            )
            result = sequential_information_network_best_response(
                game,
                downward_profile,
            )
            downward_profile = result.final.profile
            downward.append((cue, game, result.final))

        downward_by_cue = {
            cue: evaluation
            for cue, _, evaluation in downward
        }

        asynchronous_up_cues = []
        maladaptive_lock_cues = []

        for cue, game, up_eval in upward:
            down_eval = downward_by_cue[cue]
            up_labels = profile_labels(up_eval.profile)
            down_labels = profile_labels(down_eval.profile)

            is_up_partial = (
                up_eval.profile != late
                and up_eval.profile != follow
            )
            if is_up_partial:
                asynchronous_up_cues.append(cue)

            late_eval = evaluate_information_network(game, late)
            follow_eval = evaluate_information_network(game, follow)
            late_strict = is_strict_information_network_equilibrium(
                game,
                late,
            )
            follow_strict = is_strict_information_network_equilibrium(
                game,
                follow,
            )
            maladaptive_lock = (
                up_eval.profile == late
                and late_strict
                and follow_strict
                and follow_eval.joint_payoff
                > late_eval.joint_payoff + 1e-12
            )
            if maladaptive_lock:
                maladaptive_lock_cues.append(cue)

            rows.append(
                {
                    "topology": args.topology,
                    "interaction_strength": interaction,
                    "cue_accuracy": cue,
                    "up_profile": "|".join(up_labels),
                    "down_profile": "|".join(down_labels),
                    "up_joint_payoff": up_eval.joint_payoff,
                    "down_joint_payoff": down_eval.joint_payoff,
                    "path_dependent": (
                        up_eval.profile != down_eval.profile
                    ),
                    "up_asynchronous": is_up_partial,
                    "all_late_strict": late_strict,
                    "all_follow_strict": follow_strict,
                    "all_late_joint_payoff": late_eval.joint_payoff,
                    "all_follow_joint_payoff": follow_eval.joint_payoff,
                    "maladaptive_information_lock": maladaptive_lock,
                }
            )

        up_full = next(
            (
                cue
                for cue, _, evaluation in upward
                if evaluation.profile == follow
            ),
            None,
        )
        down_late = next(
            (
                cue
                for cue, _, evaluation in downward
                if evaluation.profile == late
            ),
            None,
        )

        perfect_game = canonical_endogenous_information_network(
            1.0,
            interaction_strength=interaction,
            interaction_topology=args.topology,
        )
        perfect_up = next(
            evaluation
            for cue, _, evaluation in upward
            if abs(cue - 1.0) < 1e-12
        )
        perfect_late = evaluate_information_network(
            perfect_game,
            late,
        )
        perfect_follow = evaluate_information_network(
            perfect_game,
            follow,
        )
        perfect_information_trap = (
            perfect_up.profile == late
            and is_strict_information_network_equilibrium(
                perfect_game,
                late,
            )
            and is_strict_information_network_equilibrium(
                perfect_game,
                follow,
            )
            and perfect_follow.joint_payoff
            > perfect_late.joint_payoff + 1e-12
        )

        interaction_rows.append(
            {
                "interaction_strength": interaction,
                "up_full_follow_threshold": up_full,
                "down_full_late_threshold": down_late,
                "hysteresis_width": (
                    None
                    if up_full is None or down_late is None
                    else up_full - down_late
                ),
                "asynchronous_up_cells": len(asynchronous_up_cues),
                "asynchronous_up_min": (
                    min(asynchronous_up_cues)
                    if asynchronous_up_cues else None
                ),
                "asynchronous_up_max": (
                    max(asynchronous_up_cues)
                    if asynchronous_up_cues else None
                ),
                "maladaptive_lock_cells": len(maladaptive_lock_cues),
                "maladaptive_lock_min": (
                    min(maladaptive_lock_cues)
                    if maladaptive_lock_cues else None
                ),
                "maladaptive_lock_max": (
                    max(maladaptive_lock_cues)
                    if maladaptive_lock_cues else None
                ),
                "perfect_information_trap": perfect_information_trap,
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    first_no_async = next(
        (
            row["interaction_strength"]
            for row in interaction_rows
            if row["asynchronous_up_cells"] == 0
        ),
        None,
    )
    first_lock = next(
        (
            row["interaction_strength"]
            for row in interaction_rows
            if row["maladaptive_lock_cells"] > 0
        ),
        None,
    )
    first_perfect_trap = next(
        (
            row["interaction_strength"]
            for row in interaction_rows
            if row["perfect_information_trap"]
        ),
        None,
    )

    def row_at(value):
        return next(
            row
            for row in interaction_rows
            if abs(row["interaction_strength"] - value) < 1e-12
        )

    summary = {
        "model": "payoff_b_endogenous_information_network_v1",
        "status": "exact finite-game sweep",
        "topology": args.topology,
        "grid": {
            "interaction_values": len(interaction_values),
            "cue_values": len(cue_values),
            "cells": len(rows),
        },
        "canonical_delay_costs": {
            "migrant": 0.30,
            "resident_partner": 0.10,
            "resource": 0.20,
        },
        "transition_thresholds_on_sampled_grid": {
            "first_interaction_with_no_asynchronous_upward_states": (
                first_no_async
            ),
            "first_interaction_with_maladaptive_information_lock": (
                first_lock
            ),
            "first_interaction_with_perfect_information_trap": (
                first_perfect_trap
            ),
        },
        "selected_interactions": {
            "0.00": row_at(0.0),
            "0.30": row_at(0.30),
            "0.50": row_at(0.50),
            "0.75": row_at(0.75),
            "1.00": row_at(1.0),
        },
        "interpretation": [
            "weak coupling permits asynchronous information uptake and transient mismatch",
            "intermediate coupling synchronizes uptake but creates distinct up/down transition thresholds",
            "stronger coupling creates a strict lower-payoff all-commit basin while an informed all-follow equilibrium is available",
            "at sufficiently strong coupling the low-information basin persists even when cue accuracy reaches one"
        ],
        "claim_boundary": [
            "interaction thresholds are values in the declared synthetic payoff parameterization, not natural constants",
            "delay costs are illustrative opportunity costs",
            "cue accuracy is an abstract information-quality coordinate",
            "the sweep demonstrates an exact finite-game mechanism, not a natural frequency"
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
