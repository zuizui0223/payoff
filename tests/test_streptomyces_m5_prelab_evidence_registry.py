import json
from pathlib import Path


PRELAB = Path("validation/streptomyces_m5_prelab_evidence_v1.json")
EXECUTION = Path("validation/streptomyces_m5_first_reference_execution_v1.json")
STATUS = Path("validation/streptomyces_direct_mu_first_reference_status_v1.json")


def load(path):
    return json.loads(path.read_text())


def test_primary_source_recovery_supports_candidate_but_not_class_qualification():
    data = load(PRELAB)
    evidence = data["primary_source_class_evidence"]
    assert evidence["candidate_registered_class"] == "DEEP_CLASS"
    assert evidence["candidate_class_supported"] is True
    assert evidence["registered_marker_pattern_verified"] is False
    assert data["claim_ceiling"]["deep_class_candidate_supported"] is True
    assert data["claim_ceiling"]["deletion_class_qualified"] is False


def test_archive_existence_does_not_equal_current_stock_access():
    data = load(PRELAB)
    provenance = data["material_provenance"]
    assert provenance["m5_t0_archived_material_existence_documented"] is True
    assert provenance["physical_stock_access_confirmed_for_current_project"] is False


def test_public_bioproject_does_not_equal_exact_m5_sequence_mapping():
    data = load(PRELAB)
    sequence = data["sequence_provenance"]
    assert sequence["public_bioproject_recovered"] == "PRJNA780771"
    assert sequence["m5_t0_whole_genome_sequenced_in_source_study"] is True
    assert sequence["exact_m5_t0_run_or_sample_accession_resolved"] is False
    assert sequence["registered_marker_pattern_directly_scored_from_frozen_m5_t0_sequence"] is False


def test_execution_and_status_remain_hard_closed():
    execution = load(EXECUTION)
    status = load(STATUS)
    assert execution["primary_source_class_candidate"] == "DEEP_CLASS"
    assert execution["deletion_class"] == "NOT_YET_VERIFIED"
    assert execution["marker_pattern_verified"] is False
    assert execution["qualified_reference"] is False
    assert status["qualified_d_reference_count"] == 0
    assert status["architecture_specific_inference_hard_closed"] is True
    assert status["claim_ceiling"]["deletion_class_qualified"] is False
