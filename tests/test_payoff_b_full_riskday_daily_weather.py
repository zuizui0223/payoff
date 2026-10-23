"""NASA daily-batch chronology and grid-month case/control comparison."""
from datetime import date,timedelta
from scripts.run_payoff_b_full_riskday_daily_weather import (
    batch_key,batch_range,load_daily_payload,event_prior_weather,calculate_contrast,
    VARS
)

def mock_batch(key):
    a,b=batch_range(key)
    values={}
    for var in VARS:
        day=a;series={}
        while day<=b:
            series[day.strftime("%Y%m%d")]=0.0 if var=="T2M" else 2.0
            day+=timedelta(days=1)
        values[var]=series
    return {"header":{"time_standard":"UTC"},
            "properties":{"parameter":values}}

def test_full_month_series_never_exposes_future_as_antecedent():
    d=date(2017,3,17)
    key=batch_key(d,(35.1,12.2))
    start,end=batch_range(key)
    assert start==date(2017,2,21)
    assert end==date(2017,3,31)
    raw=mock_batch(key)
    raw["properties"]["parameter"]["T2M"]["20170316"]=7.
    raw["properties"]["parameter"]["T2M"]["20170317"]=9999.
    v=event_prior_weather(load_daily_payload(raw,key),d)
    assert v["T2M_last"]==7.0
    assert v["T2M_anomaly"]==7.0

def test_other_and_censored_riskdays_are_not_stay_controls():
    d=date(2017,3,15)
    l=[
       (("bird","secret1",2017),d,(35,12),"NORTHWARD_CANDIDATE",
        {name+"_anomaly":2.0 for name in VARS}|{name+"_last":3.0 for name in VARS}),
       (("bird","secret2",2017),d,(35,12),"STAYED_TWO_DAYS",
        {name+"_anomaly":1.0 for name in VARS}|{name+"_last":2.0 for name in VARS}),
       (("bird","secret3",2017),d,(35,12),"OTHER_MOVEMENT",
        {name+"_anomaly":1000.0 for name in VARS}|{name+"_last":1000.0 for name in VARS}),
    ]
    result=calculate_contrast(l)
    assert result["complete_case_source_days"]==1
    assert result["complete_stay_source_days"]==1
    assert result["grid_year_month_adjusted_case_weighted_descriptive_difference"]["V10M_anomaly"]==1.0
    assert "secret1" not in str(result)
    assert result["site_year_month_adjusted_difference_is_causal"] is False
