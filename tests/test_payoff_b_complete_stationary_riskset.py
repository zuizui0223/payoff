from datetime import date,timedelta
from scripts.qc_payoff_b_complete_stationary_riskset import (
    risk_opportunities,collect,label_future)

def daily():
    start=date(2017,3,1)
    p=[(start+timedelta(days=i),20,10) for i in range(15)]
    p.extend([(start+timedelta(days=15),20.5,10.5),
              (start+timedelta(days=16),21.6,11.2)])
    return p

def test_complete_risk_opportunity_includes_stayers_and_eventually_movers():
    r=list(risk_opportunities(daily()))
    assert sum(x[2]=="NORTHWARD_CANDIDATE" for x in r)==1
    assert sum(x[2]=="STAYED_TWO_DAYS" for x in r)>0

def test_missing_future_outcome_is_censored_not_stationary():
    r=list(risk_opportunities(daily()[:15]))
    assert r[-1][2]=="CENSORED"
    assert r[-2][2]=="CENSORED"

def test_other_direction_is_not_stay():
    rows=[(date(2017,3,4),19.3,10.3),(date(2017,3,5),18,11)]
    assert label_future((20,10),rows)=="OTHER_MOVEMENT"

def test_source_inference_no_ids_exported():
    private,c,m,y=collect({("bird","private-id",2017):daily()})
    assert c["deduplicated_frozen_cases"]==1
    assert c["STAYED_TWO_DAYS"]>0
    assert c["NORTHWARD_CANDIDATE"]==1
    assert "private-id" not in str(c)
    assert "private-id" not in str(m)
