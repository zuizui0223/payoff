import pytest

from src.distributed_information_deadlines import (
    delay_cost_from_finite_wait_threshold,
    independent_pair_asynchrony,
    pair_asynchrony_from_joint_uptake,
    population_information_uptake,
    wait_threshold_from_delay_cost,
)


def test_canonical_thresholds_invert_exactly():
    q1 = wait_threshold_from_delay_cost(
        0.4, 2.0, 1.0, delay_cost=0.10
    )
    q2 = wait_threshold_from_delay_cost(
        0.4, 2.0, 1.0, delay_cost=0.30
    )
    assert q1 == pytest.approx(0.8125)
    assert q2 == pytest.approx(0.9375)
    assert delay_cost_from_finite_wait_threshold(
        0.4, 2.0, 1.0, wait_threshold=q1
    ) == pytest.approx(0.10)
    assert delay_cost_from_finite_wait_threshold(
        0.4, 2.0, 1.0, wait_threshold=q2
    ) == pytest.approx(0.30)


def test_population_uptake_is_empirical_delay_cdf_at_information_value():
    delays = [0.10, 0.30]

    below = population_information_uptake(
        0.4, 0.81, 2.0, 1.0, delay_costs=delays
    )
    middle = population_information_uptake(
        0.4, 0.82, 2.0, 1.0, delay_costs=delays
    )
    above = population_information_uptake(
        0.4, 0.94, 2.0, 1.0, delay_costs=delays
    )

    assert below.uptake_probability == pytest.approx(0.0)
    assert middle.uptake_probability == pytest.approx(0.5)
    assert above.uptake_probability == pytest.approx(1.0)


def test_hard_deadline_mass_causes_incomplete_uptake_at_perfect_information():
    result = population_information_uptake(
        0.4,
        1.0,
        2.0,
        1.0,
        delay_costs=[0.10, 0.30, 0.40, 0.50],
    )

    # R0=0.40 and ties commit, so D=0.40 and 0.50 never wait.
    assert result.information_value == pytest.approx(0.40)
    assert result.uptake_probability == pytest.approx(0.50)
    assert result.never_wait_fraction == pytest.approx(0.50)


def test_identical_half_uptake_maximizes_independent_pair_asynchrony():
    assert independent_pair_asynchrony(0.5, 0.5) == pytest.approx(0.5)
    assert independent_pair_asynchrony(0.1, 0.1) == pytest.approx(0.18)
    assert independent_pair_asynchrony(0.9, 0.9) == pytest.approx(0.18)


def test_general_pair_formula_allows_correlated_deadlines():
    # Positive dependence: both often wait together, so less asynchrony than
    # the independent p1*p2 case.
    assert pair_asynchrony_from_joint_uptake(
        0.5, 0.5, 0.4
    ) == pytest.approx(0.2)
    assert independent_pair_asynchrony(0.5, 0.5) == pytest.approx(0.5)


def test_invalid_joint_probability_fails_closed():
    with pytest.raises(ValueError):
        pair_asynchrony_from_joint_uptake(0.2, 0.2, 0.3)
