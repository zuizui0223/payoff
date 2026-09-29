#!/usr/bin/env python3
"""Prospective greater-snow-goose GPS cue-uptake analysis.

This script consumes *already frozen* movement day-risk rows and historical
predictive-connectivity rows.  It does not draw stopover polygons, alter the
movepp segmentation, or use focal-year future Bylot conditions to construct q.

Primary:
    depart_next_24h ~ local_temp_anom3 * z_predictive_connectivity
        + day_of_year_within_context + wind_support + precipitation
        + C(context) + C(year)

Secondary:
    frozen q-grid threshold models selected by leave-one-individual-out
    predictive log loss.  This is descriptive behavioral uptake only and must
    not be called q_wait(D).
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from src.greater_snow_goose_cue_uptake import (
    FROZEN_Q_GRID,
    evaluate_estimability,
    gaussian_binary_q,
    preoutcome_training_valid,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--day-risk", type=Path, required=True)
    p.add_argument("--connectivity", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--rows-output", type=Path)
    return p.parse_args()


def _log_loss(y, p):
    eps = 1e-12
    p = p.clip(eps, 1.0 - eps)
    return float(-(y * p.apply(math.log) + (1-y) * (1-p).apply(math.log)).mean())


def main():
    args = parse_args()

    import numpy as np
    import pandas as pd
    import statsmodels.formula.api as smf

    day = pd.read_csv(args.day_risk)
    conn = pd.read_csv(args.connectivity)

    required_day = {
        "individual_id", "year", "context", "depart_next_24h",
        "local_temp_anom3", "day_of_year_within_context",
        "wind_support", "precipitation",
    }
    required_conn = {
        "context", "year", "connectivity_rho",
        "training_end_year", "training_years",
    }
    if not required_day.issubset(day.columns):
        raise ValueError(
            "day-risk columns incomplete: "
            + ",".join(sorted(required_day - set(day.columns)))
        )
    if not required_conn.issubset(conn.columns):
        raise ValueError(
            "connectivity columns incomplete: "
            + ",".join(sorted(required_conn - set(conn.columns)))
        )

    data = day.merge(
        conn,
        on=["context", "year"],
        how="left",
        validate="many_to_one",
    )
    if data["connectivity_rho"].isna().any():
        raise ValueError("missing connectivity after context-year join")

    invalid_history = [
        not preoutcome_training_valid(
            focal_year=int(row.year),
            training_end_year=int(row.training_end_year),
            training_years=int(row.training_years),
        )
        for row in data.itertuples(index=False)
    ]
    if any(invalid_history):
        raise ValueError("predictive connectivity violates pre-outcome history rule")

    data["q_bridge"] = data["connectivity_rho"].map(gaussian_binary_q)
    rho_sd = float(data["connectivity_rho"].std(ddof=0))
    gate = evaluate_estimability(
        individuals=int(data["individual_id"].nunique()),
        years=int(data["year"].nunique()),
        contexts=int(data["context"].nunique()),
        departure_events=int(data["depart_next_24h"].sum()),
        predictive_connectivity_sd=rho_sd,
    )

    result = {
        "registration_id": "payoff_b_greater_snow_goose_gps_cue_uptake_v1_20260929",
        "status": "ESTIMABLE" if gate.estimable else "NOT_ESTIMABLE",
        "gate": {
            "estimable": gate.estimable,
            "reasons": list(gate.reasons),
            "individuals": gate.individuals,
            "years": gate.years,
            "contexts": gate.contexts,
            "departure_events": gate.departure_events,
            "predictive_connectivity_sd": gate.predictive_connectivity_sd,
        },
        "claim_boundary": [
            "behavioral cue-uptake proxy only",
            "not direct observation of cue cognition",
            "not q_wait(D)",
            "captivity duration is not identified PAYOFF-B D",
        ],
    }

    if not gate.estimable:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        return

    rho_mean = float(data["connectivity_rho"].mean())
    if rho_sd <= 0:
        raise ValueError("connectivity has no variance")
    data["z_predictive_connectivity"] = (
        data["connectivity_rho"] - rho_mean
    ) / rho_sd

    formula = (
        "depart_next_24h ~ local_temp_anom3 * z_predictive_connectivity "
        "+ day_of_year_within_context + wind_support + precipitation "
        "+ C(context) + C(year)"
    )
    fit = smf.logit(formula, data=data).fit(disp=False)
    robust = fit.get_robustcov_results(
        cov_type="cluster",
        groups=data["individual_id"].astype(str),
    )
    names = list(fit.model.exog_names)
    term = "local_temp_anom3:z_predictive_connectivity"
    idx = names.index(term)
    beta = float(robust.params[idx])
    se = float(robust.bse[idx])
    p = float(robust.pvalues[idx])
    ci = [beta - 1.96 * se, beta + 1.96 * se]

    result["primary"] = {
        "formula": formula,
        "term": term,
        "estimate": beta,
        "cluster_se": se,
        "ci_low_95": ci[0],
        "ci_high_95": ci[1],
        "p_value_two_sided": p,
        "registered_direction": "positive",
        "support_status": (
            "SUPPORTED" if beta > 0 and ci[0] > 0 else "NOT_SUPPORTED"
        ),
    }

    # Secondary threshold-like uptake.  We keep the no-threshold model as a
    # comparator and score every frozen candidate with LOIO log loss.
    individuals = sorted(data["individual_id"].astype(str).unique())
    candidates = [None, *FROZEN_Q_GRID]
    scores = []

    for threshold in candidates:
        fold_losses = []
        for held_out in individuals:
            train = data[data["individual_id"].astype(str) != held_out].copy()
            test = data[data["individual_id"].astype(str) == held_out].copy()

            if threshold is None:
                threshold_formula = (
                    "depart_next_24h ~ local_temp_anom3 "
                    "+ day_of_year_within_context + wind_support + precipitation "
                    "+ C(context) + C(year)"
                )
            else:
                train["cue_active"] = (train["q_bridge"] >= threshold).astype(int)
                test["cue_active"] = (test["q_bridge"] >= threshold).astype(int)
                threshold_formula = (
                    "depart_next_24h ~ local_temp_anom3 * cue_active "
                    "+ day_of_year_within_context + wind_support + precipitation "
                    "+ C(context) + C(year)"
                )

            try:
                model = smf.logit(threshold_formula, data=train).fit(disp=False)
                pred = model.predict(test)
                fold_losses.append(_log_loss(test["depart_next_24h"], pred))
            except Exception:
                fold_losses = []
                break

        scores.append({
            "threshold_q": threshold,
            "mean_loio_log_loss": (
                float(np.mean(fold_losses)) if fold_losses else None
            ),
            "individual_folds": len(fold_losses),
        })

    valid = [row for row in scores if row["mean_loio_log_loss"] is not None]
    threshold_rows = [row for row in valid if row["threshold_q"] is not None]
    no_threshold = next(
        (row for row in valid if row["threshold_q"] is None),
        None,
    )
    selected = min(
        threshold_rows,
        key=lambda row: row["mean_loio_log_loss"],
        default=None,
    )

    result["threshold_secondary"] = {
        "candidate_scores": scores,
        "selected_threshold_q": (
            selected["threshold_q"] if selected is not None else None
        ),
        "no_threshold_log_loss": (
            no_threshold["mean_loio_log_loss"]
            if no_threshold is not None else None
        ),
        "status": (
            "DESCRIPTIVE_CANDIDATE_ONLY"
            if selected is not None else "THRESHOLD_NOT_IDENTIFIED"
        ),
        "note": (
            "1-SE adjacency support gate requires fold-level SE and is "
            "adjudicated only if all candidates fit; no q_wait(D) claim allowed."
        ),
    }

    if args.rows_output is not None:
        args.rows_output.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(args.rows_output, index=False)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
