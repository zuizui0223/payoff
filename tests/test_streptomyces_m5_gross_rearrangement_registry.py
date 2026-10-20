import json
from pathlib import Path


PATH = Path("validation/streptomyces_m5_gross_rearrangement_audit_v1.json")


def load():
    return json.loads(PATH.read_text())


def test_gross_structure_receipt_is_prospective_and_unresolved():
    data = load()
    assert data["candidate_id"] == "M5_T0"
    assert data["public_sequence"]["target_pacbio_run"] == "SRR16954720"
    assert data["public_sequence"]["wt_control_run"] == "SRR16954715"
    assert data["resolution_contract"]["coverage_bin_bp"] == 10000
    assert data["resolution_contract"]["gross_event_min_bp"] == 50000
    assert data["current_result"]["gross_secondary_rearrangement_unresolved"] is True
    assert data["current_result"]["audit_completed"] is False
    assert data["event_catalog"] == []


def test_gross_structure_design_does_not_promote_d_reference():
    ceiling = load()["claim_ceiling"]
    assert ceiling["gross_structure_gate_closed"] is False
    assert ceiling["physical_stock_access_confirmed"] is False
    assert ceiling["realization_band_available"] is False
    assert ceiling["qualified_d_reference_count_increment"] == 0
    assert ceiling["architecture_specific_inference_open"] is False
