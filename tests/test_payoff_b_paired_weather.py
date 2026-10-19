"""No-network meteorology chronology and difference controls."""
from datetime import date,timedelta
import math
import pytest
from scripts.audit_payoff_b_paired_weather import (
    source_query,parse_nasa_span,summarize_paired,WEATHER_CONTEXT_DAYS
)

def mock_payload(start, end, extra_future=False):
    a,b={},{}
    day=start
    while day<=end:
        for h in range(24):
            ts=day.strftime("%Y%m%d")+f"{h:02d}"
            a[ts]=10.0+((day-start).days==7)*3.0
            b[ts]=2.0+((day-start).days==7)*1.0
        day+=timedelta(days=1)
    if extra_future:
        a[(end+timedelta(days=1)).strftime("%Y%m%d")+"00"]=15
    return {"header":{"time_standard":"UTC"},
            "properties":{"parameter":{"T2M":a,"WS10M":b}}}

def test_weather_before_reference_only_and_normalization():
    day=date(2016,4,12)
    url,start,last=source_query((38.21,12.31),day)
    assert start==date(2016,4,3)
    assert last==date(2016,4,11)
    assert "latitude=38.0" in url and "longitude=12.5" in url
    r=parse_nasa_span(mock_payload(start,last),start,last)
    assert r["T2M"]["predecision_anomaly"]==3
    assert r["WS10M"]["predecision_anomaly"]==1

def test_future_weather_not_usable_as_input():
    day=date(2016,4,12)
    _,start,last=source_query((0,0),day)
    with pytest.raises(ValueError,match="future"):
        parse_nasa_span(mock_payload(start,last,extra_future=True),start,last)

def test_paired_output_carries_no_animal_data():
    r=summarize_paired([
        {"temp_raw_difference":1.0,"wind_raw_difference":0.2,
         "temp_anomaly_difference":0.1,"wind_anomaly_difference":-0.2,
         "calendar_gap_days":8.0},
        {"temp_raw_difference":2.0,"wind_raw_difference":-0.4,
         "temp_anomaly_difference":0.0,"wind_anomaly_difference":0.4,
         "calendar_gap_days":10.0}
    ],"stork")
    assert r["paired_seven_day_anomaly_difference_temp_c"]["n_pairs"]==2
    assert not r["actual_bird_cue_use_unmeasured"]==False
    assert "animal_id" not in str(r).lower()
