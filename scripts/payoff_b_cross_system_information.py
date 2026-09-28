#!/usr/bin/env python3
"""PAYOFF-B cross-system information-distance empirical lane.

This script deliberately keeps inference within source datasets:
- Usui et al. bird slopes: short- versus long-distance migrant contrast.
- Freimuth et al. species slopes: local plant/pollinator benchmark.

The cross-system comparison is descriptive triangulation only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from scipy.stats import norm, t as student_t

USUI_SHA256 = "68816f6cbfccbb9b47b45be0df49f077db914c8e43e567d0ed2cac9bbafde56c"
FREIMUTH_SHA256 = "946f56b8aa5f43bb15f5bbbd8c5174be23c12691332651e09bce2cb20edf7efd"

TARGET_ORDERS = {
    "Coleoptera": "Beetles",
    "Diptera": "Flies",
    "Hymenoptera": "Bees",
    "Lepidoptera": "Butterflies/Moths",
}
PUBLISHED_FREIMUTH = {
    "Beetles": {"n": 77, "mean": -1.7, "se": 0.5},
    "Flies": {"n": 22, "mean": -3.9, "se": 0.7},
    "Bees": {"n": 20, "mean": -2.0, "se": 1.3},
    "Butterflies/Moths": {"n": 206, "mean": -1.9, "se": 0.2},
    "Plants": {"n": 1438, "mean": -5.2, "se": 0.2},
}

# Three exact raw-name overrides are required because the live GBIF name-match
# endpoint returns NONE/HIGHERRANK for these historical strings. Each override
# is constrained to the source name and only assigns the broad group needed by
# the published Freimuth analysis. They are independently verifiable in GBIF:
# Ammophila arenaria (L.) Link = Plantae/Poales/Poaceae,
# Salix alba L. = Plantae,
# Tethea or = Animalia/Lepidoptera/Drepanidae.
FREIMUTH_TAXONOMY_OVERRIDES = {
    "Ammophila arenaria": "Plants",
    "Salix alba": "Plants",
    "Tethea or": "Butterflies/Moths",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv_fallback(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="cp1252")


def cluster_meat(xw: np.ndarray, uw: np.ndarray, groups: np.ndarray) -> tuple[np.ndarray, int]:
    codes, uniques = pd.factorize(pd.Series(groups, dtype="object"), sort=False)
    k = xw.shape[1]
    meat = np.zeros((k, k), dtype=float)
    for code in range(len(uniques)):
        idx = codes == code
        score = xw[idx].T @ uw[idx]
        meat += np.outer(score, score)
    g = len(uniques)
    n = len(uw)
    if g > 1 and n > k:
        meat *= (g / (g - 1)) * ((n - 1) / (n - k))
    return meat, g


def two_way_cluster_wls(
    y: np.ndarray,
    x: np.ndarray,
    weights: np.ndarray,
    group1: np.ndarray,
    group2: np.ndarray,
) -> dict:
    sw = np.sqrt(np.asarray(weights, float))
    xw = np.asarray(x, float) * sw[:, None]
    yw = np.asarray(y, float) * sw
    bread = np.linalg.pinv(xw.T @ xw)
    beta = bread @ (xw.T @ yw)
    uw = yw - xw @ beta

    m1, g1 = cluster_meat(xw, uw, group1)
    m2, g2 = cluster_meat(xw, uw, group2)
    intersection = np.array([f"{a}|||{b}" for a, b in zip(group1, group2)], dtype=object)
    m12, g12 = cluster_meat(xw, uw, intersection)
    cov = bread @ (m1 + m2 - m12) @ bread
    cov = (cov + cov.T) / 2
    return {
        "beta": beta,
        "cov": cov,
        "n": int(len(y)),
        "clusters_study": int(g1),
        "clusters_species": int(g2),
        "clusters_intersection": int(g12),
    }


def model_matrix(df: pd.DataFrame, adjusted: bool) -> tuple[np.ndarray, list[str]]:
    base = pd.DataFrame(
        {
            "intercept": 1.0,
            "long_minus_short": (df["Migration_distance"].astype(str) == "long").astype(float),
        },
        index=df.index,
    )
    if not adjusted:
        return base.to_numpy(float), list(base.columns)

    z = pd.DataFrame(index=df.index)
    z["central_arrival_metric"] = (~df["Response_variable"].astype(str).str.lower().eq("first arrival")).astype(float)
    for col in ["Temperature_location", "Arrival_location", "Data_source", "Continent"]:
        d = pd.get_dummies(df[col].fillna("missing").astype(str), prefix=col, drop_first=True, dtype=float)
        z = pd.concat([z, d], axis=1)
    out = pd.concat([base, z], axis=1)
    # Drop columns with no variation.
    keep = [c for c in out.columns if c == "intercept" or out[c].nunique(dropna=False) > 1]
    out = out[keep]
    return out.to_numpy(float), list(out.columns)


def cluster_df(fit: dict) -> int:
    # Conservative inference uses the smaller marginal cluster count.
    return max(1, min(int(fit["clusters_study"]), int(fit["clusters_species"])) - 1)


def term_summary(fit: dict, names: list[str], term: str) -> dict:
    j = names.index(term)
    est = float(fit["beta"][j])
    var = float(fit["cov"][j, j])
    se = math.sqrt(max(var, 0.0))
    stat = est / se if se > 0 else float("nan")
    df = cluster_df(fit)
    crit = float(student_t.ppf(0.975, df))
    p = 2 * student_t.sf(abs(stat), df) if math.isfinite(stat) else float("nan")
    return {
        "estimate": est,
        "se": se,
        "ci95": [est - crit * se, est + crit * se],
        "t": stat,
        "df": df,
        "p": p,
    }


def linear_combo(fit: dict, vector: np.ndarray) -> dict:
    est = float(vector @ fit["beta"])
    var = float(vector @ fit["cov"] @ vector)
    se = math.sqrt(max(var, 0.0))
    df = cluster_df(fit)
    crit = float(student_t.ppf(0.975, df))
    return {"estimate": est, "se": se, "ci95": [est - crit * se, est + crit * se], "df": df}


def fit_bird(usui: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    d = usui.copy()
    d["Predictor"] = d["Predictor"].astype(str).str.lower()
    d["Migration_distance"] = d["Migration_distance"].astype(str).str.lower()
    d = d.loc[
        d["Predictor"].eq("temperature")
        & d["Migration_distance"].isin(["short", "long"])
    ].copy()
    for c in ["Slope", "SE"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d.loc[np.isfinite(d["Slope"]) & np.isfinite(d["SE"]) & (d["SE"] > 0)].copy()

    weights = 1.0 / np.square(d["SE"].to_numpy(float))
    cap = float(np.quantile(weights, 0.99))
    capped = np.minimum(weights, cap)

    fits = {}
    for label, adjusted, w in [
        ("ivw_distance_only", False, weights),
        ("ivw_adjusted", True, weights),
        ("ivw_adjusted_weightcap99", True, capped),
        ("unweighted_adjusted", True, np.ones(len(d), dtype=float)),
    ]:
        x, names = model_matrix(d, adjusted=adjusted)
        fit = two_way_cluster_wls(
            d["Slope"].to_numpy(float),
            x,
            w,
            d["Study"].astype(str).to_numpy(),
            d["Species"].astype(str).to_numpy(),
        )
        contrast = term_summary(fit, names, "long_minus_short")
        entry = {
            "terms": names,
            "long_minus_short": contrast,
            "n": fit["n"],
            "clusters_study": fit["clusters_study"],
            "clusters_species": fit["clusters_species"],
            "clusters_intersection": fit["clusters_intersection"],
        }
        if not adjusted:
            short_vec = np.zeros(len(names)); short_vec[names.index("intercept")] = 1
            long_vec = short_vec.copy(); long_vec[names.index("long_minus_short")] = 1
            entry["short_mean"] = linear_combo(fit, short_vec)
            entry["long_mean"] = linear_combo(fit, long_vec)
        fits[label] = entry

    loo = []
    for held_out_study in sorted(d["Study"].astype(str).unique()):
        dd = d.loc[d["Study"].astype(str) != held_out_study].copy()
        ww = 1.0 / np.square(dd["SE"].to_numpy(float))
        xx, nn = model_matrix(dd, adjusted=True)
        ff = two_way_cluster_wls(
            dd["Slope"].to_numpy(float),
            xx,
            ww,
            dd["Study"].astype(str).to_numpy(),
            dd["Species"].astype(str).to_numpy(),
        )
        ss = term_summary(ff, nn, "long_minus_short")
        loo.append({
            "held_out_study": held_out_study,
            "estimate": ss["estimate"],
            "ci95": ss["ci95"],
            "p": ss["p"],
        })
    fits["leave_one_study_out"] = {
        "n_fits": len(loo),
        "estimate_range": [float(min(x["estimate"] for x in loo)), float(max(x["estimate"] for x in loo))],
        "min_ci_lower": float(min(x["ci95"][0] for x in loo)),
        "max_p": float(max(x["p"] for x in loo)),
        "all_estimates_positive": bool(all(x["estimate"] > 0 for x in loo)),
        "all_ci_lower_positive": bool(all(x["ci95"][0] > 0 for x in loo)),
        "fits": loo,
    }

    fits["descriptives"] = {
        "rows_temperature_short_long": int(len(d)),
        "species": int(d["Species"].nunique()),
        "studies": int(d["Study"].nunique()),
        "rows_by_distance": {str(k): int(v) for k, v in d["Migration_distance"].value_counts().items()},
        "species_by_distance": {
            str(k): int(v)
            for k, v in d.groupby("Migration_distance")["Species"].nunique().items()
        },
        "weight_cap_99": cap,
    }
    keep_cols = [
        "Study", "Species", "Migration_distance", "Slope", "SE",
        "Response_variable", "Temperature_location", "Arrival_location",
        "Data_source", "Continent",
    ]
    return fits, d[keep_cols].copy()


def gbif_match(name: str, attempts: int = 4) -> dict:
    url = "https://api.gbif.org/v1/species/match"
    err = None
    for a in range(attempts):
        try:
            r = requests.get(url, params={"name": name}, timeout=25)
            r.raise_for_status()
            x = r.json()
            return {
                "species": name,
                "matchType": x.get("matchType"),
                "confidence": x.get("confidence"),
                "usageKey": x.get("usageKey"),
                "scientificName": x.get("scientificName"),
                "kingdom": x.get("kingdom"),
                "phylum": x.get("phylum"),
                "class": x.get("class"),
                "order": x.get("order"),
                "family": x.get("family"),
                "status": x.get("status"),
            }
        except Exception as e:
            err = repr(e)
            time.sleep(1.5 * (a + 1))
    return {"species": name, "error": err}


def group_from_taxonomy(row: pd.Series) -> str:
    raw_name = str(row.get("species", ""))
    if raw_name in FREIMUTH_TAXONOMY_OVERRIDES:
        return FREIMUTH_TAXONOMY_OVERRIDES[raw_name]
    kingdom = str(row.get("kingdom", ""))
    order = str(row.get("order", ""))
    if kingdom == "Plantae":
        return "Plants"
    return TARGET_ORDERS.get(order, "Unresolved")


def build_taxonomy(species: list[str], cache_path: Path | None, workers: int) -> pd.DataFrame:
    cached = pd.DataFrame()
    if cache_path and cache_path.exists():
        cached = pd.read_csv(cache_path)
    done = set(cached.get("species", pd.Series(dtype=str)).astype(str))
    todo = [s for s in species if s not in done]
    rows = []
    if todo:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(gbif_match, s): s for s in todo}
            for i, fut in enumerate(as_completed(futs), 1):
                rows.append(fut.result())
                if i % 100 == 0:
                    print(f"GBIF taxonomy: {i}/{len(todo)} resolved")
    fresh = pd.DataFrame(rows)
    if cached.empty:
        out = fresh
    elif fresh.empty:
        out = cached
    else:
        out = pd.concat([cached, fresh], ignore_index=True)
    out = out.drop_duplicates("species", keep="last").sort_values("species")
    out["payoff_group"] = out.apply(group_from_taxonomy, axis=1)
    out["taxonomy_override_applied"] = out["species"].astype(str).isin(FREIMUTH_TAXONOMY_OVERRIDES)
    out["taxonomy_override_group"] = out["species"].astype(str).map(FREIMUTH_TAXONOMY_OVERRIDES)
    return out


def summarize_freimuth(freimuth: pd.DataFrame, taxonomy: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    d = freimuth.merge(taxonomy[["species", "payoff_group", "kingdom", "order", "confidence", "matchType"]], on="species", how="left")
    d["payoff_group"] = d["payoff_group"].fillna("Unresolved")
    rows = []
    for grp, g in d.groupby("payoff_group", dropna=False):
        x = pd.to_numeric(g["slope"], errors="coerce").dropna().to_numpy(float)
        n = len(x)
        sd = float(np.std(x, ddof=1)) if n > 1 else float("nan")
        se = sd / math.sqrt(n) if n > 1 else float("nan")
        rows.append({
            "group": str(grp),
            "n": n,
            "mean": float(np.mean(x)) if n else float("nan"),
            "median": float(np.median(x)) if n else float("nan"),
            "sd": sd,
            "se": se,
            "ci95": [float(np.mean(x) - 1.96 * se), float(np.mean(x) + 1.96 * se)] if n > 1 else [None, None],
            "fraction_negative": float(np.mean(x < 0)) if n else float("nan"),
        })
    summary = pd.DataFrame(rows).sort_values("group")

    checks = {}
    for grp, ref in PUBLISHED_FREIMUTH.items():
        hit = summary.loc[summary["group"].eq(grp)]
        if hit.empty:
            checks[grp] = {"pass": False, "reason": "missing group"}
            continue
        r = hit.iloc[0]
        # Published means/SE are rounded to one decimal; count should match the
        # Dryad reconstruction and mean should reproduce within rounding tolerance.
        checks[grp] = {
            "n_observed": int(r["n"]),
            "n_published": int(ref["n"]),
            "mean_observed": float(r["mean"]),
            "mean_published_rounded": float(ref["mean"]),
            "se_observed": float(r["se"]),
            "se_published_rounded": float(ref["se"]),
            "count_match": int(r["n"]) == int(ref["n"]),
            "mean_within_0_11": abs(float(r["mean"]) - float(ref["mean"])) <= 0.11,
        }
        checks[grp]["pass"] = checks[grp]["count_match"] and checks[grp]["mean_within_0_11"]

    out = {
        "rows": int(len(d)),
        "taxonomy_unresolved": int((d["payoff_group"] == "Unresolved").sum()),
        "groups": summary.to_dict(orient="records"),
        "published_reproduction_checks": checks,
        "all_group_count_and_mean_checks_pass": all(v.get("pass", False) for v in checks.values()),
    }
    return out, summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--usui", type=Path, required=True)
    ap.add_argument("--freimuth", type=Path, required=True)
    ap.add_argument("--taxonomy-cache", type=Path)
    ap.add_argument("--taxonomy-output", type=Path, required=True)
    ap.add_argument("--bird-rows-output", type=Path, required=True)
    ap.add_argument("--freimuth-summary-output", type=Path, required=True)
    ap.add_argument("--result-output", type=Path, required=True)
    ap.add_argument("--taxonomy-workers", type=int, default=24)
    args = ap.parse_args()

    checksums = {"usui": sha256(args.usui), "freimuth": sha256(args.freimuth)}
    if checksums["usui"] != USUI_SHA256:
        raise SystemExit(f"Usui checksum mismatch: {checksums['usui']}")
    if checksums["freimuth"] != FREIMUTH_SHA256:
        raise SystemExit(f"Freimuth checksum mismatch: {checksums['freimuth']}")

    usui = read_csv_fallback(args.usui)
    freimuth = read_csv_fallback(args.freimuth)
    required_usui = {"Study", "Species", "Migration_distance", "Predictor", "Slope", "SE"}
    required_f = {"species", "slope", "slope_std_err", "main_var"}
    if not required_usui.issubset(usui.columns):
        raise SystemExit(f"Usui schema missing: {sorted(required_usui - set(usui.columns))}")
    if not required_f.issubset(freimuth.columns):
        raise SystemExit(f"Freimuth schema missing: {sorted(required_f - set(freimuth.columns))}")

    bird, bird_rows = fit_bird(usui)
    taxonomy = build_taxonomy(sorted(freimuth["species"].dropna().astype(str).unique()), args.taxonomy_cache, args.taxonomy_workers)
    freimuth_result, freimuth_summary = summarize_freimuth(freimuth, taxonomy)

    result = {
        "result_id": "payoff_b_cross_system_information_20260928",
        "contract": "payoff_b_cross_system_information_distance_v1_20260928",
        "status": "EXECUTED_DERIVED_ONLY",
        "source_checksums_sha256": checksums,
        "bird_meta_regression": bird,
        "freimuth_local_benchmark": freimuth_result,
        "cross_system_claim_boundary": {
            "licensed": "within-bird migration-distance contrast plus independent local plant-pollinator benchmark",
            "not_licensed": "a causal pollinator-versus-bird taxon coefficient or universal ranking",
        },
    }

    for p in [args.taxonomy_output, args.bird_rows_output, args.freimuth_summary_output, args.result_output]:
        p.parent.mkdir(parents=True, exist_ok=True)
    taxonomy.to_csv(args.taxonomy_output, index=False)
    bird_rows.to_csv(args.bird_rows_output, index=False)
    freimuth_summary.to_csv(args.freimuth_summary_output, index=False)
    args.result_output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
