#!/usr/bin/env python3
"""Independent ERA5 reliability replication for highlighted barnacle-goose routes."""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.barnacle_goose_phase_error_calibration import (
    fit_fixed_route_lambda,
    fit_gdd_jerk,
)
from src.wigeon_phase_error_calibration import (
    summarize_replicate_disagreement,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--multiflyway-dir", type=Path, required=True)
    p.add_argument("--svalbard-dir", type=Path, required=True)
    p.add_argument(
        "--registration-json",
        type=Path,
        default=Path(
            "data/barnacle_goose_era5_phase_reliability_registration_20260924.json"
        ),
    )
    p.add_argument("--max-retries", type=int, default=5)
    p.add_argument("--sleep-seconds", type=float, default=0.25)
    p.add_argument(
        "--onsets-output",
        type=Path,
        default=Path(
            "outputs/barnacle_goose_power_era5_onsets.csv"
        ),
    )
    p.add_argument(
        "--routes-output",
        type=Path,
        default=Path(
            "outputs/barnacle_goose_power_era5_routes.csv"
        ),
    )
    p.add_argument(
        "--request-output",
        type=Path,
        default=Path(
            "outputs/barnacle_goose_era5_request_receipt.json"
        ),
    )
    p.add_argument(
        "--receipt-output",
        type=Path,
        default=Path(
            "outputs/barnacle_goose_era5_reliability_receipt.json"
        ),
    )
    p.add_argument("--fail-on-gate-failure", action="store_true")
    return p.parse_args()


def retention_class(value: float) -> str:
    if -1.0 < value < 0.0:
        return "STABLE_OVERSHOOT"
    if 0.0 <= value < 1.0:
        return "STABLE_CONTRACTION"
    return "AMPLIFICATION_OR_BOUNDARY"


def request_daily_era5_batch(
    session,
    endpoint: str,
    regions,
    *,
    start_year: int,
    end_year: int,
    max_retries: int,
):
    rows = list(regions.itertuples(index=False))
    if not rows:
        raise ValueError("ERA5 batch requires at least one region")

    latitudes = [float(row.lat) for row in rows]
    longitudes = [float(row.lon) for row in rows]
    count = len(rows)
    params = {
        "latitude": ",".join(f"{v:.8f}" for v in latitudes),
        "longitude": ",".join(f"{v:.8f}" for v in longitudes),
        "start_date": f"{start_year}-01-01",
        "end_date": f"{end_year}-12-31",
        "daily": "temperature_2m_mean",
        "models": "era5",
        "timezone": ",".join(["GMT"] * count),
        "cell_selection": "nearest",
        "elevation": ",".join(["nan"] * count),
        "temperature_unit": "celsius",
    }
    last = None
    for attempt in range(max_retries):
        try:
            response = session.get(
                endpoint,
                params=params,
                timeout=240,
            )
            response.raise_for_status()
            payload = response.json()
            if isinstance(payload, dict):
                payload = [payload]
            if not isinstance(payload, list) or len(payload) != count:
                raise RuntimeError(
                    "ERA5 batch response count does not match region count"
                )
            for item in payload:
                daily = item.get("daily", {})
                dates = daily.get("time", [])
                values = daily.get("temperature_2m_mean", [])
                if len(dates) != len(values) or not dates:
                    raise RuntimeError(
                        "ERA5 daily response missing aligned time/temperature"
                    )
            return payload, {
                "url": response.url,
                "status_code": int(response.status_code),
                "start_year": start_year,
                "end_year": end_year,
                "locations": count,
            }
        except Exception as exc:
            last = exc
            # Long multi-decade requests can trigger provider throttling.
            # Retrieval backoff changes no scientific parameter.
            time.sleep(5.0 * (attempt + 1))
    raise RuntimeError(
        f"ERA5 batch request failed after {max_retries} attempts: {last}"
    )

def era5_onsets_for_flyway(
    flyway: str,
    regions,
    *,
    period,
    endpoint,
    max_retries,
    sleep_seconds,
    session,
):
    import pandas as pd

    rows = []
    requests_log = []
    start_year, end_year = [int(v) for v in period]

    eligible = regions.copy()
    if "published_region_eligible" in eligible.columns:
        eligible = eligible[
            eligible["published_region_eligible"] == True  # noqa:E712
        ].copy()

    payloads, batch_meta = request_daily_era5_batch(
        session,
        endpoint,
        eligible,
        start_year=start_year,
        end_year=end_year,
        max_retries=max_retries,
    )
    batch_meta["flyway"] = flyway
    batch_meta["request_kind"] = "flyway_coordinate_batch"
    requests_log.append(batch_meta)

    for region, payload in zip(
        eligible.itertuples(index=False),
        payloads,
    ):
        rid = str(region.region_id)
        lat = float(region.lat)
        daily = payload["daily"]
        frame = pd.DataFrame(
            {
                "date": pd.to_datetime(daily["time"]),
                "temperature_2m_mean": daily["temperature_2m_mean"],
            }
        )
        frame["temperature_2m_mean"] = pd.to_numeric(
            frame["temperature_2m_mean"],
            errors="coerce",
        )
        frame["year"] = frame["date"].dt.year

        for year in range(start_year, end_year + 1):
            d = frame[
                (frame["year"] == year)
                & frame["temperature_2m_mean"].notna()
            ].sort_values("date")
            if len(d) < 360:
                rows.append(
                    {
                        "flyway": flyway,
                        "region_id": rid,
                        "year": year,
                        "era5_onset_doy": math.nan,
                        "era5_gdd_fit_r2": math.nan,
                        "status": "INSUFFICIENT_DAILY_DATA",
                    }
                )
                continue
            try:
                fit = fit_gdd_jerk(
                    d["temperature_2m_mean"].astype(float).to_numpy(),
                    lat,
                    min_r_squared=0.95,
                )
                rows.append(
                    {
                        "flyway": flyway,
                        "region_id": rid,
                        "year": year,
                        "era5_onset_doy": fit.onset_day,
                        "era5_gdd_fit_r2": fit.r_squared,
                        "status": "PASS",
                    }
                )
            except Exception as exc:
                rows.append(
                    {
                        "flyway": flyway,
                        "region_id": rid,
                        "year": year,
                        "era5_onset_doy": math.nan,
                        "era5_gdd_fit_r2": math.nan,
                        "status": f"FAIL:{type(exc).__name__}",
                    }
                )
    time.sleep(sleep_seconds)

    result = pd.DataFrame(rows)
    ok = result["status"] == "PASS"
    means = (
        result.loc[ok]
        .groupby("region_id")["era5_onset_doy"]
        .mean()
        .to_dict()
    )
    result["era5_region_mean_doy"] = result["region_id"].map(means)
    result["era5_onset_anomaly_days"] = (
        result["era5_onset_doy"] - result["era5_region_mean_doy"]
    )
    return result, requests_log


def load_flyway_inputs(base: Path, flyway: str):
    import pandas as pd

    if flyway == "svalbard":
        return (
            pd.read_csv(base / "stage3_svalbard_goose_regions.csv"),
            pd.read_csv(base / "stage3_svalbard_goose_power_gdd_onsets.csv"),
            pd.read_csv(base / "stage3_svalbard_goose_transitions.csv"),
        )
    return (
        pd.read_csv(base / f"stage3_{flyway}_goose_regions.csv"),
        pd.read_csv(base / f"stage3_{flyway}_goose_power_gdd_anomalies.csv"),
        pd.read_csv(base / f"stage3_{flyway}_goose_anomaly_phase_transitions.csv"),
    )


def normalize_power_onsets(frame, flyway: str):
    import pandas as pd

    data = frame.copy()
    onset_column = (
        "onset_doy"
        if flyway == "svalbard"
        else "onset_doy_raw"
    )
    required = {
        "region_id",
        "year",
        "fit_status",
        onset_column,
        "onset_anomaly_days",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(
            f"{flyway} POWER onset file missing: "
            + ", ".join(sorted(missing))
        )
    data = data[data["fit_status"].astype(str) == "PASS"].copy()
    data["region_id"] = data["region_id"].astype(str)
    data["year"] = data["year"].astype(int)
    data["power_onset_doy"] = pd.to_numeric(
        data[onset_column],
        errors="coerce",
    )
    data["power_onset_anomaly_days"] = pd.to_numeric(
        data["onset_anomaly_days"],
        errors="coerce",
    )
    return data[
        [
            "region_id",
            "year",
            "power_onset_doy",
            "power_onset_anomaly_days",
        ]
    ]


def route_calibration(
    transitions,
    paired_onsets,
    *,
    origin_region,
    destination_region,
    expected_power_lambda,
):
    import numpy as np
    import pandas as pd

    t = transitions.copy()
    t["individual_id"] = t["individual_id"].astype(str)
    t["year"] = t["year"].astype(int)
    t["origin_region"] = t["origin_region"].astype(str)
    t["destination_region"] = t["destination_region"].astype(str)

    route = t[
        (t["origin_region"] == origin_region)
        & (t["destination_region"] == destination_region)
    ].copy()

    onset_lookup = {
        (str(row.region_id), int(row.year)): row
        for row in paired_onsets.itertuples(index=False)
    }
    rows = []
    for source in route.itertuples(index=False):
        origin = onset_lookup.get(
            (origin_region, int(source.year))
        )
        destination = onset_lookup.get(
            (destination_region, int(source.year))
        )
        if origin is None or destination is None:
            continue

        rows.append(
            {
                **source._asdict(),
                "power_origin_phase": (
                    float(source.origin_arrival_doy)
                    - float(origin.power_onset_anomaly_days)
                ),
                "power_destination_phase": (
                    float(source.destination_arrival_doy)
                    - float(destination.power_onset_anomaly_days)
                ),
                "era5_origin_phase": (
                    float(source.origin_arrival_doy)
                    - float(origin.era5_onset_anomaly_days)
                ),
                "era5_destination_phase": (
                    float(source.destination_arrival_doy)
                    - float(destination.era5_onset_anomaly_days)
                ),
                "origin_era5_minus_power_phase": (
                    float(origin.power_onset_anomaly_days)
                    - float(origin.era5_onset_anomaly_days)
                ),
                "destination_era5_minus_power_phase": (
                    float(destination.power_onset_anomaly_days)
                    - float(destination.era5_onset_anomaly_days)
                ),
            }
        )

    calibrated = pd.DataFrame(rows)
    if calibrated.empty:
        raise ValueError("highlighted route has no complete ERA5 transitions")

    power_fit = fit_fixed_route_lambda(
        calibrated,
        origin_phase_column="power_origin_phase",
        destination_phase_column="power_destination_phase",
    )
    era5_fit = fit_fixed_route_lambda(
        calibrated,
        origin_phase_column="era5_origin_phase",
        destination_phase_column="era5_destination_phase",
    )
    identity_error = abs(
        power_fit.lambda_hat - float(expected_power_lambda)
    )

    origin_error = calibrated[
        "origin_era5_minus_power_phase"
    ].astype(float)
    destination_error = calibrated[
        "destination_era5_minus_power_phase"
    ].astype(float)
    correlation = None
    correlation_p = None
    if (
        len(calibrated) >= 4
        and origin_error.std(ddof=0) > 0
        and destination_error.std(ddof=0) > 0
    ):
        from scipy.stats import pearsonr
        corr = pearsonr(origin_error, destination_error)
        correlation = float(corr.statistic)
        correlation_p = float(corr.pvalue)

    return calibrated, {
        "origin_region": origin_region,
        "destination_region": destination_region,
        "power_fit": asdict(power_fit),
        "era5_fit": asdict(era5_fit),
        "power_identity_abs_error": identity_error,
        "power_identity_passed": identity_error <= 1e-8,
        "lambda_difference_era5_minus_power": (
            era5_fit.lambda_hat - power_fit.lambda_hat
        ),
        "power_retention_class": retention_class(power_fit.lambda_hat),
        "era5_retention_class": retention_class(era5_fit.lambda_hat),
        "retention_class_preserved": (
            retention_class(power_fit.lambda_hat)
            == retention_class(era5_fit.lambda_hat)
        ),
        "endpoint_phase_discrepancy_correlation": correlation,
        "endpoint_phase_discrepancy_correlation_p": correlation_p,
    }


def main():
    args = parse_args()
    try:
        import pandas as pd
        import requests
    except ImportError as exc:
        raise RuntimeError(
            "barnacle-goose ERA5 calibration requires pandas/requests"
        ) from exc

    registration = json.loads(
        args.registration_json.read_text(encoding="utf-8")
    )
    endpoint = registration["environmental_replicate"]["endpoint"]

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "PAYOFF-B-barnacle-goose-ERA5-reliability/1.0 "
                "(scientific reproducibility workflow)"
            )
        }
    )

    all_onsets = []
    all_routes = []
    request_log = []
    results = []
    gate_failures = []

    for spec in registration["flyways"]:
        flyway = str(spec["flyway"])
        base = (
            args.svalbard_dir
            if flyway == "svalbard"
            else args.multiflyway_dir
        )
        regions, power_raw, transitions = load_flyway_inputs(
            base, flyway
        )
        power = normalize_power_onsets(power_raw, flyway)
        era5, requests_for_flyway = era5_onsets_for_flyway(
            flyway,
            regions,
            period=spec["period"],
            endpoint=endpoint,
            max_retries=args.max_retries,
            sleep_seconds=args.sleep_seconds,
            session=session,
        )
        request_log.extend(requests_for_flyway)

        paired = power.merge(
            era5[era5["status"] == "PASS"][
                [
                    "region_id",
                    "year",
                    "era5_onset_doy",
                    "era5_gdd_fit_r2",
                    "era5_onset_anomaly_days",
                ]
            ],
            on=["region_id", "year"],
            how="inner",
        )
        power_pairs = len(power)
        paired_fraction = (
            len(paired) / power_pairs
            if power_pairs
            else 0.0
        )
        paired["flyway"] = flyway
        paired["era5_minus_power_onset_anomaly_days"] = (
            paired["era5_onset_anomaly_days"]
            - paired["power_onset_anomaly_days"]
        )
        all_onsets.append(paired)

        disagreement = summarize_replicate_disagreement(
            paired["era5_minus_power_onset_anomaly_days"].astype(float)
        )

        origin, destination = [
            str(v) for v in spec["highlighted_route"]
        ]
        calibrated, route_result = route_calibration(
            transitions,
            paired,
            origin_region=origin,
            destination_region=destination,
            expected_power_lambda=float(
                spec["expected_power_lambda"]
            ),
        )
        calibrated["flyway"] = flyway
        all_routes.append(calibrated)

        support_pass = (
            len(calibrated)
            >= int(spec["minimum_route_pairs"])
            and calibrated["individual_id"].nunique()
            >= int(spec["minimum_route_individuals"])
        )
        coverage_pass = (
            paired_fraction
            >= float(
                registration["gates"][
                    "minimum_paired_region_year_fraction"
                ]
            )
        )
        identity_pass = bool(
            route_result["power_identity_passed"]
        )
        flyway_gate = bool(
            support_pass
            and coverage_pass
            and identity_pass
        )
        if not flyway_gate:
            gate_failures.append(flyway)

        results.append(
            {
                "flyway": flyway,
                "period": spec["period"],
                "paired_region_years": int(len(paired)),
                "power_region_years": int(power_pairs),
                "paired_region_year_fraction": float(paired_fraction),
                "coverage_gate_passed": bool(coverage_pass),
                "route_support_gate_passed": bool(support_pass),
                "power_identity_gate_passed": bool(identity_pass),
                "flyway_execution_gate_passed": flyway_gate,
                "replicate_disagreement": asdict(disagreement),
                "equal_independent_replicate_sensitivity_error_sd_days": (
                    disagreement.equal_independent_replicate_error_sd
                ),
                **route_result,
            }
        )

    onset_table = pd.concat(all_onsets, ignore_index=True)
    route_table = pd.concat(all_routes, ignore_index=True)
    args.onsets_output.parent.mkdir(parents=True, exist_ok=True)
    onset_table.to_csv(args.onsets_output, index=False)
    args.routes_output.parent.mkdir(parents=True, exist_ok=True)
    route_table.to_csv(args.routes_output, index=False)

    args.request_output.parent.mkdir(parents=True, exist_ok=True)
    args.request_output.write_text(
        json.dumps(
            {
                "endpoint": endpoint,
                "model": "era5",
                "daily_variable": "temperature_2m_mean",
                "requests": request_log,
                "claim_boundary": (
                    "request provenance only; Open-Meteo ERA5 is an "
                    "independent replicate surface, not the original 2015 "
                    "historical climate archive"
                ),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    receipt = {
        "status": (
            "barnacle_goose_era5_reliability_complete"
            if not gate_failures
            else "barnacle_goose_era5_reliability_gate_fail"
        ),
        "registration_source": str(args.registration_json),
        "flyways": results,
        "gate_failures": gate_failures,
        "all_execution_gates_passed": not gate_failures,
        "outputs": {
            "paired_onsets": str(args.onsets_output),
            "routes": str(args.routes_output),
            "requests": str(args.request_output),
        },
        "claim_boundary": [
            "ERA5 is an independent environmental replicate, not the original historical climate input.",
            "POWER-versus-ERA5 disagreement is a sensitivity calibration, not a gold-standard error distribution.",
            "No pooled goose lambda is estimated.",
            "The Aikens lambda outcome remains unopened."
        ],
    }
    args.receipt_output.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.receipt_output)
    for row in results:
        print(
            "barnacle_era5 "
            f"flyway={row['flyway']} "
            f"power_lambda={row['power_fit']['lambda_hat']:.6f} "
            f"era5_lambda={row['era5_fit']['lambda_hat']:.6f} "
            f"coverage={row['paired_region_year_fraction']:.4f} "
            f"class_preserved={int(row['retention_class_preserved'])}"
        )

    if args.fail_on_gate_failure and gate_failures:
        raise SystemExit(
            "barnacle-goose ERA5 reliability execution gate failed: "
            + ",".join(gate_failures)
        )


if __name__ == "__main__":
    main()
