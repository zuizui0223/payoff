import pytest

from src.prediction_correction_substitution import (
    actionable_phase_retention_slope,
    canonical_optimal_correction,
    canonical_pre_correction_risk,
    optimal_quadratic_correction,
    prediction_correction_balance,
)


def test_optimal_gain_and_retention_sum_to_one():
    result = optimal_quadratic_correction(
        0.4,
        correction_cost_curvature=0.8,
    )
    assert result.correction_gain + result.phase_retention == pytest.approx(1.0)


def test_better_information_reduces_pre_correction_risk():
    risks = [
        canonical_pre_correction_risk(
            0.4,
            q,
            2.0,
            1.0,
        )
        for q in (0.75, 0.8, 0.9, 1.0)
    ]
    assert risks == sorted(risks, reverse=True)
    assert risks[-1] == pytest.approx(0.0)


def test_better_information_weakens_optimal_reactive_correction():
    low_q = canonical_optimal_correction(
        0.4,
        0.80,
        2.0,
        1.0,
        correction_cost_curvature=0.4,
    )
    high_q = canonical_optimal_correction(
        0.4,
        0.95,
        2.0,
        1.0,
        correction_cost_curvature=0.4,
    )
    assert high_q.pre_correction_risk < low_q.pre_correction_risk
    assert high_q.correction_gain < low_q.correction_gain
    assert high_q.phase_retention > low_q.phase_retention


def test_perfect_information_requires_no_reactive_correction():
    result = canonical_optimal_correction(
        0.4,
        1.0,
        2.0,
        1.0,
        correction_cost_curvature=0.4,
    )
    assert result.pre_correction_risk == pytest.approx(0.0)
    assert result.correction_gain == pytest.approx(0.0)
    assert result.phase_retention == pytest.approx(1.0)
    assert result.minimized_total_loss == pytest.approx(0.0)


@pytest.mark.parametrize("q", [0.76, 0.80, 0.90, 0.99])
def test_phase_retention_increases_with_actionable_cue_accuracy(q):
    slope = actionable_phase_retention_slope(
        0.4,
        q,
        2.0,
        1.0,
        correction_cost_curvature=0.6,
    )
    assert slope > 0.0


def test_actionable_phase_retention_slope_matches_finite_difference():
    q = 0.85
    eps = 1e-6
    left = canonical_optimal_correction(
        0.4,
        q - eps,
        2.0,
        1.0,
        correction_cost_curvature=0.6,
    ).phase_retention
    right = canonical_optimal_correction(
        0.4,
        q + eps,
        2.0,
        1.0,
        correction_cost_curvature=0.6,
    ).phase_retention
    finite = (right - left) / (2.0 * eps)
    exact = actionable_phase_retention_slope(
        0.4,
        q,
        2.0,
        1.0,
        correction_cost_curvature=0.6,
    )
    assert finite == pytest.approx(exact, rel=1e-6)


def test_below_actionability_threshold_information_does_not_change_correction():
    a = canonical_optimal_correction(
        0.4,
        0.55,
        2.0,
        1.0,
        correction_cost_curvature=0.5,
    )
    b = canonical_optimal_correction(
        0.4,
        0.70,
        2.0,
        1.0,
        correction_cost_curvature=0.5,
    )
    assert a.pre_correction_risk == pytest.approx(b.pre_correction_risk)
    assert a.correction_gain == pytest.approx(b.correction_gain)

    with pytest.raises(ValueError, match="actionability kink"):
        actionable_phase_retention_slope(
            0.4,
            0.70,
            2.0,
            1.0,
            correction_cost_curvature=0.5,
        )


def test_cheaper_correction_produces_stronger_feedback_at_same_risk():
    cheap = optimal_quadratic_correction(
        0.4,
        correction_cost_curvature=0.2,
    )
    expensive = optimal_quadratic_correction(
        0.4,
        correction_cost_curvature=2.0,
    )
    assert cheap.correction_gain > expensive.correction_gain
    assert cheap.phase_retention < expensive.phase_retention



def test_fixed_correction_cost_gives_prediction_substitution():
    result = prediction_correction_balance(
        pre_correction_risk=0.4,
        risk_derivative=-0.2,
        correction_cost_curvature=0.5,
        correction_cost_derivative=0.0,
    )
    assert result.risk_log_derivative < 0.0
    assert result.correction_cost_log_derivative == pytest.approx(0.0)
    assert result.correction_gain_derivative < 0.0
    assert result.regime == "PREDICTION_SUBSTITUTION_DOMINANT"


def test_fast_cue_informed_cost_reduction_reverses_sign():
    result = prediction_correction_balance(
        pre_correction_risk=0.4,
        risk_derivative=-0.2,  # d log R / dq = -0.5
        correction_cost_curvature=0.5,
        correction_cost_derivative=-0.5,  # d log c / dq = -1.0
    )
    assert result.risk_log_derivative == pytest.approx(-0.5)
    assert result.correction_cost_log_derivative == pytest.approx(-1.0)
    assert result.correction_gain_logit_derivative == pytest.approx(0.5)
    assert result.correction_gain_derivative > 0.0
    assert result.regime == "CUE_INFORMED_CORRECTION_DOMINANT"


def test_equal_proportional_rates_define_exact_balance_boundary():
    result = prediction_correction_balance(
        pre_correction_risk=0.4,
        risk_derivative=-0.2,  # -0.5 proportional rate
        correction_cost_curvature=0.8,
        correction_cost_derivative=-0.4,  # -0.5 proportional rate
    )
    assert result.correction_gain_logit_derivative == pytest.approx(0.0)
    assert result.correction_gain_derivative == pytest.approx(0.0)
    assert result.regime == "LOCAL_BALANCE"


def test_logit_identity_matches_finite_difference():
    # R(q)=0.4*exp(-0.6q), c(q)=0.5*exp(-1.1q).
    import math

    q = 0.7
    eps = 1e-6

    def gain(x):
        R = 0.4 * math.exp(-0.6 * x)
        c = 0.5 * math.exp(-1.1 * x)
        return 2.0 * R / (c + 2.0 * R)

    R = 0.4 * math.exp(-0.6 * q)
    c = 0.5 * math.exp(-1.1 * q)
    result = prediction_correction_balance(
        pre_correction_risk=R,
        risk_derivative=-0.6 * R,
        correction_cost_curvature=c,
        correction_cost_derivative=-1.1 * c,
    )
    finite = (gain(q + eps) - gain(q - eps)) / (2.0 * eps)
    assert finite == pytest.approx(result.correction_gain_derivative, rel=1e-6)
    assert result.correction_gain_logit_derivative == pytest.approx(0.5)
