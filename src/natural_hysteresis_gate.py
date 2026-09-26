"""Evidence gate for natural information-triggered timing hysteresis.

PAYOFF-B already has synthetic hysteresis.  This module prevents shorter or
incomplete natural datasets from being relabelled as direct hysteresis evidence.

A direct natural test requires three temporally ordered information regimes:
baseline, disruption and recovery.  With a declared predictive-connectivity
training window W, the default independence-oriented eligibility rule requires
at least three non-overlapping W-year blocks.  This is a data-readiness rule,
not a claim that hysteresis must operate on W-year timescales.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class NaturalHysteresisDataset:
    name: str
    years: int
    has_precommitment_cue: bool
    has_future_destination_state: bool
    has_focal_timing: bool
    has_partner_timing: bool
    has_interaction_outcome: bool
    experimental_information_timing: bool = False
    notes: str = ""


@dataclass(frozen=True)
class NaturalHysteresisGate:
    dataset: NaturalHysteresisDataset
    predictive_window_years: int
    minimum_years_for_three_regimes: int
    duration_passed: bool
    information_pair_passed: bool
    timing_pair_passed: bool
    direct_hysteresis_ready: bool
    evidence_level: str
    missing_requirements: tuple[str, ...]


def evaluate_natural_hysteresis_gate(
    dataset: NaturalHysteresisDataset,
    *,
    predictive_window_years: int = 8,
) -> NaturalHysteresisGate:
    if predictive_window_years < 4:
        raise ValueError("predictive_window_years must be at least 4")
    if dataset.years <= 0:
        raise ValueError("dataset years must be positive")

    minimum_years = 3 * predictive_window_years
    duration_passed = dataset.years >= minimum_years
    information_pair_passed = (
        dataset.has_precommitment_cue
        and dataset.has_future_destination_state
    )
    timing_pair_passed = (
        dataset.has_focal_timing
        and dataset.has_partner_timing
    )

    missing: list[str] = []
    if not duration_passed:
        missing.append(
            f"need >= {minimum_years} years for three non-overlapping "
            f"{predictive_window_years}-year information regimes"
        )
    if not dataset.has_precommitment_cue:
        missing.append("pre-commitment cue series")
    if not dataset.has_future_destination_state:
        missing.append("future destination-state series")
    if not dataset.has_focal_timing:
        missing.append("focal timing series")
    if not dataset.has_partner_timing:
        missing.append("partner timing series")

    direct_ready = (
        duration_passed
        and information_pair_passed
        and timing_pair_passed
    )

    if direct_ready:
        evidence_level = "DIRECT_HYSTERESIS_READY"
    elif dataset.experimental_information_timing:
        evidence_level = "DECISION_TIME_INFORMATION_ANCHOR"
    elif information_pair_passed and dataset.has_focal_timing:
        evidence_level = "PREDICTIVE_INFORMATION_TEST"
    elif timing_pair_passed and dataset.has_interaction_outcome:
        evidence_level = "INTERACTION_TIMING_TEST"
    elif timing_pair_passed:
        evidence_level = "LONG_TERM_PHENOLOGY_CONTRAST"
    elif dataset.has_interaction_outcome:
        evidence_level = "INTERACTION_OUTCOME_ONLY"
    else:
        evidence_level = "BACKGROUND_ONLY"

    return NaturalHysteresisGate(
        dataset=dataset,
        predictive_window_years=predictive_window_years,
        minimum_years_for_three_regimes=minimum_years,
        duration_passed=duration_passed,
        information_pair_passed=information_pair_passed,
        timing_pair_passed=timing_pair_passed,
        direct_hysteresis_ready=direct_ready,
        evidence_level=evidence_level,
        missing_requirements=tuple(missing),
    )


def rank_evidence_ladder(
    datasets: Iterable[NaturalHysteresisDataset],
    *,
    predictive_window_years: int = 8,
) -> tuple[NaturalHysteresisGate, ...]:
    """Sort by evidence class without pretending the classes are a quality score."""

    order = {
        "DIRECT_HYSTERESIS_READY": 0,
        "DECISION_TIME_INFORMATION_ANCHOR": 1,
        "PREDICTIVE_INFORMATION_TEST": 2,
        "INTERACTION_TIMING_TEST": 3,
        "LONG_TERM_PHENOLOGY_CONTRAST": 4,
        "INTERACTION_OUTCOME_ONLY": 5,
        "BACKGROUND_ONLY": 6,
    }
    rows = [
        evaluate_natural_hysteresis_gate(
            dataset,
            predictive_window_years=predictive_window_years,
        )
        for dataset in datasets
    ]
    return tuple(
        sorted(
            rows,
            key=lambda row: (
                order[row.evidence_level],
                row.dataset.name,
            ),
        )
    )
