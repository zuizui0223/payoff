import json
from pathlib import Path

import pytest

from src.prospective_tracking_evaluation import (
    ReportedPhaseObservation,
    evaluate_registered_actuators,
    evaluate_registered_reported_phase,
)
from src.prospective_tracking_registry import (
    ActuatorObservation,
    ActuatorObservationSet,
    ActuatorPredictionSpec,
    ActuatorRegistration,
    PhaseRetentionRegistration,
)
from src.wigeon_gate_bundle import assemble_wigeon_gate_bundle


ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def phase_evaluation(registration_path: str):
    reg_payload = load(registration_path)
    obs_payload = load(
        "data/wigeon_phase_retention_observation_20260922.json"
    )
    reg = PhaseRetentionRegistration(**reg_payload)
    reported = obs_payload["reported_estimate"]
    obs = ReportedPhaseObservation(
        system_name=obs_payload["system_name"],
        independent_test_id=obs_payload["independent_test_id"],
        phase_coordinate_id=obs_payload["phase_coordinate_id"],
        segment_scale_id=obs_payload["segment_scale_id"],
        pairs=int(reported["pairs"]),
        lambda_retention=float(reported["lambda_retention"]),
        lambda_se=float(reported["lambda_se"]),
        p_vs_no_correction=float(reported["p_vs_no_correction"]),
    )
    return evaluate_registered_reported_phase(reg, obs)


def actuator_evaluation():
    reg_payload = load(
        "data/wigeon_stopover_actuator_registration_20260921.json"
    )
    obs_payload = load(
        "data/wigeon_stopover_actuator_observation_20260922.json"
    )
    specs = tuple(
        ActuatorPredictionSpec(
            name=row["name"],
            expected_direction=row["expected_direction"],
            zero_tolerance=float(row.get("zero_tolerance", 0.0)),
            max_p_value=(
                None
                if row.get("max_p_value") is None
                else float(row["max_p_value"])
            ),
        )
        for row in reg_payload["predictions"]
    )
    reg = ActuatorRegistration(
        system_name=reg_payload["system_name"],
        independent_test_id=reg_payload["independent_test_id"],
        forcing_regime=reg_payload["forcing_regime"],
        predictions=specs,
    )
    observations = ActuatorObservationSet(
        system_name=obs_payload["system_name"],
        independent_test_id=obs_payload["independent_test_id"],
        observations=tuple(
            ActuatorObservation(
                name=row["name"],
                observed_effect=float(row["observed_effect"]),
                p_value=float(row["p_value"]),
            )
            for row in obs_payload["observations"]
        ),
    )
    return reg, evaluate_registered_actuators(reg, observations)


def as_receipt(evaluation):
    from dataclasses import asdict

    return {
        "system_name": evaluation.system_name,
        "independent_test_id": evaluation.independent_test_id,
        "prospective_contract_satisfied": True,
        "gate": asdict(evaluation.gate),
    }


def test_source_faithful_wigeon_primary_and_strong_phase_gates_both_pass():
    primary = phase_evaluation(
        "data/wigeon_phase_retention_registration_20260921.json"
    )
    strong = phase_evaluation(
        "data/wigeon_strong_contraction_registration_20260921.json"
    )

    assert primary.gate.passed
    assert strong.gate.passed
    assert primary.gate.estimate.lambda_retention == pytest.approx(
        0.7497680211367301
    )
    assert primary.gate.estimate.lambda_se == pytest.approx(
        0.04990566712278233
    )
    assert (
        0.75 - primary.gate.estimate.lambda_retention
        == pytest.approx(0.0002319788632699)
    )


def test_w2_primary_gate_is_directional_and_did_not_preregister_p_threshold():
    registration, evaluation = actuator_evaluation()

    assert registration.predictions[0].max_p_value is None
    assert evaluation.gate.all_prospective_passed
    row = evaluation.gate.predictions[0]
    assert row.direction_passed
    assert row.support_passed
    assert row.observed_effect == pytest.approx(-0.06286262115570287)
    assert row.observed_p_value == pytest.approx(0.031661798202295054)

    diagnostics = load(
        "data/wigeon_secondary_actuator_diagnostics_20260922.json"
    )
    interpretation = diagnostics["W2_stopover_source_interpretation"]
    assert interpretation["fixed_p_value_threshold_preregistered"] is False
    assert interpretation["formal_directional_gate"] == "PASS"
    assert interpretation["secondary_gain_band"]["status"] == "FAIL"


def test_corrected_wigeon_bundle_is_lambda_pass_actuator_supported():
    primary = phase_evaluation(
        "data/wigeon_phase_retention_registration_20260921.json"
    )
    strong = phase_evaluation(
        "data/wigeon_strong_contraction_registration_20260921.json"
    )
    _, stopover = actuator_evaluation()
    diagnostics = load(
        "data/wigeon_secondary_actuator_diagnostics_20260922.json"
    )

    bundle = assemble_wigeon_gate_bundle(
        as_receipt(primary),
        as_receipt(strong),
        as_receipt(stopover),
        stopover_source_interpretation=(
            diagnostics["W2_stopover_source_interpretation"]
        ),
        travel_speed_diagnostic=diagnostics["W3_travel_speed_diagnostic"],
        distance_moderation_diagnostic=(
            diagnostics["W4_distance_moderation_diagnostic"]
        ),
    )

    assert bundle.primary_lambda_passed
    assert bundle.strong_contraction_passed
    assert bundle.stopover_direction_passed
    assert bundle.stopover_source_supported
    assert bundle.two_gate_class == "LAMBDA_PASS_ACTUATOR_SUPPORTED"
    assert bundle.lambda_retention == pytest.approx(0.7497680211367301)


def test_historical_machine_receipts_are_explicitly_superseded():
    old_wigeon = load(
        "data/payoff_b_wigeon_phase_retention_receipt_20260921.json"
    )
    old_panel = load(
        "data/payoff_b_three_taxon_phase_retention_receipt_20260921.json"
    )
    assert old_wigeon["status"] == "SUPERSEDED"
    assert old_wigeon["superseded_by"].endswith("20260922.json")
    assert old_panel["status"] == "SUPERSEDED"
    assert old_panel["superseded_by"].endswith("20260922.json")


def test_canonical_corrected_receipts_agree_on_wigeon_value_and_w2_boundary():
    wigeon = load(
        "data/payoff_b_wigeon_phase_retention_receipt_20260922.json"
    )
    panel = load(
        "data/payoff_b_three_taxon_phase_retention_receipt_20260922.json"
    )
    source = load(
        "data/wigeon_source_faithful_revalidation_result_20260922.json"
    )

    lam = wigeon["primary_phase_retention"]["lambda_hat"]
    assert lam == pytest.approx(
        source["primary_phase_retention"]["lambda_hat"]
    )
    wigeon_panel = next(
        row for row in panel["taxa"]
        if row["taxon"] == "Mareca penelope"
    )
    assert wigeon_panel["lambda_hat"] == pytest.approx(lam)

    stopover = wigeon["actuators"]["stopover"]
    assert stopover["fixed_p_value_threshold_preregistered"] is False
    assert stopover["formal_directional_gate"] == "PASS"
    assert stopover["secondary_gain_band_outcome"] == "FAIL"
