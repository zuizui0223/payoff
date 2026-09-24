import pytest

from src.phase_retention_contrast import (
    PhaseRetentionContrastObservation,
    PhaseRetentionContrastRegistration,
    evaluate_phase_retention_contrast,
)


def registration(**overrides):
    payload = dict(
        system_name="mule_deer_industrial",
        independent_test_id="aikens_lambda_perturbation_v1",
        phase_coordinate_id="signed_green_wave_phase_error_days",
        segment_scale_id="fixed_24h_migration_interval",
        group_a="small_development",
        group_b="large_development",
        expected_direction="b_greater_than_a",
        max_p_value=0.05,
        min_abs_difference=0.0,
    )
    payload.update(overrides)
    return PhaseRetentionContrastRegistration(**payload)


def observation(**overrides):
    payload = dict(
        system_name="mule_deer_industrial",
        independent_test_id="aikens_lambda_perturbation_v1",
        phase_coordinate_id="signed_green_wave_phase_error_days",
        segment_scale_id="fixed_24h_migration_interval",
        group_a="small_development",
        group_b="large_development",
        lambda_a=0.30,
        lambda_b=0.55,
        p_difference=0.01,
    )
    payload.update(overrides)
    return PhaseRetentionContrastObservation(**payload)


def test_phase_retention_contrast_passes_registered_direction_and_support():
    gate = evaluate_phase_retention_contrast(
        registration(),
        observation(),
    )

    assert gate.passed
    assert gate.direction_passed
    assert gate.magnitude_passed
    assert gate.support_passed
    assert gate.lambda_difference_b_minus_a == pytest.approx(0.25)


def test_phase_retention_contrast_fails_wrong_direction():
    gate = evaluate_phase_retention_contrast(
        registration(),
        observation(lambda_a=0.55, lambda_b=0.30),
    )

    assert not gate.passed
    assert not gate.direction_passed
    assert gate.support_passed


def test_phase_retention_contrast_fails_without_registered_support():
    gate = evaluate_phase_retention_contrast(
        registration(),
        observation(p_difference=0.20),
    )

    assert not gate.passed
    assert gate.direction_passed
    assert not gate.support_passed


def test_phase_retention_contrast_requires_matching_coordinate():
    with pytest.raises(ValueError, match="phase_coordinate_id"):
        evaluate_phase_retention_contrast(
            registration(),
            observation(
                phase_coordinate_id="different_phase_coordinate"
            ),
        )


def test_phase_retention_contrast_requires_matching_segment_scale():
    with pytest.raises(ValueError, match="segment_scale_id"):
        evaluate_phase_retention_contrast(
            registration(),
            observation(segment_scale_id="whole_route"),
        )


def test_phase_retention_contrast_can_preregister_nonzero_effect_floor():
    gate = evaluate_phase_retention_contrast(
        registration(min_abs_difference=0.30),
        observation(lambda_a=0.30, lambda_b=0.55),
    )

    assert not gate.passed
    assert gate.direction_passed
    assert not gate.magnitude_passed


def test_new_forcing_lambda_contrast_does_not_require_new_taxon():
    gate = evaluate_phase_retention_contrast(
        registration(
            system_name="Odocoileus hemionus",
            group_a="small_development",
            group_b="large_development",
        ),
        observation(
            system_name="Odocoileus hemionus",
            group_a="small_development",
            group_b="large_development",
        ),
    )
    assert gate.passed


def test_phase_retention_contrast_accepts_fit_provenance_metadata():
    provenance = {
        "source_pairs": "outputs/fixed_24h_phase_pairs.csv",
        "fit_receipt": "outputs/phase_contrast_fit_receipt.json",
        "delta_lambda_b_minus_a": 0.25,
        "delta_lambda_se": 0.04,
        "total_pairs": 240,
        "total_animals": 20,
    }
    gate = evaluate_phase_retention_contrast(
        registration(),
        observation(fit_provenance=provenance),
    )

    assert gate.passed
    assert gate.observation.fit_provenance == provenance


def test_phase_retention_contrast_rejects_invalid_fit_provenance():
    with pytest.raises(ValueError, match="fit_provenance"):
        observation(fit_provenance="not-a-mapping")
