import pytest

from src.snow_goose_j_mechanism import (
    classify_j_mechanism,
    evaluate_j_mechanism_gate,
)


def test_gate_passes_minima():
    gate = evaluate_j_mechanism_gate(
        females=30,
        capture_groups=6,
        duration_levels=2,
        min_group_size=2,
    )
    assert gate.estimable
    assert gate.reasons == ()


def test_gate_fails_closed():
    gate = evaluate_j_mechanism_gate(
        females=29,
        capture_groups=5,
        duration_levels=1,
        min_group_size=1,
    )
    assert not gate.estimable
    assert len(gate.reasons) == 4


def test_negative_clustered_signal_is_j_like_only():
    result = classify_j_mechanism(
        estimable=True,
        days_estimate=-0.20,
        days_se=0.05,
    )
    assert result.status == (
        "FED_CAPTIVITY_PHYSIOLOGICAL_J_SIGNAL_SUPPORTED"
    )
    assert result.ci_high_95 < 0
    assert "not identify natural J or D_eff" in result.interpretation


def test_null_does_not_establish_zero_direct_cost():
    result = classify_j_mechanism(
        estimable=True,
        days_estimate=-0.01,
        days_se=0.05,
    )
    assert result.status == (
        "FED_CAPTIVITY_PHYSIOLOGICAL_J_SIGNAL_NOT_SUPPORTED"
    )
    assert "does not establish J=0" in result.interpretation


def test_not_estimable():
    result = classify_j_mechanism(
        estimable=False,
        days_estimate=None,
        days_se=None,
    )
    assert result.status == "NOT_ESTIMABLE"
