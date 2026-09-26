import pytest

from itertools import permutations

from src.bayesian_timing_coordination import (
    ALWAYS_LATE,
    FOLLOW_CUE,
    BayesianTimingGame,
    TimingPlayer,
    canonical_three_player_game,
    pure_bayesian_nash_equilibria,
    sequential_best_response,
)


FOLLOW_ALL = (FOLLOW_CUE, FOLLOW_CUE, FOLLOW_CUE)


def trace(
    local_accuracy: float,
    interaction_strength: float,
    *,
    interaction_topology: str = "complete",
    prior_early: float = 0.40,
):
    accuracies = [round(0.50 + 0.01 * i, 2) for i in range(51)]

    profile = FOLLOW_ALL
    baseline = sequential_best_response(
        canonical_three_player_game(
            1.0,
            local_accuracy=local_accuracy,
            interaction_strength=interaction_strength,
            interaction_topology=interaction_topology,
            prior_early=prior_early,
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
                interaction_topology=interaction_topology,
                prior_early=prior_early,
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
                interaction_topology=interaction_topology,
                prior_early=prior_early,
            ),
            profile,
        )
        profile = result.final.profile

    recovered_game = canonical_three_player_game(
        1.0,
        local_accuracy=local_accuracy,
        interaction_strength=interaction_strength,
        interaction_topology=interaction_topology,
        prior_early=prior_early,
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



def ordered_game(order, migrant_accuracy):
    players = {
        "flower": TimingPlayer(
            name="flower",
            cue_accuracy=0.90,
            false_early_cost=1.0,
            missed_early_cost=0.25,
            interaction_strength=0.50,
        ),
        "local_pollinator": TimingPlayer(
            name="local_pollinator",
            cue_accuracy=0.90,
            false_early_cost=1.0,
            missed_early_cost=0.25,
            interaction_strength=0.50,
        ),
        "migrant": TimingPlayer(
            name="migrant",
            cue_accuracy=migrant_accuracy,
            false_early_cost=2.0,
            missed_early_cost=1.0,
            interaction_strength=0.50,
        ),
    }
    return BayesianTimingGame(
        prior_early=0.40,
        players=tuple(players[name] for name in order),
    )


def test_canonical_cascade_and_recovery_are_qualitatively_update_order_robust():
    names = ("flower", "local_pollinator", "migrant")

    for order in permutations(names):
        degraded = sequential_best_response(
            ordered_game(order, 0.71),
            (FOLLOW_CUE, FOLLOW_CUE, FOLLOW_CUE),
        )
        assert degraded.final.profile == (
            ALWAYS_LATE,
            ALWAYS_LATE,
            ALWAYS_LATE,
        )

        recovered = sequential_best_response(
            ordered_game(order, 1.0),
            degraded.final.profile,
        )
        following_names = {
            player.name
            for player, policy in zip(
                ordered_game(order, 1.0).players,
                recovered.final.profile,
            )
            if policy == FOLLOW_CUE
        }
        assert following_names == {"migrant"}



def test_early_spring_prior_changes_cascade_regime_nonmonotonically():
    low_prior = canonical_three_player_game(
        0.50,
        local_accuracy=0.90,
        interaction_strength=0.50,
        prior_early=0.40,
    )
    higher_prior = canonical_three_player_game(
        0.50,
        local_accuracy=0.90,
        interaction_strength=0.50,
        prior_early=0.50,
    )

    low_result = sequential_best_response(low_prior, FOLLOW_ALL)
    high_result = sequential_best_response(higher_prior, FOLLOW_ALL)

    assert low_result.final.profile == (
        ALWAYS_LATE,
        ALWAYS_LATE,
        ALWAYS_LATE,
    )
    assert high_result.final.profile[:2] == (
        FOLLOW_CUE,
        FOLLOW_CUE,
    )


def test_canonical_game_exposes_prior_without_changing_default():
    default = canonical_three_player_game(0.8)
    explicit = canonical_three_player_game(0.8, prior_early=0.40)

    assert default == explicit
    assert default.prior_early == pytest.approx(0.40)



def test_chain_topology_retains_information_hysteresis():
    baseline, collapse, low_profile, recovered, best = trace(
        0.90,
        0.50,
        interaction_topology="chain",
    )

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
    assert best.joint_payoff - recovered.joint_payoff == pytest.approx(0.15)


def test_removing_resident_resident_edge_makes_canonical_recovery_reversible():
    baseline, collapse, _, recovered, best = trace(
        0.90,
        0.50,
        interaction_topology="migrant_star",
    )

    assert baseline.profile == FOLLOW_ALL
    assert collapse == pytest.approx(0.71)
    assert recovered.profile == FOLLOW_ALL
    assert best.profile == FOLLOW_ALL


def test_interaction_weight_matrix_validation():
    with pytest.raises(ValueError):
        BayesianTimingGame(
            prior_early=0.40,
            players=canonical_three_player_game(1.0).players,
            interaction_weights=((0.0, 1.0), (1.0, 0.0)),
        )
