import pytest

from src.state_dependent_information_deadlines import (
    conditional_threshold_shift,
    expected_delay_cost,
    state_dependent_deadline,
)


def test_expected_delay_cost():
    assert expected_delay_cost([0.75, 0.25], [0.10, 0.50]) == pytest.approx(0.20)


def test_hidden_deadline_uses_expected_cost_not_realised_cost():
    result = state_dependent_deadline(
        0.4,
        0.90,
        2.0,
        1.0,
        deadline_state_probabilities=[0.75, 0.25],
        deadline_state_costs=[0.10, 0.50],
    )

    # E[D] = 0.20, so q_wait=(1.2+0.2)/1.6=0.875.
    assert result.expected_delay_cost == pytest.approx(0.20)
    assert result.wait_threshold == pytest.approx(0.875)
    assert result.ex_ante_decision == "wait_for_information"


def test_ex_ante_optimum_can_be_ex_post_wrong_in_harsh_state():
    result = state_dependent_deadline(
        0.4,
        0.90,
        2.0,
        1.0,
        deadline_state_probabilities=[0.75, 0.25],
        deadline_state_costs=[0.10, 0.50],
    )

    # V(0.9)=0.24. Waiting is optimal ex ante because E[D]=0.20,
    # but in the harsh state D=0.50 and commitment would have been better.
    assert result.information_value == pytest.approx(0.24)
    assert result.probability_ex_post_reversal == pytest.approx(0.25)
    assert result.expected_ex_post_regret == pytest.approx(0.25 * (0.50 - 0.24))


def test_unpredictable_state_dependence_does_not_create_year_specific_threshold():
    a = state_dependent_deadline(
        0.4,
        0.90,
        2.0,
        1.0,
        deadline_state_probabilities=[0.75, 0.25],
        deadline_state_costs=[0.10, 0.50],
    )
    b = state_dependent_deadline(
        0.4,
        0.90,
        2.0,
        1.0,
        deadline_state_probabilities=[0.75, 0.25],
        deadline_state_costs=[0.10, 0.50],
    )
    assert a.wait_threshold == pytest.approx(b.wait_threshold)


def test_precommitment_information_about_deadline_state_moves_threshold_exactly():
    # Same canonical state-loss scale S=1.6.  A pre-commitment signal that
    # raises E[D] from 0.10 to 0.30 shifts q_wait by 0.20/1.60=0.125.
    shift = conditional_threshold_shift(
        0.4,
        2.0,
        1.0,
        expected_delay_cost_before=0.10,
        expected_delay_cost_after=0.30,
    )
    assert shift == pytest.approx(0.125)


def test_state_dependence_can_remove_waiting_altogether():
    result = state_dependent_deadline(
        0.4,
        1.0,
        2.0,
        1.0,
        deadline_state_probabilities=[0.5, 0.5],
        deadline_state_costs=[0.30, 0.70],
    )
    # E[D]=0.50 exceeds R0=0.40.
    assert not result.ever_waits
    assert result.wait_threshold is None
    assert result.ex_ante_decision == "commit_now"
