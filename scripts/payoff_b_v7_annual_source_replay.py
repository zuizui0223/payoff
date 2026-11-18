"""Fail-closed source-aggregate replay for *candidate* original V7 annual onsets.

An independently sourced 1982--2011 per-region table, if supplied, can be
screened against 16 printed S1 means/SDs and 23 published Pearson q values.
A numerical match is necessary but NOT sufficient for source authentication.
No goose outcomes, guessed region geometry, or frozen V7 biological q×U fit.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

from scripts.payoff_b_v7_suppinfo_aggregate_gate import (
    QP, REGIONS, ROUTES, SOURCE_SHA, audit_pairs, readrows,
)

YEARS = tuple(range(1982, 2012))
REQUIRED_ANNUAL = frozenset({
    "flyway", "region_code", "year", "gdd_jerk_onset_julian",
    "original_source_identifier",
})
# S1 prints mean onset to integer Julian day and SD to 0.1 day; the q
# historical coefficients are printed to 2 dp. Do not retune after reading
# a candidate source. Printed 0.50 means a half-day nominal rounding band.
MEAN_ROUNDING_TOL = 0.5000001
SD_ROUNDING_TOL = 0.0500001
Q_ROUNDING_TOL = 0.0050001


def _pearson(a: list[float], b: list[float]) -> float | None:
    if len(a) != len(b) or len(a) < 3:
        raise ValueError("Pearson input lengths not supported")
    ma, mb = statistics.mean(a), statistics.mean(b)
    va = sum((x - ma)**2 for x in a)
    vb = sum((y - mb)**2 for y in b)
    if va <= 0 or vb <= 0:
        return None
    return sum((x-ma)*(y-mb) for x, y in zip(a, b)) / math.sqrt(va*vb)


def _parse_candidate(rows: list[dict]) -> tuple[dict, dict]:
    region_to_flyway = {
        code: flyway for flyway, codes in ROUTES.items() for code in codes
    }
    expected = len(region_to_flyway) * len(YEARS)
    if len(region_to_flyway) != 16:
        raise ValueError("Original region codes not unique across flyways")
    if not rows or not REQUIRED_ANNUAL.issubset(rows[0]):
        raise ValueError("Missing original candidate annual schema columns")
    if len(rows) != expected:
        raise ValueError(f"Expected exactly {expected} region-year rows")
    pairs: dict[tuple[str, int], float] = {}
    original_identifiers = set()
    for row in rows:
        code = row["region_code"].strip()
        flyway = row["flyway"].strip()
        if code not in region_to_flyway or region_to_flyway[code] != flyway:
            raise ValueError("Unknown source region / flyway assignment")
        try:
            year = int(row["year"])
            value = float(row["gdd_jerk_onset_julian"])
        except (TypeError, ValueError) as e:
            raise ValueError("Non-numeric original-source year or onset") from e
        if year not in YEARS or not math.isfinite(value) or not 1 <= value <= 366:
            raise ValueError("Candidate source year / onset outside frozen original window")
        source_identifier = row["original_source_identifier"].strip()
        if not source_identifier:
            raise ValueError("Candidate annual source provenance identifier absent")
        original_identifiers.add(source_identifier)
        key = code, year
        if key in pairs:
            raise ValueError("Duplicate original region-year key")
        pairs[key] = value
    required = {(code, year) for code in region_to_flyway for year in YEARS}
    if set(pairs) != required:
        raise ValueError("Original region-year coverage incomplete")
    return pairs, {
        "n_original_region_year_rows": len(pairs),
        "n_original_source_identifiers_claimed_not_verified": len(original_identifiers),
        "region_codes": len(region_to_flyway),
        "years": [min(YEARS), max(YEARS)],
    }


def inspect_candidate(rows: list[dict],
                      q_rows: list[dict] | None = None,
                      s1_rows: list[dict] | None = None,
                      original_file_sha256: str | None = None) -> dict:
    """Evaluate source consistency without authenticating input or bird outcome.

    Raises on structural corruption. Numerically conflicting candidate values
    are recorded explicitly with a mandatory hold, never auto-adjusted.
    """
    q_rows = q_rows if q_rows is not None else readrows(QP)
    s1_rows = s1_rows if s1_rows is not None else readrows(REGIONS)
    audit_pairs(q_rows, s1_rows)
    calendar, structure = _parse_candidate(rows)
    region_mismatches = []
    region_checks = []
    for r in s1_rows:
        code = r["code"]
        values = [calendar[(code, year)] for year in YEARS]
        actual_mean = statistics.mean(values)
        actual_sd = statistics.stdev(values)
        source_mean = float(r["mean_onset_julian_day"])
        source_sd = float(r["onset_sd_days"])
        mean_difference = actual_mean - source_mean
        sd_difference = actual_sd - source_sd
        ok = (abs(mean_difference) <= MEAN_ROUNDING_TOL and
              abs(sd_difference) <= SD_ROUNDING_TOL)
        if not ok:
            region_mismatches.append(code)
        region_checks.append({
            "code": code,
            "candidate_mean_julian": round(actual_mean, 7),
            "printed_mean_julian": source_mean,
            "candidate_sample_sd_days": round(actual_sd, 7),
            "printed_sd_days": source_sd,
            "matches_published_rounded_S1": ok,
        })
    pair_mismatches = []
    pair_checks = []
    for r in q_rows:
        flyway, a, b = r["flyway"], r["source_code"], r["target_code"]
        aa = [calendar[(a, year)] for year in YEARS]
        bb = [calendar[(b, year)] for year in YEARS]
        obs = _pearson(aa, bb)
        published = float(r["q_30year_correlation"])
        consistent = obs is not None and abs(obs - published) <= Q_ROUNDING_TOL
        if not consistent:
            pair_mismatches.append(f"{flyway}:{a}->{b}")
        pair_checks.append({
            "flyway": flyway,
            "source_code": a,
            "target_code": b,
            "candidate_30year_pearson": round(obs, 7) if obs is not None else None,
            "published_signed_q": published,
            "rounded_q_consistent": consistent,
        })
    match = not region_mismatches and not pair_mismatches
    return {
        "status": ("CANDIDATE_AGGREGATE_REPLAY_CONSISTENT_NOT_AUTHENTICATED"
                   if match else "CANDIDATE_ORIGINAL_AGGREGATES_CONFLICT_HOLD"),
        "source_original_supporting_DOCX_digest": SOURCE_SHA,
        "candidate_annual_file_sha256": original_file_sha256,
        "candidate_original_file_digest_checked_against_external_authority": False,
        "candidate_source_identifiers_verified_externally": False,
        "printed_S1_mean_rounding_tolerance_days": MEAN_ROUNDING_TOL,
        "printed_S1_SD_rounding_tolerance_days": SD_ROUNDING_TOL,
        "printed_pearson_q_rounding_tolerance": Q_ROUNDING_TOL,
        "original_row_grain": structure,
        "replayed_S1_region_checks": region_checks,
        "S1_mismatch_codes": region_mismatches,
        "replayed_23_signed_q_checks": pair_checks,
        "q_mismatch_transition_ids": pair_mismatches,
        "n_S1_matching": 16 - len(region_mismatches),
        "n_q_matching": 23 - len(pair_mismatches),
        "frozen_V7_annual_original_source_authorized": False,
        "original_geo_crosswalk_authorized": False,
        "original_goose_response_opened": False,
        "focal_q_times_geometry_U_fitted": False,
        "V7_REGISTERED_PRIMARY_GATE": "HOLD_NOT_ESTIMABLE",
        "interpretation": (
            "Numerical agreement with printed aggregates, even if achieved, "
            "does not certify original temperature inputs, regional code aliases, "
            "historical climate algorithm or source identity. Original year-specific "
            "data + 16 region GPS membership + independent geometry are still needed."
        ),
    }


def inspect_path(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"No candidate annual file at {path}")
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    with path.open(encoding="utf-8", newline="") as h:
        rows = list(csv.DictReader(h))
    return inspect_candidate(rows, original_file_sha256=sha)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--candidate-annual", type=Path, required=True)
    p.add_argument("--output", type=Path)
    opts = p.parse_args()
    result = inspect_path(opts.candidate_annual)
    if opts.output:
        opts.output.parent.mkdir(parents=True, exist_ok=True)
        opts.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n",
                               encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "n_S1_matching": result["n_S1_matching"],
        "n_q_matching": result["n_q_matching"],
        "original_source_authorized": result["frozen_V7_annual_original_source_authorized"],
        "V7_REGISTERED_PRIMARY_GATE": result["V7_REGISTERED_PRIMARY_GATE"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
