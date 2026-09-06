#!/usr/bin/env python3
"""Generate the anti-phase temporal reciprocal-invasion phase grid."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.anti_phase_temporal import anti_phase_temporal_premium
from src.temporal_reciprocal_game import (
    classify_reciprocal_temporal_state,
    reciprocal_exponents,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=0.1)
    parser.add_argument("--phi-bar", type=float, default=0.0)
    parser.add_argument("--season-duration", type=float, default=1.0)
    parser.add_argument("--u-min", type=float, default=0.0)
    parser.add_argument("--u-max", type=float, default=5.0)
    parser.add_argument("--u-step", type=float, default=0.1)
    parser.add_argument("--ratio-min", type=float, default=0.0)
    parser.add_argument("--ratio-max", type=float, default=15.0)
    parser.add_argument("--ratio-step", type=float, default=0.25)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def grid(start: float, stop: float, step: float) -> list[float]:
    if step <= 0.0:
        raise ValueError("grid step must be positive")
    if stop < start:
        raise ValueError("grid stop must be >= start")
    values = []
    value = start
    while value <= stop + step * 1e-9:
        values.append(value)
        value += step
    return values


def main() -> None:
    args = parse_args()
    if args.eta <= 0.0:
        raise ValueError("--eta must be positive for this coordination phase sweep")
    if args.season_duration <= 0.0:
        raise ValueError("--season-duration must be positive")
    if args.u_min < 0.0 or args.ratio_min < 0.0:
        raise ValueError("dimensionless grid minima must be non-negative")

    tau = args.season_duration
    epsilon = args.eta * tau
    psi = args.phi_bar * tau
    rows = []
    for ratio in grid(args.ratio_min, args.ratio_max, args.ratio_step):
        # ratio = x^2*tau/eta. Therefore x=sqrt(ratio*eta/tau).
        x = (ratio * args.eta / tau) ** 0.5
        v = x * tau
        for u in grid(args.u_min, args.u_max, args.u_step):
            m = u / tau
            premium = anti_phase_temporal_premium(x, m, tau)
            dimensionless_premium = premium * tau
            lambda_d, lambda_s = reciprocal_exponents(
                args.phi_bar, args.eta, x, m, tau
            )
            state = classify_reciprocal_temporal_state(
                args.phi_bar, args.eta, x, m, tau
            )
            rows.append(
                {
                    "u_migration_times_season": u,
                    "contrast_coordination_ratio_x2tau_over_eta": ratio,
                    "v_contrast_times_season": v,
                    "epsilon_eta_times_season": epsilon,
                    "psi_phi_bar_times_season": psi,
                    "dimensionless_temporal_premium": dimensionless_premium,
                    "dimensionless_q_F_minus_epsilon": dimensionless_premium - epsilon,
                    "lambda_d": lambda_d,
                    "lambda_s": lambda_s,
                    "state": state,
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
