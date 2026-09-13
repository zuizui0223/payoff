import json
from pathlib import Path


PATH = Path("validation/streptomyces_m5_bgi_target_opening_v1.json")


def test_target_registry_is_licensed_but_unopened_after_calibration():
    data = json.loads(PATH.read_text())
    assert data["candidate_id"] == "M5_T0"
    assert data["target_bgi_run"] == "SRR16954696"
    assert data["status"] == "OPENING_LICENSED_TARGET_UNOPENED"
    assert data["required_calibration_receipt"] == "STREPTOMYCES_M5_BGI_RESPONSE_BLIND_CALIBRATION_RESULT_V1"
    assert data["frozen_calibration"]["calibration_qualified"] is True
    assert data["frozen_calibration"]["target_used_in_calibration"] is False
    assert data["frozen_calibration"]["absence_max_ratio"] < data["frozen_calibration"]["presence_min_ratio"]
    assert data["target_bgi_ratios_opened"] is False
    assert data["target_opening_allowed"] is True
    assert data["claim_ceiling"]["m5_primary_bgi_class"] is None
    assert data["claim_ceiling"]["registered_deletion_class_qualified"] is False
    assert data["claim_ceiling"]["r2_gross_structure_resolved"] is False
    assert data["claim_ceiling"]["qualified_d_reference_count_increment"] == 0
    assert data["claim_ceiling"]["architecture_specific_inference_open"] is False
