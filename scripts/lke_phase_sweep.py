#!/usr/bin/env python3
"""Generate a CSV grid for the environmental PAYOFF phase diagram.

The sweep uses coordinates (L, K, eta) at fixed separation fraction s and writes
both the static architecture gap and the reciprocal invasion margins.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.payoff_game import (
    architecture_phi,
    classify_lke_phase,
    invasion_cost_surfaces,
    invasion_margins,
)


def frange(start: float, stop: float, step: float):
    x = start
    while x <= stop + abs(step) * 1e-9:
        yield x
        x += step


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--s", type=float, default=0.5)
    parser.add_argument("--l-min", type=float, default=0.0)
    parser.add_argument("--l-max", type=float, default=2.0)
    parser.add_argument("--k-min", type=float, default=0.0)
    parser.add_argument("--k-max", type=float, default=2.0)
    parser.add_argument("--eta-min", type=float, default=-1.0)
    parser.add_argument("--eta-max", type=float, default=1.0)
    parser.add_argument("--step", type=float, default=0.1)
    parser.add_argument(
        "--output", type=Path, default=Path("outputs/lke_phase_grid.csv")
    )
    args = parser.parse_args()

    if not 0.0 <= args.s <= 1.0:
        raise SystemExit("--s must lie in [0,1]")
    if args.step <= 0:
        raise SystemExit("--step must be positive")
    if args.l_min < 0 or args.k_min < 0:
        raise SystemExit("L and K ranges must be non-negative")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "L",
        "s",
        "K",
        "eta",
        "R",
        "phi",
        "I_D_rare_in_S",
        "I_S_rare_in_D",
        "K_D_neutral",
        "K_S_neutral",
        "phase",
    ]

    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for eta in frange(args.eta_min, args.eta_max, args.step):
            for conflict_load in frange(args.l_min, args.l_max, args.step):
                for cost in frange(args.k_min, args.k_max, args.step):
                    recovery = args.s * conflict_load
                    phi = architecture_phi(conflict_load, args.s, cost)
                    i_d, i_s = invasion_margins(
                        conflict_load, args.s, cost, eta
                    )
                    k_d, k_s = invasion_cost_surfaces(
                        conflict_load, args.s, eta
                    )
                    writer.writerow(
                        {
                            "L": f"{conflict_load:.12g}",
                            "s": f"{args.s:.12g}",
                            "K": f"{cost:.12g}",
                            "eta": f"{eta:.12g}",
                            "R": f"{recovery:.12g}",
                            "phi": f"{phi:.12g}",
                            "I_D_rare_in_S": f"{i_d:.12g}",
                            "I_S_rare_in_D": f"{i_s:.12g}",
                            "K_D_neutral": f"{k_d:.12g}",
                            "K_S_neutral": f"{k_s:.12g}",
                            "phase": classify_lke_phase(
                                conflict_load, args.s, cost, eta
                            ),
                        }
                    )

    print(args.output)


if __name__ == "__main__":
    main()
