"""Verify newly opened CC0 source feasibility verdict, not ecological effects."""
import json
from pathlib import Path
def test_newly_opened_movebank_source_gate():
    d=json.loads(Path("data/payoff_b_unopened_CC0_source_gate_20261022.json").read_text("utf-8"))
    assert d["admission"]["pinkfoot_goose"].startswith("SOURCE_THRESHOLD_FAILED")
    assert d["admission"]["egyptian_vulture"].startswith("GEOMETRY_ELIGIBLE")
    p=d["systems"]["pinkfoot_goose"]["result"]
    v=d["systems"]["egyptian_vulture"]["result"]
    assert p["biological_source_readiness"].startswith("NOT_ADMITTED")
    assert v["biological_source_readiness"]=="CANDIDATE_STAGEWISE_MIGRATION_SOURCE_GEOMETRY"
    assert v["fixed_feb_may_3day_stationary_then_2day_north_source_gate"]["total_candidate_events"]==30
    assert not v["actual_bird_departure_timestamp_verified"]
