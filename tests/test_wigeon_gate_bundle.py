import pytest

from src.wigeon_gate_bundle import assemble_wigeon_gate_bundle


LAMBDA = 0.7497680211367301
LAMBDA_SE = 0.04990566712278233
LAMBDA_P = 5.328241982727779e-7
STOPOVER_EFFECT = -0.06286262115570287
STOPOVER_P = 0.031661798202295054


def phase_receipt(*, passed, high, lam=LAMBDA):
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
                "lambda_se": LAMBDA_SE,
                "p_vs_no_correction": LAMBDA_P,
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


def stopover_receipt():
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
                    "observed_effect": STOPOVER_EFFECT,
                    "observed_p_value": STOPOVER_P,
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


def test_wigeon_bundle_recovers_source_faithful_lambda_and_stopover_support():
    bundle = assemble_wigeon_gate_bundle(
        phase_receipt(passed=True, high=1.0),
        phase_receipt(passed=True, high=0.75),
        stopover_receipt(),
        stopover_source_interpretation={
            "source_status": "SUPPORTED",
            "fixed_p_value_threshold_preregistered": False,
            "secondary_gain_band_passed": False,
        },
        travel_speed_diagnostic={
            "status": "NOT_SUPPORTED",
            "p_value": 0.41699858388761735,
        },
        distance_moderation_diagnostic={
            "status": "NOT_SUPPORTED",
            "p_value": 0.08230417519325887,
        },
    )

    assert bundle.primary_lambda_passed
    assert bundle.strong_contraction_passed
    assert bundle.stopover_direction_passed
    assert bundle.stopover_source_supported
    assert bundle.stopover_actuator_passed
    assert bundle.lambda_retention == pytest.approx(LAMBDA)
    assert bundle.lambda_se == pytest.approx(LAMBDA_SE)
    assert bundle.p_vs_no_correction == pytest.approx(LAMBDA_P)
    assert bundle.two_gate_class == "LAMBDA_PASS_ACTUATOR_SUPPORTED"
    assert bundle.travel_speed_diagnostic["status"] == "NOT_SUPPORTED"


def test_wigeon_bundle_rejects_nonprospective_primary_receipt():
    primary = phase_receipt(passed=True, high=1.0)
    primary["prospective_contract_satisfied"] = False

    with pytest.raises(ValueError, match="not prospective"):
        assemble_wigeon_gate_bundle(
            primary,
            phase_receipt(passed=True, high=0.75),
            stopover_receipt(),
            stopover_source_interpretation={
                "source_status": "SUPPORTED",
            },
        )


def test_wigeon_bundle_rejects_wrong_stopover_test_id():
    stopover = stopover_receipt()
    stopover["independent_test_id"] = "wrong_test"

    with pytest.raises(ValueError, match="W2"):
        assemble_wigeon_gate_bundle(
            phase_receipt(passed=True, high=1.0),
            phase_receipt(passed=True, high=0.75),
            stopover,
            stopover_source_interpretation={
                "source_status": "SUPPORTED",
            },
        )


def test_wigeon_bundle_exposes_no_omnibus_score():
    bundle = assemble_wigeon_gate_bundle(
        phase_receipt(passed=True, high=1.0),
        phase_receipt(passed=True, high=0.75),
        stopover_receipt(),
        stopover_source_interpretation={
            "source_status": "SUPPORTED",
        },
    )

    with pytest.raises(AttributeError, match="no omnibus"):
        _ = bundle.omnibus_score


def test_wigeon_bundle_keeps_literal_direction_separate_from_source_support():
    bundle = assemble_wigeon_gate_bundle(
        phase_receipt(passed=True, high=1.0),
        phase_receipt(passed=True, high=0.75),
        stopover_receipt(),
        stopover_source_interpretation={
            "source_status": "NOT_SUPPORTED",
            "directional_sign_observed": True,
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
            phase_receipt(passed=True, high=0.75),
            stopover_receipt(),
        )
