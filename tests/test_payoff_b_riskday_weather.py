"""Synthetic source selection tests and strict pre-decision weather chronology."""
from datetime import date,timedelta
from scripts.audit_payoff_b_riskday_weather import sample_riskdays,sample_info,summarize
from scripts.audit_payoff_b_paired_weather import source_query

def example(label,name,d):
    return (("taxon",name,2019),d,(35,13),label)

def test_fixed_selection_balances_status_without_weather():
    start=date(2019,3,1)
    raw=[example(status,f"id{i}_{status}",start+timedelta(days=i%20))
         for i in range(44)
         for status in ("NORTHWARD_CANDIDATE","STAYED_TWO_DAYS")]
    a=sample_riskdays(raw)
    b=sample_riskdays(raw)
    assert a==b
    info=sample_info(a)
    assert info["selected_riskday_outcomes"]=={
        "NORTHWARD_CANDIDATE":16,"STAYED_TWO_DAYS":32}
    assert not info["selection_uses_weather"]

def test_future_day_weather_is_not_loaded():
    url,start,day=source_query((35.1,12.6),date(2019,3,17))
    assert day==date(2019,3,16)
    assert start==date(2019,3,9)
    assert "latitude=35.0" in url

def test_aggregated_weather_not_animal_output():
    x=example("NORTHWARD_CANDIDATE","hiddenx",date(2019,3,16))
    y=example("STAYED_TWO_DAYS","hiddeny",date(2019,3,17))
    k=source_query(x[2],x[1])[0]
    j=source_query(y[2],y[1])[0]
    def val(d):
        return {"T2M":{"predecision_anomaly":d,"last_predecision_day":d+10},
                "WS10M":{"predecision_anomaly":d/2,
                         "last_predecision_day":d+2}}
    result=summarize([("x",*x),("y",*y)],{k:val(2),j:val(-1)})
    assert result["complete_weather_by_outcome"]["NORTHWARD_CANDIDATE"]["temperature_anomaly_c"]["mean"]==2
    assert result["complete_weather_by_outcome"]["STAYED_TWO_DAYS"]["temperature_anomaly_c"]["mean"]==-1
    assert "hiddenx" not in str(result)
    assert not result["modelled_true_migration_hazard"]
