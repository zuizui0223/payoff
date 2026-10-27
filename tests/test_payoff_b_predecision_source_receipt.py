"""Source-only weather availability receipt and causal-claim boundaries."""
import json
from pathlib import Path

def test_weather_source_does_not_prove_phenology_tracking():
    d=json.loads(Path("data/payoff_b_predecision_source_20261019.json").read_text())
    assert sum(x["n_candidates"] for x in d["source_transition_counts"])==310
    assert d["weather_bridge"]["selected_distinct_animal_years"]==36
    assert d["weather_bridge"]["events_with_complete_pre_move_reanalysis_weather"]==36
    assert d["weather_bridge"]["source_weather_missing"]==0
    assert not d["weather_bridge"]["weather_represents_animals_actual_forecast"]
    assert not d["scientific_verdict"]["effect_of_weather_on_departure_or_followup_measured"]
    assert not d["scientific_verdict"]["new_confirmatory_ecological_discovery"]
