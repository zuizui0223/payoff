import pytest

from src.bayesian_timing_coordination import (
    ALWAYS_LATE,
    FOLLOW_CUE,
    canonical_three_player_game,
    pure_bayesian_nash_equilibria,
    sequential_best_response,
)


FOLLOW_ALL = (FOLLOW_CUE, FOLLOW_CUE, FOLLOW_CUE)


def trace(local_accuracy: float, interaction_strength: float):
    accuracies = [round(0.50 + 0.01 * i, 2) for i in range(51)]

    profile = FOLLOW_ALL
    baseline = sequential_best_response(
        canonical_three_player_game(
            1.0,
            local_accuracy=local_accuracy,
            interaction_strength=interaction_strength,
        ),
        profile,
    ).final
    profile = baseline.profile

    collapse = None
    for migrant_accuracy in reversed(accuracies):
        result = sequential_best_response(
            canonical_three_player_game(
                migrant_accuracy,
                local_accuracy=local_accuracy,
                interaction_strength=interaction_strength,
            ),
            profile,
        )
        profile = result.final.profile
        if collapse is None and (
            profile[0] != FOLLOW_CUE
            or profile[1] != FOLLOW_CUE
        ):
            collapse = migrant_accuracy

    low_profile = profile

    for migrant_accuracy in accuracies:
        result = sequential_best_response(
            canonical_three_player_game(
                migrant_accuracy,
                local_accuracy=local_accuracy,
                interaction_strength=interaction_strength,
            ),
            profile,
        )
        profile = result.final.profile

    recovered_game = canonical_three_player_game(
        1.0,
        local_accuracy=local_accuracy,
        interaction_strength=interaction_strength,
    )
    recovered = sequential_best_response(
        recovered_game,
        profile,
    ).final
    best = pure_bayesian_nash_equilibria(recovered_game)[0]
    return baseline, collapse, low_profile, recovered, best


def test_canonical_information_loss_has_inefficient_hysteresis():
    baseline, collapse, low_profile, recovered, best = trace(0.90, 0.50)

    assert baseline.profile == FOLLOW_ALL
    assert collapse == pytest.approx(0.71)
    assert low_profile == (
        ALWAYS_LATE,
        ALWAYS_LATE,
        ALWAYS_LATE,
    )
    assert recovered.profile == (
        ALWAYS_LATE,
        ALWAYS_LATE,
        FOLLOW_CUE,
    )
    assert best.profile == FOLLOW_ALL
    assert best.joint_payoff - recovered.joint_payoff == pytest.approx(0.27)


def test_no_interaction_prevents_resident_information_cascade():
    baseline, collapse, low_profile, recovered, best = trace(0.90, 0.0)

    assert baseline.profile == FOLLOW_ALL
    assert collapse is None
    assert low_profile[:2] == (FOLLOW_CUE, FOLLOW_CUE)
    assert recovered.profile == FOLLOW_ALL
    assert best.profile == FOLLOW_ALL


def test_high_local_information_resists_migrant_information_cascade():
    baseline, collapse, low_profile, recovered, best = trace(0.95, 0.50)

    assert baseline.profile == FOLLOW_ALL
    assert collapse is None
    assert low_profile[:2] == (FOLLOW_CUE, FOLLOW_CUE)
    assert recovered.profile == FOLLOW_ALL
    assert best.profile == FOLLOW_ALL


def test_history_dependence_need_not_be_jointly_inefficient():
    baseline, collapse, _, recovered, best = trace(0.80, 0.50)

    assert baseline.profile == FOLLOW_ALL
    assert collapse == pytest.approx(0.72)
    assert recovered.profile != baseline.profile
    assert best.profile == recovered.profile
    assert best.joint_payoff == pytest.approx(recovered.joint_payoff)


def test_local_accuracy_parameter_is_exposed_without_changing_default():
    default = canonical_three_player_game(0.8)
    explicit = canonical_three_player_game(0.8, local_accuracy=0.90)

    assert default == explicit
    assert default.players[0].cue_accuracy == pytest.approx(0.90)
    assert default.players[1].cue_accuracy == pytest.approx(0.90)
