"""Tests use only toy Gaussian Markov chains; no V7/V7R goose outcomes."""

import math
import random

import pytest

from src.conditional_checkpoint_value import (
    additional_cue_action_value,
    compare_commitment_times,
    conditional_cue_information,
    optimal_control_gain,
)


def test_perfect_duplicate_checkpoint_is_not_new_information():
    info = conditional_cue_information([1.0, 0.9], 1)
    assert info.origin_r2 == pytest.approx(0.81)
    assert info.standalone_checkpoint_r2 == pytest.approx(0.81)
    assert info.incremental_r2 == pytest.approx(0.0)
    assert additional_cue_action_value(info, timing_adjustment_limit=1.0) == pytest.approx(0.0)


def test_weak_first_link_and_perfect_checkpoint_create_true_new_information():
    info = conditional_cue_information([0.0, 0.9], 1)
    assert info.origin_r2 == 0
    assert info.refreshed_r2 == pytest.approx(0.81)
    assert info.incremental_r2 == pytest.approx(0.81)
    assert info.standalone_checkpoint_r2 == pytest.approx(0.81)


def test_added_cue_reliability_reduces_incremental_r2():
    exact = conditional_cue_information([0.2, 0.8], 1, checkpoint_noise_variance=0)
    noisy = conditional_cue_information([0.2, 0.8], 1, checkpoint_noise_variance=4)
    assert 0 < noisy.incremental_r2 < exact.incremental_r2


def test_independent_noisy_repeated_measurement_can_add_information():
    redundant = conditional_cue_information([0.9], 0, origin_noise_variance=0)
    informative = conditional_cue_information([0.9], 0, origin_noise_variance=2)
    assert redundant.incremental_r2 == 0
    assert informative.incremental_r2 > 0
    assert informative.refreshed_r2 <= 1


def test_full_recourse_recovers_exact_gaussian_r2_difference():
    info = conditional_cue_information([0.1, 0.8], 1)
    gain = additional_cue_action_value(info, timing_adjustment_limit=100, effort_penalty=2)
    assert gain == pytest.approx(info.incremental_r2 / 3)


def test_zero_recourse_makes_high_quality_late_cue_unusable():
    info = conditional_cue_information([0.0, 1.0], 1)
    assert info.incremental_r2 == pytest.approx(1.0)
    assert additional_cue_action_value(info, timing_adjustment_limit=0) == 0
    compared = compare_commitment_times(info, initial_timing_adjustment_limit=0,
                                        later_timing_adjustment_limit=0, direct_delay_cost=0)
    assert not compared.defer_commitment
    assert compared.net_waiting_gain == 0


def test_positive_new_information_cannot_make_high_cost_wait_profitable():
    info = conditional_cue_information([0.1, 0.8], 1)
    good = compare_commitment_times(info, initial_timing_adjustment_limit=1,
                                   later_timing_adjustment_limit=1, direct_delay_cost=0)
    expensive = compare_commitment_times(info, initial_timing_adjustment_limit=1,
                                        later_timing_adjustment_limit=1, direct_delay_cost=2)
    assert good.defer_commitment
    assert not expensive.defer_commitment


def test_better_late_prediction_cannot_compensate_loss_of_early_action_options():
    info = conditional_cue_information([0.8, 0.9], 1)
    assert info.incremental_r2 > 0
    early = compare_commitment_times(info, initial_timing_adjustment_limit=1,
                                    later_timing_adjustment_limit=0)
    assert early.initial_optimal_gain > 0
    assert not early.defer_commitment


def test_signal_value_capped_by_information_and_control_penalty():
    for v in (0, 0.1, 0.8, 1):
        for limit in (0, 0.01, 0.1, 0.8, 3.0, 100.0):
            gain = optimal_control_gain(v, timing_adjustment_limit=limit, effort_penalty=0.5)
            assert 0 <= gain <= v / 1.5 + 1e-12
    assert optimal_control_gain(1, timing_adjustment_limit=100, effort_penalty=0.5) == pytest.approx(2/3)


def test_signal_bayes_gain_matches_simulated_optimal_actions():
    rng = random.Random(1035)
    v, limit, penalty = .65, .4, .3
    predicted = optimal_control_gain(v, timing_adjustment_limit=limit, effort_penalty=penalty)
    observed = 0.0
    for _ in range(50000):
        mu = math.sqrt(v) * rng.gauss(0, 1)
        act = min(limit, max(-limit, mu / (1 + penalty)))
        observed += 2 * act * mu - (1 + penalty) * act * act
    observed /= 50000
    assert observed == pytest.approx(predicted, abs=0.015)


def test_fail_closed_bad_noise_link_and_recourse():
    with pytest.raises(ValueError):
        conditional_cue_information([2.0], 1)
    with pytest.raises(ValueError):
        conditional_cue_information([0.9], 1, checkpoint_noise_variance=-1)
    with pytest.raises(ValueError):
        conditional_cue_information([0.9], 1.2)
    with pytest.raises(ValueError):
        optimal_control_gain(0.8, timing_adjustment_limit=-1)
    with pytest.raises(ValueError):
        optimal_control_gain(0.8, timing_adjustment_limit=1, effort_penalty=-0.5)
    with pytest.raises(ValueError):
        compare_commitment_times(conditional_cue_information([0.9], 1),
                                 initial_timing_adjustment_limit=1,
                                 later_timing_adjustment_limit=1, direct_delay_cost=-0.1)
