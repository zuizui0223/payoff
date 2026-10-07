#!/usr/bin/env python3
"""Build environment-only ERA5 spring onsets for the frozen q_B regions."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.barnacle_goose_phase_error_calibration import fit_gdd_jerk


ENDPOINT = "https://archive-api.open-meteo.com/v1/archive"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--regions-json",
        type=Path,
        default=Path("data/payoff_b_qb_origin_regions_20261008.json"),
    )
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--receipt", type=Path, required=True)
    p.add_argument("--max-retries", type=int, default=5)
    args = p.parse_args()

    try:
        import pandas as pd
        import requests
    except ImportError as exc:
        raise RuntimeError("ERA5 q_B onset build requires pandas/requests") from exc

    source = json.loads(args.regions_json.read_text(encoding="utf-8"))
    regions = source["regions"]
    years = [int(y) for y in source["historical_years"]]
    start_year, end_year = min(years), max(years)

    params = {
        "latitude": ",".join(f'{float(row["latitude"]):.8f}' for row in regions),
        "longitude": ",".join(f'{float(row["longitude"]):.8f}' for row in regions),
        "start_date": f"{start_year}-01-01",
        "end_date": f"{end_year}-12-31",
        "daily": "temperature_2m_mean",
        "models": "era5",
        "timezone": ",".join(["GMT"] * len(regions)),
        "cell_selection": "nearest",
        "elevation": ",".join(["nan"] * len(regions)),
        "temperature_unit": "celsius",
    }

    session = requests.Session()
    session.headers.update(
        {"User-Agent": "PAYOFF-B-qB-local-observability/1.0"}
    )
    payload = None
    request_url = None
    last = None
    for attempt in range(args.max_retries):
        try:
            response = session.get(ENDPOINT, params=params, timeout=240)
            response.raise_for_status()
            payload = response.json()
            request_url = response.url
            break
        except Exception as exc:
            last = exc
            time.sleep(5.0 * (attempt + 1))
    if payload is None:
        raise RuntimeError(f"ERA5 request failed: {last}")
    if isinstance(payload, dict):
        payload = [payload]
    if len(payload) != len(regions):
        raise RuntimeError("ERA5 response location count mismatch")

    rows = []
    min_r2 = 1.0
    for region, item in zip(regions, payload):
        daily = item["daily"]
        frame = pd.DataFrame(
            {
                "date": pd.to_datetime(daily["time"]),
                "temperature": daily["temperature_2m_mean"],
            }
        )
        frame["temperature"] = pd.to_numeric(frame["temperature"], errors="coerce")
        frame["year"] = frame["date"].dt.year
        region_key = f'{region["flyway"]}:{region["region"]}'
        for year in years:
            d = frame[
                (frame["year"] == year)
                & frame["temperature"].notna()
            ].sort_values("date")
            if len(d) < 360:
                raise RuntimeError(
                    f"{region_key}:{year} has only {len(d)} ERA5 days"
                )
            fit = fit_gdd_jerk(
                d["temperature"].astype(float).to_numpy(),
                float(region["latitude"]),
                min_r_squared=0.95,
            )
            min_r2 = min(min_r2, fit.r_squared)
            rows.append(
                {
                    "region_key": region_key,
                    "flyway": region["flyway"],
                    "region": region["region"],
                    "year": year,
                    "onset_doy": fit.onset_day,
                    "gdd_fit_r2": fit.r_squared,
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "region_key",
                "flyway",
                "region",
                "year",
                "onset_doy",
                "gdd_fit_r2",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    receipt = {
        "schema": "payoff_b_qb_era5_onsets_v1",
        "status": "ENVIRONMENT_ONLY",
        "regions": len(regions),
        "years": years,
        "region_years": len(rows),
        "minimum_gdd_fit_r2": min_r2,
        "endpoint": ENDPOINT,
        "request_url": request_url,
        "source_regions_json": str(args.regions_json),
        "claim_boundary": (
            "environmental phase anchor only; no goose behavior/outcome read"
        ),
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(args.output)
    print(args.receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
