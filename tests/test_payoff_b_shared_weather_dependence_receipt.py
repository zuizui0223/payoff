"""Published CC0 shared-weather block receipt supports only exploratory claims."""
import json
from pathlib import Path

def test_shared_weather_receipt_and_effect_boundaries():
    f=Path("data/payoff_b_shared_weather_dependence_result_20261022.json")
    r=json.loads(f.read_text("utf-8"))
    assert r["scientific_status"]=="POST_OUTCOME_EXPLORATORY_SOURCE_SENSITIVITY_NOT_CAUSAL"
    assert set(r["results"])=={"stork","white_fronted_goose","curlew"}
    for source in r["results"].values():
        assert source["weather_blocks"]["weather_episode_year_month"]["bootstrap_replicates_completed"]==3000
        assert source["within_same_bird"]["private_grid_ids_or_individual_ids_exported"] is False
    def ci(name,var):
        return r["results"][name]["weather_blocks"]["weather_episode_year_month"]["contrast_intervals"][var]
    assert ci("stork","ALLSKY_SFC_SW_DWN_anomaly")[1]<0
    assert ci("white_fronted_goose","T2M_anomaly")[0]<0<ci("white_fronted_goose","T2M_anomaly")[1]
    assert ci("curlew","T2M_anomaly")[0]<0<ci("curlew","T2M_anomaly")[1]
    assert r["old_preregistered_verdicts_unchanged"] is True
