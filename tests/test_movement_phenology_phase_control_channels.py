import pytest

from analysis.movement_phenology.phase_control_channels import (
    correction_strength,
    environmental_predictability_r2,
    stationary_phase_variance,
)


def test_stationary_phase_variance_separates_noise_and_feedback():
    assert stationary_phase_variance(4.0, 0.0, 0.0) == pytest.approx(4.0)
    assert stationary_phase_variance(4.0, 0.0, 0.5) == pytest.approx(4 / 0.75)


def test_predictability_and_feedback_can_improve_precision_independently():
    baseline = stationary_phase_variance(9.0, 1.0, 0.6)
    better_info = stationary_phase_variance(4.0, 1.0, 0.6)
    stronger_feedback = stationary_phase_variance(9.0, 1.0, 0.2)
    assert better_info < baseline
    assert stronger_feedback < baseline


def test_correction_strength_handles_overshoot_symmetrically():
    assert correction_strength(0.2) == pytest.approx(0.8)
    assert correction_strength(-0.2) == pytest.approx(0.8)
    assert correction_strength(1.2) == pytest.approx(-0.2)


def test_environmental_predictability_r2():
    assert environmental_predictability_r2(10.0, 2.0) == pytest.approx(0.8)


def test_stationary_gate_fails_closed():
    with pytest.raises(ValueError):
        stationary_phase_variance(1, 1, 1.0)
    with pytest.raises(ValueError):
        stationary_phase_variance(-1, 1, 0.2)
