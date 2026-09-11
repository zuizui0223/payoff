import json
from pathlib import Path


POOL = Path("validation/streptomyces_direct_mu_literature_candidate_pool_v1.json")
REFERENCE_STATUS = Path("validation/streptomyces_direct_mu_reference_panel_status_v1.json")
ARCH = Path("validation/architecture_mapping_status_v1.json")


def load(path):
    return json.loads(path.read_text())


def test_candidate_pool_recovery_does_not_create_qualified_references():
    data = load(POOL)
    assert data["adjudication"]["literature_candidate_pool_recovered"]
    assert data["adjudication"]["named_candidate_materials_recovered"]
    assert data["adjudication"]["qualified_reference_count"] == 0
    assert data["adjudication"]["entry_class_qualified_count"] == 0
    assert data["adjudication"]["intermediate_class_qualified_count"] == 0
    assert data["adjudication"]["deep_class_qualified_count"] == 0
    assert not data["adjudication"]["reference_panel_ready"]


def test_current_reference_panel_status_stays_empty_and_unqualified():
    data = load(REFERENCE_STATUS)
    assert data["current_panel"]["candidate_count"] == 0
    assert data["current_panel"]["qualified_count"] == 0
    assert not data["current_panel"]["panel_materialized"]
    assert not data["current_panel"]["panel_qualified"]
    assert not data["current_panel"]["d_band_available"]


def test_candidate_pool_does_not_promote_architecture_claims():
    pool = load(POOL)
    for key, value in pool["claim_ceiling"].items():
        assert value is False, key
    arch = load(ARCH)
    strep = next(x for x in arch["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")
    assert not strep["architecture_mapping_certified"]
