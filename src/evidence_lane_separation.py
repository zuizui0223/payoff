"""Prevent promotion leakage across PAYOFF empirical evidence lanes.

The three empirical lanes are deliberately non-substitutable:

R -- raw archive reconstruction / provenance
G -- generic two-strategy game validation
A -- architecture mapping to the PAYOFF S/D semantics

Architecture-specific empirical promotion is a separate intersection gate.  A
successful raw reconstruction never implies a game result; a successful game
result never implies an architecture mapping; and an architecture mapping never
implies frequency-dependent fitness.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RawArchiveReceipt:
    system_id: str
    dataset_id: str
    support_reference: str
    bytes_acquired: bool
    checksum_verified: bool
    manifest_reconstructed: bool
    schema_reconstructed: bool
    transformations_reconstructed: bool
    raw_analysis_reproduced: bool

    @property
    def reconstruction_certified(self) -> bool:
        return all(
            (
                self.bytes_acquired,
                self.checksum_verified,
                self.manifest_reconstructed,
                self.schema_reconstructed,
                self.transformations_reconstructed,
            )
        )

    @property
    def analysis_reproduction_certified(self) -> bool:
        return self.reconstruction_certified and self.raw_analysis_reproduced


@dataclass(frozen=True)
class GenericGameReceipt:
    system_id: str
    comparison_id: str
    strategy_unit_id: str
    dataset_id: str | None
    support_reference: str
    evidence_source_mode: str
    frequency_support_declared: bool
    common_outcome_scale_declared: bool
    generic_game_result_recovered: bool
    architecture_semantics_used_declared: bool

    @property
    def validation_certified(self) -> bool:
        return all(
            (
                self.frequency_support_declared,
                self.common_outcome_scale_declared,
                self.generic_game_result_recovered,
                not self.architecture_semantics_used_declared,
            )
        )


@dataclass(frozen=True)
class ArchitectureMappingReceipt:
    system_id: str
    comparison_id: str
    architecture_unit_id: str
    support_reference: str
    integrated_shared_candidate_declared: bool
    differentiated_released_candidate_declared: bool
    matched_net_task_declared: bool
    heritable_or_stable_unit_declared: bool
    unit_consistency_declared: bool
    mapping_independent_of_game_result_declared: bool

    @property
    def mapping_certified(self) -> bool:
        return all(
            (
                self.integrated_shared_candidate_declared,
                self.differentiated_released_candidate_declared,
                self.matched_net_task_declared,
                self.heritable_or_stable_unit_declared,
                self.unit_consistency_declared,
                self.mapping_independent_of_game_result_declared,
            )
        )


@dataclass(frozen=True)
class EvidenceLaneAdjudication:
    raw_reconstruction_certified: bool | None
    raw_analysis_reproduction_certified: bool | None
    generic_game_validation_certified: bool
    architecture_mapping_certified: bool
    pair_alignment_certified: bool
    architecture_specific_claim_licensed: bool
    blockers: tuple[str, ...]
    generic_game_claim_allowed: bool
    architecture_mapping_claim_allowed: bool
    scope: str = "PAYOFF_R_G_A_empirical_lane_separation_v1"


def _nonempty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def validate_raw_archive_receipt(receipt: RawArchiveReceipt) -> RawArchiveReceipt:
    _nonempty(receipt.system_id, "system_id")
    _nonempty(receipt.dataset_id, "dataset_id")
    _nonempty(receipt.support_reference, "support_reference")
    return receipt


def validate_generic_game_receipt(receipt: GenericGameReceipt) -> GenericGameReceipt:
    _nonempty(receipt.system_id, "system_id")
    _nonempty(receipt.comparison_id, "comparison_id")
    _nonempty(receipt.strategy_unit_id, "strategy_unit_id")
    _nonempty(receipt.support_reference, "support_reference")
    mode = _nonempty(receipt.evidence_source_mode, "evidence_source_mode")
    if mode not in {"published_text", "raw_archive", "digitized_figure", "derived_table"}:
        raise ValueError("unsupported evidence_source_mode")
    if receipt.architecture_semantics_used_declared:
        raise ValueError(
            "generic game lane must use architecture-neutral strategy labels"
        )
    if mode == "raw_archive" and not receipt.dataset_id:
        raise ValueError("raw_archive game evidence requires dataset_id")
    return receipt


def validate_architecture_mapping_receipt(
    receipt: ArchitectureMappingReceipt,
) -> ArchitectureMappingReceipt:
    _nonempty(receipt.system_id, "system_id")
    _nonempty(receipt.comparison_id, "comparison_id")
    _nonempty(receipt.architecture_unit_id, "architecture_unit_id")
    _nonempty(receipt.support_reference, "support_reference")
    if not receipt.mapping_independent_of_game_result_declared:
        raise ValueError(
            "architecture mapping must be justified independently of frequency-game outcome"
        )
    return receipt


def adjudicate_evidence_lanes(
    game: GenericGameReceipt,
    architecture: ArchitectureMappingReceipt,
    *,
    raw: RawArchiveReceipt | None = None,
    pair_alignment_declared: bool,
    pair_alignment_reference: str,
) -> EvidenceLaneAdjudication:
    """Adjudicate lane status without allowing semantic leakage.

    `pair_alignment_declared` is the explicit statement that the neutral strategy
    pair used in Lane G is the same empirical pair that Lane A maps to PAYOFF's
    integrated/shared versus differentiated/released semantics.
    """
    validate_generic_game_receipt(game)
    validate_architecture_mapping_receipt(architecture)
    if raw is not None:
        validate_raw_archive_receipt(raw)
    alignment_ref = _nonempty(pair_alignment_reference, "pair_alignment_reference")

    blockers: list[str] = []

    raw_recon = raw.reconstruction_certified if raw is not None else None
    raw_reprod = raw.analysis_reproduction_certified if raw is not None else None

    if game.evidence_source_mode == "raw_archive":
        if raw is None:
            blockers.append("RAW_RECEIPT_REQUIRED_FOR_RAW_ARCHIVE_GAME_EVIDENCE")
        else:
            if game.system_id != raw.system_id or game.dataset_id != raw.dataset_id:
                blockers.append("RAW_GAME_PROVENANCE_MISMATCH")
            if not raw.reconstruction_certified:
                blockers.append("RAW_RECONSTRUCTION_NOT_CERTIFIED")

    game_ok = game.validation_certified and not any(
        b in blockers
        for b in (
            "RAW_RECEIPT_REQUIRED_FOR_RAW_ARCHIVE_GAME_EVIDENCE",
            "RAW_GAME_PROVENANCE_MISMATCH",
            "RAW_RECONSTRUCTION_NOT_CERTIFIED",
        )
    )
    if not game.validation_certified:
        blockers.append("GENERIC_GAME_VALIDATION_NOT_CERTIFIED")

    arch_ok = architecture.mapping_certified
    if not arch_ok:
        blockers.append("ARCHITECTURE_MAPPING_NOT_CERTIFIED")

    same_system = game.system_id == architecture.system_id
    same_comparison = game.comparison_id == architecture.comparison_id
    same_unit = game.strategy_unit_id == architecture.architecture_unit_id
    pair_ok = bool(pair_alignment_declared and same_system and same_comparison and same_unit)

    if not pair_alignment_declared:
        blockers.append("PAIR_ALIGNMENT_NOT_DECLARED")
    if not same_system:
        blockers.append("GAME_ARCHITECTURE_SYSTEM_MISMATCH")
    if not same_comparison:
        blockers.append("GAME_ARCHITECTURE_COMPARISON_MISMATCH")
    if not same_unit:
        blockers.append("GAME_ARCHITECTURE_STRATEGIC_UNIT_MISMATCH")

    licensed = bool(game_ok and arch_ok and pair_ok)

    # Keep the explicit support reference alive as an audit datum even though the
    # current deterministic gate only needs non-emptiness.
    _ = alignment_ref

    return EvidenceLaneAdjudication(
        raw_reconstruction_certified=raw_recon,
        raw_analysis_reproduction_certified=raw_reprod,
        generic_game_validation_certified=game_ok,
        architecture_mapping_certified=arch_ok,
        pair_alignment_certified=pair_ok,
        architecture_specific_claim_licensed=licensed,
        blockers=tuple(dict.fromkeys(blockers)),
        generic_game_claim_allowed=game_ok,
        architecture_mapping_claim_allowed=arch_ok,
    )
