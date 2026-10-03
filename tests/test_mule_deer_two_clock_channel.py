import json
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/"data"/"payoff_b_mule_deer_two_clock_channel_result_20261003.json"
CLASSIFICATION=ROOT/"data"/"payoff_b_two_clock_classification_20261003.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_channel_audit_uses_full_validated_actuator_block():
    r=load(RESULT)
    assert r["safe_joined_rows"]==62
    assert r["safe_animals"]==40
    assert r["parser_guard"]["actuator_rows_parsed"]==152


def test_phase_error_retains_signed_actuator_coefficients():
    r=load(RESULT)
    rlo,rhi=r["movement_rate"]["raw_ci95"]["beta_DFP_Start"]
    slo,shi=r["stopover"]["raw_ci95"]["beta_DFP_Start"]
    assert rlo>0
    assert shi<0


def test_ifbfat_is_unresolved_in_both_downstream_actuator_models():
    r=load(RESULT)
    rlo,rhi=r["movement_rate"]["raw_ci95"]["beta_scaledIFBFat"]
    slo,shi=r["stopover"]["raw_ci95"]["beta_scaledIFBFat"]
    assert rlo<0<rhi
    assert slo<0<shi
    assert r["interpretation"]["channel_dissociation_supported"] is True


def test_channel_dissociation_does_not_upgrade_to_h2():
    p=load(CLASSIFICATION)
    deer={row["system"]:row for row in p["systems"]}["Ortega mule deer"]
    assert deer["hybrid"]=="H1_CANDIDATE"
    assert deer["channel_dissociation"]=="SUPPORTED"
    assert "H2" in deer["boundary"]
