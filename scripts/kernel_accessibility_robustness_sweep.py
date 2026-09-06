#!/usr/bin/env python3
"""Sweep kernel-family robustness of local architecture accessibility."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from src.architecture_phase_atlas import regular_grid
from src.kernel_accessibility_envelope import kernel_accessibility_envelope


def _floats(text: str) -> tuple[float, ...]:
    values = tuple(float(x.strip()) for x in text.split(",") if x.strip())
    if not values:
        raise argparse.ArgumentTypeError("list must not be empty")
    return values


def _strings(text: str) -> tuple[str, ...]:
    values = tuple(x.strip() for x in text.split(",") if x.strip())
    if not values:
        raise argparse.ArgumentTypeError("kernel list must not be empty")
    return values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gammas", type=_floats, default=_floats("-30,-20,-10,-5,-3,-2,-1,0"))
    parser.add_argument("--epsilons", type=_floats, default=_floats("0.05,0.1,0.2,0.3,0.4"))
    parser.add_argument("--kernels", type=_strings, default=_strings("hard,triangular,cosine,gaussian"))
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--kappa", type=float, default=1.0)
    parser.add_argument("--length", type=float, default=1.0)
    parser.add_argument("--bins", type=int, default=161)
    parser.add_argument("--jump-radius-bins", type=int, default=1)
    parser.add_argument("--csv", type=Path, default=Path("outputs/kernel_accessibility_robustness.csv"))
    parser.add_argument("--json", type=Path, default=Path("outputs/kernel_accessibility_robustness_summary.json"))
    args = parser.parse_args()

    grid = regular_grid(args.length, args.bins)
    rows = []
    counts: dict[str, int] = {}
    for epsilon in args.epsilons:
        for gamma in args.gammas:
            env = kernel_accessibility_envelope(
                grid,
                args.kernels,
                alpha=args.alpha,
                kappa=args.kappa,
                gamma=gamma,
                epsilon=epsilon,
                declared_jump_radius_bins=args.jump_radius_bins,
            )
            counts[env.robustness_class] = counts.get(env.robustness_class, 0) + 1
            rows.append({
                "epsilon": epsilon,
                "gamma": gamma,
                "declared_jump_radius_bins": args.jump_radius_bins,
                "declared_jump_distance": env.declared_jump_distance,
                "robustness_class": env.robustness_class,
                "min_critical_jump_distance": env.min_critical_jump_distance,
                "max_critical_jump_distance": env.max_critical_jump_distance,
                "accessible_kernels": ";".join(env.accessible_kernels),
                "trapped_kernels": ";".join(env.trapped_kernels),
                "critical_by_kernel": json.dumps(
                    {result.kernel: result.critical_jump_distance for result in env.results},
                    sort_keys=True,
                    separators=(",", ":"),
                ),
            })

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "status": "finite_grid_kernel_robustness_sweep_not_biological_prevalence",
        "parameters": {
            "gammas": list(args.gammas),
            "epsilons": list(args.epsilons),
            "kernels": list(args.kernels),
            "alpha": args.alpha,
            "kappa": args.kappa,
            "length": args.length,
            "bins": args.bins,
            "jump_radius_bins": args.jump_radius_bins,
            "jump_distance": args.jump_radius_bins * (grid[1] - grid[0]),
        },
        "n_cells": len(rows),
        "robustness_counts": dict(sorted(counts.items())),
        "csv": str(args.csv),
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
