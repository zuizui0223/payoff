"""Synthetic source-only tests for radar mean-greenup vs passage-median timing."""
from __future__ import annotations

import copy
import pytest

pytest.importorskip("numpy", reason="original radar extractor's empirical dependency")
from scripts import payoff_b_radar_greenup_chronology_20261122 as chrono


def fixture(timing_a=0.0, timing_b=7.0):
    x=[]
    for y in range(2003,2019):
        for site,d in [("fake_A",timing_a),("fake_B",timing_b)]:
            g=120.0 + (y-2003)*0.2
            x.append({
              "site":site,"year":y,"spring_q50":g+d,
              "mean_greenup":g,"spring_mean_temp":10.0,
            })
    return x


def contract():
    return {
      "expected_rows":32,"expected_sites":2,"expected_years":16,
      "parent_source_grain_numeric":{"expected_original_rows":32},
      "uncertainty":{"seed":20261122,"bootstrap_replicates":30,
                     "quantiles":[0.025,0.975]},
    }


def test_positive_gap_means_greenup_earlier_not_bird_earlier():
    assert chrono.date_gap(130,120)==10
    assert chrono.chronological_categories(10)["at_least_seven_days_prior"]
    assert chrono.chronological_categories(-10)["q50_strictly_before_greenup"]


def test_exact_day_is_not_strictly_earlier_or_one_day_prior():
    kinds=chrono.chronological_categories(0)
    assert kinds["same_day_or_equal_timing"]
    assert kinds["optimistic_same_day_or_prior"]
    assert not kinds["greenup_strictly_before_q50"]
    assert not kinds["at_least_one_day_prior"]


def test_pooled_year_counts_without_original_site_ids():
    result=chrono.calc(fixture(),contract())
    assert result["status"]=="SOURCE_CHRONOLOGY_COMPLETED_NOT_ANIMAL_INFORMATION"
    assert result["n_complete_station_years"]==32
    counts=result["pooled_station_year_counts"]
    assert counts["same_day_or_equal_timing"]==16
    assert counts["greenup_strictly_before_q50"]==16
    assert counts["at_least_seven_days_prior"]==16
    assert counts["q50_strictly_before_greenup"]==0
    assert result["n_years"]==16
    assert len(result["annual_aggregate_only"])==16
    assert "fake_A" not in str(result)
    assert "fake_B" not in str(result)
    assert result["individual_bird_information_or_causal_cue_use_estimated"] is False


def test_q50_before_greenup_all_years():
    result=chrono.calc(fixture(-4,-2),contract())
    assert result["pooled_station_year_counts"]["q50_strictly_before_greenup"]==32
    assert result["n_years_majority_q50_before_greenup"]==16
    assert result["pooled_station_year_counts"]["at_least_seven_days_prior"]==0


def test_fail_closed_wrong_source_grain_and_duplicate_site_year():
    with pytest.raises(ValueError,match="source original n changed"):
        chrono.calc(fixture()[:-1],contract())
    x=fixture()
    x[-1]["site"]="fake_A"
    with pytest.raises(ValueError,match="duplicate"):
        chrono.calc(x,contract())


def test_fail_closed_incomplete_and_invalid_doy():
    x=fixture()
    x[0]["spring_mean_temp"]=None
    with pytest.raises(ValueError,match="complete-case sample"):
        chrono.calc(x,contract())
    x=fixture()
    x[0]["spring_q50"]=400
    with pytest.raises(ValueError,match="calendar day"):
        chrono.calc(x,contract())


def test_bootstrap_is_year_unit_not_station_pseudoreplication():
    x=chrono.calc(fixture(),contract())
    assert x["bootstrap"]["unit"]=="calendar_year"
    assert x["bootstrap"]["replicates"]==30
    assert x["equal_year_bootstrap_ci95"]["seven_days_prior"]==[0.5,0.5]
