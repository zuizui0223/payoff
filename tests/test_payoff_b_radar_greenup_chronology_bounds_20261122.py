"""Exact finite-sample chronology bounds with one unresolved original DOY."""
import pytest
pytest.importorskip("numpy", reason="source reader uses empirical NumPy")

from scripts import payoff_b_radar_greenup_chronology_bounds_20261122 as mod


def synthetic():
    out=[]
    for year in range(2003,2019):
        for site in ["PRIVATE_A", "PRIVATE_B"]:
            greenup=120.0
            q50=115.0 if site=="PRIVATE_A" else 127.0
            if year==2012 and site=="PRIVATE_B":
                greenup=-27.0
            out.append(dict(site=site,year=year,
                            mean_greenup=greenup,
                            spring_q50=q50,spring_mean_temp=10.0))
    return out


def contract():
    return {"known_counts":{
        "source_rows":32,"complete_case_station_years":32,
        "stations":2,"years":16,"invalid_greenup_DOY_count":1,
        "invalid_greenup_year":2012,"invalid_greenup_value":-27,
        "valid_comparable_station_years":31,
    }}


def test_source_rows_admitted_with_one_unknown_not_imputed():
    z=mod.bound_source_rows(synthetic(),contract())
    assert z["status"]=="BOUNDED_SOURCE_CHRONOLOGY_POST_FAILURE_NOT_NEW_EFFECT"
    assert z["original_strict_chronology_status"]=="HOLD_REQUIRES_SOURCE_SEMANTICS"
    assert z["valid_classifiable_station_years"]==31
    assert z["unresolved_original_station_years"]==1
    b=z["pooled_exact_identification_bounds"]
    assert b["q50_strictly_before_greenup"]=={"valid_count":16,"lower":0.5,"upper":17/32}
    assert b["at_least_seven_days_prior"]=={"valid_count":15,"lower":15/32,"upper":0.5}
    assert z["n_years_majority_q50_prior_greenup_certain"]==0
    assert z["n_years_majority_q50_prior_greenup_possible"]==1
    assert "PRIVATE_A" not in str(z)
    assert "PRIVATE_B" not in str(z)
    assert z["animal_cue_availability_or_behavior_identified"] is False


def test_wrong_invalid_source_count_fails_closed():
    x=synthetic()
    x[0]["mean_greenup"]=-4.0
    with pytest.raises(ValueError,match="unexpected out-of-range"):
        mod.bound_source_rows(x,contract())


def test_unknown_source_year_or_value_mismatch_fails_closed():
    x=synthetic()
    for r in x:
        if r["year"]==2012 and r["site"]=="PRIVATE_B":
            r["mean_greenup"]=-26.0
    with pytest.raises(ValueError,match="unusual value"):
        mod.bound_source_rows(x,contract())


def test_original_duplicate_station_year_rejected():
    x=synthetic()
    x[0]["site"]="PRIVATE_B"
    with pytest.raises(ValueError,match="duplicate"):
        mod.bound_source_rows(x,contract())


def test_no_missing_source_rows_silently_deleted():
    x=synthetic()
    x[0]["spring_mean_temp"]=None
    with pytest.raises(ValueError,match="original complete-case"):
        mod.bound_source_rows(x,contract())
