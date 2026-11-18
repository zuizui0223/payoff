"""Fails closed on invented annual GDD series or missing original regional keys.

The synthetic fixture is exclusively a NEGATIVE CONTROL; it is not field
evidence, not original source data, and never becomes a V7 timing response.
"""
from copy import deepcopy
import math

import pytest

from scripts.payoff_b_v7_annual_source_replay import (
    REQUIRED_ANNUAL, YEARS, inspect_candidate,
)
from scripts.payoff_b_v7_suppinfo_aggregate_gate import REGIONS, ROUTES, readrows


def synthetic_marginally_matching_annual():
    """Fake series exactly matching the 16 printed S1 means and SDs.

    All standardized yearly deviations are shared, so every pairwise q is +1,
    intentionally *contradicting* the original 23 published q values.
    """
    s1 = readrows(REGIONS)
    years = len(YEARS)
    centered = [i - (years - 1)/2 for i in range(years)]
    unit = math.sqrt(sum(t*t for t in centered)/(years - 1))
    values = [t/unit for t in centered]
    rows = []
    for row in s1:
        code = row["code"]
        flyway = next(f for f, route in ROUTES.items() if code in route)
        mu = float(row["mean_onset_julian_day"])
        sd = float(row["onset_sd_days"])
        for year, z in zip(YEARS, values):
            rows.append({
                "flyway": flyway,
                "region_code": code,
                "year": str(year),
                "gdd_jerk_onset_julian": str(mu+sd*z),
                "original_source_identifier": "SYNTHETIC_NEGATIVE_CONTROL_NOT_REAL",
            })
    return rows


def test_full_window_and_required_schema_only_not_sufficient():
    rows = synthetic_marginally_matching_annual()
    assert len(rows) == 16*30
    assert REQUIRED_ANNUAL.issubset(rows[0])
    result = inspect_candidate(rows)
    assert result["n_S1_matching"] == 16
    assert result["n_q_matching"] == 0
    assert result["status"] == "CANDIDATE_ORIGINAL_AGGREGATES_CONFLICT_HOLD"
    assert result["V7_REGISTERED_PRIMARY_GATE"] == "HOLD_NOT_ESTIMABLE"
    assert result["original_goose_response_opened"] is False
    assert result["frozen_V7_annual_original_source_authorized"] is False
    assert result["original_geo_crosswalk_authorized"] is False


def test_missing_a_year_fails():
    with pytest.raises(ValueError, match="Expected exactly"):
        inspect_candidate(synthetic_marginally_matching_annual()[:-1])


def test_duplicate_region_year_key_fails():
    rows = synthetic_marginally_matching_annual()
    rows[-1] = deepcopy(rows[0])
    with pytest.raises(ValueError, match="Duplicate original region-year"):
        inspect_candidate(rows)


def test_wrong_flyway_mapping_fails():
    rows = synthetic_marginally_matching_annual()
    rows[0]["flyway"] = "Svalbard"
    with pytest.raises(ValueError, match="Unknown source region"):
        inspect_candidate(rows)


def test_missing_provenance_identifier_fails():
    rows = synthetic_marginally_matching_annual()
    rows[5]["original_source_identifier"] = ""
    with pytest.raises(ValueError, match="provenance"):
        inspect_candidate(rows)


def test_wrong_annual_window_fails():
    rows = synthetic_marginally_matching_annual()
    rows[0]["year"] = "2012"
    with pytest.raises(ValueError, match="outside frozen"):
        inspect_candidate(rows)


def test_nonfinite_or_infinite_onset_fails():
    rows = synthetic_marginally_matching_annual()
    rows[0]["gdd_jerk_onset_julian"] = "nan"
    with pytest.raises(ValueError, match="outside frozen"):
        inspect_candidate(rows)


def test_marginal_S1_failure_also_identified():
    rows = synthetic_marginally_matching_annual()
    first = next(x for x in rows if x["region_code"] == "IRE")
    first["gdd_jerk_onset_julian"] = str(float(first["gdd_jerk_onset_julian"])+30.0)
    result = inspect_candidate(rows)
    assert "IRE" in result["S1_mismatch_codes"]
    assert result["n_S1_matching"] == 15
    assert result["V7_REGISTERED_PRIMARY_GATE"] == "HOLD_NOT_ESTIMABLE"
