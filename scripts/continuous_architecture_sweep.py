#!/usr/bin/env python3
"""Sweep ecological mismatch feedback across the continuous architecture transition."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.continuous_architecture import (
    branching_regime,
    endpoint_subgame_parameters,
    global_potential_optimum,
    no_feedback_optimum,
    no_feedback_regime,
    two_function_coupling_for_recovery,
)


def frange(start: float, stop: float, step: float):
    if step <= 0.0:
        raise ValueError("step must be positive")
    value = start
    while value <= stop + step * 1e-9:
        yield value
        value += step


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-recovery", type=float, default=2.0)
    parser.add_argument("--linear-cost-slope", type=float, default=0.4)
    parser.add_argument("--curvature", type=float, default=1.0)
    parser.add_argument("--gamma-min", type=float, default=-1.2)
    parser.add_argument("--gamma-max", type=float, default=0.6)
    parser.add_argument("--step", type=float, default=0.1)
    parser.add_argument("--two-function-a", type=float, default=2.0)
    parser.add_argument("--two-function-b", type=float, default=3.0)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    L = args.max_recovery
    r0 = no_feedback_optimum(
        L, args.linear_cost_slope, args.curvature
    )
    base_regime = no_feedback_regime(
        L, args.linear_cost_slope, args.curvature
    )

    if 0.0 < r0 <= L:
        lambda0 = two_function_coupling_for_recovery(
            args.two_function_a,
            args.two_function_b,
            L,
            r0,
        )
    else:
        lambda0 = float("inf")

    rows = []
    for gamma in frange(args.gamma_min, args.gamma_max, args.step):
        optimum = global_potential_optimum(
            L,
            args.linear_cost_slope,
            args.curvature,
            gamma,
        )
        phi_endpoint, eta_endpoint = endpoint_subgame_parameters(
            L,
            args.linear_cost_slope,
            args.curvature,
            gamma,
        )
        rows.append(
            {
                "gamma": gamma,
                "branching_threshold": -0.5 * args.curvature,
                "branching_regime": branching_regime(args.curvature, gamma),
                "no_feedback_regime": base_regime,
                "no_feedback_recovery": r0,
                "no_feedback_two_function_coupling": lambda0,
                "global_regime": optimum["regime"],
                "mean_recovery": optimum["mean_recovery"],
                "variance_recovery": optimum["variance_recovery"],
                "endpoint_d_frequency": optimum["endpoint_d_frequency"],
                "potential": optimum["potential"],
                "endpoint_phi": phi_endpoint,
                "endpoint_eta": eta_endpoint,
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {args.output}")
    print(f"branching threshold gamma={-0.5 * args.curvature:.12g}")
    print(f"intrinsic recovery r0={r0:.12g}")


if __name__ == "__main__":
    main()
