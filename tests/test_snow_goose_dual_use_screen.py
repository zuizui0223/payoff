import pytest

from src.snow_goose_dual_use_screen import (
    classify_dual_use_compensation_signal,
    evaluate_compensation_screen_estimability,
)


def test_estimability_gate_passes_registered_minima():
    gate = evaluate_compensation_screen_estimability(
        individuals=30,
        years=4,
        origin_contexts=3,
        transitions=100,
        context_year_cells=12,
        predictive_connectivity_sd=0.03,
        wait_days_sd=1.0,
    )
    assert gate.estimable
    assert gate.reasons == ()


def test_estimability_gate_fails_closed_on_all_dimensions():
    gate = evaluate_compensation_screen_estimability(
        individuals=29,
        years=3,
        origin_contexts=2,
        transitions=99,
        context_year_cells=11,
        predictive_connectivity_sd=0.029,
        wait_days_sd=0.0,
    )
    assert not gate.estimable
    assert len(gate.reasons) == 7


def test_supported_negative_interaction_blocks_fixed_cost_promotion():
    result = classify_dual_use_compensation_signal(
        estimable=True,
        interaction_estimate=-0.20,
        interaction_se=0.05,
        loo_all_negative=True,
    )
    assert result.status == "DUAL_USE_BEHAVIORAL_SIGNAL_SUPPORTED"
    assert result.ci_high_95 < 0.0
    assert "not licensed" in result.interpretation


def test_null_does_not_confirm_exogeneity():
    result = classify_dual_use_compensation_signal(
        estimable=True,
        interaction_estimate=-0.02,
        interaction_se=0.05,
        loo_all_negative=True,
    )
    assert (
        result.status
        == "DUAL_USE_NOT_DEMONSTRATED_EXOGENEITY_UNRESOLVED"
    )
    assert "not an equivalence test" in result.interpretation


def test_not_estimable_never_returns_dual_use_support():
    result = classify_dual_use_compensation_signal(
        estimable=False,
        interaction_estimate=None,
        interaction_se=None,
        loo_all_negative=None,
    )
    assert result.status == "NOT_ESTIMABLE"



def test_ci_support_without_loo_sign_stability_fails_closed():
    result = classify_dual_use_compensation_signal(
        estimable=True,
        interaction_estimate=-0.20,
        interaction_se=0.05,
        loo_all_negative=False,
    )
    assert (
        result.status
        == "DUAL_USE_NOT_DEMONSTRATED_EXOGENEITY_UNRESOLVED"
    )
