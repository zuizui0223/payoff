#!/usr/bin/env python3
"""PAYOFF-B Stage-3 reanalysis of official mule-deer source data.

The analysis maps published migration movement rate and annual green-wave
propagation rate into the dimensionless analogue

    u_macro = animal movement rate / environmental-wave speed.

It then tests a phase-error feedback prediction:
animals behind the wave should increase u_macro and animals ahead of it should
decrease u_macro. This is an observational feedback signature, not a causal or
evolutionary-optimum estimate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats


SOURCE = Path("external/mule_deer_ortega_2023/source_data.xlsx")
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)


def ci_exp(model, term: str) -> tuple[float, float, float]:
    beta = float(model.params[term])
    lo, hi = [float(x) for x in model.conf_int().loc[term]]
    return math.exp(beta), math.exp(lo), math.exp(hi)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source workbook: {SOURCE}")

    phase = pd.read_excel(
        SOURCE, sheet_name="Fig1a,b;Fig3;SFig2;STables1,6", header=0
    )
    green = pd.read_excel(SOURCE, sheet_name="Fig4a", header=0)

    # The first row of this multi-block sheet is a section title; row 2 carries
    # the true headers for the all-deer block.
    move = pd.read_excel(
        SOURCE, sheet_name="Fig4d,4e;SFig4", header=1, usecols="A:G"
    )
    move.columns = [
        "id_yr",
        "timing",
        "compensation",
        "departure_rel_greenup",
        "standardized_DOY_Start",
        "rate_km_day",
        "stopover_day",
    ]

    for col in ("year", "km", "maxIRGdate"):
        green[col] = pd.to_numeric(green[col], errors="coerce")
    green = green.dropna(subset=["year", "km", "maxIRGdate"]).copy()
    green["year"] = green["year"].astype(int)

    wave_rows = []
    for year, d in green.groupby("year"):
        fit = smf.ols("maxIRGdate ~ km", data=d).fit()
        slope = float(fit.params["km"])
        speed = (1.0 / slope) if slope > 0 else np.nan
        # Endpoint estimate is a transparent nonparametric sensitivity check.
        dd = d.sort_values("km")
        delta_km = float(dd["km"].iloc[-1] - dd["km"].iloc[0])
        delta_t = float(dd["maxIRGdate"].iloc[-1] - dd["maxIRGdate"].iloc[0])
        endpoint_speed = (
            delta_km / delta_t if delta_km > 0 and delta_t > 0 else np.nan
        )
        wave_rows.append(
            {
                "year": int(year),
                "n_km": int(len(d)),
                "greenwave_slope_days_per_km": slope,
                "greenwave_speed_km_day": speed,
                "greenwave_endpoint_speed_km_day": endpoint_speed,
                "greenwave_linear_r2": float(fit.rsquared),
            }
        )
    wave = pd.DataFrame(wave_rows)
    wave.to_csv(OUT / "stage3_mule_deer_greenwave_speed_by_year.csv", index=False)

    phase["id_yr"] = phase["id_yr"].astype(str)
    move["id_yr"] = move["id_yr"].astype(str)

    dat = phase.merge(move, on=["id_yr", "timing"], how="inner")
    dat = dat.merge(wave, on="year", how="left")

    numeric = [
        "DFP_Start",
        "DFP_End",
        "rate_km_day",
        "stopover_day",
        "greenwave_speed_km_day",
        "greenwave_endpoint_speed_km_day",
    ]
    for col in numeric:
        dat[col] = pd.to_numeric(dat[col], errors="coerce")

    dat["u_macro"] = dat["rate_km_day"] / dat["greenwave_speed_km_day"]
    dat["u_macro_endpoint"] = (
        dat["rate_km_day"] / dat["greenwave_endpoint_speed_km_day"]
    )
    dat["q"] = np.log(dat["u_macro"])
    dat["q_endpoint"] = np.log(dat["u_macro_endpoint"])
    dat["abs_start"] = dat["DFP_Start"].abs()
    dat["abs_end"] = dat["DFP_End"].abs()
    dat["phase_error_reduction"] = dat["abs_start"] - dat["abs_end"]

    dat = dat.replace([np.inf, -np.inf], np.nan)
    core = dat.dropna(
        subset=["DFP_Start", "DFP_End", "q", "rate_km_day"]
    ).copy()

    # 1. Feedback controller signature: behind (>0 DFP) -> faster relative
    # movement; ahead (<0 DFP) -> slower relative movement.
    feedback = smf.ols("q ~ DFP_Start", data=core).fit()
    feedback_year = smf.ols("q ~ DFP_Start + C(year)", data=core).fit()

    # Endpoint environmental-speed sensitivity.
    endpoint_core = dat.dropna(subset=["DFP_Start", "q_endpoint"]).copy()
    feedback_endpoint = smf.ols("q_endpoint ~ DFP_Start", data=endpoint_core).fit()

    # 2. Phase compression from migration start to end.
    compression = smf.ols("DFP_End ~ DFP_Start", data=core).fit()
    compression_year = smf.ols("DFP_End ~ DFP_Start + C(year)", data=core).fit()

    # 3. Stopover feedback where available.
    stop = dat.dropna(subset=["DFP_Start", "stopover_day"]).copy()
    stop_model = smf.ols("stopover_day ~ DFP_Start", data=stop).fit()
    stop_year = smf.ols("stopover_day ~ DFP_Start + C(year)", data=stop).fit()

    # 4. Paired phase-error reduction.
    paired = core[["abs_start", "abs_end"]].dropna()
    paired_t = stats.ttest_rel(paired["abs_start"], paired["abs_end"])
    try:
        paired_w = stats.wilcoxon(
            paired["abs_start"], paired["abs_end"], alternative="greater"
        )
        wilcoxon_stat = float(paired_w.statistic)
        wilcoxon_p = float(paired_w.pvalue)
    except ValueError:
        wilcoxon_stat = np.nan
        wilcoxon_p = np.nan

    target_u, target_lo, target_hi = ci_exp(feedback, "Intercept")
    kappa = float(feedback.params["DFP_Start"])
    kappa_lo, kappa_hi = [
        float(x) for x in feedback.conf_int().loc["DFP_Start"]
    ]

    if kappa > 0 and target_u > 0:
        equilibrium_phase_error = -math.log(target_u) / kappa
    else:
        equilibrium_phase_error = np.nan

    median_environment_speed = float(
        wave["greenwave_speed_km_day"].median()
    )
    relaxation_distance_km = (
        median_environment_speed / kappa if kappa > 0 else np.nan
    )
    half_distance_km = (
        math.log(2.0) * relaxation_distance_km
        if np.isfinite(relaxation_distance_km)
        else np.nan
    )

    year_feedback_rows = []
    for year, d in core.groupby("year"):
        if len(d) < 4:
            continue
        m = smf.ols("q ~ DFP_Start", data=d).fit()
        year_feedback_rows.append(
            {
                "year": int(year),
                "n": int(len(d)),
                "kappa_log_u_per_day": float(m.params["DFP_Start"]),
                "kappa_p": float(m.pvalues["DFP_Start"]),
                "u0_at_zero_error": float(math.exp(m.params["Intercept"])),
                "r2": float(m.rsquared),
            }
        )
    year_feedback = pd.DataFrame(year_feedback_rows)
    year_feedback.to_csv(
        OUT / "stage3_mule_deer_feedback_by_year.csv", index=False
    )

    endpoint_target_u, endpoint_target_lo, endpoint_target_hi = ci_exp(
        feedback_endpoint, "Intercept"
    )

    result = {
        "analysis": "mule_deer_phase_feedback_v1",
        "n_animal_years": int(len(core)),
        "n_years": int(core["year"].nunique()),
        "median_u_macro": float(core["u_macro"].median()),
        "median_abs_start_days": float(core["abs_start"].median()),
        "median_abs_end_days": float(core["abs_end"].median()),
        "median_phase_error_reduction_days": float(
            core["phase_error_reduction"].median()
        ),
        "feedback_kappa_log_u_per_day": kappa,
        "feedback_kappa_ci95": [kappa_lo, kappa_hi],
        "feedback_kappa_p": float(feedback.pvalues["DFP_Start"]),
        "feedback_yearFE_kappa": float(feedback_year.params["DFP_Start"]),
        "feedback_yearFE_p": float(feedback_year.pvalues["DFP_Start"]),
        "zero_error_target_u_macro": target_u,
        "zero_error_target_u_ci95": [target_lo, target_hi],
        "equilibrium_phase_error_days": float(equilibrium_phase_error),
        "median_environment_speed_km_day": median_environment_speed,
        "local_relaxation_distance_km": float(relaxation_distance_km),
        "local_half_distance_km": float(half_distance_km),
        "n_years_positive_feedback": int(
            (year_feedback["kappa_log_u_per_day"] > 0).sum()
        ),
        "n_years_feedback_fitted": int(len(year_feedback)),
        "endpoint_speed_target_u_macro": endpoint_target_u,
        "endpoint_speed_target_u_ci95": [endpoint_target_lo, endpoint_target_hi],
        "endpoint_feedback_kappa": float(
            feedback_endpoint.params["DFP_Start"]
        ),
        "endpoint_feedback_p": float(
            feedback_endpoint.pvalues["DFP_Start"]
        ),
        "compression_slope_end_on_start": float(
            compression.params["DFP_Start"]
        ),
        "compression_slope_ci95": [
            float(x) for x in compression.conf_int().loc["DFP_Start"]
        ],
        "compression_p": float(compression.pvalues["DFP_Start"]),
        "compression_yearFE_slope": float(
            compression_year.params["DFP_Start"]
        ),
        "compression_yearFE_p": float(
            compression_year.pvalues["DFP_Start"]
        ),
        "mean_abs_start_days": float(paired["abs_start"].mean()),
        "mean_abs_end_days": float(paired["abs_end"].mean()),
        "paired_t_stat": float(paired_t.statistic),
        "paired_t_p": float(paired_t.pvalue),
        "wilcoxon_greater_stat": wilcoxon_stat,
        "wilcoxon_greater_p": wilcoxon_p,
        "stopover_beta_days_per_phase_day": float(
            stop_model.params["DFP_Start"]
        ),
        "stopover_p": float(stop_model.pvalues["DFP_Start"]),
        "stopover_yearFE_beta": float(stop_year.params["DFP_Start"]),
        "stopover_yearFE_p": float(stop_year.pvalues["DFP_Start"]),
        "claim_ceiling": (
            "Observational phase-feedback signature from published source data; "
            "not a causal, fitness, or evolutionary optimum estimate."
        ),
    }

    (OUT / "stage3_mule_deer_phase_feedback.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    pd.DataFrame([result]).to_csv(
        OUT / "stage3_mule_deer_phase_feedback.csv", index=False
    )
    dat.to_csv(OUT / "stage3_mule_deer_joined_source_data.csv", index=False)

    for name, model in [
        ("feedback", feedback),
        ("feedback_yearFE", feedback_year),
        ("feedback_endpoint", feedback_endpoint),
        ("compression", compression),
        ("compression_yearFE", compression_year),
        ("stopover", stop_model),
        ("stopover_yearFE", stop_year),
    ]:
        (OUT / f"stage3_mule_deer_{name}_summary.txt").write_text(
            model.summary().as_text() + "\n", encoding="utf-8"
        )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
