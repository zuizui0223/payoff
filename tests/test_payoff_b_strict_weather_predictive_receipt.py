"""Frozen source predictive result has no ecological causal-success promotion."""
import json
from pathlib import Path

def test_source_predictive_value_is_real_heldout_and_not_causal():
    path=Path("data/payoff_b_strict_weather_heldout_predictive_result_20261022.json")
    data=json.loads(path.read_text("utf-8"))
    assert data["full_original_source_strict_case_stay_days"]==3845
    assert data["source_days_evaluated_in_heldout_year_folds"]==3834
    assert data["cross_species_heldout_year_log_loss_skill_positive_count"]==0
    assert set(data["per_source"])=={"stork","white_fronted_goose","curlew"}
    for record in data["per_source"].values():
        assert record["heldout_year"]["status"]=="OUT_OF_FOLD_OBSERVATIONAL_PREDICTION_ESTIMABLE"
        assert record["heldout_year"]["incremental_lag_weather_log_loss_gain"]<0
        assert record["weather_complete_source_days"]==record["total_strict_source_case_or_stay_days"]
    assert data["direct_control_capacity_or_fitness_measured"] is False
    assert data["actual_stopover_departure_choice_measured"] is False
