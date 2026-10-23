"""Locked strict GPS stationary quality sensitivity receipt invariants."""
import json
from pathlib import Path
def test_strict_fix_weather_source_receipt():
    data=json.loads(Path("data/payoff_b_strict_fix_stationary_weather_verdict_20261022.json").read_text("utf-8"))
    assert data["classification"]=="POST_OUTCOME_OBSERVATIONAL_MEASUREMENT_SENSITIVITY_ONLY"
    a=data["interpretive_statistics"]
    assert a["egyptian_vulture"]["weather_queries"]==0
    assert a["stork"]["strict_3day_original_case_count"]==85
    assert a["white_fronted_goose"]["strict_3day_original_case_count"]==93
    assert a["curlew"]["strict_3day_original_case_count"]==42
    assert a["stork"]["physical_weather_case_minus_stay"]["ALLSKY_SFC_SW_DWN_anomaly"]<0
    assert a["white_fronted_goose"]["physical_weather_case_minus_stay"]["WS10M_anomaly"]<0
    assert a["curlew"]["physical_weather_case_minus_stay"]["T2M_anomaly"]<0
    assert not data["claim_boundaries"]["no_new_confirmatory_Payoff_B_information_x_actionability"]==False
    assert data["claim_boundaries"]["prior_V7R_V8_and_stork53_non_support_unchanged"]
