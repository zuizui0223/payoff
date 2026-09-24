#!/usr/bin/env python3
"""Sweep the exact closed-loop movement--phenology tracking phase diagram."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.closed_loop_tracking import (
    phenology_rate_to_feedback_gain,
    simulate_closed_loop_tracking,
    unconstrained_optimal_feedback,
)


def parse_float_list(value: str) -> list[float]:
    values = [
        float(item.strip())
        for item in value.split(",")
        if item.strip()
    ]
    if not values:
        raise argparse.ArgumentTypeError(
            "expected at least one comma-separated number"
        )
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--residual-forcings",
        type=parse_float_list,
        default=parse_float_list("0.05,0.1,0.2"),
    )
    parser.add_argument(
        "--movement-feedback-gains",
        type=parse_float_list,
        default=parse_float_list("0,0.25,0.5,0.75,1,1.25"),
    )
    parser.add_argument(
        "--phenology-rates",
        type=parse_float_list,
        default=parse_float_list("0,0.25,0.5,1,2"),
    )
    parser.add_argument("--mismatch-strength", type=float, default=1.0)
    parser.add_argument("--movement-cost", type=float, default=1.0)
    parser.add_argument("--phenology-cost", type=float, default=1.0)
    parser.add_argument("--initial-mismatch", type=float, default=0.0)
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--burn-in", type=int, default=50)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/closed_loop_tracking_phase.csv"
        ),
    )
    parser.add_argument(
        "--optima-output",
        type=Path,
        default=Path(
            "outputs/closed_loop_tracking_optima.csv"
        ),
    )
    args = parser.parse_args()

    rows = []
    for residual_forcing in args.residual_forcings:
        for movement_gain in args.movement_feedback_gains:
            for phenology_rate in args.phenology_rates:
                phenology_gain = phenology_rate_to_feedback_gain(
                    phenology_rate
                )
                result = simulate_closed_loop_tracking(
                    residual_forcing=residual_forcing,
                    movement_feedback_gain=movement_gain,
                    phenology_feedback_gain=phenology_gain,
                    initial_mismatch=args.initial_mismatch,
                    steps=args.steps,
                    burn_in=args.burn_in,
                )
                if (
                    result.stable
                    and result.theoretical_equilibrium_mismatch
                    is not None
                ):
                    steady_objective = (
                        0.5
                        * args.mismatch_strength
                        * result.theoretical_equilibrium_mismatch
                        * result.theoretical_equilibrium_mismatch
                        + 0.5
                        * args.movement_cost
                        * movement_gain
                        * movement_gain
                        + 0.5
                        * args.phenology_cost
                        * phenology_gain
                        * phenology_gain
                    )
                else:
                    steady_objective = None

                total = movement_gain + phenology_gain
                if total <= 0.0:
                    allocation = "none"
                elif movement_gain / total >= 2.0 / 3.0:
                    allocation = "movement"
                elif movement_gain / total <= 1.0 / 3.0:
                    allocation = "phenology"
                else:
                    allocation = "mixed"

                rows.append(
                    {
                        "residual_forcing": residual_forcing,
                        "movement_feedback_gain": movement_gain,
                        "phenology_rate": phenology_rate,
                        "phenology_feedback_gain": phenology_gain,
                        "total_feedback_gain": total,
                        "allocation": allocation,
                        "stability_class": result.stability_class,
                        "stable": int(result.stable),
                        "multiplier": result.multiplier,
                        "equilibrium_mismatch": (
                            result.theoretical_equilibrium_mismatch
                        ),
                        "final_mismatch": result.final_mismatch,
                        "rms_mismatch": result.rms_mismatch,
                        "steady_objective": steady_objective,
                    }
                )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]) if rows else [],
        )
        writer.writeheader()
        writer.writerows(rows)

    optima = []
    for residual_forcing in args.residual_forcings:
        optimum = unconstrained_optimal_feedback(
            residual_forcing=residual_forcing,
            mismatch_strength=args.mismatch_strength,
            movement_cost=args.movement_cost,
            phenology_cost=args.phenology_cost,
        )
        optima.append(
            {
                "residual_forcing": residual_forcing,
                "mismatch_strength": args.mismatch_strength,
                "movement_cost": args.movement_cost,
                "phenology_cost": args.phenology_cost,
                "effective_feedback_cost": (
                    optimum.effective_feedback_cost
                ),
                "total_feedback_gain": (
                    optimum.total_feedback_gain
                ),
                "movement_feedback_gain": (
                    optimum.movement_feedback_gain
                ),
                "phenology_feedback_gain": (
                    optimum.phenology_feedback_gain
                ),
                "equilibrium_mismatch": (
                    optimum.equilibrium_mismatch
                ),
                "objective_value": optimum.objective_value,
                "stability_feasible": int(
                    optimum.stability_feasible
                ),
                "phenology_fraction_feasible": int(
                    optimum.phenology_fraction_feasible
                ),
            }
        )

    args.optima_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with args.optima_output.open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(optima[0]) if optima else [],
        )
        writer.writeheader()
        writer.writerows(optima)

    counts: dict[str, int] = {}
    for row in rows:
        label = str(row["stability_class"])
        counts[label] = counts.get(label, 0) + 1

    print(
        f"{args.output} cells={len(rows)} "
        + " ".join(
            f"{name}={counts[name]}"
            for name in sorted(counts)
        )
    )
    for row in optima:
        print(
            "closed_loop_optimum "
            f"forcing={row['residual_forcing']} "
            f"K={row['total_feedback_gain']:.12g} "
            f"q_m={row['movement_feedback_gain']:.12g} "
            f"q_h={row['phenology_feedback_gain']:.12g} "
            f"e_star={row['equilibrium_mismatch']:.12g} "
            f"stable={row['stability_feasible']} "
            f"phenology_feasible={row['phenology_fraction_feasible']}"
        )


if __name__ == "__main__":
    main()
