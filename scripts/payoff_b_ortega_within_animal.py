#!/usr/bin/env python3
"""One post-publication within-animal stopover comparison; aggregate output only.

The original authors already analyzed compensation with animal/year random
intercepts. This conditional fixed-effect reanalysis identifies neither cue use
nor a causal controller. It never predicts arrival using whole-journey speed.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
from io import BytesIO
import json
from pathlib import Path
import random
import sys
import zipfile

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from payoff_b_ortega_source_data_probe import shared_strings, workbook_sheet_paths
from payoff_b_ortega_variance_funnel import parse_float, sheet_rows

SOURCE_SHA256 = "2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364"
PHASE_SHEET = "Fig1a,b;Fig3;SFig2;STables1,6"
ACTUATOR_SHEET = "Fig4d,4e;SFig4"
DEFAULT_CONTRACT = SCRIPT_DIR.parent / "data/payoff_b_ortega_within_animal_contract_v2_20261122.json"


def _unique(records, label):
    indexed = {}
    for row in records:
        key = str(row.get("id_yr", "")).strip()
        if not key:
            raise ValueError(f"missing {label} join key")
        if key in indexed:
            raise ValueError(f"duplicate {label} join key")
        indexed[key] = row
    return indexed


def join_records(phase, actuators):
    """Validate original one-to-one identities without exporting their values."""
    pmap, amap = _unique(phase, "phase"), _unique(actuators, "actuator")
    if set(pmap) != set(amap):
        raise ValueError("original phase and actuator keys do not match")
    joined = []
    for key, p in pmap.items():
        try:
            animal, suffix = key.rsplit("_", 1)
            year_value = float(p["year"])
            year = int(year_value)
            if not animal or year != year_value or int(suffix) != year:
                raise ValueError
        except (KeyError, ValueError, TypeError):
            raise ValueError("original animal-year identity is invalid") from None
        start = parse_float(p.get("DFP_Start", ""))
        if start is None:
            raise ValueError("original start phase is missing or nonfinite")
        stopover = parse_float(amap[key].get("stopover.day", ""))
        if stopover is not None and stopover < 0:
            raise ValueError("negative original stopover duration")
        joined.append({"animal": animal, "year": year, "start": start,
                       "stopover": stopover, "timing": p.get("timing", "")})
    return joined


def _records(matrix, header_row, width):
    headers = [str(x).strip() for x in matrix[header_row][:width]]
    if "id_yr" not in headers:
        raise ValueError("source table header does not contain id_yr")
    records = []
    for raw in matrix[header_row + 1:]:
        row = {h: raw[i] if i < len(raw) else "" for i, h in enumerate(headers) if h}
        if str(row.get("id_yr", "")).strip():
            records.append(row)
    return records


def load_source(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(10 * 1024 * 1024 + 1)
    sha = hashlib.sha256(raw).hexdigest()
    if sha != SOURCE_SHA256:
        raise ValueError("source SHA256 does not match authenticated original")
    with zipfile.ZipFile(BytesIO(raw)) as zf:
        strings = shared_strings(zf)
        sheets = dict(workbook_sheet_paths(zf))
        phase = sheet_rows(zf, sheets[PHASE_SHEET], strings, max_cols=12)
        actuator = sheet_rows(zf, sheets[ACTUATOR_SHEET], strings, max_cols=7)
    rows = join_records(_records(phase, 0, 12), _records(actuator, 1, 7))
    complete = [r for r in rows if r["stopover"] is not None]
    observed = (len(rows), len({r["animal"] for r in rows}), len(complete),
                len({r["animal"] for r in complete}),
                sum(r["stopover"] == 0 for r in complete))
    if observed != (152, 72, 127, 65, 15):
        raise ValueError(f"authenticated source count check failed: {observed}")
    timing_means = {}
    for label in ("early", "mid", "late"):
        values = [r["start"] for r in rows if str(r["timing"]).lower() == label]
        if values:
            timing_means[label] = float(np.mean(values))
    if set(timing_means) != {"early", "mid", "late"} or not (
        timing_means["early"] < 0 < timing_means["late"]
        and timing_means["early"] < timing_means["mid"] < timing_means["late"]
    ):
        raise ValueError("source phase sign/timing classification check failed")
    meta = {"doi": "10.1038/s41467-023-37750-z", "sha256": sha,
            "bytes": len(raw), "phase_rows": observed[0], "animals": observed[1],
            "stopover_complete_rows": observed[2], "stopover_complete_animals": observed[3],
            "genuine_zero_stopovers": observed[4], "missing_stopover_rows": 25,
            "start_phase_by_published_timing_class": timing_means,
            "positive_phase_means_later": True}
    return rows, meta


def repeated_panel(rows):
    complete = [r for r in rows if r.get("stopover") is not None]
    years = defaultdict(set)
    for row in complete:
        years[row["animal"]].add(row["year"])
    return [r for r in complete if len(years[r["animal"]]) >= 2]


def _demean(values, groups):
    values = np.asarray(values, dtype=float)
    if values.ndim == 1:
        values = values[:, None]
    _, inverse = np.unique(groups, return_inverse=True)
    counts = np.bincount(inverse)
    totals = np.zeros((len(counts), values.shape[1]))
    np.add.at(totals, inverse, values)
    return values - (totals / counts[:, None])[inverse]


def _partial(rows, values):
    """Exact projection: remove animal effects, then residualized year effects."""
    animals = np.array([r["animal"] for r in rows])
    years = np.array([r["year"] for r in rows])
    unique_years, yi = np.unique(years, return_inverse=True)
    year_dummies = np.eye(len(unique_years))[yi]
    z = _demean(year_dummies, animals)
    centered = _demean(values, animals)
    year_coef, _, year_rank, _ = np.linalg.lstsq(z, centered, rcond=None)
    residuals = centered - z @ year_coef
    nuisance_rank = len(set(animals)) + int(year_rank)
    return residuals, nuisance_rank, int(len(unique_years) - year_rank)


def design_summary(rows):
    if not rows:
        return {"n": 0, "animals": 0, "years": [], "residual_df": 0,
                "residual_exposure_rms_days": 0.0, "connected_components": 0}
    residuals, rank, components = _partial(rows, [r["start"] for r in rows])
    return {"n": len(rows), "animals": len({r["animal"] for r in rows}),
            "years": sorted({r["year"] for r in rows}),
            "year_counts": dict(sorted(Counter(r["year"] for r in rows).items())),
            "animal_observation_count_distribution": dict(sorted(Counter(
                Counter(r["animal"] for r in rows).values()).items())),
            "genuine_zero_stopovers": sum(r["stopover"] == 0 for r in rows),
            "nuisance_rank": rank, "full_model_rank": rank + 1,
            "residual_df": len(rows) - rank - 1,
            "residual_exposure_rms_days": float(np.sqrt(np.mean(residuals[:, 0] ** 2))),
            "connected_components": components}


def support_summary(rows, contract):
    complete = [r for r in rows if r["stopover"] is not None]
    panel = repeated_panel(rows)
    summary = design_summary(panel)
    limits = contract["support_before_coefficient"]
    checks = {
        "repeated_animals": summary["animals"] >= limits["minimum_repeated_animals"],
        "years": len(summary["years"]) >= limits["minimum_years"],
        "residual_df": summary["residual_df"] >= limits["minimum_residual_degrees_of_freedom"],
        "residual_phase_variation": summary["residual_exposure_rms_days"] >= limits["minimum_residual_exposure_rms_days"],
        "component_policy": (not limits["require_one_connected_animal_year_component"]
                             or summary["connected_components"] == 1),
    }
    return {"status": "PASS" if all(checks.values()) else "SUPPORT_NOT_MET",
            "checks": checks, "primary_panel": summary,
            "complete_case_rows": len(complete),
            "singleton_rows_excluded_from_primary": len(complete) - len(panel),
            "new_coefficient_computed": False}


def fit_twfe(rows):
    if not rows:
        raise ValueError("no identifying observations")
    xy = np.array([[r["start"], r["stopover"]] for r in rows], dtype=float)
    if not np.isfinite(xy).all():
        raise ValueError("nonfinite regression input")
    residuals, rank, _ = _partial(rows, xy)
    x, y = residuals.T
    xx = float(x @ x)
    if xx <= 1e-20 * max(float(xy[:, 0] @ xy[:, 0]), 1.0):
        raise ValueError("no identifying phase variation after fixed effects")
    if len(rows) - rank - 1 <= 0:
        raise ValueError("no residual degrees of freedom")
    beta = float(x @ y / xx)
    return {"beta": beta, "n": len(rows), "nuisance_rank": rank,
            "residual_df": len(rows) - rank - 1,
            "residual_exposure_rms_days": float(np.sqrt(xx / len(rows))),
            "residual_sum_squares": float(np.sum((y - beta * x) ** 2))}


def _reference_slopes(rows):
    xy = np.array([[r["start"], r["stopover"]] for r in rows], dtype=float)
    pooled = xy - xy.mean(axis=0)
    within_year = _demean(xy, [r["year"] for r in rows])
    return {"pooled": float(pooled[:, 0] @ pooled[:, 1] / (pooled[:, 0] @ pooled[:, 0])),
            "year_fixed_effects": float(within_year[:, 0] @ within_year[:, 1] /
                                        (within_year[:, 0] @ within_year[:, 0]))}


def resample_animals(rows, rng):
    histories = defaultdict(list)
    for row in rows:
        histories[row["animal"]].append(row)
    animals = sorted(histories)
    sample = []
    for draw in range(len(animals)):
        animal = rng.choice(animals)
        sample.extend({**r, "animal": f"draw_{draw}"} for r in histories[animal])
    return sample


def analyze(rows, contract):
    support = support_summary(rows, contract)
    if support["status"] != "PASS":
        return {"status": "SUPPORT_NOT_MET", "support": support, "primary": None}
    panel = repeated_panel(rows)
    primary = fit_twfe(panel)
    references = _reference_slopes(panel)
    uncertainty = contract["uncertainty"]
    rng = random.Random(uncertainty["seed"])
    boot = []
    for _ in range(uncertainty["replicates"]):
        try:
            boot.append(fit_twfe(resample_animals(panel, rng))["beta"])
        except ValueError:
            continue
    valid_fraction = len(boot) / uncertainty["replicates"]
    interval = np.quantile(boot, [0.025, 0.975]).tolist() if boot else None
    primary["ci95_animal_bootstrap"] = interval
    primary["effect_per_10_phase_days"] = 10 * primary["beta"]
    primary["ci95_per_10_phase_days"] = [10 * x for x in interval] if interval else None
    omissions = []
    for year in sorted({r["year"] for r in panel}):
        omitted = repeated_panel([r for r in panel if r["year"] != year])
        item = {"omitted_year": year, "design": design_summary(omitted)}
        try:
            item.update(status="ESTIMABLE", beta=fit_twfe(omitted)["beta"])
        except ValueError as exc:
            item.update(status="NOT_ESTIMABLE", reason=str(exc))
        omissions.append(item)
    bootstrap_ok = valid_fraction >= uncertainty["minimum_valid_fraction"]
    status = "NEGATIVE_WITHIN_ANIMAL_ASSOCIATION_SUPPORTED" if (
        bootstrap_ok and interval is not None and interval[1] < 0
    ) else "NEGATIVE_WITHIN_ANIMAL_ASSOCIATION_NOT_SUPPORTED"
    if not bootstrap_ok:
        status = "BOOTSTRAP_SUPPORT_FAILED"
    return {"status": status, "support": support, "primary": primary,
            "same_panel_reference_slopes": references,
            "bootstrap": {"unit": "animal", "replicates_requested": uncertainty["replicates"],
                          "replicates_completed": len(boot), "valid_fraction": valid_fraction,
                          "seed": uncertainty["seed"], "scope": uncertainty["scope"]},
            "year_omission_sensitivity": omissions}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--support-only", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    contract_bytes = args.contract.read_bytes()
    contract = json.loads(contract_bytes)
    rows, source = load_source(args.source)
    result = support_summary(rows, contract) if args.support_only else analyze(rows, contract)
    result.update(date=contract["date"], source=source,
                  contract_sha256=hashlib.sha256(contract_bytes).hexdigest(),
                  contract_file=args.contract.name,
                  design_version=contract.get("design_version", 1),
                  design_amendment=contract.get("amendment"),
                  analysis_class=contract["status"], prior_art=contract["prior_art"],
                  claim_limit=contract["claim_limit"], frozen_manuscripts_changed=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
