"""Dual-use environmental information for PAYOFF-B.

A later cue can do two things after an actor waits:
1. improve the seasonal action;
2. improve the downstream compensation chosen to recover from waiting.

Under additive separability, the total value of the same cue decomposes exactly
into action information value plus compensation information value.

Let
    R_A0  = prior Bayes risk for the seasonal action,
    R_A(q)= post-cue seasonal Bayes risk,
    R_C0  = compensation risk if waiting occurred but compensation state were
            not informed by the cue,
    R_C(q)= compensation risk after using the cue,
    J     = direct nonrecoverable waiting cost.

Then waiting is optimal iff

    [R_A0-R_A(q)] + [R_C0-R_C(q)] > J + R_C0,

equivalently

    V_A(q) > J + R_C(q).

Thus compensation information can lower the effective cost of waiting, but it
cannot justify waiting by itself when the seasonal action value is zero.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from src.endogenous_information_timing import (
    closed_form_information_threshold,
    information_value,
    prior_bayes_risk,
)


@dataclass(frozen=True)
class BinaryInformationGeometry:
    prior_early: float
    false_early_cost: float
    missed_early_cost: float
    prior_risk: float
    total_prior_loss: float
    other_prior_loss: float
    actionable_q: float


@dataclass(frozen=True)
class DualUseThreshold:
    direct_wait_cost: float
    action_prior_risk: float
    compensation_prior_risk: float
    action_actionable_q: float
    compensation_actionable_q: float
    baseline_uninformed_waiting_burden: float
    action_only_wait_threshold: float | None
    action_only_ever_waits: bool
    dual_use_wait_threshold: float | None
    dual_use_ever_waits: bool


def _nonnegative(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x) or x < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return x


def binary_information_geometry(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
) -> BinaryInformationGeometry:
    """Geometry of the exact symmetric binary information-value function."""

    pi = float(prior_early)
    cf = _nonnegative("false_early_cost", false_early_cost)
    cm = _nonnegative("missed_early_cost", missed_early_cost)
    if not isfinite(pi) or not 0.0 < pi < 1.0:
        raise ValueError("prior_early must lie strictly between 0 and 1")
    if cf + cm <= 0.0:
        raise ValueError("at least one state-mismatch cost is required")

    early_loss = (1.0 - pi) * cf
    late_loss = pi * cm
    total = early_loss + late_loss
    if total <= 0.0:
        raise ValueError("prior loss scale must be positive")

    prior = min(early_loss, late_loss)
    other = max(early_loss, late_loss)
    return BinaryInformationGeometry(
        prior_early=pi,
        false_early_cost=cf,
        missed_early_cost=cm,
        prior_risk=prior,
        total_prior_loss=total,
        other_prior_loss=other,
        actionable_q=other / total,
    )


def dual_use_information_values(
    cue_accuracy: float,
    *,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
    compensation_prior_early: float,
    compensation_false_early_cost: float,
    compensation_missed_early_cost: float,
) -> tuple[float, float]:
    """Return action and compensation information values from the same cue."""

    q = float(cue_accuracy)
    if not isfinite(q) or not 0.5 <= q <= 1.0:
        raise ValueError("cue_accuracy must lie in [0.5, 1]")

    action = information_value(
        action_prior_early,
        q,
        action_false_early_cost,
        action_missed_early_cost,
    )
    compensation = information_value(
        compensation_prior_early,
        q,
        compensation_false_early_cost,
        compensation_missed_early_cost,
    )
    return action, compensation


def dual_use_waiting_margin(
    cue_accuracy: float,
    *,
    direct_wait_cost: float,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
    compensation_prior_early: float,
    compensation_false_early_cost: float,
    compensation_missed_early_cost: float,
) -> float:
    """Positive iff waiting is strictly better than immediate commitment."""

    direct = _nonnegative("direct_wait_cost", direct_wait_cost)
    action_value, compensation_value = dual_use_information_values(
        cue_accuracy,
        action_prior_early=action_prior_early,
        action_false_early_cost=action_false_early_cost,
        action_missed_early_cost=action_missed_early_cost,
        compensation_prior_early=compensation_prior_early,
        compensation_false_early_cost=compensation_false_early_cost,
        compensation_missed_early_cost=compensation_missed_early_cost,
    )
    compensation_prior = prior_bayes_risk(
        compensation_prior_early,
        compensation_false_early_cost,
        compensation_missed_early_cost,
    )
    return (
        action_value
        + compensation_value
        - direct
        - compensation_prior
    )


def _candidate_root(
    *,
    target: float,
    active_action: bool,
    active_compensation: bool,
    action: BinaryInformationGeometry,
    compensation: BinaryInformationGeometry,
) -> float | None:
    slope = 0.0
    intercept = 0.0
    if active_action:
        slope += action.total_prior_loss
        intercept += action.other_prior_loss
    if active_compensation:
        slope += compensation.total_prior_loss
        intercept += compensation.other_prior_loss
    if slope <= 0.0:
        return None
    return (target + intercept) / slope


def dual_use_wait_threshold(
    *,
    direct_wait_cost: float,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
    compensation_prior_early: float,
    compensation_false_early_cost: float,
    compensation_missed_early_cost: float,
    tolerance: float = 1e-12,
) -> DualUseThreshold:
    """Exact shared-cue threshold when the cue informs action and compensation.

    The compensation module represents the downstream decision that exists only
    after waiting has created a delay. Its prior Bayes risk R_C0 is therefore a
    burden of waiting. The same cue can reduce that burden by V_C(q).

    The threshold is the first q satisfying

        V_A(q) + V_C(q) > J + R_C0.

    Returned q is the equality boundary; with the PAYOFF-B tie rule, waiting
    occurs only for q strictly above it.
    """

    direct = _nonnegative("direct_wait_cost", direct_wait_cost)
    if not isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("tolerance must be finite and non-negative")

    action = binary_information_geometry(
        action_prior_early,
        action_false_early_cost,
        action_missed_early_cost,
    )
    comp = binary_information_geometry(
        compensation_prior_early,
        compensation_false_early_cost,
        compensation_missed_early_cost,
    )

    baseline_burden = direct + comp.prior_risk
    action_only = closed_form_information_threshold(
        action_prior_early,
        action_false_early_cost,
        action_missed_early_cost,
        delay_cost=baseline_burden,
    )

    # Perfect information gives maximum total value R_A0 + R_C0.
    # Waiting at q=1 is strictly worthwhile iff R_A0 > J.
    dual_ever = action.prior_risk > direct + tolerance
    dual_threshold = None

    if dual_ever:
        target = baseline_burden
        candidates: list[float] = []

        only_action = _candidate_root(
            target=target,
            active_action=True,
            active_compensation=False,
            action=action,
            compensation=comp,
        )
        if (
            only_action is not None
            and only_action + tolerance >= action.actionable_q
            and only_action <= comp.actionable_q + tolerance
        ):
            candidates.append(only_action)

        only_comp = _candidate_root(
            target=target,
            active_action=False,
            active_compensation=True,
            action=action,
            compensation=comp,
        )
        if (
            only_comp is not None
            and only_comp + tolerance >= comp.actionable_q
            and only_comp <= action.actionable_q + tolerance
        ):
            candidates.append(only_comp)

        both = _candidate_root(
            target=target,
            active_action=True,
            active_compensation=True,
            action=action,
            compensation=comp,
        )
        if (
            both is not None
            and both + tolerance
            >= max(action.actionable_q, comp.actionable_q)
        ):
            candidates.append(both)

        valid = [
            q for q in candidates
            if 0.5 - tolerance <= q < 1.0 - tolerance
        ]
        if not valid:
            # The ever-waits condition guarantees an interior crossing for the
            # continuous piecewise-linear value function. Fail closed if the
            # piecewise algebra and the boundary check ever disagree.
            raise AssertionError(
                "dual-use threshold crossing was expected but not located"
            )
        dual_threshold = max(0.5, min(valid))

    return DualUseThreshold(
        direct_wait_cost=direct,
        action_prior_risk=action.prior_risk,
        compensation_prior_risk=comp.prior_risk,
        action_actionable_q=action.actionable_q,
        compensation_actionable_q=comp.actionable_q,
        baseline_uninformed_waiting_burden=baseline_burden,
        action_only_wait_threshold=action_only.wait_cue_accuracy,
        action_only_ever_waits=action_only.ever_waits,
        dual_use_wait_threshold=dual_threshold,
        dual_use_ever_waits=dual_ever,
    )


def compensation_information_rescue_interval(
    *,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
    compensation_prior_early: float,
    compensation_false_early_cost: float,
    compensation_missed_early_cost: float,
) -> tuple[float, float] | None:
    """Direct-cost interval where dual-use information rescues waiting.

    "Rescue" means action information alone can never justify waiting once the
    uninformed compensation burden is included, but a perfect dual-use cue can.

    Action-only never waits when

        J + R_C0 >= R_A0.

    A perfect dual-use cue permits waiting when

        J < R_A0.

    Hence the exact rescue interval is

        J in [max(0, R_A0-R_C0), R_A0).
    """

    action_risk = prior_bayes_risk(
        action_prior_early,
        action_false_early_cost,
        action_missed_early_cost,
    )
    comp_risk = prior_bayes_risk(
        compensation_prior_early,
        compensation_false_early_cost,
        compensation_missed_early_cost,
    )
    lower = max(0.0, action_risk - comp_risk)
    upper = action_risk
    if upper <= lower + 1e-12:
        return None
    return lower, upper



@dataclass(frozen=True)
class BalancedDualUsePairWindow:
    direct_wait_cost: float
    actor_1_compensation_loss: float
    actor_2_compensation_loss: float
    actor_1_wait_threshold: float | None
    actor_2_wait_threshold: float | None
    lower_wait_threshold: float | None
    upper_wait_threshold: float | None
    finite_window_width: float | None
    regime: str


def balanced_dual_use_wait_threshold(
    *,
    direct_wait_cost: float,
    compensation_loss: float,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
) -> float | None:
    """Exact shared-q threshold with a balanced compensation problem.

    The compensation state has prior 1/2 and symmetric wrong-response cost G.
    Hence R_C0=G/2 and V_C(q)=G(q-1/2).

    When J < R_A0,

        q_wait(G) = [B_A + J + G] / [S_A + G].

    When J >= R_A0, even perfect dual-use information is not worth waiting for.
    """

    direct = _nonnegative("direct_wait_cost", direct_wait_cost)
    g = _nonnegative("compensation_loss", compensation_loss)
    action = binary_information_geometry(
        action_prior_early,
        action_false_early_cost,
        action_missed_early_cost,
    )
    if direct >= action.prior_risk - 1e-12:
        return None
    q = (
        action.other_prior_loss
        + direct
        + g
    ) / (
        action.total_prior_loss
        + g
    )
    if q < action.actionable_q - 1e-12 or q >= 1.0:
        raise AssertionError("balanced dual-use threshold outside valid region")
    return q


def balanced_dual_use_pair_window(
    *,
    direct_wait_cost: float,
    actor_1_compensation_loss: float,
    actor_2_compensation_loss: float,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
) -> BalancedDualUsePairWindow:
    """Exact asynchronous window created by compensation-problem heterogeneity.

    The two actors share the seasonal-action problem, direct waiting cost J,
    and cue accuracy q. They differ only in balanced compensation-loss scale G.

    If J < R_A0, both eventually wait and unequal G values create a finite
    threshold gap:

        |q2-q1|
        =
        |G2-G1| (R_A0-J)
        / [(S_A+G1)(S_A+G2)].

    Thus raw waiting time and direct waiting cost can be identical while
    asynchronous cue use arises purely from downstream compensation geometry.
    """

    direct = _nonnegative("direct_wait_cost", direct_wait_cost)
    g1 = _nonnegative(
        "actor_1_compensation_loss",
        actor_1_compensation_loss,
    )
    g2 = _nonnegative(
        "actor_2_compensation_loss",
        actor_2_compensation_loss,
    )
    action = binary_information_geometry(
        action_prior_early,
        action_false_early_cost,
        action_missed_early_cost,
    )

    q1 = balanced_dual_use_wait_threshold(
        direct_wait_cost=direct,
        compensation_loss=g1,
        action_prior_early=action_prior_early,
        action_false_early_cost=action_false_early_cost,
        action_missed_early_cost=action_missed_early_cost,
    )
    q2 = balanced_dual_use_wait_threshold(
        direct_wait_cost=direct,
        compensation_loss=g2,
        action_prior_early=action_prior_early,
        action_false_early_cost=action_false_early_cost,
        action_missed_early_cost=action_missed_early_cost,
    )

    if q1 is None or q2 is None:
        return BalancedDualUsePairWindow(
            direct_wait_cost=direct,
            actor_1_compensation_loss=g1,
            actor_2_compensation_loss=g2,
            actor_1_wait_threshold=q1,
            actor_2_wait_threshold=q2,
            lower_wait_threshold=None,
            upper_wait_threshold=None,
            finite_window_width=0.0,
            regime="NO_ONE_WAITS_DIRECT_COST_TOO_HIGH",
        )

    low = min(q1, q2)
    high = max(q1, q2)
    if abs(g1 - g2) <= 1e-15:
        width = 0.0
        regime = "NO_ASYNCHRONY_EQUAL_COMPENSATION_GEOMETRY"
    else:
        width = (
            abs(g2 - g1)
            * (action.prior_risk - direct)
            / (
                (action.total_prior_loss + g1)
                * (action.total_prior_loss + g2)
            )
        )
        if abs(width - (high - low)) > 1e-10:
            raise AssertionError("pairwise width identity failed")
        regime = "FINITE_DUAL_USE_ASYNCHRONY"

    return BalancedDualUsePairWindow(
        direct_wait_cost=direct,
        actor_1_compensation_loss=g1,
        actor_2_compensation_loss=g2,
        actor_1_wait_threshold=q1,
        actor_2_wait_threshold=q2,
        lower_wait_threshold=low,
        upper_wait_threshold=high,
        finite_window_width=width,
        regime=regime,
    )


def balanced_dual_use_threshold_slope_in_compensation_loss(
    *,
    direct_wait_cost: float,
    compensation_loss: float,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
) -> float | None:
    """dq_wait/dG for the balanced shared-q special case.

    For J < R_A0,

        dq/dG = (R_A0-J)/(S_A+G)^2 > 0.

    The positive sign is important: a larger compensation problem creates more
    potential compensation information value, but also more residual
    compensation loss at any imperfect shared cue accuracy.
    """

    direct = _nonnegative("direct_wait_cost", direct_wait_cost)
    g = _nonnegative("compensation_loss", compensation_loss)
    action = binary_information_geometry(
        action_prior_early,
        action_false_early_cost,
        action_missed_early_cost,
    )
    if direct >= action.prior_risk - 1e-12:
        return None
    return (
        action.prior_risk - direct
    ) / (
        action.total_prior_loss + g
    ) ** 2



@dataclass(frozen=True)
class GeneralBalancedDualUsePairWindow:
    actor_1_direct_wait_cost: float
    actor_2_direct_wait_cost: float
    actor_1_compensation_loss: float
    actor_2_compensation_loss: float
    actor_1_headroom: float | None
    actor_2_headroom: float | None
    actor_1_wait_threshold: float | None
    actor_2_wait_threshold: float | None
    regime: str
    lower_wait_threshold: float | None
    upper_wait_threshold: float | None
    finite_window_width: float | None


def balanced_dual_use_threshold_headroom(
    *,
    direct_wait_cost: float,
    compensation_loss: float,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
) -> float | None:
    """Return H=(R_A0-J)/(S_A+G), so q_wait=1-H.

    H is defined only when J<R_A0, i.e. when perfect dual-use information can
    make waiting worthwhile.
    """

    direct = _nonnegative("direct_wait_cost", direct_wait_cost)
    g = _nonnegative("compensation_loss", compensation_loss)
    action = binary_information_geometry(
        action_prior_early,
        action_false_early_cost,
        action_missed_early_cost,
    )
    if direct >= action.prior_risk - 1e-12:
        return None
    return (
        action.prior_risk - direct
    ) / (
        action.total_prior_loss + g
    )


def general_balanced_dual_use_pair_window(
    *,
    actor_1_direct_wait_cost: float,
    actor_1_compensation_loss: float,
    actor_2_direct_wait_cost: float,
    actor_2_compensation_loss: float,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
) -> GeneralBalancedDualUsePairWindow:
    """General pairwise window when actors differ in J and/or G.

    For every actor that can ever wait,

        q_i = 1 - H_i,
        H_i = (R_A0-J_i)/(S_A+G_i).

    If both thresholds are finite, the exact asynchronous-window width is

        |H_1-H_2|.

    Thus direct waiting cost and compensation-problem severity are
    substitutable in their effect on the reliability threshold: many (J,G)
    combinations lie on the same iso-threshold contour.
    """

    j1 = _nonnegative(
        "actor_1_direct_wait_cost",
        actor_1_direct_wait_cost,
    )
    j2 = _nonnegative(
        "actor_2_direct_wait_cost",
        actor_2_direct_wait_cost,
    )
    g1 = _nonnegative(
        "actor_1_compensation_loss",
        actor_1_compensation_loss,
    )
    g2 = _nonnegative(
        "actor_2_compensation_loss",
        actor_2_compensation_loss,
    )

    h1 = balanced_dual_use_threshold_headroom(
        direct_wait_cost=j1,
        compensation_loss=g1,
        action_prior_early=action_prior_early,
        action_false_early_cost=action_false_early_cost,
        action_missed_early_cost=action_missed_early_cost,
    )
    h2 = balanced_dual_use_threshold_headroom(
        direct_wait_cost=j2,
        compensation_loss=g2,
        action_prior_early=action_prior_early,
        action_false_early_cost=action_false_early_cost,
        action_missed_early_cost=action_missed_early_cost,
    )

    q1 = None if h1 is None else 1.0 - h1
    q2 = None if h2 is None else 1.0 - h2

    if q1 is None and q2 is None:
        regime = "NO_ONE_WAITS"
        low = None
        high = None
        width = 0.0
    elif q1 is None or q2 is None:
        regime = "PERSISTENT_DUAL_USE_ASYMMETRY"
        finite_q = q2 if q1 is None else q1
        assert finite_q is not None
        low = finite_q
        high = 1.0
        width = None
    else:
        low = min(q1, q2)
        high = max(q1, q2)
        width = abs(h1 - h2)
        if abs(width - (high - low)) > 1e-10:
            raise AssertionError("general dual-use width identity failed")
        regime = (
            "NO_ASYNCHRONY_EQUAL_HEADROOM"
            if width <= 1e-15
            else "FINITE_DUAL_USE_ASYNCHRONY"
        )

    return GeneralBalancedDualUsePairWindow(
        actor_1_direct_wait_cost=j1,
        actor_2_direct_wait_cost=j2,
        actor_1_compensation_loss=g1,
        actor_2_compensation_loss=g2,
        actor_1_headroom=h1,
        actor_2_headroom=h2,
        actor_1_wait_threshold=q1,
        actor_2_wait_threshold=q2,
        regime=regime,
        lower_wait_threshold=low,
        upper_wait_threshold=high,
        finite_window_width=width,
    )


def iso_threshold_direct_wait_cost(
    *,
    reference_direct_wait_cost: float,
    reference_compensation_loss: float,
    target_compensation_loss: float,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
) -> float:
    """J_target that exactly offsets a change in G at fixed q_wait.

    The iso-threshold condition is

        (R-J_ref)/(S+G_ref)
        =
        (R-J_target)/(S+G_target).
    """

    j_ref = _nonnegative(
        "reference_direct_wait_cost",
        reference_direct_wait_cost,
    )
    g_ref = _nonnegative(
        "reference_compensation_loss",
        reference_compensation_loss,
    )
    g_target = _nonnegative(
        "target_compensation_loss",
        target_compensation_loss,
    )
    action = binary_information_geometry(
        action_prior_early,
        action_false_early_cost,
        action_missed_early_cost,
    )
    if j_ref >= action.prior_risk:
        raise ValueError(
            "reference actor must have a finite dual-use threshold"
        )
    headroom = (
        action.prior_risk - j_ref
    ) / (
        action.total_prior_loss + g_ref
    )
    return action.prior_risk - headroom * (
        action.total_prior_loss + g_target
    )



@dataclass(frozen=True)
class MultiModuleDualUseThreshold:
    direct_wait_cost: float
    action_prior_risk: float
    conditional_prior_risk_total: float
    conditional_module_count: int
    wait_threshold: float | None
    ever_waits: bool
    max_actionability_q: float
    all_modules_active_at_threshold: bool
    high_q_headroom: float | None


def _conditional_geometries(conditional_modules):
    geometries = []
    for index, module in enumerate(conditional_modules):
        if len(module) != 3:
            raise ValueError(
                f"conditional module {index} must be (prior, false_cost, missed_cost)"
            )
        geometries.append(
            binary_information_geometry(
                module[0],
                module[1],
                module[2],
            )
        )
    return geometries


def multi_module_waiting_margin(
    cue_accuracy: float,
    *,
    direct_wait_cost: float,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
    conditional_modules,
) -> float:
    """Waiting margin with any number of cue-informed conditional decisions.

    Each conditional module exists only if the actor waits. Its prior Bayes
    risk is therefore part of the burden of waiting. The focal cue can reduce
    that burden through the module's information value.
    """

    q = float(cue_accuracy)
    if not isfinite(q) or not 0.5 <= q <= 1.0:
        raise ValueError("cue_accuracy must lie in [0.5, 1]")
    direct = _nonnegative("direct_wait_cost", direct_wait_cost)

    action_value = information_value(
        action_prior_early,
        q,
        action_false_early_cost,
        action_missed_early_cost,
    )
    conditional = _conditional_geometries(conditional_modules)

    value = action_value
    burden = direct
    for module in conditional:
        burden += module.prior_risk
        value += information_value(
            module.prior_early,
            q,
            module.false_early_cost,
            module.missed_early_cost,
        )
    return value - burden


def multi_module_dual_use_wait_threshold(
    *,
    direct_wait_cost: float,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
    conditional_modules,
    tolerance: float = 1e-12,
) -> MultiModuleDualUseThreshold:
    """Exact threshold for one action module plus many conditional modules.

    Waiting is optimal iff

        V_A(q) + sum_j V_j(q)
        >
        J + sum_j R_j0.

    Under symmetric binary cues every V_j is continuous piecewise linear.
    The threshold is found exactly by scanning the finite set of actionability
    breakpoints and solving the linear equality on each active-set interval.

    Perfect-information feasibility is universal:

        wait can occur for some q <= 1
        iff
        R_A0 > J.

    Conditional-module prior risks cancel at perfect information.
    """

    direct = _nonnegative("direct_wait_cost", direct_wait_cost)
    if not isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("tolerance must be finite and non-negative")

    action = binary_information_geometry(
        action_prior_early,
        action_false_early_cost,
        action_missed_early_cost,
    )
    conditional = _conditional_geometries(conditional_modules)

    cond_prior = sum(module.prior_risk for module in conditional)
    ever = action.prior_risk > direct + tolerance
    max_q0 = max(
        [action.actionable_q]
        + [module.actionable_q for module in conditional]
    )

    if not ever:
        return MultiModuleDualUseThreshold(
            direct_wait_cost=direct,
            action_prior_risk=action.prior_risk,
            conditional_prior_risk_total=cond_prior,
            conditional_module_count=len(conditional),
            wait_threshold=None,
            ever_waits=False,
            max_actionability_q=max_q0,
            all_modules_active_at_threshold=False,
            high_q_headroom=None,
        )

    modules = [action, *conditional]
    target = direct + cond_prior

    # No positive waiting margin is possible before the action module becomes
    # informative. Start the exact active-set scan at q0,A.
    breaks = sorted(
        set(
            [action.actionable_q, 1.0]
            + [
                module.actionable_q
                for module in conditional
                if module.actionable_q >= action.actionable_q - tolerance
            ]
        )
    )

    threshold = None
    for left, right in zip(breaks[:-1], breaks[1:]):
        active = [
            module
            for module in modules
            if module.actionable_q <= left + tolerance
        ]
        slope = sum(module.total_prior_loss for module in active)
        if slope <= 0.0:
            continue
        intercept = sum(module.other_prior_loss for module in active)
        root = (target + intercept) / slope
        if (
            root >= left - tolerance
            and root <= right + tolerance
            and root < 1.0 - tolerance
        ):
            threshold = max(action.actionable_q, root)
            break

    if threshold is None:
        # The strict perfect-information condition guarantees an interior
        # crossing. Fail closed if the algebra and active-set scan disagree.
        raise AssertionError(
            "multi-module dual-use threshold crossing was expected but not located"
        )

    all_active = threshold >= max_q0 - tolerance
    headroom = None
    if all_active:
        total_slope = sum(module.total_prior_loss for module in modules)
        headroom = (
            action.prior_risk - direct
        ) / total_slope
        if abs(threshold - (1.0 - headroom)) > 1e-9:
            raise AssertionError("high-q headroom identity failed")

    margin = multi_module_waiting_margin(
        threshold,
        direct_wait_cost=direct,
        action_prior_early=action_prior_early,
        action_false_early_cost=action_false_early_cost,
        action_missed_early_cost=action_missed_early_cost,
        conditional_modules=conditional_modules,
    )
    if abs(margin) > 1e-8:
        raise AssertionError("multi-module threshold does not solve zero margin")

    return MultiModuleDualUseThreshold(
        direct_wait_cost=direct,
        action_prior_risk=action.prior_risk,
        conditional_prior_risk_total=cond_prior,
        conditional_module_count=len(conditional),
        wait_threshold=threshold,
        ever_waits=True,
        max_actionability_q=max_q0,
        all_modules_active_at_threshold=all_active,
        high_q_headroom=headroom,
    )


def multi_module_rescue_interval(
    *,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
    conditional_modules,
) -> tuple[float, float] | None:
    """Direct-cost interval where informing all conditional modules rescues wait.

    If the conditional modules remain uninformed, action information alone can
    never justify waiting when

        J + sum R_j0 >= R_A0.

    Perfect information across all modules permits waiting when

        J < R_A0.

    Therefore the exact rescue interval is

        J in [max(0, R_A0-sum R_j0), R_A0).
    """

    action = binary_information_geometry(
        action_prior_early,
        action_false_early_cost,
        action_missed_early_cost,
    )
    conditional = _conditional_geometries(conditional_modules)
    burden = sum(module.prior_risk for module in conditional)
    lower = max(0.0, action.prior_risk - burden)
    upper = action.prior_risk
    if upper <= lower + 1e-12:
        return None
    return lower, upper



@dataclass(frozen=True)
class IdenticalModuleComplexityScaling:
    direct_wait_cost: float
    conditional_module_count: int
    conditional_loss: float
    action_prior_risk: float
    action_total_loss: float
    wait_threshold: float | None
    headroom: float | None
    first_derivative_continuous_n: float | None
    second_derivative_continuous_n: float | None


def identical_balanced_module_complexity_scaling(
    *,
    direct_wait_cost: float,
    conditional_module_count: int,
    conditional_loss: float,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
) -> IdenticalModuleComplexityScaling:
    """Exact q_wait scaling for n identical balanced conditional modules.

    Each conditional module has prior 1/2 and symmetric wrong-response cost G.
    For J < R_A0,

        q_wait(n) = 1 - (R_A0-J)/(S_A+nG).

    Treating n as continuous for comparative statics,

        dq/dn   = (R_A0-J)G/(S_A+nG)^2 > 0
        d2q/dn2 = -2(R_A0-J)G^2/(S_A+nG)^3 <= 0.

    Thus decision complexity raises the reliability threshold toward one, but
    the marginal penalty of each additional identical module diminishes.
    """

    direct = _nonnegative("direct_wait_cost", direct_wait_cost)
    g = _nonnegative("conditional_loss", conditional_loss)
    if (
        isinstance(conditional_module_count, bool)
        or int(conditional_module_count) != conditional_module_count
        or conditional_module_count < 0
    ):
        raise ValueError(
            "conditional_module_count must be a non-negative integer"
        )
    n = int(conditional_module_count)

    action = binary_information_geometry(
        action_prior_early,
        action_false_early_cost,
        action_missed_early_cost,
    )

    if direct >= action.prior_risk - 1e-12:
        return IdenticalModuleComplexityScaling(
            direct_wait_cost=direct,
            conditional_module_count=n,
            conditional_loss=g,
            action_prior_risk=action.prior_risk,
            action_total_loss=action.total_prior_loss,
            wait_threshold=None,
            headroom=None,
            first_derivative_continuous_n=None,
            second_derivative_continuous_n=None,
        )

    denominator = action.total_prior_loss + n * g
    headroom = (action.prior_risk - direct) / denominator
    threshold = 1.0 - headroom

    first = (
        (action.prior_risk - direct) * g / denominator**2
    )
    second = (
        -2.0
        * (action.prior_risk - direct)
        * g**2
        / denominator**3
    )

    return IdenticalModuleComplexityScaling(
        direct_wait_cost=direct,
        conditional_module_count=n,
        conditional_loss=g,
        action_prior_risk=action.prior_risk,
        action_total_loss=action.total_prior_loss,
        wait_threshold=threshold,
        headroom=headroom,
        first_derivative_continuous_n=first,
        second_derivative_continuous_n=second,
    )


def identical_balanced_module_count_window(
    *,
    direct_wait_cost: float,
    actor_1_module_count: int,
    actor_2_module_count: int,
    conditional_loss: float,
    action_prior_early: float,
    action_false_early_cost: float,
    action_missed_early_cost: float,
) -> float | None:
    """Exact pairwise q-window generated only by module-count heterogeneity.

    For finite thresholds and common J,G,

        |q2-q1|
        =
        (R_A0-J) G |n2-n1|
        / [(S_A+n1G)(S_A+n2G)].

    Returns None when J >= R_A0 and neither actor can ever wait.
    """

    one = identical_balanced_module_complexity_scaling(
        direct_wait_cost=direct_wait_cost,
        conditional_module_count=actor_1_module_count,
        conditional_loss=conditional_loss,
        action_prior_early=action_prior_early,
        action_false_early_cost=action_false_early_cost,
        action_missed_early_cost=action_missed_early_cost,
    )
    two = identical_balanced_module_complexity_scaling(
        direct_wait_cost=direct_wait_cost,
        conditional_module_count=actor_2_module_count,
        conditional_loss=conditional_loss,
        action_prior_early=action_prior_early,
        action_false_early_cost=action_false_early_cost,
        action_missed_early_cost=action_missed_early_cost,
    )

    if one.wait_threshold is None or two.wait_threshold is None:
        return None

    n1 = one.conditional_module_count
    n2 = two.conditional_module_count
    g = one.conditional_loss
    r_minus_j = one.action_prior_risk - one.direct_wait_cost
    s = one.action_total_loss

    width = (
        r_minus_j
        * g
        * abs(n2 - n1)
        / ((s + n1 * g) * (s + n2 * g))
    )
    if abs(
        width - abs(two.wait_threshold - one.wait_threshold)
    ) > 1e-10:
        raise AssertionError(
            "module-count asynchronous-window identity failed"
        )
    return width
