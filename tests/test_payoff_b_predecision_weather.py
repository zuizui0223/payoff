import math
from datetime import date,timedelta
from scripts.audit_payoff_b_predecision_weather import (
    nasa_power_request,parse_power_day,source_meteorology_availability,collect_events
)

def synthetic_response(day,with_future=False):
    k=day.strftime("%Y%m%d")
    a={f"{k}{h:02d}":10.+h*.1 for h in range(24)}
    b={f"{k}{h:02d}":2.0 for h in range(24)}
    if with_future:a["2015030400"]=20.0
    return {"header":{"time_standard":"UTC"},
            "properties":{"parameter":{"T2M":a,"WS10M":b}}}

def test_hourly_cue_is_from_only_previous_calendar_date():
    day=date(2015,3,2)
    url=nasa_power_request(30.123,22.987,day)
    assert "latitude=30.0" in url and "longitude=23.0" in url
    assert "start=20150302" in url and "end=20150302" in url
    assert "time-standard=UTC" in url
    got=parse_power_day(synthetic_response(day),day)
    assert got["source_valid"]
    assert got["valid_wind_hours"]==24
    assert got["wind_speed_10m_mean_m_s"]==2.

def test_future_weather_would_be_rejected_not_silent():
    day=date(2015,3,2)
    import pytest
    with pytest.raises(ValueError,match="later or earlier"):
        parse_power_day(synthetic_response(day,with_future=True),day)

def test_synthetic_covariates_are_not_construed_as_animal_cue_use():
    day=date(2015,3,2)
    rows=[("hash",30,23,day)]
    def weather(lat,lon,date_value):
        return parse_power_day(synthetic_response(date_value),date_value)
    r=source_meteorology_availability(rows,fetch=weather)
    assert r["selected_distinct_identity_years"]==1
    assert r["source_valid_pre_move_weather_days"]==1
    assert not r["cue_was_actually_perceived_by_bird"]
    assert not r["causal_behavior_or_fitness_effect_tested"]

def test_one_event_per_animal_year_before_weather_selection():
    t=date(2015,3,1)
    days=[(t+timedelta(days=i),lat,lon) for i,(lat,lon) in enumerate(
       [(20,10),(20.01,10.01),(20.02,10.02),
        (20.6,10.7),(21.6,11.3)])]
    groups={("Taxon","secret-id",2015):days}
    c,e,n=collect_events(groups)
    assert c==1 and n==1 and len(e)==1
    assert e[0][3]==date(2015,3,2)
    assert "secret-id" not in str(e)
