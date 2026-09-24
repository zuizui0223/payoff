import json
from pathlib import Path

from src.cross_system_lambda_reliability import (
    LambdaReliabilitySystem,
    evaluate_cross_system_lambda_reliability,
    systems_from_registry,
)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = (
    ROOT
    / "data"
    / "payoff_b_lambda_recovery_taxon_registry_20260922.json"
)


def test_current_registry_licenses_coordinate_but_not_latent_magnitude_comparison():
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    gate = evaluate_cross_system_lambda_reliability(
        systems_from_registry(payload)
    )

    assert gate.unique_taxa == 3
    assert gate.estimator_scale_coordinate_licensed
    assert not gate.latent_magnitude_comparison_licensed
    assert gate.taxa_with_any_reliability_calibration == 2
    assert gate.taxa_with_source_specific_error_identification == 0
    assert gate.taxa_pending_reliability_calibration == 3
    assert (
        "ASSUMPTION_CONDITIONAL_SENSITIVITY_IS_NOT_CORRECTED_TRUTH"
        in gate.blockers
    )
    assert (
        "DIRECT_SYSTEMS_PENDING_RELIABILITY_CALIBRATION"
        in gate.blockers
    )


def test_barnacle_and_wigeon_are_sensitivity_ready_not_source_specific_error_identified():
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    rows = systems_from_registry(payload)
    greenland = next(
        row for row in rows if row.system_id == "barnacle_greenland_R2_R3"
    )
    barents = next(
        row for row in rows if row.system_id == "barnacle_barents_R1_R2"
    )
    assert greenland.calibration_class == "SENSITIVITY_ASSUMPTION_CONDITIONAL"
    assert barents.calibration_class == "SENSITIVITY_ASSUMPTION_CONDITIONAL"


def test_wigeon_is_sensitivity_ready_not_source_specific_error_identified():
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    rows = systems_from_registry(payload)
    wigeon = next(
        row
        for row in rows
        if row.system_id == "eurasian_wigeon_staging_transition"
    )
    assert wigeon.calibration_class == (
        "SENSITIVITY_ASSUMPTION_CONDITIONAL"
    )


def test_latent_magnitude_comparison_requires_identified_error_for_every_taxon():
    rows = (
        LambdaReliabilitySystem(
            system_id="a",
            taxon="Taxon a",
            observed_lambda=0.2,
            calibration_status="COMPLETE_SOURCE_SPECIFIC_IDENTIFIED",
            confirmatory_recovery_ready=True,
        ),
        LambdaReliabilitySystem(
            system_id="b",
            taxon="Taxon b",
            observed_lambda=0.4,
            calibration_status="COMPLETE_SOURCE_SPECIFIC_IDENTIFIED",
            confirmatory_recovery_ready=True,
        ),
        LambdaReliabilitySystem(
            system_id="c",
            taxon="Taxon c",
            observed_lambda=0.7,
            calibration_status="COMPLETE_SOURCE_SPECIFIC_IDENTIFIED",
            confirmatory_recovery_ready=True,
        ),
    )
    gate = evaluate_cross_system_lambda_reliability(rows)
    assert gate.estimator_scale_coordinate_licensed
    assert gate.latent_magnitude_comparison_licensed
    assert gate.taxa_with_source_specific_error_identification == 3
    assert gate.taxa_pending_reliability_calibration == 0
