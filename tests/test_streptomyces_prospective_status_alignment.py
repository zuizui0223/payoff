import json
from pathlib import Path


ARCH = Path("validation/architecture_mapping_status_v1.json")
TRI = Path("validation/streptomyces_red_triangulation_preregistration_v1.json")
MU = Path("validation/streptomyces_direct_mu_measurement_contract_v1.json")


def load(path):
    return json.loads(path.read_text())


def streptomyces_arch_row():
    data = load(ARCH)
    return next(row for row in data["systems"] if row["system_id"] == "STREPTOMYCES_COELICOLOR")


def test_three_surfaces_agree_matched_generalist_shared_architecture_is_not_recovered():
    arch = streptomyces_arch_row()
    tri = load(TRI)
    mu = load(MU)
    assert not arch["matched_generalist_shared_architecture_recovered"]
    assert not tri["matched_generalist_shared_architecture_recovered"]
    assert not mu["matched_generalist_shared_architecture_recovered"]
    assert not arch["matched_comparator_certified"]
    assert not tri["matched_s_comparator_certified"]
    assert not mu["matched_s_comparator_certified"]


def test_triangulation_is_frozen_preoutcome_but_still_prospective():
    arch = streptomyces_arch_row()
    tri = load(TRI)
    mu = load(MU)
    assert arch["two_probe_triangulation_frozen_preoutcome"]
    assert arch["two_probe_triangulation_prospective"]
    assert tri["outcome_frozen_before_direct_mu_data"]
    assert tri["prospective"]
    assert mu["prospective"]
    assert not tri["outcome_data_opened"]
    assert not mu["outcome_data_opened"]
    assert not arch["two_probe_direct_mu_outcome_available"]
    assert not mu["direct_mu_result_available"]


def test_freeze_never_implies_empirical_architecture_confirmation():
    arch = streptomyces_arch_row()
    tri = load(TRI)
    mu = load(MU)
    assert not arch["mapping_certified"]
    assert not tri["architecture_mapping_certified"]
    assert not mu["architecture_mapping_certified"]
    assert not mu["architecture_frequency_claim_licensed"]
    assert not tri["architecture_mapping_promotion_allowed_from_triangulation_alone"]
    assert not tri["architecture_frequency_promotion_allowed_from_triangulation_alone"]


def test_direct_mu_contract_is_linked_without_promoting_status():
    arch = streptomyces_arch_row()
    tri = load(TRI)
    assert arch["direct_mu_measurement_contract"] == "STREPTOMYCES_DIRECT_MU_MEASUREMENT_CONTRACT_V1"
    assert tri["direct_mu_measurement_contract"] == "STREPTOMYCES_DIRECT_MU_MEASUREMENT_CONTRACT_V1"
    assert "DIRECT_MU_OUTCOME_NOT_YET_AVAILABLE" in arch["primary_blockers"]
