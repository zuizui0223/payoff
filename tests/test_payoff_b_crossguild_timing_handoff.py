from scripts.run_payoff_b_crossguild_timing_handoff import (
    EXPECTED_ADMITTED,eligible_rows,evaluate,
)
from datetime import date

def test_prior_source_case_gate_remains_fixed():
    assert EXPECTED_ADMITTED=={
        "stork":91, "woodcock_argos":37,
        "white_fronted_goose":23,"curlew":7,"dabbling_ducks":0}

def test_source_censor_counts_preserved():
    from scripts.qc_public_movebank_spring_geometry import analyze_one
    valid=[(date(2015,3,i),float(i*2)) for i in range(1,21)]
    invalid=[(date(2015,3,i),1.0) for i in range(1,21)]
    groups={
        ("Synthetic taxon","animal A",2015):valid,
        ("Synthetic taxon","animal B",2015):invalid,
    }
    rows,stat=eligible_rows(groups)
    assert len(rows["Synthetic taxon"])==1
    assert stat["Synthetic taxon"]["LATITUDINAL_RANGE_UNRESOLVED"]==1

def test_unevaluable_sample_reports_none_not_zero_beta():
    rows=[{"animal":str(i),"year":2015,"x":60+i,"y":90+i} for i in range(7)]
    v=evaluate(rows)
    assert v["status"]=="NOT_ESTIMABLE_FROZEN_SAMPLE_GATE"
    assert "year_FE_beta_X20_to_Y80" not in v
    assert v["ecological_effect_confirmed"] is False

def test_within_year_slope_does_not_claim_information_feedback():
    rows=[]
    for year in range(2013,2018):
        for i in range(4):
            rows.append({"animal":str(i),"year":year,
                         "x":float(70+i+year),"y":float(90+i*.5+year)})
    v=evaluate(rows)
    assert v["status"]=="NOT_ESTIMABLE_FROZEN_SAMPLE_GATE"
    assert not v["ecological_effect_confirmed"]
