#!/usr/bin/env python3
"""Map act-now versus wait-for-information regimes in PAYOFF-B."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.endogenous_information_timing import (
    InformationTimingScenario,
    evaluate_information_timing,
    information_value,
    sex_specific_information_access,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--prior-early", type=float, default=0.40)
    p.add_argument("--false-early-cost", type=float, default=2.0)
    p.add_argument("--missed-early-cost", type=float, default=1.0)
    p.add_argument("--partner-externality", type=float, default=1.0)
    p.add_argument("--cue-min", type=float, default=0.50)
    p.add_argument("--cue-max", type=float, default=1.00)
    p.add_argument("--cue-step", type=float, default=0.01)
    p.add_argument("--delay-min", type=float, default=0.00)
    p.add_argument("--delay-max", type=float, default=0.80)
    p.add_argument("--delay-step", type=float, default=0.01)
    p.add_argument("--early-sex-delay", type=float, default=0.30)
    p.add_argument("--late-sex-delay", type=float, default=0.10)
    p.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/payoff_b_information_timing_phase.csv"),
    )
    p.add_argument(
        "--summary-output",
        type=Path,
        default=Path("outputs/payoff_b_information_timing_summary.json"),
    )
    return p.parse_args()


def grid(start, stop, step):
    if step <= 0:
        raise ValueError("step must be positive")
    values = []
    value = start
    while value <= stop + 1e-12:
        values.append(round(value, 12))
        value += step
    return values


def main():
    args = parse_args()
    rows = []
    cue_values = grid(args.cue_min, args.cue_max, args.cue_step)
    delay_values = grid(args.delay_min, args.delay_max, args.delay_step)

    for cue in cue_values:
        scenario = InformationTimingScenario(
            prior_early=args.prior_early,
            cue_accuracy_after_wait=cue,
            false_early_cost=args.false_early_cost,
            missed_early_cost=args.missed_early_cost,
            partner_false_early_externality=args.partner_externality,
            partner_missed_early_externality=args.partner_externality,
        )
        for delay in delay_values:
            diagnostic = evaluate_information_timing(
                scenario,
                delay_cost=delay,
            )
            if diagnostic.information_timing_wedge:
                phase = "private_commit_joint_wait"
            elif (
                diagnostic.private_decision == "wait_for_information"
                and diagnostic.joint_decision == "wait_for_information"
            ):
                phase = "both_wait"
            elif (
                diagnostic.private_decision == "commit_now"
                and diagnostic.joint_decision == "commit_now"
            ):
                phase = "both_commit"
            else:
                phase = "private_wait_joint_commit"

            rows.append(
                {
                    "cue_accuracy": cue,
                    "delay_cost": delay,
                    "private_information_value": (
                        diagnostic.private_information_value
                    ),
                    "joint_information_value": (
                        diagnostic.joint_information_value
                    ),
                    "private_decision": diagnostic.private_decision,
                    "joint_decision": diagnostic.joint_decision,
                    "phase": phase,
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    sex_rows = []
    for cue in cue_values:
        scenario = InformationTimingScenario(
            prior_early=args.prior_early,
            cue_accuracy_after_wait=cue,
            false_early_cost=args.false_early_cost,
            missed_early_cost=args.missed_early_cost,
        )
        early_decision, late_decision = sex_specific_information_access(
            scenario,
            early_sex_delay_cost=args.early_sex_delay,
            late_sex_delay_cost=args.late_sex_delay,
        )
        sex_rows.append(
            {
                "cue_accuracy": cue,
                "information_value": information_value(
                    args.prior_early,
                    cue,
                    args.false_early_cost,
                    args.missed_early_cost,
                ),
                "early_sex_decision": early_decision,
                "late_sex_decision": late_decision,
            }
        )

    first_late_wait = next(
        (
            row["cue_accuracy"]
            for row in sex_rows
            if row["late_sex_decision"] == "wait_for_information"
        ),
        None,
    )
    first_early_wait = next(
        (
            row["cue_accuracy"]
            for row in sex_rows
            if row["early_sex_decision"] == "wait_for_information"
        ),
        None,
    )
    phase_counts = {}
    for row in rows:
        phase_counts[row["phase"]] = phase_counts.get(row["phase"], 0) + 1

    summary = {
        "model": "payoff_b_endogenous_information_timing_v1",
        "status": "exact synthetic phase map",
        "parameters": {
            "prior_early": args.prior_early,
            "false_early_cost": args.false_early_cost,
            "missed_early_cost": args.missed_early_cost,
            "partner_externality": args.partner_externality,
            "early_sex_delay_cost": args.early_sex_delay,
            "late_sex_delay_cost": args.late_sex_delay,
        },
        "phase_counts": phase_counts,
        "sex_specific_information_thresholds_on_sampled_grid": {
            "late_sex_first_wait_accuracy": first_late_wait,
            "early_sex_first_wait_accuracy": first_early_wait,
        },
        "claim_boundary": [
            "delay costs are illustrative payoff units, not fitted sex-specific parameters",
            "cue accuracy is an abstract information-quality coordinate",
            "the source-backed flycatcher experiment anchors timing-dependent information availability but does not estimate this model"
        ],
    }
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
