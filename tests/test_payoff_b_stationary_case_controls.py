from datetime import date,timedelta
from scripts.qc_payoff_b_stationary_case_controls import (
    opportunities,match_opportunities,CONTROL_DAYS)

def test_stationary_control_before_fixed_case():
    day=date(2016,3,1)
    points=[(day+timedelta(days=i),20.0,10.0) for i in range(14)]
    points.extend([(day+timedelta(days=14),20.6,10.5),
                   (day+timedelta(days=15),21.6,11.2)])
    cases,controls=opportunities(points)
    assert cases=={date(2016,3,14)}
    chosen,totals=match_opportunities({("Bird","hidden",2016):points})
    assert totals["original_case_candidates"]==1
    assert totals["distinct_matched_identity_years"]==1
    assert "hidden" not in str(totals)
    assert CONTROL_DAYS==(5,21)

def test_missing_previous_control_not_relabelled():
    day=date(2016,3,1)
    track=[(day+timedelta(days=i),20,10) for i in range(3)]
    track += [(day+timedelta(days=3),20.5,10.5),
              (day+timedelta(days=4),21.6,11.2)]
    selected,count=match_opportunities({("Bird","secret",2016):track})
    assert count["original_case_candidates"]==1
    assert count["cases_without_matched_prior_control"]==1
    assert not selected
