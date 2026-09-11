import json
from pathlib import Path


ARCH = Path("validation/architecture_mapping_status_v1.json")
TASK = Path("validation/streptomyces_red_mediator_task_entanglement_v1.json")


def load(path):
    return json.loads(path.read_text())


def test_red_task_match_receipt_and_architecture_registry_share_same_claim_ceiling():
    arch = load(ARCH)
    row = next(x for x in arch["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")
    task = load(TASK)

    assert task["system_id"] == row["system_id"]
    assert task["prospective"]
    assert task["expected"]["mediator_task_entangled"]
    assert not task["expected"]["task_match_qualified"]
    assert not task["matched_generalist_shared_architecture_recovered"]
    assert not row["matched_generalist_shared_architecture_recovered"]
    assert not task["matched_s_promotion_licensed"]
    assert not row["matched_s_promotion_licensed"]
    assert not task["architecture_mapping_certified"]
    assert not row["mapping_certified"]


def test_task_subgate_never_changes_generic_game_or_e1_status():
    task = load(TASK)
    assert not task["expected"]["generic_game_promoted"]
    assert not task["expected"]["eta_identified"]
    assert not task["expected"]["e1_promoted"]
    assert not task["architecture_frequency_feedback_identified"]
