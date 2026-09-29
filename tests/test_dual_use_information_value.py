import pytest

from src.dual_use_information_value import (
    balanced_dual_use_pair_window,
    balanced_dual_use_threshold_slope_in_compensation_loss,
    balanced_dual_use_wait_threshold,
    compensation_information_rescue_interval,
    dual_use_information_values,
    dual_use_wait_threshold,
    dual_use_waiting_margin,
)


ACTION = dict(
    action_prior_early=0.4,
    action_false_early_cost=2.0,
    action_missed_early_cost=1.0,
)

COMP = dict(
    compensation_prior_early=0.5,
    compensation_false_early_cost=1.0,
    compensation_missed_early_cost=1.0,
)


def test_same_cue_value_decomposes_into_two_nonnegative_components():
    va, vc = dual_use_information_values(
        0.90,
        **ACTION,
        **COMP,
    )
    assert va == pytest.approx(0.24)
    assert vc == pytest.approx(0.40)


def test_compensation_information_alone_cannot_justify_waiting():
    # The action cue is not yet actionable at q=0.70 (action q0=0.75).
    va, vc = dual_use_information_values(
        0.70,
        **ACTION,
        **COMP,
    )
    assert va == pytest.approx(0.0)
    assert vc == pytest.approx(0.20)

    margin = dual_use_waiting_margin(
        0.70,
        direct_wait_cost=0.10,
        **ACTION,
        **COMP,
    )
    # Compensation prior risk is 0.50, so Vc alone cannot pay J + R_C0.
    assert margin == pytest.approx(0.20 - 0.10 - 0.50)
    assert margin < 0.0


def test_dual_use_information_can_rescue_waiting_when_action_only_never_does():
    result = dual_use_wait_threshold(
        direct_wait_cost=0.10,
        **ACTION,
        **COMP,
    )
    # Without compensation information, the waiting burden is
    # J + R_C0 = 0.60 > action R0 = 0.40, so action information alone
    # is never worth waiting for.
    assert not result.action_only_ever_waits
    assert result.action_only_wait_threshold is None

    # With the same cue also informing compensation:
    # Va + Vc = (1.6q-1.2) + (q-0.5) = 2.6q-1.7
    # equality with 0.60 gives q=2.3/2.6.
    assert result.dual_use_ever_waits
    assert result.dual_use_wait_threshold == pytest.approx(2.3 / 2.6)

    just_above = result.dual_use_wait_threshold + 1e-5
    assert dual_use_waiting_margin(
        just_above,
        direct_wait_cost=0.10,
        **ACTION,
        **COMP,
    ) > 0.0


def test_dual_use_threshold_cannot_fall_below_action_actionability_boundary():
    for direct in (0.0, 0.05, 0.10, 0.20, 0.39):
        result = dual_use_wait_threshold(
            direct_wait_cost=direct,
            **ACTION,
            **COMP,
        )
        if result.dual_use_ever_waits:
            assert result.dual_use_wait_threshold is not None
            assert (
                result.dual_use_wait_threshold
                >= result.action_actionable_q
            )


def test_perfect_dual_use_information_can_never_overcome_direct_cost_at_action_value_limit():
    # Maximum action information value is R_A0=0.4.
    at_limit = dual_use_wait_threshold(
        direct_wait_cost=0.40,
        **ACTION,
        **COMP,
    )
    above = dual_use_wait_threshold(
        direct_wait_cost=0.50,
        **ACTION,
        **COMP,
    )
    assert not at_limit.dual_use_ever_waits
    assert at_limit.dual_use_wait_threshold is None
    assert not above.dual_use_ever_waits


def test_exact_rescue_interval():
    interval = compensation_information_rescue_interval(
        **ACTION,
        **COMP,
    )
    # R_A0=0.40 and R_C0=0.50 -> [0, 0.40).
    assert interval == pytest.approx((0.0, 0.40))

    inside = dual_use_wait_threshold(
        direct_wait_cost=0.20,
        **ACTION,
        **COMP,
    )
    assert not inside.action_only_ever_waits
    assert inside.dual_use_ever_waits


def test_dual_use_information_never_raises_threshold_relative_to_action_only():
    # Use a small compensation burden so action-only waiting remains feasible.
    small_comp = dict(
        compensation_prior_early=0.5,
        compensation_false_early_cost=0.10,
        compensation_missed_early_cost=0.10,
    )
    result = dual_use_wait_threshold(
        direct_wait_cost=0.05,
        **ACTION,
        **small_comp,
    )
    assert result.action_only_ever_waits
    assert result.dual_use_ever_waits
    assert result.action_only_wait_threshold is not None
    assert result.dual_use_wait_threshold is not None
    assert (
        result.dual_use_wait_threshold
        <= result.action_only_wait_threshold
    )


@pytest.mark.parametrize("action_prior", [0.3, 0.4, 0.6])
@pytest.mark.parametrize("action_costs", [(2.0, 1.0), (1.0, 2.0), (1.0, 1.0)])
@pytest.mark.parametrize("comp_prior", [0.3, 0.5, 0.7])
@pytest.mark.parametrize("comp_costs", [(1.0, 1.0), (0.5, 1.0), (1.0, 0.5)])
@pytest.mark.parametrize("direct", [0.0, 0.05, 0.20, 0.50])
def test_closed_form_threshold_matches_margin_sign_across_grid(
    action_prior,
    action_costs,
    comp_prior,
    comp_costs,
    direct,
):
    params = dict(
        action_prior_early=action_prior,
        action_false_early_cost=action_costs[0],
        action_missed_early_cost=action_costs[1],
        compensation_prior_early=comp_prior,
        compensation_false_early_cost=comp_costs[0],
        compensation_missed_early_cost=comp_costs[1],
    )
    result = dual_use_wait_threshold(
        direct_wait_cost=direct,
        **params,
    )

    perfect_margin = dual_use_waiting_margin(
        1.0,
        direct_wait_cost=direct,
        **params,
    )

    if not result.dual_use_ever_waits:
        assert result.dual_use_wait_threshold is None
        assert perfect_margin <= 1e-10
        return

    threshold = result.dual_use_wait_threshold
    assert threshold is not None
    assert threshold >= result.action_actionable_q - 1e-10

    at_threshold = dual_use_waiting_margin(
        threshold,
        direct_wait_cost=direct,
        **params,
    )
    assert at_threshold == pytest.approx(0.0, abs=1e-9)

    epsilon = 1e-7
    below = max(0.5, threshold - epsilon)
    above = min(1.0, threshold + epsilon)

    assert dual_use_waiting_margin(
        below,
        direct_wait_cost=direct,
        **params,
    ) <= 1e-8
    assert dual_use_waiting_margin(
        above,
        direct_wait_cost=direct,
        **params,
    ) >= -1e-8

    if result.action_only_ever_waits:
        assert result.action_only_wait_threshold is not None
        assert threshold <= result.action_only_wait_threshold + 1e-10


def test_zero_value_compensation_module_recovers_original_threshold():
    zero_value_comp = dict(
        compensation_prior_early=0.5,
        compensation_false_early_cost=0.0,
        compensation_missed_early_cost=1.0,
    )
    result = dual_use_wait_threshold(
        direct_wait_cost=0.10,
        **ACTION,
        **zero_value_comp,
    )

    # Compensation prior Bayes risk is zero, so the cue cannot improve that
    # module and the theorem collapses to the original action-only threshold:
    # (1.2 + 0.1)/1.6 = 0.8125.
    assert result.compensation_prior_risk == pytest.approx(0.0)
    assert result.action_only_ever_waits
    assert result.dual_use_ever_waits
    assert result.action_only_wait_threshold == pytest.approx(0.8125)
    assert result.dual_use_wait_threshold == pytest.approx(0.8125)



def test_balanced_dual_use_threshold_closed_form():
    q = balanced_dual_use_wait_threshold(
        direct_wait_cost=0.10,
        compensation_loss=1.0,
        **ACTION,
    )
    # (B+J+G)/(S+G) = (1.2+0.1+1)/(1.6+1) = 2.3/2.6.
    assert q == pytest.approx(2.3 / 2.6)


def test_compensation_geometry_alone_creates_pairwise_asynchrony():
    window = balanced_dual_use_pair_window(
        direct_wait_cost=0.10,
        actor_1_compensation_loss=0.20,
        actor_2_compensation_loss=1.00,
        **ACTION,
    )
    assert window.regime == "FINITE_DUAL_USE_ASYNCHRONY"
    assert window.actor_1_wait_threshold == pytest.approx(
        (1.2 + 0.1 + 0.2) / (1.6 + 0.2)
    )
    assert window.actor_2_wait_threshold == pytest.approx(2.3 / 2.6)
    assert window.finite_window_width == pytest.approx(
        window.upper_wait_threshold - window.lower_wait_threshold
    )
    assert window.finite_window_width == pytest.approx(
        (1.00 - 0.20) * (0.40 - 0.10)
        / ((1.60 + 0.20) * (1.60 + 1.00))
    )


def test_equal_compensation_geometry_erases_dual_use_asynchrony():
    window = balanced_dual_use_pair_window(
        direct_wait_cost=0.10,
        actor_1_compensation_loss=0.50,
        actor_2_compensation_loss=0.50,
        **ACTION,
    )
    assert window.regime == "NO_ASYNCHRONY_EQUAL_COMPENSATION_GEOMETRY"
    assert window.finite_window_width == pytest.approx(0.0)
    assert window.actor_1_wait_threshold == pytest.approx(
        window.actor_2_wait_threshold
    )


def test_direct_cost_above_action_value_blocks_both_actors_regardless_of_G():
    window = balanced_dual_use_pair_window(
        direct_wait_cost=0.40,
        actor_1_compensation_loss=0.10,
        actor_2_compensation_loss=10.0,
        **ACTION,
    )
    assert window.regime == "NO_ONE_WAITS_DIRECT_COST_TOO_HIGH"
    assert window.actor_1_wait_threshold is None
    assert window.actor_2_wait_threshold is None


def test_more_severe_compensation_problem_raises_shared_q_threshold():
    q_small = balanced_dual_use_wait_threshold(
        direct_wait_cost=0.10,
        compensation_loss=0.20,
        **ACTION,
    )
    q_large = balanced_dual_use_wait_threshold(
        direct_wait_cost=0.10,
        compensation_loss=1.00,
        **ACTION,
    )
    assert q_small is not None and q_large is not None
    assert q_large > q_small

    slope = balanced_dual_use_threshold_slope_in_compensation_loss(
        direct_wait_cost=0.10,
        compensation_loss=0.50,
        **ACTION,
    )
    assert slope == pytest.approx(
        (0.40 - 0.10) / (1.60 + 0.50) ** 2
    )
    assert slope > 0.0


@pytest.mark.parametrize("g1", [0.0, 0.1, 0.5, 1.0, 2.0])
@pytest.mark.parametrize("g2", [0.0, 0.2, 0.7, 1.5, 3.0])
@pytest.mark.parametrize("direct", [0.0, 0.1, 0.2, 0.39])
def test_pairwise_width_identity_grid(g1, g2, direct):
    window = balanced_dual_use_pair_window(
        direct_wait_cost=direct,
        actor_1_compensation_loss=g1,
        actor_2_compensation_loss=g2,
        **ACTION,
    )
    assert window.actor_1_wait_threshold is not None
    assert window.actor_2_wait_threshold is not None
    assert window.finite_window_width == pytest.approx(
        abs(
            window.actor_2_wait_threshold
            - window.actor_1_wait_threshold
        )
    )
