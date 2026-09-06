#!/usr/bin/env python3
"""Fit partition-distance feedback gamma on selected pairs and predict holdouts.

Input CSV columns
-----------------
pair_id,role,first_modules,second_modules,delta0,delta1[,analysis_weight]

`first_modules` and `second_modules` use `+` inside modules and `|` between
modules. delta0 is second-minus-first payoff gap when the second architecture
is rare; delta1 is the same gap when the second architecture is common.

The command also requires function geometry and a frozen per-extra-module cost
kappa so intrinsic architecture gaps are predicted independently.
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

from src.hard_module_partition import hard_partition_recovery
from src.hard_partition_game import partition_distance
from src.hard_partition_feedback_identification import (
    endpoint_gap_inversion,
    weighted_common_gamma_fit,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--functions", type=Path, required=True)
    parser.add_argument("--pairs", type=Path, required=True)
    parser.add_argument("--kappa", type=float, required=True)
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


def parse_modules(text: str, ids: Sequence[str]):
    index = {name: i for i, name in enumerate(ids)}
    modules = []
    seen = set()
    for raw_module in [part.strip() for part in text.split("|") if part.strip()]:
        module = []
        for name in [part.strip() for part in raw_module.split("+") if part.strip()]:
            if name not in index:
                raise ValueError(f"unknown function id {name!r}")
            if name in seen:
                raise ValueError(f"function {name!r} occurs more than once")
            seen.add(name)
            module.append(index[name])
        if not module:
            raise ValueError("modules cannot be empty")
        modules.append(tuple(sorted(module)))
    if seen != set(ids):
        raise ValueError("partition must cover every function exactly once")
    return tuple(modules)


def intrinsic_payoff(optima, weights, partition, kappa: float) -> float:
    recovery = hard_partition_recovery(optima, weights, partition)
    return recovery - kappa * (len(partition) - 1)


def load_pairs(path: Path, ids, optima, weights, kappa: float):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {
            "pair_id",
            "role",
            "first_modules",
            "second_modules",
            "delta0",
            "delta1",
        }
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path} must contain columns {sorted(required)}")
        use_weights = "analysis_weight" in reader.fieldnames
        rows: List[Dict[str, object]] = []
        seen = set()
        for line, row in enumerate(reader, start=2):
            pair_id = row["pair_id"].strip()
            if not pair_id or pair_id in seen:
                raise ValueError(f"pair_id must be non-empty and unique at {path}:{line}")
            seen.add(pair_id)
            role = row["role"].strip().lower()
            if role not in {"fit", "holdout"}:
                raise ValueError("role must be fit or holdout")
            first = parse_modules(row["first_modules"].strip(), ids)
            second = parse_modules(row["second_modules"].strip(), ids)
            q = partition_distance(len(ids), first, second)
            if q <= 0.0:
                raise ValueError("pair partitions must be distinct")
            delta0 = float(row["delta0"])
            delta1 = float(row["delta1"])
            observed = endpoint_gap_inversion(delta0, delta1)
            first_b = intrinsic_payoff(optima, weights, first, kappa)
            second_b = intrinsic_payoff(optima, weights, second, kappa)
            phi_arch = second_b - first_b
            analysis_weight = 1.0
            if use_weights:
                raw = row.get("analysis_weight", "").strip()
                if raw:
                    analysis_weight = float(raw)
                if analysis_weight <= 0.0:
                    raise ValueError("analysis_weight must be positive")
            rows.append(
                {
                    "pair_id": pair_id,
                    "role": role,
                    "first_modules": row["first_modules"].strip(),
                    "second_modules": row["second_modules"].strip(),
                    "partition_distance": q,
                    "first_intrinsic_payoff": first_b,
                    "second_intrinsic_payoff": second_b,
                    "phi_arch": phi_arch,
                    "delta0_observed": delta0,
                    "delta1_observed": delta1,
                    "phi_observed": observed["phi"],
                    "eta_observed": observed["eta"],
                    "phi_bridge_residual": observed["phi"] - phi_arch,
                    "analysis_weight": analysis_weight,
                }
            )
    if not rows:
        raise ValueError("pairs file cannot be empty")
    if not any(row["role"] == "fit" for row in rows):
        raise ValueError("at least one fit pair is required")
    if not any(row["role"] == "holdout" for row in rows):
        raise ValueError("at least one holdout pair is required")
    return rows, use_weights


def main() -> None:
    args = parse_args()
    if args.kappa < 0.0:
        raise ValueError("kappa must be non-negative")
    ids, optima, weights = load_functions(args.functions)
    rows, use_weights = load_pairs(
        args.pairs, ids, optima, weights, args.kappa
    )
    fit_rows = [row for row in rows if row["role"] == "fit"]
    fit = weighted_common_gamma_fit(
        [float(row["eta_observed"]) for row in fit_rows],
        [float(row["partition_distance"]) for row in fit_rows],
        [float(row["analysis_weight"]) for row in fit_rows]
        if use_weights
        else None,
    )
    gamma = float(fit["gamma_hat"])

    scored = []
    for row in rows:
        eta_pred = gamma * float(row["partition_distance"])
        phi_pred = float(row["phi_arch"])
        delta0_pred = phi_pred - eta_pred
        delta1_pred = phi_pred + eta_pred
        scored.append(
            {
                **row,
                "gamma_hat_fit_only": gamma,
                "eta_predicted": eta_pred,
                "delta0_predicted": delta0_pred,
                "delta1_predicted": delta1_pred,
                "delta0_residual": float(row["delta0_observed"]) - delta0_pred,
                "delta1_residual": float(row["delta1_observed"]) - delta1_pred,
            }
        )

    holdout = [row for row in scored if row["role"] == "holdout"]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "feedback_receipts.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(scored[0]))
        writer.writeheader()
        writer.writerows(scored)

    summary = {
        "fit_pair_count": len(fit_rows),
        "holdout_pair_count": len(holdout),
        "kappa_frozen": args.kappa,
        "gamma_hat": gamma,
        "fit_gamma_weighted_sse": fit["weighted_sse"],
        "fit_max_abs_phi_bridge_residual": max(
            abs(float(row["phi_bridge_residual"])) for row in fit_rows
        ),
        "holdout_max_abs_phi_bridge_residual": max(
            abs(float(row["phi_bridge_residual"])) for row in holdout
        ),
        "holdout_max_abs_delta0_residual": max(
            abs(float(row["delta0_residual"])) for row in holdout
        ),
        "holdout_max_abs_delta1_residual": max(
            abs(float(row["delta1_residual"])) for row in holdout
        ),
        "holdout_pairs": [row["pair_id"] for row in holdout],
    }
    with (args.output_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    print(args.output_dir)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
