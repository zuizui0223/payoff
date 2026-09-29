import pytest

from src.greater_snow_goose_cue_uptake import (
    FROZEN_Q_GRID,
    adjudicate_threshold_folds,
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
        context_years=12,
        predictive_connectivity_sd=0.03,
        minimum_within_context_connectivity_sd=0.001,
    )
    assert result.estimable
    assert result.reasons == ()


def test_estimability_gate_fails_closed():
    result = evaluate_estimability(
        individuals=29,
        years=3,
        contexts=2,
        departure_events=99,
        context_years=11,
        predictive_connectivity_sd=0.029,
        minimum_within_context_connectivity_sd=0.0,
    )
    assert not result.estimable
    assert len(result.reasons) == 7


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



def _flat_candidates(base=0.50):
    return {q: [base, base, base, base] for q in FROZEN_Q_GRID}


def test_threshold_gate_supports_unique_interior_candidate():
    candidates = _flat_candidates(0.50)
    candidates[0.575] = [0.40, 0.41, 0.39, 0.40]
    candidates[0.550] = [0.46, 0.47, 0.45, 0.46]
    candidates[0.600] = [0.47, 0.48, 0.46, 0.47]
    result = adjudicate_threshold_folds(
        no_threshold_losses=[0.55, 0.54, 0.56, 0.55],
        candidate_losses=candidates,
    )
    assert result.status == "SUPPORTED_BEHAVIORAL_THRESHOLD_LIKE"
    assert result.selected_threshold_q == pytest.approx(0.575)
    assert result.reasons == ()


def test_threshold_gate_rejects_adjacent_one_se_tie():
    candidates = _flat_candidates(0.60)
    candidates[0.575] = [0.400, 0.410, 0.390, 0.400]
    # Mean loss is slightly worse than the selected candidate, but the
    # paired individual-level difference is noisy enough to remain within 1 SE.
    candidates[0.550] = [0.360, 0.470, 0.350, 0.460]
    candidates[0.600] = [0.470, 0.480, 0.460, 0.470]
    result = adjudicate_threshold_folds(
        no_threshold_losses=[0.55, 0.54, 0.56, 0.55],
        candidate_losses=candidates,
    )
    assert result.status == "THRESHOLD_NOT_IDENTIFIED"
    assert "LOWER_ADJACENT_TIED_WITHIN_1SE" in result.reasons


def test_threshold_gate_rejects_grid_endpoint():
    candidates = _flat_candidates(0.60)
    candidates[0.500] = [0.40, 0.41, 0.39, 0.40]
    result = adjudicate_threshold_folds(
        no_threshold_losses=[0.55, 0.54, 0.56, 0.55],
        candidate_losses=candidates,
    )
    assert result.status == "THRESHOLD_NOT_IDENTIFIED"
    assert "BEST_THRESHOLD_IS_GRID_ENDPOINT" in result.reasons


def test_threshold_gate_requires_beating_no_threshold():
    candidates = _flat_candidates(0.60)
    candidates[0.575] = [0.50, 0.51, 0.49, 0.50]
    candidates[0.550] = [0.57, 0.58, 0.56, 0.57]
    candidates[0.600] = [0.58, 0.59, 0.57, 0.58]
    result = adjudicate_threshold_folds(
        no_threshold_losses=[0.45, 0.44, 0.46, 0.45],
        candidate_losses=candidates,
    )
    assert result.status == "THRESHOLD_NOT_IDENTIFIED"
    assert "DOES_NOT_BEAT_NO_THRESHOLD" in result.reasons


def test_threshold_gate_requires_complete_frozen_grid():
    candidates = _flat_candidates(0.50)
    candidates.pop(0.700)
    result = adjudicate_threshold_folds(
        no_threshold_losses=[0.55, 0.54, 0.56, 0.55],
        candidate_losses=candidates,
    )
    assert result.status == "THRESHOLD_NOT_IDENTIFIED"
    assert "INCOMPLETE_FROZEN_Q_GRID" in result.reasons



def test_estimability_requires_within_context_q_variation():
    result = evaluate_estimability(
        individuals=30,
        years=4,
        contexts=3,
        departure_events=120,
        context_years=12,
        predictive_connectivity_sd=0.10,
        minimum_within_context_connectivity_sd=0.0,
    )
    assert not result.estimable
    assert "NO_WITHIN_CONTEXT_CONNECTIVITY_VARIATION" in result.reasons
