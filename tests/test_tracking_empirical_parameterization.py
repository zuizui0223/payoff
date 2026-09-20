from math import isclose

import pytest

from src.tracking_empirical_parameterization import (
    audit_residual_compression,
    build_tracking_parameterization,
    climate_velocity_from_wave_speed,
    implied_component_variances,
    identify_tracking_fitness_from_matched_contrasts,
    implied_directional_movement_moments,
    infer_directional_movement_kernel_from_moments,
    infer_movement_kernel_from_component_variances,
    infer_phenology_rate_from_residual_pair,
    infer_quadratic_architecture_cost,
    infer_quadratic_mismatch_strength,
    infer_tracking_rate_from_correction_fraction,
)


def test_movement_variance_inverse_round_trip():
    estimate = infer_movement_kernel_from_component_variances(
        variance_x=0.12,
        variance_y=0.03,
        patch_spacing=0.5,
    )
    recovered_x, recovered_y = implied_component_variances(
        estimate.migration_rate,
        estimate.x_weight,
        estimate.y_weight,
        patch_spacing=0.5,
    )
    assert isclose(recovered_x, 0.12, rel_tol=1e-12, abs_tol=1e-12)
    assert isclose(recovered_y, 0.03, rel_tol=1e-12, abs_tol=1e-12)
    assert isclose(
        estimate.anisotropy_ratio_y_over_x,
        0.25,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_zero_movement_keeps_rate_zero_and_marks_anisotropy_unidentified():
    estimate = infer_movement_kernel_from_component_variances(
        0.0,
        0.0,
        patch_spacing=1.0,
    )
    assert estimate.migration_rate == 0.0
    assert estimate.moving_fraction == 0.0
    assert not estimate.anisotropy_identified
    assert estimate.anisotropy_ratio_y_over_x is None


def test_one_step_kernel_rejects_variance_beyond_support():
    with pytest.raises(ValueError):
        infer_movement_kernel_from_component_variances(
            variance_x=0.8,
            variance_y=0.3,
            patch_spacing=1.0,
        )


def test_tracking_rate_inverse_round_trip():
    for q in (0.0, 0.1, 0.5, 0.9):
        rate = infer_tracking_rate_from_correction_fraction(q)
        implied = 1.0 - __import__("math").exp(-rate)
        assert isclose(implied, q, rel_tol=1e-12, abs_tol=1e-12)


def test_phenology_residual_pair_recovers_rate():
    rate = infer_phenology_rate_from_residual_pair(
        residual_before=10.0,
        residual_after=5.0,
    )
    assert isclose(
        rate,
        __import__("math").log(2.0),
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_phenology_residual_pair_rejects_overshoot():
    with pytest.raises(ValueError):
        infer_phenology_rate_from_residual_pair(
            residual_before=10.0,
            residual_after=-1.0,
        )


def test_wave_speed_conversion():
    assert isclose(
        climate_velocity_from_wave_speed(
            spatial_gradient=0.2,
            wave_speed=3.0,
        ),
        0.6,
        abs_tol=1e-12,
    )


def test_quadratic_strength_inverses():
    assert isclose(
        infer_quadratic_mismatch_strength(
            mismatch=2.0,
            growth_loss=1.0,
        ),
        0.5,
        abs_tol=1e-12,
    )
    assert isclose(
        infer_quadratic_architecture_cost(
            tracking_rate=0.5,
            growth_cost=0.05,
        ),
        0.2,
        abs_tol=1e-12,
    )


def test_build_parameterization_keeps_unidentified_growth_terms_out():
    result = build_tracking_parameterization(
        variance_x=0.08,
        variance_y=0.02,
        patch_spacing=0.5,
        spatial_gradient=0.2,
        wave_speed=0.3,
        phenology_correction_fraction=0.25,
        phenology_scale=0.1,
        max_abs_phenology_shift=20.0,
    )
    assert result.climate_velocity == pytest.approx(0.06)
    assert result.dispersal_x_weight == pytest.approx(0.8)
    assert result.dispersal_y_weight == pytest.approx(0.2)
    assert result.phenology_rate > 0.0
    assert result.max_abs_phenology_shift == 20.0


def test_matched_growth_contrasts_recover_tracking_fitness_terms():
    baseline = 0.4
    abiotic_strength = 1.2
    interaction_strength = 0.8
    migration_cost = 0.10
    phenology_cost = 0.05
    joint_cost = 0.03

    e = 0.5
    mismatch = 0.4
    m = 0.6
    h = 0.7
    jm = 0.4
    jh = 0.5

    estimate = identify_tracking_fitness_from_matched_contrasts(
        baseline_growth=baseline,
        abiotic_growth=(
            baseline - 0.5 * abiotic_strength * e * e
        ),
        abiotic_mismatch=e,
        interaction_growth=(
            baseline
            - 0.5 * interaction_strength * mismatch * mismatch
        ),
        interaction_mismatch=mismatch,
        migration_growth=(
            baseline - migration_cost * m * m
        ),
        migration_rate=m,
        phenology_growth=(
            baseline - phenology_cost * h * h
        ),
        phenology_rate=h,
        joint_growth=(
            baseline
            - migration_cost * jm * jm
            - phenology_cost * jh * jh
            - joint_cost * jm * jh
        ),
        joint_migration_rate=jm,
        joint_phenology_rate=jh,
    )

    assert estimate.baseline_growth == pytest.approx(baseline)
    assert estimate.abiotic_strength == pytest.approx(
        abiotic_strength
    )
    assert estimate.interaction_strength == pytest.approx(
        interaction_strength
    )
    assert estimate.migration_cost == pytest.approx(migration_cost)
    assert estimate.phenology_cost == pytest.approx(phenology_cost)
    assert estimate.joint_cost == pytest.approx(joint_cost)


def test_matched_growth_contrasts_reject_negative_penalty_identification():
    with pytest.raises(ValueError):
        identify_tracking_fitness_from_matched_contrasts(
            baseline_growth=0.4,
            abiotic_growth=0.5,
            abiotic_mismatch=0.5,
            interaction_growth=0.3,
            interaction_mismatch=0.5,
            migration_growth=0.3,
            migration_rate=0.5,
            phenology_growth=0.3,
            phenology_rate=0.5,
            joint_growth=0.2,
            joint_migration_rate=0.5,
            joint_phenology_rate=0.5,
        )


def test_residual_compression_audit_classifies_sign_crossing():
    audit = audit_residual_compression(
        residual_before=-30.0,
        residual_after=4.0,
    )
    assert audit.status == "sign_crossing_or_overshoot"
    assert not audit.monotone_first_order_compatible
    assert audit.compression_ratio is None


def test_residual_compression_audit_classifies_monotone_compression():
    audit = audit_residual_compression(
        residual_before=20.0,
        residual_after=11.0,
    )
    assert audit.status == "monotone_compression"
    assert audit.monotone_first_order_compatible
    assert audit.compression_ratio == pytest.approx(0.55)
    assert audit.log_compression == pytest.approx(
        -__import__("math").log(0.55)
    )


def test_residual_compression_audit_rejects_amplification():
    audit = audit_residual_compression(
        residual_before=5.0,
        residual_after=8.0,
    )
    assert audit.status == "mismatch_amplification"
    assert not audit.monotone_first_order_compatible


def test_directional_movement_moment_inverse_round_trip():
    migration_rate = 0.7
    x_weight = 0.8
    y_weight = 0.2
    x_bias = 0.6
    y_bias = -0.25
    patch_spacing = 2.0

    mean_x, mean_y, second_x, second_y = (
        implied_directional_movement_moments(
            migration_rate,
            x_weight,
            y_weight,
            x_bias,
            y_bias,
            patch_spacing,
        )
    )
    estimate = infer_directional_movement_kernel_from_moments(
        mean_x,
        mean_y,
        second_x,
        second_y,
        patch_spacing,
    )

    assert estimate.migration_rate == pytest.approx(migration_rate)
    assert estimate.x_weight == pytest.approx(x_weight)
    assert estimate.y_weight == pytest.approx(y_weight)
    assert estimate.x_bias == pytest.approx(x_bias)
    assert estimate.y_bias == pytest.approx(y_bias)


def test_directional_inverse_rejects_impossible_mean_given_second_moment():
    with pytest.raises(ValueError):
        infer_directional_movement_kernel_from_moments(
            mean_x=1.0,
            mean_y=0.0,
            second_moment_x=0.1,
            second_moment_y=0.0,
            patch_spacing=1.0,
        )
