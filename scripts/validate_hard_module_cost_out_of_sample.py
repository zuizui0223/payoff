#!/usr/bin/env python3
"""Fit hard-module kappa on registered fit rows and predict held-out margins.

Input CSV columns
-----------------
architecture_id,module_count,recovery,direct_margin,role[,analysis_weight]

role must be one of:
    fit
    holdout

Only fit rows enter kappa estimation. Held-out rows are scored after kappa is
frozen.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.hard_module_cost_identification import weighted_constant_kappa_fit


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def load_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {
            "architecture_id",
            "module_count",
            "recovery",
            "direct_margin",
            "role",
        }
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
            module_count = int(row["module_count"])
            recovery = float(row["recovery"])
            direct_margin = float(row["direct_margin"])
            if module_count <= 1:
                raise ValueError("module_count must exceed one")
            if recovery < 0.0:
                raise ValueError("recovery must be non-negative")
            analysis_weight = 1.0
            if use_weights:
                raw = row.get("analysis_weight", "").strip()
                if raw:
                    analysis_weight = float(raw)
                if analysis_weight <= 0.0:
                    raise ValueError("analysis_weight must be positive")
            rows.append(
                {
                    "architecture_id": architecture_id,
                    "role": role,
                    "module_count": module_count,
                    "recovery": recovery,
                    "direct_margin": direct_margin,
                    "analysis_weight": analysis_weight,
                }
            )
    if not rows:
        raise ValueError("input cannot be empty")
    if not any(row["role"] == "fit" for row in rows):
        raise ValueError("at least one fit row is required")
    if not any(row["role"] == "holdout" for row in rows):
        raise ValueError("at least one holdout row is required")
    return rows, use_weights


def main() -> None:
    args = parse_args()
    rows, use_weights = load_rows(args.input)
    fit_rows = [row for row in rows if row["role"] == "fit"]
    holdout_rows = [row for row in rows if row["role"] == "holdout"]

    fit = weighted_constant_kappa_fit(
        [float(row["recovery"]) for row in fit_rows],
        [float(row["direct_margin"]) for row in fit_rows],
        [int(row["module_count"]) for row in fit_rows],
        [float(row["analysis_weight"]) for row in fit_rows]
        if use_weights
        else None,
    )
    kappa = float(fit["kappa_hat"])

    scored = []
    for row in rows:
        q = int(row["module_count"]) - 1
        predicted = float(row["recovery"]) - kappa * q
        residual = float(row["direct_margin"]) - predicted
        scored.append(
            {
                **row,
                "extra_module_count": q,
                "kappa_hat_from_fit_only": kappa,
                "predicted_margin": predicted,
                "prediction_residual": residual,
            }
        )

    holdout_residuals = [
        float(row["prediction_residual"])
        for row in scored
        if row["role"] == "holdout"
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "validation_receipts.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(scored[0]))
        writer.writeheader()
        writer.writerows(scored)

    summary = {
        "fit_count": len(fit_rows),
        "holdout_count": len(holdout_rows),
        "kappa_hat": kappa,
        "fit_weighted_sse": fit["weighted_sse"],
        "holdout_max_abs_residual": max(abs(value) for value in holdout_residuals),
        "holdout_mean_abs_residual": sum(abs(value) for value in holdout_residuals)
        / len(holdout_residuals),
        "holdout_architectures": [
            row["architecture_id"] for row in holdout_rows
        ],
    }
    with (args.output_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    print(args.output_dir)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
