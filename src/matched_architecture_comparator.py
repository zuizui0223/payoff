"""Architecture-lane subgate for matched S/D comparator pairs.

This gate is deliberately independent of Lane G outcomes. It asks whether an
integrated/shared candidate and a differentiated/released candidate are a
matched biological pair at the same strategic-unit level, with the intended
architecture difference isolated well enough to support PAYOFF semantics.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MatchedArchitectureComparatorReceipt:
    system_id: str
    shared_candidate_id: str
    differentiated_candidate_id: str
    architecture_unit_id: str
    support_reference: str
    same_strategic_unit_level_declared: bool
    same_net_task_declared: bool
    matched_background_declared: bool
    focal_architecture_difference_isolated_declared: bool
    shared_generalist_only_state_verified_declared: bool
    differentiated_state_verified_declared: bool
    both_units_stable_over_assay_declared: bool
    common_task_assay_available_declared: bool
    comparator_selection_independent_of_game_result_declared: bool
    comparator_selection_independent_of_raw_availability_declared: bool

    @property
    def unit_match_certified(self) -> bool:
        return all(
            (
                self.same_strategic_unit_level_declared,
                self.same_net_task_declared,
                self.both_units_stable_over_assay_declared,
                self.common_task_assay_available_declared,
            )
        )

    @property
    def contrast_isolation_certified(self) -> bool:
        return all(
            (
                self.matched_background_declared,
                self.focal_architecture_difference_isolated_declared,
                self.shared_generalist_only_state_verified_declared,
                self.differentiated_state_verified_declared,
            )
        )

    @property
    def matched_comparator_certified(self) -> bool:
        return all(
            (
                self.unit_match_certified,
                self.contrast_isolation_certified,
                self.comparator_selection_independent_of_game_result_declared,
                self.comparator_selection_independent_of_raw_availability_declared,
            )
        )


@dataclass(frozen=True)
class MatchedArchitectureComparatorAdjudication:
    unit_match_certified: bool
    contrast_isolation_certified: bool
    matched_comparator_certified: bool
    blockers: tuple[str, ...]
    generic_game_promoted: bool = False
    architecture_frequency_feedback_promoted: bool = False
    scope: str = "PAYOFF_matched_architecture_comparator_gate_v1"


def _nonempty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def adjudicate_matched_architecture_comparator(
    receipt: MatchedArchitectureComparatorReceipt,
) -> MatchedArchitectureComparatorAdjudication:
    _nonempty(receipt.system_id, "system_id")
    _nonempty(receipt.shared_candidate_id, "shared_candidate_id")
    _nonempty(receipt.differentiated_candidate_id, "differentiated_candidate_id")
    _nonempty(receipt.architecture_unit_id, "architecture_unit_id")
    _nonempty(receipt.support_reference, "support_reference")
    if receipt.shared_candidate_id == receipt.differentiated_candidate_id:
        raise ValueError("shared and differentiated candidates must differ")
    if not receipt.comparator_selection_independent_of_game_result_declared:
        raise ValueError("matched comparator selection must be independent of game result")
    if not receipt.comparator_selection_independent_of_raw_availability_declared:
        raise ValueError("matched comparator selection must be independent of raw availability")

    checks = (
        (receipt.same_strategic_unit_level_declared, "STRATEGIC_UNIT_LEVEL_NOT_MATCHED"),
        (receipt.same_net_task_declared, "NET_TASK_NOT_MATCHED"),
        (receipt.matched_background_declared, "BACKGROUND_NOT_MATCHED"),
        (
            receipt.focal_architecture_difference_isolated_declared,
            "FOCAL_ARCHITECTURE_DIFFERENCE_NOT_ISOLATED",
        ),
        (
            receipt.shared_generalist_only_state_verified_declared,
            "SHARED_GENERALIST_ONLY_STATE_NOT_VERIFIED",
        ),
        (
            receipt.differentiated_state_verified_declared,
            "DIFFERENTIATED_STATE_NOT_VERIFIED",
        ),
        (
            receipt.both_units_stable_over_assay_declared,
            "BOTH_UNITS_NOT_STABLE_OVER_ASSAY",
        ),
        (
            receipt.common_task_assay_available_declared,
            "COMMON_TASK_ASSAY_NOT_AVAILABLE",
        ),
    )
    blockers = tuple(label for passed, label in checks if not passed)
    return MatchedArchitectureComparatorAdjudication(
        unit_match_certified=receipt.unit_match_certified,
        contrast_isolation_certified=receipt.contrast_isolation_certified,
        matched_comparator_certified=receipt.matched_comparator_certified,
        blockers=blockers,
    )
