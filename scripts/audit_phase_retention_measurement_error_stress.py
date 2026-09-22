#!/usr/bin/env python3
"""Audit how much classical phase error is needed to mimic observed lambdas."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.phase_retention_recovery import (
    required_equal_error_sd_ratio,
)


def parse_correlations(value: str) -> tuple[float, ...]:
    values = tuple(
        float(item.strip())
        for item in value.split(",")
        if item.strip()
    )
    if not values:
        raise argparse.ArgumentTypeError(
            "at least one error correlation is required"
        )
    return values


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--registry-json",
        type=Path,
        default=Path(
            "data/payoff_b_lambda_recovery_taxon_registry_20260922.json"
        ),
    )
    p.add_argument(
        "--error-correlations",
        type=parse_correlations,
        default=(0.0, 0.25, 0.5, 0.8),
    )
    p.add_argument(
        "--true-lambda",
        type=float,
        default=1.0,
    )
    p.add_argument(
        "--csv-output",
        type=Path,
        default=Path(
            "outputs/payoff_b_lambda_error_stress.csv"
        ),
    )
    p.add_argument(
        "--receipt-output",
        type=Path,
        default=Path(
            "outputs/payoff_b_lambda_error_stress_receipt.json"
        ),
    )
    args = p.parse_args()

    registry = json.loads(
        args.registry_json.read_text(encoding="utf-8")
    )
    systems = registry.get("systems")
    if not isinstance(systems, list) or not systems:
        raise SystemExit("registry has no systems")

    rows = []
    for system in systems:
        observed = float(system["observed_lambda"])
        for rho in args.error_correlations:
            ratio = required_equal_error_sd_ratio(
                observed_naive_lambda=observed,
                true_lambda=args.true_lambda,
                error_correlation=rho,
            )
            rows.append(
                {
                    "system_id": system["system_id"],
                    "taxon": system["taxon"],
                    "interval_id": system["interval_id"],
                    "n_pairs": int(system["n_pairs"]),
                    "observed_lambda": observed,
                    "true_lambda_null": args.true_lambda,
                    "error_correlation": rho,
                    "required_equal_error_sd_over_latent_phase_sd": ratio,
                    "finite_equal_error_solution": ratio is not None,
                }
            )

    args.csv_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    with args.csv_output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
        )
        writer.writeheader()
        writer.writerows(rows)

    receipt = {
        "status": "lambda_measurement_error_stress_complete",
        "registry_source": str(args.registry_json),
        "true_lambda_null": args.true_lambda,
        "error_correlations": list(args.error_correlations),
        "rows": rows,
        "claim_boundary": (
            "required noise-to-signal thresholds under an equal-error additive "
            "model; these are stress thresholds, not empirical error estimates"
        ),
    }
    args.receipt_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.csv_output)
    print(args.receipt_output)


if __name__ == "__main__":
    main()
