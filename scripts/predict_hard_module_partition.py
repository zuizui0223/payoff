#!/usr/bin/env python3
"""Predict exact hard-module partitions from scalar function optima.

Input CSV
---------
function_id,optimum,weight

The hard-module architecture forces all functions inside one module to share one
coordinate, while different modules have independent coordinates. With a fixed
fitness cost per extra module, the globally optimal scalar partition is solved
exactly by dynamic programming.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import List, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.hard_module_partition import (
    fixed_k_loss_curve,
    module_count_intervals,
    module_summary,
    optimal_penalized_partition,
    weighted_shared_loss,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--functions", type=Path, required=True)
    parser.add_argument("--extra-module-cost", type=float, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def load_functions(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"function_id", "optimum", "weight"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path} must contain columns {sorted(required)}")
        ids: List[str] = []
        optima: List[float] = []
        weights: List[float] = []
        for line, row in enumerate(reader, start=2):
            function_id = row["function_id"].strip()
            if not function_id or function_id in ids:
                raise ValueError(f"function_id must be non-empty and unique at {path}:{line}")
            optimum = float(row["optimum"])
            weight = float(row["weight"])
            if weight <= 0.0:
                raise ValueError(f"weight must be positive for {function_id}")
            ids.append(function_id)
            optima.append(optimum)
            weights.append(weight)
    if not ids:
        raise ValueError("functions file cannot be empty")
    return ids, optima, weights


def module_label(modules, ids: Sequence[str]) -> str:
    return "|".join(
        "{" + ",".join(ids[index] for index in module) + "}"
        for module in modules
    )


def module_means_text(modules, optima, weights) -> str:
    return ";".join(
        f"{float(module_summary(optima, weights, module)['mean']):.12g}"
        for module in modules
    )


def write_fixed_k(output: Path, ids, optima, weights):
    curve = fixed_k_loss_curve(optima, weights)
    shared = weighted_shared_loss(optima, weights)
    rows = []
    for row in curve:
        modules = row["modules"]
        rows.append(
            {
                "module_count": row["module_count"],
                "modules": module_label(modules, ids),
                "module_means": module_means_text(modules, optima, weights),
                "within_loss": row["within_loss"],
                "recovery": shared - float(row["within_loss"]),
            }
        )
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def write_intervals(output: Path, ids, optima, weights):
    rows = []
    for row in module_count_intervals(optima, weights):
        upper = float(row["upper_cost"])
        rows.append(
            {
                "module_count": row["module_count"],
                "modules": module_label(row["modules"], ids),
                "within_loss": row["within_loss"],
                "recovery": row["recovery"],
                "lower_extra_module_cost": row["lower_cost"],
                "upper_extra_module_cost": "inf" if math.isinf(upper) else upper,
            }
        )
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def main() -> None:
    args = parse_args()
    if args.extra_module_cost < 0.0:
        raise ValueError("extra-module-cost must be non-negative")
    ids, optima, weights = load_functions(args.functions)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    fixed_rows = write_fixed_k(
        args.output_dir / "fixed_module_counts.csv", ids, optima, weights
    )
    interval_rows = write_intervals(
        args.output_dir / "module_count_intervals.csv", ids, optima, weights
    )
    best = optimal_penalized_partition(
        optima, weights, args.extra_module_cost
    )

    summary = {
        "function_count": len(ids),
        "function_ids": ids,
        "fully_shared_conflict_load": weighted_shared_loss(optima, weights),
        "extra_module_cost": args.extra_module_cost,
        "optimal_module_count": best["module_count"],
        "optimal_modules": module_label(best["modules"], ids),
        "optimal_module_means": list(best["module_means"]),
        "within_loss": best["within_loss"],
        "recovery": best["recovery"],
        "architecture_cost": best["architecture_cost"],
        "net_gain": best["net_gain"],
        "fixed_k_rows": len(fixed_rows),
        "supported_module_counts": [row["module_count"] for row in interval_rows],
    }
    with (args.output_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    print(args.output_dir)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
