#!/usr/bin/env python3
"""Estimate fixed-transition STEP-controller slopes using onset anomalies only.

Within a fixed region, adding an unknown constant mean onset shifts phase by a
constant and therefore does not change:
- stopover-duration slope versus arrival phase;
- destination phase-transfer slope versus origin phase.

This permits direct cross-flyway comparison of actuator gain and lambda without
claiming absolute target phase E*.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import norm


OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--flyway", required=True)
    p.add_argument("--stopovers", required=True)
    p.add_argument("--regions", required=True)
    p.add_argument("--anomalies", required=True)
    p.add_argument("--min-n", type=int, default=6)
    p.add_argument("--min-individuals", type=int, default=4)
    return p.parse_args()


def doy_fraction(ts: pd.Timestamp) -> float:
    start = pd.Timestamp(year=ts.year, month=1, day=1, tz=ts.tz)
    return 1.0 + (ts - start).total_seconds() / 86400.0


def cluster_fit(formula: str, data: pd.DataFrame):
    base = smf.ols(formula, data=data).fit()
    return base.get_robustcov_results(
        cov_type="cluster",
        groups=data["individual_id"],
    )


def result_term(model, name: str):
    names = list(model.model.exog_names)
    i = names.index(name)
    return float(model.params[i]), float(model.bse[i]), float(model.pvalues[i])


def main():
    args = parse_args()
    stops = pd.read_csv(args.stopovers, parse_dates=["start", "end"])
    regions = pd.read_csv(args.regions)
    anomalies = pd.read_csv(args.anomalies)

    if "published_region_eligible" in regions:
        eligible = set(
            regions.loc[
                regions["published_region_eligible"] == True, "region_id"  # noqa:E712
            ].astype(str)
        )
    else:
        eligible = set(regions["region_id"].astype(str))

    stops = stops[stops["region_id"].astype(str).isin(eligible)].copy()
    stops["region_id"] = stops["region_id"].astype(str)
    stops["arrival_doy"] = stops["start"].apply(doy_fraction)
    stops["departure_doy"] = stops["end"].apply(doy_fraction)
    stops["stopover_days"] = stops["duration_hours"] / 24.0

    anomalies = anomalies[
        anomalies["fit_status"].astype(str) == "PASS"
    ][["region_id", "year", "onset_anomaly_days"]].copy()
    anomalies["region_id"] = anomalies["region_id"].astype(str)

    visits = stops.merge(anomalies, on=["region_id", "year"], how="left")
    # Anchor-free phase coordinates: true phase differs only by region-specific
    # constants, irrelevant to fixed-transition slopes.
    visits["arrival_phase_anom"] = (
        visits["arrival_doy"] - visits["onset_anomaly_days"]
    )
    visits["departure_phase_anom"] = (
        visits["departure_doy"] - visits["onset_anomaly_days"]
    )

    transition_rows = []
    for (ind, year), d in visits.groupby(["individual_id", "year"]):
        d = d.sort_values("start").reset_index(drop=True)
        for i in range(len(d) - 1):
            a = d.iloc[i]
            b = d.iloc[i + 1]
            if str(a["region_id"]) == str(b["region_id"]):
                continue
            if not np.isfinite(a["arrival_phase_anom"]) or not np.isfinite(
                b["arrival_phase_anom"]
            ):
                continue
            transition_rows.append(
                {
                    "individual_id": str(ind),
                    "year": int(year),
                    "origin_region": str(a["region_id"]),
                    "destination_region": str(b["region_id"]),
                    "origin_arrival_phase_anom": float(a["arrival_phase_anom"]),
                    "origin_departure_phase_anom": float(a["departure_phase_anom"]),
                    "origin_stopover_days": float(a["stopover_days"]),
                    "destination_arrival_phase_anom": float(
                        b["arrival_phase_anom"]
                    ),
                    "origin_arrival_doy": float(a["arrival_doy"]),
                    "destination_arrival_doy": float(b["arrival_doy"]),
                }
            )
    tr = pd.DataFrame(transition_rows)
    if tr.empty:
        raise SystemExit("No anomaly-joined transitions")

    prefix = f"stage3_{args.flyway}_goose"
    tr.to_csv(OUT / f"{prefix}_anomaly_phase_transitions.csv", index=False)

    rows = []
    for (origin, dest), d in tr.groupby(
        ["origin_region", "destination_region"]
    ):
        if len(d) < args.min_n or d["individual_id"].nunique() < args.min_individuals:
            continue

        stop = cluster_fit(
            "origin_stopover_days ~ origin_arrival_phase_anom", d
        )
        phase = cluster_fit(
            "destination_arrival_phase_anom ~ origin_arrival_phase_anom", d
        )
        stop_beta, stop_se, stop_p = result_term(
            stop, "origin_arrival_phase_anom"
        )
        lam, lam_se, lam_p0 = result_term(
            phase, "origin_arrival_phase_anom"
        )
        z1 = (lam - 1.0) / lam_se
        p1 = float(2 * norm.sf(abs(z1)))

        rows.append(
            {
                "flyway": args.flyway,
                "origin_region": str(origin),
                "destination_region": str(dest),
                "n": int(len(d)),
                "n_individuals": int(d["individual_id"].nunique()),
                "n_years": int(d["year"].nunique()),
                "stopover_slope": stop_beta,
                "stopover_slope_se_cluster": stop_se,
                "stopover_slope_p_cluster": stop_p,
                "stopover_gain": -stop_beta,
                "phase_transfer_lambda": lam,
                "phase_transfer_se_cluster": lam_se,
                "phase_transfer_p_vs_zero": lam_p0,
                "phase_transfer_z_vs_no_correction_one": z1,
                "phase_transfer_p_vs_no_correction_one": p1,
                "correction_fraction": 1.0 - lam,
                "lambda_abs": abs(lam),
                "claim_class": "ANCHOR_INVARIANT_FIXED_TRANSITION_SLOPE",
            }
        )

    result = pd.DataFrame(rows)
    result.to_csv(
        OUT / f"{prefix}_step_controller_by_transition.csv", index=False
    )

    receipt = {
        "flyway": args.flyway,
        "n_joined_transitions": int(len(tr)),
        "n_fitted_transition_pairs": int(len(result)),
        "transition_receipts": result.to_dict(orient="records"),
        "claim_ceiling": (
            "Fixed-transition slope estimates are invariant to unknown constant "
            "regional mean-onset anchors. Absolute phase targets are not licensed."
        ),
    }
    (OUT / f"{prefix}_step_controller_receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
