import pytest

from src.information_rescue_coalition import (
    coalition_adoption,
    complete_graph_minimum_coalition_size,
    complete_graph_pinned_seed_threshold,
    minimum_pinned_rescue_coalitions,
    minimum_self_financing_coalitions,
    pinned_rescue,
)
from src.shared_cue_deadline_network import (
    SharedCueGame,
    SharedCuePlayer,
    canonical_shared_cue_deadline_game,
)


def homogeneous_complete_game(
    *,
    n=5,
    information_cost=0.30,
    interaction_strength=0.50,
):
    return SharedCueGame(
        prior_early=0.40,
        cue_accuracy=1.0,
        players=tuple(
            SharedCuePlayer(
                name=f"p{i}",
                false_early_cost=2.0,
                missed_early_cost=1.0,
                interaction_strength=interaction_strength,
                information_cost=information_cost,
            )
            for i in range(n)
        ),
        interaction_weights=None,
    )


def test_canonical_complete_and_chain_need_full_voluntary_coalition():
    for topology in ("complete", "chain"):
        game = canonical_shared_cue_deadline_game(
            1.0,
            interaction_topology=topology,
        )
        coalitions = minimum_self_financing_coalitions(game)

        assert len(coalitions) == 1
        assert coalitions[0].members == (0, 1, 2)
        assert coalitions[0].weakly_self_financing
        assert not coalitions[0].strictly_self_financing


def test_canonical_migrant_star_has_two_weak_two_species_coalitions():
    game = canonical_shared_cue_deadline_game(
        1.0,
        interaction_topology="migrant_star",
    )
    coalitions = minimum_self_financing_coalitions(game)

    assert {row.members for row in coalitions} == {
        (0, 2),
        (1, 2),
    }
    assert all(row.weakly_self_financing for row in coalitions)


def test_chain_has_one_keystone_single_species_rescue_seed():
    game = canonical_shared_cue_deadline_game(
        1.0,
        interaction_topology="chain",
    )
    rescues = minimum_pinned_rescue_coalitions(game)

    assert len(rescues) == 1
    assert rescues[0].pinned_members == (1,)
    assert rescues[0].pinned_names == ("local_pollinator",)
    assert rescues[0].reaches_fully_informed_while_pinned
    assert rescues[0].persists_after_release

    assert not pinned_rescue(game, (0,)).persists_after_release
    assert not pinned_rescue(game, (2,)).persists_after_release


def test_complete_and_migrant_star_any_singleton_can_nucleate_recovery():
    for topology in ("complete", "migrant_star"):
        game = canonical_shared_cue_deadline_game(
            1.0,
            interaction_topology=topology,
        )
        rescues = minimum_pinned_rescue_coalitions(game)

        assert {row.pinned_members for row in rescues} == {
            (0,),
            (1,),
            (2,),
        }
        assert all(row.persists_after_release for row in rescues)


def test_homogeneous_complete_graph_voluntary_coalition_formula_matches_enumeration():
    # R=.4, D=.3, pI=.2, N=5 gives weak threshold k=3 and
    # strict threshold k=4.
    game = homogeneous_complete_game()
    formula = complete_graph_minimum_coalition_size(
        n=5,
        prior_risk=0.40,
        information_cost=0.30,
        switch_probability=0.40,
        interaction_strength=0.50,
    )
    weak = minimum_self_financing_coalitions(game, strict=False)
    strict = minimum_self_financing_coalitions(game, strict=True)

    assert formula.weak_minimum_size == 3
    assert formula.strict_minimum_size == 4
    assert {len(row.members) for row in weak} == {3}
    assert {len(row.members) for row in strict} == {4}


def test_homogeneous_complete_graph_pinned_seed_formula_matches_cascade():
    # For the same N=5 game, H(k)>0 once k>1, so two temporary
    # informed seeds nucleate full recovery.
    game = homogeneous_complete_game()
    formula = complete_graph_pinned_seed_threshold(
        n=5,
        prior_risk=0.40,
        information_cost=0.30,
        switch_probability=0.40,
        interaction_strength=0.50,
    )

    assert formula.weak_outsider_adoption_seed_size == 1
    assert formula.strict_outsider_adoption_seed_size == 2

    one = pinned_rescue(game, (0,))
    two = pinned_rescue(game, (0, 1))
    assert not one.reaches_fully_informed_while_pinned
    assert two.reaches_fully_informed_while_pinned
    assert two.persists_after_release


def test_full_coalition_can_be_weakly_but_not_strictly_self_financing():
    game = canonical_shared_cue_deadline_game(
        1.0,
        interaction_topology="complete",
    )
    result = coalition_adoption(game, (0, 1, 2))

    assert result.gains_vs_old == pytest.approx((0.05, 0.0, 0.10))
    assert result.weakly_self_financing
    assert not result.strictly_self_financing
    assert result.joint_gain_vs_old == pytest.approx(0.15)


def test_no_voluntary_coalition_exists_if_information_cost_exceeds_prior_risk_for_everyone():
    game = homogeneous_complete_game(
        information_cost=0.50,
        interaction_strength=0.50,
    )
    formula = complete_graph_minimum_coalition_size(
        n=5,
        prior_risk=0.40,
        information_cost=0.50,
        switch_probability=0.40,
        interaction_strength=0.50,
    )

    assert formula.weak_minimum_size is None
    assert formula.strict_minimum_size is None
    assert minimum_self_financing_coalitions(game) == ()
