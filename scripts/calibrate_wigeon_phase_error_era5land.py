#!/usr/bin/env python3
"""Calibrate wigeon phase-reconstruction sensitivity with ERA5-Land.

The scientific contract is frozen in
data/wigeon_phase_error_era5land_replication_registration_20260922.json.

This script retrieves Open-Meteo ERA5-Land daily mean temperature at the
original reconstructed staging-event coordinates, applies the source-faithful
January-July 5 C cumulative-minimum TGS rule, pairs the result with the frozen
NASA POWER reconstruction, refits the exact wigeon controller, and runs the
registered true-lambda=1 sensitivity nulls.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.wigeon_phase_error_calibration import (
    fit_source_faithful_controller,
    simulate_true_lambda_one_null,
    summarize_replicate_disagreement,
    tgs_onset_from_daily_mean,
)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--staging-events", type=Path, required=True)
    p.add_argument("--transitions", type=Path, required=True)
    p.add_argument(
        "--registration-json",
        type=Path,
        default=Path(
            "data/wigeon_phase_error_era5land_replication_registration_20260922.json"
        ),
    )
    p.add_argument("--batch-size", type=int, default=20)
    p.add_argument("--max-retries", type=int, default=5)
    p.add_argument("--sleep-seconds", type=float, default=0.2)
    p.add_argument(
        "--events-output",
        type=Path,
        default=Path(
            "outputs/wigeon_power_era5land_event_calibration.csv"
        ),
    )
    p.add_argument(
        "--transitions-output",
        type=Path,
        default=Path(
            "outputs/wigeon_power_era5land_transition_calibration.csv"
        ),
    )
    p.add_argument(
        "--raw-request-output",
        type=Path,
        default=Path(
            "outputs/wigeon_era5land_request_receipt.json"
        ),
    )
    p.add_argument(
        "--receipt-output",
        type=Path,
        default=Path(
            "outputs/wigeon_phase_error_era5land_calibration_receipt.json"
        ),
    )
    p.add_argument("--fail-on-gate-failure", action="store_true")
    return p.parse_args()


def chunks(frame, size: int):
    for start in range(0, len(frame), size):
        yield frame.iloc[start : start + size].copy()


def event_key(individual_id, year, segment):
    return (str(individual_id), int(year), int(segment))


def request_batch(session, endpoint, rows, year, *, max_retries):
    latitudes = [float(v) for v in rows["lat"]]
    longitudes = [float(v) for v in rows["lon"]]
    count = len(rows)
    params = {
        "latitude": ",".join(f"{v:.8f}" for v in latitudes),
        "longitude": ",".join(f"{v:.8f}" for v in longitudes),
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-07-31",
        "daily": "temperature_2m_mean",
        "models": "era5_land",
        "timezone": ",".join(["GMT"] * count),
        "cell_selection": "nearest",
        "elevation": ",".join(["nan"] * count),
        "temperature_unit": "celsius",
    }

    last = None
    for attempt in range(max_retries):
        try:
            response = session.get(endpoint, params=params, timeout=120)
            response.raise_for_status()
            payload = response.json()
            if isinstance(payload, dict):
                payload = [payload]
            if not isinstance(payload, list) or len(payload) != count:
                raise RuntimeError(
                    "Open-Meteo response count does not match request count"
                )
            return payload, {
                "url": response.url,
                "year": int(year),
                "locations": count,
                "status_code": int(response.status_code),
            }
        except Exception as exc:
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(
        f"Open-Meteo ERA5-Land request failed after {max_retries} attempts: {last}"
    )


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


def extract_era5_events(
    staging,
    registration,
    *,
    batch_size,
    max_retries,
    sleep_seconds,
    session=None,
):
    try:
        import numpy as np
        import pandas as pd
        import requests
    except ImportError as exc:
        raise RuntimeError(
            "wigeon ERA5-Land calibration requires pandas, numpy and requests"
        ) from exc

    endpoint = registration["replicate_environment_source"]["api_endpoint"]
    session = requests.Session() if session is None else session
    session.headers.update(
        {
            "User-Agent": (
                "PAYOFF-B-wigeon-phase-error-calibration/1.0 "
                "(scientific reproducibility workflow)"
            )
        }
    )

    required = {
        "individual_id",
        "year",
        "segment",
        "arrival_doy",
        "arrival_phase_days",
        "tgs_onset_doy",
        "lat",
        "lon",
    }
    missing = required.difference(staging.columns)
    if missing:
        raise ValueError(
            "staging events missing columns: "
            + ", ".join(sorted(missing))
        )

    rows = []
    requests_log = []
    for year in sorted(int(v) for v in staging["year"].unique()):
        subset = staging[staging["year"] == year].copy()
        for batch_index, batch in enumerate(chunks(subset, batch_size), start=1):
            payloads, request_meta = request_batch(
                session,
                endpoint,
                batch,
                year,
                max_retries=max_retries,
            )
            request_meta["batch_index"] = batch_index
            requests_log.append(request_meta)

            for (source_index, source), payload in zip(
                batch.iterrows(), payloads
            ):
                valid = finite_daily_pairs(payload)
                individual_retry_performed = False
                if len(valid) < 210:
                    retry_payloads, retry_meta = request_batch(
                        session,
                        endpoint,
                        batch.loc[[source_index]],
                        year,
                        max_retries=max_retries,
                    )
                    retry_meta["batch_index"] = batch_index
                    retry_meta["request_kind"] = "single_location_retry"
                    retry_meta["event_identity"] = {
                        "individual_id": str(source["individual_id"]),
                        "year": int(source["year"]),
                        "segment": int(source["segment"]),
                    }
                    requests_log.append(retry_meta)
                    payload = retry_payloads[0]
                    valid = finite_daily_pairs(payload)
                    individual_retry_performed = True

                status = "PASS"
                era5_tgs = None
                reason = None
                if len(valid) < 210:
                    status = "INSUFFICIENT_JAN_JUL_DAILY_DATA"
                    reason = f"valid_days={len(valid)}"
                else:
                    try:
                        era5_tgs = tgs_onset_from_daily_mean(
                            [row[0] for row in valid],
                            [float(row[1]) for row in valid],
                            threshold_c=5.0,
                        )
                    except Exception as exc:
                        status = "TGS_RECONSTRUCTION_FAILED"
                        reason = f"{type(exc).__name__}:{exc}"

                era5_phase = (
                    None
                    if era5_tgs is None
                    else float(source["arrival_doy"]) - float(era5_tgs)
                )
                power_phase = float(source["arrival_phase_days"])
                phase_difference = (
                    None
                    if era5_phase is None
                    else era5_phase - power_phase
                )

                rows.append(
                    {
                        "individual_id": str(source["individual_id"]),
                        "year": int(source["year"]),
                        "segment": int(source["segment"]),
                        "arrival_doy": float(source["arrival_doy"]),
                        "event_lat": float(source["lat"]),
                        "event_lon": float(source["lon"]),
                        "power_tgs_onset_doy": float(source["tgs_onset_doy"]),
                        "power_phase_days": power_phase,
                        "era5land_tgs_onset_doy": era5_tgs,
                        "era5land_phase_days": era5_phase,
                        "era5land_minus_power_phase_days": phase_difference,
                        "provider_grid_lat": payload.get("latitude"),
                        "provider_grid_lon": payload.get("longitude"),
                        "provider_grid_elevation": payload.get("elevation"),
                        "valid_daily_values": len(valid),
                        "individual_retry_performed": (
                            individual_retry_performed
                        ),
                        "status": status,
                        "reason": reason,
                    }
                )
            time.sleep(sleep_seconds)

    result = pd.DataFrame(rows)
    if result.duplicated(["individual_id", "year", "segment"]).any():
        raise ValueError("duplicate staging-event identity after ERA5-Land query")
    return result, requests_log


def build_transition_table(frozen, events):
    import numpy as np
    import pandas as pd

    lookup = {
        event_key(row.individual_id, row.year, row.segment): row
        for row in events.itertuples(index=False)
    }
    rows = []
    for row in frozen.itertuples(index=False):
        origin = lookup.get(
            event_key(row.individual_id, row.year, row.origin_segment)
        )
        destination = lookup.get(
            event_key(row.individual_id, row.year, row.destination_segment)
        )
        if origin is None or destination is None:
            raise ValueError("frozen transition cannot be mapped to staging events")

        rows.append(
            {
                **row._asdict(),
                "power_origin_phase": float(row.origin_phase),
                "power_destination_phase": float(row.destination_phase),
                "era5_origin_phase": (
                    np.nan
                    if origin.era5land_phase_days is None
                    else float(origin.era5land_phase_days)
                ),
                "era5_destination_phase": (
                    np.nan
                    if destination.era5land_phase_days is None
                    else float(destination.era5land_phase_days)
                ),
                "origin_replicate_difference": (
                    np.nan
                    if origin.era5land_minus_power_phase_days is None
                    else float(origin.era5land_minus_power_phase_days)
                ),
                "destination_replicate_difference": (
                    np.nan
                    if destination.era5land_minus_power_phase_days is None
                    else float(destination.era5land_minus_power_phase_days)
                ),
            }
        )
    return pd.DataFrame(rows)


def phase_validation(events, registration):
    valid = events[events["status"] == "PASS"].copy()
    phase = valid["era5land_phase_days"].astype(float)
    ref = registration["coverage_gate"]["published_phase_validation"]
    median_value = float(phase.median()) if len(phase) else None
    q1 = float(phase.quantile(0.25)) if len(phase) else None
    q3 = float(phase.quantile(0.75)) if len(phase) else None

    event_gate = len(phase) >= int(ref["minimum_events"])
    median_gate = (
        median_value is not None
        and abs(median_value - float(ref["reference_median_days"]))
        <= float(ref["maximum_abs_median_difference_days"])
    )
    iqr_gate = (
        q1 is not None
        and q3 is not None
        and q1 <= float(ref["reference_q3_days"])
        and q3 >= float(ref["reference_q1_days"])
    )
    return {
        "n_events": int(len(phase)),
        "median_days": median_value,
        "q1_days": q1,
        "q3_days": q3,
        "event_count_gate": bool(event_gate),
        "median_gate": bool(median_gate),
        "iqr_overlap_gate": bool(iqr_gate),
        "all_passed": bool(event_gate and median_gate and iqr_gate),
    }


def main():
    args = parse_args()
    if args.batch_size <= 0:
        raise SystemExit("--batch-size must be positive")

    try:
        import numpy as np
        import pandas as pd
        from scipy.stats import pearsonr
    except ImportError as exc:
        raise RuntimeError(
            "wigeon ERA5-Land calibration requires empirical dependencies"
        ) from exc

    registration = json.loads(
        args.registration_json.read_text(encoding="utf-8")
    )
    staging = pd.read_csv(args.staging_events)
    transitions = pd.read_csv(args.transitions)
    staging["individual_id"] = staging["individual_id"].astype(str)
    transitions["individual_id"] = transitions["individual_id"].astype(str)

    if len(staging) != 256:
        raise SystemExit(
            f"frozen staging-event count mismatch: {len(staging)} != 256"
        )
    if len(transitions) != 224:
        raise SystemExit(
            f"frozen transition count mismatch: {len(transitions)} != 224"
        )
    if transitions["individual_id"].nunique() != 28:
        raise SystemExit("frozen wigeon transition individual count mismatch")

    events, request_log = extract_era5_events(
        staging,
        registration,
        batch_size=args.batch_size,
        max_retries=args.max_retries,
        sleep_seconds=args.sleep_seconds,
    )
    valid_events = events[events["status"] == "PASS"].copy()
    paired_fraction = len(valid_events) / len(events)

    coverage_contract = registration["coverage_gate"]
    coverage_gate = (
        len(valid_events)
        >= int(coverage_contract["minimum_events_with_both_reconstructions"])
        and paired_fraction
        >= float(coverage_contract["minimum_fraction_of_frozen_256_events"])
        and not (
            coverage_contract["require_no_ERA5_TGS_at_or_after_doy_300"]
            and (
                valid_events["era5land_tgs_onset_doy"].astype(float) >= 300
            ).any()
        )
    )
    published_validation = phase_validation(events, registration)
    coverage_gate = bool(
        coverage_gate and published_validation["all_passed"]
    )

    disagreement = summarize_replicate_disagreement(
        valid_events["era5land_minus_power_phase_days"].astype(float)
    )

    calibrated_transitions = build_transition_table(
        transitions,
        events,
    )
    complete = calibrated_transitions.dropna(
        subset=[
            "era5_origin_phase",
            "era5_destination_phase",
            "origin_replicate_difference",
            "destination_replicate_difference",
        ]
    ).copy()

    all_frozen_transitions_complete = len(complete) == 224

    power_fit_full = fit_source_faithful_controller(
        calibrated_transitions,
        origin_phase_column="power_origin_phase",
        destination_phase_column="power_destination_phase",
    )
    power_fit_paired = fit_source_faithful_controller(
        complete,
        origin_phase_column="power_origin_phase",
        destination_phase_column="power_destination_phase",
    )
    era5_fit = fit_source_faithful_controller(
        complete,
        origin_phase_column="era5_origin_phase",
        destination_phase_column="era5_destination_phase",
    )

    identity = registration["lambda_reestimation"]["power_refit_identity_gate"]
    power_identity_error = abs(
        power_fit_full.lambda_hat - float(identity["expected_lambda_hat"])
    )
    power_identity_gate = (
        power_identity_error
        <= float(identity["maximum_absolute_difference"])
    )

    correlation = pearsonr(
        complete["origin_replicate_difference"].astype(float),
        complete["destination_replicate_difference"].astype(float),
    )
    discrepancy_correlation = float(correlation.statistic)
    discrepancy_correlation_p = float(correlation.pvalue)

    null_config = registration[
        "true_lambda_one_sensitivity"
    ]["null_distribution"]
    equal_error_sd = disagreement.equal_independent_replicate_error_sd
    full_disagreement_sd = disagreement.sample_sd
    scenarios = [
        simulate_true_lambda_one_null(
            name="equal_independent_replicates_rho0",
            observed_lambda_hat=power_fit_full.lambda_hat,
            observed_residualized_predictor_sd=(
                power_fit_full.residualized_origin_phase_sd
            ),
            predictor_error_sd=equal_error_sd,
            error_correlation=0.0,
            process_noise_sd=power_fit_full.process_residual_sample_sd,
            n_pairs=int(null_config["n_pairs"]),
            replicates=int(null_config["replicates"]),
            seed=int(null_config["seed"]),
        ),
        simulate_true_lambda_one_null(
            name="equal_replicates_discrepancy_correlation_proxy",
            observed_lambda_hat=power_fit_full.lambda_hat,
            observed_residualized_predictor_sd=(
                power_fit_full.residualized_origin_phase_sd
            ),
            predictor_error_sd=equal_error_sd,
            error_correlation=discrepancy_correlation,
            process_noise_sd=power_fit_full.process_residual_sample_sd,
            n_pairs=int(null_config["n_pairs"]),
            replicates=int(null_config["replicates"]),
            seed=int(null_config["seed"]) + 1,
        ),
        simulate_true_lambda_one_null(
            name="conservative_full_disagreement_rho0",
            observed_lambda_hat=power_fit_full.lambda_hat,
            observed_residualized_predictor_sd=(
                power_fit_full.residualized_origin_phase_sd
            ),
            predictor_error_sd=full_disagreement_sd,
            error_correlation=0.0,
            process_noise_sd=power_fit_full.process_residual_sample_sd,
            n_pairs=int(null_config["n_pairs"]),
            replicates=int(null_config["replicates"]),
            seed=int(null_config["seed"]) + 2,
        ),
    ]

    args.events_output.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(args.events_output, index=False)
    args.transitions_output.parent.mkdir(parents=True, exist_ok=True)
    calibrated_transitions.to_csv(args.transitions_output, index=False)

    args.raw_request_output.parent.mkdir(parents=True, exist_ok=True)
    args.raw_request_output.write_text(
        json.dumps(
            {
                "endpoint": registration[
                    "replicate_environment_source"
                ]["api_endpoint"],
                "model": "era5_land",
                "requests": request_log,
                "request_count": len(request_log),
                "claim_boundary": (
                    "request provenance only; no claim that Open-Meteo output "
                    "is byte-identical to the authors' original CDS archive"
                ),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    receipt = {
        "status": (
            "wigeon_phase_error_calibration_complete"
            if coverage_gate and power_identity_gate
            else "wigeon_phase_error_calibration_gate_fail"
        ),
        "registration_source": str(args.registration_json),
        "source_counts": {
            "staging_events": int(len(staging)),
            "frozen_transitions": int(len(transitions)),
            "paired_events": int(len(valid_events)),
            "paired_event_fraction": float(paired_fraction),
            "complete_transition_pairs": int(len(complete)),
            "all_frozen_transitions_complete": bool(
                all_frozen_transitions_complete
            ),
        },
        "coverage_gate_passed": coverage_gate,
        "published_phase_validation": published_validation,
        "power_refit_identity": {
            "passed": power_identity_gate,
            "expected_lambda_hat": float(
                identity["expected_lambda_hat"]
            ),
            "observed_lambda_hat": power_fit_full.lambda_hat,
            "absolute_difference": power_identity_error,
            "tolerance": float(identity["maximum_absolute_difference"]),
        },
        "replicate_disagreement": asdict(disagreement),
        "equal_independent_replicate_sensitivity_error_sd": (
            disagreement.equal_independent_replicate_error_sd
        ),
        "conservative_full_disagreement_scale": disagreement.sample_sd,
        "consecutive_discrepancy_correlation": {
            "pearson_r": discrepancy_correlation,
            "p_value": discrepancy_correlation_p,
            "role": (
                "sensitivity proxy for consecutive phase-error correlation; "
                "not direct source-specific error-correlation identification"
            ),
        },
        "power_controller": asdict(power_fit_full),
        "paired_power_controller": asdict(power_fit_paired),
        "era5land_controller": asdict(era5_fit),
        "controller_difference": {
            "paired_era5land_minus_power_lambda_hat": (
                era5_fit.lambda_hat - power_fit_paired.lambda_hat
            ),
            "paired_era5land_minus_power_stopover_slope": (
                era5_fit.stopover_slope - power_fit_paired.stopover_slope
            ),
        },
        "true_lambda_one_sensitivity": [
            asdict(row)
            for row in scenarios
        ],
        "outputs": {
            "events": str(args.events_output),
            "transitions": str(args.transitions_output),
            "request_receipt": str(args.raw_request_output),
        },
        "claim_boundary": [
            "POWER-ERA5-Land disagreement is a replicate-disagreement calibration, not a gold-standard error estimate.",
            "The equal-independent-replicate SD and full-disagreement SD are sensitivity scales under frozen assumptions.",
            "The true-lambda=1 simulations are FWL residual-scale parametric sensitivity nulls and do not model cluster dependence.",
            "No result changes the registered Aikens analysis or opens the Aikens lambda outcome."
        ],
    }

    args.receipt_output.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.receipt_output)
    print(
        "wigeon_era5land_calibration "
        f"status={receipt['status']} "
        f"events={len(valid_events)}/256 "
        f"transitions={len(complete)}/224 "
        f"power_lambda_full={power_fit_full.lambda_hat:.6f} "
        f"power_lambda_paired={power_fit_paired.lambda_hat:.6f} "
        f"era5_lambda_paired={era5_fit.lambda_hat:.6f} "
        f"disagreement_sd={disagreement.sample_sd:.6f}"
    )

    if (
        args.fail_on_gate_failure
        and receipt["status"]
        != "wigeon_phase_error_calibration_complete"
    ):
        raise SystemExit("wigeon ERA5-Land calibration gate failed")


if __name__ == "__main__":
    main()
