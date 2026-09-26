import pytest

from src.endogenous_information_timing import (
    InformationTimingScenario,
    decision_for_delay_cost,
    evaluate_information_timing,
    information_value,
    maximum_affordable_wait_days,
    posterior_cue_bayes_risk,
    prior_bayes_risk,
    sex_specific_information_access,
)


def test_uninformative_cue_has_zero_value():
    before = prior_bayes_risk(0.4, 2.0, 1.0)
    after = posterior_cue_bayes_risk(0.4, 0.5, 2.0, 1.0)

    assert before == pytest.approx(0.4)
    assert after == pytest.approx(before)
    assert information_value(0.4, 0.5, 2.0, 1.0) == pytest.approx(0.0)


def test_perfect_information_value_equals_prior_bayes_risk():
    value = information_value(0.4, 1.0, 2.0, 1.0)

    assert value == pytest.approx(0.4)


def test_information_can_be_non_actionable_until_accuracy_is_high_enough():
    assert information_value(0.4, 0.70, 2.0, 1.0) == pytest.approx(0.0)
    assert information_value(0.4, 0.80, 2.0, 1.0) == pytest.approx(0.08)
    assert information_value(0.4, 0.90, 2.0, 1.0) == pytest.approx(0.24)


def test_partner_externality_creates_information_timing_wedge():
    scenario = InformationTimingScenario(
        prior_early=0.40,
        cue_accuracy_after_wait=0.90,
        false_early_cost=2.0,
        missed_early_cost=1.0,
        partner_false_early_externality=1.0,
        partner_missed_early_externality=1.0,
    )
    diagnostic = evaluate_information_timing(
        scenario,
        delay_cost=0.40,
    )

    assert diagnostic.private_information_value == pytest.approx(0.24)
    assert diagnostic.joint_information_value == pytest.approx(0.54)
    assert diagnostic.private_decision == "commit_now"
    assert diagnostic.joint_decision == "wait_for_information"
    assert diagnostic.information_timing_wedge


def test_sex_specific_delay_costs_generate_endogenous_information_asymmetry():
    scenario = InformationTimingScenario(
        prior_early=0.40,
        cue_accuracy_after_wait=0.90,
        false_early_cost=2.0,
        missed_early_cost=1.0,
    )
    early_sex, late_sex = sex_specific_information_access(
        scenario,
        early_sex_delay_cost=0.30,
        late_sex_delay_cost=0.10,
    )

    assert early_sex == "commit_now"
    assert late_sex == "wait_for_information"


def test_tie_preserves_early_commitment():
    assert decision_for_delay_cost(0.2, 0.2) == "commit_now"


def test_maximum_wait_days_is_information_value_over_daily_cost():
    assert maximum_affordable_wait_days(
        0.24,
        delay_cost_per_day=0.04,
    ) == pytest.approx(6.0)


@pytest.mark.parametrize(
    "accuracy, expected_value",
    [
        (0.5, 0.0),
        (0.6, 0.0),
        (0.7, 0.0),
        (0.8, 0.08),
        (0.9, 0.24),
        (1.0, 0.40),
    ],
)
def test_canonical_information_value_curve(accuracy, expected_value):
    assert information_value(
        0.4,
        accuracy,
        2.0,
        1.0,
    ) == pytest.approx(expected_value)
