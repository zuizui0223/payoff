import json
from pathlib import Path


PRELAB = Path("validation/streptomyces_m5_prelab_evidence_v1.json")
EXECUTION = Path("validation/streptomyces_m5_first_reference_execution_v1.json")
STATUS = Path("validation/streptomyces_direct_mu_first_reference_status_v1.json")


def load(path):
    return json.loads(path.read_text())


def test_public_sequence_now_verifies_deep_class_but_not_reference_qualification():
    data = load(PRELAB)
    evidence = data["primary_source_class_evidence"]
    assert evidence["candidate_registered_class"] == "DEEP_CLASS"
    assert evidence["candidate_class_supported"] is True
    assert evidence["registered_marker_pattern_verified"] is True
    assert data["integrity_status"]["core_reference_SCO3879_dnaA_verified"] is True
    assert data["claim_ceiling"]["deep_class_candidate_supported"] is True
    assert data["claim_ceiling"]["deletion_class_qualified"] is True
    assert data["realization_status"]["qualified_reference"] is False


def test_archive_existence_does_not_equal_current_stock_access():
    data = load(PRELAB)
    provenance = data["material_provenance"]
    assert provenance["m5_t0_archived_material_existence_documented"] is True
    assert provenance["physical_stock_access_confirmed_for_current_project"] is False


def test_exact_public_mapping_and_marker_scoring_are_recovered():
    data = load(PRELAB)
    sequence = data["sequence_provenance"]
    assert sequence["public_bioproject_recovered"] == "PRJNA780771"
    assert sequence["m5_t0_whole_genome_sequenced_in_source_study"] is True
    assert sequence["exact_m5_t0_run_or_sample_accession_resolved"] is True
    assert sequence["m5_t0_pacbio_run"] == "SRR16954720"
    assert sequence["m5_t0_bgi_run"] == "SRR16954696"
    assert sequence["candidate_identity_keyed_by_exact_run_experiment_alias_not_shared_biosample"] is True
    assert sequence["registered_marker_pattern_directly_scored_from_frozen_m5_t0_sequence"] is True


def test_execution_advances_genomic_fields_but_architecture_inference_stays_closed():
    execution = load(EXECUTION)
    status = load(STATUS)
    assert execution["primary_source_class_candidate"] == "DEEP_CLASS"
    assert execution["deletion_class"] == "DEEP_CLASS"
    assert execution["marker_pattern_verified"] is True
    assert execution["core_reference_present"] is True
    assert execution["qualified_reference"] is False
    assert execution["gross_secondary_rearrangement_unresolved"] is True
    assert execution["derived_d_realization_band"] is None
    assert status["qualified_d_reference_count"] == 0
    assert status["architecture_specific_inference_hard_closed"] is True
    assert status["claim_ceiling"]["deletion_class_qualified"] is True
    assert status["claim_ceiling"]["first_qualified_d_reference_recovered"] is False
