import json
from pathlib import Path


PATH = Path("validation/streptomyces_m5_bgi_target_opening_v1.json")


def test_target_registry_freezes_consumed_opening_and_unresolved_primary_class():
    data = json.loads(PATH.read_text())
    assert data["candidate_id"] == "M5_T0"
    assert data["target_bgi_run"] == "SRR16954696"
    assert data["status"] == "TARGET_OPENED_RESULT_FROZEN"
    assert data["required_calibration_receipt"] == "STREPTOMYCES_M5_BGI_RESPONSE_BLIND_CALIBRATION_RESULT_V1"
    assert data["target_result_receipt"] == "STREPTOMYCES_M5_BGI_TARGET_RESULT_V1"
    assert data["frozen_calibration"]["calibration_qualified"] is True
    assert data["frozen_calibration"]["target_used_in_calibration"] is False
    assert data["target_bgi_ratios_opened"] is True
    assert data["target_opening_allowed"] is False
    assert data["opening_license_consumed"] is True
    assert data["current_blocker"] == "PRIMARY_BGI_MARKER_PATTERN_UNRESOLVED"
    ceiling = data["claim_ceiling"]
    assert ceiling["m5_primary_bgi_class"] is None
    assert ceiling["sco7662_state"] == "ABSENT"
    assert ceiling["sco7350_state"] == "ABSENT"
    assert ceiling["sco7036_state"] == "UNRESOLVED"
    assert ceiling["sco3879_state"] == "PRESENT"
    assert ceiling["registered_deletion_class_qualified"] is False
    assert ceiling["r2_gross_structure_resolved"] is False
    assert ceiling["qualified_d_reference_count_increment"] == 0
    assert ceiling["architecture_specific_inference_open"] is False
