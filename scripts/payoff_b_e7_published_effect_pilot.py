#!/usr/bin/env python3
"""Nonpromotable E7 diagnostic.

This script intentionally computes what an ordinary three-study random-effects
meta-analysis would return IF the registered diagnostic uncertainty
approximations were treated as standard errors. That IF is false for at least
two source systems. The output is therefore a stress test for heterogeneity,
not an inferential result.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def dl_meta(rows: list[dict]) -> dict:
    y = [float(r["effect"]) for r in rows]
    se = [float(r["diagnostic_se"]) for r in rows]
    v = [x * x for x in se]
    w = [1.0 / x for x in v]
    sw = sum(w)
    mu_fixed = sum(a * b for a, b in zip(w, y)) / sw
    q = sum(a * (b - mu_fixed) ** 2 for a, b in zip(w, y))
    df = len(y) - 1
    c = sw - sum(a * a for a in w) / sw
    tau2 = max(0.0, (q - df) / c) if c > 0 else 0.0
    wr = [1.0 / (vv + tau2) for vv in v]
    swr = sum(wr)
    mu_random = sum(a * b for a, b in zip(wr, y)) / swr
    se_random = math.sqrt(1.0 / swr)
    i2 = max(0.0, (q - df) / q) * 100.0 if q > 0 else 0.0
    max_weight_fixed = max(w) / sw
    max_weight_random = max(wr) / swr
    return {
        "k": len(y),
        "fixed_mean": mu_fixed,
        "Q": q,
        "Q_df": df,
        "tau2_DL": tau2,
        "I2_percent_diagnostic": i2,
        "random_mean": mu_random,
        "random_se": se_random,
        "random_normal_ci95": [
            mu_random - 1.96 * se_random,
            mu_random + 1.96 * se_random,
        ],
        "max_fixed_weight_fraction": max_weight_fixed,
        "max_random_weight_fraction": max_weight_random,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if payload.get("status") != "NONPROMOTABLE_DIAGNOSTIC":
        raise SystemExit("refusing to run unless input is explicitly NONPROMOTABLE_DIAGNOSTIC")
    if any(row.get("inferential_variance_valid") is not False for row in payload["rows"]):
        raise SystemExit("diagnostic contract requires inferential_variance_valid=false for every row")

    meta = dl_meta(payload["rows"])
    result = {
        "result_id": "payoff_b_e7_published_effect_pilot_result_20260928",
        "status": "NONPROMOTABLE_DIAGNOSTIC_ONLY",
        "effect_definition": payload["effect_definition"],
        "source_point_estimates": [
            {"study": r["study"], "effect": r["effect"]}
            for r in payload["rows"]
        ],
        "diagnostic_meta_if_invalid_SE_assumptions_are_forced": meta,
        "ecological_readout": {
            "signs": [
                "positive" if r["effect"] > 0 else "negative" if r["effect"] < 0 else "zero"
                for r in payload["rows"]
            ],
            "universal_partner_ordering_supported": False,
            "heterogeneity_large_under_diagnostic_weights": meta["I2_percent_diagnostic"] > 50,
        },
        "promotion": {
            "allowed": False,
            "reason": (
                "At least two study-level delta variances depend on unverified "
                "zero-covariance and/or SE-label assumptions. The pooled mean, "
                "CI, tau2 and I2 are stress-test diagnostics only."
            ),
        },
        "hard_boundary": payload["hard_boundary"],
    }

    assert result["status"] == "NONPROMOTABLE_DIAGNOSTIC_ONLY"
    assert result["promotion"]["allowed"] is False
    assert len(set(result["ecological_readout"]["signs"])) > 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
