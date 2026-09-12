import json
from pathlib import Path


ARCH = Path("validation/architecture_mapping_status_v1.json")
PROMO = Path("validation/streptomyces_mechanism_to_architecture_promotion_v1.json")
FIRST_REF = Path("validation/streptomyces_direct_mu_first_reference_status_v1.json")


def load(path):
    return json.loads(path.read_text())


def test_architecture_registry_links_blocked_promotion_receipt():
    arch = load(ARCH)
    row = next(x for x in arch["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")
    promo = load(PROMO)
    assert row["mechanism_to_architecture_promotion_receipt"] == promo["receipt_id"]
    assert not row["task_matched_architecture_counterfactual_recovered"]
    assert not row["matched_s_promotion_licensed"]
    assert not row["mapping_certified"]
    assert "TASK_MATCHED_ARCHITECTURE_COUNTERFACTUAL_NOT_RECOVERED" in row["primary_blockers"]


def test_prospective_mechanism_program_does_not_remove_matched_s_blocker():
    arch = load(ARCH)
    row = next(x for x in arch["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")
    assert row["two_probe_triangulation_prospective"]
    assert not row["two_probe_direct_mu_outcome_available"]
    assert not row["matched_generalist_shared_architecture_recovered"]
    assert "MATCHED_GENERALIST_SHARED_ARCHITECTURE_NOT_RECOVERED" in row["primary_blockers"]


def test_zero_qualified_d_reference_is_explicit_architecture_mapping_hard_stop():
    arch = load(ARCH)
    row = next(x for x in arch["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")
    first = load(FIRST_REF)
    assert row["direct_mu_first_reference_receipt"] == first["receipt_id"]
    assert row["qualified_direct_mu_matched_d_reference_count"] == 0
    assert row["qualified_direct_mu_matched_d_reference_count"] == first["qualified_d_reference_count"]
    assert not row["direct_mu_matched_d_reference_precondition_satisfied"]
    assert row["architecture_specific_inference_hard_closed"]
    assert "ZERO_QUALIFIED_DIRECT_MU_MATCHED_D_REFERENCE" in row["primary_blockers"]
