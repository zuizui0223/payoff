"""Synthetic counterexamples for the SCH-BALANCE-SLK/PAYOFF causal handoff.

These are model receipts, not biological observations and not historical proof.
The two tests use different architecture reference states. Never equate the
full release of a pre-existing coupled two-axis architecture with the
shared-one-axis to partially separated-two-axis recovery R=sL.
"""

from math import isclose

from src.modularization_barrier import (
    two_function_release_thresholds,
    two_function_classify_cost,
)


def test_shared_conflict_can_favor_shared_architecture():
    """L>0 need not imply any net value for the new two-axis architecture."""
    a = b = 1.0
    theta_gap = 2.0
    residual_coupling = 1.0
    L = a * b / (a + b) * theta_gap**2
    s = a * b / (a * b + residual_coupling * (a + b))
    R = s * L
    K = 0.8
    phi = R - K
    assert isclose(L, 2.0)
    assert isclose(s, 1.0 / 3.0)
    assert isclose(R, 2.0 / 3.0)
    assert L > 0.0 and phi < 0.0


def test_globally_favored_architecture_can_fail_rare_invasion():
    """Positive intrinsic phi is not equivalent to rare-D invasion."""
    L = 2.0
    s = 1.0 / 3.0
    K = 0.5
    eta = 0.3  # stipulated positive coordination feedback
    phi = s * L - K
    rare_d_invasion = phi - eta
    assert isclose(phi, 1.0 / 6.0)
    assert isclose(rare_d_invasion, -2.0 / 15.0)
    assert 0.0 < phi < eta
    assert rare_d_invasion < 0.0


def test_finite_jump_module_release_is_beneficial_but_not_small_step_accessible():
    """Full release and marginal release use the SAME two-axis reference here."""
    c0 = 1.0
    k = 0.9
    bounds = two_function_release_thresholds(
        a=1.0, b=1.0, theta_gap=2.0, reference_coupling=c0
    )
    local = bounds["local_threshold"]
    global_ = bounds["global_threshold"]
    assert isclose(local, 4.0 / 9.0)
    assert isclose(global_, 4.0 / 3.0)
    assert two_function_classify_cost(1.0, 1.0, 2.0, c0, k) == "finite_jump_barrier"
    assert local - k < 0.0
    assert isclose((global_ - k) * c0, 13.0 / 30.0)
    assert (global_ - k) * c0 > 0.0


def test_historical_origin_is_not_entailed_by_any_of_these_math_receipts():
    """Exact equations omit ancestral states, mutation paths, and observed changes."""
    required_historical_fields = {
        "ancestral_architecture",
        "dated_transition",
        "independent_origin_or_reversal",
        "heritable_architecture_path",
        "alternative_hypothesis_comparison",
    }
    model_only_receipt = {"L": 2.0, "R": 2.0 / 3.0, "K": 0.5, "eta": 0.3}
    assert not required_historical_fields.issubset(model_only_receipt)
