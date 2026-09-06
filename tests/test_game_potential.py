from math import isclose

from src.game_potential import (
    coexistence_frequency,
    coordination_basin_sizes,
    mean_game_payoff,
    potential_rate,
    potential_slope,
    risk_dominant_architecture,
)
from src.payoff_game import payoff_gap, replicator_rhs


def test_potential_slope_is_twice_payoff_gap():
    for p in [0.0, 0.13, 0.5, 0.91, 1.0]:
        assert isclose(
            potential_slope(p, phi=0.4, eta=-0.7),
            2.0 * payoff_gap(p, phi=0.4, eta=-0.7),
            abs_tol=1e-12,
        )


def test_potential_rate_is_nonnegative_and_matches_chain_rule():
    phi, eta = 0.2, -0.8
    for p in [0.1, 0.3, 0.6, 0.9]:
        rate = potential_rate(p, phi, eta)
        chain = potential_slope(p, phi, eta) * replicator_rhs(p, phi, eta)
        assert rate >= 0.0
        assert isclose(rate, chain, abs_tol=1e-12)


def test_pure_state_potential_difference_tracks_static_phi():
    for phi in [-0.4, 0.0, 0.7]:
        v_s = mean_game_payoff(0.0, phi, eta=0.5)
        v_d = mean_game_payoff(1.0, phi, eta=0.5)
        assert isclose(v_s, 0.0, abs_tol=1e-12)
        assert isclose(v_d - v_s, 2.0 * phi, abs_tol=1e-12)


def test_negative_feedback_static_gap_controls_coexistence_majority():
    eta = -1.0
    p_neg = coexistence_frequency(phi=-0.3, eta=eta)
    p_zero = coexistence_frequency(phi=0.0, eta=eta)
    p_pos = coexistence_frequency(phi=0.3, eta=eta)
    assert p_neg is not None and p_neg < 0.5
    assert p_zero is not None and isclose(p_zero, 0.5)
    assert p_pos is not None and p_pos > 0.5


def test_positive_feedback_static_gap_controls_risk_dominance():
    eta = 1.0
    assert risk_dominant_architecture(phi=-0.3, eta=eta) == "S"
    assert risk_dominant_architecture(phi=0.0, eta=eta) == "tie"
    assert risk_dominant_architecture(phi=0.3, eta=eta) == "D"


def test_coordination_basin_sizes_sum_to_one_and_shift_with_phi():
    eta = 1.0
    s1, d1 = coordination_basin_sizes(phi=-0.4, eta=eta)
    s2, d2 = coordination_basin_sizes(phi=0.4, eta=eta)
    assert isclose(s1 + d1, 1.0)
    assert isclose(s2 + d2, 1.0)
    assert s1 > d1
    assert d2 > s2


def test_potential_module_returns_none_outside_relevant_middle_regime():
    assert coexistence_frequency(phi=0.0, eta=0.5) is None
    assert coexistence_frequency(phi=2.0, eta=-0.5) is None
    assert coordination_basin_sizes(phi=0.0, eta=-0.5) is None
    assert coordination_basin_sizes(phi=2.0, eta=0.5) is None
    assert risk_dominant_architecture(phi=2.0, eta=0.5) is None
