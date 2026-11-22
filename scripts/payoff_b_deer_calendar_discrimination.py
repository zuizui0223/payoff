#!/usr/bin/env python3
"""Source-authenticated mule-deer calendar-vs-phenophase test (exploratory).

Use only the same published repeated-deer sample as PR #413. A coefficient
conditional on raw calendar departure day is NOT a cue-use or causal result.
No original animal-year rows or identifiers leave this program.
"""
from __future__ import annotations

import argparse
from collections import Counter
from io import BytesIO
import hashlib
import json
from pathlib import Path
import random
import sys
import urllib.request
import zipfile

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from payoff_b_ortega_within_animal import (  # noqa: E402
    SOURCE_SHA256, PHASE_SHEET, _partial, _records, load_source,
    repeated_panel, resample_animals,
)
from payoff_b_ortega_source_data_probe import (  # noqa: E402
    shared_strings, workbook_sheet_paths,
)
from payoff_b_ortega_variance_funnel import parse_float, sheet_rows  # noqa: E402

DEFAULT_URL = (
    "https://media.springernature.com/original/springer-static/esm/"
    "art%3A10.1038%2Fs41467-023-37750-z/MediaObjects/"
    "41467_2023_37750_MOESM4_ESM.xlsx"
)
DEFAULT_CONTRACT = HERE.parent / "data/payoff_b_deer_calendar_discrimination_contract_20261122.json"


def get_original(path: Path | None, url: str) -> Path:
    """Retrieve at most 2 MiB and check the immutable original checksum."""
    if path is not None:
        raw = path.read_bytes()
    else:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; PAYOFF-source-replay/1)",
            "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*",
        })
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read(2_000_001)
    if len(raw) > 2_000_000:
        raise ValueError("Source exceeds 2 MiB source-size gate")
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("Source SHA256 does not equal authenticated original")
    if path is not None:
        return path
    from tempfile import NamedTemporaryFile
    tmp = NamedTemporaryFile(suffix=".xlsx", delete=False)
    tmp.write(raw)
    tmp.close()
    return Path(tmp.name)


def source_panel(source: Path) -> tuple[list[dict], dict]:
    rows, metadata = load_source(source)
    raw = source.read_bytes()
    with zipfile.ZipFile(BytesIO(raw)) as zf:
        sheets = dict(workbook_sheet_paths(zf))
        raw_phase = sheet_rows(
            zf, sheets[PHASE_SHEET], shared_strings(zf), max_cols=12
        )
    original = _records(raw_phase, 0, 12)
    calendar_by_id = {}
    for line in original:
        key = str(line.get("id_yr", "")).strip()
        if key in calendar_by_id:
            raise ValueError("Duplicate original phase identity")
        doy = parse_float(line.get("DOY_Start", ""))
        if not key or doy is None or not 1 <= doy <= 366:
            raise ValueError("Invalid original raw DOY_Start")
        calendar_by_id[key] = doy
    if len(calendar_by_id) != len(rows):
        raise ValueError("DOY rows do not match authenticated phase rows")
    for row in rows:
        key = f"{row['animal']}_{row['year']}"
        if key not in calendar_by_id:
            raise ValueError("Calendar/phase animal-year mismatch")
        row["calendar"] = calendar_by_id[key]
    panel = repeated_panel(rows)
    if (len(panel), len({r["animal"] for r in panel})) != (100, 38):
        raise ValueError("Parent 100-row/38-animal sample is not reproduced")
    meta = {
        "source_doi": metadata["doi"],
        "sha256": metadata["sha256"],
        "source_animal_years": metadata["phase_rows"],
        "original_stopover_complete": metadata["stopover_complete_rows"],
        "repeated_panel_rows": len(panel),
        "repeated_individuals": len({r["animal"] for r in panel}),
        "years": sorted({r["year"] for r in panel}),
        "genuine_zero_stopovers": sum(r["stopover"] == 0 for r in panel),
    }
    return panel, meta


def prefit_design(rows: list[dict], gate: dict) -> dict:
    """Inspect only two predictors and FE geometry: no outcome accessed."""
    n = len(rows)
    animals = len({r["animal"] for r in rows})
    years = len({r["year"] for r in rows})
    if not rows:
        return {"status": "NOT_ESTIMABLE_NO_ROWS"}
    x = np.array([[r["start"], r["calendar"]] for r in rows], dtype=float)
    v, rank, components = _partial(rows, x)
    phase, calendar = v.T
    calendar_ss = float(calendar @ calendar)
    phase_ss = float(phase @ phase)
    phase_after_calendar = phase - (
        calendar * (float(phase @ calendar) / calendar_ss)
        if calendar_ss > 1e-12 else np.zeros_like(phase)
    )
    conditional_ss = float(phase_after_calendar @ phase_after_calendar)
    vif = phase_ss / conditional_ss if conditional_ss > 1e-12 else float("inf")
    residual_df = n - rank - 2
    calendar_rms = float(np.sqrt(calendar_ss / n))
    phase_rms = float(np.sqrt(conditional_ss / n))
    checks = {
        "rows": n >= gate["min_rows"],
        "individuals": animals >= gate["min_repeated_individuals"],
        "years": years >= gate["min_years"],
        "residual_df": residual_df >= gate["min_residual_df"],
        "independent_calendar": calendar_rms >= gate["min_raw_calendar_after_FE_rms_days"],
        "independent_phase": phase_rms >= gate["min_DFP_after_FE_and_calendar_rms_days"],
        "collinearity": bool(np.isfinite(vif) and vif <= gate["max_DFP_calendar_partial_VIF"]),
    }
    return {
        "status": "PASS" if all(checks.values()) else "NOT_ESTIMABLE",
        "checks": checks,
        "n": n,
        "animals": animals,
        "years": years,
        "components": components,
        "nuisance_rank": rank,
        "residual_df": residual_df,
        "calendar_after_FE_rms_days": calendar_rms,
        "phase_after_FE_and_calendar_rms_days": phase_rms,
        "phase_calendar_partial_VIF": vif if np.isfinite(vif) else None,
        "phase_after_FE_rms_days": float(np.sqrt(phase_ss / n)),
    }


def fit_conditional(rows: list[dict]) -> dict:
    """Exact FWL calendar-adjusted phase slope; no threshold selection."""
    r, rank, _ = _partial(rows, [
        [s["start"], s["calendar"], s["stopover"]] for s in rows
    ])
    phase, calendar, stop = r.T
    c2 = float(calendar @ calendar)
    if c2 <= 1e-12:
        raise ValueError("No conditional calendar variation")
    phase_given_calendar = phase - calendar * (float(calendar @ phase) / c2)
    stop_given_calendar = stop - calendar * (float(calendar @ stop) / c2)
    x2 = float(phase_given_calendar @ phase_given_calendar)
    if x2 <= 1e-10:
        raise ValueError("No conditional phase variation")
    beta_phase = float(phase_given_calendar @ stop_given_calendar) / x2
    beta_calendar_null = float(calendar @ stop) / c2
    sse_calendar_only = float(stop_given_calendar @ stop_given_calendar)
    sse_joint = float(np.sum((stop_given_calendar - beta_phase * phase_given_calendar) ** 2))
    return {
        "beta_DFP_after_calendar": beta_phase,
        "beta_calendar_only_after_FE": beta_calendar_null,
        "calendar_only_residual_ss": sse_calendar_only,
        "calendar_plus_phase_residual_ss": sse_joint,
        "in_sample_partial_SSE_reduction_fraction": (
            (sse_calendar_only - sse_joint) / sse_calendar_only
            if sse_calendar_only > 1e-12 else None
        ),
        "nuisance_rank": rank,
        "residual_df": len(rows) - rank - 2,
    }


def analyze(rows: list[dict], contract: dict) -> dict:
    design = prefit_design(rows, contract["support_gates_before_primary_coefficient"])
    out = {
        "status": "NOT_ESTIMABLE",
        "design": design,
        "primary": None,
        "class": contract["status"],
        "source": contract["provenance"]["source_doi"],
        "no_causal_information_use_claim": True,
    }
    if design["status"] != "PASS":
        return out
    primary = fit_conditional(rows)
    requested = contract["uncertainty"]["replicates"]
    rng = random.Random(contract["uncertainty"]["seed"])
    betas = []
    for _ in range(requested):
        sample = resample_animals(rows, rng)
        try:
            betas.append(fit_conditional(sample)["beta_DFP_after_calendar"])
        except ValueError:
            continue
    valid_fraction = len(betas) / requested
    if len(betas):
        interval = np.quantile(betas, [0.025, 0.975]).tolist()
    else:
        interval = None
    primary["animal_cluster_bootstrap_CI95"] = interval
    primary["per_10_phase_day_effect"] = 10 * primary["beta_DFP_after_calendar"]
    primary["per_10_phase_day_CI95"] = (
        [10 * z for z in interval] if interval is not None else None
    )
    out["primary"] = primary
    out["bootstrap"] = {
        "unit": "individual", "requested": requested, "valid": len(betas),
        "valid_fraction": valid_fraction, "seed": contract["uncertainty"]["seed"],
        "conditional_on_observed_years": True,
    }
    if valid_fraction < contract["uncertainty"]["minimum_valid_fraction"]:
        out["status"] = "BOOTSTRAP_SUPPORT_FAIL"
    elif interval is not None and interval[1] < 0:
        out["status"] = "NEGATIVE_CALENDAR_CONDITIONAL_ASSOCIATION"
    else:
        out["status"] = "NO_SUPPORTED_NEGATIVE_CALENDAR_CONDITIONAL_ASSOCIATION"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path)
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    ap.add_argument("--support-only", action="store_true")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    contract_bytes = args.contract.read_bytes()
    contract = json.loads(contract_bytes)
    path = get_original(args.source, args.url)
    try:
        rows, metadata = source_panel(path)
    finally:
        if args.source is None:
            path.unlink(missing_ok=True)
    if args.support_only:
        outcome = {
            "status": "SOURCE_ONLY_SUPPORT",
            "design": prefit_design(rows, contract["support_gates_before_primary_coefficient"]),
            "primary": None,
        }
    else:
        outcome = analyze(rows, contract)
    outcome.update(date="2026-11-22", source_metadata=metadata,
                   contract_sha256=hashlib.sha256(contract_bytes).hexdigest(),
                   claim_ceiling="Exploratory within-animal association; not observed cue use or causation.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(outcome, indent=2, allow_nan=False) + "\n")
    print("PAYOFF_DEER_CALENDAR_RESULT_JSON=" + json.dumps(outcome, separators=(",", ":")))


if __name__ == "__main__":
    main()
