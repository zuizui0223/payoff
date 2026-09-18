#!/usr/bin/env python3
"""Reconstruct annual spring-onset anomalies for a barnacle-goose flyway.

For controller slopes within a fixed origin/destination region pair, the unknown
30-y mean onset at each region affects only regression intercepts. Therefore
annual GDD-jerk anomalies are sufficient for stopover-gain and phase-transfer
slope estimation.

Environmental source: NASA POWER daily T2M.
Phenology transform: registered latitude-dependent GDD + logistic GDD jerk.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr

from analysis.movement_phenology.gdd_jerk import fit_gdd_jerk
from analysis.movement_phenology.stage3_svalbard_goose_power_gdd import (
    power_daily_t2m,
)


OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--flyway", required=True)
    p.add_argument("--regions", required=True)
    p.add_argument("--start-year", type=int, default=1982)
    p.add_argument("--end-year", type=int, default=2011)
    return p.parse_args()


def main():
    args = parse_args()
    regions = pd.read_csv(args.regions)
    if "published_region_eligible" in regions:
        regions = regions[regions["published_region_eligible"] == True].copy()  # noqa:E712
    if regions.empty:
        raise SystemExit("No eligible regions for environmental reconstruction")

    onset_rows = []
    query_receipts = []

    for _, row in regions.iterrows():
        rid = str(row["region_id"])
        lat = float(row["lat"])
        lon = float(row["lon"])
        temp = power_daily_t2m(lat, lon, args.start_year, args.end_year)

        n_pass = 0
        for year, d in temp.groupby("year"):
            d = d.sort_values("date")
            if len(d) < 360:
                onset_rows.append(
                    {
                        "region_id": rid,
                        "year": int(year),
                        "onset_doy_raw": np.nan,
                        "gdd_fit_r2": np.nan,
                        "fit_status": "INSUFFICIENT_DAILY_DATA",
                    }
                )
                continue
            try:
                fit = fit_gdd_jerk(
                    d["t2m_c"].to_numpy(),
                    lat,
                    min_r_squared=0.95,
                )
                n_pass += 1
                onset_rows.append(
                    {
                        "region_id": rid,
                        "year": int(year),
                        "onset_doy_raw": float(fit.onset_day),
                        "gdd_fit_r2": float(fit.r_squared),
                        "fit_status": "PASS",
                    }
                )
            except Exception as exc:
                onset_rows.append(
                    {
                        "region_id": rid,
                        "year": int(year),
                        "onset_doy_raw": np.nan,
                        "gdd_fit_r2": np.nan,
                        "fit_status": f"FAIL:{type(exc).__name__}",
                    }
                )

        query_receipts.append(
            {
                "region_id": rid,
                "lat": lat,
                "lon": lon,
                "n_daily": int(len(temp)),
                "n_annual_pass": int(n_pass),
            }
        )

    onsets = pd.DataFrame(onset_rows)
    ok = onsets["fit_status"] == "PASS"
    means = (
        onsets.loc[ok]
        .groupby("region_id")["onset_doy_raw"]
        .mean()
        .to_dict()
    )
    onsets["region_mean_raw_doy"] = onsets["region_id"].map(means)
    onsets["onset_anomaly_days"] = (
        onsets["onset_doy_raw"] - onsets["region_mean_raw_doy"]
    )

    prefix = f"stage3_{args.flyway}_goose"
    onsets.to_csv(OUT / f"{prefix}_power_gdd_anomalies.csv", index=False)

    summary = (
        onsets.loc[ok]
        .groupby("region_id")
        .agg(
            n_years=("year", "size"),
            mean_raw_doy=("onset_doy_raw", "mean"),
            sd_raw_doy=("onset_doy_raw", "std"),
            min_fit_r2=("gdd_fit_r2", "min"),
        )
        .reset_index()
        .merge(
            regions[
                [
                    "region_id",
                    "lat",
                    "lon",
                    "n_individuals",
                    "n_stop_events",
                ]
            ],
            on="region_id",
            how="left",
        )
    )
    summary.to_csv(OUT / f"{prefix}_power_gdd_region_summary.csv", index=False)

    wide = onsets.loc[ok].pivot(
        index="year", columns="region_id", values="onset_anomaly_days"
    )
    pair_rows = []
    for i, a in enumerate(wide.columns):
        for b in wide.columns[i + 1 :]:
            d = pd.DataFrame({"a": wide[a], "b": wide[b]}).dropna()
            if len(d) < 4:
                continue
            r, p = pearsonr(d["a"], d["b"])
            slope = float(np.polyfit(d["a"], d["b"], 1)[0])
            pair_rows.append(
                {
                    "region_a": str(a),
                    "region_b": str(b),
                    "n_years": int(len(d)),
                    "phenology_correlation_r": float(r),
                    "correlation_p": float(p),
                    "anomaly_slope_ols": slope,
                }
            )
    pd.DataFrame(pair_rows).to_csv(
        OUT / f"{prefix}_power_predictability_all_pairs.csv", index=False
    )

    receipt = {
        "flyway": args.flyway,
        "source": "NASA POWER daily T2M",
        "method": "latitude-dependent GDD + logistic third-derivative jerk",
        "period": [args.start_year, args.end_year],
        "n_regions": int(regions["region_id"].nunique()),
        "n_pass": int(ok.sum()),
        "n_total": int(len(onsets)),
        "query_receipts": query_receipts,
        "claim_ceiling": (
            "Annual anomaly reconstruction only. Raw absolute onset is not "
            "interpreted as recovery of the historical ECA/NOAA mean phase."
        ),
    }
    (OUT / f"{prefix}_power_gdd_anomaly_receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
