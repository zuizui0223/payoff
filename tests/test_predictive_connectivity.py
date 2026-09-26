import pytest

from src.predictive_connectivity import (
    detrended_predictive_connectivity,
    gaussian_binary_agreement_from_correlation,
    gaussian_optimal_binary_accuracy_from_correlation,
    pearson_correlation,
    trailing_precommitment_connectivity,
)


def test_gaussian_binary_bridge_has_expected_limits():
    assert gaussian_binary_agreement_from_correlation(0.0) == pytest.approx(0.5)
    assert gaussian_binary_agreement_from_correlation(1.0) == pytest.approx(1.0)
    assert gaussian_binary_agreement_from_correlation(-1.0) == pytest.approx(0.0)
    assert gaussian_optimal_binary_accuracy_from_correlation(-1.0) == pytest.approx(1.0)


def test_detrended_connectivity_recovers_shared_interannual_signal():
    years = list(range(2000, 2008))
    anomaly = [1, -1, -1, 1, 1, -1, -1, 1]
    origin = [
        10.0 * index + anomaly[index]
        for index in range(len(years))
    ]
    destination = [
        20.0 * index + 3.0 * anomaly[index]
        for index in range(len(years))
    ]

    result = detrended_predictive_connectivity(
        years,
        origin,
        destination,
    )

    assert result.n_pairs == 8
    assert result.rho == pytest.approx(1.0)
    assert result.r_squared == pytest.approx(1.0)
    assert result.gaussian_binary_agreement == pytest.approx(1.0)


def test_detrended_connectivity_preserves_inverse_information_sign():
    years = list(range(2000, 2008))
    anomaly = [1, -1, -1, 1, 1, -1, -1, 1]
    origin = [
        10.0 * index + anomaly[index]
        for index in range(len(years))
    ]
    destination = [
        20.0 * index - 2.0 * anomaly[index]
        for index in range(len(years))
    ]

    result = detrended_predictive_connectivity(
        years,
        origin,
        destination,
    )

    assert result.rho == pytest.approx(-1.0)
    assert result.gaussian_binary_agreement == pytest.approx(0.0)
    assert result.gaussian_optimal_binary_accuracy == pytest.approx(1.0)


def test_trailing_connectivity_does_not_use_target_year():
    years = list(range(2000, 2009))
    anomaly = [1, -1, -1, 1, 1, -1, -1, 1]
    origin = [
        10.0 * index + anomaly[index]
        for index in range(8)
    ] + [999999.0]
    destination = [
        20.0 * index + 3.0 * anomaly[index]
        for index in range(8)
    ] + [-999999.0]

    result = trailing_precommitment_connectivity(
        years,
        origin,
        destination,
        target_year=2008,
        window_years=8,
    )

    assert result.n_pairs == 8
    assert result.rho == pytest.approx(1.0)


def test_trailing_connectivity_refuses_insufficient_precommitment_history():
    with pytest.raises(ValueError, match="insufficient pre-outcome"):
        trailing_precommitment_connectivity(
            [2005, 2006, 2007, 2008],
            [1.0, 2.0, 3.0, 4.0],
            [1.2, 2.1, 3.2, 100.0],
            target_year=2008,
            window_years=8,
            min_pairs=4,
        )


def test_pearson_refuses_zero_variance():
    with pytest.raises(ValueError, match="zero variance"):
        pearson_correlation(
            [1.0, 1.0, 1.0],
            [1.0, 2.0, 3.0],
        )
