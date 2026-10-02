import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "payoff_b_information_recourse_two_axis_audit_20261002.json"


def load():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_two_axis_audit_is_prospective_and_submission_safe():
    payload = load()
    assert payload["status"] == "TWO_AXIS_EVIDENCE_AUDIT_COMPLETE_FULL_Q_R_TEST_NOT_IDENTIFIED"
    assert payload["frozen_submission_affected"] is False


def test_information_and_recourse_axes_are_kept_distinct():
    payload = load()
    boundary = payload["theoretical_axes"]["key_boundary"]
    assert "distinct quantities" in boundary
    assert "neither may be substituted" in boundary


def test_wigeon_registered_cross_axis_test_remains_not_supported():
    payload = load()
    wigeon = next(
        row for row in payload["evidence"]["cross_axis_tests"]
        if row["system"] == "Eurasian wigeon"
    )
    assert wigeon["sample"]["transitions"] == 224
    assert wigeon["sample"]["individuals"] == 28
    assert wigeon["estimate"] == 0.0202
    assert wigeon["p"] == 0.756
    assert wigeon["status"] == "NOT_SUPPORTED"


def test_barnacle_transition_screen_is_descriptive_boundary_only():
    payload = load()
    barnacle = next(
        row for row in payload["evidence"]["cross_axis_tests"]
        if row["system"] == "barnacle goose matched transition screen"
    )
    assert barnacle["matched_pairs"] == 7
    assert barnacle["spearman_rho"] == -0.464
    assert barnacle["p"] == 0.294
    assert barnacle["status"] == "NOT_SUPPORTED"
    assert "non-independent" in barnacle["boundary"]


def test_snow_goose_joint_lane_is_still_preoutcome():
    payload = load()
    snow = next(
        row for row in payload["evidence"]["cross_axis_tests"]
        if row["system"] == "greater snow goose"
    )
    assert snow["status"] == "PREOUTCOME_REGISTERED_NOT_EXECUTED"
    assert "same-system bridge" in snow["role"]


def test_full_natural_q_r_validation_remains_unidentified():
    payload = load()
    unsupported = payload["synthesis"]["not_supported"]
    assert "a natural validation of V(q,r)=r*V_A(q)" in unsupported
    assert "phase-retention lambda is equivalent to reduced-form actionability r" in unsupported
    assert "one system must independently calibrate q(t)" in payload["synthesis"]["current_direct_test_bottleneck"]
