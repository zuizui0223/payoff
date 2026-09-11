"""Response-blind scale qualification for the Streptomyces congener programme.

Task and genotoxicity scales are intentionally treated differently. A canonical
colony-level task assay already exists in the focal Streptomyces division-of-
labour literature. The genotoxicity intermediate does not yet have an accepted
S. coelicolor primary assay, so it must be qualified on controls while congener
outcomes remain blinded.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CanonicalTaskScaleReceipt:
    scale_id: str
    support_reference: str
    focal_task: str
    higher_is_better_declared: bool
    direct_external_function_readout_declared: bool
    assay_protocol_preoutcome_frozen: bool
    candidate_outcomes_used_to_select_scale: bool
    fitness_guardrail_kept_separate: bool

    @property
    def task_scale_qualified(self) -> bool:
        return all(
            (
                bool(self.scale_id.strip()),
                bool(self.support_reference.strip()),
                bool(self.focal_task.strip()),
                self.higher_is_better_declared,
                self.direct_external_function_readout_declared,
                self.assay_protocol_preoutcome_frozen,
                not self.candidate_outcomes_used_to_select_scale,
                self.fitness_guardrail_kept_separate,
            )
        )


@dataclass(frozen=True)
class ResponseBlindGenotoxicityQualificationReceipt:
    assay_id: str
    support_reference: str
    focal_system_id: str
    candidate_outcomes_blinded_declared: bool
    positive_genotoxic_control_declared: bool
    negative_control_declared: bool
    positive_control_response_certified: bool
    negative_control_specificity_certified: bool
    repeatability_certified: bool
    assay_direction_frozen_declared: bool
    assay_unit_frozen_declared: bool
    sampling_context_frozen_declared: bool
    distinct_from_direct_mu_outcome_declared: bool
    not_pigment_amount_only_declared: bool
    not_ros_amount_only_declared: bool

    @property
    def genotoxicity_scale_qualified(self) -> bool:
        return all(
            (
                bool(self.assay_id.strip()),
                bool(self.support_reference.strip()),
                bool(self.focal_system_id.strip()),
                self.candidate_outcomes_blinded_declared,
                self.positive_genotoxic_control_declared,
                self.negative_control_declared,
                self.positive_control_response_certified,
                self.negative_control_specificity_certified,
                self.repeatability_certified,
                self.assay_direction_frozen_declared,
                self.assay_unit_frozen_declared,
                self.sampling_context_frozen_declared,
                self.distinct_from_direct_mu_outcome_declared,
                self.not_pigment_amount_only_declared,
                self.not_ros_amount_only_declared,
            )
        )


@dataclass(frozen=True)
class AssayQualificationAdjudication:
    qualified: bool
    blockers: tuple[str, ...]
    congener_outcomes_opened: bool = False
    matched_s_promoted: bool = False
    architecture_mapping_promoted: bool = False
    generic_game_promoted: bool = False
    scope: str = "response_blind_assay_scale_qualification_v1"


def adjudicate_genotoxicity_assay(
    receipt: ResponseBlindGenotoxicityQualificationReceipt,
) -> AssayQualificationAdjudication:
    if not receipt.candidate_outcomes_blinded_declared:
        raise ValueError("genotoxicity assay must be qualified before congener outcomes are opened")

    checks = (
        (bool(receipt.assay_id.strip()), "ASSAY_ID_MISSING"),
        (bool(receipt.support_reference.strip()), "SUPPORT_REFERENCE_MISSING"),
        (bool(receipt.focal_system_id.strip()), "FOCAL_SYSTEM_ID_MISSING"),
        (receipt.positive_genotoxic_control_declared, "POSITIVE_CONTROL_NOT_DECLARED"),
        (receipt.negative_control_declared, "NEGATIVE_CONTROL_NOT_DECLARED"),
        (receipt.positive_control_response_certified, "POSITIVE_CONTROL_RESPONSE_NOT_CERTIFIED"),
        (receipt.negative_control_specificity_certified, "NEGATIVE_CONTROL_SPECIFICITY_NOT_CERTIFIED"),
        (receipt.repeatability_certified, "REPEATABILITY_NOT_CERTIFIED"),
        (receipt.assay_direction_frozen_declared, "ASSAY_DIRECTION_NOT_FROZEN"),
        (receipt.assay_unit_frozen_declared, "ASSAY_UNIT_NOT_FROZEN"),
        (receipt.sampling_context_frozen_declared, "SAMPLING_CONTEXT_NOT_FROZEN"),
        (receipt.distinct_from_direct_mu_outcome_declared, "ASSAY_NOT_DISTINCT_FROM_DIRECT_MU"),
        (receipt.not_pigment_amount_only_declared, "PIGMENT_AMOUNT_ONLY_IS_NOT_GENOTOXICITY"),
        (receipt.not_ros_amount_only_declared, "ROS_AMOUNT_ONLY_IS_NOT_GENOTOXICITY"),
    )
    blockers = tuple(label for passed, label in checks if not passed)
    return AssayQualificationAdjudication(
        qualified=receipt.genotoxicity_scale_qualified,
        blockers=blockers,
    )
