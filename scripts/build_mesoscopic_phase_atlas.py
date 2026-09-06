#!/usr/bin/env python3
"""Build a CSV/JSON finite-grid mesoscopic architecture phase atlas."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from src.architecture_phase_atlas import build_phase_atlas, phase_counts


def _float_list(text: str) -> tuple[float, ...]:
    values = tuple(float(x.strip()) for x in text.split(",") if x.strip())
    if not values:
        raise argparse.ArgumentTypeError("list must not be empty")
    return values


def _int_list(text: str) -> tuple[int, ...]:
    values = tuple(int(x.strip()) for x in text.split(",") if x.strip())
    if not values or any(x < 0 for x in values):
        raise argparse.ArgumentTypeError("jump radii must be non-negative integers")
    return values


def _epsilon_list(text: str) -> tuple[float | None, ...]:
    values: list[float | None] = []
    for token in (x.strip() for x in text.split(",") if x.strip()):
        if token.lower() in {"global", "none", "inf"}:
            values.append(None)
        else:
            value = float(token)
            if value < 0.0:
                raise argparse.ArgumentTypeError("epsilon must be non-negative")
            values.append(value)
    if not values:
        raise argparse.ArgumentTypeError("epsilon list must not be empty")
    return tuple(values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gammas", type=_float_list, default=_float_list("-2,-1,-0.75,-0.5,-0.25,0,0.5"))
    parser.add_argument("--epsilons", type=_epsilon_list, default=_epsilon_list("0.05,0.1,0.2,0.4,global"))
    parser.add_argument("--jump-radii", type=_int_list, default=_int_list("1,2,4"))
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--kappa", type=float, default=1.0)
    parser.add_argument("--length", type=float, default=1.0)
    parser.add_argument("--bins", type=int, default=41)
    parser.add_argument("--beta", type=float, default=1.5)
    parser.add_argument("--mutation-rate", type=float, default=0.03)
    parser.add_argument("--steps", type=int, default=800)
    parser.add_argument("--csv", type=Path, default=Path("outputs/mesoscopic_phase_atlas.csv"))
    parser.add_argument("--json", type=Path, default=Path("outputs/mesoscopic_phase_atlas_summary.json"))
    args = parser.parse_args()

    cells = build_phase_atlas(
        args.gammas,
        args.epsilons,
        args.jump_radii,
        alpha=args.alpha,
        kappa=args.kappa,
        length=args.length,
        bins=args.bins,
        beta=args.beta,
        mutation_rate=args.mutation_rate,
        steps=args.steps,
    )

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "gamma",
        "epsilon",
        "jump_radius_bins",
        "critical_uphill_jump_bins",
        "small_jump_trapped",
        "dynamical_regime",
        "monomorphic_like",
        "final_mean",
        "final_variance",
        "peak_locations",
        "left_endpoint_mass",
        "right_endpoint_mass",
        "last_l1_change",
    ]
    with args.csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for cell in cells:
            row = cell.to_dict()
            row["peak_locations"] = json.dumps(row["peak_locations"], separators=(",", ":"))
            writer.writerow(row)

    trapped = sum(cell.small_jump_trapped for cell in cells)
    summary = {
        "status": "finite_grid_exploratory_atlas_not_theorem",
        "parameters": {
            "gammas": list(args.gammas),
            "epsilons": ["global" if x is None else x for x in args.epsilons],
            "jump_radii_bins": list(args.jump_radii),
            "alpha": args.alpha,
            "kappa": args.kappa,
            "length": args.length,
            "bins": args.bins,
            "beta": args.beta,
            "mutation_rate": args.mutation_rate,
            "steps": args.steps,
        },
        "n_cells": len(cells),
        "phase_counts": phase_counts(cells),
        "small_jump_trapped_cells": trapped,
        "small_jump_accessible_cells": len(cells) - trapped,
        "csv": str(args.csv),
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
