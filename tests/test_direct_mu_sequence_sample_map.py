import pytest

from src.direct_mu_sequence_sample_map import (
    SequenceSampleMapCandidate,
    qualify_sequence_sample_map,
)


def test_public_bioproject_without_candidate_mapping_does_not_qualify():
    receipt = qualify_sequence_sample_map(
        SequenceSampleMapCandidate(
            candidate_id="M5_T0",
            public_sequence_available=True,
        )
    )
    assert not receipt.mapping_qualified
    assert not receipt.sequence_marker_reconstruction_allowed
    assert "BIOSAMPLE_ACCESSION_NOT_MAPPED" in receipt.blockers
    assert "SRA_RUN_ACCESSION_NOT_MAPPED" in receipt.blockers
    assert "SOURCE_METADATA_DOES_NOT_UNAMBIGUOUSLY_NAME_CANDIDATE" in receipt.blockers
    assert "CANDIDATE_TO_SEQUENCE_MAPPING_NOT_INDEPENDENTLY_CROSSCHECKED" in receipt.blockers
    assert not receipt.physical_material_identity_established
    assert not receipt.reference_qualified


def test_complete_mapping_only_unlocks_sequence_reconstruction():
    receipt = qualify_sequence_sample_map(
        SequenceSampleMapCandidate(
            candidate_id="M5_T0",
            biosample_accession="SAMN_TEST",
            sra_run_accessions=("SRR_TEST",),
            source_metadata_names_candidate=True,
            mapping_independently_crosschecked=True,
            public_sequence_available=True,
        )
    )
    assert receipt.mapping_qualified
    assert receipt.sequence_marker_reconstruction_allowed
    assert receipt.blockers == ()
    assert not receipt.physical_material_identity_established
    assert not receipt.reference_qualified


def test_sequence_mapping_never_substitutes_for_physical_reference_qualification():
    receipt = qualify_sequence_sample_map(
        SequenceSampleMapCandidate(
            candidate_id="M1_T0",
            biosample_accession="SAMN_TEST2",
            sra_run_accessions=("SRR_TEST2", "SRR_TEST3"),
            source_metadata_names_candidate=True,
            mapping_independently_crosschecked=True,
            public_sequence_available=True,
        )
    )
    assert receipt.mapping_qualified
    assert not receipt.physical_material_identity_established
    assert not receipt.reference_qualified


def test_missing_public_sequence_is_a_distinct_blocker():
    receipt = qualify_sequence_sample_map(
        SequenceSampleMapCandidate(candidate_id="M1_T0")
    )
    assert "PUBLIC_SEQUENCE_NOT_AVAILABLE" in receipt.blockers


@pytest.mark.parametrize("candidate_id", ["", "   ", None, 1])
def test_invalid_candidate_id_rejected(candidate_id):
    with pytest.raises(ValueError):
        qualify_sequence_sample_map(SequenceSampleMapCandidate(candidate_id=candidate_id))
