#!/usr/bin/env python3
"""Post-hoc diagnosis of coastal ERA5-Land gaps in the wigeon calibration.

The registered calibration uses Open-Meteo ERA5-Land with

    cell_selection=nearest

and that primary gate is never changed by this script.

ERA5-Land is masked over oceans. When a registered nearest-cell request returns
HTTP 200 but no finite Jan--Jul temperatures, this diagnostic repeats the same
coordinate/year/model request with

    cell_selection=land

only to test whether the missingness is consistent with coastal/ocean grid-cell
selection. Recovered rows are not substituted into the registered calibration.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.wigeon_phase_error_calibration import (
    tgs_onset_from_daily_mean,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--calibration-events", type=Path, required=True)
    p.add_argument(
        "--registration-json",
        type=Path,
        default=Path(
            "data/wigeon_phase_error_era5land_replication_registration_20260922.json"
        ),
    )
    p.add_argument("--max-retries", type=int, default=5)
    p.add_argument("--sleep-seconds", type=float, default=0.2)
    p.add_argument(
        "--events-output",
        type=Path,
        default=Path(
            "outputs/wigeon_era5land_coastal_mask_diagnostic.csv"
        ),
    )
    p.add_argument(
        "--receipt-output",
        type=Path,
        default=Path(
            "outputs/wigeon_era5land_coastal_mask_diagnostic_receipt.json"
        ),
    )
    return p.parse_args()


def finite_daily_pairs(payload):
    daily = payload.get("daily", {})
    dates = daily.get("time", [])
    temperatures = daily.get("temperature_2m_mean", [])
    return [
        (day, temperature)
        for day, temperature in zip(dates, temperatures)
        if temperature is not None
        and math.isfinite(float(temperature))
    ]


def request_land_cell(
    session,
    endpoint: str,
    *,
    latitude: float,
    longitude: float,
    year: int,
    max_retries: int,
):
    params = {
        "latitude": f"{latitude:.8f}",
        "longitude": f"{longitude:.8f}",
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-07-31",
        "daily": "temperature_2m_mean",
        "models": "era5_land",
        "timezone": "GMT",
        "cell_selection": "land",
        "elevation": "nan",
        "temperature_unit": "celsius",
    }
    last = None
    for attempt in range(max_retries):
        try:
            response = session.get(
                endpoint,
                params=params,
                timeout=120,
            )
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise RuntimeError(
                    "single-location land-cell response is not an object"
                )
            return payload, {
                "url": response.url,
                "status_code": int(response.status_code),
                "attempt": attempt + 1,
            }
        except Exception as exc:
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(
        "Open-Meteo land-cell diagnostic failed after "
        f"{max_retries} attempts: {last}"
    )


def diagnose_missing_events(
    events,
    registration,
    *,
    max_retries: int,
    sleep_seconds: float,
    session=None,
):
    try:
        import pandas as pd
        import requests
    except ImportError as exc:
        raise RuntimeError(
            "coastal-mask diagnostic requires pandas and requests"
        ) from exc

    required = {
        "individual_id",
        "year",
        "segment",
        "arrival_doy",
        "event_lat",
        "event_lon",
        "status",
        "reason",
    }
    missing = required.difference(events.columns)
    if missing:
        raise ValueError(
            "calibration event table missing columns: "
            + ", ".join(sorted(missing))
        )

    endpoint = registration[
        "replicate_environment_source"
    ]["api_endpoint"]
    session = requests.Session() if session is None else session
    session.headers.update(
        {
            "User-Agent": (
                "PAYOFF-B-wigeon-coastal-mask-diagnostic/1.0 "
                "(post-hoc scientific diagnostic)"
            )
        }
    )

    failed = events[events["status"] != "PASS"].copy()
    rows = []
    request_log = []
    for source in failed.itertuples(index=False):
        payload, meta = request_land_cell(
            session,
            endpoint,
            latitude=float(source.event_lat),
            longitude=float(source.event_lon),
            year=int(source.year),
            max_retries=max_retries,
        )
        valid = finite_daily_pairs(payload)
        land_status = "PASS"
        reason = None
        tgs = None
        if len(valid) < 210:
            land_status = "INSUFFICIENT_JAN_JUL_DAILY_DATA"
            reason = f"valid_days={len(valid)}"
        else:
            try:
                tgs = tgs_onset_from_daily_mean(
                    [row[0] for row in valid],
                    [float(row[1]) for row in valid],
                    threshold_c=5.0,
                )
            except Exception as exc:
                land_status = "TGS_RECONSTRUCTION_FAILED"
                reason = f"{type(exc).__name__}:{exc}"

        land_phase = (
            None
            if tgs is None
            else float(source.arrival_doy) - float(tgs)
        )
        rows.append(
            {
                "individual_id": str(source.individual_id),
                "year": int(source.year),
                "segment": int(source.segment),
                "event_lat": float(source.event_lat),
                "event_lon": float(source.event_lon),
                "registered_nearest_status": str(source.status),
                "registered_nearest_reason": (
                    None
                    if pd.isna(source.reason)
                    else str(source.reason)
                ),
                "diagnostic_cell_selection": "land",
                "land_status": land_status,
                "land_valid_daily_values": len(valid),
                "land_tgs_onset_doy": tgs,
                "land_phase_days": land_phase,
                "provider_grid_lat": payload.get("latitude"),
                "provider_grid_lon": payload.get("longitude"),
                "provider_grid_elevation": payload.get("elevation"),
                "reason": reason,
            }
        )
        request_log.append(
            {
                **meta,
                "individual_id": str(source.individual_id),
                "year": int(source.year),
                "segment": int(source.segment),
                "cell_selection": "land",
            }
        )
        time.sleep(sleep_seconds)

    return pd.DataFrame(rows), request_log


def main():
    args = parse_args()
    if args.max_retries <= 0:
        raise SystemExit("--max-retries must be positive")

    import pandas as pd

    events = pd.read_csv(args.calibration_events)
    registration = json.loads(
        args.registration_json.read_text(encoding="utf-8")
    )
    diagnostic, request_log = diagnose_missing_events(
        events,
        registration,
        max_retries=args.max_retries,
        sleep_seconds=args.sleep_seconds,
    )

    args.events_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    diagnostic.to_csv(
        args.events_output,
        index=False,
    )

    primary_pass = int((events["status"] == "PASS").sum())
    missing_count = int((events["status"] != "PASS").sum())
    recovered = int(
        (diagnostic["land_status"] == "PASS").sum()
    ) if len(diagnostic) else 0
    counterfactual_coverage = (
        (primary_pass + recovered) / len(events)
        if len(events)
        else 0.0
    )

    receipt = {
        "status": "wigeon_era5land_coastal_mask_diagnostic_complete",
        "role": "POST_HOC_DIAGNOSTIC_ONLY",
        "registered_primary_cell_selection": "nearest",
        "diagnostic_cell_selection": "land",
        "primary_gate_changed": False,
        "primary_valid_events": primary_pass,
        "primary_missing_events": missing_count,
        "land_recovered_missing_events": recovered,
        "land_recovery_fraction_of_missing": (
            recovered / missing_count
            if missing_count
            else 0.0
        ),
        "counterfactual_event_coverage_if_land_recovery_were_used": (
            counterfactual_coverage
        ),
        "all_missing_events_recovered_by_land_cell": (
            recovered == missing_count
        ),
        "requests": request_log,
        "outputs": {
            "events": str(args.events_output),
        },
        "claim_boundary": [
            "The registered nearest-cell calibration gate remains unchanged.",
            "Land-cell recovery is post-hoc and cannot convert the registered calibration from FAIL to PASS.",
            "This diagnostic tests whether HTTP-200/null ERA5-Land responses are consistent with ocean-masked nearest cells at coastal staging coordinates.",
        ],
    }
    args.receipt_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.receipt_output)
    print(
        "wigeon_era5land_coastal_mask "
        f"primary_missing={missing_count} "
        f"land_recovered={recovered} "
        f"counterfactual_coverage={counterfactual_coverage:.6f}"
    )


if __name__ == "__main__":
    main()
