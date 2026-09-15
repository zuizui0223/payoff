from math import isclose, isfinite

import pytest

from src.interaction_kernel_robustness import (
    kernel_architecture_payoff,
    kernel_interaction_payoff,
)


def _scaled(q: float):
    return {
        "grid": (0.0, q),
        "alpha": 1.0 / q,
        "kappa": 1.0 / q / q,
        "gamma": 2.0 / q / q,
        "epsilon": 2.0 * q,
    }


@pytest.mark.parametrize("kernel", ["hard", "triangular", "cosine", "gaussian", "global"])
def test_kernel_payoffs_remain_finite_when_coordinate_square_overflows(kernel):
    base_epsilon = None if kernel == "global" else 2.0
    expected_interaction = kernel_interaction_payoff(
        (0.0, 1.0),
        (1.0, 0.0),
        gamma=2.0,
        epsilon=base_epsilon,
        kernel=kernel,
    )
    expected_total = kernel_architecture_payoff(
        (0.0, 1.0),
        (1.0, 0.0),
        alpha=1.0,
        kappa=1.0,
        gamma=2.0,
        epsilon=base_epsilon,
        kernel=kernel,
    )

    for q, rel_tol in ((1e155, 1e-11), (1e160, 2e-3)):
        p = _scaled(q)
        epsilon = None if kernel == "global" else p["epsilon"]
        interaction = kernel_interaction_payoff(
            p["grid"],
            (1.0, 0.0),
            gamma=p["gamma"],
            epsilon=epsilon,
            kernel=kernel,
        )
        total = kernel_architecture_payoff(
            p["grid"],
            (1.0, 0.0),
            alpha=p["alpha"],
            kappa=p["kappa"],
            gamma=p["gamma"],
            epsilon=epsilon,
            kernel=kernel,
        )
        assert all(isfinite(value) for value in interaction + total)
        for observed, expected in zip(interaction, expected_interaction):
            assert isclose(observed, expected, rel_tol=rel_tol, abs_tol=0.0)
        for observed, expected in zip(total, expected_total):
            assert isclose(observed, expected, rel_tol=rel_tol, abs_tol=0.0)


def test_kernel_payoff_parameters_fail_closed_when_nonfinite():
    with pytest.raises(ValueError):
        kernel_interaction_payoff(
            (0.0, 1.0), (1.0, 0.0), gamma=float("inf"), epsilon=None, kernel="global"
        )
    with pytest.raises(ValueError):
        kernel_architecture_payoff(
            (0.0, 1.0),
            (1.0, 0.0),
            alpha=float("nan"),
            kappa=1.0,
            gamma=0.0,
            epsilon=None,
            kernel="global",
        )
    with pytest.raises(ValueError):
        kernel_architecture_payoff(
            (0.0, 1.0),
            (1.0, 0.0),
            alpha=1.0,
            kappa=float("inf"),
            gamma=0.0,
            epsilon=None,
            kernel="global",
        )
