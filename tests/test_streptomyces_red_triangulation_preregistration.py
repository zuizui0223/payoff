import json
from pathlib import Path

from src.mechanism_probe_triangulation import (
    MechanismProbeOutcome,
    adjudicate_two_probe_triangulation,
)


REGISTRY = Path("validation/streptomyces_red_triangulation_preregistration_v1.json")


def test_current_preregistered_state_recomputes_as_unresolved():
    data = json.loads(REGISTRY.read_text())
    outcomes = tuple(MechanismProbeOutcome(**row) for row in data["current_outcomes"])
    result = adjudicate_two_probe_triangulation(
        outcomes,
        primary_probe_ids=tuple(data["primary_probe_ids"]),
    )
    assert result.status == data["expected_current_status"]
    assert result.status == "INCOMPLETE_OR_UNRESOLVED_TRIANGULATION"
    assert result.unresolved_probe_count == 2
    assert not result.mediator_generation_effect_triangulated
    assert not result.registered_route_not_supported


def test_primary_probe_set_is_frozen_and_secondary_candidate_cannot_replace_it():
    data = json.loads(REGISTRY.read_text())
    assert data["primary_probe_ids"] == [
        "M1141_VS_M1142_RED_CLUSTER_DIFFERENCE",
        "M145_VS_redU_SINGLE_MUTANT",
    ]
    secondary_ids = {
        row["probe_id"] for row in data["secondary_probe_candidates_not_allowed_to_replace_primary_posthoc"]
    }
    assert "redJ_DELETION_COMPLEMENTATION_SERIES" in secondary_ids
    assert not secondary_ids.intersection(data["primary_probe_ids"])


def test_triangulation_cannot_promote_matched_s_game_or_e1():
    data = json.loads(REGISTRY.read_text())
    assert not data["matched_s_promotion_allowed_from_triangulation_alone"]
    assert not data["generic_game_promotion_allowed_from_triangulation_alone"]
    assert not data["architecture_frequency_promotion_allowed_from_triangulation_alone"]
