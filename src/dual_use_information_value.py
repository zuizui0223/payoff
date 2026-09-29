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
