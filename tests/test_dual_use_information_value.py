import pytest

from src.dual_use_information_value import (
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
