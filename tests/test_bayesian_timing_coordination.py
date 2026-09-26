import pytest

from src.bayesian_timing_coordination import (
    ALWAYS_LATE,
    FOLLOW_CUE,
    canonical_three_player_game,
    evaluate_profile,
    policy_label,
    pure_bayesian_nash_equilibria,
    sequential_best_response,
)


FOLLOW_ALL = (FOLLOW_CUE, FOLLOW_CUE, FOLLOW_CUE)
LATE_ALL = (ALWAYS_LATE, ALWAYS_LATE, ALWAYS_LATE)


def labels(profile):
    return tuple(policy_label(policy) for policy in profile)


def test_following_cues_is_stable_before_information_collapse():
    result = sequential_best_response(
        canonical_three_player_game(0.72),
        FOLLOW_ALL,
    )
    assert result.converged
    assert result.final.profile == FOLLOW_ALL


def test_small_further_information_loss_triggers_collective_late_cascade():
    result = sequential_best_response(
        canonical_three_player_game(0.71),
        FOLLOW_ALL,
    )
    assert result.converged
    assert result.final.profile == LATE_ALL


def test_information_recovery_does_not_restore_original_coordination():
    recovered = sequential_best_response(
        canonical_three_player_game(1.0),
        LATE_ALL,
    )
    assert recovered.converged
    assert labels(recovered.final.profile) == (
        "always_late",
        "always_late",
        "follow_cue",
    )
    assert recovered.final.profile != FOLLOW_ALL


def test_recovered_game_contains_better_equilibrium_than_historical_endpoint():
    game = canonical_three_player_game(1.0)
    recovered = sequential_best_response(game, LATE_ALL)
    equilibria = pure_bayesian_nash_equilibria(game)

    assert len(equilibria) >= 2
    assert equilibria[0].profile == FOLLOW_ALL
    assert (
        equilibria[0].joint_payoff
        > recovered.final.joint_payoff
    )


def test_historical_endpoint_is_itself_a_bayesian_nash_equilibrium():
    game = canonical_three_player_game(1.0)
    recovered = sequential_best_response(game, LATE_ALL)
    equilibria = pure_bayesian_nash_equilibria(game)
    profiles = {row.profile for row in equilibria}
    assert recovered.final.profile in profiles


def test_canonical_joint_payoff_order_at_full_migrant_information():
    game = canonical_three_player_game(1.0)
    efficient = evaluate_profile(game, FOLLOW_ALL)
    history_locked = evaluate_profile(
        game,
        (ALWAYS_LATE, ALWAYS_LATE, FOLLOW_CUE),
    )
    assert efficient.joint_payoff == pytest.approx(-0.33)
    assert history_locked.joint_payoff == pytest.approx(-0.60)
    assert efficient.joint_payoff > history_locked.joint_payoff
