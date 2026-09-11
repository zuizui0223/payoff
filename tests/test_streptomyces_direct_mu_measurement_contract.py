import json
from pathlib import Path


CONTRACT = Path("validation/streptomyces_direct_mu_measurement_contract_v1.json")
TRIANGULATION = Path("validation/streptomyces_red_triangulation_preregistration_v1.json")
ARCH = Path("validation/architecture_mapping_status_v1.json")


def load(path):
    return json.loads(path.read_text())


def test_direct_mu_contract_is_explicitly_prospective_and_preoutcome():
    data = load(CONTRACT)
    assert data["status"] == "PROSPECTIVE_PREOUTCOME_MEASUREMENT_CONTRACT"
    assert data["prospective"]
    assert not data["outcome_data_opened"]
    assert not data["direct_mu_result_available"]


def test_matched_shared_generalist_architecture_remains_unrecovered():
    data = load(CONTRACT)
    assert not data["matched_generalist_shared_architecture_recovered"]
    assert not data["matched_s_comparator_certified"]
    assert not data["architecture_mapping_certified"]
    assert not data["architecture_frequency_claim_licensed"]


def test_state_and_realization_channels_are_both_required():
    channels = load(CONTRACT)["required_measurement_channels"]
    assert channels["state_channel"]["required"]
    assert channels["state_channel"]["core_reference_required"]
    assert channels["state_channel"]["same_age_intact_baseline_dosage_calibration_required"]
    assert channels["realization_channel"]["required"]
    assert channels["realization_channel"]["must_be_separate_from_final_mutant_fraction"]


def test_primary_probes_match_frozen_triangulation_registry():
    contract = load(CONTRACT)
    triangulation = load(TRIANGULATION)
    assert contract["primary_probe_ids_frozen_before_outcome"] == triangulation["primary_probe_ids"]


def test_positive_mu_or_triangulation_cannot_auto_promote_architecture_or_game():
    flags = load(CONTRACT)["claim_separation"]
    assert flags
    assert not any(flags.values())


def test_current_architecture_registry_still_reports_no_matched_s_and_no_mapping():
    data = load(ARCH)
    row = next(x for x in data["systems"] if x["system_id"] == "STREPTOMYCES_COELICOLOR")
    assert not row["matched_generalist_only_comparator_recovered"]
    assert not row["matched_comparator_certified"]
    assert not row["mapping_certified"]


def test_nonsignificance_and_boundary_contact_are_not_promoted_to_exclusion():
    rule = load(CONTRACT)["probe_result_rule"]
    assert rule["boundary_contact"] == "unresolved"
    assert rule["nonsignificant_only"] == "unresolved"
    assert rule["material_reduction_threshold_must_be_declared_before_outcome"]
