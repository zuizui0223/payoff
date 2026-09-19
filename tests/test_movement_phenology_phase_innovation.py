import math

import pytest

from analysis.movement_phenology.phase_innovation import (
    constant_route_variance_after_steps,
    next_phase_variance,
    propagate_route_variance,
    stationary_phase_sd,
    stationary_phase_variance,
)


def test_one_step_variance_decomposes_feedback_and_innovation():
    assert next_phase_variance(100.0, 0.5, 3.0) == pytest.approx(34.0)


def test_stationary_variance_satisfies_recursion():
    lam = 0.4
    sd = 5.0
    v = stationary_phase_variance(lam, sd)
    assert next_phase_variance(v, lam, sd) == pytest.approx(v)
    assert stationary_phase_sd(lam, sd) == pytest.approx(math.sqrt(v))


def test_more_environmental_innovation_increases_phase_noise_without_gain_change():
    lam = 0.3
    assert stationary_phase_sd(lam, 10.0) > stationary_phase_sd(lam, 3.0)


def test_stronger_correction_reduces_phase_noise_for_same_environment():
    sd = 6.0
    # Smaller |lambda| means less retention of prior phase error.
    assert stationary_phase_sd(0.2, sd) < stationary_phase_sd(0.8, sd)


def test_closed_form_matches_iterated_recursion():
    v = 49.0
    lam = -0.3
    sd = 4.0
    for n in range(8):
        iter_v = v
        for _ in range(n):
            iter_v = next_phase_variance(iter_v, lam, sd)
        closed = constant_route_variance_after_steps(v, lam, sd, n)
        assert closed == pytest.approx(iter_v)


def test_variable_route_propagation():
    values = propagate_route_variance(
        25.0,
        [0.5, 0.0, -0.2],
        [2.0, 3.0, 1.0],
    )
    assert values == pytest.approx(
        [
            25.0,
            0.25 * 25.0 + 4.0,
            9.0,
            0.04 * 9.0 + 1.0,
        ]
    )


def test_unstable_lambda_has_no_stationary_variance():
    with pytest.raises(ValueError):
        stationary_phase_variance(1.0, 2.0)
    with pytest.raises(ValueError):
        stationary_phase_variance(-1.2, 2.0)
