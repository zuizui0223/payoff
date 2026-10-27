"""Frozen directional source weather ledger is not a positive causal claim."""
import json
from pathlib import Path
def test_source_directional_weather_receipt():
    p=Path("data/payoff_b_directional_riskset_weather_result_20261022.json")
    d=json.loads(p.read_text("utf-8"))
    assert d["completed_weather_days"]==144
    assert set(d["by_system"])=={"stork","white_fronted_goose","curlew"}
    assert d["by_system"]["stork"]["northwind_10m_anomaly_case_minus_stay_m_s"]<0
    assert d["by_system"]["white_fronted_goose"]["northwind_10m_anomaly_case_minus_stay_m_s"]>0
    assert not d["true_route_relative_tailwind"]
    assert not d["signed_timing_action_or_fitness_tested"]
    assert d["classification"].endswith("NO_CUE_USE_CAUSAL_IDENTIFICATION")
