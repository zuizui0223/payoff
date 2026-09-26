import pytest

from src.bayesian_timing_coordination import (
    ALWAYS_LATE,
    FOLLOW_CUE,
)
from src.endogenous_information_network import (
    all_commit_late_profile,
    all_wait_follow_profile,
    canonical_endogenous_information_network,
    evaluate_information_network,
    information_network_best_response_margins,
    is_strict_information_network_equilibrium,
    profile_labels,
    sequential_information_network_best_response,
)


def solve(q, interaction, initial):
    game = canonical_endogenous_information_network(
        q,
        interaction_strength=interaction,
    )
    return game, sequential_information_network_best_response(
        game,
        initial,
    ).final


def test_no_interaction_produces_asynchronous_information_uptake():
    late = all_commit_late_profile()

    _, low = solve(0.80, 0.0, late)
    _, middle1 = solve(0.85, 0.0, late)
    _, middle2 = solve(0.90, 0.0, late)
    _, high = solve(0.95, 0.0, late)

    assert profile_labels(low.profile) == (
        "always_late",
        "always_late",
        "always_late",
    )
    assert profile_labels(middle1.profile) == (
        "always_late",
        "follow_cue",
        "always_late",
    )
    assert profile_labels(middle2.profile) == (
        "always_late",
        "follow_cue",
        "follow_cue",
    )
    assert profile_labels(high.profile) == (
        "follow_cue",
        "follow_cue",
        "follow_cue",
    )


def test_moderate_interaction_synchronizes_uptake_but_creates_hysteresis():
    late = all_commit_late_profile()
    follow = all_wait_follow_profile()

    game_94 = canonical_endogenous_information_network(
        0.94,
        interaction_strength=0.50,
    )
    from_late = sequential_information_network_best_response(
        game_94,
        late,
    ).final
    from_follow = sequential_information_network_best_response(
        game_94,
        follow,
    ).final

    assert from_late.profile == late
    assert from_follow.profile == follow
    assert is_strict_information_network_equilibrium(
        game_94,
        late,
    )
    assert is_strict_information_network_equilibrium(
        game_94,
        follow,
    )
    assert from_follow.joint_payoff > from_late.joint_payoff

    game_95 = canonical_endogenous_information_network(
        0.95,
        interaction_strength=0.50,
    )
    escaped = sequential_information_network_best_response(
        game_95,
        late,
    ).final
    assert escaped.profile == follow


def test_moderate_interaction_has_different_up_and_down_thresholds():
    late = all_commit_late_profile()
    follow = all_wait_follow_profile()

    upward = late
    upward_switch = None
    for i in range(50, 101):
        q = i / 100
        game = canonical_endogenous_information_network(
            q,
            interaction_strength=0.50,
        )
        upward = sequential_information_network_best_response(
            game,
            upward,
        ).final.profile
        if upward_switch is None and upward == follow:
            upward_switch = q

    downward = follow
    downward_switch = None
    for i in range(100, 49, -1):
        q = i / 100
        game = canonical_endogenous_information_network(
            q,
            interaction_strength=0.50,
        )
        downward = sequential_information_network_best_response(
            game,
            downward,
        ).final.profile
        if downward_switch is None and downward == late:
            downward_switch = q

    assert upward_switch == pytest.approx(0.95)
    assert downward_switch == pytest.approx(0.87)
    assert upward_switch > downward_switch


def test_strong_interaction_can_trap_network_even_under_perfect_information():
    late = all_commit_late_profile()
    follow = all_wait_follow_profile()
    game = canonical_endogenous_information_network(
        1.0,
        interaction_strength=1.0,
    )

    from_late = sequential_information_network_best_response(
        game,
        late,
    ).final
    from_follow = sequential_information_network_best_response(
        game,
        follow,
    ).final

    assert from_late.profile == late
    assert from_follow.profile == follow
    assert is_strict_information_network_equilibrium(game, late)
    assert is_strict_information_network_equilibrium(game, follow)
    assert from_follow.joint_payoff > from_late.joint_payoff
    assert from_follow.joint_payoff == pytest.approx(-0.60)
    assert from_late.joint_payoff == pytest.approx(-1.20)


def test_strong_perfect_information_trap_has_positive_unilateral_margins():
    game = canonical_endogenous_information_network(
        1.0,
        interaction_strength=1.0,
    )
    margins = information_network_best_response_margins(
        game,
        all_commit_late_profile(),
    )

    assert margins == pytest.approx((0.30, 0.10, 0.20))


def test_follow_cue_pays_delay_cost_even_when_information_is_perfect():
    game = canonical_endogenous_information_network(
        1.0,
        interaction_strength=0.0,
    )
    follow = evaluate_information_network(
        game,
        all_wait_follow_profile(),
    )

    assert follow.expected_payoffs == pytest.approx(
        (-0.30, -0.10, -0.20)
    )


def test_chain_topology_preserves_unified_hysteresis_at_moderate_coupling():
    late = all_commit_late_profile()
    follow = all_wait_follow_profile()
    game = canonical_endogenous_information_network(
        0.94,
        interaction_strength=0.50,
        interaction_topology="chain",
    )

    from_late = sequential_information_network_best_response(
        game,
        late,
    ).final
    from_follow = sequential_information_network_best_response(
        game,
        follow,
    ).final

    assert from_late.profile == late
    assert from_follow.profile == follow
