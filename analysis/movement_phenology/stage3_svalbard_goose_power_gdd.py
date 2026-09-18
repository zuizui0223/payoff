#!/usr/bin/env python3
"""Reconstruct annual onset of spring for Svalbard-goose stopover regions.

Environmental input:
NASA POWER daily T2M, queried at the reconstructed region centroids.

Phenology transform:
van-Wijk-style latitude-dependent GDD + logistic GDD jerk.

This is an independent modern reconstruction. It does not claim byte-identical
reproduction of the historical ECA/NOAA series used by Kölzsch et al. (2015).
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import time

import numpy as np
import pandas as pd
import requests

from analysis.movement_phenology.gdd_jerk import fit_gdd_jerk


REGIONS = Path("outputs/movement_phenology/stage3_svalbard_goose_regions.csv")
OUT = Path("outputs/movement_phenology")
OUT.mkdir(parents=True, exist_ok=True)

POWER_ENDPOINT = "https://power.larc.nasa.gov/api/temporal/daily/point"
START_YEAR = 1982
END_YEAR = 2011


def power_daily_t2m(lat: float, lon: float, start_year: int, end_year: int):
    rows = []
    # Chunk requests to keep payloads bounded and retries cheap.
    for y0 in range(start_year, end_year + 1, 5):
        y1 = min(end_year, y0 + 4)
        params = {
            "parameters": "T2M",
            "community": "AG",
            "longitude": f"{lon:.6f}",
            "latitude": f"{lat:.6f}",
            "start": f"{y0}0101",
            "end": f"{y1}1231",
            "format": "JSON",
        }
        last_error = None
        for attempt in range(4):
            try:
                resp = requests.get(
                    POWER_ENDPOINT, params=params, timeout=90
                )
                resp.raise_for_status()
                payload = resp.json()
                values = payload["properties"]["parameter"]["T2M"]
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
                last_error = None
                break
            except Exception as exc:
                last_error = exc
                time.sleep(1.5 * (attempt + 1))
        if last_error is not None:
            raise RuntimeError(
                f"NASA POWER failed for {lat},{lon} {y0}-{y1}: {last_error}"
            )
        time.sleep(0.25)

    d = pd.DataFrame(rows).drop_duplicates("date").sort_values("date")
    if d.empty:
        raise RuntimeError(f"No POWER data for {lat},{lon}")
    d["year"] = d["date"].dt.year
    d["doy"] = d["date"].dt.dayofyear
    return d


def fisher_r_pvalue(x, y):
    from scipy.stats import pearsonr

    d = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(d) < 4:
        return np.nan, np.nan, len(d)
    r, p = pearsonr(d["x"], d["y"])
    return float(r), float(p), int(len(d))


def main():
    regions = pd.read_csv(REGIONS)
    regions = regions[regions["published_region_eligible"] == True].copy()  # noqa:E712
    regions = regions.sort_values("lat").reset_index(drop=True)

    onset_rows = []
    temperature_receipts = []

    for _, region in regions.iterrows():
        rid = str(region["region_id"])
        lat = float(region["lat"])
        lon = float(region["lon"])
        temp = power_daily_t2m(lat, lon, START_YEAR, END_YEAR)

        for year, d in temp.groupby("year"):
            d = d.sort_values("date")
            # Require essentially complete annual coverage.
            if len(d) < 360:
                onset_rows.append(
                    {
                        "region_id": rid,
                        "year": int(year),
                        "onset_doy": np.nan,
                        "gdd_fit_r2": np.nan,
                        "t_base_c": np.nan,
                        "fit_status": "INSUFFICIENT_DAILY_DATA",
                        "n_daily": int(len(d)),
                    }
                )
                continue
            try:
                fit = fit_gdd_jerk(
                    d["t2m_c"].to_numpy(),
                    lat,
                    min_r_squared=0.95,
                )
                onset_rows.append(
                    {
                        "region_id": rid,
                        "year": int(year),
                        "onset_doy": float(fit.onset_day),
                        "gdd_fit_r2": float(fit.r_squared),
                        "t_base_c": float(fit.t_base),
                        "fit_status": "PASS",
                        "n_daily": int(len(d)),
                    }
                )
            except Exception as exc:
                onset_rows.append(
                    {
                        "region_id": rid,
                        "year": int(year),
                        "onset_doy": np.nan,
                        "gdd_fit_r2": np.nan,
                        "t_base_c": np.nan,
                        "fit_status": f"FAIL:{type(exc).__name__}",
                        "n_daily": int(len(d)),
                    }
                )

        temperature_receipts.append(
            {
                "region_id": rid,
                "lat": lat,
                "lon": lon,
                "n_daily_total": int(len(temp)),
                "date_min": str(temp["date"].min().date()),
                "date_max": str(temp["date"].max().date()),
            }
        )

    onsets = pd.DataFrame(onset_rows)
    onsets.to_csv(OUT / "stage3_svalbard_goose_power_gdd_onsets.csv", index=False)

    summary = (
        onsets[onsets["fit_status"] == "PASS"]
        .groupby("region_id")
        .agg(
            n_years=("year", "size"),
            mean_onset_doy=("onset_doy", "mean"),
            sd_onset_doy=("onset_doy", "std"),
            median_onset_doy=("onset_doy", "median"),
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
                    "median_start_doy",
                ]
            ],
            on="region_id",
            how="left",
        )
    )
    summary.to_csv(
        OUT / "stage3_svalbard_goose_power_gdd_region_summary.csv",
        index=False,
    )

    wide = onsets.pivot(index="year", columns="region_id", values="onset_doy")
    corr_rows = []
    ordered = list(regions["region_id"])
    for a, b in zip(ordered[:-1], ordered[1:]):
        if a not in wide or b not in wide:
            continue
        r, p, n = fisher_r_pvalue(wide[a], wide[b])
        x = pd.DataFrame({"a": wide[a], "b": wide[b]}).dropna()
        if len(x) >= 4:
            slope = float(np.polyfit(x["a"] - x["a"].mean(),
                                     x["b"] - x["b"].mean(), 1)[0])
        else:
            slope = np.nan
        corr_rows.append(
            {
                "origin_region": a,
                "destination_region": b,
                "n_years": n,
                "phenology_correlation_r": r,
                "correlation_p": p,
                "anomaly_slope_ols": slope,
            }
        )
    corr = pd.DataFrame(corr_rows)
    corr.to_csv(
        OUT / "stage3_svalbard_goose_power_predictability.csv",
        index=False,
    )

    # External validation anchors explicitly stated in Kölzsch et al. (2015):
    # Scotland initial stopover ~26 March; Svalbard breeding region ~16 June.
    # Convert to representative non-leap DOY.
    published_anchors = {"R1": 85.0, "R4": 167.0}
    anchor_rows = []
    for rid, target in published_anchors.items():
        hit = summary[summary["region_id"] == rid]
        if hit.empty:
            continue
        estimate = float(hit["mean_onset_doy"].iloc[0])
        anchor_rows.append(
            {
                "region_id": rid,
                "published_mean_doy_approx": target,
                "reconstructed_mean_doy": estimate,
                "difference_days": estimate - target,
            }
        )
    anchors = pd.DataFrame(anchor_rows)
    anchors.to_csv(
        OUT / "stage3_svalbard_goose_power_anchor_validation.csv",
        index=False,
    )

    receipt = {
        "source": "NASA POWER daily T2M",
        "phenology_method": "latitude-dependent GDD + logistic third-derivative spring jerk",
        "period": [START_YEAR, END_YEAR],
        "n_regions": int(len(regions)),
        "n_onset_pass": int((onsets["fit_status"] == "PASS").sum()),
        "n_onset_total": int(len(onsets)),
        "all_region_year_fits_pass": bool(
            (onsets["fit_status"] == "PASS").all()
        ),
        "region_summary": summary.to_dict(orient="records"),
        "consecutive_predictability": corr.to_dict(orient="records"),
        "anchor_validation": anchors.to_dict(orient="records"),
        "temperature_receipts": temperature_receipts,
        "claim_ceiling": (
            "Independent modern phenology reconstruction; not exact recovery "
            "of historical ECA/NOAA inputs used in the 2015 paper."
        ),
    }
    (OUT / "stage3_svalbard_goose_power_gdd_receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
