"""Frozen original CC0 vulture time-bracket receipt, not cue-effect proof."""
import json
from pathlib import Path
def test_new_vulture_hourly_source_receipt():
    d=json.loads(Path("data/payoff_b_new_vulture_time_brackets_20261022.json").read_text("utf-8"))
    gate=d["original_source_receipt"]["result"]["hour_bracket_source_admission"]
    assert gate["original_stationary_then_northward_candidate_events"]==30
    assert gate["first_event_per_original_bird_calendar_year"]==18
    assert gate["source_hour_bracket_outcome_counts"]["BRACKET_WITHIN_24H"]==15
    assert gate["brackets_narrower_than_h"]["6"]==0
    assert gate["fixed_future_hourly_meteorology_source_gate"]["passed"] is True
    assert d["actual_migration_choice_observed"] is False
    assert d["cue_signal_perception_measured"] is False
