import json
from pathlib import Path

from src.mediator_task_entanglement import (
    MediatorTaskEntanglementReceipt,
    adjudicate_mediator_task_entanglement,
)


PATH = Path("validation/streptomyces_red_mediator_task_entanglement_v1.json")


def load_data():
    return json.loads(PATH.read_text())


def test_current_red_probe_task_match_recomputes_as_blocked():
    data = load_data()
    result = adjudicate_mediator_task_entanglement(
        MediatorTaskEntanglementReceipt(
            system_id=data["system_id"],
            mediator_id=data["mediator_id"],
            perturbation_id=data["perturbation_id"],
            focal_task_id=data["focal_task_id"],
            support_reference=data["support_reference"],
            **data["inputs"],
        )
    )
    for key, expected in data["expected"].items():
        assert getattr(result, key) == expected
    assert set(result.blockers) == set(data["current_blockers"])


def test_current_red_program_is_prospective_and_not_matched_s():
    data = load_data()
    assert data["prospective"]
    assert not data["direct_mu_outcome_available"]
    assert not data["matched_generalist_shared_architecture_recovered"]
    assert not data["matched_s_promotion_licensed"]
    assert not data["architecture_mapping_certified"]
    assert not data["architecture_frequency_feedback_identified"]


def test_same_mediator_addback_is_explicitly_not_the_registered_shortcut():
    data = load_data()
    assert "SAME_RED_PRODIGININE_ADDBACK" in data["inadmissible_shortcut"]
    assert "ORTHOGONAL_TASK_RESCUE_INDEPENDENT_OF_GENERATION_PATH" in data["admissible_future_routes"]
