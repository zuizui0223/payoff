"""Published 2015 Fig3 regional RMSD x incoming historical q (exploratory).

NOT frozen V7 region-year/animal response. NOT geographic urgency U.
Input: 13 printed original Fig3 site-level aggregated RMSDs + 23 original
supplement q coefficients. Fits only small-n descriptive aggregate models.
No individual GPS, annual climate, p-values, confidence intervals or causality.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from statistics import mean

from scripts.payoff_b_v7_suppinfo_aggregate_gate import (
    ROOT, QP, REGIONS, ROUTES, audit_pairs, readrows
)

PRINTED_RMSD = ROOT / "data/payoff_b_v7_fig3_printed_rmsd_20261119.csv"
BARRIER_CODES = {"SIC", "SGR", "SNO", "SVA", "WS"}
FLYWAYS = list(ROUTES)
ACTUAL_2015_DOI = "10.1111/1365-2656.12281"


def _rounded(value: float | None) -> float | None:
    return round(value, 9) if value is not None else None


def _solve(A: list[list[float]], b: list[float]) -> list[float]:
    """Small dense linear solve with pivoted elimination; reject rank failures."""
    n = len(b)
    if len(A) != n or any(len(row) != n for row in A):
        raise ValueError("matrix dimensions mismatch")
    mat = [A[i][:] + [b[i]] for i in range(n)]
    for j in range(n):
        pivot = max(range(j, n), key=lambda i: abs(mat[i][j]))
        if abs(mat[pivot][j]) < 1e-10:
            raise ValueError("aggregate design matrix rank deficient")
        mat[j], mat[pivot] = mat[pivot], mat[j]
        v = mat[j][j]
        for k in range(j, n+1):
            mat[j][k] /= v
        for i in range(n):
            if i == j:
                continue
            v = mat[i][j]
            for k in range(j, n+1):
                mat[i][k] -= v * mat[j][k]
    return [mat[i][n] for i in range(n)]


def _regress(X: list[list[float]], y: list[float],
             ridge: float = 0.0, penalize_intercept: bool = False) -> dict:
    if len(X) != len(y) or not X or len(X[0]) == 0:
        raise ValueError("empty or mismatched design")
    p = len(X[0])
    if any(len(row) != p for row in X):
        raise ValueError("inconsistent model columns")
    gram = [[sum(row[i]*row[j] for row in X) +
             (ridge if i == j and (i > 0 or penalize_intercept) else 0.)
             for j in range(p)] for i in range(p)]
    cross = [sum(row[i]*v for row, v in zip(X, y)) for i in range(p)]
    beta = _solve(gram, cross)
    predictions = [sum(x*b for x, b in zip(row, beta)) for row in X]
    sse = sum((v-yhat)**2 for v, yhat in zip(y, predictions))
    return {"beta": beta, "sse": sse, "prediction": predictions}


def _pearson(a: list[float], b: list[float]) -> float | None:
    if len(a) != len(b) or len(a) < 3:
        return None
    ma, mb = mean(a), mean(b)
    ss_a = sum((x-ma)**2 for x in a)
    ss_b = sum((x-mb)**2 for x in b)
    if ss_a <= 0 or ss_b <= 0:
        return None
    return sum((x-ma)*(y-mb) for x,y in zip(a,b)) / math.sqrt(ss_a*ss_b)


def _rank(v: list[float]) -> list[float]:
    out = [0.] * len(v)
    for _, inds in _group_sorted_ties(v):
        rank = sum(i+1 for i in inds)/len(inds)
        for i in inds:
            out[i] = rank
    return out


def _group_sorted_ties(values: list[float]):
    order = sorted(range(len(values)), key=lambda i: values[i])
    p = 0
    while p < len(order):
        stop = p+1
        while stop < len(order) and values[order[stop]] == values[order[p]]:
            stop += 1
        yield values[order[p]], list(range(p, stop)) if False else order[p:stop]
        p = stop


def _ols_columns(rows: list[dict], product: bool) -> list[list[float]]:
    return [
        [1., float(row["flyway"] == "Svalbard"),
         float(row["flyway"] == "Barents Sea"),
         row["q"], row["ordinal_stage"], float(row["barrier"])] +
        ([row["q"] * row["ordinal_stage"]] if product else [])
        for row in rows
    ]


def _fig3_rows(rows: list[dict] | None = None,
               q: list[dict] | None = None,
               s1: list[dict] | None = None) -> list[dict]:
    rows = readrows(PRINTED_RMSD) if rows is None else rows
    q = readrows(QP) if q is None else q
    s1 = readrows(REGIONS) if s1 is None else s1
    audit_pairs(q, s1)
    q_adj = {(r["flyway"],r["target_code"]):r
             for r in q if r["consecutive"] == "1"}
    if len(q_adj) != 13 or len(rows) != 13:
        raise ValueError("Expected exactly 13 published destination RMSD/q pairs")
    seen = set()
    joined = []
    for r in rows:
        f, c = r["flyway"],r["destination_region_code"]
        if f not in ROUTES or (f,c) not in q_adj or (f,c) in seen:
            raise ValueError("Fig3 destination not in consecutive source q")
        seen.add((f,c))
        try:
            rmsd = float(r["published_figure3_rmsd_days"])
        except ValueError as exc:
            raise ValueError("Unparseable Fig3 printed RMSD") from exc
        if (r["original_paper_doi"] != ACTUAL_2015_DOI
            or r["source_text"] != "Fig3 printed panel label"
            or not math.isfinite(rmsd) or rmsd <= 0 or rmsd >= 366):
            raise ValueError("Published figure source identity or RMSD invalid")
        expected_name = {
            "BALT":"Baltic States", "KAN":"Kanin Peninsula",
            "NSE":"Novaya Zemlya"
        }.get(c, next(x["region_S1_name"] for x in s1 if x["code"]==c))
        if r["figure3_printed_region"] != expected_name:
            raise ValueError("Fig3 region name differs from Table S1 candidate")
        orig = q_adj[(f,c)]
        step = ROUTES[f].index(c)
        if step < 1:
            raise ValueError("Invalid original destination route order")
        clean = (orig["source_alias_status"] == "exact"
                 and orig["target_alias_status"] == "exact")
        joined.append({
            "flyway": f,
            "source_code": orig["source_code"],
            "target_code": c,
            "fig3_panel": r["figure3_panel"],
            "rmsd_days_published_site_aggregate": rmsd,
            "q": float(orig["q_30year_correlation"]),
            "ordinal_stage": (step-1)/(len(ROUTES[f])-2),
            "barrier": c in BARRIER_CODES,
            "alias_clean": clean,
            "original_site_and_region_grains_differ": True,
        })
    if len(seen) != 13 or Counter(r["flyway"] for r in joined) != {
            "Greenland":4,"Svalbard":3,"Barents Sea":6}:
        raise ValueError("Original 13 printed Fig3 rows or route composition changed")
    if sum(r["alias_clean"] for r in joined) != 11:
        raise ValueError("Expected 11 q pairs free of unresolved original code labels")
    return joined


def _ols_summary(rows: list[dict]) -> dict:
    y = [r["rmsd_days_published_site_aggregate"] for r in rows]
    A = _regress(_ols_columns(rows, False), y)
    B = _regress(_ols_columns(rows, True), y)
    loocv_coeffs = []
    for drop in range(len(rows)):
        subset = rows[:drop]+rows[drop+1:]
        ysub = [r["rmsd_days_published_site_aggregate"] for r in subset]
        loocv_coeffs.append(_regress(_ols_columns(subset,True),ysub)["beta"][-1])
    return {
        "n_region_aggregates": len(rows),
        "n_additive_columns": 6,
        "n_plus_product_columns": 7,
        "nominal_full_model_residual_df_if_independent": len(rows)-7,
        "additive_SSE": _rounded(A["sse"]),
        "with_ordinal_product_SSE": _rounded(B["sse"]),
        "relative_in_sample_SSE_decrease": _rounded(
            1-B["sse"]/A["sse"] if A["sse"] > 0 else None),
        "additive_q_beta_days_per_unit_r": _rounded(A["beta"][3]),
        "product_model_q_beta_at_stage_zero": _rounded(B["beta"][3]),
        "product_model_ordinal_q_by_stage_beta": _rounded(B["beta"][-1]),
        "loocv_product_beta_min": _rounded(min(loocv_coeffs)),
        "loocv_product_beta_max": _rounded(max(loocv_coeffs)),
        "loocv_product_beta_positive_count": sum(b>0 for b in loocv_coeffs),
        "loocv_product_beta_negative_count": sum(b<0 for b in loocv_coeffs),
        "loocv_fit_omits_destination_only_not_independent_source_flyway":
            True,
        "p_values_CIs_and_independent_animal_replication": "NOT_REPORTED",
    }


def _ridge_features(rows: list[dict], train: list[dict], product: bool):
    # Freeze train-only standardization to prevent heldout flyway leakage.
    qm = mean(r["q"] for r in train)
    sm = mean(r["ordinal_stage"] for r in train)
    qsd = math.sqrt(mean((r["q"]-qm)**2 for r in train))
    ssd = math.sqrt(mean((r["ordinal_stage"]-sm)**2 for r in train))
    if qsd <= 0 or ssd <= 0:
        raise ValueError("Zero train-only standardization spread")
    def transform(row):
        zq = (row["q"] - qm)/qsd
        zs = (row["ordinal_stage"] - sm)/ssd
        return [1., zq, zs, float(row["barrier"])] + ([zq*zs] if product else [])
    return [transform(row) for row in rows]


def _lofo_ridge(rows: list[dict]) -> dict:
    by_flyway = {}
    weighted_errors = {False:[],True:[]}
    for hold in FLYWAYS:
        train = [r for r in rows if r["flyway"] != hold]
        test = [r for r in rows if r["flyway"] == hold]
        if not test or len(train) < 5:
            raise ValueError("Insufficient registered flyway groups")
        y_train = [r["rmsd_days_published_site_aggregate"] for r in train]
        y_test = [r["rmsd_days_published_site_aggregate"] for r in test]
        record = {"n_holdout_published_regions":len(test)}
        for product,label in ((False,"additive"),(True,"with_q_times_ordinal")):
            X_train = _ridge_features(train,train,product)
            X_test = _ridge_features(test,train,product)
            model = _regress(X_train,y_train,ridge=1.0)
            predicted = [sum(v*b for v,b in zip(row,model["beta"]))
                         for row in X_test]
            sqerr = [(obs-pred)**2 for obs,pred in zip(y_test,predicted)]
            record[f"{label}_MSE_days_squared"] = _rounded(mean(sqerr))
            weighted_errors[product].extend(sqerr)
        by_flyway[hold] = record
    mse_a=mean(weighted_errors[False])
    mse_b=mean(weighted_errors[True])
    return {
        "method": "leave-one-entire-flyway-out, train-standardized fixed alpha=1 ridge, no flyway dummies",
        "ridge_alpha_not_tuned": 1.0,
        "additive_heldout_MSE_days_squared": _rounded(mse_a),
        "product_heldout_MSE_days_squared": _rounded(mse_b),
        "product_minus_additive_heldout_MSE_days_squared": _rounded(mse_b-mse_a),
        "per_flyway": by_flyway,
        "n_independent_flyway_holdouts": 3,
        "do_not_interpret_as_large_sample_out_of_system_validation": True,
    }


def summarize(rows: list[dict]) -> dict:
    if len(rows) not in (11,13):
        raise ValueError("Source variants must have n=11 or 13")
    yy=[r["rmsd_days_published_site_aggregate"] for r in rows]
    qq=[r["q"] for r in rows]
    return {
        "n_fig3_published_region_rmsds":len(rows),
        "n_flyways":len(set(r["flyway"] for r in rows)),
        "mean_rmsd_days":_rounded(mean(yy)),
        "mean_q":_rounded(mean(qq)),
        "raw_Pearson_q_vs_published_RMSD":_rounded(_pearson(qq,yy)),
        "raw_Spearman_q_vs_published_RMSD":_rounded(_pearson(_rank(qq),_rank(yy))),
        "by_flyway":{
            f:{
                "n":len([r for r in rows if r["flyway"]==f]),
                "Pearson_q_RMSD":_rounded(_pearson(
                    [r["q"] for r in rows if r["flyway"]==f],
                    [r["rmsd_days_published_site_aggregate"] for r in rows
                     if r["flyway"]==f])),
            } for f in FLYWAYS
        },
        "descriptive_ols":_ols_summary(rows),
        "exploratory_cross_flyway_ridge":_lofo_ridge(rows),
    }


def run() -> dict:
    rows = _fig3_rows()
    return {
        "status":"POST_PUBLICATION_AGGREGATE_DIAGNOSTIC_V7_STILL_NOT_ESTIMABLE",
        "as_of":"2026-11-19",
        "source_article":"https://doi.org/10.1111/1365-2656.12281",
        "source_figure":"published Fig. 3 (a-i,k-n); numbers printed at regions",
        "source_historical_q":"published 1982-2011 supplement (23 Pearson q, 13 adjacent)",
        "outcome":"site-level goose-arrival RMSD aggregated to Fig3 region, not individual or registered region-year timing error",
        "model_freeze":"docs/PAYOFF_B_FIG3_PUBLISHED_AGGREGATE_PREFIT_20261119.md",
        "all_13_adjacent":summarize(rows),
        "only_11_without_unresolved_source_alias":summarize(
            [r for r in rows if r["alias_clean"]]),
        "p_values_or_significant_biological_claims":False,
        "new_independent_natural_replication":False,
        "frozen_V7_geometry_only_U_available":False,
        "frozen_V7_focal_q_times_U_estimated":False,
        "V7_PRIMARY_STATUS":"NOT_ESTIMABLE",
        "published_natural_prior_art_remains_original_2015_results":True,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=run()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",
                               encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))


if __name__=="__main__":
    main()
