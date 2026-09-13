import json
from pathlib import Path


PATH = Path("validation/streptomyces_m5_gross_structure_status_v2.json")


def test_terminal_losses_are_source_resolved_but_r2_remains_open():
    data = json.loads(PATH.read_text())
    src = data["preexisting_source_record"]
    assert src["m5_t0_left_terminal_deletion_bp"] == 372936
    assert src["m5_t0_right_terminal_deletion_bp"] == 864624
    assert src["m5_t0_total_terminal_deletion_bp"] == 1237560
    assert src["m5_transfer25_additional_left_deletion_bp"] == 0
    assert src["m5_transfer25_additional_right_deletion_bp"] == 0

    adj = data["adjudication"]
    assert adj["terminal_deletion_sizes_resolved_from_preexisting_source_data"] is True
    assert adj["gross_secondary_rearrangement_unresolved"] is True
    assert adj["r2_closed"] is False
    assert set(adj["blockers"]) == {
        "LEFT_ASSOCIATED_BND_STRUCTURAL_INTERPRETATION_OPEN",
        "RIGHT_ASSOCIATED_BND_STRUCTURAL_INTERPRETATION_OPEN",
    }

    ceiling = data["claim_boundary"]
    assert ceiling["r2_gross_structure_resolved"] is False
    assert ceiling["qualified_d_reference"] is False
    assert ceiling["qualified_d_reference_count_increment"] == 0
    assert ceiling["architecture_specific_inference_open"] is False


def test_m5_informed_terminal_threshold_rescue_is_forbidden():
    data = json.loads(PATH.read_text())
    assert "DO_NOT_TUNE" in data["forbidden_recovery_route"]
    assert len(data["permitted_recovery_routes"]) == 2
