"""Protect the original Egyptian-vulture declared source and thresholds."""
from scripts.qc_payoff_b_egyptian_vulture_fullrisk import (
    SOURCE,EXPECTED_ORIGINAL_CANDIDATES,
    EXPECTED_SPRING_SOURCE_ANIMAL_YEARS_WITH_CANDIDATES,
    MIN_WEATHER_CASES_IN_MATCHING_GRIDMONTH,
    MIN_WEATHER_GRIDMONTH_OVERLAP_STRATA,MAX_NASA_MONTHLY_BATCHES
)
from scripts.qc_payoff_b_unopened_gps_source import SOURCES

def test_vulture_source_fixed_before_any_weather():
    assert SOURCE=="egyptian_vulture"
    assert SOURCES[SOURCE]["taxon"]=="Neophron percnopterus"
    assert SOURCES[SOURCE]["doi"]=="10.5441/001/1.385gk270"
    assert EXPECTED_ORIGINAL_CANDIDATES==30
    assert EXPECTED_SPRING_SOURCE_ANIMAL_YEARS_WITH_CANDIDATES==18
    assert MIN_WEATHER_CASES_IN_MATCHING_GRIDMONTH==10
    assert MIN_WEATHER_GRIDMONTH_OVERLAP_STRATA==5
    assert MAX_NASA_MONTHLY_BATCHES==500
