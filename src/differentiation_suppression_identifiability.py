"""Identify whether a putative matched-S perturbation suppresses differentiation generation.

Observed specialist frequency is not itself a generation-rate estimand.  In the
simplest one-generation bookkeeping model,

    F = mu * r / ((1-mu) + mu*r)

where `mu` is the probability/fraction entering the specialist state and `r` is
specialist survival or realized output relative to the generalist state.  A
lower observed F can therefore result from a lower generation rate, poorer
post-generation survival, or both.

This module belongs to PAYOFF Lane A only.  It never promotes a generic game
claim, a frequency parameter, or an architecture-specific E1 claim.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


def _q(value: object) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    raise ValueError("use an exact rational-compatible value")


def observed_specialist_fraction(
    generation_fraction: object,
    relative_specialist_realization: object,
) -> Fraction:
    """Return F = mu*r / ((1-mu)+mu*r) exactly."""
    mu = _q(generation_fraction)
    r = _q(relative_specialist_realization)
    if not (0 <= mu <= 1):
        raise ValueError("generation_fraction must lie in [0,1]")
    if r < 0:
        raise ValueError("relative_specialist_realization must be nonnegative")
    denominator = (1 - mu) + mu * r
    if denominator == 0:
        raise ValueError("undefined all-zero realized output")
    return mu * r / denominator


def realization_ratio_for_same_observed_fraction(
    observed_fraction: object,
    generation_fraction: object,
) -> Fraction:
    """Construct r giving a chosen observed F for any strict interior mu.

    Solving F = mu*r / ((1-mu)+mu*r) gives

        r = F(1-mu) / (mu(1-F)).

    Hence F alone does not identify mu.
    """
    f = _q(observed_fraction)
    mu = _q(generation_fraction)
    if not (0 < f < 1):
        raise ValueError("observed_fraction must lie strictly in (0,1)")
    if not (0 < mu < 1):
        raise ValueError("generation_fraction must lie strictly in (0,1)")
    return f * (1 - mu) / (mu * (1 - f))


@dataclass(frozen=True)
class DifferentiationSuppressionReceipt:
    system_id: str
    perturbation_id: str
    support_reference: str
    observed_specialist_frequency_reduced_declared: bool
    direct_generation_rate_measured_declared: bool
    generation_rate_reduced_declared: bool
    post_generation_survival_or_realization_matched_declared: bool
    generalist_growth_matched_declared: bool
    generalist_sporulation_matched_declared: bool
    net_task_preserved_declared: bool
    ecological_context_matched_declared: bool
    background_matched_declared: bool
    focal_differentiation_mechanism_isolated_declared: bool
    stable_or_heritable_unit_declared: bool
    independent_of_game_result_declared: bool
    independent_of_raw_availability_declared: bool

    @property
    def generation_suppression_identified(self) -> bool:
        return all(
            (
                self.observed_specialist_frequency_reduced_declared,
                self.direct_generation_rate_measured_declared,
                self.generation_rate_reduced_declared,
                self.post_generation_survival_or_realization_matched_declared,
            )
        )

    @property
    def matched_s_candidate_certified(self) -> bool:
        return all(
            (
                self.generation_suppression_identified,
                self.generalist_growth_matched_declared,
                self.generalist_sporulation_matched_declared,
                self.net_task_preserved_declared,
                self.ecological_context_matched_declared,
                self.background_matched_declared,
                self.focal_differentiation_mechanism_isolated_declared,
                self.stable_or_heritable_unit_declared,
                self.independent_of_game_result_declared,
                self.independent_of_raw_availability_declared,
            )
        )


@dataclass(frozen=True)
class DifferentiationSuppressionAdjudication:
    generation_suppression_identified: bool
    matched_s_candidate_certified: bool
    blockers: tuple[str, ...]
    generic_game_promoted: bool = False
    architecture_frequency_claim_promoted: bool = False
    scope: str = "PAYOFF_differentiation_generation_vs_survival_gate_v1"


def _nonempty(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def adjudicate_differentiation_suppression(
    receipt: DifferentiationSuppressionReceipt,
) -> DifferentiationSuppressionAdjudication:
    _nonempty(receipt.system_id, "system_id")
    _nonempty(receipt.perturbation_id, "perturbation_id")
    _nonempty(receipt.support_reference, "support_reference")
    if not receipt.independent_of_game_result_declared:
        raise ValueError("Lane A suppression mapping must be independent of game outcome")
    if not receipt.independent_of_raw_availability_declared:
        raise ValueError("Lane A suppression mapping must not depend on raw availability")

    checks = (
        (receipt.observed_specialist_frequency_reduced_declared, "SPECIALIST_FREQUENCY_REDUCTION_NOT_SHOWN"),
        (receipt.direct_generation_rate_measured_declared, "DIRECT_DIFFERENTIATION_GENERATION_RATE_NOT_MEASURED"),
        (receipt.generation_rate_reduced_declared, "DIFFERENTIATION_GENERATION_REDUCTION_NOT_SHOWN"),
        (receipt.post_generation_survival_or_realization_matched_declared, "POST_GENERATION_SURVIVAL_OR_REALIZATION_NOT_MATCHED"),
        (receipt.generalist_growth_matched_declared, "GENERALIST_GROWTH_NOT_MATCHED"),
        (receipt.generalist_sporulation_matched_declared, "GENERALIST_SPORULATION_NOT_MATCHED"),
        (receipt.net_task_preserved_declared, "NET_TASK_NOT_PRESERVED"),
        (receipt.ecological_context_matched_declared, "ECOLOGICAL_CONTEXT_NOT_MATCHED"),
        (receipt.background_matched_declared, "BACKGROUND_NOT_MATCHED"),
        (receipt.focal_differentiation_mechanism_isolated_declared, "FOCAL_DIFFERENTIATION_MECHANISM_NOT_ISOLATED"),
        (receipt.stable_or_heritable_unit_declared, "STABLE_OR_HERITABLE_S_UNIT_NOT_ESTABLISHED"),
    )
    blockers = tuple(label for passed, label in checks if not passed)
    return DifferentiationSuppressionAdjudication(
        generation_suppression_identified=receipt.generation_suppression_identified,
        matched_s_candidate_certified=receipt.matched_s_candidate_certified,
        blockers=blockers,
    )
