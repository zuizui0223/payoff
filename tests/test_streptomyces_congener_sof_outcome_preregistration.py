import json
from pathlib import Path

from src.congener_sof_outcome_adjudication import (
    adjudicate_congener_sof_outcome,
    adjudicate_genotoxic_generation_branch,
)


PATH = Path("validation/streptomyces_congener_sof_outcome_preregistration_v1.json")
CANDIDATES = Path("validation/streptomyces_prodiginine_congener_sof_candidates_v1.json")
ARCH = Path("validation/architecture_mapping_status_v1.json")


def load():
    return json.loads(PATH.read_text())


def test_rule_is_frozen_but_outcomes_cannot_open_until_thresholds_are_frozen():
    data = load()
    assert data["rule_frozen_before_outcome"]
    assert not data["outcome_data_opened"]
    assert not data["numeric_thresholds_frozen"]
    assert not data["outcome_opening_allowed"]
    assert len(data["thresholds_required_before_outcome_opening"]) == 3


def test_primary_candidates_match_preoutcome_congener_registry():
    data = load()
    candidates = json.loads(CANDIDATES.read_text())
    ready = [
        row["probe_id"]
        for row in candidates["candidates"]
        if row["expected_biochemical_congener_probe_ready"]
    ]
    assert data["primary_candidate_ids"] == ready


def test_current_candidate_outcomes_recompute_to_unresolved():
    data = load()
    for row in data["current_candidate_outcomes"]:
        c2 = adjudicate_genotoxic_generation_branch(
            row["genotoxicity_result"], row["direct_mu_result"]
        )
        assert c2.branch_result == row["joint_C2_result"]
        final = adjudicate_congener_sof_outcome(row["task_result"], c2.branch_result)
        assert final.outcome_class == row["outcome_class"]
        assert not final.separation_of_function_supported


def test_nonsignificance_is_not_task_preservation_contract():
    assert not load()["task_rule"]["nonsignificance_alone_counts_as_preserved"]


def test_sof_positive_hypothetical_still_does_not_promote_architecture_or_game():
    positive = adjudicate_congener_sof_outcome(
        "preserved", "genotoxic_generation_reduced"
    )
    assert positive.separation_of_function_supported
    assert not positive.matched_s_promoted
    assert not positive.architecture_mapping_promoted
    assert not positive.generic_game_promoted
    assert not positive.eta_promoted
    assert not positive.e1_promoted


def test_current_claim_ceiling_matches_architecture_registry():
    data = load()
    arch = json.loads(ARCH.read_text())
    strep = next(x for x in arch["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")
    ceiling = data["claim_ceiling"]
    assert ceiling["separation_of_function_supported_count"] == 0
    assert ceiling["matched_generalist_shared_architecture_recovered"] is False
    assert ceiling["matched_s_certified"] is False
    assert ceiling["architecture_mapping_certified"] is False
    assert strep["matched_generalist_shared_architecture_recovered"] is False
    assert strep["matched_comparator_certified"] is False
    assert strep["mapping_certified"] is False
