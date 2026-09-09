"""Guard against inventing a scalar PAYOFF gap from multimetric performance data.

Lane G only. Metrics must already be oriented so `positive` means the candidate
strategy performs better than the comparator on that metric and `negative`
means worse. Architecture semantics are outside this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

_ALLOWED = frozenset({"positive", "negative", "zero", "unresolved"})


@dataclass(frozen=True)
class MultimetricScalarizationReceipt:
    support_reference: str
    metric_states: tuple[tuple[str, str], ...]
    orientation_frozen_declared: bool
    weight_invariant_scalar_sign: str | None
    pareto_relation: str
    scalarization_required: bool
    unresolved_metrics_present: bool
    generic_frequency_game_identified: bool = False
    architecture_mapping_identified: bool = False
    architecture_specific_claim_licensed: bool = False
    scope: str = "generic_multimetric_performance_scalarization_guard"


def adjudicate_multimetric_sign(
    metric_states: Mapping[str, str],
    *,
    support_reference: str,
    orientation_frozen_declared: bool,
) -> MultimetricScalarizationReceipt:
    """Adjudicate whether a scalar sign is invariant to all positive weights.

    Each metric is direction-normalized before entry. With all aggregation
    weights strictly positive, a positive sign is weight-invariant only when no
    metric is negative or unresolved and at least one is positive; the mirrored
    rule gives a negative sign. Mixed positive/negative evidence proves that an
    aggregate sign depends on scalarization choices. This function does not
    choose those weights and does not identify a frequency game.
    """
    if not isinstance(support_reference, str) or not support_reference.strip():
        raise ValueError("declare support provenance")
    if orientation_frozen_declared is not True:
        raise ValueError("freeze metric orientations before adjudication")
    if not metric_states:
        raise ValueError("at least one metric is required")

    normalized: list[tuple[str, str]] = []
    for metric, state in metric_states.items():
        if not isinstance(metric, str) or not metric.strip():
            raise ValueError("metric names must be non-empty strings")
        if not isinstance(state, str) or state.strip().lower() not in _ALLOWED:
            raise ValueError(
                "metric state must be positive, negative, zero, or unresolved"
            )
        normalized.append((metric.strip(), state.strip().lower()))

    normalized.sort()
    states = {state for _, state in normalized}
    has_pos = "positive" in states
    has_neg = "negative" in states
    has_unresolved = "unresolved" in states

    sign: str | None = None
    scalarization_required = False

    if has_pos and has_neg:
        pareto = "tradeoff_non_dominance"
        scalarization_required = True
    elif has_unresolved:
        pareto = "unresolved"
        scalarization_required = True
    elif has_pos:
        pareto = "candidate_weakly_pareto_dominates"
        sign = "positive"
    elif has_neg:
        pareto = "comparator_weakly_pareto_dominates"
        sign = "negative"
    else:
        pareto = "all_registered_metrics_tied"
        sign = "zero"

    return MultimetricScalarizationReceipt(
        support_reference=support_reference.strip(),
        metric_states=tuple(normalized),
        orientation_frozen_declared=True,
        weight_invariant_scalar_sign=sign,
        pareto_relation=pareto,
        scalarization_required=scalarization_required,
        unresolved_metrics_present=has_unresolved,
    )
