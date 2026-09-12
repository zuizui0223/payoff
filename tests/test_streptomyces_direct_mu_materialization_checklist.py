import json
from pathlib import Path

CHECKLIST = Path("validation/streptomyces_direct_mu_materialization_checklist_v1.json")
REFERENCE_STATUS = Path("validation/streptomyces_direct_mu_reference_panel_status_v1.json")
ARCH = Path("validation/architecture_mapping_status_v1.json")


def load(path):
    return json.loads(path.read_text())


def test_priorities_are_frozen_but_not_qualified():
    data = load(CHECKLIST)
    ids = [x["candidate_id"] for x in data["priority_candidates"]]
    assert ids == ["M5_T0", "M1_T0"]
    assert [x["priority_rank"] for x in data["priority_candidates"]] == [1, 2]
    for candidate in data["priority_candidates"]:
        assert candidate["current_status"] == "MATERIALIZATION_PRIORITY_NOT_QUALIFIED"
        assert all(value is False for value in candidate["qualification_requirements"].values())


def test_material_recovery_never_auto_qualifies_reference():
    data = load(CHECKLIST)
    assert data["claim_ceiling"]["qualified_reference_count"] == 0
    assert not data["claim_ceiling"]["d_band_available"]
    assert not data["claim_ceiling"]["direct_mu_outcome_available"]


def test_current_reference_panel_and_architecture_claims_remain_closed():
    panel = load(REFERENCE_STATUS)
    assert panel["qualified_reference_counts"] == {
        "ENTRY_CLASS": 0,
        "INTERMEDIATE_CLASS": 0,
        "DEEP_CLASS": 0,
    }
    assert not panel["panel_qualified"]
    assert not panel["d_band_available"]

    arch = load(ARCH)
    strep = next(x for x in arch["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")
    assert not strep["mapping_certified"]
    assert not strep["matched_generalist_shared_architecture_recovered"]


def test_materialization_sequence_ends_in_existing_qualification_gate():
    data = load(CHECKLIST)
    assert data["materialization_sequence"][-1] == "RUN_REFERENCE_PANEL_QUALIFICATION"
    assert "MEASURE_72_TO_120H_CORE_EQUIVALENT_REALIZATION" in data["materialization_sequence"]
    assert "GENOTYPE_REGISTERED_MARKERS_SCO7662_SCO7350_SCO7036_PLUS_CORE_SCO3879" in data["materialization_sequence"]
