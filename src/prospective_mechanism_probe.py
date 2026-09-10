"""Prospective Lane-A mechanism-probe qualification without architecture promotion.

A useful perturbation for testing *why* differentiation occurs is not yet a
matched PAYOFF S architecture.  This module records that intermediate status.
It deliberately separates:

1. a probe that is suitable for a direct test of the differentiation-generation
   mechanism; and
2. a certified matched-S strategic architecture.

The first can be true while the second remains false.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProspectiveMechanismProbeReceipt:
    system_id: str
    probe_id: str
    comparator_id: str
    mediator_id: str
    support_reference: str
    matched_comparator_background_declared: bool
    focal_mediator_perturbation_declared: bool
    mediator_suppression_confirmed_declared: bool
    gross_growth_comparable_declared: bool
    gross_sporulation_comparable_declared: bool
    direct_generation_rate_assay_available_in_principle_declared: bool
    known_probe_specificity_caveat: str
    direct_generation_rate_reduction_measured_declared: bool
    post_generation_realization_matched_declared: bool
    net_task_preserved_declared: bool
    stable_or_heritable_s_unit_declared: bool
    independent_of_game_result_declared: bool
    independent_of_raw_availability_declared: bool

    @property
    def mechanism_probe_ready(self) -> bool:
        return all(
            (
                self.matched_comparator_background_declared,
                self.focal_mediator_perturbation_declared,
                self.mediator_suppression_confirmed_declared,
                self.gross_growth_comparable_declared,
                self.gross_sporulation_comparable_declared,
                self.direct_generation_rate_assay_available_in_principle_declared,
                self.independent_of_game_result_declared,
                self.independent_of_raw_availability_declared,
            )
        )

    @property
    def matched_s_certified(self) -> bool:
        """A much stronger status than probe readiness."""
        return all(
            (
                self.mechanism_probe_ready,
                self.direct_generation_rate_reduction_measured_declared,
                self.post_generation_realization_matched_declared,
                self.net_task_preserved_declared,
                self.stable_or_heritable_s_unit_declared,
            )
        )


@dataclass(frozen=True)
class ProspectiveMechanismProbeAdjudication:
    mechanism_probe_ready: bool
    matched_s_certified: bool
    probe_blockers: tuple[str, ...]
    matched_s_blockers: tuple[str, ...]
    generic_game_promoted: bool = False
    architecture_mapping_promoted: bool = False
    architecture_frequency_claim_promoted: bool = False
    scope: str = "PAYOFF_prospective_differentiation_mechanism_probe_v1"


def _nonempty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def adjudicate_prospective_mechanism_probe(
    receipt: ProspectiveMechanismProbeReceipt,
) -> ProspectiveMechanismProbeAdjudication:
    _nonempty(receipt.system_id, "system_id")
    _nonempty(receipt.probe_id, "probe_id")
    _nonempty(receipt.comparator_id, "comparator_id")
    _nonempty(receipt.mediator_id, "mediator_id")
    _nonempty(receipt.support_reference, "support_reference")
    _nonempty(receipt.known_probe_specificity_caveat, "known_probe_specificity_caveat")

    if not receipt.independent_of_game_result_declared:
        raise ValueError("mechanism-probe qualification must be independent of game outcome")
    if not receipt.independent_of_raw_availability_declared:
        raise ValueError("mechanism-probe qualification must not depend on raw availability")

    probe_checks = (
        (receipt.matched_comparator_background_declared, "COMPARATOR_BACKGROUND_NOT_MATCHED"),
        (receipt.focal_mediator_perturbation_declared, "FOCAL_MEDIATOR_NOT_PERTURBED"),
        (receipt.mediator_suppression_confirmed_declared, "MEDIATOR_SUPPRESSION_NOT_CONFIRMED"),
        (receipt.gross_growth_comparable_declared, "GROSS_GROWTH_NOT_COMPARABLE"),
        (receipt.gross_sporulation_comparable_declared, "GROSS_SPORULATION_NOT_COMPARABLE"),
        (
            receipt.direct_generation_rate_assay_available_in_principle_declared,
            "DIRECT_GENERATION_RATE_ASSAY_NOT_DECLARED",
        ),
    )
    probe_blockers = tuple(label for passed, label in probe_checks if not passed)

    matched_s_checks = (
        (
            receipt.direct_generation_rate_reduction_measured_declared,
            "DIFFERENTIATION_GENERATION_REDUCTION_NOT_MEASURED",
        ),
        (
            receipt.post_generation_realization_matched_declared,
            "POST_GENERATION_REALIZATION_NOT_MATCHED",
        ),
        (receipt.net_task_preserved_declared, "NET_TASK_NOT_PRESERVED"),
        (receipt.stable_or_heritable_s_unit_declared, "STABLE_OR_HERITABLE_S_UNIT_NOT_ESTABLISHED"),
    )
    matched_s_blockers = tuple(label for passed, label in matched_s_checks if not passed)

    return ProspectiveMechanismProbeAdjudication(
        mechanism_probe_ready=receipt.mechanism_probe_ready,
        matched_s_certified=receipt.matched_s_certified,
        probe_blockers=probe_blockers,
        matched_s_blockers=matched_s_blockers,
    )
