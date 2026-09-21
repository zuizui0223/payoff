"""Prospective taxon-inclusion gate for PAYOFF-B cross-system tests.

Taxa are not added to increase sample size mechanically. A candidate system
must add a distinct inferential contribution to the phase-retention programme.

At least one of the following scientific contributions is required:
- an independent prospectively registered lambda test;
- a forcing regime not represented in the current synthesis;
- a predeclared lambda boundary / sign-change test;
- a prospective actuator discriminator between competing mechanisms.

Compatibility with the common phase coordinate and segment scale is a separate
hard requirement.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TaxonInclusionProposal:
    system_name: str
    independent_test_id: str
    phase_coordinate_id: str
    segment_scale_id: str
    forcing_regime: str
    lambda_test_preregistered: bool
    forcing_regime_is_new: bool
    tests_lambda_boundary_or_sign_change: bool
    prospective_actuator_discriminator: bool
    raw_data_available: bool = False

    def __post_init__(self) -> None:
        for name in (
            "system_name",
            "independent_test_id",
            "phase_coordinate_id",
            "segment_scale_id",
            "forcing_regime",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")


@dataclass(frozen=True)
class TaxonInclusionGate:
    include: bool
    coordinate_compatible: bool
    segment_scale_compatible: bool
    independent_test_id_is_new: bool
    scientific_contribution_count: int
    contributions: tuple[str, ...]
    blockers: tuple[str, ...]
    raw_data_available: bool


def evaluate_taxon_inclusion(
    proposal: TaxonInclusionProposal,
    *,
    canonical_phase_coordinate_id: str,
    canonical_segment_scale_id: str,
    existing_independent_test_ids: set[str] | frozenset[str],
) -> TaxonInclusionGate:
    """Evaluate whether a candidate taxon adds inferential value.

    Raw-data availability is recorded but never counts as a scientific
    contribution by itself.
    """

    if not canonical_phase_coordinate_id.strip():
        raise ValueError(
            "canonical_phase_coordinate_id must be non-empty"
        )
    if not canonical_segment_scale_id.strip():
        raise ValueError(
            "canonical_segment_scale_id must be non-empty"
        )

    coordinate_compatible = (
        proposal.phase_coordinate_id
        == canonical_phase_coordinate_id
    )
    segment_scale_compatible = (
        proposal.segment_scale_id
        == canonical_segment_scale_id
    )
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
    if proposal.prospective_actuator_discriminator:
        contributions.append(
            "prospective_actuator_mechanism_discriminator"
        )

    blockers: list[str] = []
    if not coordinate_compatible:
        blockers.append("PHASE_COORDINATE_INCOMPATIBLE")
    if not segment_scale_compatible:
        blockers.append("SEGMENT_SCALE_INCOMPATIBLE")
    if not independent_test_id_is_new:
        blockers.append("INDEPENDENT_TEST_ID_ALREADY_USED")
    if not contributions:
        blockers.append("NO_NEW_INFERENTIAL_CONTRIBUTION")

    include = (
        coordinate_compatible
        and segment_scale_compatible
        and independent_test_id_is_new
        and bool(contributions)
    )

    return TaxonInclusionGate(
        include=include,
        coordinate_compatible=coordinate_compatible,
        segment_scale_compatible=segment_scale_compatible,
        independent_test_id_is_new=independent_test_id_is_new,
        scientific_contribution_count=len(contributions),
        contributions=tuple(contributions),
        blockers=tuple(blockers),
        raw_data_available=proposal.raw_data_available,
    )
