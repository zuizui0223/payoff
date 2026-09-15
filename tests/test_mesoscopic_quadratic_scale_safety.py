from math import isclose, isfinite

from src.mesoscopic_architecture import (
    architecture_payoff,
    bounded_interaction_payoff,
    intrinsic_payoff,
)


def _scaled_parameters(q: float):
    return {
        "grid": (0.0, q),
        "alpha": 1.0 / q,
        "kappa": 1.0 / (q * q) if isfinite(q * q) else 1.0 / q / q,
        "gamma": 2.0 / q / q,
        "epsilon": 2.0 * q,
    }


def test_intrinsic_quadratic_remains_finite_when_coordinate_square_overflows():
    expected = intrinsic_payoff(1.0, alpha=1.0, kappa=1.0)
    assert expected == 0.5

    for q, rel_tol in ((1e155, 1e-11), (1e160, 2e-3)):
        p = _scaled_parameters(q)
        observed = intrinsic_payoff(q, alpha=p["alpha"], kappa=p["kappa"])
        assert isfinite(observed)
        assert isclose(observed, expected, rel_tol=rel_tol, abs_tol=0.0)


def test_bounded_interaction_quadratic_remains_finite_when_distance_square_overflows():
    expected = bounded_interaction_payoff(
        (0.0, 1.0), (1.0, 0.0), gamma=2.0, epsilon=2.0
    )
    assert expected == (0.0, -2.0)

    for q, rel_tol in ((1e155, 1e-11), (1e160, 2e-3)):
        p = _scaled_parameters(q)
        observed = bounded_interaction_payoff(
            p["grid"],
            (1.0, 0.0),
            gamma=p["gamma"],
            epsilon=p["epsilon"],
        )
        assert all(isfinite(value) for value in observed)
        assert isclose(observed[0], expected[0], abs_tol=0.0)
        assert isclose(observed[1], expected[1], rel_tol=rel_tol, abs_tol=0.0)


def test_full_architecture_payoff_is_coordinate_unit_invariant_at_extreme_scale():
    expected = architecture_payoff(
        (0.0, 1.0),
        (1.0, 0.0),
        alpha=1.0,
        kappa=1.0,
        gamma=2.0,
        epsilon=2.0,
    )
    assert expected == (0.0, -1.5)

    for q, rel_tol in ((1e155, 1e-11), (1e160, 2e-3)):
        p = _scaled_parameters(q)
        observed = architecture_payoff(
            p["grid"],
            (1.0, 0.0),
            alpha=p["alpha"],
            kappa=p["kappa"],
            gamma=p["gamma"],
            epsilon=p["epsilon"],
        )
        assert all(isfinite(value) for value in observed)
        assert isclose(observed[0], expected[0], abs_tol=0.0)
        assert isclose(observed[1], expected[1], rel_tol=rel_tol, abs_tol=0.0)
