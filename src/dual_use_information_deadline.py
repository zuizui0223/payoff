"""Dual-use information value for PAYOFF-B.

A later information package can be useful twice:

1. it can improve the focal seasonal action;
2. after waiting has created a downstream compensation problem, it can improve
   the choice of compensation.

This module treats the compensation state as a balanced binary state with a
wrong-compensation loss G and a cue accuracy r in [0.5, 1].  The residual
compensation risk after observing that cue is (1-r)G.

The direct nonrecoverable waiting cost J remains separate.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from src.endogenous_information_timing import (
    closed_form_information_threshold,
    information_value,
)


@dataclass(frozen=True)
class DualUseInformationDecision:
    action_cue_accuracy: float
    compensation_cue_accuracy: float
    action_information_value: float
    compensation_information_value: float
    direct_wait_cost: float
    residual_compensation_risk: float
    total_value_relative_to_uninformed_compensation: float
    waits: bool


@dataclass(frozen=True)
class DualUseSharedThreshold:
    threshold_accuracy: float | None
    ever_waits: bool
    action_only_threshold_without_compensation_information: float | None
    actionability_threshold: float


def _unit_interval_accuracy(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x) or not 0.5 <= x <= 1.0:
        raise ValueError(f"{name} must lie in [0.5, 1]")
    return x


def _nonnegative(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x) or x < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return x


def compensation_information_value(
    compensation_cue_accuracy: float,
    wrong_compensation_cost: float,
) -> float:
    """Value of a balanced binary compensation cue.

    Before the cue, the best compensation guess has risk G/2.
    After a symmetric cue of accuracy r, residual risk is (1-r)G.
    Hence value = (r-1/2)G.
    """

    r = _unit_interval_accuracy(
        "compensation_cue_accuracy",
        compensation_cue_accuracy,
    )
    g = _nonnegative(
        "wrong_compensation_cost",
        wrong_compensation_cost,
    )
    return (r - 0.5) * g


def residual_compensation_risk(
    compensation_cue_accuracy: float,
    wrong_compensation_cost: float,
) -> float:
    r = _unit_interval_accuracy(
        "compensation_cue_accuracy",
        compensation_cue_accuracy,
    )
    g = _nonnegative(
        "wrong_compensation_cost",
        wrong_compensation_cost,
    )
    return (1.0 - r) * g


def dual_use_information_decision(
    prior_early: float,
    action_cue_accuracy: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    direct_wait_cost: float,
    compensation_cue_accuracy: float,
    wrong_compensation_cost: float,
) -> DualUseInformationDecision:
    """Evaluate waiting when information also improves compensation choice."""

    q = _unit_interval_accuracy(
        "action_cue_accuracy",
        action_cue_accuracy,
    )
    r = _unit_interval_accuracy(
        "compensation_cue_accuracy",
        compensation_cue_accuracy,
    )
    j = _nonnegative("direct_wait_cost", direct_wait_cost)
    g = _nonnegative(
        "wrong_compensation_cost",
        wrong_compensation_cost,
    )

    action_value = information_value(
        prior_early,
        q,
        false_early_cost,
        missed_early_cost,
    )
    comp_value = compensation_information_value(r, g)
    residual = residual_compensation_risk(r, g)

    # Immediate commitment has no downstream compensation problem.
    # Waiting is beneficial only if action information exceeds the direct
    # waiting cost plus the residual compensation risk after its cue.
    waits = action_value > j + residual + 1e-12

    return DualUseInformationDecision(
        action_cue_accuracy=q,
        compensation_cue_accuracy=r,
        action_information_value=action_value,
        compensation_information_value=comp_value,
        direct_wait_cost=j,
        residual_compensation_risk=residual,
        total_value_relative_to_uninformed_compensation=(
            action_value + comp_value
        ),
        waits=waits,
    )


def action_threshold_given_compensation_accuracy(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    direct_wait_cost: float,
    compensation_cue_accuracy: float,
    wrong_compensation_cost: float,
) -> float | None:
    """Exact q threshold when compensation cue accuracy r is fixed."""

    r = _unit_interval_accuracy(
        "compensation_cue_accuracy",
        compensation_cue_accuracy,
    )
    j = _nonnegative("direct_wait_cost", direct_wait_cost)
    g = _nonnegative(
        "wrong_compensation_cost",
        wrong_compensation_cost,
    )
    effective = j + (1.0 - r) * g

    base = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=effective,
    )
    return base.wait_cue_accuracy


def shared_dual_accuracy_threshold(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    *,
    direct_wait_cost: float,
    wrong_compensation_cost: float,
) -> DualUseSharedThreshold:
    """Exact threshold when one accuracy x applies to both information uses.

    Compensation state is balanced binary.  In the active region:

        V_action(x) > J + (1-x)G

    which gives

        x > [max(A,L) + J + G] / [A+L+G].

    Waiting at x=1 is possible iff J < R0.  The compensation-only uncertainty
    can therefore make action-only waiting impossible while dual-use
    information restores a finite threshold.
    """

    pi = float(prior_early)
    cf = _nonnegative("false_early_cost", false_early_cost)
    cm = _nonnegative("missed_early_cost", missed_early_cost)
    j = _nonnegative("direct_wait_cost", direct_wait_cost)
    g = _nonnegative(
        "wrong_compensation_cost",
        wrong_compensation_cost,
    )
    if not isfinite(pi) or not 0.0 < pi < 1.0:
        raise ValueError("prior_early must lie strictly between 0 and 1")

    a = (1.0 - pi) * cf
    l = pi * cm
    s = a + l
    if s <= 0.0:
        raise ValueError("state-loss scale must be positive")

    r0 = min(a, l)
    q0 = max(a, l) / s

    # If compensation information were absent (r=0.5), its prior residual
    # risk G/2 behaves like an extra fixed waiting cost.
    no_comp_info = closed_form_information_threshold(
        pi,
        cf,
        cm,
        delay_cost=j + 0.5 * g,
    ).wait_cue_accuracy

    if j >= r0:
        return DualUseSharedThreshold(
            threshold_accuracy=None,
            ever_waits=False,
            action_only_threshold_without_compensation_information=(
                no_comp_info
            ),
            actionability_threshold=q0,
        )

    threshold = (max(a, l) + j + g) / (s + g)
    return DualUseSharedThreshold(
        threshold_accuracy=threshold,
        ever_waits=True,
        action_only_threshold_without_compensation_information=no_comp_info,
        actionability_threshold=q0,
    )
