"""Empirical bridge for the PAYOFF-B information-deadline theorem.

This module does not re-derive the theorem.  It turns its deterministic
predictions into fail-closed checks for future observations.

A direct empirical test requires independently measured:
    - cue reliability q,
    - delay/opportunity cost D,
    - state-mismatch losses C_F and C_M plus prior pi,
    - whether the actor actually waits for/uses the later cue.

Migration distance, route distance, phenological sensitivity, phase correction,
and predictive connectivity alone are not substitutes for D or cue-use status.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable

from src.endogenous_information_timing import (
    closed_form_information_threshold,
    desynchronization_window,
)


@dataclass(frozen=True)
class EmpiricalThresholdPrediction:
    prior_early: float
    false_early_cost: float
    missed_early_cost: float
    delay_cost: float
    wait_threshold: float | None
    ever_waits: bool


@dataclass(frozen=True)
class InferredThresholdInterval:
    """Deterministic threshold interval implied by observed cue-use decisions.

    With the PAYOFF-B tie rule, an actor waits iff q > q_wait.  Therefore a
    non-use observation at q implies q_wait >= q, while a use observation at q
    implies q_wait < q.
    """

    lower_inclusive: float | None
    upper_exclusive: float | None
    monotone: bool
    observations: int


def _validate_q(value: float) -> float:
    q = float(value)
    if not isfinite(q) or not 0.5 <= q <= 1.0:
        raise ValueError("cue accuracy must lie in [0.5, 1]")
    return q


def threshold_prediction(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    delay_cost: float,
) -> EmpiricalThresholdPrediction:
    """Return the theorem-predicted information-use threshold."""

    result = closed_form_information_threshold(
        prior_early,
        false_early_cost,
        missed_early_cost,
        delay_cost=delay_cost,
    )
    return EmpiricalThresholdPrediction(
        prior_early=float(prior_early),
        false_early_cost=float(false_early_cost),
        missed_early_cost=float(missed_early_cost),
        delay_cost=float(delay_cost),
        wait_threshold=result.wait_cue_accuracy,
        ever_waits=result.ever_waits,
    )


def predicted_information_use(
    cue_accuracy: float,
    prediction: EmpiricalThresholdPrediction,
) -> bool:
    """Whether the actor should use the later cue under the exact model."""

    q = _validate_q(cue_accuracy)
    if prediction.wait_threshold is None:
        return False
    return q > prediction.wait_threshold


def infer_deterministic_threshold_interval(
    observations: Iterable[tuple[float, bool]],
) -> InferredThresholdInterval:
    """Infer the threshold interval from deterministic use/non-use observations.

    Repeated observations at the same q must agree.  Any use at a lower q
    followed by non-use at a higher q violates the deterministic threshold
    model and returns monotone=False rather than silently fitting a threshold.
    """

    rows = [(_validate_q(q), bool(used)) for q, used in observations]
    if not rows:
        raise ValueError("at least one observation is required")

    by_q: dict[float, set[bool]] = {}
    for q, used in rows:
        by_q.setdefault(q, set()).add(used)
    if any(len(values) > 1 for values in by_q.values()):
        return InferredThresholdInterval(
            lower_inclusive=None,
            upper_exclusive=None,
            monotone=False,
            observations=len(rows),
        )

    ordered = sorted((q, next(iter(values))) for q, values in by_q.items())
    seen_use = False
    for _, used in ordered:
        if used:
            seen_use = True
        elif seen_use:
            return InferredThresholdInterval(
                lower_inclusive=None,
                upper_exclusive=None,
                monotone=False,
                observations=len(rows),
            )

    non_use = [q for q, used in rows if not used]
    use = [q for q, used in rows if used]
    return InferredThresholdInterval(
        lower_inclusive=max(non_use) if non_use else None,
        upper_exclusive=min(use) if use else None,
        monotone=True,
        observations=len(rows),
    )


def interval_contains_prediction(
    interval: InferredThresholdInterval,
    predicted_threshold: float | None,
) -> bool:
    """Whether an exact predicted threshold is compatible with observations."""

    if not interval.monotone:
        return False
    if predicted_threshold is None:
        # Never-wait prediction is compatible only if no use was observed.
        return interval.upper_exclusive is None

    q = _validate_q(predicted_threshold)
    if interval.lower_inclusive is not None and q < interval.lower_inclusive:
        return False
    if interval.upper_exclusive is not None and q >= interval.upper_exclusive:
        return False
    return True


def predicted_pair_asynchrony(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    actor_a_delay_cost: float,
    actor_b_delay_cost: float,
    cue_accuracy: float,
) -> bool:
    """Whether the exact two-actor theorem predicts asynchronous cue use."""

    q = _validate_q(cue_accuracy)
    window = desynchronization_window(
        prior_early,
        false_early_cost,
        missed_early_cost,
        actor_a_delay_cost=actor_a_delay_cost,
        actor_b_delay_cost=actor_b_delay_cost,
    )

    if window.regime == "FINITE_DESYNCHRONIZATION_WINDOW":
        assert window.lower_bound_open is not None
        assert window.upper_bound_closed is not None
        return window.lower_bound_open < q <= window.upper_bound_closed

    if window.regime == "PERSISTENT_ASYMMETRIC_UPTAKE":
        assert window.lower_bound_open is not None
        return q > window.lower_bound_open

    return False


@dataclass(frozen=True)
class RevealedDelayCostInterval:
    """Delay-cost interval implied by a threshold bracket under the exact model."""

    lower_inclusive: float | None
    upper_exclusive: float | None
    compatible_with_nonnegative_cost: bool


def revealed_delay_cost(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    wait_threshold: float,
) -> float:
    """Invert the exact information-deadline theorem to recover D.

    For an interior threshold q_wait,

        D = q_wait (A + L) - max(A, L).

    This is a revealed-model quantity.  It becomes an independent empirical
    test only when compared with a separately estimated opportunity cost.
    """

    q = _validate_q(wait_threshold)
    pi = float(prior_early)
    cf = float(false_early_cost)
    cm = float(missed_early_cost)
    if not isfinite(pi) or not 0.0 < pi < 1.0:
        raise ValueError("prior_early must lie strictly between 0 and 1")
    if not all(isfinite(x) and x >= 0.0 for x in (cf, cm)):
        raise ValueError("state-mismatch costs must be non-negative")
    a = (1.0 - pi) * cf
    l = pi * cm
    total = a + l
    if total <= 0.0:
        raise ValueError("prior expected-loss scale must be positive")
    actionable = max(a, l) / total
    if q < actionable - 1e-12:
        raise ValueError("wait threshold cannot lie below actionable cue threshold")
    d = q * total - max(a, l)
    if d < -1e-12:
        raise AssertionError("revealed delay cost cannot be negative")
    return max(0.0, d)


def revealed_delay_cost_interval(
    prior_early: float,
    false_early_cost: float,
    missed_early_cost: float,
    threshold_interval: InferredThresholdInterval,
) -> RevealedDelayCostInterval:
    """Map an observed threshold bracket into a revealed-D bracket.

    The transformation is monotone.  Bounds are clipped at D=0 because the
    declared model excludes negative waiting costs.  A non-monotone threshold
    observation is incompatible and fails closed.
    """

    if not threshold_interval.monotone:
        return RevealedDelayCostInterval(
            lower_inclusive=None,
            upper_exclusive=None,
            compatible_with_nonnegative_cost=False,
        )

    pi = float(prior_early)
    cf = float(false_early_cost)
    cm = float(missed_early_cost)
    if not isfinite(pi) or not 0.0 < pi < 1.0:
        raise ValueError("prior_early must lie strictly between 0 and 1")
    if not all(isfinite(x) and x >= 0.0 for x in (cf, cm)):
        raise ValueError("state-mismatch costs must be non-negative")
    a = (1.0 - pi) * cf
    l = pi * cm
    total = a + l
    if total <= 0.0:
        raise ValueError("prior expected-loss scale must be positive")
    other = max(a, l)
    q0 = other / total

    lower_q = threshold_interval.lower_inclusive
    upper_q = threshold_interval.upper_exclusive
    if upper_q is not None and upper_q <= q0:
        return RevealedDelayCostInterval(
            lower_inclusive=None,
            upper_exclusive=None,
            compatible_with_nonnegative_cost=False,
        )

    effective_lower_q = q0 if lower_q is None else max(q0, lower_q)
    lower_d = max(0.0, effective_lower_q * total - other)
    upper_d = (
        None
        if upper_q is None
        else max(0.0, upper_q * total - other)
    )
    return RevealedDelayCostInterval(
        lower_inclusive=lower_d,
        upper_exclusive=upper_d,
        compatible_with_nonnegative_cost=True,
    )
