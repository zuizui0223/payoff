import pytest

from src.bayesian_timing_coordination import ALWAYS_LATE, FOLLOW_CUE
from src.shared_cue_deadline_network import (
    canonical_shared_cue_deadline_game,
    evaluate_shared_cue_profile,
    informed_profile_stability_thresholds,
    is_shared_cue_nash,
    perfect_information_coordination_trap,
    sequential_shared_cue_best_response,
)


def test_perfect_information_trap_has_two_strict_equilibria_and_better_informed_joint_payoff():
    game = canonical_shared_cue_deadline_game(
        1.0,
        interaction_topology="chain",
    )
    diagnostic = perfect_information_coordination_trap(game)

    assert diagnostic.perfect_information_coordination_trap
    assert diagnostic.old_profile_is_nash
    assert diagnostic.old_profile_is_strict_nash
    assert diagnostic.informed_profile_is_nash
    assert diagnostic.informed_profile_is_strict_nash
    assert diagnostic.coordinated_information_is_better
    assert diagnostic.joint_information_gain == pytest.approx(0.15)

    assert diagnostic.prior_risks == pytest.approx((0.10, 0.10, 0.40))
    assert diagnostic.information_costs == pytest.approx((0.05, 0.10, 0.30))
    assert diagnostic.interaction_penalties_for_first_mover == pytest.approx(
        (0.20, 0.20, 0.20)
    )
    assert diagnostic.unilateral_information_gains == pytest.approx(
        (-0.15, -0.20, -0.10)
    )


def test_exact_interaction_thresholds_for_perfect_information_bistability():
    diagnostic = perfect_information_coordination_trap(
        canonical_shared_cue_deadline_game(
            1.0,
            interaction_topology="complete",
        )
    )

    assert diagnostic.minimum_interaction_for_old_profile == pytest.approx(
        (0.125, 0.0, 0.25)
    )
    assert diagnostic.minimum_interaction_for_informed_profile == pytest.approx(
        (0.0, 0.0, 0.0)
    )
    assert diagnostic.minimum_interaction_for_bistability == pytest.approx(
        (0.125, 0.0, 0.25)
    )


@pytest.mark.parametrize("topology", ["complete", "chain", "migrant_star"])
def test_information_degradation_then_full_recovery_is_history_dependent(topology):
    informed = (FOLLOW_CUE, FOLLOW_CUE, FOLLOW_CUE)
    old = (ALWAYS_LATE, ALWAYS_LATE, ALWAYS_LATE)

    profile = informed
    collapse_q = None
    for step in range(50, -1, -1):
        q = round(0.50 + 0.01 * step, 2)
        game = canonical_shared_cue_deadline_game(
            q,
            interaction_topology=topology,
        )
        path = sequential_shared_cue_best_response(game, profile)
        profile = path[-1].profile
        if collapse_q is None and profile == old:
            collapse_q = q

    assert collapse_q == pytest.approx(0.79)
    assert profile == old

    for step in range(51):
        q = round(0.50 + 0.01 * step, 2)
        game = canonical_shared_cue_deadline_game(
            q,
            interaction_topology=topology,
        )
        path = sequential_shared_cue_best_response(game, profile)
        profile = path[-1].profile

    assert profile == old

    recovered_game = canonical_shared_cue_deadline_game(
        1.0,
        interaction_topology=topology,
    )
    old_eval = evaluate_shared_cue_profile(
        recovered_game,
        old,
    )
    informed_eval = evaluate_shared_cue_profile(
        recovered_game,
        informed,
    )
    assert old_eval.joint_payoff == pytest.approx(-0.60)
    assert informed_eval.joint_payoff == pytest.approx(-0.45)
    assert informed_eval.joint_payoff > old_eval.joint_payoff


def test_old_profile_is_not_a_perfect_information_equilibrium_without_interaction_for_key_players():
    game = canonical_shared_cue_deadline_game(
        1.0,
        interaction_topology="complete",
    )
    zero_players = tuple(
        type(player)(
            name=player.name,
            false_early_cost=player.false_early_cost,
            missed_early_cost=player.missed_early_cost,
            interaction_strength=0.0,
            information_cost=player.information_cost,
        )
        for player in game.players
    )
    zero_game = type(game)(
        prior_early=game.prior_early,
        cue_accuracy=game.cue_accuracy,
        players=zero_players,
        interaction_weights=game.interaction_weights,
    )
    old = (ALWAYS_LATE, ALWAYS_LATE, ALWAYS_LATE)

    assert not is_shared_cue_nash(zero_game, old)


def test_perfect_information_trap_is_not_specific_to_edge_placement_when_all_nodes_are_connected():
    for topology in ("complete", "chain", "migrant_star"):
        diagnostic = perfect_information_coordination_trap(
            canonical_shared_cue_deadline_game(
                1.0,
                interaction_topology=topology,
            )
        )
        assert diagnostic.perfect_information_coordination_trap
        assert diagnostic.old_profile_is_strict_nash
        assert diagnostic.informed_profile_is_strict_nash
        assert diagnostic.joint_information_gain == pytest.approx(0.15)



def test_exact_all_informed_stability_boundary_is_driven_by_migrant():
    game = canonical_shared_cue_deadline_game(
        1.0,
        interaction_topology="chain",
    )
    thresholds = informed_profile_stability_thresholds(game)

    assert thresholds[0] == pytest.approx(7.0 / 12.0)
    assert thresholds[1] == pytest.approx(2.0 / 3.0)
    assert thresholds[2] == pytest.approx(0.80)
    assert max(thresholds) == pytest.approx(0.80)


def test_grid_collapse_occurs_immediately_below_exact_boundary():
    topology = "chain"
    informed = (FOLLOW_CUE, FOLLOW_CUE, FOLLOW_CUE)

    at_boundary = sequential_shared_cue_best_response(
        canonical_shared_cue_deadline_game(
            0.80,
            interaction_topology=topology,
        ),
        informed,
    )[-1].profile
    below_boundary = sequential_shared_cue_best_response(
        canonical_shared_cue_deadline_game(
            0.79,
            interaction_topology=topology,
        ),
        informed,
    )[-1].profile

    assert at_boundary == informed
    assert below_boundary == (
        ALWAYS_LATE,
        ALWAYS_LATE,
        ALWAYS_LATE,
    )
