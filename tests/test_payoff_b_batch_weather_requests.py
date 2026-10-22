"""Original source weather-batching cost without exposing cell locations."""
from datetime import date,timedelta
from scripts.plan_payoff_b_batch_weather_requests import plan_batch_queries

def test_aggregate_grid_batch_cost_and_case_control_overlap():
    day=date(2017,3,12)
    rows=[
      (("Bird","hiddenA",2017),day,(45.2,12.2),"NORTHWARD_CANDIDATE"),
      (("Bird","hiddenB",2017),day+timedelta(days=1),(45.15,12.16),"STAYED_TWO_DAYS"),
      (("Bird","hiddenC",2017),day+timedelta(days=2),(49.1,12.5),"STAYED_TWO_DAYS"),
    ]
    out=plan_batch_queries(rows)
    assert out["at_risk_source_days"]==3
    assert out["unique_grid_calendar_months"]==2
    assert out["grid_months_with_both_northward_and_stay_observations"]==1
    assert out["northward_case_days_in_overlap_gridmonths"]==1
    assert "hiddenA" not in str(out)
    assert "45.0" not in str(out)
    assert not out["independence_of_weather_grid_months"]
