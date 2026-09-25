#!/usr/bin/env python3
"""Evaluate calendar-duration decay as a retrospective lambda sensitivity."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd

from src.interval_duration_phase_decay import (
    classify_duration_evidence,
    compare_segment_and_duration_models,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_hash(path: Path, expected: str) -> None:
    actual = sha256(path)
    if actual != expected:
        raise ValueError(
            f"source hash mismatch for {path}: {actual} != {expected}"
        )


def intercept(n: int) -> np.ndarray:
    return np.ones((n, 1), dtype=float)


def add_log_duration_nuisance(z: np.ndarray, duration) -> np.ndarray:
    raw = np.log(np.asarray(duration, dtype=float))
    sd = float(raw.std(ddof=0))
    if sd <= 0.0 or not math.isfinite(sd):
        raise ValueError("log duration has no usable variation")
    scaled = (raw - float(raw.mean())) / sd
    return np.column_stack([z, scaled])


def wigeon_with_duration(transitions: pd.DataFrame, events: pd.DataFrame):
    tr = transitions.copy()
    ev = events[["individual_id", "year", "segment", "arrival_doy"]].copy()
    tr["individual_id"] = tr["individual_id"].astype(str)
    ev["individual_id"] = ev["individual_id"].astype(str)
    origin = ev.rename(
        columns={
            "segment": "origin_segment",
            "arrival_doy": "origin_arrival_doy",
        }
    )
    destination = ev.rename(
        columns={
            "segment": "destination_segment",
            "arrival_doy": "destination_arrival_doy",
        }
    )
    tr = tr.merge(
        origin,
        on=["individual_id", "year", "origin_segment"],
        how="left",
        validate="many_to_one",
    ).merge(
        destination,
        on=["individual_id", "year", "destination_segment"],
        how="left",
        validate="many_to_one",
    )
    tr["delta_t_days"] = (
        tr["destination_arrival_doy"] - tr["origin_arrival_doy"]
    )
    if tr["delta_t_days"].isna().any() or (tr["delta_t_days"] <= 0).any():
        raise ValueError("wigeon duration join produced invalid intervals")
    return tr


def wigeon_nuisance(data: pd.DataFrame) -> np.ndarray:
    d = data.copy()
    cols = []
    for column in ("origin_progress_km", "endpoint_distance_km"):
        values = d[column].astype(float).to_numpy()
        sd = float(values.std(ddof=0))
        if sd <= 0.0:
            raise ValueError(f"{column} has no variation")
        cols.append((values - float(values.mean())) / sd)
    z_progress, z_endpoint = cols
    design = [
        np.ones(len(d), dtype=float),
        z_progress,
        z_endpoint,
        z_progress * z_endpoint,
    ]
    years = sorted(int(y) for y in d["year"].unique())
    year_values = d["year"].astype(int).to_numpy()
    for year in years[1:]:
        design.append((year_values == year).astype(float))
    return np.column_stack(design)


def run_pair(
    *,
    name: str,
    data: pd.DataFrame,
    origin_column: str,
    destination_column: str,
    duration_column: str,
    nuisance: np.ndarray,
    groups,
    expected_lambda: float,
    identity_tolerance: float,
):
    primary = compare_segment_and_duration_models(
        origin_phase=data[origin_column].to_numpy(dtype=float),
        destination_phase=data[destination_column].to_numpy(dtype=float),
        duration_days=data[duration_column].to_numpy(dtype=float),
        nuisance=nuisance,
        groups=groups,
    )
    reproduced = primary["segment_model"]["lambda_hat"]
    if abs(reproduced - expected_lambda) > identity_tolerance:
        raise ValueError(
            f"{name} constant-lambda identity gate failed: "
            f"{reproduced} vs {expected_lambda}"
        )

    adjusted_nuisance = add_log_duration_nuisance(
        nuisance,
        data[duration_column].to_numpy(dtype=float),
    )
    adjusted = compare_segment_and_duration_models(
        origin_phase=data[origin_column].to_numpy(dtype=float),
        destination_phase=data[destination_column].to_numpy(dtype=float),
        duration_days=data[duration_column].to_numpy(dtype=float),
        nuisance=adjusted_nuisance,
        groups=groups,
    )

    d0 = primary["delta_aic_duration_minus_segment"]
    d1 = adjusted["delta_aic_duration_minus_segment"]
    return {
        "system_id": name,
        "constant_lambda_identity_gate": "PASS",
        "expected_lambda": expected_lambda,
        "original_matched": primary,
        "log_duration_adjusted": adjusted,
        "classification": classify_duration_evidence(d0, d1),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--contract", type=Path, required=True)
    p.add_argument("--mule-deer", type=Path, required=True)
    p.add_argument("--wigeon-power-transitions", type=Path, required=True)
    p.add_argument("--wigeon-power-events", type=Path, required=True)
    p.add_argument("--wigeon-era5-transitions", type=Path, required=True)
    p.add_argument("--wigeon-era5-events", type=Path, required=True)
    p.add_argument("--greenland", type=Path, required=True)
    p.add_argument("--barents", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    if contract["Aikens_lambda_outcome_opened"] is not False:
        raise ValueError("Aikens outcome must remain unopened")

    source = contract["sources"]
    require_hash(args.mule_deer, source["mule_deer"]["file_sha256"])
    require_hash(
        args.wigeon_power_transitions,
        source["wigeon_power"]["transition_sha256"],
    )
    require_hash(
        args.wigeon_power_events,
        source["wigeon_power"]["event_sha256"],
    )
    require_hash(
        args.wigeon_era5_transitions,
        source["wigeon_era5"]["transition_sha256"],
    )
    require_hash(
        args.wigeon_era5_events,
        source["wigeon_era5"]["event_sha256"],
    )
    require_hash(
        args.greenland,
        source["barnacle_greenland"]["file_sha256"],
    )
    require_hash(
        args.barents,
        source["barnacle_barents"]["file_sha256"],
    )

    rows = []

    mule = pd.read_csv(args.mule_deer)
    mule = mule.dropna(
        subset=["DFP_Start", "DFP_End", "DOY_Start", "DOY_End", "individual_id"]
    ).copy()
    mule["delta_t_days"] = (
        mule["DOY_End"].astype(float) - mule["DOY_Start"].astype(float)
    )
    rows.append(
        run_pair(
            name="mule_deer_whole_migration",
            data=mule,
            origin_column="DFP_Start",
            destination_column="DFP_End",
            duration_column="delta_t_days",
            nuisance=intercept(len(mule)),
            groups=mule["individual_id"].astype(str).to_numpy(),
            expected_lambda=float(source["mule_deer"]["expected_lambda"]),
            identity_tolerance=1e-9,
        )
    )

    wp = wigeon_with_duration(
        pd.read_csv(args.wigeon_power_transitions),
        pd.read_csv(args.wigeon_power_events),
    )
    rows.append(
        run_pair(
            name="eurasian_wigeon_POWER",
            data=wp,
            origin_column="origin_phase",
            destination_column="destination_phase",
            duration_column="delta_t_days",
            nuisance=wigeon_nuisance(wp),
            groups=wp["individual_id"].astype(str).to_numpy(),
            expected_lambda=float(source["wigeon_power"]["expected_lambda"]),
            identity_tolerance=1e-9,
        )
    )

    we = wigeon_with_duration(
        pd.read_csv(args.wigeon_era5_transitions),
        pd.read_csv(args.wigeon_era5_events),
    )
    rows.append(
        run_pair(
            name="eurasian_wigeon_ERA5",
            data=we,
            origin_column="era5_origin_phase",
            destination_column="era5_destination_phase",
            duration_column="delta_t_days",
            nuisance=wigeon_nuisance(we),
            groups=we["individual_id"].astype(str).to_numpy(),
            expected_lambda=float(source["wigeon_era5"]["expected_lambda"]),
            identity_tolerance=1e-9,
        )
    )

    for key, path, origin, destination in (
        ("barnacle_greenland", args.greenland, "R2", "R3"),
        ("barnacle_barents", args.barents, "R1", "R2"),
    ):
        frame = pd.read_csv(path)
        data = frame[
            (frame["origin_region"] == origin)
            & (frame["destination_region"] == destination)
        ].copy()
        data["delta_t_days"] = (
            data["destination_arrival_doy"].astype(float)
            - data["origin_arrival_doy"].astype(float)
        )
        rows.append(
            run_pair(
                name=key,
                data=data,
                origin_column="origin_arrival_phase_anom",
                destination_column="destination_arrival_phase_anom",
                duration_column="delta_t_days",
                nuisance=intercept(len(data)),
                groups=data["individual_id"].astype(str).to_numpy(),
                expected_lambda=float(source[key]["expected_lambda"]),
                identity_tolerance=1e-8,
            )
        )

    result = {
        "result_id": "payoff_b_phase_duration_decay_sensitivity_20260925",
        "created_date": contract["created_date"],
        "contract_id": contract["contract_id"],
        "status": "RETROSPECTIVE_DURATION_MODEL_DIAGNOSTIC_COMPLETE",
        "Aikens_lambda_outcome_opened": False,
        "systems": rows,
        "svalbard_boundary": source["barnacle_svalbard_boundary"],
        "claim_boundary": [
            "this is retrospective diagnostic evidence, not prospective support",
            "raw registered lambda results are unchanged",
            "calendar-time exponential decay is only one possible duration model",
            "negative-lambda overshoot is not representable by monotone exponential retention",
            "Aikens fixed-24h registration is unchanged and outcome remains unopened",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
