"""Source-receipt and failure-mode tests for PAYOFF-B empirical audit."""
import copy
import json

import pytest

from scripts.audit_payoff_b_empirical_forecast_gate_20261114 import SOURCE, audit


def source():
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def test_reconcile_original_public_source_receipt():
    result = audit(source())
    assert result["taxon_count"] == 3
    assert result["year_test_days_total"] == 3834
    assert result["positive_year_logloss_gain_taxa"] == 0
    assert result["positive_animal_logloss_gain_taxa"] == 2
    assert result["split_sign_disagreement_taxa"] == 2
    assert result["equal_taxon_mean_year_logloss_gain"] == pytest.approx(
        (-0.002651019071237326 - 0.01738244812780132 - 0.000020604115910760612) / 3
    )
    assert result["day_weighted_descriptive_year_logloss_gain"] < 0
    assert not result["information_capacity_coordination_decomposition_identified"]


@pytest.mark.parametrize("mutation", [
    lambda s: s.update(schema="unverified"),
    lambda s: s.update(predictor_uses_future_GPS_or_weather=True),
    lambda s: s.update(direct_control_capacity_or_fitness_measured=True),
    lambda s: s["per_source"]["stork"]["heldout_year"].update(split_scheme="whole_animal"),
    lambda s: s["per_source"]["curlew"]["heldout_year"].update(heldout_original_source_days=100),
    lambda s: s["per_source"]["stork"]["heldout_year"].update(incremental_lag_weather_log_loss_gain=1.0),
    lambda s: s["per_source"]["stork"]["heldout_year"].update(heldout_original_source_cases=10),
    lambda s: s["per_source"].pop("curlew"),
])
def test_changed_source_fails_closed(mutation):
    s = copy.deepcopy(source())
    mutation(s)
    with pytest.raises(ValueError):
        audit(s)
