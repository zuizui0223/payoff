#!/usr/bin/env python3
"""Post-freeze barnacle-goose route variance-geometry audit.

The analysis is frozen by
data/payoff_b_barnacle_variance_geometry_contract_20261003.json.

It uses exactly the highlighted transition rows already used for the frozen
barnacle-goose phase-retention estimates. It does not alter those estimates and
does not treat the three flyways as independent taxa.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data" / "payoff_b_barnacle_variance_geometry_rows_20261003.csv"
CONTRACT = ROOT / "data" / "payoff_b_barnacle_variance_geometry_contract_20261003.json"


def mean(xs):
    return sum(xs) / len(xs)


def sample_var(xs):
    if len(xs) < 2:
        raise ValueError("sample variance requires >=2 values")
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def sample_cov(xs, ys):
    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("covariance requires equal vectors of length >=2")
    mx, my = mean(xs), mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)


def percentile(xs, p):
    vals = sorted(xs)
    if not vals:
        raise ValueError("empty percentile input")
    if len(vals) == 1:
        return vals[0]
    pos = (len(vals) - 1) * p
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return vals[lo]
    frac = pos - lo
    return vals[lo] * (1 - frac) + vals[hi] * frac


def ci95(xs):
    return [percentile(xs, 0.025), percentile(xs, 0.975)]


def route_metrics(rows):
    x = [float(r["origin_phase"]) for r in rows]
    y = [float(r["destination_phase"]) for r in rows]
    vx = sample_var(x)
    vy = sample_var(y)
    lam = sample_cov(x, y) / vx
    intercept = mean(y) - lam * mean(x)
    residuals = [yy - (intercept + lam * xx) for xx, yy in zip(x, y)]
    resid_var = sample_var(residuals)
    ratio = vy / vx
    residual_ratio = resid_var / vx
    identity_error = ratio - (lam * lam + residual_ratio)
    inherited_fraction = (lam * lam / ratio) if ratio > 0 else None
    return {
        "n": len(rows),
        "n_individuals": len({str(r["individual_id"]) for r in rows}),
        "origin_mean": mean(x),
        "destination_mean": mean(y),
        "origin_variance": vx,
        "destination_variance": vy,
        "variance_ratio": ratio,
        "sd_ratio": math.sqrt(ratio),
        "lambda_hat": lam,
        "lambda_squared": lam * lam,
        "normalized_residual_variance": residual_ratio,
        "inherited_destination_variance_fraction": inherited_fraction,
        "ols_variance_identity_error": identity_error,
        "variance_class": (
            "CONTRACTION" if ratio < 1.0 else
            "EXPANSION" if ratio > 1.0 else
            "NO_CHANGE"
        ),
    }


def bootstrap(rows, replicates, seed):
    ids = sorted({str(r["individual_id"]) for r in rows})
    by_id = defaultdict(list)
    for row in rows:
        by_id[str(row["individual_id"])].append(row)
    rng = random.Random(seed)
    vals = defaultdict(list)

    for _ in range(replicates):
        sampled_ids = [rng.choice(ids) for _ in ids]
        sample = []
        for individual in sampled_ids:
            sample.extend(by_id[individual])
        try:
            m = route_metrics(sample)
        except (ValueError, ZeroDivisionError):
            continue
        for key in (
            "variance_ratio",
            "lambda_hat",
            "normalized_residual_variance",
            "inherited_destination_variance_fraction",
        ):
            value = m[key]
            if value is not None and math.isfinite(value):
                vals[key].append(value)

    return {
        "cluster_unit": "individual_id",
        "unique_individuals": len(ids),
        "replicates_requested": replicates,
        "replicates_completed": len(vals["variance_ratio"]),
        "seed": seed,
        "variance_ratio_ci95": ci95(vals["variance_ratio"]),
        "lambda_ci95": ci95(vals["lambda_hat"]),
        "normalized_residual_variance_ci95": ci95(
            vals["normalized_residual_variance"]
        ),
        "inherited_destination_variance_fraction_ci95": ci95(
            vals["inherited_destination_variance_fraction"]
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/payoff_b_barnacle_variance_geometry_result.json"),
    )
    parser.add_argument("--bootstrap-replicates", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20261003)
    args = parser.parse_args()

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    with ROWS.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    result_routes = []
    for i, spec in enumerate(contract["routes"]):
        subset = [
            row for row in rows
            if row["flyway"] == spec["flyway"]
            and row["origin_region"] == spec["origin"]
            and row["destination_region"] == spec["destination"]
        ]
        metrics = route_metrics(subset)
        if metrics["n"] < spec["minimum_n"]:
            raise SystemExit(
                f"{spec['flyway']} support too small: {metrics['n']}"
            )
        if metrics["n_individuals"] < spec["minimum_individuals"]:
            raise SystemExit(
                f"{spec['flyway']} individual support too small: "
                f"{metrics['n_individuals']}"
            )
        if abs(metrics["lambda_hat"] - spec["known_lambda"]) > 1e-12:
            raise SystemExit(
                f"{spec['flyway']} lambda identity failed: "
                f"{metrics['lambda_hat']} vs {spec['known_lambda']}"
            )
        if abs(metrics["ols_variance_identity_error"]) > 1e-10:
            raise SystemExit(
                f"{spec['flyway']} OLS variance identity failed"
            )
        boot = bootstrap(
            subset,
            args.bootstrap_replicates,
            args.seed + i,
        )
        result_routes.append(
            {
                "flyway": spec["flyway"],
                "route": f"{spec['origin']}->{spec['destination']}",
                **metrics,
                "bootstrap": boot,
            }
        )

    result = {
        "date": "2026-10-03",
        "status": "POSTFREEZE_DESCRIPTIVE_VARIANCE_GEOMETRY_AUDIT",
        "frozen_submission_affected": False,
        "contract": str(CONTRACT.relative_to(ROOT)),
        "source_rows": str(ROWS.relative_to(ROOT)),
        "routes": result_routes,
        "synthesis": {
            "all_lambda_abs_below_one": all(
                abs(row["lambda_hat"]) < 1 for row in result_routes
            ),
            "all_variance_ratios_below_one": all(
                row["variance_ratio"] < 1 for row in result_routes
            ),
            "key_result": (
                "mean phase memory and population phase dispersion are "
                "different response coordinates"
            ),
            "no_pooled_goose_variance_ratio": True,
        },
        "boundaries": contract["forbidden_claims"],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
