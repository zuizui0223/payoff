import pytest

from src.wigeon_gate_bundle import assemble_wigeon_gate_bundle


def phase_receipt(*, passed, high, lam=0.85994):
    return {
        "system_name": "Eurasian wigeon",
        "independent_test_id": "wigeon_vantoor2021_W1",
        "prospective_contract_satisfied": True,
        "gate": {
            "passed": passed,
            "estimate": {
                "pairs": 224,
                "lambda_retention": lam,
                "residual_forcing": None,
                "rmse": None,
                "r_squared": None,
                "retention_class": "restoring",
                "source_kind": "reported_summary",
                "lambda_se": 0.04509,
                "p_vs_no_correction": 0.00190,
            },
            "prediction": {
                "lambda_low": None if high == 1.0 else -0.75,
                "lambda_high": high,
                "min_pairs": 30,
                "require_retention_class": "restoring",
            },
            "interval_passed": passed,
            "class_passed": True,
            "reasons": [] if passed else [
                "observed lambda lies outside the predeclared prediction interval"
            ],
        },
    }


def stopover_receipt(*, passed=False):
    return {
        "system_name": "Eurasian wigeon",
        "independent_test_id": "wigeon_vantoor2021_W2_stopover",
        "prospective_contract_satisfied": True,
        "gate": {
            "system_name": "Eurasian wigeon",
            "predictions": [
                {
                    "name": "stopover_duration",
                    "expected_direction": "decrease",
                    "observed_effect": -0.00014,
                    "observed_p_value": 0.972,
                    "max_p_value": None,
                    "direction_passed": True,
                    "support_passed": True,
                    "passed": True,
                    "prospective": True,
                }
            ],
            "prospective_predictions": 1,
            "passed_predictions": 1,
            "failed_predictions": 0,
            "all_prospective_passed": True,
        },
    }


def test_wigeon_bundle_recovers_lambda_pass_actuator_fail():
    bundle = assemble_wigeon_gate_bundle(
        phase_receipt(passed=True, high=1.0),
        phase_receipt(passed=False, high=0.75),
        stopover_receipt(passed=False),
        stopover_source_interpretation={
            "source_status": "NOT_SUPPORTED",
        },
        travel_speed_diagnostic={
            "status": "NOT_SUPPORTED",
            "p_value": 0.197,
        },
        distance_moderation_diagnostic={
            "status": "NOT_SUPPORTED",
            "p_value": 0.371,
        },
    )

    assert bundle.primary_lambda_passed
    assert not bundle.strong_contraction_passed
    assert bundle.stopover_direction_passed
    assert not bundle.stopover_source_supported
    assert not bundle.stopover_actuator_passed
    assert bundle.lambda_retention == pytest.approx(0.85994)
    assert bundle.lambda_se == pytest.approx(0.04509)
    assert bundle.p_vs_no_correction == pytest.approx(0.00190)
    assert bundle.two_gate_class == "LAMBDA_PASS_ACTUATOR_NOT_SUPPORTED"
    assert bundle.travel_speed_diagnostic["status"] == "NOT_SUPPORTED"


def test_wigeon_bundle_rejects_nonprospective_primary_receipt():
    primary = phase_receipt(passed=True, high=1.0)
    primary["prospective_contract_satisfied"] = False

    with pytest.raises(ValueError, match="not prospective"):
        assemble_wigeon_gate_bundle(
            primary,
            phase_receipt(passed=False, high=0.75),
            stopover_receipt(passed=False),
        stopover_source_interpretation={
            "source_status": "NOT_SUPPORTED",
        },
        )


def test_wigeon_bundle_rejects_wrong_stopover_test_id():
    stopover = stopover_receipt(passed=False)
    stopover["independent_test_id"] = "wrong_test"

    with pytest.raises(ValueError, match="W2"):
        assemble_wigeon_gate_bundle(
            phase_receipt(passed=True, high=1.0),
            phase_receipt(passed=False, high=0.75),
            stopover,
            stopover_source_interpretation={
                "source_status": "NOT_SUPPORTED",
            },
        )


def test_wigeon_bundle_exposes_no_omnibus_score():
    bundle = assemble_wigeon_gate_bundle(
        phase_receipt(passed=True, high=1.0),
        phase_receipt(passed=False, high=0.75),
        stopover_receipt(passed=False),
        stopover_source_interpretation={
            "source_status": "NOT_SUPPORTED",
        },
    )

    with pytest.raises(AttributeError, match="no omnibus"):
        _ = bundle.omnibus_score


def test_wigeon_bundle_keeps_literal_w2_direction_separate_from_source_support():
    bundle = assemble_wigeon_gate_bundle(
        phase_receipt(passed=True, high=1.0),
        phase_receipt(passed=False, high=0.75),
        stopover_receipt(passed=False),
        stopover_source_interpretation={
            "source_status": "NOT_SUPPORTED",
            "directional_sign_observed": True,
            "p_value": 0.972,
        },
    )

    assert bundle.stopover_direction_passed
    assert not bundle.stopover_source_supported
    assert bundle.two_gate_class == (
        "LAMBDA_PASS_ACTUATOR_NOT_SUPPORTED"
    )


def test_wigeon_bundle_requires_source_support_interpretation():
    with pytest.raises(ValueError, match="source interpretation"):
        assemble_wigeon_gate_bundle(
            phase_receipt(passed=True, high=1.0),
            phase_receipt(passed=False, high=0.75),
            stopover_receipt(passed=False),
        )
