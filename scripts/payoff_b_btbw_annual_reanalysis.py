"""Source-frozen descriptive annual reanalysis of Lany et al. BTBW data.

Not a test of counterfactual fitness regret, individual information use,
or biological recourse. See docs/PAYOFF_B_BTBW_ANNUAL_PREANALYSIS_LOCK_20261010.md.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Sequence

import numpy as np
import statsmodels.api as sm
from scipy.stats import t as student_t

REQUIRED = (
    "Year", "prop.F.ASY", "Acsa.budburst", "Acsa.canopy",
    "arrival.50", "clutch.init.50", "ln.mean.cats", "density",
    "survival", "mean.fledged",
)
BASE = ("Acsa.canopy", "ln.mean.cats", "density", "prop.F.ASY")


def read_annual(path: Path) -> list[dict[str, float]]:
    """Accept CR-only legacy CSV and modern LF; fail closed on source drift."""
    txt = path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    reader = csv.DictReader(txt.splitlines())
    if reader.fieldnames is None or any(f not in reader.fieldnames for f in REQUIRED):
        raise ValueError("Missing a registered annual column")
    rows = []
    for row in reader:
        parsed = {}
        for key in REQUIRED:
            raw = row[key]
            parsed[key] = float(raw) if raw not in ("", None) else float("nan")
        rows.append(parsed)
    years = [int(r["Year"]) for r in rows]
    if len(rows) != 25 or sorted(years) != list(range(1986, 2011)) or len(set(years)) != 25:
        raise ValueError("Source-year gate failed")
    if any(float(int(r["Year"])) != r["Year"] for r in rows):
        raise ValueError("Nonintegral year")
    for r in rows:
        year = int(r["Year"])
        for k in REQUIRED:
            if k == "arrival.50" and year <= 1988 and np.isnan(r[k]):
                continue
            if not np.isfinite(r[k]):
                raise ValueError(f"Unexpected NA/nonfinite at {year} {k}")
        if not 0 <= r["prop.F.ASY"] <= 1 or not 0 < r["survival"] <= 1:
            raise ValueError("Proportion/survival outside range")
        r["lag"] = r["clutch.init.50"] - r["Acsa.canopy"]
        r["postarrival"] = r["clutch.init.50"] - r["arrival.50"]
    return sorted(rows, key=lambda r: r["Year"])


def fit(y: np.ndarray, x: np.ndarray, names: Sequence[str]) -> dict:
    """OLS coefficients plus year-level HC3 intervals; descriptive only."""
    X = sm.add_constant(np.asarray(x, dtype=float), has_constant="add")
    model = sm.OLS(np.asarray(y, dtype=float), X).fit()
    hc3 = model.get_robustcov_results(cov_type="HC3")
    ci = hc3.conf_int(alpha=0.05)
    keys = ["intercept", *names]
    return {
        "n": len(y),
        "r2": float(model.rsquared),
        "terms": {key: {
            "coef": float(model.params[j]),
            "ols_se": float(model.bse[j]),
            "hc3_se": float(hc3.bse[j]),
            "hc3_ci95": [float(ci[j, 0]), float(ci[j, 1])],
            "hc3_p_vs_zero": float(hc3.pvalues[j]),
        } for j, key in enumerate(keys)},
    }


def zscore_feature(train: np.ndarray, test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    means = np.mean(train, axis=0)
    sd = np.std(train, axis=0, ddof=0)
    if np.any(sd <= 0):
        raise ValueError("Constant training-only feature")
    return (train - means) / sd, (test - means) / sd


def annual_regression(
    rows: list[dict[str, float]],
    names: Sequence[str],
    drop_year: int | None = None,
) -> dict:
    use = [r for r in rows if r["Year"] != drop_year]
    y = np.array([r["mean.fledged"] for r in use])
    x = np.array([[r[k] for k in names] for r in use])
    xz, _ = zscore_feature(x, x)
    return fit(y, xz, names)


def temporal_mse(rows: list[dict[str, float]], names: Sequence[str]) -> dict:
    """Historical/holdout association only; NOT an animal's seasonal forecast."""
    train = [r for r in rows if r["Year"] <= 1999]
    holdout = [r for r in rows if r["Year"] >= 2000]
    xtr = np.array([[r[k] for k in names] for r in train])
    xte = np.array([[r[k] for k in names] for r in holdout])
    ytr = np.array([r["mean.fledged"] for r in train])
    yte = np.array([r["mean.fledged"] for r in holdout])
    zxtr, zxte = zscore_feature(xtr, xte)
    coeff, _, _, _ = np.linalg.lstsq(
        sm.add_constant(zxtr, has_constant="add"), ytr, rcond=None
    )
    pred = sm.add_constant(zxte, has_constant="add") @ coeff
    return {
        "train_n": len(train),
        "test_n": len(holdout),
        "test_mse": float(np.mean((yte - pred) ** 2)),
    }


def run(path: Path) -> dict:
    rows = read_annual(path)
    response = np.array([r["clutch.init.50"] for r in rows])
    canopy = np.array([r["Acsa.canopy"] for r in rows])
    budburst = np.array([r["Acsa.budburst"] for r in rows])
    cl_canopy = fit(response, canopy[:, None], ["Acsa.canopy"])
    slope = cl_canopy["terms"]["Acsa.canopy"]
    test_stat = (slope["coef"] - 1) / slope["hc3_se"]
    cl_canopy["canopy_slope_hc3_p_vs_one"] = float(
        2 * student_t.sf(abs(test_stat), len(rows) - 2)
    )

    stage = [r for r in rows if np.isfinite(r["arrival.50"])]
    stage_x = np.array([r["Acsa.canopy"] for r in stage])[:, None]
    model_sets = {
        "base": BASE,
        "plus_lag": (*BASE, "lag"),
        "plus_nest_survival": (*BASE, "survival"),
        "plus_lag_and_nest_survival": (*BASE, "lag", "survival"),
    }
    annual = {
        name: annual_regression(rows, columns)
        for name, columns in model_sets.items()
    }
    heldout = {
        name: temporal_mse(rows, columns)
        for name, columns in model_sets.items()
    }
    loo = [
        annual_regression(rows, model_sets["plus_lag"], int(r["Year"]))[
            "terms"]["lag"]["coef"]
        for r in rows
    ]
    return {
        "status": "DESCRIPTIVE_PRIOR_ART_ONLY",
        "source": {
            "doi": "10.5061/dryad.g1m27",
            "year_n": len(rows),
            "years": [1986, 2010],
            "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "male_arrival_nonmissing_years": len(stage),
        },
        "temporal": {
            "clutch_vs_canopy": cl_canopy,
            "clutch_vs_budburst": fit(response, budburst[:, None], ["Acsa.budburst"]),
            "arrival_vs_canopy": fit(
                np.array([r["arrival.50"] for r in stage]),
                stage_x, ["Acsa.canopy"]
            ),
            "postarrival_interval_vs_canopy": fit(
                np.array([r["postarrival"] for r in stage]),
                stage_x, ["Acsa.canopy"]
            ),
            "median_clutch_minus_canopy_days_mean": float(
                np.mean([r["lag"] for r in rows])
            ),
        },
        "annual_fitness_association": {
            "models": annual,
            "holdout_2000_2010": heldout,
            "loo_lag_coef_min": float(min(loo)),
            "loo_lag_coef_max": float(max(loo)),
            "loo_lag_signs": {
                "positive": sum(x > 0 for x in loo),
                "negative": sum(x < 0 for x in loo),
            },
        },
        "unidentified": {
            "counterfactual_fitness_regret": "NOT_IDENTIFIED",
            "individual_information_use": "NOT_IDENTIFIED",
            "individually_feasible_recourse": "NOT_IDENTIFIED",
            "fitness_optimal_lag": "NOT_IDENTIFIED",
        },
        "warnings": [
            "Annual-level associations cannot estimate an individual fitness response surface",
            "Heldout test uses contemporaneous season-completed predictors, not decision-time cues",
            "Nest survival is a measured component of reproductive outcome, not a causal predictor",
            "Inference uses 25 years; HC3 does not correct serial autocorrelation",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": result["status"],
        "n": result["source"]["year_n"],
        "canopy_slope": result["temporal"]["clutch_vs_canopy"]["terms"]["Acsa.canopy"]["coef"],
        "lag_fitness_hc3_ci": result["annual_fitness_association"]["models"]["plus_lag"]["terms"]["lag"]["hc3_ci95"],
    }))


if __name__ == "__main__":
    main()
