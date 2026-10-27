"""Directional wind, solar and strict historical timeline tests, synthetic."""
from datetime import date,timedelta
import pytest
from scripts.audit_payoff_b_riskday_directional_weather import (
    parse_weather,request_query,summarize_source,SOURCE_VARS
)

def fake_weather(start,end,future=False):
    d=start;one={};two={}
    while d<=end:
        for hour in range(24):
            key=d.strftime("%Y%m%d")+f"{hour:02d}"
            one[key]=2.0 if d<end else 3.0
            two[key]=140.0 if d<end else 180.0
        d+=timedelta(days=1)
    if future:one[(end+timedelta(days=1)).strftime("%Y%m%d")+"00"]=3.
    return {"header":{"time_standard":"UTC"},
            "properties":{"parameter":{"V10M":one,
                     "ALLSKY_SFC_SW_DWN":two}}}

def test_northward_wind_signed_and_solar_shift():
    url,start,end=request_query((34.1,13.2),date(2019,3,17))
    assert start==date(2019,3,9) and end==date(2019,3,16)
    assert "parameters=V10M%2CALLSKY_SFC_SW_DWN" in url
    result=parse_weather(fake_weather(start,end),start,end)
    assert result["V10M"]["change_vs_previous_seven_days"]==1
    assert result["ALLSKY_SFC_SW_DWN"]["change_vs_previous_seven_days"]==40

def test_future_day_rejected():
    url,start,end=request_query((34,13),date(2019,3,17))
    with pytest.raises(ValueError,match="after predecision"):
        parse_weather(fake_weather(start,end,True),start,end)

def test_source_summary_contains_no_ids_dates_or_locations():
    d=date(2019,3,17)
    sampled=[
      ("h1",("Bird","SecretA",2019),d,(34,13),"NORTHWARD_CANDIDATE"),
      ("h2",("Bird","SecretB",2019),d+timedelta(days=1),
       (34,13),"STAYED_TWO_DAYS")
    ]
    k=request_query(sampled[0][3],sampled[0][2])[0]
    j=request_query(sampled[1][3],sampled[1][2])[0]
    def obs(v):
        return {"V10M":{"prior_decision_day_mean":v,
                        "change_vs_previous_seven_days":v-1},
                "ALLSKY_SFC_SW_DWN":{"prior_decision_day_mean":100+v,
                        "change_vs_previous_seven_days":v*2}}
    out=summarize_source(sampled,{k:obs(4),j:obs(2)})
    assert out["case_minus_stay_group_mean_differences"]["northwind_anomaly"]==2
    assert "SecretA" not in str(out)
    assert out["northward_wind_10m_is_route_specific_tailwind"] is False
