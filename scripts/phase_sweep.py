#!/usr/bin/env python3
"""Generate a CSV phase grid for the minimal PAYOFF architecture game."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.payoff_game import classify_phase, interior_equilibrium


def frange(start: float, stop: float, step: float):
    x = start
    while x <= stop + abs(step) * 1e-9:
        yield x
        x += step


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phi-min", type=float, default=-2.0)
    parser.add_argument("--phi-max", type=float, default=2.0)
    parser.add_argument("--eta-min", type=float, default=-2.0)
    parser.add_argument("--eta-max", type=float, default=2.0)
    parser.add_argument("--step", type=float, default=0.05)
    parser.add_argument("--output", type=Path, default=Path("outputs/phase_grid.csv"))
    args = parser.parse_args()

    if args.step <= 0:
        raise SystemExit("--step must be positive")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["phi", "eta", "phase", "p_star"])
        writer.writeheader()
        for eta in frange(args.eta_min, args.eta_max, args.step):
            for phi in frange(args.phi_min, args.phi_max, args.step):
                p_star = interior_equilibrium(phi, eta)
                writer.writerow(
                    {
                        "phi": f"{phi:.12g}",
                        "eta": f"{eta:.12g}",
                        "phase": classify_phase(phi, eta),
                        "p_star": "" if p_star is None else f"{p_star:.12g}",
                    }
                )

    print(args.output)


if __name__ == "__main__":
    main()
