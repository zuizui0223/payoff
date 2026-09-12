"""Qualification gate for mapping archived candidate IDs to public sequence records.

Public WGS availability is not enough to reconstruct a registered D-reference.
Each candidate must be unambiguously linked to a BioSample and one or more SRA
runs before sequence-derived marker or rearrangement evidence may be used.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SequenceSampleMapCandidate:
    candidate_id: str
    biosample_accession: str | None = None
    sra_run_accessions: tuple[str, ...] = ()
    source_metadata_names_candidate: bool = False
    mapping_independently_crosschecked: bool = False
    public_sequence_available: bool = False


@dataclass(frozen=True)
class SequenceSampleMapReceipt:
    candidate_id: str
    mapping_qualified: bool
    blockers: tuple[str, ...]
    sequence_marker_reconstruction_allowed: bool
    physical_material_identity_established: bool = False
    reference_qualified: bool = False


def qualify_sequence_sample_map(c: SequenceSampleMapCandidate) -> SequenceSampleMapReceipt:
    if not isinstance(c.candidate_id, str) or not c.candidate_id.strip():
        raise ValueError("candidate_id must be a nonempty string")

    blockers: list[str] = []
    if not c.public_sequence_available:
        blockers.append("PUBLIC_SEQUENCE_NOT_AVAILABLE")
    if not c.biosample_accession:
        blockers.append("BIOSAMPLE_ACCESSION_NOT_MAPPED")
    if not c.sra_run_accessions:
        blockers.append("SRA_RUN_ACCESSION_NOT_MAPPED")
    if not c.source_metadata_names_candidate:
        blockers.append("SOURCE_METADATA_DOES_NOT_UNAMBIGUOUSLY_NAME_CANDIDATE")
    if not c.mapping_independently_crosschecked:
        blockers.append("CANDIDATE_TO_SEQUENCE_MAPPING_NOT_INDEPENDENTLY_CROSSCHECKED")

    qualified = not blockers
    return SequenceSampleMapReceipt(
        candidate_id=c.candidate_id,
        mapping_qualified=qualified,
        blockers=tuple(blockers),
        sequence_marker_reconstruction_allowed=qualified,
    )
