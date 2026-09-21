from math import isclose

import pytest

from src.irg_reconstruction import (
    DoubleLogisticParameters,
    NDVIObservation,
    double_logistic_derivative,
    double_logistic_ndvi,
    fit_peak_irg,
    peak_irg_day_from_parameters,
    preprocess_ndvi,
)


def synthetic_observations():
    params = DoubleLogisticParameters(
        alpha=0.05,
        beta=0.85,
        gamma=0.08,
        delta=120.0,
        epsilon=0.04,
        theta=285.0,
    )
    rows = []
    for doy in range(1, 362, 8):
        rows.append(
            NDVIObservation(
                doy=doy,
                ndvi=double_logistic_ndvi(
                    float(doy),
                    params,
                ),
                snow_free=(doy >= 73),
                quality_good=True,
            )
        )
    return rows


def test_peak_irg_for_separated_seasons_is_near_spring_midpoint():
    params = DoubleLogisticParameters(
        alpha=0.0,
        beta=1.0,
        gamma=0.10,
        delta=120.0,
        epsilon=0.03,
        theta=300.0,
    )
    peak_doy, peak_value = peak_irg_day_from_parameters(
        params
    )

    assert abs(peak_doy - 120) <= 1
    assert peak_value > 0.02
    assert double_logistic_derivative(
        float(peak_doy),
        params,
    ) == pytest.approx(peak_value)


def test_preprocess_uses_two_consecutive_snow_free_release():
    rows = []
    for doy, snow_free, value in (
        (1, False, 0.10),
        (9, False, 0.11),
        (17, False, 0.12),
        (25, False, 0.10),
        (33, False, 0.11),
        (41, False, 0.10),
        (49, False, 0.12),
        (57, False, 0.11),
        (65, True, 0.15),
        (73, False, 0.16),
        (81, True, 0.20),
        (89, True, 0.30),
        (97, True, 0.45),
        (105, True, 0.60),
        (113, True, 0.75),
        (121, True, 0.82),
        (129, True, 0.85),
        (137, True, 0.86),
    ):
        rows.append(
            NDVIObservation(
                doy=doy,
                ndvi=value,
                snow_free=snow_free,
            )
        )

    processed = preprocess_ndvi(rows)

    assert processed.snow_release_doy == 81
    assert processed.valid_observations == len(rows)
    assert 0.0 <= min(processed.scaled_ndvi)
    assert max(processed.scaled_ndvi) <= 1.0


def test_preprocess_rejects_missing_snow_flags_in_strict_mode():
    rows = [
        NDVIObservation(
            doy=doy,
            ndvi=0.2 + 0.001 * doy,
            snow_free=(None if doy == 81 else doy >= 73),
        )
        for doy in range(1, 130, 8)
    ]
    with pytest.raises(ValueError, match="snow_free"):
        preprocess_ndvi(rows)


def test_quality_bad_observations_are_removed_before_fit_contract():
    rows = synthetic_observations()
    rows.append(
        NDVIObservation(
            doy=366,
            ndvi=1.0,
            snow_free=True,
            quality_good=False,
        )
    )
    processed = preprocess_ndvi(rows)
    assert processed.valid_observations == len(rows) - 1
    assert 366 not in processed.doy


def test_peak_irg_rejects_reversed_season_midpoints():
    params = DoubleLogisticParameters(
        alpha=0.0,
        beta=1.0,
        gamma=0.05,
        delta=250.0,
        epsilon=0.04,
        theta=180.0,
    )
    with pytest.raises(ValueError, match="autumn midpoint"):
        peak_irg_day_from_parameters(params)


def test_spring_scale_is_logistic_quarter_to_three_quarter_scale():
    params = DoubleLogisticParameters(
        alpha=0.0,
        beta=1.0,
        gamma=0.1,
        delta=120.0,
        epsilon=0.03,
        theta=280.0,
    )
    assert isclose(
        params.spring_scale_days,
        10.986122886681096,
        rel_tol=1e-12,
    )


def test_optional_scipy_fit_recovers_synthetic_peak_irg():
    pytest.importorskip("scipy")
    processed = preprocess_ndvi(
        synthetic_observations()
    )
    fit = fit_peak_irg(processed)

    assert fit.optimizer_success
    assert abs(fit.peak_irg_doy - 120) <= 10
    assert fit.fit_rmse < 0.12
    assert fit.spring_scale_days > 0.0
