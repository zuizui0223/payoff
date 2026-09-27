import pytest

from src.endogenous_information_timing import (
    InformationTimingScenario,
    closed_form_information_threshold,
    closed_form_mismatch_probability_during_asynchrony,
    decision_for_delay_cost,
    desynchronization_window,
    evaluate_information_timing,
    expected_shared_cue_action_mismatch,
    information_acquisition_wedge_interval,
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



def test_improving_information_can_create_intermediate_desynchronization():
    def mismatch(q):
        return expected_shared_cue_action_mismatch(
            InformationTimingScenario(
                prior_early=0.40,
                cue_accuracy_after_wait=q,
                false_early_cost=2.0,
                missed_early_cost=1.0,
            ),
            actor_a_delay_cost=0.30,
            actor_b_delay_cost=0.10,
        )

    assert mismatch(0.81) == pytest.approx(0.0)
    assert mismatch(0.82) == pytest.approx(0.436)
    assert mismatch(0.90) == pytest.approx(0.42)
    assert mismatch(0.93) == pytest.approx(0.414)
    assert mismatch(0.94) == pytest.approx(0.0)


def test_information_desynchronization_requires_unequal_waiting_decisions():
    scenario = InformationTimingScenario(
        prior_early=0.40,
        cue_accuracy_after_wait=0.90,
        false_early_cost=2.0,
        missed_early_cost=1.0,
    )

    assert expected_shared_cue_action_mismatch(
        scenario,
        actor_a_delay_cost=0.10,
        actor_b_delay_cost=0.10,
    ) == pytest.approx(0.0)
    assert expected_shared_cue_action_mismatch(
        scenario,
        actor_a_delay_cost=0.30,
        actor_b_delay_cost=0.30,
    ) == pytest.approx(0.0)
    assert expected_shared_cue_action_mismatch(
        scenario,
        actor_a_delay_cost=0.30,
        actor_b_delay_cost=0.10,
    ) > 0.0



def test_closed_form_canonical_wait_thresholds_match_grid_result():
    low = closed_form_information_threshold(
        0.40,
        2.0,
        1.0,
        delay_cost=0.10,
    )
    high = closed_form_information_threshold(
        0.40,
        2.0,
        1.0,
        delay_cost=0.30,
    )

    assert low.prior_action == 0
    assert low.prior_bayes_risk == pytest.approx(0.40)
    assert low.actionable_cue_accuracy == pytest.approx(0.75)
    assert low.wait_cue_accuracy == pytest.approx(0.8125)
    assert high.wait_cue_accuracy == pytest.approx(0.9375)


def test_exact_desynchronization_window_width_is_delay_gap_over_loss_scale():
    result = desynchronization_window(
        0.40,
        2.0,
        1.0,
        actor_a_delay_cost=0.30,
        actor_b_delay_cost=0.10,
    )

    assert result.regime == "FINITE_DESYNCHRONIZATION_WINDOW"
    assert result.lower_bound_open == pytest.approx(0.8125)
    assert result.upper_bound_closed == pytest.approx(0.9375)
    assert result.finite_window_width == pytest.approx(0.125)
    assert result.finite_window_width == pytest.approx(
        (0.30 - 0.10) / (1.20 + 0.40)
    )


@pytest.mark.parametrize(
    "q",
    [0.76, 0.82, 0.90, 0.93, 0.99],
)
def test_closed_form_mismatch_matches_bruteforce_when_one_actor_waits(q):
    scenario = InformationTimingScenario(
        prior_early=0.40,
        cue_accuracy_after_wait=q,
        false_early_cost=2.0,
        missed_early_cost=1.0,
    )
    brute = expected_shared_cue_action_mismatch(
        scenario,
        actor_a_delay_cost=0.30,
        actor_b_delay_cost=0.10,
    )
    window = desynchronization_window(
        0.40,
        2.0,
        1.0,
        actor_a_delay_cost=0.30,
        actor_b_delay_cost=0.10,
    )
    assert window.lower_bound_open is not None
    assert window.upper_bound_closed is not None

    if window.lower_bound_open < q <= window.upper_bound_closed:
        expected = closed_form_mismatch_probability_during_asynchrony(
            0.40,
            2.0,
            1.0,
            cue_accuracy=q,
        )
    else:
        expected = 0.0

    assert brute == pytest.approx(expected)


def test_prior_early_case_has_symmetric_closed_form_threshold():
    result = closed_form_information_threshold(
        0.80,
        1.0,
        2.0,
        delay_cost=0.10,
    )

    # Prior early loss = 0.20; prior late loss = 1.60.
    assert result.prior_action == 1
    assert result.prior_bayes_risk == pytest.approx(0.20)
    assert result.actionable_cue_accuracy == pytest.approx(1.60 / 1.80)
    assert result.wait_cue_accuracy == pytest.approx(1.70 / 1.80)


def test_high_delay_actor_never_waits_and_asynchrony_persists_to_perfect_cue():
    result = desynchronization_window(
        0.40,
        2.0,
        1.0,
        actor_a_delay_cost=0.50,
        actor_b_delay_cost=0.10,
    )

    assert result.regime == "PERSISTENT_ASYMMETRIC_UPTAKE"
    assert result.lower_bound_open == pytest.approx(0.8125)
    assert result.upper_bound_closed == pytest.approx(1.0)
    assert result.finite_window_width is None

    perfect = expected_shared_cue_action_mismatch(
        InformationTimingScenario(
            prior_early=0.40,
            cue_accuracy_after_wait=1.0,
            false_early_cost=2.0,
            missed_early_cost=1.0,
        ),
        actor_a_delay_cost=0.50,
        actor_b_delay_cost=0.10,
    )
    assert perfect == pytest.approx(0.40)


def test_equal_delays_remove_asynchronous_information_window():
    result = desynchronization_window(
        0.40,
        2.0,
        1.0,
        actor_a_delay_cost=0.20,
        actor_b_delay_cost=0.20,
    )
    assert result.regime == "NO_ASYNCHRONY_EQUAL_DELAY"
    assert result.finite_window_width == pytest.approx(0.0)


def test_information_acquisition_wedge_interval_is_exact():
    scenario = InformationTimingScenario(
        prior_early=0.40,
        cue_accuracy_after_wait=0.90,
        false_early_cost=2.0,
        missed_early_cost=1.0,
        partner_false_early_externality=1.0,
        partner_missed_early_externality=1.0,
    )
    interval = information_acquisition_wedge_interval(scenario)

    assert interval is not None
    assert interval[0] == pytest.approx(0.24)
    assert interval[1] == pytest.approx(0.54)


def test_no_externality_means_no_information_acquisition_wedge():
    scenario = InformationTimingScenario(
        prior_early=0.40,
        cue_accuracy_after_wait=0.90,
        false_early_cost=2.0,
        missed_early_cost=1.0,
    )
    assert information_acquisition_wedge_interval(scenario) is None



@pytest.mark.parametrize("prior", [0.2, 0.4, 0.5, 0.7, 0.8])
@pytest.mark.parametrize("false_cost", [0.5, 1.0, 2.0])
@pytest.mark.parametrize("missed_cost", [0.5, 1.0, 2.0])
def test_closed_form_wait_rule_matches_bruteforce_grid(
    prior,
    false_cost,
    missed_cost,
):
    early_loss = (1.0 - prior) * false_cost
    late_loss = prior * missed_cost
    risk = min(early_loss, late_loss)
    delays = [0.0, 0.25 * risk, 0.75 * risk, risk, 1.25 * risk]

    for delay in delays:
        threshold = closed_form_information_threshold(
            prior,
            false_cost,
            missed_cost,
            delay_cost=delay,
        )
        for step in range(51):
            q = 0.5 + 0.01 * step
            brute = decision_for_delay_cost(
                information_value(
                    prior,
                    q,
                    false_cost,
                    missed_cost,
                ),
                delay,
            )
            if threshold.wait_cue_accuracy is None:
                expected = "commit_now"
            elif q > threshold.wait_cue_accuracy + 1e-12:
                expected = "wait_for_information"
            else:
                expected = "commit_now"
            assert brute == expected


@pytest.mark.parametrize(
    "prior,false_cost,missed_cost,low_delay,high_delay",
    [
        (0.4, 2.0, 1.0, 0.1, 0.3),
        (0.7, 1.0, 2.0, 0.05, 0.15),
        (0.5, 1.0, 1.0, 0.05, 0.20),
    ],
)
def test_window_width_identity_is_exact_across_parameterizations(
    prior,
    false_cost,
    missed_cost,
    low_delay,
    high_delay,
):
    result = desynchronization_window(
        prior,
        false_cost,
        missed_cost,
        actor_a_delay_cost=low_delay,
        actor_b_delay_cost=high_delay,
    )
    assert result.regime == "FINITE_DESYNCHRONIZATION_WINDOW"

    total_loss = (
        (1.0 - prior) * false_cost
        + prior * missed_cost
    )
    assert result.finite_window_width == pytest.approx(
        (high_delay - low_delay) / total_loss
    )
