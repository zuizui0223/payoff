#!/usr/bin/env python3
"""Post-freeze descriptive Ortega et al. 2023 phase-variance audit.

This analysis is frozen by
data/payoff_b_ortega_variance_funnel_contract_20261003.json.

It reproduces the public animal-year start/end phase funnel from the Nature
Communications Source Data file and connects it descriptively to movement-rate
and stopover actuators.  It is not a test of the latent PAYOFF-B K/g/phi
controller and does not alter the frozen GEB V2 submission.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
import urllib.request
import zipfile
from collections import defaultdict
from io import BytesIO
from pathlib import Path

from payoff_b_ortega_source_data_probe import (
    DEFAULT_URL,
    cell_value,
    col_index,
    shared_strings,
    workbook_sheet_paths,
    NS,
)
from xml.etree import ElementTree as ET


EXPECTED_SHA256 = "2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364"
PHASE_SHEET = "Fig1a,b;Fig3;SFig2;STables1,6"
ACTUATOR_SHEET = "Fig4d,4e;SFig4"


def download(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "Chrome/130 Safari/537.36"
            ),
            "Accept": (
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet,application/octet-stream,*/*"
            ),
        },
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()


def sheet_rows(
    zf: zipfile.ZipFile,
    path: str,
    strings: list[str],
    *,
    max_cols: int = 100,
) -> list[list[str]]:
    root = ET.fromstring(zf.read(path))
    out: list[list[str]] = []
    for row in root.findall("main:sheetData/main:row", NS):
        vals: dict[int, str] = {}
        for cell in row.findall("main:c", NS):
            idx = col_index(cell.attrib.get("r", ""))
            if idx >= max_cols:
                continue
            val = cell_value(cell, strings)
            vals[idx] = val
        if not vals:
            out.append([])
            continue
        width = min(max(vals) + 1, max_cols)
        arr = [""] * width
        for idx, val in vals.items():
            if idx < width:
                arr[idx] = val
        out.append(arr)
    return out


def parse_float(value: str) -> float | None:
    value = str(value).strip()
    if value == "" or value.upper() in {"NA", "NAN", "NULL"}:
        return None
    try:
        x = float(value)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def sample_var(xs: list[float]) -> float:
    if len(xs) < 2:
        raise ValueError("sample variance requires at least two observations")
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def sample_cov(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("covariance requires equal vectors of length >=2")
    mx, my = mean(xs), mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)


def ols_slope(xs: list[float], ys: list[float]) -> float:
    return sample_cov(xs, ys) / sample_var(xs)


def pearson(xs: list[float], ys: list[float]) -> float:
    return sample_cov(xs, ys) / math.sqrt(sample_var(xs) * sample_var(ys))


def percentile(xs: list[float], p: float) -> float:
    ys = sorted(xs)
    if not ys:
        raise ValueError("empty percentile input")
    if len(ys) == 1:
        return ys[0]
    pos = (len(ys) - 1) * p
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return ys[lo]
    frac = pos - lo
    return ys[lo] * (1.0 - frac) + ys[hi] * frac


def ci95(xs: list[float]) -> list[float]:
    return [percentile(xs, 0.025), percentile(xs, 0.975)]


def year_center(rows: list[dict], field: str) -> list[float]:
    groups: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        groups[row["year"]].append(row[field])
    means = {year: mean(vals) for year, vals in groups.items()}
    return [row[field] - means[row["year"]] for row in rows]


def metrics(rows: list[dict]) -> dict:
    starts = [row["start"] for row in rows]
    ends = [row["end"] for row in rows]
    start_var = sample_var(starts)
    end_var = sample_var(ends)
    start_y = year_center(rows, "start")
    end_y = year_center(rows, "end")
    y_start_var = sample_var(start_y)
    y_end_var = sample_var(end_y)
    closer = sum(abs(e) < abs(s) for s, e in zip(starts, ends))
    equal = sum(abs(e) == abs(s) for s, e in zip(starts, ends))
    return {
        "n": len(rows),
        "start_mean": mean(starts),
        "end_mean": mean(ends),
        "start_sd": math.sqrt(start_var),
        "end_sd": math.sqrt(end_var),
        "start_variance": start_var,
        "end_variance": end_var,
        "variance_ratio_end_over_start": end_var / start_var,
        "sd_ratio_end_over_start": math.sqrt(end_var / start_var),
        "start_min": min(starts),
        "start_max": max(starts),
        "end_min": min(ends),
        "end_max": max(ends),
        "whole_route_lambda": ols_slope(starts, ends),
        "whole_route_r": pearson(starts, ends),
        "within_year_start_variance": y_start_var,
        "within_year_end_variance": y_end_var,
        "within_year_variance_ratio": y_end_var / y_start_var,
        "within_year_lambda": ols_slope(start_y, end_y),
        "within_year_r": pearson(start_y, end_y),
        "closer_to_peak_n": closer,
        "closer_to_peak_fraction": closer / len(rows),
        "equal_abs_phase_n": equal,
        "mean_abs_start": mean([abs(x) for x in starts]),
        "mean_abs_end": mean([abs(x) for x in ends]),
    }


def actuator_metrics(rows: list[dict]) -> dict:
    rate_rows = [r for r in rows if r.get("rate") is not None]
    stop_rows = [r for r in rows if r.get("stopover") is not None]
    out = {
        "movement_rate_n": len(rate_rows),
        "stopover_n": len(stop_rows),
    }
    if len(rate_rows) >= 2:
        x = [r["start"] for r in rate_rows]
        y = [r["rate"] for r in rate_rows]
        out["movement_rate_slope_per_DFP_day"] = ols_slope(x, y)
        out["movement_rate_r"] = pearson(x, y)
        xc = year_center(rate_rows, "start")
        # year-center response manually
        by_year = defaultdict(list)
        for rr in rate_rows:
            by_year[rr["year"]].append(rr["rate"])
        ym = {k: mean(v) for k, v in by_year.items()}
        yc = [rr["rate"] - ym[rr["year"]] for rr in rate_rows]
        out["movement_rate_within_year_slope"] = ols_slope(xc, yc)
    if len(stop_rows) >= 2:
        x = [r["start"] for r in stop_rows]
        y = [r["stopover"] for r in stop_rows]
        out["stopover_slope_days_per_DFP_day"] = ols_slope(x, y)
        out["stopover_r"] = pearson(x, y)
        xc = year_center(stop_rows, "start")
        by_year = defaultdict(list)
        for rr in stop_rows:
            by_year[rr["year"]].append(rr["stopover"])
        ym = {k: mean(v) for k, v in by_year.items()}
        yc = [rr["stopover"] - ym[rr["year"]] for rr in stop_rows]
        out["stopover_within_year_slope"] = ols_slope(xc, yc)
    return out


def cluster_bootstrap(
    phase_rows: list[dict],
    actuator_rows: list[dict],
    *,
    replicates: int,
    seed: int,
) -> dict:
    phase_by_id: dict[str, list[dict]] = defaultdict(list)
    for row in phase_rows:
        phase_by_id[row["animal"]].append(row)
    actuator_by_id: dict[str, list[dict]] = defaultdict(list)
    for row in actuator_rows:
        actuator_by_id[row["animal"]].append(row)

    ids = sorted(phase_by_id)
    rng = random.Random(seed)

    raw_ratio = []
    year_ratio = []
    raw_lambda = []
    year_lambda = []
    closer_frac = []
    rate_slope = []
    stop_slope = []
    rate_within_year_slope = []
    stop_within_year_slope = []

    for _ in range(replicates):
        sampled = [rng.choice(ids) for _ in ids]
        phase_sample: list[dict] = []
        actuator_sample: list[dict] = []
        for draw_i, animal in enumerate(sampled):
            # Synthetic cluster label is irrelevant to the estimand, but each
            # sampled cluster contributes all animal-years and can appear more
            # than once, as required by a cluster bootstrap.
            phase_sample.extend(phase_by_id[animal])
            actuator_sample.extend(actuator_by_id.get(animal, []))
        try:
            m = metrics(phase_sample)
            raw_ratio.append(m["variance_ratio_end_over_start"])
            year_ratio.append(m["within_year_variance_ratio"])
            raw_lambda.append(m["whole_route_lambda"])
            year_lambda.append(m["within_year_lambda"])
            closer_frac.append(m["closer_to_peak_fraction"])
        except (ValueError, ZeroDivisionError):
            continue

        am = actuator_metrics(actuator_sample)
        if "movement_rate_slope_per_DFP_day" in am:
            rate_slope.append(am["movement_rate_slope_per_DFP_day"])
        if "movement_rate_within_year_slope" in am:
            rate_within_year_slope.append(am["movement_rate_within_year_slope"])
        if "stopover_slope_days_per_DFP_day" in am:
            stop_slope.append(am["stopover_slope_days_per_DFP_day"])
        if "stopover_within_year_slope" in am:
            stop_within_year_slope.append(am["stopover_within_year_slope"])

    return {
        "cluster_unit": "animal",
        "unique_animals": len(ids),
        "replicates_requested": replicates,
        "replicates_completed": len(raw_ratio),
        "seed": seed,
        "variance_ratio_ci95": ci95(raw_ratio),
        "within_year_variance_ratio_ci95": ci95(year_ratio),
        "whole_route_lambda_ci95": ci95(raw_lambda),
        "within_year_lambda_ci95": ci95(year_lambda),
        "closer_to_peak_fraction_ci95": ci95(closer_frac),
        "movement_rate_slope_ci95": ci95(rate_slope) if rate_slope else None,
        "movement_rate_within_year_slope_ci95": (
            ci95(rate_within_year_slope) if rate_within_year_slope else None
        ),
        "stopover_slope_ci95": ci95(stop_slope) if stop_slope else None,
        "stopover_within_year_slope_ci95": (
            ci95(stop_within_year_slope) if stop_within_year_slope else None
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/payoff_b_ortega_variance_funnel_result.json"),
    )
    parser.add_argument("--bootstrap-replicates", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20261003)
    args = parser.parse_args()

    raw = download(args.url)
    sha = hashlib.sha256(raw).hexdigest()
    if sha != EXPECTED_SHA256:
        raise SystemExit(
            f"source SHA256 mismatch: got {sha}, expected {EXPECTED_SHA256}"
        )

    with zipfile.ZipFile(BytesIO(raw)) as zf:
        strings = shared_strings(zf)
        paths = dict(workbook_sheet_paths(zf))
        phase_matrix = sheet_rows(zf, paths[PHASE_SHEET], strings, max_cols=12)
        actuator_matrix = sheet_rows(zf, paths[ACTUATOR_SHEET], strings, max_cols=20)

    phase_header = phase_matrix[0]
    phase_idx = {name: i for i, name in enumerate(phase_header)}
    phase_rows = []
    for row in phase_matrix[1:]:
        if not row:
            continue
        def get(name: str) -> str:
            i = phase_idx[name]
            return row[i] if i < len(row) else ""
        start = parse_float(get("DFP_Start"))
        end = parse_float(get("DFP_End"))
        year = get("year")
        id_yr = get("id_yr")
        if start is None or end is None or not year or not id_yr:
            continue
        phase_rows.append(
            {
                "id_yr": id_yr,
                "animal": id_yr.rsplit("_", 1)[0],
                "year": year,
                "timing": get("timing"),
                "start": start,
                "end": end,
            }
        )

    # The first actuator block occupies A:G; row 1 is a group title and row 2
    # contains the actual column names.
    actuator_header = actuator_matrix[1][:7]
    actuator_idx = {name: i for i, name in enumerate(actuator_header)}
    actuator_map = {}
    for row in actuator_matrix[2:]:
        if not row:
            continue
        def get_a(name: str) -> str:
            i = actuator_idx[name]
            return row[i] if i < len(row) else ""
        id_yr = get_a("id_yr")
        if not id_yr:
            continue
        actuator_map[id_yr] = {
            "rate": parse_float(get_a("rate.km.day")),
            "stopover": parse_float(get_a("stopover.day")),
            "compensation": get_a("compensation"),
        }

    joined = []
    for row in phase_rows:
        act = actuator_map.get(row["id_yr"], {})
        joined.append({**row, **act})

    result = {
        "date": "2026-10-03",
        "status": "POSTFREEZE_DESCRIPTIVE_SOURCE_DATA_AUDIT",
        "frozen_submission_affected": False,
        "source": {
            "article": "Ortega et al. 2023 Nature Communications 14:2008",
            "doi": "10.1038/s41467-023-37750-z",
            "source_data_sha256": sha,
            "phase_sheet": PHASE_SHEET,
            "actuator_sheet": ACTUATOR_SHEET,
        },
        "phase": metrics(phase_rows),
        "actuators": actuator_metrics(joined),
        "bootstrap": cluster_bootstrap(
            phase_rows,
            joined,
            replicates=args.bootstrap_replicates,
            seed=args.seed,
        ),
        "boundaries": [
            "published convergence and signed compensation are prior art, not a new PAYOFF-B discovery",
            "variance contraction alone does not identify individualized feedback",
            "no K, g, phi, r or D_eff is estimated",
            "measurement error, passive retention, selection and changing environmental variance remain alternative contributors",
            "the result does not retune frozen GEB V2 or any preregistered gate",
        ],
    }

    # Mechanical consistency checks.
    if result["phase"]["n"] != 152:
        raise SystemExit(f"expected 152 animal-years, got {result['phase']['n']}")
    if result["bootstrap"]["unique_animals"] != 72:
        raise SystemExit(
            f"expected 72 unique animals, got {result['bootstrap']['unique_animals']}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
