import pytest

from src.partial_information_coordination import (
    ALWAYS_BASELINE,
    FOLLOW_CUE,
    HiddenStateGame,
    SpeciesCueParameters,
    focal_threshold_diagnostic,
    full_information_nash_equilibria,
    information_deficit_diagnostic,
    oracle_action_profile,
    posterior_advanced,
    pure_bayesian_nash_equilibria,
    realized_growths,
)


def canonical_game(migrant_accuracy: float = 0.60) -> HiddenStateGame:
    local = SpeciesCueParameters(
        name="local_responder",
        cue_accuracy=1.0,
        baseline_growth=0.30,
        abiotic_mismatch_cost=0.60,
        interaction_mismatch_cost=0.20,
        advance_cost=0.05,
    )
    migrant = SpeciesCueParameters(
        name="migrant",
        cue_accuracy=migrant_accuracy,
        baseline_growth=0.40,
        abiotic_mismatch_cost=0.50,
        interaction_mismatch_cost=0.40,
        advance_cost=0.30,
    )
    return HiddenStateGame(
        species=(local, local, migrant),
        prior_advanced=0.5,
    )


def test_symmetric_binary_cue_has_expected_posterior():
    assert posterior_advanced(0.5, 0.60, 1) == pytest.approx(0.60)
    assert posterior_advanced(0.5, 0.60, 0) == pytest.approx(0.40)


def test_exact_information_threshold_is_two_thirds_in_canonical_game():
    diagnostic = focal_threshold_diagnostic(canonical_game(), 2)

    assert diagnostic.critical_posterior_advanced == pytest.approx(2 / 3)
    assert diagnostic.critical_positive_cue_accuracy == pytest.approx(2 / 3)
    assert diagnostic.posterior_after_advanced_cue == pytest.approx(0.60)
    assert diagnostic.best_response_policy == ALWAYS_BASELINE
    assert not diagnostic.advances_after_positive_cue


def test_canonical_partial_information_game_has_unique_information_trap():
    equilibria = pure_bayesian_nash_equilibria(canonical_game())

    assert len(equilibria) == 1
    equilibrium = equilibria[0]
    assert equilibrium.policies == (
        FOLLOW_CUE,
        FOLLOW_CUE,
        ALWAYS_BASELINE,
    )
    assert equilibrium.expected_growths[0] == pytest.approx(0.225)
    assert equilibrium.expected_growths[1] == pytest.approx(0.225)
    assert equilibrium.expected_growths[2] == pytest.approx(-0.05)


def test_perfect_information_solution_is_viable_and_a_nash_equilibrium():
    game = canonical_game()

    assert oracle_action_profile(game, 0) == (0, 0, 0)
    assert oracle_action_profile(game, 1) == (1, 1, 1)
    assert full_information_nash_equilibria(game, 1) == ((1, 1, 1),)

    early_growth = realized_growths(game, 1, (1, 1, 1))
    assert all(value > 0.0 for value in early_growth)


def test_information_deficit_exists_without_full_information_coordination_deficit():
    diagnostic = information_deficit_diagnostic(canonical_game())

    assert diagnostic.oracle_expected_mean_growth == pytest.approx(0.2666666667)
    assert (
        diagnostic.full_information_equilibrium_expected_mean_growth
        == pytest.approx(0.2666666667)
    )
    assert (
        diagnostic.partial_information_equilibrium_expected_mean_growth
        == pytest.approx(0.1333333333)
    )
    assert diagnostic.coordination_deficit == pytest.approx(0.0)
    assert diagnostic.information_deficit == pytest.approx(0.1333333333)
    assert diagnostic.total_deficit == pytest.approx(0.1333333333)
    assert diagnostic.information_only_trap


def test_realized_early_state_can_be_bad_despite_existing_viable_solution():
    game = canonical_game()

    oracle = realized_growths(game, 1, (1, 1, 1))
    incomplete_information = realized_growths(game, 1, (1, 1, 0))

    assert oracle == pytest.approx((0.25, 0.25, 0.10))
    assert incomplete_information == pytest.approx((0.15, 0.15, -0.50))


def test_crossing_cue_reliability_threshold_switches_migrant_policy():
    below = pure_bayesian_nash_equilibria(
        canonical_game(migrant_accuracy=0.66)
    )
    above = pure_bayesian_nash_equilibria(
        canonical_game(migrant_accuracy=0.70)
    )

    assert len(below) == 1
    assert below[0].policies[2] == ALWAYS_BASELINE
    assert len(above) == 1
    assert above[0].policies[2] == FOLLOW_CUE


def test_perfect_migrant_information_removes_information_deficit():
    diagnostic = information_deficit_diagnostic(
        canonical_game(migrant_accuracy=1.0)
    )

    assert diagnostic.information_deficit == pytest.approx(0.0)
    assert diagnostic.total_deficit == pytest.approx(0.0)
    assert not diagnostic.information_only_trap
