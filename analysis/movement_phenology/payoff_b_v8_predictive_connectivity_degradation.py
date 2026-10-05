#!/usr/bin/env python3

from __future__ import annotations

import math
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

try:
    import pyreadr
except ImportError as exc:
    raise SystemExit("pyreadr is required to read the frozen Amaral final.rds") from exc

SOURCE_COMMIT = "62c58d77c2028bd863dfe3697b0d9cf29ceaeab0"
SOURCE_URL = (
    "https://raw.githubusercontent.com/br-amaral/BirdMigrationSpeed/"
    + SOURCE_COMMIT
    + "/data/final.rds"
)
EARLY_YEARS = tuple(range(2002, 2010))
LATE_YEARS = tuple(range(2010, 2018))
MIN_PAIRS = 6
BOOT_REPS_PAIR = 2000
BOOT_REPS_SPECIES = 10000
BOOT_SEED = 20261005

OUT = Path("outputs")
OUT.mkdir(parents=True, exist_ok=True)
CACHE = OUT / "amaral_final_frozen.rds"


def truthy(x: pd.Series) -> pd.Series:
    return x.astype(str).str.upper().isin(["TRUE", "T", "1"])


def haversine_km(lat1, lon1, lat2, lon2):
    lat1 = np.asarray(lat1, dtype=float)
    lon1 = np.asarray(lon1, dtype=float)
    lat2 = np.asarray(lat2, dtype=float)
    lon2 = np.asarray(lon2, dtype=float)
    rad = np.pi / 180.0
    p1 = lat1 * rad
    p2 = lat2 * rad
    dp = (lat2 - lat1) * rad
    dl = (lon2 - lon1) * rad
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 6371.0088 * 2 * np.arctan2(np.sqrt(a), np.sqrt(np.maximum(0, 1 - a)))


def detrended_rho(paired: pd.DataFrame, years) -> tuple[float, int]:
    z = paired[paired["year"].isin(years)].dropna(
        subset=["year", "source_greenup", "target_greenup"]
    ).copy()
    n = len(z)
    if n < MIN_PAIRS:
        return math.nan, n
    if z["year"].nunique() != n:
        raise RuntimeError("Duplicate years within one source-target window")
    year = z["year"].to_numpy(dtype=float)
    source = z["source_greenup"].to_numpy(dtype=float)
    target = z["target_greenup"].to_numpy(dtype=float)
    X = np.column_stack([np.ones(n), year])
    b_source = np.linalg.lstsq(X, source, rcond=None)[0]
    b_target = np.linalg.lstsq(X, target, rcond=None)[0]
    rs = source - X @ b_source
    rt = target - X @ b_target
    if np.std(rs, ddof=1) <= 0 or np.std(rt, ddof=1) <= 0:
        return math.nan, n
    return float(np.corrcoef(rs, rt)[0, 1]), n


def fit_mixed_intercept(df: pd.DataFrame, group_col: str) -> float:
    model = smf.mixedlm("delta_rho ~ 1", df, groups=df[group_col])
    fit = model.fit(reml=True, method="lbfgs", disp=False)
    return float(fit.fe_params["Intercept"])


def main() -> None:
    if not CACHE.exists():
        raise SystemExit(
            f"Missing {CACHE}. Download exactly {SOURCE_URL} before execution."
        )

    loaded = pyreadr.read_r(str(CACHE))
    if not loaded:
        raise SystemExit("No object read from RDS")
    dat = next(iter(loaded.values()))

    required = {
        "species", "year", "cell", "cell_lat2", "cell_lng",
        "gr_mn", "mig_cell", "breed_cell",
    }
    missing = sorted(required - set(dat.columns))
    if missing:
        raise SystemExit(f"Missing required columns: {missing}")

    cells = dat[[
        "species", "cell", "cell_lat2", "cell_lng", "mig_cell", "breed_cell"
    ]].drop_duplicates().copy()
    cells["cell"] = pd.to_numeric(cells["cell"], errors="coerce")
    cells["cell_lat2"] = pd.to_numeric(cells["cell_lat2"], errors="coerce")
    cells["cell_lng"] = pd.to_numeric(cells["cell_lng"], errors="coerce")
    cells["is_mig"] = truthy(cells["mig_cell"])
    cells["is_breed"] = truthy(cells["breed_cell"])

    targets = cells.loc[
        cells["is_breed"],
        ["species", "cell", "cell_lat2", "cell_lng"],
    ].sort_values(["species", "cell"])

    mappings = []
    for _, target in targets.iterrows():
        candidates = cells.loc[
            (cells["species"] == target["species"])
            & cells["is_mig"]
            & cells["cell_lat2"].notna()
            & (cells["cell_lat2"] < target["cell_lat2"]),
            ["cell", "cell_lat2", "cell_lng"],
        ].copy()
        if candidates.empty:
            continue
        candidates["distance_km"] = haversine_km(
            candidates["cell_lat2"],
            candidates["cell_lng"],
            target["cell_lat2"],
            target["cell_lng"],
        )
        candidates = candidates.sort_values(["distance_km", "cell"])
        source = candidates.iloc[0]
        mappings.append({
            "species": target["species"],
            "target_cell": float(target["cell"]),
            "source_cell": float(source["cell"]),
            "source_lat": float(source["cell_lat2"]),
            "source_lon": float(source["cell_lng"]),
            "target_lat": float(target["cell_lat2"]),
            "target_lon": float(target["cell_lng"]),
            "source_target_distance_km": float(source["distance_km"]),
        })
    mapping = pd.DataFrame(mappings)
    if mapping.empty:
        raise SystemExit("No source-target mappings")

    green = dat[["year", "cell", "gr_mn"]].drop_duplicates().copy()
    green["year"] = pd.to_numeric(green["year"], errors="coerce").astype("Int64")
    green["cell"] = pd.to_numeric(green["cell"], errors="coerce")
    green["gr_mn"] = pd.to_numeric(green["gr_mn"], errors="coerce")
    green = green.dropna(subset=["year", "cell", "gr_mn"]).copy()
    green["year"] = green["year"].astype(int)

    rows = []
    for _, mp in mapping.iterrows():
        source = green.loc[
            green["cell"] == mp["source_cell"], ["year", "gr_mn"]
        ].rename(columns={"gr_mn": "source_greenup"})
        target = green.loc[
            green["cell"] == mp["target_cell"], ["year", "gr_mn"]
        ].rename(columns={"gr_mn": "target_greenup"})
        paired = source.merge(target, on="year", how="inner")

        early_rho, early_n = detrended_rho(paired, EARLY_YEARS)
        late_rho, late_n = detrended_rho(paired, LATE_YEARS)
        rows.append({
            "species": mp["species"],
            "target_cell": mp["target_cell"],
            "source_cell": mp["source_cell"],
            "source_target_distance_km": mp["source_target_distance_km"],
            "early_rho": early_rho,
            "early_n": early_n,
            "late_rho": late_rho,
            "late_n": late_n,
            "delta_rho": late_rho - early_rho
            if np.isfinite(early_rho) and np.isfinite(late_rho)
            else math.nan,
        })

    rows = pd.DataFrame(rows)
    eligible = rows.loc[
        rows["early_rho"].notna()
        & rows["late_rho"].notna()
        & (rows["early_n"] >= MIN_PAIRS)
        & (rows["late_n"] >= MIN_PAIRS)
    ].copy()

    species_summary = (
        eligible.groupby("species", as_index=False)
        .agg(mean_delta_rho=("delta_rho", "mean"), n_pairs=("delta_rho", "size"))
    )

    n_pairs = len(eligible)
    n_species = len(species_summary)
    n_species_ge3 = int((species_summary["n_pairs"] >= 3).sum())
    gate_pass = n_pairs >= 100 and n_species >= 20 and n_species_ge3 >= 15

    eligible.to_csv(OUT / "payoff_b_v8_connectivity_degradation_pairs.csv", index=False)
    species_summary.to_csv(
        OUT / "payoff_b_v8_connectivity_degradation_species.csv", index=False
    )

    gate = {
        "source_commit": SOURCE_COMMIT,
        "early_window": "2002-2009",
        "late_window": "2010-2017",
        "min_pairs_per_window": MIN_PAIRS,
        "eligible_pairs": n_pairs,
        "eligible_species": n_species,
        "species_with_at_least_3_pairs": n_species_ge3,
        "admission_gate": "PASS" if gate_pass else "FAIL",
    }

    if not gate_pass:
        pd.DataFrame([gate]).to_csv(
            OUT / "payoff_b_v8_connectivity_degradation_result.csv", index=False
        )
        print(pd.DataFrame([gate]).to_string(index=False))
        return

    pair_mixed_estimate = fit_mixed_intercept(eligible, "species")

    rng = np.random.default_rng(BOOT_SEED)
    species_levels = species_summary["species"].tolist()
    boot_pair = []
    for _ in range(BOOT_REPS_PAIR):
        sampled = rng.choice(species_levels, size=len(species_levels), replace=True)
        pieces = []
        for k, sp in enumerate(sampled):
            z = eligible.loc[eligible["species"] == sp].copy()
            z["boot_species"] = f"{sp}__{k}"
            pieces.append(z)
        bd = pd.concat(pieces, ignore_index=True)
        try:
            boot_pair.append(fit_mixed_intercept(bd, "boot_species"))
        except Exception:
            continue

    if len(boot_pair) < 0.9 * BOOT_REPS_PAIR:
        raise RuntimeError("Too many failed species-cluster bootstrap fits")
    pair_boot_ci = np.quantile(boot_pair, [0.025, 0.975])

    species_mean = float(species_summary["mean_delta_rho"].mean())
    negative_species = int((species_summary["mean_delta_rho"] < 0).sum())
    positive_species = int((species_summary["mean_delta_rho"] > 0).sum())
    zero_species = int((species_summary["mean_delta_rho"] == 0).sum())
    sign_n = negative_species + positive_species
    sign_p = (
        float(stats.binomtest(
            negative_species, sign_n, p=0.5, alternative="greater"
        ).pvalue)
        if sign_n > 0 else math.nan
    )

    rng2 = np.random.default_rng(BOOT_SEED + 1)
    vals = species_summary["mean_delta_rho"].to_numpy()
    boot_species = np.array([
        rng2.choice(vals, size=len(vals), replace=True).mean()
        for _ in range(BOOT_REPS_SPECIES)
    ])
    species_boot_ci = np.quantile(boot_species, [0.025, 0.975])

    supported = (
        pair_mixed_estimate < 0
        and pair_boot_ci[1] < 0
        and negative_species > sign_n / 2
        and np.isfinite(sign_p)
        and sign_p < 0.05
    )

    result = {
        **gate,
        "pair_mixed_estimate": pair_mixed_estimate,
        "pair_species_cluster_boot_ci_low": float(pair_boot_ci[0]),
        "pair_species_cluster_boot_ci_high": float(pair_boot_ci[1]),
        "pair_bootstrap_successful_reps": len(boot_pair),
        "species_mean_delta_rho": species_mean,
        "species_boot_ci_low": float(species_boot_ci[0]),
        "species_boot_ci_high": float(species_boot_ci[1]),
        "negative_species": negative_species,
        "positive_species": positive_species,
        "zero_species": zero_species,
        "sign_test_n": sign_n,
        "sign_test_one_sided_p": sign_p,
        "support_status": (
            "SUPPORTED_BROAD_DEGRADATION"
            if supported else "NOT_SUPPORTED_BROAD_DEGRADATION"
        ),
    }
    pd.DataFrame([result]).to_csv(
        OUT / "payoff_b_v8_connectivity_degradation_result.csv", index=False
    )
    print(pd.DataFrame([result]).to_string(index=False))


if __name__ == "__main__":
    main()
