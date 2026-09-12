"""Fail-closed adjudication for M5_T0 pre-lab evidence.

Primary-source evidence may support a deletion-class *candidate* without
silently satisfying the registered direct-mu D-reference qualification gate.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class M5PrelabEvidence:
    archived_material_existence_documented: bool
    physical_stock_access_confirmed: bool
    t0_whole_genome_sequenced: bool
    public_sequence_project_recovered: bool
    exact_t0_sequence_accession_resolved: bool
    chloramphenicol_marker_support: bool
    arginine_auxotrophy_marker_support: bool
    terminal_deletion_context_reported: bool
    direct_registered_marker_pattern_verified: bool
    core_reference_verified: bool
    gross_secondary_rearrangement_resolved: bool
    realization_band_available: bool

    @property
    def deep_class_candidate_supported(self) -> bool:
        return all(
            (
                self.chloramphenicol_marker_support,
                self.arginine_auxotrophy_marker_support,
                self.terminal_deletion_context_reported,
            )
        )

    @property
    def deletion_class_qualified(self) -> bool:
        # Primary phenotype can nominate DEEP_CLASS, but the registered class
        # is not qualified until the exact marker pattern is scored directly.
        return self.deep_class_candidate_supported and self.direct_registered_marker_pattern_verified

    @property
    def prelab_material_ready(self) -> bool:
        return all(
            (
                self.archived_material_existence_documented,
                self.physical_stock_access_confirmed,
                self.t0_whole_genome_sequenced,
                self.public_sequence_project_recovered,
                self.exact_t0_sequence_accession_resolved,
                self.deletion_class_qualified,
                self.core_reference_verified,
                self.gross_secondary_rearrangement_resolved,
            )
        )

    @property
    def qualified_reference(self) -> bool:
        # Even a fully closed pre-lab packet cannot qualify a D reference
        # without an independently measured same-context realization band.
        return self.prelab_material_ready and self.realization_band_available


def blockers(e: M5PrelabEvidence) -> tuple[str, ...]:
    out: list[str] = []
    if not e.archived_material_existence_documented:
        out.append("ARCHIVED_MATERIAL_EXISTENCE_NOT_DOCUMENTED")
    if not e.physical_stock_access_confirmed:
        out.append("PHYSICAL_STOCK_ACCESS_NOT_CONFIRMED")
    if not e.t0_whole_genome_sequenced:
        out.append("M5_T0_GENOME_NOT_SEQUENCED")
    if not e.public_sequence_project_recovered:
        out.append("PUBLIC_SEQUENCE_PROJECT_NOT_RECOVERED")
    if not e.exact_t0_sequence_accession_resolved:
        out.append("EXACT_M5_T0_SEQUENCE_ACCESSION_NOT_RESOLVED")
    if not e.deep_class_candidate_supported:
        out.append("DEEP_CLASS_CANDIDATE_NOT_SUPPORTED")
    if not e.direct_registered_marker_pattern_verified:
        out.append("REGISTERED_MARKER_PATTERN_NOT_DIRECTLY_VERIFIED")
    if not e.core_reference_verified:
        out.append("CORE_REFERENCE_NOT_VERIFIED")
    if not e.gross_secondary_rearrangement_resolved:
        out.append("GROSS_SECONDARY_REARRANGEMENT_NOT_RESOLVED")
    if not e.realization_band_available:
        out.append("72_120H_D_REALIZATION_BAND_NOT_AVAILABLE")
    return tuple(out)


def next_action(e: M5PrelabEvidence) -> str:
    if not e.physical_stock_access_confirmed:
        return "CONFIRM_CURRENT_M5_T0_STOCK_ACCESS_OR_CUSTODIAN"
    if not e.exact_t0_sequence_accession_resolved:
        return "RESOLVE_EXACT_M5_T0_SEQUENCE_ACCESSION"
    if not e.direct_registered_marker_pattern_verified:
        return "DIRECTLY_SCORE_REGISTERED_DELETION_MARKERS"
    if not e.core_reference_verified or not e.gross_secondary_rearrangement_resolved:
        return "RESOLVE_CORE_AND_GROSS_REARRANGEMENT_STRUCTURE"
    if not e.realization_band_available:
        return "RUN_MATCHED_72_120H_D_REALIZATION_ASSAY"
    return "RUN_EXISTING_PER_REFERENCE_QUALIFICATION_GATE"
