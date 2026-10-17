"""Journal-facing mathematical theory claim, supplement and result-freeze guards.

Checks exact coexistence of the general case, boundary regimes, the
threshold-only short expression, the noisy Gaussian observation caveat
and the original V8/S3 data. Does not estimate animal-level mechanisms.
"""
from pathlib import Path

from scripts.audit_amnat_v4_review_readiness import audit

ROOT=Path(__file__).resolve().parents[1]
MANUSCRIPT=ROOT/"manuscript/PAYOFF_B_INFORMATION_CONTROL_V4_V8_INTEGRATED.md"
FRONT=ROOT/"submission/AMNAT_V4_FRONTMATTER_REVISED_20261011.md"
SUPP=ROOT/"submission/AMNAT_V4_SUPPLEMENTARY_MATHEMATICAL_NOTE_S4_20261017.md"


def read():
    return (MANUSCRIPT.read_text(encoding="utf-8"),
            FRONT.read_text(encoding="utf-8"),
            SUPP.read_text(encoding="utf-8"))


def test_general_decision_time_not_mislabelled_as_universal_special_case():
    ms,_,s4=read()
    assert "A_\\infty=S(q_0+\\Delta q)-B" in ms
    assert "t^*=\\max" in ms
    assert "threshold-normalized case" in ms
    assert "Sq_0=B" in ms
    assert "no finite waiting time has positive" in ms
    assert "the unique zero-cost optimum is" not in ms
    assert "Only in the **threshold-normalized case**" in ms
    assert "A_\\infty\\leq0" in s4
    assert "R\\leq1" in s4
    assert "R>1" in s4
    assert "nonzero" in s4
    assert "not the general optimal decision time" in s4


def test_noisy_information_retention_does_not_claim_variance_equals_lambda2():
    ms,_,s4=read()
    assert "conditional-mean" in ms
    assert "phase-independent mean innovation" in ms
    assert "Neither \\(K_i\\) nor \\(h_i\\)" in ms
    assert "observation-noise-free" in ms
    assert "Noisy cue estimates retain additional" in ms
    assert "P_{\\mathrm{next}}-\\lambda^2P" in s4
    assert "h^2K(1-K)" in s4
    assert "Q=0" in s4


def test_main_word_limit_and_source_data_are_unchanged_by_proof():
    ms,front,s4=read()
    outcome=audit(ms,front)
    assert outcome["status"]=="SOURCE_SCIENCE_CHECKS_PASS_SUBMISSION_HOLD",outcome["science_source_errors"]
    assert outcome["estimated_main_plus_abstract_words"] <= 7500
    assert outcome["submission_ready"] is False
    assert "+0.369" in ms and "+0.062" in ms
    assert "Table S3" in ms and "Table S2" in ms
    assert "NOT_SUPPORTED" in ms or "not supported" in ms.lower()
    assert "not a newly established ecological theorem" in s4
    assert "not estimates of birds' perceived cues" in ms
