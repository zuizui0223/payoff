import pytest

from src.greater_snow_goose_cue_uptake import (
    FROZEN_Q_GRID,
    evaluate_estimability,
    gaussian_binary_q,
    preoutcome_training_valid,
    threshold_active,
)


def test_estimability_gate_passes_registered_minima():
    result = evaluate_estimability(
        individuals=30,
        years=4,
        contexts=3,
        departure_events=100,
        predictive_connectivity_sd=0.03,
    )
    assert result.estimable
    assert result.reasons == ()


def test_estimability_gate_fails_closed():
    result = evaluate_estimability(
        individuals=29,
        years=3,
        contexts=2,
        departure_events=99,
        predictive_connectivity_sd=0.029,
    )
    assert not result.estimable
    assert len(result.reasons) == 5


def test_gaussian_q_bridge_matches_existing_contract():
    assert gaussian_binary_q(0.0) == pytest.approx(0.5)
    assert gaussian_binary_q(1.0) == pytest.approx(1.0)


def test_threshold_grid_is_frozen():
    assert FROZEN_Q_GRID == (
        0.500, 0.525, 0.550, 0.575, 0.600,
        0.625, 0.650, 0.675, 0.700,
    )
    assert threshold_active(0.625, 0.625)
    assert not threshold_active(0.624, 0.625)
    with pytest.raises(ValueError):
        threshold_active(0.63, 0.63)


def test_predictive_connectivity_must_be_preoutcome():
    assert preoutcome_training_valid(
        focal_year=2019,
        training_end_year=2018,
        training_years=20,
    )
    assert not preoutcome_training_valid(
        focal_year=2019,
        training_end_year=2019,
        training_years=20,
    )
    assert not preoutcome_training_valid(
        focal_year=2019,
        training_end_year=2018,
        training_years=14,
    )
