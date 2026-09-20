from math import isclose

import pytest

from src.tracking_empirical_parameterization import (
    build_tracking_parameterization,
    climate_velocity_from_wave_speed,
    implied_component_variances,
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
