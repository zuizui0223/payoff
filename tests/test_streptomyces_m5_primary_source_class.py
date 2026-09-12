import json
from pathlib import Path


CLASS_RECEIPT = Path("validation/streptomyces_m5_primary_source_class_v1.json")
CHECKLIST = Path("validation/streptomyces_direct_mu_materialization_checklist_v1.json")
PANEL = Path("validation/streptomyces_direct_mu_reference_panel_status_v1.json")
ARCH = Path("validation/architecture_mapping_status_v1.json")


def load(path):
    return json.loads(path.read_text())


def test_primary_source_supports_deep_candidate_but_not_registered_class():
    data = load(CLASS_RECEIPT)
    adjudication = data["registered_class_adjudication"]
    assert adjudication["candidate_class"] == "DEEP_CLASS"
    assert adjudication["candidate_class_supported"] is True
    assert adjudication["exact_registered_marker_pattern_verified"] is False
    assert adjudication["registered_deletion_class_qualified"] is False
    assert data["claim_ceiling"]["qualified_reference"] is False


def test_materialization_checklist_records_candidate_evidence_without_passing_any_gate():
    data = load(CHECKLIST)
    m5 = next(x for x in data["priority_candidates"] if x["candidate_id"] == "M5_T0")
    assert m5["primary_source_class_receipt"] == "STREPTOMYCES_M5_PRIMARY_SOURCE_CLASS_V1"
    assert m5["known_positive"]["primary_source_deep_class_candidate_supported"] is True
    assert m5["qualification_requirements"]["registered_marker_class_verified"] is False
    assert m5["qualification_requirements"]["entry_or_severity_class_assigned_preoutcome"] is False
    assert m5["current_status"] == "MATERIALIZATION_PRIORITY_NOT_QUALIFIED"


def test_source_class_recovery_does_not_change_reference_count_or_architecture_ceiling():
    panel = load(PANEL)
    assert sum(panel["qualified_reference_counts"].values()) == 0
    assert panel["panel_qualified"] is False
    assert panel["d_band_available"] is False

    arch = load(ARCH)
    strep = next(x for x in arch["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")
    assert strep["mapping_certified"] is False
    assert strep["matched_generalist_shared_architecture_recovered"] is False
