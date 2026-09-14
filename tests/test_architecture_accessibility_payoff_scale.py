from src.architecture_phase_atlas import (
    global_payoff_indices,
    minimum_uphill_jump_radius_to_global,
    uphill_reachable_indices,
)


BASE = (0.0, 0.10, 0.09, 0.20)


def _transform(scale: float, baseline: float):
    return tuple(baseline + scale * value for value in BASE)


def test_accessibility_is_invariant_to_payoff_scaling_and_common_baseline():
    expected_reachable = uphill_reachable_indices(BASE, 0, jump_radius_bins=1)
    expected_global = global_payoff_indices(BASE)
    expected_radius = minimum_uphill_jump_radius_to_global(BASE, 0)
    assert expected_radius == 2

    for scale in (1e-16, 1.0, 1e16):
        for baseline in (0.0, 100.0 * scale):
            payoff = _transform(scale, baseline)
            assert uphill_reachable_indices(payoff, 0, jump_radius_bins=1) == expected_reachable
            assert global_payoff_indices(payoff) == expected_global
            assert minimum_uphill_jump_radius_to_global(payoff, 0) == expected_radius


def test_tiny_strict_payoff_advantage_is_not_collapsed_by_absolute_floor():
    payoff = (0.0, 1e-16)
    assert global_payoff_indices(payoff) == (1,)
    assert uphill_reachable_indices(payoff, 0, jump_radius_bins=1) == (0, 1)
    assert minimum_uphill_jump_radius_to_global(payoff, 0) == 1


def test_equal_payoffs_have_all_global_states_and_no_strict_uphill_edges():
    payoff = (3.0, 3.0, 3.0)
    assert global_payoff_indices(payoff) == (0, 1, 2)
    assert uphill_reachable_indices(payoff, 1, jump_radius_bins=2) == (1,)
    assert minimum_uphill_jump_radius_to_global(payoff, 1) == 0
