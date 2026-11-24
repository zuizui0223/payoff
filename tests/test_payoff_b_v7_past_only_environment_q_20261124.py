"""Synthetic-only V7 environmental historical forecast gates. Never bird timing."""
import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts import payoff_b_v7_past_only_environment_q_20261124 as h


def fake_series(group="greenland",transition="R2-R3"):
    return [{"flyway":group,"transition":transition,"year":y,
             "source":float(100+(y-1982)%9),
             "target":float(109+2*((y-1982)%9))}
            for y in range(1982,2014)]


def contract():
    return {"time_rule":{"focal_migration_years":[2006,2007,2008,2009,2010,2011]},
            "threshold_gate":{"independent_historical_transitions_min":10,
             "independent_flyways_min":2,
             "distinct_focal_years_min":3}}


def test_future_2012_target_cannot_change_2006_past_only_q_or_forecast():
    rows=fake_series()
    a=h.evaluate(rows,contract())
    perturbed=deepcopy(rows)
    perturbed[-1]["target"]=366.0
    b=h.evaluate(perturbed,contract())
    a2006=[x for x in a["environmental_forecast_scores_only"] if x["year"]==2006][0]
    b2006=[x for x in b["environmental_forecast_scores_only"] if x["year"]==2006][0]
    assert a2006==b2006
    assert a2006["n_prior_pairs"]==24
    assert a2006["latest_training_year"]==2005
    assert a2006["current_year_target_used_in_training"] is False
    assert a2006["actual_bird_had_source_onset_before_departure_verified"] is False
    assert a["status"]=="V7_HISTORICAL_Q_SOURCE_SUPPORT_GATE_NOT_MET"


def test_past_correlation_negative_retained_not_abs():
    years=[{"year":y,"source":float(101+(y%12)),
            "target":float(145-(y%12))}
            for y in range(1982,2006)]
    z=h.historical_forecast(years,2006)
    assert z["status"]=="PAST_ONLY_ENVIRONMENT_PREDICTIVE_MODEL_ESTIMABLE"
    assert abs(z["signed_historical_source_target_r"]+1)<1e-10


def test_focal_year_and_future_year_banned_from_training():
    y=fake_series()
    with pytest.raises(ValueError,match="Future or focal"):
        h.historical_forecast(y,2006)
    with pytest.raises(ValueError,match="registered"):
        h.historical_forecast(y,2013)


def test_original_column_fields_only_and_duplicate_transition_year_rejected():
    good="flyway,transition,year,source_spring_onset_doy,target_spring_onset_doy\n" \
          "greenland,R2-R3,1982,100,110\n"
    z=h.parse_env_rows(good)
    assert len(z)==1
    assert z[0]["source"]==100
    with pytest.raises(ValueError,match="Duplicate"):
        h.parse_env_rows(good+"greenland,R2-R3,1982,102,111\n")
    with pytest.raises(ValueError,match="five-field"):
        h.parse_env_rows("timestamp,animal_id,departure\n2006,A,101\n")


def test_support_gate_only_if_flyways_and_transitions_with_heldout_years():
    rows=[]
    for grp in ["greenland","svalbard"]:
        for j in range(6):
            rows+=fake_series(grp,f"R{j}-R{j+1}")
    z=h.evaluate(rows,contract())
    assert z["status"]=="HISTORICAL_ENVIRONMENT_Q_SUPPORT_ESTIMABLE_ONLY"
    assert z["n_frozen_transitions_with_forward_year_scores"]==12
    assert z["n_flyways_with_forward_year_scores"]==2
    assert z["n_distinct_focal_years_with_scores"]==6
    assert z["actual_predeparture_source_onset_exposure_verified"] is False
    assert z["ecological_recourse_r_or_q_times_r_fitted"] is False
    # Even synthetic support has no goose timing data and does not establish V7 behavior.
    assert z["bird_focal_migration_timing_accessed"] is False


def test_insufficient_earlier_phenology_never_imputed_from_future():
    rows=fake_series()
    limited=[r for r in rows if r["year"]>=2003 and r["year"]<2006]
    z=h.historical_forecast(limited,2006)
    assert z["status"]=="INSUFFICIENT_PAST_ENVIRONMENT_YEARS"
    assert z["n_prior_pairs"]==3


def test_contract_has_explicit_anti_lookahead_and_original_v7_not_changed():
    c=json.loads(h.CONTRACT.read_text())
    assert c["time_rule"]["no_future_year_training"] is True
    assert c["time_rule"]["no_current_focal_year_training"] is True
    assert c["no_ebird"] is True
    assert c["cannot_overwrite_prior_contract_or_frozen_submission"] is True
    assert c["candidate_measure"]["minimum_prior_paired_years"]==20
