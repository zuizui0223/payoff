"""Architecture-lane gate for treating a multigenotype consortium as one strategy.

This module is deliberately independent of frequency-game outcomes.  It asks
whether an assemblage can be used as the same level of strategic unit as a
comparator architecture.  Internal composition q and external architecture
frequency p must remain distinct variables.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConsortiumStrategicUnitReceipt:
    system_id: str
    candidate_unit_id: str
    support_reference: str
    member_set_predeclared: bool
    unit_boundary_predeclared: bool
    assembly_or_regeneration_protocol_declared: bool
    composition_state_reproducible_declared: bool
    propagation_or_transmission_declared: bool
    identity_retained_over_assay_horizon_declared: bool
    internal_composition_q_separated_from_external_frequency_p_declared: bool
    external_frequency_can_vary_whole_units_declared: bool
    unit_level_fitness_or_output_defined_declared: bool
    certification_independent_of_game_result_declared: bool
    certification_independent_of_raw_availability_declared: bool

    @property
    def structural_identity_certified(self) -> bool:
        return all(
            (
                self.member_set_predeclared,
                self.unit_boundary_predeclared,
                self.assembly_or_regeneration_protocol_declared,
                self.composition_state_reproducible_declared,
                self.propagation_or_transmission_declared,
                self.identity_retained_over_assay_horizon_declared,
            )
        )

    @property
    def payoff_unit_alignment_certified(self) -> bool:
        return all(
            (
                self.internal_composition_q_separated_from_external_frequency_p_declared,
                self.external_frequency_can_vary_whole_units_declared,
                self.unit_level_fitness_or_output_defined_declared,
            )
        )

    @property
    def strategic_unit_certified(self) -> bool:
        return all(
            (
                self.structural_identity_certified,
                self.payoff_unit_alignment_certified,
                self.certification_independent_of_game_result_declared,
                self.certification_independent_of_raw_availability_declared,
            )
        )


@dataclass(frozen=True)
class ConsortiumStrategicUnitAdjudication:
    structural_identity_certified: bool
    payoff_unit_alignment_certified: bool
    strategic_unit_certified: bool
    blockers: tuple[str, ...]
    architecture_mapping_promoted: bool = False
    generic_game_promoted: bool = False
    scope: str = "PAYOFF_multigenotype_consortium_strategic_unit_gate_v1"


def _nonempty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def adjudicate_consortium_strategic_unit(
    receipt: ConsortiumStrategicUnitReceipt,
) -> ConsortiumStrategicUnitAdjudication:
    _nonempty(receipt.system_id, "system_id")
    _nonempty(receipt.candidate_unit_id, "candidate_unit_id")
    _nonempty(receipt.support_reference, "support_reference")
    if not receipt.certification_independent_of_game_result_declared:
        raise ValueError(
            "strategic-unit certification must be independent of game outcome"
        )
    if not receipt.certification_independent_of_raw_availability_declared:
        raise ValueError(
            "strategic-unit certification must not depend on raw-data availability"
        )

    blockers: list[str] = []
    checks = (
        (receipt.member_set_predeclared, "MEMBER_SET_NOT_PREDECLARED"),
        (receipt.unit_boundary_predeclared, "UNIT_BOUNDARY_NOT_PREDECLARED"),
        (
            receipt.assembly_or_regeneration_protocol_declared,
            "ASSEMBLY_OR_REGENERATION_PROTOCOL_NOT_DECLARED",
        ),
        (
            receipt.composition_state_reproducible_declared,
            "COMPOSITION_STATE_REPRODUCIBILITY_NOT_DECLARED",
        ),
        (
            receipt.propagation_or_transmission_declared,
            "UNIT_PROPAGATION_OR_TRANSMISSION_NOT_DECLARED",
        ),
        (
            receipt.identity_retained_over_assay_horizon_declared,
            "UNIT_IDENTITY_OVER_ASSAY_HORIZON_NOT_DECLARED",
        ),
        (
            receipt.internal_composition_q_separated_from_external_frequency_p_declared,
            "INTERNAL_Q_NOT_SEPARATED_FROM_EXTERNAL_P",
        ),
        (
            receipt.external_frequency_can_vary_whole_units_declared,
            "WHOLE_UNIT_EXTERNAL_FREQUENCY_NOT_DEFINED",
        ),
        (
            receipt.unit_level_fitness_or_output_defined_declared,
            "UNIT_LEVEL_FITNESS_OR_OUTPUT_NOT_DEFINED",
        ),
    )
    for passed, label in checks:
        if not passed:
            blockers.append(label)

    return ConsortiumStrategicUnitAdjudication(
        structural_identity_certified=receipt.structural_identity_certified,
        payoff_unit_alignment_certified=receipt.payoff_unit_alignment_certified,
        strategic_unit_certified=receipt.strategic_unit_certified,
        blockers=tuple(blockers),
    )
