import pytest

from src.greater_snow_goose_information_bridge import (
    gaussian_binary_accuracy,
    perturbation_cost_on_probability_scale,
    threshold_shift_from_context_cost,
)


@pytest.mark.parametrize(
    "rho, expected",
    [
        (0.03, 0.5095507295604322),
        (0.25, 0.5804306232551663),
        (0.11, 0.5350850864964299),
        (0.35, 0.6138184173040148),
        (0.37, 0.6206423182403581),
    ],
)
def test_published_temperature_correlations_map_to_expected_q_bridge(rho, expected):
    assert gaussian_binary_accuracy(rho) == pytest.approx(expected)


def test_2007_four_day_perturbation_probability_drop():
    p0, p4, absolute, relative = perturbation_cost_on_probability_scale(
        -1.80, -0.37, delayed_days=4
    )
    assert p0 == pytest.approx(0.1418510649)
    assert p4 == pytest.approx(0.0362637164)
    assert absolute == pytest.approx(0.1055873485)
    assert relative == pytest.approx(0.7443535838)


def test_2008_favourable_year_has_small_descriptive_drop():
    _, _, absolute, relative = perturbation_cost_on_probability_scale(
        -1.07, -0.03, delayed_days=4
    )
    assert absolute == pytest.approx(0.0221441484)
    assert relative == pytest.approx(0.0867027447)


def test_2009_unfavourable_year_has_large_descriptive_drop():
    _, _, absolute, relative = perturbation_cost_on_probability_scale(
        -1.37, -0.38, delayed_days=4
    )
    assert absolute == pytest.approx(0.1499697280)
    assert relative == pytest.approx(0.7401532014)


def test_context_cost_gap_moves_threshold_exactly():
    assert threshold_shift_from_context_cost(0.10, 0.30, 1.60) == pytest.approx(0.125)
