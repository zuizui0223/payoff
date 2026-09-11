"""Guard against promoting a mechanism probe into a matched architecture claim.

Lane A only.  A positive mediator result can be necessary evidence for a
candidate shared/generalist architecture but is not sufficient when the
perturbation also changes the biological task, unit, background, or stability.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MechanismToArchitecturePromotionReceipt:
    system_id: str
    mechanism_id: str
    candidate_shared_id: str
    candidate_differentiated_id: str
    support_reference: str
    triangulated_generation_reduction_declared: bool
    preoutcome_probe_rule_respected_declared: bool
    candidate_shared_unit_exists_declared: bool
    same_strategic_unit_level_declared: bool
    same_net_task_preserved_or_rescued_declared: bool
    task_match_independent_of_differentiation_mechanism_declared: bool
    matched_background_declared: bool
    focal_architecture_difference_isolated_declared: bool
    shared_generalist_only_state_verified_declared: bool
    differentiated_state_verified_declared: bool
    both_units_stable_over_assay_declared: bool
    promotion_independent_of_game_result_declared: bool
    promotion_independent_of_raw_availability_declared: bool

    @property
    def mechanism_support_certified(self) -> bool:
        return all(
            (
                self.triangulated_generation_reduction_declared,
                self.preoutcome_probe_rule_respected_declared,
            )
        )

    @property
    def task_matched_architecture_counterfactual_certified(self) -> bool:
        return all(
            (
                self.candidate_shared_unit_exists_declared,
                self.same_strategic_unit_level_declared,
                self.same_net_task_preserved_or_rescued_declared,
                self.task_match_independent_of_differentiation_mechanism_declared,
                self.matched_background_declared,
                self.focal_architecture_difference_isolated_declared,
                self.shared_generalist_only_state_verified_declared,
                self.differentiated_state_verified_declared,
                self.both_units_stable_over_assay_declared,
            )
        )

    @property
    def matched_s_promotion_licensed(self) -> bool:
        return all(
            (
                self.mechanism_support_certified,
                self.task_matched_architecture_counterfactual_certified,
                self.promotion_independent_of_game_result_declared,
                self.promotion_independent_of_raw_availability_declared,
            )
        )


@dataclass(frozen=True)
class MechanismToArchitecturePromotionAdjudication:
    mechanism_support_certified: bool
    task_matched_architecture_counterfactual_certified: bool
    matched_s_promotion_licensed: bool
    blockers: tuple[str, ...]
    generic_game_promoted: bool = False
    eta_identified: bool = False
    e1_promoted: bool = False
    scope: str = "PAYOFF_mechanism_to_matched_architecture_promotion_gate_v1"


def _nonempty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def adjudicate_mechanism_to_architecture_promotion(
    receipt: MechanismToArchitecturePromotionReceipt,
) -> MechanismToArchitecturePromotionAdjudication:
    _nonempty(receipt.system_id, "system_id")
    _nonempty(receipt.mechanism_id, "mechanism_id")
    _nonempty(receipt.candidate_shared_id, "candidate_shared_id")
    _nonempty(receipt.candidate_differentiated_id, "candidate_differentiated_id")
    _nonempty(receipt.support_reference, "support_reference")
    if receipt.candidate_shared_id == receipt.candidate_differentiated_id:
        raise ValueError("shared and differentiated candidates must differ")
    if not receipt.promotion_independent_of_game_result_declared:
        raise ValueError("architecture promotion must be independent of Lane G outcome")
    if not receipt.promotion_independent_of_raw_availability_declared:
        raise ValueError("architecture promotion must be independent of raw-data availability")

    checks = (
        (
            receipt.triangulated_generation_reduction_declared,
            "TRIANGULATED_GENERATION_REDUCTION_NOT_ESTABLISHED",
        ),
        (
            receipt.preoutcome_probe_rule_respected_declared,
            "PREOUTCOME_PROBE_RULE_NOT_ESTABLISHED",
        ),
        (receipt.candidate_shared_unit_exists_declared, "MATCHED_SHARED_UNIT_NOT_RECOVERED"),
        (receipt.same_strategic_unit_level_declared, "STRATEGIC_UNIT_LEVEL_NOT_MATCHED"),
        (
            receipt.same_net_task_preserved_or_rescued_declared,
            "NET_TASK_NOT_PRESERVED_OR_RESCUED",
        ),
        (
            receipt.task_match_independent_of_differentiation_mechanism_declared,
            "TASK_MATCH_NOT_INDEPENDENT_OF_DIFFERENTIATION_MECHANISM",
        ),
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
    )
    blockers = tuple(label for passed, label in checks if not passed)
    return MechanismToArchitecturePromotionAdjudication(
        mechanism_support_certified=receipt.mechanism_support_certified,
        task_matched_architecture_counterfactual_certified=(
            receipt.task_matched_architecture_counterfactual_certified
        ),
        matched_s_promotion_licensed=receipt.matched_s_promotion_licensed,
        blockers=blockers,
    )
