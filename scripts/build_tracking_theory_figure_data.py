#!/usr/bin/env python3
"""Build figure-ready data for the frozen PAYOFF-B tracking-theory manuscript.

The builder is intentionally source-conservative. It reads only the five
2026-09-20 synthetic receipts licensed by the tracking-theory claim freeze.
It does not read later empirical phase-retention results.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

TRACKING = DATA / "payoff_b_tracking_synthetic_receipt_20260920.json"
MOVING = DATA / "payoff_b_moving_landscape_receipt_20260920.json"
CONNECTIVITY = DATA / "payoff_b_2d_connectivity_receipt_20260920.json"
CLOSED_LOOP = DATA / "payoff_b_closed_loop_tracking_receipt_20260920.json"
FEEDBACK = DATA / "payoff_b_movement_feedback_landscape_receipt_20260920.json"

FROZEN_DATE = "2026-09-20"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require_frozen(receipt: dict, path: Path) -> None:
    observed = receipt.get("frozen_date")
    if observed != FROZEN_DATE:
        raise ValueError(
            f"{path.name} has frozen_date={observed!r}; expected {FROZEN_DATE}"
        )


def build_figure_data() -> dict:
    tracking = load_json(TRACKING)
    moving = load_json(MOVING)
    connectivity = load_json(CONNECTIVITY)
    closed_loop = load_json(CLOSED_LOOP)
    feedback = load_json(FEEDBACK)

    for receipt, path in (
        (tracking, TRACKING),
        (moving, MOVING),
        (connectivity, CONNECTIVITY),
        (closed_loop, CLOSED_LOOP),
        (feedback, FEEDBACK),
    ):
        require_frozen(receipt, path)

    replication = tracking["demographic_stress"]["replication_128_replicates"]
    drift = tracking["drift_escape"]["beta_5"]
    gate = connectivity["coevolution"]["direct_gate"]
    fine = connectivity["coevolution"]["fine_mutation_step_0_1"]

    return {
        "status": "payoff_b_tracking_theory_figure_data",
        "frozen_date": FROZEN_DATE,
        "manuscript": "manuscript/PAYOFF_B_TRACKING_THEORY_V1.md",
        "source_policy": (
            "five frozen 2026-09-20 synthetic receipts only; "
            "post-2026-09-20 empirical lambda results excluded"
        ),
        "figure_2_temporal_bypass": {
            "one_dimensional_frontier": moving["persistence_frontier"]["brackets"],
            "frontier_outcome": moving["persistence_frontier"]["frontier_outcome"],
            "two_dimensional_zmax4_sequence": connectivity[
                "zigzag_temporal_buffering"
            ]["canonical_zmax4_sequence"],
            "zigzag_penalties": connectivity["zigzag_temporal_buffering"][
                "mean_growth_penalty_open_minus_zigzag"
            ],
            "zigzag_penalty_reduction": connectivity[
                "zigzag_temporal_buffering"
            ]["penalty_magnitude_reduction_0_to_4"],
            "anisotropy_reductions": connectivity["anisotropic_movement"][
                "penalty_magnitude_reduction_z0_to_z4"
            ],
        },
        "figure_3_coordination_gate": {
            "positive_interaction_cells": fine["positive_interaction_cells"],
            "barriers": fine["barriers"],
            "persistence_rescues": fine["persistence_rescues"],
            "no_interaction_coarse": connectivity["coevolution"][
                "coarse_mutation_step_0_2"
            ]["interaction_0"],
            "direct_gate": gate,
            "overlap_sensitivity": connectivity[
                "distribution_overlap_sensitivity"
            ],
        },
        "figure_4_synchronization": connectivity["partner_asymmetry"],
        "figure_5_demography_and_drift": {
            "barrier_cells": tracking["demographic_stress"]["barrier_cells"],
            "replication_128": {
                "max_persistence_gain": replication["max_persistence_gain"],
                "mean_persistence_gain_all_barrier_cells": replication[
                    "mean_persistence_gain_all_barrier_cells"
                ],
                "visibility_examples": replication["visibility_examples"],
                "local_persistence_bin_0_3_to_0_7": replication[
                    "local_persistence_bin_0_3_to_0_7"
                ],
                "local_persistence_bin_0_9_to_1_0": replication[
                    "local_persistence_bin_0_9_to_1_0"
                ],
            },
            "pilot_ge_0_10": tracking["demographic_stress"][
                "pilot_32_replicates"
            ]["barrier_cells_gain_ge_0_10"],
            "replication_ge_0_10": replication[
                "barrier_cells_gain_ge_0_10"
            ],
            "drift_beta_5": [
                {
                    "N": int(key.removeprefix("N_")),
                    **value,
                }
                for key, value in drift.items()
            ],
            "drift_retained_interpretation": tracking["drift_escape"][
                "retained_interpretation"
            ],
        },
        "figure_6_local_null_vs_landscape": {
            "closed_loop_exact": closed_loop["exact_results"],
            "closed_loop_equal_cost_witness": closed_loop[
                "equal_cost_witness"
            ],
            "explicit_feedback_design": feedback["design"],
            "high_forcing_persistence": feedback[
                "high_forcing_persistence"
            ],
            "fixed_gain_1_6": feedback["fixed_gain_1_6"],
            "within_persistent_controller_benefit": feedback[
                "within_persistent_controller_benefit"
            ],
        },
        "source_receipts": [
            str(path.relative_to(ROOT))
            for path in (
                TRACKING,
                MOVING,
                CONNECTIVITY,
                CLOSED_LOOP,
                FEEDBACK,
            )
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/payoff_b_tracking_theory_figure_data.json"),
    )
    args = parser.parse_args()

    payload = build_figure_data()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(
        "tracking_theory_figure_data "
        f"barriers={payload['figure_3_coordination_gate']['barriers']} "
        f"rescues={payload['figure_3_coordination_gate']['persistence_rescues']} "
        f"frozen_date={payload['frozen_date']}"
    )


if __name__ == "__main__":
    main()
