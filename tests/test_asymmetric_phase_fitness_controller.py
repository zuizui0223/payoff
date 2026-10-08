"""Synthetic tests of a standard asymmetric loss, NOT empirical fitness validation."""

import math
import random
from statistics import NormalDist

import pytest

from src.asymmetric_phase_fitness_controller import (
    expected_asymmetric_loss,
    optimal_asymmetric_timing,
    resource_to_fitness_phase,
)


def calculate(*, phase_mean=0.0, phase_sd=1.0,
              early_cost=0.14, late_cost=0.06,
              effort_penalty=0.0, max_delay=5.0, max_advance=5.0):
    return optimal_asymmetric_timing(
        phase_mean=phase_mean, phase_sd=phase_sd,
        early_cost=early_cost, late_cost=late_cost,
        effort_penalty=effort_penalty,
        max_delay=max_delay, max_advance=max_advance,
    )


def test_unequal_loss_changes_optimal_percentile_not_mean():
    result = calculate()
    assert result.quantile_without_effort == pytest.approx(.3)
    assert result.correction == pytest.approx(NormalDist().inv_cdf(.3), abs=1e-10)
    assert result.correction < 0  # delay, to avoid costly early residual
    assert result.expected_gain > 0


def test_reverse_marginal_costs_reverse_decision():
    left = calculate(early_cost=.14, late_cost=.06)
    right = calculate(early_cost=.06, late_cost=.14)
    assert right.correction == pytest.approx(-left.correction, abs=1e-10)


def test_symmetric_loss_unbiased_phase_gives_zero_adjustment():
    r = calculate(early_cost=.1, late_cost=.1)
    assert r.correction == pytest.approx(0, abs=1e-11)
    assert r.expected_gain == pytest.approx(0, abs=1e-11)


def test_fitness_optimum_offset_is_not_resource_marker():
    # Published winter moth composite fitness peak: about 2 days after
    # budburst, and this is experimental not a universal wild value.
    e = resource_to_fitness_phase(resource_relative_phase=0,
                                  fitness_target_offset=2)
    assert e == -2
    r = calculate(phase_mean=e, phase_sd=0.0,
                  effort_penalty=0.0, max_delay=4.0)
    assert r.correction == pytest.approx(-2)
    assert r.residual_mean_error == pytest.approx(0)
    assert r.expected_gain > 0


def test_zero_recourse_cannot_change_action_even_with_informative_phase():
    r = calculate(max_delay=0.0, max_advance=0.0)
    assert r.correction == 0.0
    assert r.expected_gain == 0.0


def test_finite_recourse_clips_asymmetric_bayes_action():
    r = calculate(max_delay=0.1, max_advance=0.1)
    assert r.correction == pytest.approx(-.1)
    assert 0 < r.expected_gain < calculate().expected_gain


def test_known_phase_with_quadratic_effort_has_asymmetric_capped_adjustment():
    late = calculate(phase_mean=10, phase_sd=0, early_cost=14,
                     late_cost=6, effort_penalty=2,
                     max_delay=10, max_advance=10)
    early = calculate(phase_mean=-10, phase_sd=0, early_cost=14,
                      late_cost=6, effort_penalty=2,
                      max_delay=10, max_advance=10)
    assert late.correction == pytest.approx(3)    # c_late / kappa
    assert early.correction == pytest.approx(-7)  # -c_early / kappa
    assert early.chosen_expected_loss < early.no_correction_expected_loss


def test_nonzero_effort_reduces_absolute_timing_change_in_example():
    r0 = calculate(effort_penalty=0.0)
    r1 = calculate(effort_penalty=0.08)
    r2 = calculate(effort_penalty=1.0)
    assert abs(r0.correction) > abs(r1.correction) > abs(r2.correction)


def test_exact_expected_risk_matches_seeded_monte_carlo():
    rng = random.Random(20261008)
    mu, sd, u = .3, .9, -.2
    ce, cl, k = .14, .06, .1
    exact = expected_asymmetric_loss(
        phase_mean=mu, phase_sd=sd, correction=u,
        early_cost=ce, late_cost=cl, effort_penalty=k)
    empirical = 0.0
    for _ in range(75000):
        e = rng.gauss(mu, sd)
        empirical += ce * max(u-e, 0) + cl * max(e-u, 0) + .5*k*u*u
    assert empirical / 75000 == pytest.approx(exact, abs=.002)


def test_action_is_minimum_on_dense_grid_and_not_worse_than_zero():
    for mu, sd, ce, cl, k in [
        (-1., 1., .14, .06, 0.),
        (0., 1., .14, .06, .2),
        (1., 2., .06, .14, .5),
        (2., 0., .14, .06, .1),
        (-2., 0., .14, .06, .1),
    ]:
        opt = calculate(phase_mean=mu, phase_sd=sd,
                        early_cost=ce, late_cost=cl,
                        effort_penalty=k, max_delay=3, max_advance=3)
        grid = [
            expected_asymmetric_loss(
                phase_mean=mu, phase_sd=sd, correction=-3 + 6*i/600,
                early_cost=ce, late_cost=cl, effort_penalty=k)
            for i in range(601)
        ]
        assert opt.chosen_expected_loss <= min(grid) + 1e-10
        assert opt.chosen_expected_loss <= opt.no_correction_expected_loss + 1e-10


def test_no_phase_cost_leads_to_no_timing_change():
    r = calculate(early_cost=0, late_cost=0, effort_penalty=.5)
    assert r.correction == 0
    assert r.expected_gain == 0


def test_input_validation_fails_closed():
    with pytest.raises(ValueError):
        calculate(phase_mean=float("nan"))
    with pytest.raises(ValueError):
        calculate(phase_sd=-1)
    with pytest.raises(ValueError):
        calculate(early_cost=-.01)
    with pytest.raises(ValueError):
        calculate(late_cost=float("inf"))
    with pytest.raises(ValueError):
        calculate(effort_penalty=-2)
    with pytest.raises(ValueError):
        calculate(max_delay=-1)
    with pytest.raises(ValueError):
        calculate(max_advance=-1)
    with pytest.raises(ValueError):
        resource_to_fitness_phase(0, float("nan"))


def test_posterior_uncertainty_changes_optimal_timing_under_asymmetric_cost():
    # Existing decision-theoretic identity; the general ecological
    # phenomenon was already treated by Lof et al. (2012).
    r1 = calculate(phase_mean=0, phase_sd=1, max_delay=10, max_advance=10)
    r2 = calculate(phase_mean=0, phase_sd=2, max_delay=10, max_advance=10)
    r0 = calculate(phase_mean=0, phase_sd=0, max_delay=10, max_advance=10)
    assert r1.correction == pytest.approx(NormalDist().inv_cdf(.3))
    assert r2.correction == pytest.approx(2 * r1.correction)
    assert r0.correction == pytest.approx(0)
    # Under otherwise identical *symmetric* loss no uncertainty bias remains.
    symmetric = calculate(phase_mean=0, phase_sd=2,
                          early_cost=.1, late_cost=.1)
    assert symmetric.correction == pytest.approx(0)


def test_identical_forecast_mean_different_loss_shapes_can_desynchronize():
    a = calculate(phase_mean=0, phase_sd=1,
                  early_cost=.14, late_cost=.06, max_delay=5, max_advance=5)
    b = calculate(phase_mean=0, phase_sd=1,
                  early_cost=.1, late_cost=.1, max_delay=5, max_advance=5)
    assert a.correction < b.correction
    assert abs(a.correction - b.correction) == pytest.approx(.524400512708, abs=1e-9)
    # This numerical timing difference does not prove a cross-species
    # coordination trap or any demographic fitness consequence.
