#!/usr/bin/env python3
"""Trace shared-cue information-use collapse and recovery in PAYOFF-B."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.bayesian_timing_coordination import ALWAYS_LATE, FOLLOW_CUE
from src.shared_cue_deadline_network import (
    canonical_shared_cue_deadline_game,
    evaluate_shared_cue_profile,
    perfect_information_coordination_trap,
    sequential_shared_cue_best_response,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/payoff_b_shared_cue_deadline_hysteresis.json"),
    )
    p.add_argument(
        "--trace-output",
        type=Path,
        default=Path("outputs/payoff_b_shared_cue_deadline_trace.csv"),
    )
    return p.parse_args()


def label(profile):
    labels = {
        ALWAYS_LATE: "late",
        FOLLOW_CUE: "follow",
        (1, 0): "invert",
        (1, 1): "early",
    }
    return "|".join(labels[policy] for policy in profile)


def trace_topology(topology: str):
    informed = (FOLLOW_CUE, FOLLOW_CUE, FOLLOW_CUE)
    old = (ALWAYS_LATE, ALWAYS_LATE, ALWAYS_LATE)
    rows = []

    profile = informed
    collapse_q = None
    for step in range(50, -1, -1):
        q = round(0.50 + 0.01 * step, 2)
        game = canonical_shared_cue_deadline_game(
            q,
            interaction_topology=topology,
        )
        path = sequential_shared_cue_best_response(game, profile)
        profile = path[-1].profile
        if collapse_q is None and profile == old:
            collapse_q = q
        rows.append(
            {
                "topology": topology,
                "direction": "degradation",
                "cue_accuracy": q,
                "profile": label(profile),
                "joint_payoff": path[-1].joint_payoff,
            }
        )

    low_profile = profile
    recovery_q = None
    for step in range(51):
        q = round(0.50 + 0.01 * step, 2)
        game = canonical_shared_cue_deadline_game(
            q,
            interaction_topology=topology,
        )
        path = sequential_shared_cue_best_response(game, profile)
        profile = path[-1].profile
        if recovery_q is None and profile == informed:
            recovery_q = q
        rows.append(
            {
                "topology": topology,
                "direction": "recovery",
                "cue_accuracy": q,
                "profile": label(profile),
                "joint_payoff": path[-1].joint_payoff,
            }
        )

    perfect_game = canonical_shared_cue_deadline_game(
        1.0,
        interaction_topology=topology,
    )
    diagnostic = perfect_information_coordination_trap(perfect_game)
    old_eval = evaluate_shared_cue_profile(perfect_game, old)
    informed_eval = evaluate_shared_cue_profile(perfect_game, informed)

    return {
        "summary": {
            "topology": topology,
            "collapse_q_on_0_01_grid": collapse_q,
            "profile_at_q_0_5": label(low_profile),
            "recovery_q_on_0_01_grid": recovery_q,
            "profile_after_full_recovery": label(profile),
            "old_joint_payoff_at_q_1": old_eval.joint_payoff,
            "informed_joint_payoff_at_q_1": informed_eval.joint_payoff,
            "joint_information_gain_at_q_1": diagnostic.joint_information_gain,
            "unilateral_information_gains_at_q_1": list(
                diagnostic.unilateral_information_gains
            ),
            "old_profile_strict_nash_at_q_1": (
                diagnostic.old_profile_is_strict_nash
            ),
            "informed_profile_strict_nash_at_q_1": (
                diagnostic.informed_profile_is_strict_nash
            ),
            "perfect_information_coordination_trap": (
                diagnostic.perfect_information_coordination_trap
            ),
            "minimum_interaction_for_bistability": list(
                diagnostic.minimum_interaction_for_bistability
            ),
        },
        "rows": rows,
    }


def main():
    args = parse_args()
    all_rows = []
    summaries = []
    for topology in ("complete", "chain", "migrant_star"):
        result = trace_topology(topology)
        summaries.append(result["summary"])
        all_rows.extend(result["rows"])

    args.trace_output.parent.mkdir(parents=True, exist_ok=True)
    with args.trace_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_rows[0]))
        writer.writeheader()
        writer.writerows(all_rows)

    result = {
        "result_id": "payoff_b_shared_cue_deadline_hysteresis_v1",
        "status": "EXACT_FINITE_GAME_TRACE",
        "canonical_parameters": {
            "prior_early": 0.40,
            "player_information_costs": [0.05, 0.10, 0.30],
            "interaction_strength": 0.50,
            "cue_path": "1.00 down to 0.50 and back to 1.00 by 0.01",
        },
        "topology_results": summaries,
        "main_inference": (
            "a temporary decline in shared cue reliability can collapse "
            "coordinated information use; after collapse, restoring the cue "
            "to perfect accuracy need not restore information use even though "
            "the all-informed profile has higher joint payoff"
        ),
        "claim_boundary": [
            "synthetic shared-cue finite game, not a calibrated natural network",
            "the canonical interaction strengths and information costs are illustrative",
            "the topology-independent canonical trap concerns symmetric all-old/all-informed profiles; topology-dependent memory in heterogeneous private-cue games remains a separate result",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
