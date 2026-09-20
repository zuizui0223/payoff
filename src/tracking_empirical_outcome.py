"""Held-out ecological outcome validation for PAYOFF-B tracking projections.

This layer is deliberately downstream of tracking-control validation.

A model can reproduce held-out movement/phase moments and still fail to predict
population or state outcomes. Therefore outcome validation is kept as a
separate estimand with separately predeclared tolerances.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class LandscapeOutcomeObservation:
    final_abundance: float | None = None
    final_climate_centroid: float | None = None
    final_phenology_shift: float | None = None
    rms_abiotic_mismatch: float | None = None
    mean_low_density_growth: float | None = None
    persisted: bool | None = None

    def __post_init__(self) -> None:
        for name in (
            "final_abundance",
            "final_climate_centroid",
            "final_phenology_shift",
            "rms_abiotic_mismatch",
            "mean_low_density_growth",
        ):
            value = getattr(self, name)
            if value is not None and not isfinite(value):
                raise ValueError(
                    f"{name} must be finite when supplied"
                )
        if self.final_abundance is not None and self.final_abundance < 0.0:
            raise ValueError("final_abundance must be non-negative")
        if (
            self.rms_abiotic_mismatch is not None
            and self.rms_abiotic_mismatch < 0.0
        ):
            raise ValueError(
                "rms_abiotic_mismatch must be non-negative"
            )


@dataclass(frozen=True)
class LandscapeOutcomeValidation:
    observed: LandscapeOutcomeObservation
    compared_metrics: int
    final_abundance_error: float | None
    final_abundance_relative_error: float | None
    final_climate_centroid_error: float | None
    final_phenology_shift_error: float | None
    rms_abiotic_mismatch_error: float | None
    mean_low_density_growth_error: float | None
    persistence_match: bool | None


@dataclass(frozen=True)
class OutcomeValidationThresholds:
    max_abs_final_abundance_relative_error: float | None = None
    max_abs_climate_centroid_error: float | None = None
    max_abs_phenology_shift_error: float | None = None
    max_abs_rms_mismatch_error: float | None = None
    max_abs_low_density_growth_error: float | None = None
    require_persistence_match: bool = False

    def __post_init__(self) -> None:
        values = (
            self.max_abs_final_abundance_relative_error,
            self.max_abs_climate_centroid_error,
            self.max_abs_phenology_shift_error,
            self.max_abs_rms_mismatch_error,
            self.max_abs_low_density_growth_error,
        )
        for value in values:
            if value is not None:
                if not isfinite(value) or value < 0.0:
                    raise ValueError(
                        "outcome tolerances must be non-negative and finite"
                    )
        if not self.require_persistence_match and all(
            value is None for value in values
        ):
            raise ValueError(
                "at least one ecological outcome criterion must be declared"
            )


@dataclass(frozen=True)
class OutcomeValidationGate:
    passed: bool
    thresholds: OutcomeValidationThresholds
    criteria_evaluated: int
    reasons: tuple[str, ...]


def validate_landscape_outcome(
    prediction: dict[str, float | bool],
    observed: LandscapeOutcomeObservation,
) -> LandscapeOutcomeValidation:
    """Compare a frozen prediction dictionary with held-out observations."""

    metrics = 0

    def error(
        key: str,
        observed_value: float | None,
    ) -> float | None:
        nonlocal metrics
        if observed_value is None:
            return None
        if key not in prediction:
            raise ValueError(
                f"prediction dictionary is missing required key {key}"
            )
        predicted = float(prediction[key])
        if not isfinite(predicted):
            raise ValueError(
                f"predicted {key} must be finite"
            )
        metrics += 1
        return predicted - observed_value

    abundance_error = error(
        "final_abundance",
        observed.final_abundance,
    )
    if (
        abundance_error is not None
        and observed.final_abundance is not None
        and observed.final_abundance != 0.0
    ):
        abundance_relative_error = (
            abundance_error / observed.final_abundance
        )
    else:
        abundance_relative_error = None

    centroid_error = error(
        "final_climate_centroid",
        observed.final_climate_centroid,
    )
    phenology_error = error(
        "final_phenology_shift",
        observed.final_phenology_shift,
    )
    mismatch_error = error(
        "rms_abiotic_mismatch",
        observed.rms_abiotic_mismatch,
    )
    growth_error = error(
        "mean_low_density_growth",
        observed.mean_low_density_growth,
    )

    if observed.persisted is None:
        persistence_match = None
    else:
        if "persisted" not in prediction:
            raise ValueError(
                "prediction dictionary is missing persisted"
            )
        metrics += 1
        persistence_match = (
            bool(prediction["persisted"])
            == observed.persisted
        )

    if metrics == 0:
        raise ValueError(
            "held-out ecological outcome contains no comparable metrics"
        )

    return LandscapeOutcomeValidation(
        observed=observed,
        compared_metrics=metrics,
        final_abundance_error=abundance_error,
        final_abundance_relative_error=(
            abundance_relative_error
        ),
        final_climate_centroid_error=centroid_error,
        final_phenology_shift_error=phenology_error,
        rms_abiotic_mismatch_error=mismatch_error,
        mean_low_density_growth_error=growth_error,
        persistence_match=persistence_match,
    )


def evaluate_outcome_validation_gate(
    validation: LandscapeOutcomeValidation,
    thresholds: OutcomeValidationThresholds,
) -> OutcomeValidationGate:
    """Evaluate independently declared ecological outcome tolerances."""

    reasons: list[str] = []
    criteria = 0

    def check(
        label: str,
        observed_error: float | None,
        threshold: float | None,
    ) -> None:
        nonlocal criteria
        if threshold is None:
            return
        criteria += 1
        if observed_error is None:
            reasons.append(
                f"{label} criterion declared but held-out metric is unavailable"
            )
        elif abs(observed_error) > threshold:
            reasons.append(
                f"{label} error exceeds predeclared tolerance"
            )

    check(
        "final abundance relative",
        validation.final_abundance_relative_error,
        thresholds.max_abs_final_abundance_relative_error,
    )
    check(
        "climate centroid",
        validation.final_climate_centroid_error,
        thresholds.max_abs_climate_centroid_error,
    )
    check(
        "phenology shift",
        validation.final_phenology_shift_error,
        thresholds.max_abs_phenology_shift_error,
    )
    check(
        "RMS mismatch",
        validation.rms_abiotic_mismatch_error,
        thresholds.max_abs_rms_mismatch_error,
    )
    check(
        "low-density growth",
        validation.mean_low_density_growth_error,
        thresholds.max_abs_low_density_growth_error,
    )

    if thresholds.require_persistence_match:
        criteria += 1
        if validation.persistence_match is None:
            reasons.append(
                "persistence criterion declared but held-out persistence is unavailable"
            )
        elif not validation.persistence_match:
            reasons.append(
                "predicted persistence does not match held-out persistence"
            )

    return OutcomeValidationGate(
        passed=(len(reasons) == 0),
        thresholds=thresholds,
        criteria_evaluated=criteria,
        reasons=tuple(reasons),
    )
