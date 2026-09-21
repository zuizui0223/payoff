"""Inferential inclusion gate for PAYOFF-B cross-system evidence.

The evidence unit is an independent test, not a taxon label.

A candidate is not included merely because data exist or because it occupies a
new forcing regime. It must supply at least one prospectively evaluable endpoint:

- a lambda endpoint on the common phase-retention coordinate; or
- a system-specific actuator discriminator.

Lambda evidence additionally requires compatibility with the canonical phase
coordinate and segment scale. Actuator-only perturbations do not, because they
contribute zero lambda support by construction.

The historical class/function names retain "Taxon" for backward compatibility,
but the gate now applies equally to within-taxon forcing perturbations.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TaxonInclusionProposal:
    system_name: str
    independent_test_id: str
    forcing_regime: str
    lambda_test_preregistered: bool
    forcing_regime_is_new: bool
    tests_lambda_boundary_or_sign_change: bool
    prospective_actuator_discriminator: bool
    within_system_lambda_perturbation: bool = False
    phase_coordinate_id: str | None = None
    segment_scale_id: str | None = None
    raw_data_available: bool = False

    def __post_init__(self) -> None:
        for name in (
            "system_name",
            "independent_test_id",
            "forcing_regime",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")

        if self.phase_coordinate_id is not None:
            if not self.phase_coordinate_id.strip():
                raise ValueError(
                    "phase_coordinate_id must be non-empty when supplied"
                )
        if self.segment_scale_id is not None:
            if not self.segment_scale_id.strip():
                raise ValueError(
                    "segment_scale_id must be non-empty when supplied"
                )

    @property
    def requests_lambda_evidence(self) -> bool:
        return (
            self.lambda_test_preregistered
            or self.tests_lambda_boundary_or_sign_change
            or self.within_system_lambda_perturbation
        )

    @property
    def requests_cross_system_lambda_evidence(self) -> bool:
        return (
            self.lambda_test_preregistered
            or self.tests_lambda_boundary_or_sign_change
        ) and not self.within_system_lambda_perturbation

    @property
    def requests_actuator_evidence(self) -> bool:
        return self.prospective_actuator_discriminator


# Preferred semantic alias for new code.
EvidenceInclusionProposal = TaxonInclusionProposal


@dataclass(frozen=True)
class TaxonInclusionGate:
    include: bool
    lambda_evidence_requested: bool
    actuator_evidence_requested: bool
    coordinate_compatible: bool | None
    segment_scale_compatible: bool | None
    independent_test_id_is_new: bool
    registered_endpoint_present: bool
    contributes_to_lambda_synthesis: bool
    contributes_within_system_lambda_perturbation: bool
    contributes_actuator_only: bool
    scientific_contribution_count: int
    contributions: tuple[str, ...]
    blockers: tuple[str, ...]
    raw_data_available: bool


EvidenceInclusionGate = TaxonInclusionGate


def evaluate_taxon_inclusion(
    proposal: TaxonInclusionProposal,
    *,
    canonical_phase_coordinate_id: str,
    canonical_segment_scale_id: str,
    existing_independent_test_ids: set[str] | frozenset[str],
) -> TaxonInclusionGate:
    """Evaluate whether a candidate independent test adds inferential value.

    New forcing is informative context, but is not sufficient by itself.
    At least one registered endpoint (lambda or actuator) is required.
    """

    if not canonical_phase_coordinate_id.strip():
        raise ValueError(
            "canonical_phase_coordinate_id must be non-empty"
        )
    if not canonical_segment_scale_id.strip():
        raise ValueError(
            "canonical_segment_scale_id must be non-empty"
        )

    lambda_requested = proposal.requests_lambda_evidence
    cross_system_lambda_requested = (
        proposal.requests_cross_system_lambda_evidence
    )
    within_system_lambda_requested = (
        proposal.within_system_lambda_perturbation
    )
    actuator_requested = proposal.requests_actuator_evidence
    registered_endpoint_present = (
        lambda_requested or actuator_requested
    )

    if cross_system_lambda_requested:
        coordinate_compatible: bool | None = (
            proposal.phase_coordinate_id
            == canonical_phase_coordinate_id
        )
        segment_scale_compatible: bool | None = (
            proposal.segment_scale_id
            == canonical_segment_scale_id
        )
    elif within_system_lambda_requested:
        # A within-system perturbation needs a declared coordinate/scale, but
        # it does not need to match the cross-system synthesis contract.
        coordinate_compatible = (
            proposal.phase_coordinate_id is not None
            and bool(proposal.phase_coordinate_id.strip())
        )
        segment_scale_compatible = (
            proposal.segment_scale_id is not None
            and bool(proposal.segment_scale_id.strip())
        )
    else:
        # Not applicable to actuator-only evidence.
        coordinate_compatible = None
        segment_scale_compatible = None

    independent_test_id_is_new = (
        proposal.independent_test_id
        not in existing_independent_test_ids
    )

    contributions: list[str] = []
    if proposal.lambda_test_preregistered:
        contributions.append(
            "prospectively_registered_independent_lambda_test"
        )
    if proposal.forcing_regime_is_new:
        contributions.append("new_forcing_regime")
    if proposal.tests_lambda_boundary_or_sign_change:
        contributions.append(
            "predeclared_lambda_boundary_or_sign_change"
        )
    if proposal.within_system_lambda_perturbation:
        contributions.append(
            "prospective_within_system_lambda_perturbation"
        )
    if proposal.prospective_actuator_discriminator:
        contributions.append(
            "prospective_actuator_mechanism_discriminator"
        )

    blockers: list[str] = []
    if not independent_test_id_is_new:
        blockers.append("INDEPENDENT_TEST_ID_ALREADY_USED")
    if not registered_endpoint_present:
        blockers.append("NO_REGISTERED_ENDPOINT")

    if cross_system_lambda_requested:
        if not coordinate_compatible:
            blockers.append("PHASE_COORDINATE_INCOMPATIBLE")
        if not segment_scale_compatible:
            blockers.append("SEGMENT_SCALE_INCOMPATIBLE")
    elif within_system_lambda_requested:
        if not coordinate_compatible:
            blockers.append("WITHIN_SYSTEM_PHASE_COORDINATE_MISSING")
        if not segment_scale_compatible:
            blockers.append("WITHIN_SYSTEM_SEGMENT_SCALE_MISSING")

    lambda_eligible = (
        cross_system_lambda_requested
        and bool(coordinate_compatible)
        and bool(segment_scale_compatible)
        and independent_test_id_is_new
    )
    within_system_lambda_eligible = (
        within_system_lambda_requested
        and bool(coordinate_compatible)
        and bool(segment_scale_compatible)
        and independent_test_id_is_new
    )
    actuator_eligible = (
        actuator_requested
        and independent_test_id_is_new
    )

    include = (
        registered_endpoint_present
        and independent_test_id_is_new
        and (
            lambda_eligible
            or within_system_lambda_eligible
            or actuator_eligible
        )
    )

    return TaxonInclusionGate(
        include=include,
        lambda_evidence_requested=lambda_requested,
        actuator_evidence_requested=actuator_requested,
        coordinate_compatible=coordinate_compatible,
        segment_scale_compatible=segment_scale_compatible,
        independent_test_id_is_new=independent_test_id_is_new,
        registered_endpoint_present=registered_endpoint_present,
        contributes_to_lambda_synthesis=lambda_eligible,
        contributes_within_system_lambda_perturbation=(
            within_system_lambda_eligible
        ),
        contributes_actuator_only=(
            actuator_eligible
            and not lambda_eligible
            and not within_system_lambda_eligible
        ),
        scientific_contribution_count=len(contributions),
        contributions=tuple(contributions),
        blockers=tuple(blockers),
        raw_data_available=proposal.raw_data_available,
    )


def evaluate_evidence_inclusion(
    proposal: EvidenceInclusionProposal,
    *,
    canonical_phase_coordinate_id: str,
    canonical_segment_scale_id: str,
    existing_independent_test_ids: set[str] | frozenset[str],
) -> EvidenceInclusionGate:
    """Preferred alias for the generalized independent-test gate."""

    return evaluate_taxon_inclusion(
        proposal,
        canonical_phase_coordinate_id=canonical_phase_coordinate_id,
        canonical_segment_scale_id=canonical_segment_scale_id,
        existing_independent_test_ids=existing_independent_test_ids,
    )
