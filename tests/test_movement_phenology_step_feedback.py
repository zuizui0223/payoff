import pytest

from analysis.movement_phenology.step_feedback import (
    correction_fraction,
    is_locally_contracting,
    phase_transfer_slope_from_stopover_gain,
    stopover_gain_from_slope,
)


def test_no_stopover_response_means_no_phase_contraction():
    assert phase_transfer_slope_from_stopover_gain(0.0) == pytest.approx(1.0)
    assert correction_fraction(1.0) == pytest.approx(0.0)


def test_unit_stopover_gain_resets_phase_in_one_step():
    assert phase_transfer_slope_from_stopover_gain(1.0) == pytest.approx(0.0)
    assert correction_fraction(0.0) == pytest.approx(1.0)
    assert is_locally_contracting(0.0)


def test_stable_overshoot_is_allowed():
    lam = phase_transfer_slope_from_stopover_gain(1.5)
    assert lam == pytest.approx(-0.5)
    assert is_locally_contracting(lam)


def test_stopover_stability_boundary():
    assert is_locally_contracting(
        phase_transfer_slope_from_stopover_gain(0.5)
    )
    assert is_locally_contracting(
        phase_transfer_slope_from_stopover_gain(1.5)
    )
    assert not is_locally_contracting(
        phase_transfer_slope_from_stopover_gain(2.1)
    )


def test_svalbard_stopover_slopes_predict_strong_contraction():
    g_r1_r2 = stopover_gain_from_slope(-0.9102342618415553)
    g_r2_r4 = stopover_gain_from_slope(-0.5889955062414662)
    assert phase_transfer_slope_from_stopover_gain(g_r1_r2) == pytest.approx(
        0.0897657381584447
    )
    assert phase_transfer_slope_from_stopover_gain(g_r2_r4) == pytest.approx(
        0.4110044937585338
    )
