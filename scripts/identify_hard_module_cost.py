#!/usr/bin/env python3
"""Identify constant per-extra-module cost from direct partition worldlines.

Input CSV columns
-----------------
architecture_id,module_count,recovery,direct_margin[,analysis_weight]

All recovery and direct-margin quantities must already be on one matched fitness
scale. The command fits
    recovery - direct_margin = kappa * (module_count - 1)
through the origin.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List

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
        required = {"architecture_id", "module_count", "recovery", "direct_margin"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path} must contain columns {sorted(required)}")
        use_weights = "analysis_weight" in reader.fieldnames
        ids: List[str] = []
        module_counts: List[int] = []
        recoveries: List[float] = []
        margins: List[float] = []
        weights: List[float] = []
        for line, row in enumerate(reader, start=2):
            architecture_id = row["architecture_id"].strip()
            if not architecture_id or architecture_id in ids:
                raise ValueError(
                    f"architecture_id must be non-empty and unique at {path}:{line}"
                )
            module_count = int(row["module_count"])
            recovery = float(row["recovery"])
            margin = float(row["direct_margin"])
            if module_count <= 1:
                raise ValueError("module_count must exceed one")
            if recovery < 0.0:
                raise ValueError("recovery must be non-negative")
            weight = 1.0
            if use_weights:
                raw = row.get("analysis_weight", "").strip()
                if raw:
                    weight = float(raw)
                if weight <= 0.0:
                    raise ValueError("analysis_weight must be positive")
            ids.append(architecture_id)
            module_counts.append(module_count)
            recoveries.append(recovery)
            margins.append(margin)
            weights.append(weight)
    if not ids:
        raise ValueError("input cannot be empty")
    return ids, module_counts, recoveries, margins, weights, use_weights


def main() -> None:
    args = parse_args()
    ids, module_counts, recoveries, margins, weights, use_weights = load_rows(args.input)
    fit = weighted_constant_kappa_fit(
        recoveries,
        margins,
        module_counts,
        weights if use_weights else None,
    )

    rows = []
    for i, architecture_id in enumerate(ids):
        rows.append(
            {
                "architecture_id": architecture_id,
                "module_count": module_counts[i],
                "extra_module_count": module_counts[i] - 1,
                "recovery": recoveries[i],
                "direct_margin": margins[i],
                "analysis_weight": weights[i],
                "implied_kappa": fit["implied_kappas"][i],
                "predicted_margin": fit["predicted_margins"][i],
                "bridge_residual": fit["residuals"][i],
            }
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "cost_receipts.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "architecture_count": len(ids),
        "kappa_hat": fit["kappa_hat"],
        "weighted_sse": fit["weighted_sse"],
        "max_abs_bridge_residual": max(abs(value) for value in fit["residuals"]),
        "implied_kappa_min": min(fit["implied_kappas"]),
        "implied_kappa_max": max(fit["implied_kappas"]),
        "input_used_analysis_weights": use_weights,
    }
    with (args.output_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    print(args.output_dir)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
