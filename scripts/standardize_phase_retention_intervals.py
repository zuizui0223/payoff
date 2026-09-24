#!/usr/bin/env python3
"""Standardize phase-retention coefficients across unequal interval scales.

This module intentionally separates three quantities:

1. signed segment-scale lambda (the original estimator);
2. an equivalent magnitude-decay constant k_eq on a declared reference
   duration;
3. propagated path-memory retention under an explicitly homogeneous-lambda
   approximation.

The transformation is descriptive. It does not refit a continuous-time
controller and must not erase negative-lambda overshoot cases.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT = Path(
    "data/payoff_b_phase_retention_interval_standardization_contract_20260925.json"
)
DEFAULT_OUTPUT = Path(
    "outputs/payoff_b_phase_retention_interval_standardization_20260925.json"
)


def _finite_float(value: Any, name: str) -> float:
    x = float(value)
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def equivalent_interval_metrics(lam: float, duration_days: float) -> dict[str, Any]:
    lam = _finite_float(lam, "lambda")
    duration_days = _finite_float(duration_days, "duration_days")
    if duration_days <= 0:
        raise ValueError("duration_days must be > 0")

    magnitude = abs(lam)
    sign = 0 if lam == 0 else (1 if lam > 0 else -1)

    if magnitude == 0:
        return {
            "lambda": lam,
            "lambda_sign": sign,
            "retention_magnitude": 0.0,
            "reference_duration_days": duration_days,
            "equivalent_decay_constant_per_day": None,
            "equivalent_daily_retention": 0.0,
            "equivalent_daily_correction": 1.0,
            "equivalent_half_life_days": 0.0,
            "rate_status": "ZERO_RETENTION_LIMIT",
        }

    k_eq = -math.log(magnitude) / duration_days
    daily_retention = math.exp(-k_eq)
    if k_eq > 0:
        half_life = math.log(2.0) / k_eq
        rate_status = "CONTRACTION"
    elif k_eq < 0:
        half_life = None
        rate_status = "AMPLIFICATION"
    else:
        half_life = None
        rate_status = "COMPLETE_RETENTION"

    return {
        "lambda": lam,
        "lambda_sign": sign,
        "retention_magnitude": magnitude,
        "reference_duration_days": duration_days,
        "equivalent_decay_constant_per_day": k_eq,
        "equivalent_daily_retention": daily_retention,
        "equivalent_daily_correction": 1.0 - daily_retention,
        "equivalent_half_life_days": half_life,
        "rate_status": rate_status,
    }


def duration_sensitivity(lam: float, q25: float, median: float, q75: float) -> dict[str, Any]:
    rows = {
        "q25_duration": equivalent_interval_metrics(lam, q25),
        "median_duration": equivalent_interval_metrics(lam, median),
        "q75_duration": equivalent_interval_metrics(lam, q75),
    }
    ks = [
        row["equivalent_decay_constant_per_day"]
        for row in rows.values()
        if row["equivalent_decay_constant_per_day"] is not None
    ]
    return {
        "rows": rows,
        "k_eq_min_over_duration_iqr": min(ks) if ks else None,
        "k_eq_max_over_duration_iqr": max(ks) if ks else None,
    }


def _expand_histogram(histogram: dict[str, int]) -> list[int]:
    values: list[int] = []
    for raw_n, raw_count in sorted(histogram.items(), key=lambda item: int(item[0])):
        n = int(raw_n)
        count = int(raw_count)
        if n <= 0 or count <= 0:
            raise ValueError("transition-count histogram requires positive integers")
        values.extend([n] * count)
    return values


def _median(values: list[float]) -> float:
    ordered = sorted(values)
    n = len(ordered)
    if n == 0:
        raise ValueError("cannot summarize empty values")
    mid = n // 2
    if n % 2:
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


def path_memory_summary(retention: float, path_rule: dict[str, Any]) -> dict[str, Any]:
    mode = path_rule["mode"]
    if not path_rule.get("licensed", False):
        return {
            "licensed": False,
            "mode": mode,
            "reason": path_rule.get("reason"),
        }

    if mode == "whole_interval_is_path":
        return {
            "licensed": True,
            "mode": mode,
            "path_retention_magnitude": retention,
            "path_correction_magnitude": 1.0 - retention,
            "interpretation": (
                "the original interval already spans the declared migration path"
            ),
        }

    if mode == "homogeneous_transition_count_histogram":
        counts = _expand_histogram(path_rule["transition_count_histogram"])
        expected_n = int(path_rule["animal_years"])
        if len(counts) != expected_n:
            raise ValueError(
                f"histogram expands to {len(counts)} rows, expected {expected_n}"
            )
        if sum(counts) != int(path_rule["transitions"]):
            raise ValueError(
                "histogram transition total does not match frozen transition count"
            )

        path_values = [retention ** n for n in counts]
        median_n = _median([float(n) for n in counts])
        return {
            "licensed": True,
            "mode": mode,
            "unit": path_rule["unit"],
            "animal_years": len(counts),
            "unique_individuals": int(path_rule["unique_individuals"]),
            "transitions": sum(counts),
            "transition_count_mean": sum(counts) / len(counts),
            "transition_count_median": median_n,
            "retention_at_median_transition_count": retention ** median_n,
            "correction_at_median_transition_count": 1.0 - retention ** median_n,
            "mean_path_retention_magnitude": sum(path_values) / len(path_values),
            "median_path_retention_magnitude": _median(path_values),
            "minimum_path_retention_magnitude": min(path_values),
            "maximum_path_retention_magnitude": max(path_values),
            "interpretation": (
                "propagated memory of the initial phase deviation under a "
                "homogeneous transition coefficient; not predicted final phase "
                "error after intercepts, innovations or route-stage heterogeneity"
            ),
        }

    raise ValueError(f"unsupported path mode: {mode}")


def build_result(contract: dict[str, Any]) -> dict[str, Any]:
    if contract.get("Aikens_lambda_outcome_opened") is not False:
        raise ValueError("contract must remain pre-Aikens-outcome")

    output_systems = []
    for system in contract["systems"]:
        duration = system["duration_days"]
        q25 = _finite_float(duration["q25"], "q25")
        median = _finite_float(duration["median"], "median")
        q75 = _finite_float(duration["q75"], "q75")
        if not (0 < q25 <= median <= q75):
            raise ValueError(f"invalid duration quartiles for {system['system_id']}")

        variants = []
        for variant in system["lambda_variants"]:
            lam = _finite_float(variant["lambda"], "lambda")
            metrics = equivalent_interval_metrics(lam, median)
            metrics["duration_sensitivity"] = duration_sensitivity(
                lam, q25, median, q75
            )
            metrics["path_memory"] = path_memory_summary(
                metrics["retention_magnitude"],
                system["path_rule"],
            )
            metrics["variant_id"] = variant["variant_id"]
            metrics["role"] = variant["role"]
            variants.append(metrics)

        output_systems.append(
            {
                "system_id": system["system_id"],
                "taxon": system["taxon"],
                "interval_id": system["interval_id"],
                "duration_days": duration,
                "path_rule": system["path_rule"],
                "variants": variants,
            }
        )

    return {
        "result_id": "payoff_b_phase_retention_interval_standardization_20260925",
        "frozen_date": contract["frozen_date"],
        "contract_id": contract["contract_id"],
        "Aikens_lambda_outcome_opened": False,
        "status": "INTERVAL_STANDARDIZATION_SECONDARY_COORDINATES_COMPLETE",
        "systems": output_systems,
        "claim_boundary": [
            "raw lambda remains the system-specific primary estimator",
            "k_eq is an equivalent reference-interval transformation, not a fitted continuous-time controller rate",
            "negative lambda sign remains a separate overshoot flag",
            "path-memory retention propagates only the initial-error memory component under a homogeneous-lambda approximation",
            "whole-route path retention is not licensed for the highlighted goose fixed transitions",
            "SIMEX variants remain measurement-error sensitivities rather than corrected truth",
            "the Aikens lambda outcome remains unopened and its preregistered contrast is unchanged",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    result = build_result(contract)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
