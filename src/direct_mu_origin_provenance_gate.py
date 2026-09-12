"""Require explicit derivation provenance before a literature mutant counts as an independent D origin.

Strain naming patterns, plate prefixes, phenotypes, deletion class, or publication in the same
panel are not sufficient to infer biological independence. This gate is prospective evidence
governance only; it does not qualify a reference or identify direct-mu.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class OriginProvenanceCandidate:
    candidate_id: str
    source_study: str
    explicit_founder_record_available: bool
    source_colony_or_lineage_id_available: bool
    derivation_independent_of_other_registered_candidates: bool
    independence_inferred_from_name_only: bool = False

@dataclass(frozen=True)
class OriginProvenanceReceipt:
    candidate_id: str
    independent_origin_certified: bool
    blockers: tuple[str, ...]


def certify_origin_provenance(c: OriginProvenanceCandidate) -> OriginProvenanceReceipt:
    blockers = []
    if not c.candidate_id.strip() or not c.source_study.strip():
        blockers.append("CANDIDATE_ID_OR_SOURCE_MISSING")
    if c.independence_inferred_from_name_only:
        blockers.append("INDEPENDENCE_INFERRED_FROM_STRAIN_NAME")
    if not c.explicit_founder_record_available:
        blockers.append("EXPLICIT_FOUNDER_RECORD_NOT_RECOVERED")
    if not c.source_colony_or_lineage_id_available:
        blockers.append("SOURCE_COLONY_OR_LINEAGE_ID_NOT_RECOVERED")
    if not c.derivation_independent_of_other_registered_candidates:
        blockers.append("INDEPENDENT_DERIVATION_NOT_ESTABLISHED")
    return OriginProvenanceReceipt(c.candidate_id, not blockers, tuple(blockers))
