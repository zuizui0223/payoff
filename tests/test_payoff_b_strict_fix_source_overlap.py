"""Synthetic source riskday mask and overlap; never read real locations."""
from datetime import date,timedelta
from scripts.qc_payoff_b_strict_fix_source_overlap import (
    filtered_source_gate,CASE,STAY,MIN_CASES_SAME_GRIDYEAR_MONTH,
    ORIGINAL_CLEAN_COUNT,
)

def test_original_strict_case_counts_fixed_before_weather():
    assert ORIGINAL_CLEAN_COUNT["stork"]==(1110,85,716)
    assert ORIGINAL_CLEAN_COUNT["egyptian_vulture"]==(1257,13,1029)
    assert MIN_CASES_SAME_GRIDYEAR_MONTH==10

def test_grid_month_stay_overlap_is_source_only():
    d=date(2015,4,2)
    risk=[
       (("Bird","A",2015),d,(20.,10.),CASE),
       (("Bird","B",2015),d+timedelta(days=1),(20.,10.),STAY),
       (("Bird","C",2015),d+timedelta(days=2),(23.,10.),STAY),
       (("Bird","D",2015),d+timedelta(days=3),(20.,10.),"CENSORED"),
    ]
    result=filtered_source_gate(risk,[True,True,False,True])
    assert result["strict_all_3days_fix_within_30km_source_riskdays"]==3
    assert result["strict_all_3days_source_label_counts"][CASE]==1
    assert result["strict_case_and_stay_weather_source_query_plan"]["grid_months_with_both_northward_and_stay_observations"]==1
    assert result["source_overlap_preweather_admission"]["passed"] is False
    assert result["original_weather_association_refitted"] is False
    assert "20.0" not in str(result)
