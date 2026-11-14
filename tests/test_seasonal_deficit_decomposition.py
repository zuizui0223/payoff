"""Regression tests for crossed counterfactual deficit allocation."""
from itertools import product
from math import isclose
from random import Random

import pytest

from src.seasonal_deficit_decomposition import decompose_seasonal_deficit


def first_witness():
    return decompose_seasonal_deficit(
        prior_early=0.55,
        cue_accuracy=0.55,
        joint_losses={
            "late": (0.0, 3.5),
            "early": (4.5, 0.0),
            "buffer": (1.0, 1.0),
        },
        private_losses={
            "late": (0.0, 1.5),
            "early": (2.5, 0.0),
            "buffer": (1.0, 1.0),
        },
        limited_actions=("late", "early"),
        full_actions=("late", "early", "buffer"),
    )


def test_witness_has_all_three_positive_deficits():
    x = first_witness()
    assert x.full_perfect == pytest.approx(0)
    assert x.limited_perfect == pytest.approx(0)
    assert x.full_cue == pytest.approx(1.0)
    assert x.limited_cue == pytest.approx(1.7775)
    assert x.decentralized_cue == pytest.approx(1.925)
    assert x.information_deficit == pytest.approx(1.38875)
    assert x.capacity_deficit == pytest.approx(0.38875)
    assert x.coordination_deficit == pytest.approx(0.1475)
    assert x.total_deficit == pytest.approx(1.925)
    assert x.information_capacity_interaction == pytest.approx(0.7775)


def test_witness_private_and_joint_early_cue_disagree():
    x = first_witness()
    assert (x.joint_policy_late_cue, x.joint_policy_early_cue) == (
        "late", "early"
    )
    assert (
        x.decentralized_policy_late_cue,
        x.decentralized_policy_early_cue,
    ) == ("late", "late")


def test_more_capacity_can_erase_some_information_value():
    x = first_witness()
    assert x.information_if_limited_capacity == pytest.approx(1.7775)
    assert x.information_if_full_capacity == pytest.approx(1)
    assert x.capacity_if_perfect_information == pytest.approx(0)
    assert x.capacity_if_available_cue == pytest.approx(0.7775)


def test_lost_action_can_erase_information_value_entirely():
    x = decompose_seasonal_deficit(
        prior_early=0.4,
        cue_accuracy=0.8,
        joint_losses={"late": (0.0, 1.0), "early": (2.0, 0.0)},
        private_losses={"late": (0.0, 1.0), "early": (2.0, 0.0)},
        limited_actions=("late",),
        full_actions=("late", "early"),
    )
    assert x.information_if_limited_capacity == pytest.approx(0)
    assert x.information_if_full_capacity == pytest.approx(0.32)
    assert x.capacity_if_available_cue == pytest.approx(0.08)
    assert x.capacity_if_perfect_information == pytest.approx(0.4)
    assert x.information_capacity_interaction == pytest.approx(-0.32)
    assert x.information_deficit == pytest.approx(0.16)
    assert x.capacity_deficit == pytest.approx(0.24)
    assert x.coordination_deficit == pytest.approx(0)
    assert x.total_deficit == pytest.approx(0.4)


def test_no_capacity_difference_gives_zero_capacity_allocation():
    x = decompose_seasonal_deficit(
        prior_early=0.55,
        cue_accuracy=0.55,
        joint_losses={"late": (0, 3.5), "early": (4.5, 0)},
        private_losses={"late": (0, 1.5), "early": (2.5, 0)},
        limited_actions=("late", "early"),
        full_actions=("late", "early"),
    )
    assert x.capacity_deficit == pytest.approx(0)
    assert x.information_capacity_interaction == pytest.approx(0)
    assert x.coordination_deficit > 0


def test_private_equals_joint_has_no_coordination_deficit():
    losses = {"late": (0, 2), "early": (3, 0), "buffer": (0.8, 0.8)}
    x = decompose_seasonal_deficit(
        prior_early=0.4,
        cue_accuracy=0.8,
        joint_losses=losses,
        private_losses=losses,
        limited_actions=("late", "early"),
        full_actions=("late", "early", "buffer"),
    )
    assert x.coordination_deficit == pytest.approx(0)


def test_perfect_information_cue_equals_perfect_information_risk():
    losses = {"late": (0.2, 1), "early": (2, 0.3)}
    x = decompose_seasonal_deficit(
        prior_early=0.35,
        cue_accuracy=1.0,
        joint_losses=losses,
        private_losses=losses,
        limited_actions=("late", "early"),
        full_actions=("late", "early"),
    )
    assert x.full_perfect == pytest.approx(0.235)
    assert x.full_cue == pytest.approx(x.full_perfect)
    assert x.information_deficit == pytest.approx(0)
    assert x.total_deficit == pytest.approx(0)


def _exact_policy_risk(prior, q, actions, choosing_losses, scoring_losses):
    def expected_loss(policy):
        value = 0.0
        for state, state_prob in ((0, 1 - prior), (1, prior)):
            for cue in (0, 1):
                cue_prob = q if state == cue else 1 - q
                value += state_prob * cue_prob * scoring_losses[policy[cue]][state]
        return value
    all_policies = list(product(actions, repeat=2))
    winning = min(all_policies, key=lambda policy: _loss_for(policy, choosing_losses, prior, q))
    return expected_loss(winning)


def _loss_for(policy, losses, prior, q):
    return sum(
        state_prob * (q if state == cue else 1 - q) * losses[policy[cue]][state]
        for state, state_prob in ((0, 1 - prior), (1, prior))
        for cue in (0, 1)
    )


def test_independent_policy_enumeration_and_nonnegative_identity():
    rng = Random(20261114)
    actions = ("a", "b", "c")
    for _ in range(120):
        prior = rng.uniform(0.05, 0.95)
        q = rng.uniform(0.5, 1.0)
        joint = {a: (rng.uniform(0, 6), rng.uniform(0, 6)) for a in actions}
        private = {a: (rng.uniform(0, 6), rng.uniform(0, 6)) for a in actions}
        lim = ("a", "b")
        full = actions
        d = decompose_seasonal_deficit(
            prior_early=prior,
            cue_accuracy=q,
            joint_losses=joint,
            private_losses=private,
            limited_actions=lim,
            full_actions=full,
        )
        # Independent enumeration of every two-cue pure policy, no posterior
        # thresholds or special-case formulas used.
        assert d.limited_cue == pytest.approx(
            min(_loss_for(policy, joint, prior, q) for policy in product(lim, repeat=2))
        )
        assert d.full_cue == pytest.approx(
            min(_loss_for(policy, joint, prior, q) for policy in product(full, repeat=2))
        )
        assert d.decentralized_cue == pytest.approx(
            _exact_policy_risk(prior, q, lim, private, joint)
        )
        assert d.information_deficit >= -1e-10
        assert d.capacity_deficit >= -1e-10
        assert d.coordination_deficit >= -1e-10
        assert d.information_deficit + d.capacity_deficit + d.coordination_deficit == pytest.approx(d.total_deficit)
        assert d.information_capacity_interaction == pytest.approx(
            d.capacity_if_available_cue - d.capacity_if_perfect_information
        )


@pytest.mark.parametrize("kwargs", [
    {"prior_early": 0.0},
    {"prior_early": float("nan")},
    {"cue_accuracy": 0.49},
    {"cue_accuracy": 1.01},
    {"limited_actions": ()},
    {"limited_actions": ("late", "late")},
    {"limited_actions": ("nonexistent",)},
    {"joint_losses": {"late": (-1, 1), "early": (1, 0)}},
    {"private_losses": {"late": (0, 1)}},
])
def test_invalid_counterfactual_inputs_fail_closed(kwargs):
    args = dict(
        prior_early=0.5,
        cue_accuracy=0.8,
        joint_losses={"late": (0, 1), "early": (2, 0)},
        private_losses={"late": (0, 1), "early": (2, 0)},
        limited_actions=("late",),
        full_actions=("late", "early"),
    )
    args.update(kwargs)
    with pytest.raises(ValueError):
        decompose_seasonal_deficit(**args)
