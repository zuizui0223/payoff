"""Synthetic guardrails for original radar q10–q90 / greenup chronology.

No actual original site/year observations are exposed. Source benchmark gating
is exercised on a fictional two-year fixture, not a new ecological test.
"""
from __future__ import annotations
import copy
import pytest

from scripts import payoff_b_radar_migration_window_20261124 as m


def fixture():
    rows=[]
    for y,site,q10,q50,q90,g in [
        (2012,"PRIVATE_A",100,110,120,-27),
        (2012,"PRIVATE_B",100,110,120,90),
        (2012,"PRIVATE_C",100,110,120,106),
        (2013,"PRIVATE_A",100,110,120,115),
        (2013,"PRIVATE_B",100,110,120,130),
        (2013,"PRIVATE_C",100,110,120,110),
    ]:
        rows.append({"year":y,"site":site,"spring_q10":q10,
                     "spring_q50":q50,"spring_q90":q90,"mean_greenup":g,
                     "spring_mean_temp":12.0})
    return rows


def contract():
    return {
      "expected_source_rows":6,"expected_base_complete_rows":6,
      "expected_sites":3,"expected_years":2,"source_years":[2012,2013],
      "source_structure_gates":{
        "validate_original_q50_counts":{
          "strict_greenup_before_q50":2,
          "q50_before_greenup":2,"tie":1,"unclassifiable":1
        },
        "max_total_unclassifiable_fraction":0.20
      },
      "primary_exclusive_classes":["TEST_1","TEST_2","TEST_3","TEST_4"],
    }


def test_ties_straddle_migration_window_unambiguously():
    assert m.exclusive_class(100,110,120,99.999)=="greenup_before_q10"
    assert m.exclusive_class(100,110,120,100)=="greenup_q10_to_before_q50"
    assert m.exclusive_class(100,110,120,110)=="greenup_q50_to_q90"
    assert m.exclusive_class(100,110,120,120)=="greenup_q50_to_q90"
    assert m.exclusive_class(100,110,120,120.01)=="greenup_after_q90"
    with pytest.raises(ValueError,match="Nonmonotonic"):
        m.exclusive_class(112,110,125,110)


def test_full_partition_and_unknown_bounds_no_imputation():
    z=m.summarize(fixture(),contract())
    assert z["status"]=="WINDOW_CHRONOLOGY_COMPLETED_BOUNDING_NOT_CUE_USE"
    assert z["source_counts"]["classifiable"]==5
    assert z["source_counts"]["unclassifiable"]==1
    assert z["classifiable_exclusive_counts"]=={
        "greenup_before_q10":1,
        "greenup_q10_to_before_q50":1,
        "greenup_q50_to_q90":2,
        "greenup_after_q90":1
    }
    b=z["pooled_logical_bounds"]["greenup_before_q10"]
    assert b["fraction_lower"]==pytest.approx(1/6)
    assert b["fraction_upper"]==pytest.approx(2/6)
    assert z["pooled_logical_bounds"]["greenup_at_least_7d_before_q10"]["classifiable_positive_count"]==1
    assert z["parent_q50_checkpoint"]==contract()["source_structure_gates"]["validate_original_q50_counts"]
    assert len(z["annual_aggregate"])==2
    assert "PRIVATE_A" not in str(z)
    assert "PRIVATE_B" not in str(z)
    assert z["no_individual_bird_information_use_estimated"] is True


def test_q10_absent_does_not_change_denominator_or_silently_impute():
    x=fixture()
    x[2]["spring_q10"]=None
    z=m.summarize(x,contract())
    assert z["status"]=="SOURCE_SUPPORT_FAILED" # 2/6 unknown exceeds 20%
    assert z["source_counts"]["unclassifiable"]==2
    assert z["pooled_logical_bounds"] is None


def test_nonmonotonic_quantile_gate_fails_closed():
    x=fixture()
    x[2]["spring_q10"]=130
    z=m.summarize(x,contract())
    assert z["source_checks"]["quantiles_ordered"] is False
    assert z["pooled_logical_bounds"] is None


def test_parent_q50_checkpoint_prevents_reinterpreting_negative_day():
    x=fixture()
    x[0]["mean_greenup"]=-26
    with pytest.raises(ValueError,match="q50 source checkpoint"):
        m.summarize(x,contract())


def test_calendar_day_outside_366_yields_unknown_not_repair():
    x=fixture()
    x[3]["spring_q10"]=400
    z=m.summarize(x,contract())
    assert z["status"]=="SOURCE_SUPPORT_FAILED"
    assert z["source_counts"]["unclassifiable"]==2
    assert z["pooled_logical_bounds"] is None


def test_source_csv_duplicate_station_year_rejected(tmp_path):
    p=tmp_path/"original_private.csv"
    p.write_text(
        "site,year,spring_q10,spring_q50,spring_q90,mean_greenup,spring_mean_temp\n"
        "S1,2012,100,110,120,90,10\n"
        "S1,2012,100,111,120,90,10\n"
    )
    with pytest.raises(ValueError,match="Duplicate"):
        m.source_rows(p)
