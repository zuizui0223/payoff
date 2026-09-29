#!/usr/bin/env python3
"""Build pre-outcome ERA5 climate covariates for the snow-goose GPS lane.

The script never uses focal-year Bylot conditions.  For each focal migration
year it reconstructs route-context predictive connectivity from the immediately
preceding 20 calendar years, and constructs focal local temperature anomalies
against the same strictly pre-outcome 20-year daily climatology.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from datetime import date, datetime, timedelta
from pathlib import Path

from src.greater_snow_goose_climate import (
    CONTEXT_ORDER,
    initial_bearing_deg,
    seasonal_window,
    target_window,
    training_years,
    wind_support_ms,
)
from src.predictive_connectivity import detrended_predictive_connectivity


ENDPOINT = "https://archive-api.open-meteo.com/v1/archive"
HOURLY = (
    "temperature_2m,precipitation,wind_speed_10m,wind_direction_10m"
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--staging-contexts", type=Path, required=True)
    p.add_argument("--day-risk", type=Path, required=True)
    p.add_argument("--weather-output", type=Path, required=True)
    p.add_argument("--connectivity-output", type=Path, required=True)
    p.add_argument("--receipt-output", type=Path, required=True)
    p.add_argument("--max-retries", type=int, default=5)
    p.add_argument("--sleep-seconds", type=float, default=0.10)
    return p.parse_args()


def _date_range(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def _request_location_year(
    session,
    *,
    location_id,
    lat,
    lon,
    year,
    route_bearing,
    max_retries,
):
    params = {
        "latitude": f"{float(lat):.8f}",
        "longitude": f"{float(lon):.8f}",
        "start_date": f"{int(year)}-03-29",
        "end_date": f"{int(year)}-06-15",
        "hourly": HOURLY,
        "models": "era5",
        "timezone": "GMT",
        "cell_selection": "nearest",
        "temperature_unit": "celsius",
        "wind_speed_unit": "ms",
        "precipitation_unit": "mm",
    }
    last = None
    for attempt in range(max_retries):
        try:
            response = session.get(ENDPOINT, params=params, timeout=120)
            response.raise_for_status()
            payload = response.json()
            return payload, {
                "location_id": location_id,
                "year": int(year),
                "url": response.url,
                "status_code": int(response.status_code),
            }
        except Exception as exc:
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(
        f"ERA5 request failed for {location_id} {year}: {last}"
    )


def _strict_daily(payload, *, route_bearing):
    hourly = payload.get("hourly", {})
    names = (
        "time",
        "temperature_2m",
        "precipitation",
        "wind_speed_10m",
        "wind_direction_10m",
    )
    columns = [hourly.get(name, []) for name in names]
    if len({len(values) for values in columns}) != 1:
        raise ValueError("ERA5 hourly arrays have inconsistent lengths")

    by_day = {}
    for timestamp, temp, precip, speed, direction in zip(*columns):
        if any(value is None for value in (temp, precip, speed, direction)):
            continue
        values = tuple(float(v) for v in (temp, precip, speed, direction))
        if any(not math.isfinite(v) for v in values):
            continue
        day = str(timestamp)[:10]
        support = (
            None
            if route_bearing is None
            else wind_support_ms(values[2], values[3], route_bearing)
        )
        by_day.setdefault(day, []).append(
            (values[0], values[1], support)
        )

    daily = {}
    for day, rows in by_day.items():
        if len(rows) != 24:
            continue
        temp = sum(row[0] for row in rows) / 24.0
        precipitation = sum(row[1] for row in rows)
        supports = [row[2] for row in rows if row[2] is not None]
        daily[day] = {
            "temperature_2m_mean": temp,
            "precipitation_sum": precipitation,
            "wind_support_mean": (
                sum(supports) / len(supports) if supports else None
            ),
        }
    return daily


def _window_mean_temperature(daily, start, end):
    keys = [d.isoformat() for d in _date_range(start, end)]
    missing = [key for key in keys if key not in daily]
    if missing:
        raise ValueError(
            f"missing ERA5 daily temperature in frozen seasonal window: {missing[:3]}"
        )
    return sum(daily[key]["temperature_2m_mean"] for key in keys) / len(keys)


def _fixed_coordinates(contexts):
    import pandas as pd

    required = {
        "context",
        "centroid_lon",
        "centroid_lat",
        "target_bylot_lon",
        "target_bylot_lat",
    }
    if not required.issubset(contexts.columns):
        raise ValueError(
            "staging-context table lacks frozen coordinate columns"
        )
    observed = set(contexts["context"].astype(str).unique())
    if observed != set(CONTEXT_ORDER):
        raise ValueError("staging contexts do not match frozen three-context map")

    coords = {}
    for context in CONTEXT_ORDER:
        subset = contexts[contexts["context"].astype(str) == context]
        coords[context] = (
            float(subset["centroid_lon"].median()),
            float(subset["centroid_lat"].median()),
        )
    target = (
        float(contexts["target_bylot_lon"].median()),
        float(contexts["target_bylot_lat"].median()),
    )
    if not all(math.isfinite(v) for pair in coords.values() for v in pair):
        raise ValueError("non-finite context coordinates")
    if not all(math.isfinite(v) for v in target):
        raise ValueError("non-finite Bylot target coordinates")

    bearings = {}
    for i, context in enumerate(CONTEXT_ORDER):
        destination = (
            coords[CONTEXT_ORDER[i + 1]]
            if i + 1 < len(CONTEXT_ORDER)
            else target
        )
        bearings[context] = initial_bearing_deg(
            coords[context][0],
            coords[context][1],
            destination[0],
            destination[1],
        )
    return coords, target, bearings


def main():
    args = parse_args()
    try:
        import pandas as pd
        import requests
    except ImportError as exc:
        raise RuntimeError(
            "snow-goose climate construction requires pandas and requests"
        ) from exc

    contexts = pd.read_csv(args.staging_contexts)
    risk = pd.read_csv(args.day_risk)
    required_risk = {"individual_id", "year", "context", "date"}
    if not required_risk.issubset(risk.columns):
        raise ValueError("day-risk skeleton lacks required identity columns")

    risk["year"] = risk["year"].astype(int)
    risk["context"] = risk["context"].astype(str)
    focal_years = sorted(int(v) for v in risk["year"].unique())
    if not focal_years:
        raise ValueError("no focal years in day-risk table")

    coords, target, bearings = _fixed_coordinates(contexts)
    first_history = min(focal_years) - 20
    last_focal = max(focal_years)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "PAYOFF-B-greater-snow-goose-climate/1.0"
    })

    climate = {}
    request_log = []
    for context in CONTEXT_ORDER:
        lon, lat = coords[context]
        for year in range(first_history, last_focal + 1):
            payload, meta = _request_location_year(
                session,
                location_id=context,
                lat=lat,
                lon=lon,
                year=year,
                route_bearing=bearings[context],
                max_retries=args.max_retries,
            )
            climate[(context, year)] = _strict_daily(
                payload,
                route_bearing=bearings[context],
            )
            request_log.append(meta)
            time.sleep(args.sleep_seconds)

    # The focal-year future target is deliberately never downloaded.
    for year in range(first_history, last_focal):
        payload, meta = _request_location_year(
            session,
            location_id="target_bylot",
            lat=target[1],
            lon=target[0],
            year=year,
            route_bearing=None,
            max_retries=args.max_retries,
        )
        climate[("target_bylot", year)] = _strict_daily(
            payload,
            route_bearing=None,
        )
        request_log.append(meta)
        time.sleep(args.sleep_seconds)

    connectivity_rows = []
    for focal_year in focal_years:
        train = training_years(focal_year, 20)
        target_values = [
            _window_mean_temperature(
                climate[("target_bylot", year)],
                *target_window(year),
            )
            for year in train
        ]
        for context in CONTEXT_ORDER:
            origin_values = [
                _window_mean_temperature(
                    climate[(context, year)],
                    *seasonal_window(context, year),
                )
                for year in train
            ]
            est = detrended_predictive_connectivity(
                train,
                origin_values,
                target_values,
                min_pairs=15,
            )
            connectivity_rows.append({
                "context": context,
                "year": focal_year,
                "connectivity_rho": est.rho,
                "training_end_year": focal_year - 1,
                "training_years": est.n_pairs,
                "context_lon": coords[context][0],
                "context_lat": coords[context][1],
                "target_bylot_lon": target[0],
                "target_bylot_lat": target[1],
            })

    connectivity = pd.DataFrame(connectivity_rows)

    enriched_rows = []
    for row in risk.itertuples(index=False):
        context = str(row.context)
        focal_year = int(row.year)
        current_date = datetime.strptime(str(row.date), "%Y-%m-%d").date()
        train = training_years(focal_year, 20)
        anomalies = []
        for lag in (2, 1, 0):
            focal_day = current_date - timedelta(days=lag)
            focal_key = focal_day.isoformat()
            current_daily = climate[(context, focal_year)].get(focal_key)
            if current_daily is None:
                raise ValueError(
                    f"missing focal ERA5 day {context} {focal_key}"
                )
            historical = []
            for year in train:
                hist_day = date(
                    year,
                    focal_day.month,
                    focal_day.day,
                ).isoformat()
                hist_daily = climate[(context, year)].get(hist_day)
                if hist_daily is None:
                    raise ValueError(
                        f"missing historical ERA5 day {context} {hist_day}"
                    )
                historical.append(hist_daily["temperature_2m_mean"])
            baseline = sum(historical) / len(historical)
            anomalies.append(
                current_daily["temperature_2m_mean"] - baseline
            )

        current_daily = climate[(context, focal_year)][current_date.isoformat()]
        record = row._asdict()
        record.update({
            "same_day_temp_anom": anomalies[-1],
            "local_temp_anom3": sum(anomalies) / 3.0,
            "wind_support": current_daily["wind_support_mean"],
            "precipitation": current_daily["precipitation_sum"],
        })
        enriched_rows.append(record)

    enriched = pd.DataFrame(enriched_rows)
    if enriched[["local_temp_anom3", "wind_support", "precipitation"]].isna().any().any():
        raise ValueError("weather attachment produced missing primary covariates")

    args.weather_output.parent.mkdir(parents=True, exist_ok=True)
    enriched.to_csv(args.weather_output, index=False)
    args.connectivity_output.parent.mkdir(parents=True, exist_ok=True)
    connectivity.to_csv(args.connectivity_output, index=False)

    receipt = {
        "status": "PREOUTCOME_CLIMATE_TABLE_COMPLETE",
        "provider": "Open-Meteo Historical Weather API",
        "endpoint": ENDPOINT,
        "model": "era5",
        "hourly_variables": HOURLY.split(","),
        "focal_years": focal_years,
        "historical_window_years": 20,
        "first_historical_year": first_history,
        "last_target_year_downloaded": last_focal - 1,
        "focal_year_target_bylot_downloaded": False,
        "request_count": len(request_log),
        "requests": request_log,
        "route_context_coordinates": {
            context: {
                "lon": coords[context][0],
                "lat": coords[context][1],
                "bearing_to_next_deg": bearings[context],
            }
            for context in CONTEXT_ORDER
        },
        "target_bylot": {"lon": target[0], "lat": target[1]},
        "claim_boundary": [
            "ERA5 via Open-Meteo is a reproducible reanalysis source, not a claim of byte identity with prior published climate extractions",
            "predictive connectivity uses only years strictly before each focal migration year",
            "focal-year Bylot conditions are never downloaded or used",
            "same-day temperature anomaly is diagnostic only; local_temp_anom3 is the frozen primary cue",
        ],
    }
    args.receipt_output.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
