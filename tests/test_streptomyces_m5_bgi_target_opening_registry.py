import json
from pathlib import Path


PATH = Path("validation/streptomyces_m5_bgi_target_opening_v1.json")


def test_target_registry_stays_closed_before_calibration_result():
    data = json.loads(PATH.read_text())
    assert data["candidate_id"] == "M5_T0"
    assert data["target_bgi_run"] == "SRR16954696"
    assert data["target_bgi_ratios_opened"] is False
    assert data["target_opening_allowed"] is False
    assert data["claim_ceiling"]["m5_primary_bgi_class"] is None
    assert data["claim_ceiling"]["registered_deletion_class_qualified"] is False
    assert data["claim_ceiling"]["qualified_d_reference_count_increment"] == 0
    assert data["claim_ceiling"]["architecture_specific_inference_open"] is False
