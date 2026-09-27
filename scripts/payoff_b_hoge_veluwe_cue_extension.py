#!/usr/bin/env python3
"""Source-faithful extension of the frozen Ivory Coast cue through 2015.

This module deliberately reuses the exact CV24C NCEP/NCAR downloader and fixed
20-day / 3x3 spatial rule. It does not read resource, resident or migrant
phenology and therefore cannot tune the cue against the joined outcome.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from payoff_b_cv24c_cue_driver import ERDDAP, _download_annual_cue


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--baseline",
        type=Path,
        default=ROOT / "data" / "payoff_b_cv24c_frozen_cue_prefix_1980_2010.json",
    )
    p.add_argument("--start-year", type=int, default=1980)
    p.add_argument("--end-year", type=int, default=2015)
    p.add_argument(
        "--annual-output",
        type=Path,
        default=Path("outputs/hoge_veluwe_cue_extension_annual.csv"),
    )
    p.add_argument(
        "--receipt-output",
        type=Path,
        default=Path("outputs/hoge_veluwe_cue_extension_receipt.json"),
    )
    p.add_argument("--erddap", default=ERDDAP)
    return p.parse_args()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()



def canonical_hash(rows: list[dict], digits: int = 9) -> str:
    canonical = [
        [
            int(row["year"]),
            round(float(row["ivory_coast_temp_c"]), digits),
        ]
        for row in sorted(rows, key=lambda row: int(row["year"]))
    ]
    payload = (json.dumps(canonical, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(payload).hexdigest()


def validate_frozen_prefix(
    frame,
    baseline: dict,
    *,
    tolerance_c: float = 1e-9,
) -> dict:
    expected = {
        int(row["year"]): float(row["ivory_coast_temp_c"])
        for row in baseline["rows"]
    }
    observed = {
        int(row.year): float(row.ivory_coast_temp_c)
        for row in frame.itertuples(index=False)
        if int(row.year) in expected
    }
    if set(observed) != set(expected):
        return {
            "passed": False,
            "reason": "frozen prefix years do not match",
            "expected_years": sorted(expected),
            "observed_years": sorted(observed),
        }
    differences = {
        year: observed[year] - expected[year]
        for year in sorted(expected)
    }
    max_abs = max(abs(value) for value in differences.values())
    expected_rows = [
        {"year": year, "ivory_coast_temp_c": expected[year]}
        for year in sorted(expected)
    ]
    observed_rows = [
        {"year": year, "ivory_coast_temp_c": observed[year]}
        for year in sorted(expected)
    ]
    return {
        "passed": max_abs <= tolerance_c,
        "tolerance_c": tolerance_c,
        "max_abs_difference_c": max_abs,
        "expected_round9_sha256": canonical_hash(expected_rows, 9),
        "observed_round9_sha256": canonical_hash(observed_rows, 9),
        "expected_round12_sha256": baseline["canonical_round_12_sha256"],
        "observed_round12_sha256": canonical_hash(observed_rows, 12),
    }


def build_rows(start_year: int, end_year: int, erddap: str):
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    session = requests.Session()
    session.headers.update(
        {"User-Agent": "PAYOFF-B-Hoge-Veluwe-cue-extension/1.0"}
    )
    retry = Retry(
        total=8,
        connect=5,
        read=5,
        status=8,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return [
        _download_annual_cue(session, erddap, year)
        for year in range(start_year, end_year + 1)
    ]


def main():
    args = parse_args()
    import pandas as pd

    if args.start_year != 1980 or args.end_year != 2015:
        raise ValueError(
            "registered Hoge Veluwe cue extension is fixed at 1980-2015"
        )

    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    rows = build_rows(args.start_year, args.end_year, args.erddap)
    frame = pd.DataFrame(rows).sort_values("year")
    expected = list(range(1980, 2016))
    if frame["year"].tolist() != expected:
        raise RuntimeError("cue extension did not return every registered year")
    if frame["ivory_coast_temp_c"].isna().any():
        raise RuntimeError("cue extension contains missing annual cue values")

    for column, expected_values in (
        ("grid_lat_min", {5.0}),
        ("grid_lat_max", {10.0}),
        ("grid_lon_min", {352.5}),
        ("grid_lon_max", {357.5}),
    ):
        observed = set(float(v) for v in frame[column].dropna().unique())
        if observed != expected_values:
            raise RuntimeError(
                f"registered grid changed in {column}: {sorted(observed)}"
            )

    prefix = validate_frozen_prefix(frame, baseline)
    if not prefix["passed"]:
        raise RuntimeError(
            "1980-2010 cue prefix failed frozen-value comparison: "
            + json.dumps(prefix, sort_keys=True)
        )

    args.annual_output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.annual_output, index=False, float_format="%.10g")

    transports = {
        str(key): int(value)
        for key, value in frame["transport"].value_counts().items()
    }
    receipt = {
        "result_id": "payoff_b_hoge_veluwe_cue_extension_20260927",
        "status": "SOURCE_FAITHFUL_CUE_EXTENSION_COMPLETE",
        "years": [1980, 2015],
        "n_years": int(len(frame)),
        "cue_window": "20 calendar days beginning 18 February",
        "grid_latitudes_deg_n": [10.0, 7.5, 5.0],
        "grid_longitudes_deg_e": [352.5, 355.0, 357.5],
        "implementation": (
            "imports the exact ERDDAP/PSL annual downloader from "
            "scripts/payoff_b_cv24c_cue_driver.py"
        ),
        "frozen_prefix_validation": prefix,
        "frozen_prefix_provenance": {
            "workflow_run_id": baseline["source_workflow_run_id"],
            "artifact_id": baseline["source_artifact_id"],
            "artifact_sha256": baseline["source_artifact_sha256"],
            "annual_csv_sha256": baseline["source_annual_csv_sha256"],
        },
        "annual_csv_sha256": sha256(args.annual_output),
        "transport_counts": transports,
        "outcome_firewall": {
            "resource_data_read": False,
            "resident_timing_read": False,
            "migrant_timing_read": False,
            "cue_resource_connectivity_computed": False,
            "information_reversal_gate_opened": False,
            "history_test_opened": False,
        },
    }
    args.receipt_output.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
