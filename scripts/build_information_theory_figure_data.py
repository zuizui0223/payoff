#!/usr/bin/env python3
"""Build frozen figure-data tables for PAYOFF-B information theory V2."""

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
from src.endogenous_information_timing import (
    closed_form_information_threshold,
    information_value,
)
from src.information_uptake_network import (
    complete_graph_weights,
    evaluate_network_uptake,
)
from src.shared_cue_deadline_network import (
    canonical_shared_cue_deadline_game,
    sequential_shared_cue_best_response,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/payoff_b_information_figure_data"),
    )
    return p.parse_args()


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def panel_a_deadline_thresholds():
    low = closed_form_information_threshold(
        0.40, 2.0, 1.0, delay_cost=0.10
    )
    high = closed_form_information_threshold(
        0.40, 2.0, 1.0, delay_cost=0.30
    )
    rows = []
    for step in range(101):
        q = 0.50 + 0.005 * step
        value = information_value(0.40, q, 2.0, 1.0)
        rows.append(
            {
                "cue_accuracy": q,
                "information_value": value,
                "low_delay": 0.10,
                "high_delay": 0.30,
                "low_actor_uses_cue": value > 0.10,
                "high_actor_uses_cue": value > 0.30,
                "actionable_threshold": low.actionable_cue_accuracy,
                "low_wait_threshold": low.wait_cue_accuracy,
                "high_wait_threshold": high.wait_cue_accuracy,
            }
        )
    return rows


def panel_b_complete_network():
    # Twenty otherwise identical actors with a broad deterministic deadline
    # distribution entirely below the perfect-information value R0=.4.
    delays = tuple(0.01 + (0.38 / 19.0) * i for i in range(20))
    weights = complete_graph_weights(20)
    rows = []
    for step in range(101):
        q = 0.50 + 0.005 * step
        state = evaluate_network_uptake(
            prior_early=0.40,
            false_early_cost=2.0,
            missed_early_cost=1.0,
            cue_accuracy=q,
            delay_costs=delays,
            weights=weights,
        )
        rows.append(
            {
                "cue_accuracy": q,
                "informed_count": state.informed_count,
                "informed_fraction": state.informed_fraction,
                "cut_fraction": state.cut_fraction,
                "conditional_action_mismatch_probability": (
                    state.conditional_action_mismatch_probability
                ),
                "expected_edge_mismatch_fraction": (
                    state.expected_edge_mismatch_fraction
                ),
            }
        )
    return rows


def _chain_weights(n):
    rows = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n - 1):
        rows[i][i + 1] = 1.0
        rows[i + 1][i] = 1.0
    return tuple(tuple(row) for row in rows)


def panel_c_deadline_placement():
    weights = _chain_weights(5)
    configurations = {
        "peripheral_first": (0.05, 0.10, 0.20, 0.30, 0.35),
        "central_first": (0.30, 0.20, 0.05, 0.10, 0.35),
    }
    rows = []
    for label, delays in configurations.items():
        for step in range(101):
            q = 0.50 + 0.005 * step
            state = evaluate_network_uptake(
                prior_early=0.40,
                false_early_cost=2.0,
                missed_early_cost=1.0,
                cue_accuracy=q,
                delay_costs=delays,
                weights=weights,
            )
            rows.append(
                {
                    "configuration": label,
                    "cue_accuracy": q,
                    "informed_count": state.informed_count,
                    "cut_fraction": state.cut_fraction,
                    "expected_edge_mismatch_fraction": (
                        state.expected_edge_mismatch_fraction
                    ),
                }
            )
    return rows


def _profile_label(profile):
    labels = {
        ALWAYS_LATE: "late",
        FOLLOW_CUE: "follow",
        (1, 0): "invert",
        (1, 1): "early",
    }
    return "|".join(labels[p] for p in profile)


def panel_d_recovery_hysteresis():
    informed = (FOLLOW_CUE, FOLLOW_CUE, FOLLOW_CUE)
    profile = informed
    rows = []

    for step in range(100, 49, -1):
        q = step / 100.0
        game = canonical_shared_cue_deadline_game(
            q,
            interaction_topology="chain",
        )
        path = sequential_shared_cue_best_response(game, profile)
        profile = path[-1].profile
        rows.append(
            {
                "direction": "degradation",
                "cue_accuracy": q,
                "profile": _profile_label(profile),
                "joint_payoff": path[-1].joint_payoff,
                "all_follow": profile == informed,
            }
        )

    for step in range(50, 101):
        q = step / 100.0
        game = canonical_shared_cue_deadline_game(
            q,
            interaction_topology="chain",
        )
        path = sequential_shared_cue_best_response(game, profile)
        profile = path[-1].profile
        rows.append(
            {
                "direction": "recovery",
                "cue_accuracy": q,
                "profile": _profile_label(profile),
                "joint_payoff": path[-1].joint_payoff,
                "all_follow": profile == informed,
            }
        )
    return rows


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    panels = {
        "panel_a_deadline_thresholds": panel_a_deadline_thresholds(),
        "panel_b_complete_network": panel_b_complete_network(),
        "panel_c_deadline_placement": panel_c_deadline_placement(),
        "panel_d_recovery_hysteresis": panel_d_recovery_hysteresis(),
    }
    filenames = {}
    for name, rows in panels.items():
        path = args.output_dir / f"{name}.csv"
        write_csv(path, rows)
        filenames[name] = str(path)

    receipt = {
        "result_id": "payoff_b_information_theory_figure_data_v1",
        "status": "FROZEN_SYNTHETIC_FIGURE_DATA",
        "panels": {
            "A": "individual information value and exact deadline thresholds",
            "B": "complete-network information-uptake frontier and edge cut",
            "C": "same delay-cost distribution rearranged on a chain",
            "D": "shared-cue degradation and recovery hysteresis",
        },
        "canonical_exact_markers": {
            "actionable_q": 0.75,
            "low_wait_q": 0.8125,
            "high_wait_q": 0.9375,
            "all_informed_stability_q": 0.80,
            "grid_collapse_q": 0.79,
        },
        "files": filenames,
        "claim_boundary": [
            "all panels are synthetic mechanism illustrations",
            "deadline distributions and network placements are not empirical estimates",
            "natural network recovery hysteresis remains prospective",
        ],
    }
    (args.output_dir / "receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
