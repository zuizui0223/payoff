#!/usr/bin/env python3
"""Prospective greater-snow-goose downstream compensation screen.

A supported registered signal means the focal cue may also alter downstream
compensation, so cue-independent fixed-D_eff promotion is blocked.
A null result does not prove cue exogeneity.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.snow_goose_dual_use_screen import (
    classify_dual_use_compensation_signal,
    evaluate_compensation_screen_estimability,
)


ROUTE_ORDER = {
    "St_Lawrence": 0,
    "Nunavik": 1,
    "Baffin": 2,
    "Bylot": 3,
}

ALLOWED_SEGMENTS = {
    (origin, destination)
    for origin, origin_order in ROUTE_ORDER.items()
    for destination, destination_order in ROUTE_ORDER.items()
    if origin_order < destination_order and origin != "Bylot"
}

REQUIRED = {
    "individual",
    "year",
    "origin_context",
    "destination_context",
    "departure_date",
    "transit_duration_days",
    "wait_days_in_origin",
    "local_temp_anom3",
    "same_day_temp_anom",
    "day_of_year_within_context",
    "wind_support",
    "precipitation",
    "predictive_connectivity_rho",
    "connectivity_training_n",
    "connectivity_window_end_year",
}

PRIMARY_FORMULA = (
    "log_transit_duration_days ~ "
    "local_temp_anom3 * z_predictive_connectivity "
    "+ z_wait_days + day_of_year_within_context "
    "+ wind_support + precipitation + same_day_temp_anom "
    "+ C(route_segment) + C(year)"
)

SECONDARY_FORMULA = (
    "log_transit_duration_days ~ "
    "local_temp_anom3 * z_predictive_connectivity * z_wait_days "
    "+ day_of_year_within_context "
    "+ wind_support + precipitation + same_day_temp_anom "
    "+ C(route_segment) + C(year)"
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--transitions", type=Path, required=True)
    p.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/payoff_b_greater_snow_goose_dual_use_screen.json"
        ),
    )
    return p.parse_args()


def _zscore(series, name):
    mean = float(series.mean())
    sd = float(series.std(ddof=0))
    if not math.isfinite(sd) or sd <= 0.0:
        raise ValueError(f"{name} has no variance")
    return (series.astype(float) - mean) / sd, sd


def main():
    args = parse_args()
    try:
        import numpy as np
        import pandas as pd
        import statsmodels.formula.api as smf
    except ImportError as exc:
        raise RuntimeError(
            "snow-goose compensation screen requires empirical dependencies"
        ) from exc

    data = pd.read_csv(args.transitions)
    missing = REQUIRED - set(data.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    if data.empty:
        raise ValueError("transition table is empty")
    if data[list(REQUIRED)].isna().any().any():
        raise ValueError("required transition columns contain missing values")

    pairs = set(
        zip(
            data["origin_context"].astype(str),
            data["destination_context"].astype(str),
        )
    )
    invalid = pairs - ALLOWED_SEGMENTS
    if invalid:
        raise ValueError(f"unexpected route segments: {sorted(invalid)}")

    data["year"] = data["year"].astype(int)
    data["route_segment"] = (
        data["origin_context"].astype(str)
        + "__"
        + data["destination_context"].astype(str)
    )
    data["skip_next_context"] = [
        int(
            ROUTE_ORDER[str(destination)]
            - ROUTE_ORDER[str(origin)]
            > 1
        )
        for origin, destination in zip(
            data["origin_context"],
            data["destination_context"],
        )
    ]
    data["transit_duration_days"] = pd.to_numeric(
        data["transit_duration_days"], errors="raise"
    )
    data["wait_days_in_origin"] = pd.to_numeric(
        data["wait_days_in_origin"], errors="raise"
    )
    if (data["transit_duration_days"] <= 0).any():
        raise ValueError("transit_duration_days must be positive")
    if (data["wait_days_in_origin"] < 0).any():
        raise ValueError("wait_days_in_origin must be non-negative")

    numeric = [
        "local_temp_anom3",
        "same_day_temp_anom",
        "day_of_year_within_context",
        "wind_support",
        "precipitation",
        "predictive_connectivity_rho",
    ]
    for col in numeric:
        data[col] = pd.to_numeric(data[col], errors="raise")
        if not np.isfinite(data[col].to_numpy(dtype=float)).all():
            raise ValueError(f"{col} contains non-finite values")

    if (
        (data["predictive_connectivity_rho"] < -1.0)
        | (data["predictive_connectivity_rho"] > 1.0)
    ).any():
        raise ValueError("predictive_connectivity_rho must lie in [-1,1]")
    if (data["connectivity_training_n"].astype(int) < 15).any():
        raise ValueError("connectivity training n below frozen minimum")
    if (
        data["connectivity_window_end_year"].astype(int)
        > data["year"].astype(int) - 1
    ).any():
        raise ValueError("predictive connectivity leaks focal/future year")

    data["z_predictive_connectivity"], rho_sd = _zscore(
        data["predictive_connectivity_rho"],
        "predictive_connectivity_rho",
    )
    data["z_wait_days"], wait_sd = _zscore(
        data["wait_days_in_origin"],
        "wait_days_in_origin",
    )
    data["log_transit_duration_days"] = np.log(
        data["transit_duration_days"].astype(float)
    )
    data["context_year_cell"] = (
        data["origin_context"].astype(str)
        + "__"
        + data["year"].astype(str)
    )

    gate = evaluate_compensation_screen_estimability(
        individuals=int(data["individual"].astype(str).nunique()),
        years=int(data["year"].nunique()),
        origin_contexts=int(data["origin_context"].astype(str).nunique()),
        transitions=int(len(data)),
        context_year_cells=int(data["context_year_cell"].nunique()),
        predictive_connectivity_sd=rho_sd,
        wait_days_sd=wait_sd,
    )

    result = {
        "registration_id": (
            "payoff_b_greater_snow_goose_dual_use_compensation_screen_v1_20260930"
        ),
        "status": "NOT_ESTIMABLE",
        "estimability_gate": {
            "estimable": gate.estimable,
            "reasons": list(gate.reasons),
            "individuals": gate.individuals,
            "years": gate.years,
            "origin_contexts": gate.origin_contexts,
            "transitions": gate.transitions,
            "context_year_cells": gate.context_year_cells,
            "predictive_connectivity_sd": gate.predictive_connectivity_sd,
            "wait_days_sd": gate.wait_days_sd,
        },
        "primary": None,
        "secondary_wait_dependence": None,
        "secondary_route_skip": None,
        "claim_boundary": [
            "behavioral compensation screen only",
            "supported signal blocks fixed-D_eff promotion but does not prove cue cognition",
            "null does not establish cue exogeneity",
            "does not estimate D_eff or q_wait",
        ],
    }

    if gate.estimable:
        fit = smf.ols(PRIMARY_FORMULA, data=data).fit(
            cov_type="cluster",
            cov_kwds={"groups": data["individual"].astype(str)},
        )
        term = "local_temp_anom3:z_predictive_connectivity"
        if term not in fit.params.index:
            raise RuntimeError(f"primary interaction missing: {term}")
        estimate = float(fit.params[term])
        se = float(fit.bse[term])

        loo_estimates = []
        for cell in sorted(data["context_year_cell"].unique()):
            reduced = data[data["context_year_cell"] != cell].copy()
            reduced_fit = smf.ols(PRIMARY_FORMULA, data=reduced).fit()
            if term not in reduced_fit.params.index:
                raise RuntimeError(
                    f"LOO primary interaction missing after dropping {cell}"
                )
            loo_estimates.append(
                {
                    "dropped_context_year": str(cell),
                    "estimate": float(reduced_fit.params[term]),
                }
            )
        loo_all_negative = all(
            row["estimate"] < 0.0 for row in loo_estimates
        )

        classification = classify_dual_use_compensation_signal(
            estimable=True,
            interaction_estimate=estimate,
            interaction_se=se,
            loo_all_negative=loo_all_negative,
        )
        result["status"] = classification.status
        result["primary"] = {
            "formula": PRIMARY_FORMULA,
            "term": term,
            "estimate": estimate,
            "cluster_se": se,
            "ci_low_95": classification.ci_low_95,
            "ci_high_95": classification.ci_high_95,
            "registered_direction": "negative",
            "loo_context_year_estimates": loo_estimates,
            "loo_all_negative": loo_all_negative,
            "interpretation": classification.interpretation,
        }

        try:
            secondary = smf.ols(SECONDARY_FORMULA, data=data).fit(
                cov_type="cluster",
                cov_kwds={"groups": data["individual"].astype(str)},
            )
            three = (
                "local_temp_anom3:"
                "z_predictive_connectivity:"
                "z_wait_days"
            )
            result["secondary_wait_dependence"] = {
                "formula": SECONDARY_FORMULA,
                "term": three,
                "estimate": (
                    float(secondary.params[three])
                    if three in secondary.params.index
                    else None
                ),
                "cluster_se": (
                    float(secondary.bse[three])
                    if three in secondary.bse.index
                    else None
                ),
                "registered_direction": "negative",
                "role": (
                    "secondary diagnostic: stronger cue-linked transit "
                    "compression after longer waiting"
                ),
            }
        except Exception as exc:
            result["secondary_wait_dependence"] = {
                "status": "NOT_ESTIMABLE",
                "reason": type(exc).__name__,
            }

        try:
            eligible_skip = data[
                data["origin_context"].isin(["St_Lawrence", "Nunavik"])
            ].copy()
            if (
                len(eligible_skip) >= 50
                and eligible_skip["skip_next_context"].nunique() == 2
            ):
                import statsmodels.api as sm
                import statsmodels.formula.api as smf

                skip_formula = (
                    "skip_next_context ~ "
                    "local_temp_anom3 * z_predictive_connectivity "
                    "+ z_wait_days + day_of_year_within_context "
                    "+ wind_support + precipitation + same_day_temp_anom "
                    "+ C(origin_context) + C(year)"
                )
                skip_fit = smf.glm(
                    skip_formula,
                    data=eligible_skip,
                    family=sm.families.Binomial(),
                ).fit(
                    cov_type="cluster",
                    cov_kwds={
                        "groups": eligible_skip["individual"].astype(str)
                    },
                )
                skip_term = "local_temp_anom3:z_predictive_connectivity"
                result["secondary_route_skip"] = {
                    "formula": skip_formula,
                    "term": skip_term,
                    "estimate": float(skip_fit.params[skip_term]),
                    "cluster_se": float(skip_fit.bse[skip_term]),
                    "registered_direction": "positive",
                    "role": (
                        "secondary actuator diagnostic: warm predictive "
                        "cues increase probability of skipping the next "
                        "intermediate route context"
                    ),
                }
            else:
                result["secondary_route_skip"] = {
                    "status": "NOT_ESTIMABLE",
                    "reason": "INSUFFICIENT_SKIP_VARIATION_OR_ROWS",
                }
        except Exception as exc:
            result["secondary_route_skip"] = {
                "status": "NOT_ESTIMABLE",
                "reason": type(exc).__name__,
            }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
