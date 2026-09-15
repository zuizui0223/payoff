from math import isclose

import pytest

from src.mesoscopic_architecture import bounded_interaction_payoff


def _assert_tuple_close(left, right):
    assert len(left) == len(right)
    for observed, expected in zip(left, right):
        assert isclose(observed, expected, rel_tol=2e-13, abs_tol=1e-300)


def test_decimal_boundary_membership_is_invariant_to_coordinate_units():
    # In binary float, 0.4 - 0.3 is 0.10000000000000003, while 4 - 3 is 1.
    # Both are the exact hard-kernel boundary in their respective units.
    base = bounded_interaction_payoff(
        (0.0, 0.3, 0.4),
        (0.0, 1.0, 0.0),
        gamma=2.0,
        epsilon=0.1,
    )
    scaled = bounded_interaction_payoff(
        (0.0, 3.0, 4.0),
        (0.0, 1.0, 0.0),
        gamma=2.0 / 100.0,
        epsilon=1.0,
    )
    _assert_tuple_close(base, scaled)
    assert isclose(base[2], -0.02, rel_tol=2e-13, abs_tol=0.0)


def test_bounded_interaction_payoff_is_coordinate_scale_invariant():
    grid = (0.0, 0.2, 0.4, 0.8)
    density = (0.0, 1.0, 0.0, 0.0)
    gamma = -1.5
    epsilon = 0.25
    reference = bounded_interaction_payoff(
        grid, density, gamma=gamma, epsilon=epsilon
    )

    for scale in (1e-16, 1.0, 1e16):
        observed = bounded_interaction_payoff(
            tuple(scale * x for x in grid),
            density,
            gamma=gamma / (scale * scale),
            epsilon=epsilon * scale,
        )
        _assert_tuple_close(observed, reference)


def test_materially_outside_point_stays_outside_at_every_scale():
    for scale in (1e-16, 1.0, 1e16):
        result = bounded_interaction_payoff(
            (0.0, scale, 3.0 * scale),
            (0.0, 1.0, 0.0),
            gamma=1.0 / (scale * scale),
            epsilon=scale,
        )
        assert result[2] == 0.0


def test_nonfinite_gamma_and_epsilon_fail_closed():
    grid = (0.0, 0.5, 1.0)
    density = (1.0, 0.0, 0.0)
    for gamma in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(ValueError, match="gamma must be finite"):
            bounded_interaction_payoff(grid, density, gamma=gamma, epsilon=0.5)
    for epsilon in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(ValueError, match="epsilon must be finite"):
            bounded_interaction_payoff(grid, density, gamma=1.0, epsilon=epsilon)
