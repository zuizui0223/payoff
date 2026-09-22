#!/usr/bin/env python3
"""Direct phase-control analysis for the Svalbard barnacle-goose flyway.

Inputs:
- reconstructed broad stopover visits from public raw GPS;
- annual region-level GDD-jerk onset reconstructed from public daily temperature.

The analysis distinguishes mainland progression from the final Arctic crossing.
This is important because capital breeders may deliberately overtake the green
wave near the breeding grounds rather than stabilize one phase throughout.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import norm


OUT = Path("outputs/movement_phenology")
STOPS = OUT / "stage3_svalbard_goose_stopovers.csv"
REGIONS = OUT / "stage3_svalbard_goose_regions.csv"
ONSETS = OUT / "stage3_svalbard_goose_power_gdd_onsets.csv"
SCENARIOS = OUT / "stage3_svalbard_goose_anchor_sensitivity_onsets.csv"


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0088
    p1 = math.radians(float(lat1))
    p2 = math.radians(float(lat2))
    dl = math.radians(float(lon2) - float(lon1))
    dp = p2 - p1
    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    )
    return 2 * r * math.asin(min(1.0, math.sqrt(a)))


def doy_fraction(ts: pd.Timestamp) -> float:
    start = pd.Timestamp(
        year=ts.year, month=1, day=1, tz=ts.tz
    )
    return 1.0 + (ts - start).total_seconds() / 86400.0


def build_visits(stops: pd.DataFrame) -> pd.DataFrame:
    rows = []
    stops = stops.sort_values(
        ["individual_id", "year", "start"]
    ).copy()

    for (ind, year), d in stops.groupby(["individual_id", "year"]):
        # Retain only broad regions; skipped minor stops remain implicitly part
        # of the migration pace between broad regions.
        d = d[d["region_id"].notna()].copy()
        if d.empty:
            continue
        current = None
        for _, x in d.iterrows():
            rid = str(x["region_id"])
            if current is None or rid != current["region_id"]:
                if current is not None:
                    rows.append(current)
                current = {
                    "individual_id": str(ind),
                    "year": int(year),
                    "region_id": rid,
                    "arrival": x["start"],
                    "departure": x["end"],
                    "n_site_clusters": 1,
                }
            else:
                current["departure"] = max(current["departure"], x["end"])
                current["n_site_clusters"] += 1
        if current is not None:
            rows.append(current)

    visits = pd.DataFrame(rows)
    visits["arrival"] = pd.to_datetime(visits["arrival"], utc=True)
    visits["departure"] = pd.to_datetime(visits["departure"], utc=True)
    visits["stopover_days"] = (
        visits["departure"] - visits["arrival"]
    ).dt.total_seconds() / 86400.0
    visits["arrival_doy"] = visits["arrival"].map(doy_fraction)
    visits["departure_doy"] = visits["departure"].map(doy_fraction)
    return visits


def cluster_fit(formula: str, data: pd.DataFrame, group="individual_id"):
    model = smf.ols(formula, data=data).fit(
        cov_type="cluster",
        cov_kwds={"groups": data[group]},
    )
    return model


def parameter_receipt(model, term):
    return {
        "estimate": float(model.params[term]),
        "se_cluster": float(model.bse[term]),
        "p_cluster": float(model.pvalues[term]),
        "ci95_cluster": [
            float(x) for x in model.conf_int().loc[term]
        ],
    }


def main():
    stops = pd.read_csv(STOPS, parse_dates=["start", "end"])
    regions = pd.read_csv(REGIONS)
    onsets = pd.read_csv(ONSETS)

    regions = regions[
        regions["published_region_eligible"] == True  # noqa:E712
    ].copy()
    region_meta = regions.set_index("region_id").to_dict(orient="index")

    onset = onsets[
        onsets["fit_status"] == "PASS"
    ][["region_id", "year", "onset_calibrated_doy"]].copy()
    onset = onset.rename(columns={"onset_calibrated_doy": "onset_doy"})

    visits = build_visits(stops)
    visits = visits.merge(
        onset,
        on=["region_id", "year"],
        how="left",
    )
    visits["arrival_phase_days"] = (
        visits["arrival_doy"] - visits["onset_doy"]
    )
    visits["departure_phase_days"] = (
        visits["departure_doy"] - visits["onset_doy"]
    )
    visits.to_csv(
        OUT / "stage3_svalbard_goose_region_visits.csv",
        index=False,
    )

    transition_rows = []
    for (ind, year), d in visits.groupby(["individual_id", "year"]):
        d = d.sort_values("arrival").reset_index(drop=True)
        for i in range(len(d) - 1):
            a = d.iloc[i]
            b = d.iloc[i + 1]
            if a["region_id"] == b["region_id"]:
                continue
            if (
                not np.isfinite(a["onset_doy"])
                or not np.isfinite(b["onset_doy"])
            ):
                continue

            ma = region_meta.get(a["region_id"])
            mb = region_meta.get(b["region_id"])
            if ma is None or mb is None:
                continue

            distance = haversine_km(
                ma["lat"], ma["lon"], mb["lat"], mb["lon"]
            )
            transit_days = (
                b["arrival"] - a["departure"]
            ).total_seconds() / 86400.0
            env_delta_days = float(b["onset_doy"] - a["onset_doy"])

            if transit_days <= 0 or env_delta_days <= 0 or distance <= 0:
                continue

            animal_pace = distance / transit_days
            env_speed = distance / env_delta_days
            u = animal_pace / env_speed

            origin = str(a["region_id"])
            dest = str(b["region_id"])
            if dest == "R4":
                stage = "ARCTIC_CROSSING"
            else:
                stage = "MAINLAND"

            transition_rows.append(
                {
                    "individual_id": str(ind),
                    "year": int(year),
                    "origin_region": origin,
                    "destination_region": dest,
                    "stage": stage,
                    "origin_lat": float(ma["lat"]),
                    "destination_lat": float(mb["lat"]),
                    "distance_km": distance,
                    "origin_arrival_doy": float(a["arrival_doy"]),
                    "origin_departure_doy": float(a["departure_doy"]),
                    "destination_arrival_doy": float(b["arrival_doy"]),
                    "origin_onset_doy": float(a["onset_doy"]),
                    "destination_onset_doy": float(b["onset_doy"]),
                    "origin_arrival_phase_days": float(
                        a["arrival_phase_days"]
                    ),
                    "origin_departure_phase_days": float(
                        a["departure_phase_days"]
                    ),
                    "destination_arrival_phase_days": float(
                        b["arrival_phase_days"]
                    ),
                    "origin_stopover_days": float(a["stopover_days"]),
                    "transit_days": transit_days,
                    "environment_phase_delta_days": env_delta_days,
                    "animal_pace_km_day": animal_pace,
                    "environment_wave_speed_km_day": env_speed,
                    "u_macro": u,
                    "log_u": math.log(u),
                    "phase_change_days": float(
                        b["arrival_phase_days"]
                        - a["departure_phase_days"]
                    ),
                }
            )

    tr = pd.DataFrame(transition_rows)
    if tr.empty:
        raise SystemExit("No licensed broad-region transitions")

    tr.to_csv(
        OUT / "stage3_svalbard_goose_transitions.csv",
        index=False,
    )

    results = {
        "n_transitions": int(len(tr)),
        "n_individuals": int(tr["individual_id"].nunique()),
        "n_years": int(tr["year"].nunique()),
        "stage_counts": tr["stage"].value_counts().to_dict(),
        "transition_counts": [
            {
                "origin_region": str(a),
                "destination_region": str(b),
                "n": int(n),
            }
            for (a, b), n in (
                tr.groupby(["origin_region", "destination_region"]).size().items()
            )
        ],
    }

    # Overall model with explicit stage interaction.
    if tr["individual_id"].nunique() >= 5:
        full = cluster_fit(
            "log_u ~ origin_departure_phase_days * C(stage)",
            tr,
        )
        results["overall_stage_interaction"] = {
            "n": int(len(tr)),
            "model": "log_u ~ departure_phase * stage",
            "coefficients": {
                term: {
                    "estimate": float(full.params[term]),
                    "se_cluster": float(full.bse[term]),
                    "p_cluster": float(full.pvalues[term]),
                }
                for term in full.params.index
            },
        }
        (OUT / "stage3_svalbard_goose_controller_overall_summary.txt").write_text(
            full.summary().as_text() + "\n", encoding="utf-8"
        )

    stage_receipts = []
    for stage, d in tr.groupby("stage"):
        if len(d) < 8 or d["individual_id"].nunique() < 4:
            continue
        model = cluster_fit(
            "log_u ~ origin_departure_phase_days",
            d,
        )
        phase_model = cluster_fit(
            "destination_arrival_phase_days ~ origin_departure_phase_days",
            d,
        )
        stop_model = cluster_fit(
            "origin_stopover_days ~ origin_arrival_phase_days",
            d,
        )

        alpha = float(model.params["Intercept"])
        kappa = float(model.params["origin_departure_phase_days"])
        e_star = -alpha / kappa if kappa > 0 else np.nan
        median_ce = float(d["environment_wave_speed_km_day"].median())
        ell = median_ce / kappa if kappa > 0 else np.nan

        rec = {
            "stage": stage,
            "n": int(len(d)),
            "n_individuals": int(d["individual_id"].nunique()),
            "kappa": kappa,
            "kappa_se_cluster": float(
                model.bse["origin_departure_phase_days"]
            ),
            "kappa_p_cluster": float(
                model.pvalues["origin_departure_phase_days"]
            ),
            "u0": float(math.exp(alpha)),
            "equilibrium_phase_days": float(e_star)
            if np.isfinite(e_star)
            else None,
            "median_environment_speed_km_day": median_ce,
            "relaxation_distance_km": float(ell)
            if np.isfinite(ell)
            else None,
            "phase_transfer_slope": float(
                phase_model.params["origin_departure_phase_days"]
            ),
            "phase_transfer_p_cluster": float(
                phase_model.pvalues["origin_departure_phase_days"]
            ),
            "stopover_phase_beta": float(
                stop_model.params["origin_arrival_phase_days"]
            ),
            "stopover_phase_p_cluster": float(
                stop_model.pvalues["origin_arrival_phase_days"]
            ),
            "median_origin_departure_phase": float(
                d["origin_departure_phase_days"].median()
            ),
            "median_destination_arrival_phase": float(
                d["destination_arrival_phase_days"].median()
            ),
            "median_u": float(d["u_macro"].median()),
        }
        stage_receipts.append(rec)

        (OUT / f"stage3_svalbard_goose_controller_{stage.lower()}_summary.txt").write_text(
            model.summary().as_text() + "\n", encoding="utf-8"
        )

    stage_df = pd.DataFrame(stage_receipts)
    stage_df.to_csv(
        OUT / "stage3_svalbard_goose_controller_by_stage.csv",
        index=False,
    )
    results["stage_receipts"] = stage_receipts

    # Descriptive strategic contrast, always reported.
    descriptive = (
        tr.groupby("stage")
        .agg(
            n=("log_u", "size"),
            median_u=("u_macro", "median"),
            median_departure_phase=(
                "origin_departure_phase_days", "median"
            ),
            median_arrival_phase=(
                "destination_arrival_phase_days", "median"
            ),
            median_phase_change=("phase_change_days", "median"),
            median_transit_days=("transit_days", "median"),
        )
        .reset_index()
    )
    descriptive.to_csv(
        OUT / "stage3_svalbard_goose_stage_descriptives.csv",
        index=False,
    )
    results["stage_descriptives"] = descriptive.to_dict(orient="records")

    # Transition-specific behavioral feedback is less dependent on pooling
    # different route segments. Estimate speed and stopover responses wherever
    # repeated individual/year observations are adequate.
    pair_rows = []
    for (origin, dest), d in tr.groupby(["origin_region", "destination_region"]):
        if len(d) < 6 or d["individual_id"].nunique() < 4:
            continue
        speed_m = cluster_fit(
            "np.log(animal_pace_km_day) ~ origin_departure_phase_days", d
        )
        stop_m = cluster_fit(
            "origin_stopover_days ~ origin_arrival_phase_days", d
        )
        u_m = cluster_fit(
            "log_u ~ origin_departure_phase_days", d
        )
        phase_m = cluster_fit(
            "destination_arrival_phase_days ~ origin_arrival_phase_days", d
        )
        lam = float(phase_m.params["origin_arrival_phase_days"])
        lam_se = float(phase_m.bse["origin_arrival_phase_days"])
        z_vs_one = (lam - 1.0) / lam_se
        p_vs_one = float(2.0 * norm.sf(abs(z_vs_one)))
        pair_rows.append(
            {
                "origin_region": str(origin),
                "destination_region": str(dest),
                "n": int(len(d)),
                "n_individuals": int(d["individual_id"].nunique()),
                "behavioral_speed_gain": float(
                    speed_m.params["origin_departure_phase_days"]
                ),
                "behavioral_speed_gain_se_cluster": float(
                    speed_m.bse["origin_departure_phase_days"]
                ),
                "behavioral_speed_gain_p_cluster": float(
                    speed_m.pvalues["origin_departure_phase_days"]
                ),
                "relative_speed_gain": float(
                    u_m.params["origin_departure_phase_days"]
                ),
                "relative_speed_gain_se_cluster": float(
                    u_m.bse["origin_departure_phase_days"]
                ),
                "relative_speed_gain_p_cluster": float(
                    u_m.pvalues["origin_departure_phase_days"]
                ),
                "stopover_phase_beta": float(
                    stop_m.params["origin_arrival_phase_days"]
                ),
                "stopover_phase_se_cluster": float(
                    stop_m.bse["origin_arrival_phase_days"]
                ),
                "stopover_phase_p_cluster": float(
                    stop_m.pvalues["origin_arrival_phase_days"]
                ),
                "phase_transfer_arrival_to_arrival": lam,
                "phase_transfer_se_cluster": lam_se,
                "phase_transfer_p_vs_zero": float(
                    phase_m.pvalues["origin_arrival_phase_days"]
                ),
                "phase_transfer_z_vs_no_correction_one": float(z_vs_one),
                "phase_transfer_p_vs_no_correction_one": p_vs_one,
                "first_order_correction_fraction": float(1.0 - lam),
                "stopover_only_predicted_transfer": float(
                    1.0 + stop_m.params["origin_arrival_phase_days"]
                ),
            }
        )
    pair_df = pd.DataFrame(pair_rows)
    pair_df.to_csv(
        OUT / "stage3_svalbard_goose_controller_by_transition.csv",
        index=False,
    )
    results["transition_specific_receipts"] = pair_rows

    # Anchor-sensitivity audit. Annual POWER anomalies are preserved while
    # uncertain Norwegian 30-y means vary by +/-5 days.
    sensitivity_rows = []
    if SCENARIOS.exists():
        scenario_onsets = pd.read_csv(SCENARIOS)
        base_stops = pd.read_csv(STOPS, parse_dates=["start", "end"])
        base_visits = build_visits(base_stops)
        for sid, onset_s in scenario_onsets.groupby("scenario_id"):
            os = onset_s[["region_id", "year", "onset_calibrated_doy"]].rename(
                columns={"onset_calibrated_doy": "onset_doy"}
            )
            vs = base_visits.merge(os, on=["region_id", "year"], how="left")
            vs["arrival_phase_days"] = vs["arrival_doy"] - vs["onset_doy"]
            vs["departure_phase_days"] = vs["departure_doy"] - vs["onset_doy"]

            rows_s = []
            for (ind, year), d in vs.groupby(["individual_id", "year"]):
                d = d.sort_values("arrival").reset_index(drop=True)
                for i in range(len(d) - 1):
                    a = d.iloc[i]
                    b = d.iloc[i + 1]
                    if a["region_id"] == b["region_id"]:
                        continue
                    if not np.isfinite(a["onset_doy"]) or not np.isfinite(b["onset_doy"]):
                        continue
                    ma = region_meta.get(a["region_id"])
                    mb = region_meta.get(b["region_id"])
                    if ma is None or mb is None:
                        continue
                    distance = haversine_km(
                        ma["lat"], ma["lon"], mb["lat"], mb["lon"]
                    )
                    transit_days = (
                        b["arrival"] - a["departure"]
                    ).total_seconds() / 86400.0
                    env_delta_days = float(b["onset_doy"] - a["onset_doy"])
                    if transit_days <= 0 or env_delta_days <= 0 or distance <= 0:
                        continue
                    animal_pace = distance / transit_days
                    env_speed = distance / env_delta_days
                    rows_s.append(
                        {
                            "individual_id": str(ind),
                            "year": int(year),
                            "origin_region": str(a["region_id"]),
                            "destination_region": str(b["region_id"]),
                            "origin_departure_phase_days": float(
                                a["departure_phase_days"]
                            ),
                            "animal_pace_km_day": animal_pace,
                            "log_u": math.log(animal_pace / env_speed),
                        }
                    )
            ts = pd.DataFrame(rows_s)
            if ts.empty:
                continue
            for (origin, dest), d in ts.groupby(
                ["origin_region", "destination_region"]
            ):
                if len(d) < 6 or d["individual_id"].nunique() < 4:
                    continue
                speed_m = cluster_fit(
                    "np.log(animal_pace_km_day) ~ origin_departure_phase_days", d
                )
                u_m = cluster_fit(
                    "log_u ~ origin_departure_phase_days", d
                )
                sensitivity_rows.append(
                    {
                        "scenario_id": str(sid),
                        "origin_region": str(origin),
                        "destination_region": str(dest),
                        "n": int(len(d)),
                        "behavioral_speed_gain": float(
                            speed_m.params["origin_departure_phase_days"]
                        ),
                        "behavioral_speed_gain_p_cluster": float(
                            speed_m.pvalues["origin_departure_phase_days"]
                        ),
                        "relative_speed_gain": float(
                            u_m.params["origin_departure_phase_days"]
                        ),
                        "relative_speed_gain_p_cluster": float(
                            u_m.pvalues["origin_departure_phase_days"]
                        ),
                    }
                )
    sens_df = pd.DataFrame(sensitivity_rows)
    sens_df.to_csv(
        OUT / "stage3_svalbard_goose_anchor_sensitivity_controller.csv",
        index=False,
    )
    results["anchor_sensitivity_n_models"] = int(len(sens_df))
    if not sens_df.empty:
        robust = (
            sens_df.groupby(["origin_region", "destination_region"])
            .agg(
                n_scenarios=("scenario_id", "nunique"),
                behavioral_gain_min=("behavioral_speed_gain", "min"),
                behavioral_gain_max=("behavioral_speed_gain", "max"),
                behavioral_positive_fraction=(
                    "behavioral_speed_gain", lambda x: float((x > 0).mean())
                ),
                relative_gain_min=("relative_speed_gain", "min"),
                relative_gain_max=("relative_speed_gain", "max"),
                relative_positive_fraction=(
                    "relative_speed_gain", lambda x: float((x > 0).mean())
                ),
            )
            .reset_index()
        )
        robust.to_csv(
            OUT / "stage3_svalbard_goose_anchor_sensitivity_summary.csv",
            index=False,
        )
        results["anchor_sensitivity_summary"] = robust.to_dict(orient="records")

    results["claim_ceiling"] = (
        "Independent direct STEP-controller reconstruction using public GPS plus POWER "
        "annual GDD-jerk anomalies calibrated to published/figure-derived "
        "30-y mean onset anchors. Norwegian anchor uncertainty is propagated "
        "through +/-5-day sensitivity; interpret controller estimates only "
        "when signs are robust to that audit."
    )

    (OUT / "stage3_svalbard_goose_controller_receipt.json").write_text(
        json.dumps(results, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
