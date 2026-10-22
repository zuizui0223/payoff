"""Frozen full-coverage totals are factual, not ecological effect tests."""
import json
from pathlib import Path

def test_complete_stationary_riskset_source_receipt():
    p=Path("data/payoff_b_complete_stationary_riskset_20261022.json")
    obj=json.loads(p.read_text(encoding="utf-8"))
    total=obj["totals"]
    assert len(obj["three_species_source_systems"])==3
    assert total["stationary_anchor_risk_days"]==5509
    assert sum(total[x] for x in (
      "raw_northward_candidate_days","staying_two_followup_days",
      "other_movement","missing_two_day_followup_censored"))==5509
    assert total["frozen_seven_day_deduplicated_case_events"]==310
    assert total["source_animal_years_with_eligible_anchor"]==184
    assert obj["inferential_state"]=="NOT_TESTED"
    for src in obj["three_species_source_systems"].values():
        assert src["status"]=="COMPLETE_STATIONARY_RISKSET_VERIFIED"
        assert src["coverage"]["risk_entry_uses_future_information"] is False
        assert src["coverage"]["censored_cases_labeled_stay"] is False
