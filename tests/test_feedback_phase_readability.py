import pytest

from src.feedback_phase_readability import local_phase_readability
from src.irg_reconstruction import (
    DoubleLogisticParameters,
    PeakIRGFit,
    ProcessedNDVI,
)


def _fit(*, peak=0.04, scale=20.0, rmse=0.02):
    gamma = 1.0986122886681098 / scale
    return PeakIRGFit(
        parameters=DoubleLogisticParameters(
            alpha=0.0,
            beta=1.0,
            gamma=gamma,
            delta=120.0,
            epsilon=0.03,
            theta=280.0,
        ),
        peak_irg_doy=120,
        peak_irg_value=peak,
        spring_scale_days=scale,
        fit_rmse=rmse,
        processed=ProcessedNDVI(
            doy=(1, 20, 40, 60, 80, 100, 120, 140),
            scaled_ndvi=(0, 0, 0.05, 0.1, 0.3, 0.6, 0.9, 1.0),
            winter_baseline=0.1,
            upper_scale_reference=0.8,
            snow_release_doy=60,
            valid_observations=8,
        ),
        optimizer_success=True,
        optimizer_message="fixture",
    )


def test_primary_readability_is_peak_irg():
    out = local_phase_readability(_fit(peak=0.05, scale=25.0, rmse=0.01))
    assert out.peak_irg == pytest.approx(0.05)


def test_inverse_spring_scale_sensitivity():
    out = local_phase_readability(_fit(scale=20.0))
    assert out.inverse_spring_scale == pytest.approx(0.05)


def test_snr_uses_no_arbitrary_epsilon():
    out = local_phase_readability(_fit(peak=0.04, rmse=0.02))
    assert out.peak_irg_over_rmse == pytest.approx(2.0)


def test_zero_rmse_marks_snr_unavailable_instead_of_inventing_floor():
    out = local_phase_readability(_fit(rmse=0.0))
    assert out.peak_irg_over_rmse is None
