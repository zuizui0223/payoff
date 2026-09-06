#!/usr/bin/env python3
"""Generate the exact two-patch spatial polarization branch for PAYOFF."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.spatial_metapopulation import (
    classify_two_patch_polarization,
    two_patch_polarized_eigenvalues,
    two_patch_polarized_equilibria,
)


def frange(start: float, stop: float, step: float):
    x = start
    while x <= stop + abs(step) * 1e-9:
        yield x
        x += step


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=1.0)
    parser.add_argument("--m-min", type=float, default=0.0)
    parser.add_argument("--m-max", type=float, default=0.35)
    parser.add_argument("--step", type=float, default=0.01)
    parser.add_argument("--output", type=Path, default=Path("outputs/spatial_two_patch.csv"))
    args = parser.parse_args()

    if args.eta <= 0:
        raise SystemExit("--eta must be positive")
    if args.m_min < 0 or args.m_max < args.m_min or args.step <= 0:
        raise SystemExit("invalid migration range")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "eta",
        "migration_rate",
        "m_over_eta",
        "phase",
        "p_low",
        "p_high",
        "uniform_rate",
        "transverse_rate",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for m in frange(args.m_min, args.m_max, args.step):
            pair = two_patch_polarized_equilibria(args.eta, m)
            rates = two_patch_polarized_eigenvalues(args.eta, m)
            writer.writerow(
                {
                    "eta": f"{args.eta:.12g}",
                    "migration_rate": f"{m:.12g}",
                    "m_over_eta": f"{m / args.eta:.12g}",
                    "phase": classify_two_patch_polarization(args.eta, m),
                    "p_low": "" if pair is None else f"{pair[0]:.12g}",
                    "p_high": "" if pair is None else f"{pair[1]:.12g}",
                    "uniform_rate": "" if rates is None else f"{rates[0]:.12g}",
                    "transverse_rate": "" if rates is None else f"{rates[1]:.12g}",
                }
            )

    print(args.output)


if __name__ == "__main__":
    main()
