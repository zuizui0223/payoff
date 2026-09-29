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
    adjudicate_threshold_folds,
    dual_cluster_direction_supported,
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
    ys = [float(v) for v in y]
    ps = [min(1.0 - eps, max(eps, float(v))) for v in p]
    if len(ys) != len(ps) or not ys:
        raise ValueError("response and prediction vectors must align")
    return -sum(
        yy * math.log(pp) + (1.0 - yy) * math.log(1.0 - pp)
        for yy, pp in zip(ys, ps)
    ) / len(ys)


def _mean_se(values):
    values = [float(v) for v in values]
    if not values:
        return None, None
    mean = sum(values) / len(values)
    if len(values) < 2:
        return mean, None
    variance = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
    return mean, math.sqrt(variance / len(values))


def main():
    args = parse_args()

    import numpy as np
    import pandas as pd
    import statsmodels.formula.api as smf
    from scipy.stats import t as student_t

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

    expected_contexts = {
        "southern_staging",
        "mid_arctic_staging",
        "northern_arctic_staging",
    }
    observed_contexts = set(data["context"].astype(str).unique())
    if observed_contexts != expected_contexts:
        raise ValueError(
            "shared staging contexts do not match frozen south/mid/north mapping"
        )

    if not set(data["depart_next_24h"].dropna().unique()).issubset({0, 1}):
        raise ValueError("depart_next_24h must be binary")
    numeric_required = [
        "local_temp_anom3",
        "day_of_year_within_context",
        "wind_support",
        "precipitation",
        "connectivity_rho",
    ]
    for column in numeric_required:
        values = pd.to_numeric(data[column], errors="coerce")
        if values.isna().any() or not np.isfinite(values.to_numpy()).all():
            raise ValueError(f"{column} contains missing or non-finite values")
        data[column] = values

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
    context_year = (
        data[["context", "year", "connectivity_rho"]]
        .drop_duplicates()
        .copy()
    )
    context_year["context_year"] = (
        context_year["context"].astype(str)
        + "::"
        + context_year["year"].astype(str)
    )
    rho_sd = float(context_year["connectivity_rho"].std(ddof=0))
    within_context_sds = []
    for context in sorted(expected_contexts):
        values = context_year.loc[
            context_year["context"].astype(str) == context,
            "connectivity_rho",
        ].astype(float)
        within_context_sds.append(
            float(values.std(ddof=0)) if len(values) >= 2 else 0.0
        )
    minimum_within_context_sd = min(within_context_sds)

    data["context_year"] = (
        data["context"].astype(str) + "::" + data["year"].astype(str)
    )
    gate = evaluate_estimability(
        individuals=int(data["individual_id"].nunique()),
        years=int(data["year"].nunique()),
        contexts=int(data["context"].nunique()),
        departure_events=int(data["depart_next_24h"].sum()),
        context_years=int(context_year["context_year"].nunique()),
        predictive_connectivity_sd=rho_sd,
        minimum_within_context_connectivity_sd=minimum_within_context_sd,
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
            "context_years": gate.context_years,
            "predictive_connectivity_sd": gate.predictive_connectivity_sd,
            "minimum_within_context_connectivity_sd": (
                gate.minimum_within_context_connectivity_sd
            ),
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
    term = "local_temp_anom3:z_predictive_connectivity"
    try:
        base_fit = smf.logit(formula, data=data).fit(
            disp=False,
            maxiter=200,
        )
        fit_individual = smf.logit(formula, data=data).fit(
            disp=False,
            maxiter=200,
            cov_type="cluster",
            cov_kwds={"groups": data["individual_id"].astype(str)},
        )
        fit_context_year = smf.logit(formula, data=data).fit(
            disp=False,
            maxiter=200,
            cov_type="cluster",
            cov_kwds={"groups": data["context_year"].astype(str)},
        )
    except Exception as exc:
        result["status"] = "PRIMARY_MODEL_FIT_FAILED"
        result["primary"] = {
            "formula": formula,
            "term": term,
            "support_status": "NOT_ESTIMABLE",
            "failure_type": type(exc).__name__,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        return

    beta = float(base_fit.params[term])
    n_individual_clusters = int(data["individual_id"].astype(str).nunique())
    n_context_year_clusters = int(data["context_year"].astype(str).nunique())

    def cluster_summary(fit, clusters):
        se = float(fit.bse[term])
        df = int(clusters) - 1
        critical = float(student_t.ppf(0.975, df))
        statistic = beta / se
        p_value = float(2.0 * student_t.sf(abs(statistic), df))
        return {
            "clusters": int(clusters),
            "df": df,
            "standard_error": se,
            "critical_t_95": critical,
            "ci_low_95": beta - critical * se,
            "ci_high_95": beta + critical * se,
            "p_value_two_sided": p_value,
        }

    individual_inference = cluster_summary(
        fit_individual,
        n_individual_clusters,
    )
    context_year_inference = cluster_summary(
        fit_context_year,
        n_context_year_clusters,
    )
    supported = dual_cluster_direction_supported(
        beta,
        individual_inference["ci_low_95"],
        context_year_inference["ci_low_95"],
    )

    result["primary"] = {
        "formula": formula,
        "term": term,
        "estimate": beta,
        "registered_direction": "positive",
        "individual_cluster": individual_inference,
        "context_year_cluster": context_year_inference,
        "support_rule": (
            "positive estimate with positive Student-t 95% CI lower bound "
            "under both individual and context-year clustering"
        ),
        "support_status": (
            "SUPPORTED" if supported else "NOT_SUPPORTED"
        ),
    }

    # Secondary threshold-like uptake.  We keep the no-threshold model as a
    # comparator and score every frozen candidate with LOIO log loss.
    individuals = sorted(data["individual_id"].astype(str).unique())
    candidates = [None, *FROZEN_Q_GRID]
    fold_losses_by_candidate = {}

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
                train["cue_active"] = (
                    train["q_bridge"] >= threshold
                ).astype(int)
                test["cue_active"] = (
                    test["q_bridge"] >= threshold
                ).astype(int)
                threshold_formula = (
                    "depart_next_24h ~ local_temp_anom3 * cue_active "
                    "+ day_of_year_within_context + wind_support + precipitation "
                    "+ C(context) + C(year)"
                )

            try:
                model = smf.logit(
                    threshold_formula,
                    data=train,
                ).fit(disp=False, maxiter=200)
                pred = model.predict(test)
                fold_losses.append(
                    _log_loss(test["depart_next_24h"], pred)
                )
            except Exception:
                fold_losses = []
                break

        fold_losses_by_candidate[threshold] = fold_losses

    no_threshold_losses = fold_losses_by_candidate.get(None, [])
    candidate_losses = {
        q: fold_losses_by_candidate.get(q, [])
        for q in FROZEN_Q_GRID
    }
    adjudication = adjudicate_threshold_folds(
        no_threshold_losses=no_threshold_losses,
        candidate_losses=candidate_losses,
    )

    scores = []
    for threshold in candidates:
        losses = fold_losses_by_candidate[threshold]
        mean_loss, se_loss = _mean_se(losses)
        scores.append({
            "threshold_q": threshold,
            "mean_loio_log_loss": mean_loss,
            "se_across_individual_folds": se_loss,
            "individual_folds": len(losses),
            "fold_losses": losses,
        })

    result["threshold_secondary"] = {
        "candidate_scores": scores,
        "status": adjudication.status,
        "selected_threshold_q": adjudication.selected_threshold_q,
        "selected_mean_log_loss": adjudication.selected_mean_log_loss,
        "no_threshold_mean_log_loss": adjudication.no_threshold_mean_log_loss,
        "lower_neighbor_q": adjudication.lower_neighbor_q,
        "upper_neighbor_q": adjudication.upper_neighbor_q,
        "lower_paired_mean_difference": (
            adjudication.lower_paired_mean_difference
        ),
        "upper_paired_mean_difference": (
            adjudication.upper_paired_mean_difference
        ),
        "lower_paired_se": adjudication.lower_paired_se,
        "upper_paired_se": adjudication.upper_paired_se,
        "reasons": list(adjudication.reasons),
        "support_rule": (
            "selected threshold must be interior, beat no-threshold mean "
            "LOIO log loss, and beat both adjacent q-grid points by more "
            "than one SE of the paired individual-fold loss difference"
        ),
        "claim_boundary": (
            "behavioral threshold-like candidate only; never q_wait(D)"
        ),
    }

    if args.rows_output is not None:
        args.rows_output.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(args.rows_output, index=False)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
