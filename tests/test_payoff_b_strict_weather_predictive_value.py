"""Synthetic pure-logic and model-leakage CV controls (no real GPS)."""
from datetime import date,timedelta
from scripts.audit_payoff_b_strict_weather_predictive_value import (
    site_time_features, make_risk_features, fold_score, CASE, STAY,
)

def test_only_source_day_and_trailing_stationary_run_enter_baseline():
    day=date(2017,3,9)
    same=("Bird","secret",2017)
    rows=[
        (same,day-timedelta(days=1),(35,13),STAY),
        (same,day,(35,13),CASE),
        (same,day+timedelta(days=2),(35,13),STAY),
    ]
    x=make_risk_features(rows,(True,True,True))
    assert len(x)==3
    assert x[1]["base"][-1]>x[0]["base"][-1]
    assert x[2]["base"][-1]==x[0]["base"][-1]
    assert "secret" not in str(x[0]["base"])
    assert len(site_time_features(day,(35,13),2))==6

def synthetic():
    # 5 calendar years, different animal IDs/year, no future predictor use.
    data=[]
    for year in range(2013,2018):
        for i in range(80):
            positive=(i%9==0)
            # No assumed positive effect; weather and labels are synthetic.
            base=site_time_features(date(year,3,1+i%20),(35+i%4,12),i%9+1)
            weather=[float((i+j)%11)/4 for j in range(8)]
            data.append(dict(base=base,weather=weather,y=int(positive),
                             year=year,animal=f"anonymous-{year}-{i}"))
    return data

def test_true_year_holdout_has_proper_score_and_no_prediction_export():
    out=fold_score(synthetic(),None,scheme="calendar_year")
    assert out["status"]=="OUT_OF_FOLD_OBSERVATIONAL_PREDICTION_ESTIMABLE"
    assert out["n_folds_admitted"]==5
    assert out["heldout_original_source_days"]==400
    assert out["baseline_log_loss"]>=0
    assert "anonymous-" not in str(out)

def test_heldout_animal_cv_is_not_same_random_rows():
    out=fold_score(synthetic(),None,scheme="whole_animal")
    assert out["status"]=="OUT_OF_FOLD_OBSERVATIONAL_PREDICTION_ESTIMABLE"
    assert out["heldout_original_source_days"]==400
    assert out["n_folds_admitted"]==5
    assert out["no_individual_predictions_or_animal_ids_exported"] is True
