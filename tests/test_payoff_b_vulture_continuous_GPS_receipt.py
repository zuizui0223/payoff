"""Exact archived result and biological claim boundary for fix-level vulture audit."""
import json
from pathlib import Path
def test_original_vulture_fix_level_measurement_receipt():
    p=Path("data/payoff_b_vulture_continuous_GPS_measurement_result_20261022.json")
    r=json.loads(p.read_text("utf-8"))
    d=r["original_source_receipt"]["result"]["source_event_sampling_diagnostic"]
    assert d["original_candidate_animal_years"]==18
    assert d["old_UTC_day_boundary_original_source_bracket_status_counts"]["BRACKET_WITHIN_24H"]==15
    assert d["new_raw_fix_to_fix_brackets_under_hours"]["6"]==17
    assert d["original_distinct_animal_years_with_sustained_12h_outside_evidence"]==12
    assert d["first_crossing_has_sampled_return_within12h"]==6
    assert r["actual_behavioral_departure_observed"] is False
    assert r["cue_effects_tested"] is False
