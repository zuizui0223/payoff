"""Frozen source weather results are descriptive, not population hazard estimates."""
import json
from pathlib import Path
def test_riskday_weather_result_receipt():
    p=Path("data/payoff_b_complete_riskday_weather_20261022.json")
    x=json.loads(p.read_text("utf-8"))
    assert set(x["source_statistics"])=={"stork","white_fronted_goose","curlew"}
    assert x["source_group_weather_counts"]=="144/144 valid, 48/48 each system"
    for name,a in x["source_statistics"].items():
        assert a["n_cases"]==16 and a["n_stays"]==32
        assert a["no_missing_source_weather"] is True
        assert x["all_source_group_receipts"][name]["result"]["status"]=="WEATHER_DESCRIPTIVE_SOURCE_COMPLETE"
    assert x["no_hazard_model_fitted"] is True
    assert x["birds_true_perceived_cues_measured"] is False
    assert x["fitness_benefit_tested"] is False
