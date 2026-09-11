import json
from pathlib import Path


CONGENER = Path("validation/streptomyces_prodiginine_congener_sof_candidates_v1.json")
TASK = Path("validation/streptomyces_red_mediator_task_entanglement_v1.json")
ARCH = Path("validation/architecture_mapping_status_v1.json")


def test_congener_candidates_do_not_override_current_task_or_architecture_ceiling():
    congener = json.loads(CONGENER.read_text())
    task = json.loads(TASK.read_text())
    arch = json.loads(ARCH.read_text())
    strep = next(x for x in arch["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")

    assert congener["current_summary"]["biochemical_congener_probe_ready_count"] == 2
    assert congener["current_summary"]["separation_of_function_certified_count"] == 0

    assert task["expected"]["separation_of_function_qualified"] is False
    assert task["expected"]["task_match_qualified"] is False
    assert task["matched_generalist_shared_architecture_recovered"] is False
    assert task["matched_s_promotion_licensed"] is False

    assert strep["matched_generalist_shared_architecture_recovered"] is False
    assert strep["matched_comparator_certified"] is False
    assert strep["mapping_certified"] is False
    assert arch["any_mapping_certified"] is False


def test_congener_candidate_lane_has_no_game_promotion_path():
    summary = json.loads(CONGENER.read_text())["current_summary"]
    assert summary["generic_game_promoted"] is False
    assert summary["eta_promoted"] is False
    assert summary["e1_promoted"] is False
