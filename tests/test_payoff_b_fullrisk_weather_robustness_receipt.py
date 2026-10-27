"""Source-backed post-outcome robustness receipt invariants."""
import json
from pathlib import Path
def test_fullrisk_weather_robustness_receipt():
    d=json.loads(Path("data/payoff_b_fullrisk_weather_robustness_20261022.json").read_text("utf-8"))
    assert d["status"]=="POST_OUTCOME_EXPLORATORY_ROBUSTNESS_NOT_CONFIRMATORY"
    assert set(d["per_system"])=={"stork","white_fronted_goose","curlew"}
    assert all(r["bootstrap_valid"]==1000 for r in d["per_system"].values())
    stork=d["per_system"]["stork"]
    goose=d["per_system"]["white_fronted_goose"]
    assert stork["effects"]["ALLSKY_SFC_SW_DWN_anomaly"]<0
    assert goose["effects"]["T2M_anomaly"]>0
    assert d["inferential_ceiling"]["shared_spatial_weather_dependence_controlled"] is False
    assert d["inferential_ceiling"]["causal_migration_effect_identified"] is False
