import pytest

from src.dual_use_information_value import (
    balanced_dual_use_pair_window,
    balanced_dual_use_threshold_headroom,
    balanced_dual_use_threshold_slope_in_compensation_loss,
    general_balanced_dual_use_pair_window,
    iso_threshold_direct_wait_cost,
    multi_module_dual_use_wait_threshold,
    multi_module_rescue_interval,
    multi_module_waiting_margin,
    identical_balanced_module_complexity_scaling,
    identical_balanced_module_count_window,
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



def test_general_pairwise_headroom_identity():
    window = general_balanced_dual_use_pair_window(
        actor_1_direct_wait_cost=0.05,
        actor_1_compensation_loss=0.20,
        actor_2_direct_wait_cost=0.20,
        actor_2_compensation_loss=1.00,
        **ACTION,
    )
    h1 = (0.40 - 0.05) / (1.60 + 0.20)
    h2 = (0.40 - 0.20) / (1.60 + 1.00)
    assert window.actor_1_headroom == pytest.approx(h1)
    assert window.actor_2_headroom == pytest.approx(h2)
    assert window.actor_1_wait_threshold == pytest.approx(1.0 - h1)
    assert window.actor_2_wait_threshold == pytest.approx(1.0 - h2)
    assert window.finite_window_width == pytest.approx(abs(h1 - h2))


def test_J_and_G_can_exactly_offset_on_iso_threshold_contour():
    j_target = iso_threshold_direct_wait_cost(
        reference_direct_wait_cost=0.20,
        reference_compensation_loss=0.20,
        target_compensation_loss=0.80,
        **ACTION,
    )
    assert j_target < 0.20

    window = general_balanced_dual_use_pair_window(
        actor_1_direct_wait_cost=0.20,
        actor_1_compensation_loss=0.20,
        actor_2_direct_wait_cost=j_target,
        actor_2_compensation_loss=0.80,
        **ACTION,
    )
    assert window.regime == "NO_ASYNCHRONY_EQUAL_HEADROOM"
    assert window.finite_window_width == pytest.approx(0.0)
    assert window.actor_1_wait_threshold == pytest.approx(
        window.actor_2_wait_threshold
    )


def test_one_actor_can_never_wait_while_other_has_finite_threshold():
    window = general_balanced_dual_use_pair_window(
        actor_1_direct_wait_cost=0.10,
        actor_1_compensation_loss=1.00,
        actor_2_direct_wait_cost=0.40,
        actor_2_compensation_loss=0.00,
        **ACTION,
    )
    assert window.regime == "PERSISTENT_DUAL_USE_ASYMMETRY"
    assert window.actor_1_wait_threshold is not None
    assert window.actor_2_wait_threshold is None
    assert window.upper_wait_threshold == pytest.approx(1.0)
    assert window.finite_window_width is None


@pytest.mark.parametrize("j1", [0.0, 0.1, 0.25, 0.39])
@pytest.mark.parametrize("j2", [0.0, 0.05, 0.2, 0.39])
@pytest.mark.parametrize("g1", [0.0, 0.3, 1.0])
@pytest.mark.parametrize("g2", [0.0, 0.7, 2.0])
def test_general_pairwise_width_is_absolute_headroom_difference(
    j1, j2, g1, g2
):
    window = general_balanced_dual_use_pair_window(
        actor_1_direct_wait_cost=j1,
        actor_1_compensation_loss=g1,
        actor_2_direct_wait_cost=j2,
        actor_2_compensation_loss=g2,
        **ACTION,
    )
    assert window.actor_1_headroom is not None
    assert window.actor_2_headroom is not None
    assert window.finite_window_width == pytest.approx(
        abs(window.actor_1_headroom - window.actor_2_headroom)
    )



def test_multi_module_no_conditional_modules_reduces_to_original_threshold():
    result = multi_module_dual_use_wait_threshold(
        direct_wait_cost=0.10,
        conditional_modules=[],
        **ACTION,
    )
    assert result.ever_waits
    assert result.conditional_module_count == 0
    assert result.wait_threshold == pytest.approx((1.20 + 0.10) / 1.60)


def test_multi_module_perfect_information_feasibility_ignores_conditional_burden():
    huge_modules = [
        (0.5, 100.0, 100.0),
        (0.3, 200.0, 50.0),
        (0.7, 50.0, 200.0),
    ]
    below = multi_module_dual_use_wait_threshold(
        direct_wait_cost=0.39,
        conditional_modules=huge_modules,
        **ACTION,
    )
    at = multi_module_dual_use_wait_threshold(
        direct_wait_cost=0.40,
        conditional_modules=huge_modules,
        **ACTION,
    )
    assert below.ever_waits
    assert below.wait_threshold is not None
    assert not at.ever_waits
    assert at.wait_threshold is None


def test_two_balanced_modules_have_exact_high_q_headroom():
    modules = [
        (0.5, 1.0, 1.0),
        (0.5, 1.0, 1.0),
    ]
    result = multi_module_dual_use_wait_threshold(
        direct_wait_cost=0.10,
        conditional_modules=modules,
        **ACTION,
    )
    # Target J + 2*0.5 = 1.1.
    # In the all-active region:
    # Va + V1 + V2 = (1.6q-1.2) + 2(q-0.5)
    #                  = 3.6q - 2.2.
    # 3.6q - 2.2 = 1.1 -> q = 3.3/3.6.
    assert result.wait_threshold == pytest.approx(3.3 / 3.6)
    assert result.all_modules_active_at_threshold
    assert result.high_q_headroom == pytest.approx(
        (0.40 - 0.10) / (1.60 + 1.0 + 1.0)
    )
    assert result.wait_threshold == pytest.approx(
        1.0 - result.high_q_headroom
    )


def test_multi_module_rescue_interval_depends_on_total_conditional_prior_burden():
    modules = [
        (0.5, 0.20, 0.20),  # prior risk .10
        (0.5, 0.40, 0.40),  # prior risk .20
    ]
    interval = multi_module_rescue_interval(
        conditional_modules=modules,
        **ACTION,
    )
    # R_A0=.40; total conditional prior burden=.30.
    assert interval == pytest.approx((0.10, 0.40))

    result = multi_module_dual_use_wait_threshold(
        direct_wait_cost=0.20,
        conditional_modules=modules,
        **ACTION,
    )
    assert result.ever_waits
    assert result.wait_threshold is not None


def test_conditional_information_alone_never_generates_positive_margin_before_action_q0():
    modules = [
        (0.5, 10.0, 10.0),
        (0.5, 20.0, 20.0),
    ]
    for q in (0.50, 0.55, 0.60, 0.70, 0.749999):
        assert multi_module_waiting_margin(
            q,
            direct_wait_cost=0.0,
            conditional_modules=modules,
            **ACTION,
        ) <= 1e-10


@pytest.mark.parametrize("direct", [0.0, 0.05, 0.20, 0.39])
@pytest.mark.parametrize(
    "modules",
    [
        [],
        [(0.5, 1.0, 1.0)],
        [(0.3, 0.5, 1.0), (0.7, 1.0, 0.5)],
        [(0.2, 2.0, 1.0), (0.5, 0.2, 0.2), (0.8, 1.0, 2.0)],
    ],
)
def test_multi_module_threshold_matches_margin_sign(direct, modules):
    result = multi_module_dual_use_wait_threshold(
        direct_wait_cost=direct,
        conditional_modules=modules,
        **ACTION,
    )
    assert result.ever_waits
    threshold = result.wait_threshold
    assert threshold is not None

    assert multi_module_waiting_margin(
        threshold,
        direct_wait_cost=direct,
        conditional_modules=modules,
        **ACTION,
    ) == pytest.approx(0.0, abs=1e-8)

    eps = 1e-7
    assert multi_module_waiting_margin(
        max(0.5, threshold - eps),
        direct_wait_cost=direct,
        conditional_modules=modules,
        **ACTION,
    ) <= 1e-7
    assert multi_module_waiting_margin(
        min(1.0, threshold + eps),
        direct_wait_cost=direct,
        conditional_modules=modules,
        **ACTION,
    ) >= -1e-7



def test_wait_contingent_decision_complexity_cannot_lower_threshold_below_no_problem_world():
    no_problem = multi_module_dual_use_wait_threshold(
        direct_wait_cost=0.10,
        conditional_modules=[],
        **ACTION,
    )
    one_problem = multi_module_dual_use_wait_threshold(
        direct_wait_cost=0.10,
        conditional_modules=[(0.5, 0.20, 0.20)],
        **ACTION,
    )
    two_problems = multi_module_dual_use_wait_threshold(
        direct_wait_cost=0.10,
        conditional_modules=[
            (0.5, 0.20, 0.20),
            (0.5, 0.40, 0.40),
        ],
        **ACTION,
    )

    assert no_problem.wait_threshold is not None
    assert one_problem.wait_threshold is not None
    assert two_problems.wait_threshold is not None

    assert one_problem.wait_threshold >= no_problem.wait_threshold
    assert two_problems.wait_threshold >= no_problem.wait_threshold


@pytest.mark.parametrize(
    "modules",
    [
        [(0.5, 0.20, 0.20)],
        [(0.3, 0.50, 1.00), (0.7, 1.00, 0.50)],
        [(0.2, 2.0, 1.0), (0.5, 0.2, 0.2), (0.8, 1.0, 2.0)],
    ],
)
def test_conditional_modules_never_improve_waiting_margin_relative_to_no_problem(modules):
    for q in (0.50, 0.60, 0.75, 0.85, 0.95, 1.00):
        no_problem = multi_module_waiting_margin(
            q,
            direct_wait_cost=0.10,
            conditional_modules=[],
            **ACTION,
        )
        with_problems = multi_module_waiting_margin(
            q,
            direct_wait_cost=0.10,
            conditional_modules=modules,
            **ACTION,
        )
        assert with_problems <= no_problem + 1e-10



def test_identical_module_complexity_closed_form():
    result = identical_balanced_module_complexity_scaling(
        direct_wait_cost=0.10,
        conditional_module_count=3,
        conditional_loss=0.50,
        **ACTION,
    )
    expected_headroom = (0.40 - 0.10) / (1.60 + 3 * 0.50)
    assert result.headroom == pytest.approx(expected_headroom)
    assert result.wait_threshold == pytest.approx(
        1.0 - expected_headroom
    )


def test_more_identical_conditional_decisions_push_threshold_toward_one():
    thresholds = []
    for n in (0, 1, 2, 5, 10, 100):
        result = identical_balanced_module_complexity_scaling(
            direct_wait_cost=0.10,
            conditional_module_count=n,
            conditional_loss=0.50,
            **ACTION,
        )
        assert result.wait_threshold is not None
        thresholds.append(result.wait_threshold)

    assert thresholds == sorted(thresholds)
    assert thresholds[0] == pytest.approx((1.20 + 0.10) / 1.60)
    assert thresholds[-1] > 0.99


def test_complexity_penalty_has_positive_first_and_negative_second_derivative():
    result = identical_balanced_module_complexity_scaling(
        direct_wait_cost=0.10,
        conditional_module_count=4,
        conditional_loss=0.50,
        **ACTION,
    )
    assert result.first_derivative_continuous_n is not None
    assert result.second_derivative_continuous_n is not None
    assert result.first_derivative_continuous_n > 0.0
    assert result.second_derivative_continuous_n < 0.0


def test_zero_severity_modules_do_not_change_threshold():
    baseline = identical_balanced_module_complexity_scaling(
        direct_wait_cost=0.10,
        conditional_module_count=0,
        conditional_loss=0.0,
        **ACTION,
    )
    many = identical_balanced_module_complexity_scaling(
        direct_wait_cost=0.10,
        conditional_module_count=100,
        conditional_loss=0.0,
        **ACTION,
    )
    assert baseline.wait_threshold == pytest.approx(many.wait_threshold)
    assert many.first_derivative_continuous_n == pytest.approx(0.0)
    assert many.second_derivative_continuous_n == pytest.approx(0.0)


def test_module_count_heterogeneity_alone_creates_asynchronous_window():
    width = identical_balanced_module_count_window(
        direct_wait_cost=0.10,
        actor_1_module_count=1,
        actor_2_module_count=4,
        conditional_loss=0.50,
        **ACTION,
    )
    expected = (
        (0.40 - 0.10)
        * 0.50
        * 3
        / ((1.60 + 1 * 0.50) * (1.60 + 4 * 0.50))
    )
    assert width == pytest.approx(expected)
    assert width > 0.0


def test_direct_cost_limit_blocks_waiting_for_any_number_of_modules():
    for n in (0, 1, 10, 1000):
        result = identical_balanced_module_complexity_scaling(
            direct_wait_cost=0.40,
            conditional_module_count=n,
            conditional_loss=1.0,
            **ACTION,
        )
        assert result.wait_threshold is None
        assert result.headroom is None



def test_fixed_module_count_gap_has_shrinking_asynchrony_at_high_complexity():
    widths = []
    lower_thresholds = []
    for baseline_n in (0, 1, 5, 20, 100):
        width = identical_balanced_module_count_window(
            direct_wait_cost=0.10,
            actor_1_module_count=baseline_n,
            actor_2_module_count=baseline_n + 2,
            conditional_loss=0.50,
            **ACTION,
        )
        one = identical_balanced_module_complexity_scaling(
            direct_wait_cost=0.10,
            conditional_module_count=baseline_n,
            conditional_loss=0.50,
            **ACTION,
        )
        assert width is not None
        assert one.wait_threshold is not None
        widths.append(width)
        lower_thresholds.append(one.wait_threshold)

    assert widths == sorted(widths, reverse=True)
    assert lower_thresholds == sorted(lower_thresholds)
    assert lower_thresholds[-1] > 0.99
    assert widths[-1] < widths[0] / 100


def test_module_count_window_has_exact_fixed_gap_formula():
    n = 7
    k = 3
    g = 0.4
    width = identical_balanced_module_count_window(
        direct_wait_cost=0.10,
        actor_1_module_count=n,
        actor_2_module_count=n + k,
        conditional_loss=g,
        **ACTION,
    )
    expected = (
        (0.40 - 0.10)
        * g
        * k
        / ((1.60 + n * g) * (1.60 + (n + k) * g))
    )
    assert width == pytest.approx(expected)
