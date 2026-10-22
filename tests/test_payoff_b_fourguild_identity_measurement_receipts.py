"""Source-file source integrity, not ecological fitness effects."""
import json
from pathlib import Path
def test_four_original_source_fix_integrity():
    r=json.loads(Path("data/payoff_b_fourguild_fix_level_stationarity_20261022.json").read_text("utf-8"))
    assert r["totals"]["riskdays"]==7368
    assert r["totals"]["cases"]==366 and r["totals"]["stays"]==5483
    assert r["totals"]["case_any3_out"]==133
    assert r["totals"]["stay_any3_out"]==829
    assert not r["weather_effect_not_reestimated_in_this_QC"]==False
def test_stork_cohort_ids_not_unique_independence():
    r=json.loads(Path("data/payoff_b_stork_cohort_identifier_integrity_20261022.json").read_text("utf-8"))
    assert r["shared_tag_IDs"]==35
    assert r["shared_tags_with_overlapping_intervals"]==2
    assert r["identical_animal_ring_or_deployment_ID_values"]==0
    assert not r["independent_biological_cohorts_confirmed"]
