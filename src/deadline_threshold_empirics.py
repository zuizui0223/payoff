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
