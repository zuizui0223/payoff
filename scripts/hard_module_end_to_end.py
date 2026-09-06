#!/usr/bin/env python3
"""End-to-end hard-module pipeline from function geometry to held-out validation.

Inputs
------
functions.csv
    function_id,optimum,weight

worldlines.csv
    architecture_id,role,modules,direct_margin[,analysis_weight]

`modules` uses `+` within a module and `|` between modules, for example:
    F1+F2|F3
    F1|F2|F3

The script computes each partition recovery from function geometry, fits kappa
using only role=fit rows, predicts role=holdout margins, and then predicts the
global hard-module architecture under the frozen kappa.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.hard_module_accessibility import (
    greedy_hard_split_path,
    split_tree_accessibility,
    target_is_split_accessible,
)
from src.hard_module_cost_identification import weighted_constant_kappa_fit
from src.hard_module_partition import (
    hard_partition_recovery,
    module_summary,
    optimal_penalized_partition,
    weighted_shared_loss,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--functions", type=Path, required=True)
    parser.add_argument("--worldlines", type=Path, required=True)
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
            fid = row["function_id"].strip()
            if not fid or fid in ids:
                raise ValueError(f"function_id must be non-empty and unique at {path}:{line}")
            optimum = float(row["optimum"])
            weight = float(row["weight"])
            if weight <= 0.0:
                raise ValueError(f"weight must be positive for {fid}")
            ids.append(fid)
            optima.append(optimum)
            weights.append(weight)
    if not ids:
        raise ValueError("functions file cannot be empty")
    return ids, optima, weights


def parse_modules(text: str, function_ids: Sequence[str]) -> Tuple[Tuple[int, ...], ...]:
    index = {name: i for i, name in enumerate(function_ids)}
    raw_modules = [part.strip() for part in text.split("|") if part.strip()]
    if not raw_modules:
        raise ValueError("modules cannot be empty")
    modules = []
    seen = set()
    for raw_module in raw_modules:
        names = [name.strip() for name in raw_module.split("+") if name.strip()]
        if not names:
            raise ValueError("each module must contain at least one function")
        module = []
        for name in names:
            if name not in index:
                raise ValueError(f"unknown function id {name!r} in modules")
            if name in seen:
                raise ValueError(f"function {name!r} appears in more than one module")
            seen.add(name)
            module.append(index[name])
        modules.append(tuple(sorted(module)))
    if seen != set(function_ids):
        missing = sorted(set(function_ids) - seen)
        raise ValueError(f"modules must cover all functions exactly once; missing={missing}")
    return tuple(modules)


def load_worldlines(path: Path, ids: Sequence[str], optima, weights):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"architecture_id", "role", "modules", "direct_margin"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path} must contain columns {sorted(required)}")
        use_weights = "analysis_weight" in reader.fieldnames
        rows: List[Dict[str, object]] = []
        seen = set()
        for line, row in enumerate(reader, start=2):
            architecture_id = row["architecture_id"].strip()
            if not architecture_id or architecture_id in seen:
                raise ValueError(
                    f"architecture_id must be non-empty and unique at {path}:{line}"
                )
            seen.add(architecture_id)
            role = row["role"].strip().lower()
            if role not in {"fit", "holdout"}:
                raise ValueError(f"role must be fit or holdout at {path}:{line}")
            modules = parse_modules(row["modules"].strip(), ids)
            direct_margin = float(row["direct_margin"])
            analysis_weight = 1.0
            if use_weights:
                raw_weight = row.get("analysis_weight", "").strip()
                if raw_weight:
                    analysis_weight = float(raw_weight)
                if analysis_weight <= 0.0:
                    raise ValueError("analysis_weight must be positive")
            recovery = hard_partition_recovery(optima, weights, modules)
            rows.append(
                {
                    "architecture_id": architecture_id,
                    "role": role,
                    "modules": modules,
                    "module_count": len(modules),
                    "recovery": recovery,
                    "direct_margin": direct_margin,
                    "analysis_weight": analysis_weight,
                }
            )
    if not rows:
        raise ValueError("worldlines file cannot be empty")
    if not any(row["role"] == "fit" for row in rows):
        raise ValueError("at least one fit row is required")
    return rows, use_weights


def module_label(modules, ids: Sequence[str]) -> str:
    return "|".join(
        "{" + ",".join(ids[index] for index in module) + "}"
        for module in modules
    )


def main() -> None:
    args = parse_args()
    ids, optima, weights = load_functions(args.functions)
    rows, use_weights = load_worldlines(args.worldlines, ids, optima, weights)

    fit_rows = [row for row in rows if row["role"] == "fit"]
    fit = weighted_constant_kappa_fit(
        [float(row["recovery"]) for row in fit_rows],
        [float(row["direct_margin"]) for row in fit_rows],
        [int(row["module_count"]) for row in fit_rows],
        [float(row["analysis_weight"]) for row in fit_rows] if use_weights else None,
    )
    kappa = float(fit["kappa_hat"])

    scored = []
    for row in rows:
        q = int(row["module_count"]) - 1
        predicted = float(row["recovery"]) - kappa * q
        residual = float(row["direct_margin"]) - predicted
        scored.append(
            {
                "architecture_id": row["architecture_id"],
                "role": row["role"],
                "modules": module_label(row["modules"], ids),
                "module_count": row["module_count"],
                "recovery": row["recovery"],
                "release_fraction": (
                    0.0
                    if weighted_shared_loss(optima, weights) == 0.0
                    else float(row["recovery"]) / weighted_shared_loss(optima, weights)
                ),
                "direct_margin": row["direct_margin"],
                "predicted_margin": predicted,
                "prediction_residual": residual,
                "analysis_weight": row["analysis_weight"],
            }
        )

    best = optimal_penalized_partition(optima, weights, kappa)
    access = split_tree_accessibility(optima, weights, best["modules"])
    greedy = greedy_hard_split_path(optima, weights, kappa)
    holdout_residuals = [
        abs(float(row["prediction_residual"]))
        for row in scored
        if row["role"] == "holdout"
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "worldline_receipts.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(scored[0]))
        writer.writeheader()
        writer.writerows(scored)

    shared_loss = weighted_shared_loss(optima, weights)
    summary = {
        "function_ids": ids,
        "fully_shared_conflict_load": shared_loss,
        "fit_architecture_count": len(fit_rows),
        "holdout_architecture_count": len(rows) - len(fit_rows),
        "kappa_hat": kappa,
        "fit_weighted_sse": fit["weighted_sse"],
        "holdout_max_abs_residual": max(holdout_residuals) if holdout_residuals else None,
        "optimal_module_count": best["module_count"],
        "optimal_modules": module_label(best["modules"], ids),
        "optimal_recovery": best["recovery"],
        "optimal_release_fraction": 0.0 if shared_loss == 0.0 else best["recovery"] / shared_loss,
        "optimal_architecture_cost": best["architecture_cost"],
        "optimal_net_gain": best["net_gain"],
        "optimal_split_accessibility_threshold": access["accessibility_threshold"],
        "optimal_split_accessible": target_is_split_accessible(
            optima, weights, best["modules"], kappa
        ),
        "greedy_final_modules": module_label(greedy[-1]["modules"], ids),
        "greedy_matches_global": greedy[-1]["modules"] == best["modules"],
    }
    with (args.output_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    print(args.output_dir)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
