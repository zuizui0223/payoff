#!/usr/bin/env python3
"""Run the preregistered Hoge Veluwe environmental-information reversal Gate B.

Gate B opens only the certified precommitment cue and caterpillar-resource
coordinates. It does not read pied-flycatcher timing, great-tit timing, compute
resident-migrant mismatch, or run the history model.

Licensed outcomes:
- NO_CUE_RESOURCE_REVERSAL
- UNSTABLE_CUE_RESOURCE_REVERSAL
- INFORMATION_REVERSAL_STABLE

Gate C remains closed unless Gate B is stable *and* the separately registered
history-source gate is complete.
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from src.predictive_connectivity import detrended_predictive_connectivity
from payoff_b_hoge_veluwe_source_gate import (
    _dryad_download_file,
    _session,
    sha256_path,
)


@dataclass(frozen=True)
class LineFit:
    intercept: float
    slope: float
    sse: float
    n: int
    k: int
    aicc: float


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--contract",
        type=Path,
        default=ROOT
        / "data"
        / "payoff_b_hoge_veluwe_network_hysteresis_contract_20260927.json",
    )
    p.add_argument(
        "--source-gate-result",
        type=Path,
        default=ROOT
        / "data"
        / "payoff_b_hoge_veluwe_source_gate_a_result_20260928.json",
    )
    p.add_argument("--cue-csv", type=Path, required=True)
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/hoge_veluwe_gate_b"),
    )
    p.add_argument("--timeout", type=int, default=120)
    return p.parse_args()


def _aicc(sse: float, n: int, k: int) -> float:
    if n <= k + 1:
        return float("inf")
    sse = max(float(sse), 1e-15)
    aic = n * math.log(sse / n) + 2.0 * k
    return aic + (2.0 * k * (k + 1)) / (n - k - 1)


def _line_fit(x, y, *, k: int = 2) -> LineFit:
    import numpy as np

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 3:
        raise ValueError("line fit requires at least three rows")
    X = np.column_stack([np.ones(len(x)), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    residual = y - X @ coef
    sse = float(np.sum(residual**2))
    return LineFit(
        intercept=float(coef[0]),
        slope=float(coef[1]),
        sse=sse,
        n=int(len(x)),
        k=int(k),
        aicc=_aicc(sse, len(x), k),
    )


def _candidate_segmented_fit(x, y, split_index: int) -> dict:
    import numpy as np

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    left = _line_fit(x[:split_index], y[:split_index])
    right = _line_fit(x[split_index:], y[split_index:])
    sse = left.sse + right.sse
    n = len(x)
    return {
        "left": left,
        "right": right,
        "sse": float(sse),
        "aicc": _aicc(sse, n, 5),
        "split_index": int(split_index),
        "break_year": int(x[split_index]),
        "left_final_year": int(x[split_index - 1]),
    }


def _best_segmented_fit(x, y, min_segment_years: int) -> dict:
    candidates = [
        _candidate_segmented_fit(x, y, split)
        for split in range(
            min_segment_years,
            len(x) - min_segment_years + 1,
        )
    ]
    if not candidates:
        raise ValueError("no licensed segmented breakpoint candidates")
    best_aicc = min(row["aicc"] for row in candidates)
    tied = [
        row
        for row in candidates
        if abs(row["aicc"] - best_aicc) <= 1e-12
    ]
    return min(tied, key=lambda row: row["break_year"])


def _recovery_diagnostics(x, segmented: dict) -> dict:
    left = segmented["left"]
    right = segmented["right"]
    start_year = float(x[0])
    low_year = float(segmented["left_final_year"])
    final_year = float(x[-1])

    predicted_start = left.intercept + left.slope * start_year
    predicted_low = left.intercept + left.slope * low_year
    predicted_final = right.intercept + right.slope * final_year

    decline = predicted_start - predicted_low
    recovery = predicted_final - predicted_low
    fraction = (
        recovery / decline
        if decline > 0.0 and math.isfinite(decline)
        else float("nan")
    )
    return {
        "predicted_start_connectivity": float(predicted_start),
        "predicted_break_low_connectivity": float(predicted_low),
        "predicted_final_connectivity": float(predicted_final),
        "decline": float(decline),
        "recovery": float(recovery),
        "recovery_fraction": float(fraction),
    }


def _fit_reversal_geometry(
    years,
    rho,
    *,
    min_segment_years: int,
) -> dict:
    import numpy as np

    x = np.asarray(years, dtype=float)
    y = np.asarray(rho, dtype=float)
    if len(x) < 2 * min_segment_years:
        return {
            "estimable": False,
            "reason": "too few connectivity years for two licensed segments",
        }

    linear = _line_fit(x, y, k=2)
    segmented = _best_segmented_fit(
        x,
        y,
        min_segment_years,
    )
    recovery = _recovery_diagnostics(x, segmented)
    delta_aicc = linear.aicc - segmented["aicc"]

    geometry_pass = (
        delta_aicc >= 4.0
        and segmented["left"].slope < 0.0
        and segmented["right"].slope > 0.0
        and math.isfinite(recovery["recovery_fraction"])
        and recovery["recovery_fraction"] >= 0.50
    )
    return {
        "estimable": True,
        "geometry_pass": bool(geometry_pass),
        "linear": {
            "intercept": linear.intercept,
            "slope": linear.slope,
            "sse": linear.sse,
            "aicc": linear.aicc,
            "k": 2,
        },
        "segmented": {
            "break_year": segmented["break_year"],
            "left_final_year": segmented["left_final_year"],
            "left_intercept": segmented["left"].intercept,
            "left_slope": segmented["left"].slope,
            "right_intercept": segmented["right"].intercept,
            "right_slope": segmented["right"].slope,
            "sse": segmented["sse"],
            "aicc": segmented["aicc"],
            "k": 5,
            "delta_aicc_vs_linear": float(delta_aicc),
            **recovery,
        },
    }


def _leave_one_year_out_stability(
    years,
    rho,
    *,
    full_break_year: int,
    min_segment_years: int,
    slope_fraction_threshold: float,
    break_fraction_threshold: float,
    break_tolerance_years: int,
) -> dict:
    rows = []
    years = list(int(v) for v in years)
    rho = list(float(v) for v in rho)

    for omitted_index, omitted_year in enumerate(years):
        x = years[:omitted_index] + years[omitted_index + 1 :]
        y = rho[:omitted_index] + rho[omitted_index + 1 :]
        try:
            fit = _fit_reversal_geometry(
                x,
                y,
                min_segment_years=min_segment_years,
            )
        except Exception as exc:
            rows.append(
                {
                    "omitted_year": omitted_year,
                    "estimable": False,
                    "error": f"{type(exc).__name__}: {exc}",
                    "slope_signs_preserved": False,
                    "breakpoint_within_tolerance": False,
                }
            )
            continue

        if not fit.get("estimable"):
            rows.append(
                {
                    "omitted_year": omitted_year,
                    "estimable": False,
                    "reason": fit.get("reason"),
                    "slope_signs_preserved": False,
                    "breakpoint_within_tolerance": False,
                }
            )
            continue

        seg = fit["segmented"]
        slope_ok = (
            seg["left_slope"] < 0.0
            and seg["right_slope"] > 0.0
        )
        break_ok = (
            abs(int(seg["break_year"]) - int(full_break_year))
            <= int(break_tolerance_years)
        )
        rows.append(
            {
                "omitted_year": omitted_year,
                "estimable": True,
                "break_year": int(seg["break_year"]),
                "left_slope": float(seg["left_slope"]),
                "right_slope": float(seg["right_slope"]),
                "delta_aicc_vs_linear": float(seg["delta_aicc_vs_linear"]),
                "recovery_fraction": float(seg["recovery_fraction"]),
                "slope_signs_preserved": bool(slope_ok),
                "breakpoint_within_tolerance": bool(break_ok),
            }
        )

    denominator = len(rows)
    slope_fraction = (
        sum(row["slope_signs_preserved"] for row in rows) / denominator
        if denominator
        else 0.0
    )
    break_fraction = (
        sum(row["breakpoint_within_tolerance"] for row in rows) / denominator
        if denominator
        else 0.0
    )
    passes = (
        slope_fraction >= slope_fraction_threshold
        and break_fraction >= break_fraction_threshold
    )
    return {
        "passes": bool(passes),
        "denominator": denominator,
        "slope_sign_fraction": float(slope_fraction),
        "breakpoint_within_tolerance_fraction": float(break_fraction),
        "required_slope_sign_fraction": float(slope_fraction_threshold),
        "required_breakpoint_fraction": float(break_fraction_threshold),
        "breakpoint_tolerance_years": int(break_tolerance_years),
        "rows": rows,
    }


def _read_cue(path: Path, *, expected_sha256: str):
    import pandas as pd

    digest = sha256_path(path)
    if digest != expected_sha256:
        raise ValueError(
            "cue CSV SHA256 does not match the frozen Gate-A receipt: "
            f"{digest} != {expected_sha256}"
        )
    frame = pd.read_csv(path)
    required = {"year", "ivory_coast_temp_c"}
    if not required.issubset(frame.columns):
        raise ValueError(
            f"cue CSV missing required columns: {sorted(required - set(frame.columns))}"
        )
    frame = frame[["year", "ivory_coast_temp_c"]].copy()
    frame["year"] = pd.to_numeric(frame["year"], errors="raise").astype(int)
    frame["ivory_coast_temp_c"] = pd.to_numeric(
        frame["ivory_coast_temp_c"],
        errors="raise",
    )
    if frame["year"].duplicated().any():
        raise ValueError("cue CSV contains duplicate years")
    if frame["year"].min() != 1980 or frame["year"].max() != 2015:
        raise ValueError("cue CSV must cover exactly the frozen 1980-2015 span")
    return frame, digest


def _read_resource(path: Path):
    import pandas as pd

    frame = pd.read_excel(path)
    required = {"Year", "MidDate"}
    if not required.issubset(frame.columns):
        raise ValueError(
            f"resource file missing required columns: {sorted(required - set(frame.columns))}"
        )
    frame = frame[["Year", "MidDate"]].copy()
    frame["year"] = pd.to_numeric(frame["Year"], errors="raise").astype(int)
    frame["resource_peak_april_day"] = pd.to_numeric(
        frame["MidDate"],
        errors="raise",
    )
    frame = frame[["year", "resource_peak_april_day"]]
    if frame["year"].duplicated().any():
        raise ValueError("resource source contains duplicate years")
    if frame["year"].min() != 1985 or frame["year"].max() != 2020:
        raise ValueError("resource source must retain the certified 1985-2020 span")
    if 1991 in set(frame["year"]):
        raise ValueError("registered missing resource year 1991 unexpectedly present")
    expected = set(range(1985, 2021)) - {1991}
    if set(frame["year"]) != expected:
        missing = sorted(expected - set(frame["year"]))
        extra = sorted(set(frame["year"]) - expected)
        raise ValueError(
            f"resource year set differs from registered source; missing={missing} extra={extra}"
        )
    if not frame["resource_peak_april_day"].between(-50, 150).all():
        raise ValueError(
            "MidDate values fall outside a conservative April-day plausibility range"
        )
    return frame


def _build_connectivity(
    cue,
    resource,
    *,
    target_start: int,
    target_end: int,
    window_years: int,
    min_pairs: int,
):
    import pandas as pd

    annual = cue.merge(resource, on="year", how="inner")
    rows = []
    for target_year in range(target_start, target_end + 1):
        history = annual[
            (annual["year"] >= target_year - window_years)
            & (annual["year"] < target_year)
        ].copy()
        if len(history) < min_pairs:
            raise ValueError(
                f"target year {target_year} has only {len(history)} paired years"
            )
        est = detrended_predictive_connectivity(
            history["year"].tolist(),
            history["ivory_coast_temp_c"].tolist(),
            history["resource_peak_april_day"].tolist(),
            min_pairs=min_pairs,
        )
        rows.append(
            {
                "target_year": target_year,
                "training_n": int(est.n_pairs),
                "connectivity_rho": float(est.rho),
                "connectivity_r2": float(est.r_squared),
                "gaussian_binary_agreement": float(
                    est.gaussian_binary_agreement
                ),
            }
        )
    return annual, pd.DataFrame(rows)


def _registered_stability_settings(contract: dict) -> dict:
    gate = contract["information_reversal_gate"]
    stability = gate["leave_one_history_year_out_stability_gate"]
    bp = stability["minimum_fraction_breakpoint_within_years_of_full_fit"]
    return {
        "min_segment_years": int(gate["min_segment_years"]),
        "slope_fraction_threshold": float(
            stability["minimum_fraction_preserving_both_slope_signs"]
        ),
        "break_fraction_threshold": float(bp["fraction"]),
        "break_tolerance_years": int(bp["tolerance_years"]),
    }


def _gate_result(connectivity, contract: dict) -> dict:
    years = connectivity["target_year"].astype(int).tolist()
    rho = connectivity["connectivity_rho"].astype(float).tolist()
    settings = _registered_stability_settings(contract)

    full = _fit_reversal_geometry(
        years,
        rho,
        min_segment_years=settings["min_segment_years"],
    )
    if not full.get("estimable"):
        return {
            "status": "NO_CUE_RESOURCE_REVERSAL",
            "gate_b_passed": False,
            "reason": full.get("reason", "not estimable"),
            "full_fit": full,
            "stability": None,
        }

    if not full["geometry_pass"]:
        return {
            "status": "NO_CUE_RESOURCE_REVERSAL",
            "gate_b_passed": False,
            "full_fit": full,
            "stability": None,
        }

    stability = _leave_one_year_out_stability(
        years,
        rho,
        full_break_year=full["segmented"]["break_year"],
        min_segment_years=settings["min_segment_years"],
        slope_fraction_threshold=settings["slope_fraction_threshold"],
        break_fraction_threshold=settings["break_fraction_threshold"],
        break_tolerance_years=settings["break_tolerance_years"],
    )
    if not stability["passes"]:
        return {
            "status": "UNSTABLE_CUE_RESOURCE_REVERSAL",
            "gate_b_passed": False,
            "full_fit": full,
            "stability": stability,
        }

    return {
        "status": "INFORMATION_REVERSAL_STABLE",
        "gate_b_passed": True,
        "full_fit": full,
        "stability": stability,
    }


def main():
    args = parse_args()
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    gate_a = json.loads(args.source_gate_result.read_text(encoding="utf-8"))

    if gate_a.get("gate_b_licensed") is not True:
        raise RuntimeError("Gate B is not licensed by frozen Gate-A adjudication")
    if gate_a.get("outcome_firewall", {}).get("cue_resource_connectivity_computed"):
        raise RuntimeError("Gate-A receipt unexpectedly indicates Gate B was already opened")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    source_dir = args.output_dir / "source"
    if source_dir.exists():
        shutil.rmtree(source_dir)
    source_dir.mkdir(parents=True)

    cue, cue_digest = _read_cue(
        args.cue_csv,
        expected_sha256=gate_a["cue_extension"]["annual_csv_sha256"],
    )

    resource_contract = contract["sources"]["destination_resource_state"]
    session = _session()
    resource_meta = _dryad_download_file(
        session,
        resource_contract["dataset_doi"],
        resource_contract["file"],
        source_dir,
        args.timeout,
    )
    frozen_resource_sha = gate_a[
        "certified_sources"
    ]["destination_resource_state"]["computed_sha256"]
    if resource_meta["sha256"] != frozen_resource_sha:
        raise RuntimeError(
            "resource file no longer matches frozen Gate-A SHA256: "
            f"{resource_meta['sha256']} != {frozen_resource_sha}"
        )
    resource = _read_resource(Path(resource_meta["path"]))

    overlap_start, overlap_end = contract["population"]["primary_overlap_years"]
    annual = cue.merge(resource, on="year", how="inner")
    annual = annual[
        (annual["year"] >= overlap_start)
        & (annual["year"] <= overlap_end)
    ].copy()

    expected_pair_years = list(range(overlap_start, overlap_end + 1))
    expected_pair_years.remove(1991)
    if annual["year"].tolist() != expected_pair_years:
        raise RuntimeError(
            "paired cue-resource years differ from the registered source overlap"
        )

    history_start, history_end = contract["population"][
        "primary_history_years_after_connectivity_construction"
    ]
    coord = contract["coordinates"]["cue_resource_predictive_connectivity"]
    _, connectivity = _build_connectivity(
        cue,
        resource,
        target_start=history_start,
        target_end=history_end,
        window_years=int(coord["window_years"]),
        min_pairs=int(coord["min_pairs"]),
    )
    if len(connectivity) != contract["population"]["expected_primary_history_year_count"]:
        raise RuntimeError("connectivity history length differs from frozen 24-year span")

    gate = _gate_result(connectivity, contract)

    annual_path = args.output_dir / "gate_b_cue_resource_annual.csv"
    connectivity_path = args.output_dir / "gate_b_connectivity.csv"
    annual.to_csv(annual_path, index=False)
    connectivity.to_csv(connectivity_path, index=False)

    result = {
        "result_id": "payoff_b_hoge_veluwe_gate_b_20260928",
        "contract_id": contract["contract_id"],
        "gate_a_result": gate_a["result_id"],
        "status": gate["status"],
        "gate_b_passed": gate["gate_b_passed"],
        "gate_c_licensed": False,
        "gate_c_license_reason": (
            "history source gate remains blocked on the exact migrant archive"
            if gate["gate_b_passed"]
            else "Gate B did not pass"
        ),
        "registered_source_overlap": [overlap_start, overlap_end],
        "registered_history_span": [history_start, history_end],
        "source_provenance": {
            "cue_csv_sha256": cue_digest,
            "resource_file_sha256": resource_meta["sha256"],
            "resource_transport": resource_meta["download_transport"],
            "resource_dryad_doi": resource_contract["dataset_doi"],
            "resource_filename": resource_contract["file"],
            "resource_units": resource_contract["source_units"],
        },
        "annual_pair_rows": int(len(annual)),
        "connectivity_rows": int(len(connectivity)),
        "window_years": int(coord["window_years"]),
        "min_pairs": int(coord["min_pairs"]),
        "gate": gate,
        "output_hashes": {
            "annual_pairs_sha256": sha256_path(annual_path),
            "connectivity_sha256": sha256_path(connectivity_path),
        },
        "outcome_firewall": {
            "cue_data_read": True,
            "resource_data_read": True,
            "resident_timing_read": False,
            "migrant_timing_read": False,
            "focal_partner_mismatch_computed": False,
            "history_test_opened": False,
        },
        "claim_boundary": [
            "Gate B tests only environmental cue-resource reversal geometry",
            "Gate B does not test resident-migrant history or the Nash mechanism",
            "Gate C stays closed unless Gate B passes and the history-source gate is complete",
            "no natural hysteresis or rescue-seed claim is licensed by Gate B alone",
        ],
    }

    result_path = args.output_dir / "gate_b_result.json"
    result_path.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    shutil.rmtree(source_dir, ignore_errors=True)

    print(
        "PAYOFF_B_HV_GATE_B "
        f"status={result['status']} "
        f"rows={result['connectivity_rows']} "
        f"gate_b_passed={result['gate_b_passed']}"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
