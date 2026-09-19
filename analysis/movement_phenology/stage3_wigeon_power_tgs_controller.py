#!/usr/bin/env python3
"""Direct movement–phenology controller reconstruction for Eurasian wigeon.

Inputs
------
- published-HMM staging-site reconstruction;
- NASA POWER daily T2M as an independent temperature source;
- exact 5 C TGS cumulative-minimum transform from the paper supplement.

This is a third-taxon validation lane. NASA POWER is not asserted to be
byte-identical to the paper's ERA5 input, so the direct controller is promoted
only if both the movement-replication gate and a published arrival-phase
validation gate pass.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import time

import numpy as np
import pandas as pd
import requests
import statsmodels.formula.api as smf
from scipy.stats import norm

from analysis.movement_phenology.tgs import thermal_growing_season_onset


OUT = Path("outputs/movement_phenology")
STAGING = OUT / "stage3_wigeon_staging_sites.csv"
TRACKS = OUT / "stage3_wigeon_track_summary.csv"
HMM_RECEIPT = OUT / "stage3_wigeon_hmm_reconstruction_receipt.json"

POWER_ENDPOINT = "https://power.larc.nasa.gov/api/temporal/daily/point"
GRID_DEG = 0.5

PUBLISHED = {
    "arrival_events_with_environment": 208,
    "arrival_phase_median_days": 22.5,
    "arrival_phase_q1_days": 13.0,
    "arrival_phase_q3_days": 35.3,
}


def rounded_cell(lat: float, lon: float):
    return (
        round(float(lat) / GRID_DEG) * GRID_DEG,
        round(float(lon) / GRID_DEG) * GRID_DEG,
    )


def power_daily_t2m(lat: float, lon: float, start_year: int, end_year: int):
    params = {
        "parameters": "T2M",
        "community": "AG",
        "longitude": f"{lon:.4f}",
        "latitude": f"{lat:.4f}",
        "start": f"{start_year}0101",
        "end": f"{end_year}1231",
        "format": "JSON",
    }
    last = None
    for attempt in range(5):
        try:
            r = requests.get(
                POWER_ENDPOINT, params=params, timeout=90
            )
            r.raise_for_status()
            values = r.json()["properties"]["parameter"]["T2M"]
            rows = []
            for date, value in values.items():
                v = float(value)
                if v <= -900:
                    continue
                rows.append(
                    {
                        "date": pd.to_datetime(date, format="%Y%m%d"),
                        "t2m_c": v,
                    }
                )
            d = pd.DataFrame(rows).drop_duplicates("date").sort_values("date")
            if d.empty:
                raise RuntimeError("empty POWER response")
            d["year"] = d["date"].dt.year
            d["doy"] = d["date"].dt.dayofyear
            return d
        except Exception as exc:
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(
        f"POWER failed for {lat},{lon} {start_year}-{end_year}: {last}"
    )


def doy_fraction(ts: pd.Timestamp) -> float:
    ts = pd.Timestamp(ts)
    start = pd.Timestamp(year=ts.year, month=1, day=1, tz=ts.tz)
    return 1.0 + (ts - start).total_seconds() / 86400.0


def robust_fit(formula: str, data: pd.DataFrame):
    base = smf.ols(formula, data=data).fit()
    if data["individual_id"].nunique() >= 4:
        return base.get_robustcov_results(
            cov_type="cluster",
            groups=data["individual_id"],
        )
    return base


def term(model, name: str):
    names = list(model.model.exog_names)
    i = names.index(name)
    return (
        float(model.params[i]),
        float(model.bse[i]),
        float(model.pvalues[i]),
    )


def write_blocked(reason: str, details: dict):
    receipt = {
        "analysis": "wigeon_direct_phase_controller_v1",
        "status": "BLOCKED",
        "reason": reason,
        **details,
        "claim_ceiling": (
            "No direct wigeon controller estimate is licensed until the "
            "movement and environmental validation gates pass."
        ),
    }
    (OUT / "stage3_wigeon_direct_controller_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, default=str))


def main():
    if not STAGING.exists() or not TRACKS.exists() or not HMM_RECEIPT.exists():
        write_blocked(
            "MISSING_HMM_OUTPUT",
            {
                "staging_exists": STAGING.exists(),
                "tracks_exists": TRACKS.exists(),
                "hmm_receipt_exists": HMM_RECEIPT.exists(),
            },
        )
        return

    hmm = json.loads(HMM_RECEIPT.read_text(encoding="utf-8"))
    hmm_gate = bool(hmm.get("promotion_ready_for_environmental_controller"))
    if not hmm_gate:
        write_blocked(
            "HMM_REPLICATION_GATE_FAILED",
            {"hmm_receipt": hmm},
        )
        return

    staging = pd.read_csv(STAGING, parse_dates=["arrival", "last_loc"])
    tracks = pd.read_csv(TRACKS)
    if staging.empty:
        write_blocked("NO_STAGING_EVENTS", {})
        return

    staging["individual_id"] = staging["individual_id"].astype(str)
    tracks["individual_id"] = tracks["individual_id"].astype(str)
    staging["year"] = staging["year"].astype(int)
    tracks["year"] = tracks["year"].astype(int)

    staging["arrival_doy"] = staging["arrival"].apply(doy_fraction)
    staging["departure_doy"] = staging["last_loc"].apply(doy_fraction)
    staging["cell_lat"], staging["cell_lon"] = zip(
        *[
            rounded_cell(lat, lon)
            for lat, lon in zip(staging["lat"], staging["lon"])
        ]
    )

    years = sorted(int(y) for y in staging["year"].unique())
    start_year, end_year = min(years), max(years)

    tgs_rows = []
    query_rows = []

    cells = (
        staging[["cell_lat", "cell_lon"]]
        .drop_duplicates()
        .sort_values(["cell_lat", "cell_lon"])
    )
    for _, cell in cells.iterrows():
        lat = float(cell["cell_lat"])
        lon = float(cell["cell_lon"])
        try:
            temp = power_daily_t2m(lat, lon, start_year, end_year)
            n_pass = 0
            for year in years:
                d = temp[temp["year"] == year].sort_values("date")
                if len(d) < 350:
                    tgs_rows.append(
                        {
                            "cell_lat": lat,
                            "cell_lon": lon,
                            "year": year,
                            "tgs_onset_doy": np.nan,
                            "status": "INSUFFICIENT_DAILY_DATA",
                        }
                    )
                    continue
                fit = thermal_growing_season_onset(
                    d["t2m_c"].to_numpy(),
                    d["doy"].to_numpy(),
                    threshold_c=5.0,
                )
                n_pass += 1
                tgs_rows.append(
                    {
                        "cell_lat": lat,
                        "cell_lon": lon,
                        "year": year,
                        "tgs_onset_doy": float(fit.onset_day),
                        "status": "PASS",
                    }
                )
            query_rows.append(
                {
                    "cell_lat": lat,
                    "cell_lon": lon,
                    "status": "PASS",
                    "n_years_pass": n_pass,
                }
            )
        except Exception as exc:
            query_rows.append(
                {
                    "cell_lat": lat,
                    "cell_lon": lon,
                    "status": f"FAIL:{type(exc).__name__}:{exc}",
                    "n_years_pass": 0,
                }
            )
        time.sleep(0.15)

    tgs = pd.DataFrame(tgs_rows)
    query = pd.DataFrame(query_rows)
    tgs.to_csv(OUT / "stage3_wigeon_power_tgs_cells.csv", index=False)
    query.to_csv(OUT / "stage3_wigeon_power_tgs_queries.csv", index=False)

    env = staging.merge(
        tgs[tgs["status"] == "PASS"][
            ["cell_lat", "cell_lon", "year", "tgs_onset_doy"]
        ],
        on=["cell_lat", "cell_lon", "year"],
        how="left",
    )
    env["arrival_phase_days"] = (
        env["arrival_doy"] - env["tgs_onset_doy"]
    )
    env["departure_phase_days"] = (
        env["departure_doy"] - env["tgs_onset_doy"]
    )

    env = env.merge(
        tracks[
            [
                "individual_id",
                "year",
                "endpoint_distance_km",
                "cumulative_migration_distance_km",
                "migration_speed_km_day",
            ]
        ],
        on=["individual_id", "year"],
        how="left",
    )

    valid_phase = env["arrival_phase_days"].dropna()
    if len(valid_phase):
        phase_median = float(valid_phase.median())
        phase_q1 = float(valid_phase.quantile(0.25))
        phase_q3 = float(valid_phase.quantile(0.75))
    else:
        phase_median = phase_q1 = phase_q3 = np.nan

    validation = {
        "n_staging_events_total": int(len(env)),
        "n_staging_events_with_tgs": int(valid_phase.notna().sum()),
        "arrival_phase_median_days": phase_median,
        "arrival_phase_q1_days": phase_q1,
        "arrival_phase_q3_days": phase_q3,
        "published": PUBLISHED,
    }
    validation["event_count_gate"] = (
        validation["n_staging_events_with_tgs"] >= 150
    )
    validation["median_phase_gate"] = (
        np.isfinite(phase_median)
        and abs(phase_median - PUBLISHED["arrival_phase_median_days"]) <= 12.0
    )
    validation["iqr_overlap_gate"] = (
        np.isfinite(phase_q1)
        and np.isfinite(phase_q3)
        and phase_q1 <= PUBLISHED["arrival_phase_q3_days"]
        and phase_q3 >= PUBLISHED["arrival_phase_q1_days"]
    )
    env_gate = bool(
        validation["event_count_gate"]
        and validation["median_phase_gate"]
        and validation["iqr_overlap_gate"]
    )

    pd.DataFrame([validation]).to_csv(
        OUT / "stage3_wigeon_tgs_validation.csv", index=False
    )
    env.to_csv(OUT / "stage3_wigeon_tgs_events.csv", index=False)

    # Build consecutive staging-to-staging transitions.
    rows = []
    for (ind, year), d in env.groupby(["individual_id", "year"]):
        d = d.sort_values("arrival").reset_index(drop=True)
        d = d[d["arrival_phase_days"].notna()].reset_index(drop=True)
        for i in range(len(d) - 1):
            a = d.iloc[i]
            b = d.iloc[i + 1]
            speed = a.get("speed_btw_km_day", np.nan)
            if not np.isfinite(speed) or speed <= 0:
                speed = np.nan
            rows.append(
                {
                    "individual_id": str(ind),
                    "year": int(year),
                    "origin_segment": int(a["segment"]),
                    "destination_segment": int(b["segment"]),
                    "origin_phase": float(a["arrival_phase_days"]),
                    "destination_phase": float(b["arrival_phase_days"]),
                    "phase_change": float(
                        b["arrival_phase_days"] - a["arrival_phase_days"]
                    ),
                    "origin_stopover_days": float(a["duration_days"]),
                    "travel_speed_km_day": float(speed)
                    if np.isfinite(speed)
                    else np.nan,
                    "origin_progress_km": float(a["d2start_km"]),
                    "destination_progress_km": float(b["d2start_km"]),
                    "endpoint_distance_km": float(a["endpoint_distance_km"]),
                }
            )
    tr = pd.DataFrame(rows)
    tr.to_csv(OUT / "stage3_wigeon_controller_transitions.csv", index=False)

    if not env_gate or len(tr) < 30 or tr["individual_id"].nunique() < 10:
        write_blocked(
            "ENVIRONMENT_OR_TRANSITION_GATE_FAILED",
            {
                "hmm_gate": hmm_gate,
                "environment_validation": validation,
                "n_transitions": int(len(tr)),
                "n_transition_individuals": int(
                    tr["individual_id"].nunique()
                ) if len(tr) else 0,
            },
        )
        return

    # Standardized route covariates absorb the documented change in target
    # phase with route progress / total migration distance.
    tr["z_progress"] = (
        tr["origin_progress_km"] - tr["origin_progress_km"].mean()
    ) / tr["origin_progress_km"].std(ddof=0)
    tr["z_endpoint"] = (
        tr["endpoint_distance_km"] - tr["endpoint_distance_km"].mean()
    ) / tr["endpoint_distance_km"].std(ddof=0)

    phase_model = robust_fit(
        "phase_change ~ origin_phase + z_progress + z_endpoint "
        "+ z_progress:z_endpoint + C(year)",
        tr,
    )
    beta_e, beta_e_se, beta_e_p = term(phase_model, "origin_phase")
    lam = 1.0 + beta_e
    lam_se = beta_e_se
    z_vs_one = beta_e / beta_e_se
    p_vs_one = float(2.0 * norm.sf(abs(z_vs_one)))

    # Strategy moderation: does endpoint migration distance change retention?
    interaction_model = robust_fit(
        "phase_change ~ origin_phase * z_endpoint + z_progress + C(year)",
        tr,
    )
    beta_int, beta_int_se, beta_int_p = term(
        interaction_model, "origin_phase:z_endpoint"
    )

    stop_model = robust_fit(
        "origin_stopover_days ~ origin_phase + z_progress + z_endpoint "
        "+ C(year)",
        tr,
    )
    stop_beta, stop_se, stop_p = term(stop_model, "origin_phase")

    sp = tr.dropna(subset=["travel_speed_km_day"]).copy()
    if len(sp) >= 20 and sp["individual_id"].nunique() >= 8:
        sp["log_travel_speed"] = np.log(sp["travel_speed_km_day"])
        speed_model = robust_fit(
            "log_travel_speed ~ origin_phase + z_progress + z_endpoint "
            "+ C(year)",
            sp,
        )
        speed_beta, speed_se, speed_p = term(speed_model, "origin_phase")
    else:
        speed_beta = speed_se = speed_p = np.nan

    # Reproduce the paper's route-distance phenomenology as a validation lane.
    phase_events = env.dropna(
        subset=[
            "arrival_phase_days",
            "d2start_km",
            "endpoint_distance_km",
        ]
    ).copy()
    phase_events["z_progress"] = (
        phase_events["d2start_km"] - phase_events["d2start_km"].mean()
    ) / phase_events["d2start_km"].std(ddof=0)
    phase_events["z_endpoint"] = (
        phase_events["endpoint_distance_km"]
        - phase_events["endpoint_distance_km"].mean()
    ) / phase_events["endpoint_distance_km"].std(ddof=0)
    route_model = robust_fit(
        "arrival_phase_days ~ z_progress * z_endpoint + C(year)",
        phase_events,
    )
    route_int, route_int_se, route_int_p = term(
        route_model, "z_progress:z_endpoint"
    )

    receipt = {
        "analysis": "wigeon_direct_phase_controller_v1",
        "status": "DIRECT_CONTROLLER"
        if env_gate
        else "SENSITIVITY_ONLY",
        "source_environment": (
            "NASA POWER T2M + published 5C thermal-growing-season rule"
        ),
        "environment_validation": validation,
        "n_transitions": int(len(tr)),
        "n_individuals": int(tr["individual_id"].nunique()),
        "phase_change_beta_on_origin_error": beta_e,
        "phase_change_beta_se_cluster": beta_e_se,
        "phase_change_beta_p_cluster": beta_e_p,
        "phase_retention_lambda": lam,
        "phase_retention_se_cluster": lam_se,
        "phase_retention_p_vs_no_correction_one": p_vs_one,
        "phase_retention_abs": abs(lam),
        "correction_strength": 1.0 - abs(lam),
        "endpoint_distance_moderation_beta": beta_int,
        "endpoint_distance_moderation_se": beta_int_se,
        "endpoint_distance_moderation_p": beta_int_p,
        "stopover_slope_day_per_phase_day": stop_beta,
        "stopover_slope_se_cluster": stop_se,
        "stopover_slope_p_cluster": stop_p,
        "travel_log_speed_gain_per_phase_day": speed_beta,
        "travel_log_speed_gain_se_cluster": speed_se,
        "travel_log_speed_gain_p_cluster": speed_p,
        "route_progress_x_endpoint_phase_beta": route_int,
        "route_progress_x_endpoint_phase_se": route_int_se,
        "route_progress_x_endpoint_phase_p": route_int_p,
        "controller_stability_class": (
            "STABLE_CONTRACTION"
            if abs(lam) < 1 and lam >= 0
            else "STABLE_OVERSHOOT"
            if abs(lam) < 1 and lam < 0
            else "AMPLIFICATION"
        ),
        "claim_ceiling": (
            "Direct observational phase-retention estimate in a third taxon "
            "conditional on published-HMM replication and POWER-vs-published "
            "TGS validation. NASA POWER is an independent environmental "
            "reconstruction, not the paper's original ERA5 grid."
        ),
    }
    (OUT / "stage3_wigeon_direct_controller_receipt.json").write_text(
        json.dumps(receipt, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, default=str))


if __name__ == "__main__":
    main()
