"""Original NASA daily-weather source ledger validation."""
import json
from pathlib import Path
def test_all_riskday_weather_receipt():
    r=json.loads(Path("data/payoff_b_complete_riskday_daily_weather_20261022.json").read_text("utf-8"))
    assert r["totals"]["n_complete_weather"]==5509
    assert r["totals"]["n_risk_days"]==5509
    assert r["totals"]["batch_queries"]==809
    assert r["totals"]["failed_requests"]==0
    assert r["totals"]["n_matching_gridyearmonth_strata"]==176
    assert r["totals"]["n_case_days_with_gridyearmonth_stay"]==215
    assert set(r["summarized"])=={"stork","white_fronted_goose","curlew"}
    assert not r["causal_effects_or_confirmatory_pvalues_estimated"]
    assert not r["true_animal_departure_hazard_estimated"]
    assert r["full_source_results"]["stork"]["result"]["status"]=="ALL_RISKDAY_SOURCE_WEATHER_ASSOCIATION_DESCRIPTIVE_COMPLETE"
