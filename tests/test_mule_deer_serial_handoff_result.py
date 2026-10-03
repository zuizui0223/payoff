import json
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
HANDOFF=ROOT/"data"/"payoff_b_mule_deer_serial_handoff_result_20261003.json"
CLASS=ROOT/"data"/"payoff_b_two_clock_classification_20261003.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_serial_handoff_fails_primary_rule():
    r=load(HANDOFF)
    assert r["decision_rule"]["outcome"]=="NOT_COMPATIBLE"
    assert r["decision_rule"]["phase_pass"] is False
    assert r["decision_rule"]["fat_conditional_null"] is False


def test_primary_clustered_intervals_match_boundary():
    r=load(HANDOFF)
    p=r["bootstrap"]["raw_DFP_Start_ci95"]
    f=r["bootstrap"]["raw_scaledIFBFat_ci95"]
    assert p[0] < 0 < p[1]
    assert f[1] < 0


def test_year_centered_sensitivity_is_unresolved_for_both():
    r=load(HANDOFF)
    p=r["bootstrap"]["year_fe_DFP_Start_ci95"]
    f=r["bootstrap"]["year_fe_scaledIFBFat_ci95"]
    assert p[0] < 0 < p[1]
    assert f[0] < 0 < f[1]


def test_classification_does_not_upgrade_serial_handoff():
    p=load(CLASS)
    deer=next(x for x in p["systems"] if x["system"]=="Ortega mule deer")
    assert deer["serial_handoff"]=="NOT_COMPATIBLE_PRIMARY"
    assert deer["hybrid"]=="H1_CANDIDATE"
