import pytest

from src.partial_information_coordination import (
    PartialInformationTimingGame,
    critical_early_cue_accuracy,
    evaluate_partial_information_game,
    joint_action_threshold,
    posterior_early,
    private_action_threshold,
)


def canonical_game(**kwargs):
    defaults = dict(
        prior_early=0.55,
        cue_accuracy=0.55,
        false_early_cost=2.0,
        missed_early_cost=1.0,
        migrant_interaction_mismatch_cost=0.5,
        resident_interaction_mismatch_cost_per_partner=1.0,
        resident_partners=2,
    )
    defaults.update(kwargs)
    return PartialInformationTimingGame(**defaults)


def test_bayes_posterior_is_exact_for_symmetric_remote_cue():
    game = canonical_game()
    assert posterior_early(game, "early") == pytest.approx(
        0.3025 / (0.3025 + 0.2025)
    )
    assert posterior_early(game, "late") == pytest.approx(0.5)


def test_resident_externality_lowers_joint_evidence_threshold():
    game = canonical_game()
    assert private_action_threshold(game) == pytest.approx(0.625)
    assert joint_action_threshold(game) == pytest.approx(0.5625)
    assert joint_action_threshold(game) < private_action_threshold(game)


def test_canonical_case_has_information_coordination_wedge():
    diagnostic = evaluate_partial_information_game(canonical_game())

    assert diagnostic.early_cue_private_action == "late"
    assert diagnostic.early_cue_joint_action == "early"
    assert diagnostic.early_cue_regime == "information_coordination_wedge"
    assert diagnostic.coordination_deficit > 0.0
    assert diagnostic.information_deficit > 0.0


def test_critical_accuracy_brackets_the_canonical_wedge():
    diagnostic = evaluate_partial_information_game(canonical_game())

    assert diagnostic.private_critical_accuracy == pytest.approx(
        0.5769230769230769
    )
    assert diagnostic.joint_critical_accuracy == pytest.approx(
        0.5126582278481012
    )
    assert diagnostic.accuracy_wedge_width == pytest.approx(
        0.0642648490749757
    )
    assert (
        diagnostic.joint_critical_accuracy
        < 0.55
        < diagnostic.private_critical_accuracy
    )


def test_high_reliability_aligns_private_and_joint_early_action():
    diagnostic = evaluate_partial_information_game(
        canonical_game(cue_accuracy=0.8)
    )
    assert diagnostic.early_cue_private_action == "early"
    assert diagnostic.early_cue_joint_action == "early"
    assert diagnostic.early_cue_regime == "aligned_early"


def test_low_reliability_becomes_information_limited():
    diagnostic = evaluate_partial_information_game(
        canonical_game(cue_accuracy=0.5)
    )
    assert diagnostic.early_cue_private_action == "late"
    assert diagnostic.early_cue_joint_action == "late"
    assert diagnostic.early_cue_regime == "information_limited"


def test_externality_is_required_for_coordination_deficit():
    diagnostic = evaluate_partial_information_game(
        canonical_game(
            resident_interaction_mismatch_cost_per_partner=0.0,
        )
    )
    assert diagnostic.private_threshold == pytest.approx(
        diagnostic.joint_threshold
    )
    assert diagnostic.accuracy_wedge_width == pytest.approx(0.0)
    assert diagnostic.coordination_deficit == pytest.approx(0.0)


def test_deficit_decomposition_is_exact():
    diagnostic = evaluate_partial_information_game(canonical_game())
    assert diagnostic.capacity_deficit == pytest.approx(0.0)
    assert diagnostic.total_adaptation_deficit == pytest.approx(
        diagnostic.capacity_deficit
        + diagnostic.information_deficit
        + diagnostic.coordination_deficit
    )
    assert diagnostic.expected_joint_loss_private_policy == pytest.approx(
        diagnostic.total_adaptation_deficit
    )


@pytest.mark.parametrize("threshold", [0.2, 0.5, 0.8])
def test_critical_accuracy_inverts_early_cue_posterior(threshold):
    prior = 0.55
    q = critical_early_cue_accuracy(prior, threshold)
    game = PartialInformationTimingGame(
        prior_early=prior,
        cue_accuracy=max(0.5, q),
    )
    if q >= 0.5:
        assert posterior_early(game, "early") == pytest.approx(threshold)
