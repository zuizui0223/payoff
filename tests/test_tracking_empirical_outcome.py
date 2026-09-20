import pytest

from src.tracking_empirical_outcome import (
    LandscapeOutcomeObservation,
    OutcomeValidationThresholds,
    evaluate_outcome_validation_gate,
    validate_landscape_outcome,
)


def prediction():
    return {
        "final_abundance": 100.0,
        "final_climate_centroid": 4.0,
        "final_phenology_shift": 2.0,
        "rms_abiotic_mismatch": 0.5,
        "mean_low_density_growth": 0.2,
        "persisted": True,
    }


def test_outcome_validation_reports_metric_errors_without_refitting():
    observed = LandscapeOutcomeObservation(
        final_abundance=90.0,
        final_climate_centroid=3.5,
        final_phenology_shift=2.2,
        rms_abiotic_mismatch=0.6,
        mean_low_density_growth=0.18,
        persisted=True,
    )
    validation = validate_landscape_outcome(
        prediction(),
        observed,
    )

    assert validation.compared_metrics == 6
    assert validation.final_abundance_error == pytest.approx(10.0)
    assert validation.final_abundance_relative_error == pytest.approx(
        10.0 / 90.0
    )
    assert validation.final_climate_centroid_error == pytest.approx(0.5)
    assert validation.final_phenology_shift_error == pytest.approx(-0.2)
    assert validation.rms_abiotic_mismatch_error == pytest.approx(-0.1)
    assert validation.mean_low_density_growth_error == pytest.approx(0.02)
    assert validation.persistence_match


def test_outcome_gate_passes_predeclared_tolerances():
    validation = validate_landscape_outcome(
        prediction(),
        LandscapeOutcomeObservation(
            final_abundance=95.0,
            final_climate_centroid=3.9,
            persisted=True,
        ),
    )
    gate = evaluate_outcome_validation_gate(
        validation,
        OutcomeValidationThresholds(
            max_abs_final_abundance_relative_error=0.10,
            max_abs_climate_centroid_error=0.2,
            require_persistence_match=True,
        ),
    )
    assert gate.passed
    assert gate.criteria_evaluated == 3
    assert gate.reasons == ()


def test_outcome_gate_fails_persistence_and_numeric_error_separately():
    validation = validate_landscape_outcome(
        prediction(),
        LandscapeOutcomeObservation(
            final_abundance=50.0,
            persisted=False,
        ),
    )
    gate = evaluate_outcome_validation_gate(
        validation,
        OutcomeValidationThresholds(
            max_abs_final_abundance_relative_error=0.25,
            require_persistence_match=True,
        ),
    )
    assert not gate.passed
    assert len(gate.reasons) == 2


def test_declared_threshold_fails_when_held_out_metric_is_missing():
    validation = validate_landscape_outcome(
        prediction(),
        LandscapeOutcomeObservation(
            persisted=True,
        ),
    )
    gate = evaluate_outcome_validation_gate(
        validation,
        OutcomeValidationThresholds(
            max_abs_climate_centroid_error=1.0,
        ),
    )
    assert not gate.passed
    assert any(
        "unavailable" in reason
        for reason in gate.reasons
    )


def test_zero_observed_abundance_has_no_relative_error_but_can_use_persistence():
    validation = validate_landscape_outcome(
        prediction(),
        LandscapeOutcomeObservation(
            final_abundance=0.0,
            persisted=False,
        ),
    )
    assert validation.final_abundance_error == pytest.approx(100.0)
    assert validation.final_abundance_relative_error is None

    gate = evaluate_outcome_validation_gate(
        validation,
        OutcomeValidationThresholds(
            require_persistence_match=True,
        ),
    )
    assert not gate.passed


def test_outcome_thresholds_require_at_least_one_criterion():
    with pytest.raises(ValueError):
        OutcomeValidationThresholds()


def test_empty_held_out_outcome_is_rejected():
    with pytest.raises(ValueError):
        validate_landscape_outcome(
            prediction(),
            LandscapeOutcomeObservation(),
        )
