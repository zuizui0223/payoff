import pytest

from src.portfolio_fragility_identification import (
    decompose_variance_change,
)


def test_identity_closes_exactly():
    r=decompose_variance_change(
        baseline_error=[-2.0,-1.0,1.0,2.0],
        individual_shift=[0.0,1.0,-0.5,2.0],
        post_weights=[1.0,2.0,1.0,3.0],
    )
    assert r.identity_residual == pytest.approx(0.0,abs=1e-12)
    assert r.observed_variance_change == pytest.approx(
        r.selection_reweighting_component+r.within_individual_component
    )


def test_selection_alone_can_change_variance():
    r=decompose_variance_change(
        baseline_error=[-3.0,-1.0,1.0,3.0],
        individual_shift=[0.0,0.0,0.0,0.0],
        post_weights=[0.1,1.0,1.0,0.1],
    )
    assert r.within_individual_component == pytest.approx(0.0)
    assert r.selection_reweighting_component < 0
    assert r.observed_variance_change < 0


def test_fragility_alone_isolated_with_equal_weights():
    r=decompose_variance_change(
        baseline_error=[-2.0,-1.0,1.0,2.0],
        individual_shift=[-2.0,-1.0,1.0,2.0],
        post_weights=[1.0,1.0,1.0,1.0],
    )
    assert r.selection_reweighting_component == pytest.approx(0.0)
    assert r.within_individual_component > 0
    assert r.observed_variance_change == pytest.approx(
        r.within_individual_component
    )


def test_selection_can_mask_within_individual_fragility():
    r=decompose_variance_change(
        baseline_error=[-4.0,-1.0,1.0,4.0],
        individual_shift=[-1.0,-1.0,1.0,1.0],
        post_weights=[0.05,1.0,1.0,0.05],
    )
    assert r.within_individual_component > 0
    assert r.selection_reweighting_component < 0
    assert r.observed_variance_change < r.within_individual_component


def test_negative_weights_rejected():
    with pytest.raises(ValueError,match="non-negative"):
        decompose_variance_change(
            baseline_error=[0.0,1.0],
            individual_shift=[0.0,0.0],
            post_weights=[1.0,-1.0],
        )
