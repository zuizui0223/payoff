"""Shared tag dataset cannot be declared independent without source identity."""
import json
from pathlib import Path

def test_published_stork_tag_overlap_unresolved():
    p=Path("data/payoff_b_stork_shared_tag_timeline_result_20261022.json")
    x=json.loads(p.read_text(encoding="utf-8"))
    s=x["source_original_identity_ledger"]["aggregate_tag_timeline"]
    assert s["original_published_shared_tag_ids"]==35
    assert s["tag_timeline_status_counts"]["tag_ids_with_any_simultaneous_deployment_interval"]==2
    assert s["tag_timeline_status_counts"]["tag_ids_missing_comparable_on_off_dates"]==33
    assert x["independent_cohort_eligible_for_main_Payoff_B_test"] is False
    assert x["raw_identifiers_dates_locations_exported"] is False
