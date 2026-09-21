import pytest

from src.taxon_inclusion_gate import (
    TaxonInclusionProposal,
    evaluate_taxon_inclusion,
)


COMMON_COORDINATE = "signed_resource_phase_error"
COMMON_SCALE = "standardized_tracking_segment_v1"
EXISTING = frozenset({"A_lambda_holdout", "W_lambda_holdout"})


def proposal(**overrides):
    base = dict(
        system_name="candidate_X",
        independent_test_id="X_lambda_holdout",
        phase_coordinate_id=COMMON_COORDINATE,
        segment_scale_id=COMMON_SCALE,
        forcing_regime="novel_regime",
        lambda_test_preregistered=False,
        forcing_regime_is_new=False,
        tests_lambda_boundary_or_sign_change=False,
        prospective_actuator_discriminator=False,
        raw_data_available=False,
    )
    base.update(overrides)
    return TaxonInclusionProposal(**base)


def evaluate(row):
    return evaluate_taxon_inclusion(
        row,
        canonical_phase_coordinate_id=COMMON_COORDINATE,
        canonical_segment_scale_id=COMMON_SCALE,
        existing_independent_test_ids=EXISTING,
    )


def test_raw_data_availability_alone_does_not_license_taxon_addition():
    gate = evaluate(
        proposal(raw_data_available=True)
    )

    assert not gate.include
    assert gate.raw_data_available
    assert gate.scientific_contribution_count == 0
    assert "NO_REGISTERED_ENDPOINT" in gate.blockers


def test_preregistered_independent_lambda_test_is_sufficient_contribution():
    gate = evaluate(
        proposal(lambda_test_preregistered=True)
    )

    assert gate.include
    assert gate.scientific_contribution_count == 1
    assert (
        "prospectively_registered_independent_lambda_test"
        in gate.contributions
    )


def test_new_forcing_regime_alone_does_not_license_addition():
    gate = evaluate(
        proposal(
            forcing_regime_is_new=True,
            raw_data_available=True,
        )
    )

    assert not gate.include
    assert gate.contributions == ("new_forcing_regime",)
    assert "NO_REGISTERED_ENDPOINT" in gate.blockers


def test_new_forcing_plus_actuator_discriminator_can_license_same_taxon_perturbation():
    gate = evaluate(
        proposal(
            phase_coordinate_id=None,
            segment_scale_id=None,
            forcing_regime_is_new=True,
            prospective_actuator_discriminator=True,
            raw_data_available=True,
        )
    )

    assert gate.include
    assert gate.lambda_evidence_requested is False
    assert gate.actuator_evidence_requested is True
    assert gate.coordinate_compatible is None
    assert gate.segment_scale_compatible is None
    assert gate.contributes_to_lambda_synthesis is False
    assert gate.contributes_actuator_only is True
    assert gate.contributions == (
        "new_forcing_regime",
        "prospective_actuator_mechanism_discriminator",
    )


def test_lambda_boundary_prediction_can_license_addition():
    gate = evaluate(
        proposal(
            tests_lambda_boundary_or_sign_change=True,
        )
    )

    assert gate.include
    assert gate.contributions == (
        "predeclared_lambda_boundary_or_sign_change",
    )


def test_system_specific_actuator_discriminator_can_license_addition():
    gate = evaluate(
        proposal(
            prospective_actuator_discriminator=True,
        )
    )

    assert gate.include
    assert gate.contributions == (
        "prospective_actuator_mechanism_discriminator",
    )
    assert gate.contributes_to_lambda_synthesis is False
    assert gate.contributes_actuator_only is True


def test_reused_independent_test_id_is_rejected():
    gate = evaluate(
        proposal(
            independent_test_id="A_lambda_holdout",
            lambda_test_preregistered=True,
        )
    )

    assert not gate.include
    assert "INDEPENDENT_TEST_ID_ALREADY_USED" in gate.blockers


def test_phase_coordinate_mismatch_is_hard_blocker():
    gate = evaluate(
        proposal(
            phase_coordinate_id="arrival_date_residual",
            lambda_test_preregistered=True,
        )
    )

    assert not gate.include
    assert "PHASE_COORDINATE_INCOMPATIBLE" in gate.blockers


def test_segment_scale_mismatch_is_hard_blocker():
    gate = evaluate(
        proposal(
            segment_scale_id="whole_route",
            lambda_test_preregistered=True,
        )
    )

    assert not gate.include
    assert "SEGMENT_SCALE_INCOMPATIBLE" in gate.blockers


def test_multiple_contributions_are_recorded_without_creating_a_score():
    gate = evaluate(
        proposal(
            lambda_test_preregistered=True,
            forcing_regime_is_new=True,
            tests_lambda_boundary_or_sign_change=True,
            prospective_actuator_discriminator=True,
        )
    )

    assert gate.include
    assert gate.scientific_contribution_count == 4
    assert len(gate.contributions) == 4


def test_empty_canonical_coordinate_is_rejected():
    with pytest.raises(ValueError):
        evaluate_taxon_inclusion(
            proposal(lambda_test_preregistered=True),
            canonical_phase_coordinate_id="",
            canonical_segment_scale_id=COMMON_SCALE,
            existing_independent_test_ids=EXISTING,
        )


def test_actuator_only_evidence_does_not_require_phase_coordinate():
    row = TaxonInclusionProposal(
        system_name="industrial_mule_deer_perturbation",
        independent_test_id="aikens_actuator_perturbation",
        forcing_regime="industrial_development",
        lambda_test_preregistered=False,
        forcing_regime_is_new=True,
        tests_lambda_boundary_or_sign_change=False,
        prospective_actuator_discriminator=True,
        phase_coordinate_id=None,
        segment_scale_id=None,
        raw_data_available=True,
    )
    gate = evaluate(row)

    assert gate.include
    assert gate.coordinate_compatible is None
    assert gate.segment_scale_compatible is None
    assert gate.contributes_actuator_only
    assert not gate.contributes_to_lambda_synthesis


def test_within_system_lambda_perturbation_is_included_without_cross_system_pooling():
    gate = evaluate(
        proposal(
            system_name="industrial_mule_deer_lambda_perturbation",
            independent_test_id="aikens2022_lambda_perturbation_v1",
            phase_coordinate_id="signed_days_relative_to_local_peak_IRG",
            segment_scale_id="fixed_24h_spring_migration_interval",
            forcing_regime="industrial_development_route_boundary",
            forcing_regime_is_new=True,
            within_system_lambda_perturbation=True,
            raw_data_available=True,
        )
    )

    assert gate.include
    assert not gate.contributes_to_lambda_synthesis
    assert gate.contributes_within_system_lambda_perturbation
    assert not gate.contributes_actuator_only
    assert (
        "prospective_within_system_lambda_perturbation"
        in gate.contributions
    )
    assert gate.coordinate_compatible is True
    assert gate.segment_scale_compatible is True


def test_within_system_lambda_perturbation_requires_declared_local_coordinate_and_scale():
    gate = evaluate(
        proposal(
            system_name="bad_within_system_test",
            independent_test_id="bad_within_system_test_v1",
            phase_coordinate_id=None,
            segment_scale_id=None,
            within_system_lambda_perturbation=True,
        )
    )

    assert not gate.include
    assert "WITHIN_SYSTEM_PHASE_COORDINATE_MISSING" in gate.blockers
    assert "WITHIN_SYSTEM_SEGMENT_SCALE_MISSING" in gate.blockers
