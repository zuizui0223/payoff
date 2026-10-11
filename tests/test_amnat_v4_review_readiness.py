"""Journal-level editorial checks; no empirical outcomes are recomputed."""
from pathlib import Path

from scripts.audit_amnat_v4_review_readiness import audit

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "manuscript/PAYOFF_B_INFORMATION_CONTROL_V4_V8_INTEGRATED.md"
FRONT = ROOT / "submission/AMNAT_V4_FRONTMATTER_REVISED_20261011.md"


def get_sources():
    return MAIN.read_text(encoding="utf-8"), FRONT.read_text(encoding="utf-8")


def test_agreed_main_text_keeps_review_restrictions_explicit():
    s, f = get_sources()
    result = audit(s, f)
    assert result["status"] == "SOURCE_SCIENCE_CHECKS_PASS_SUBMISSION_HOLD"
    assert not result["submission_ready"]
    assert result["science_source_errors"] == []
    assert result["methods_before_results"]
    assert result["heading_sequence_valid"]
    assert result["abstract_word_count"] <= 200
    assert result["keyword_count"] == 6
    assert result["estimated_main_plus_abstract_words"] <= 7500
    assert all(result["claim_guards"].values())
    assert "complete Literature Cited absent" in result["submission_blockers"]
    assert "internal provenance remains in source" in result["submission_blockers"]


def test_abbreviated_obvious_false_claim_fails():
    s, f = get_sources()
    mutated = s.replace("unique spatial source", "duplicated species records")
    result = audit(mutated, f)
    assert result["status"] == "SOURCE_SCIENCE_CHECKS_FAIL"
    assert any("range_pair_inference" in x for x in result["science_source_errors"])


def test_abstract_mismatch_is_detected():
    s, f = get_sources()
    f = f.replace(
        "Seasonal organisms must align", "All organisms perfectly align"
    )
    result = audit(s, f)
    assert "frontmatter abstract differs from manuscript" in result["science_source_errors"]


def test_drop_independent_sample_caveat_is_detected():
    s, f = get_sources()
    assert "same individuals' migration speed" in s
    bad = s.replace("same individuals' migration speed", "movement speed")
    result = audit(bad, f)
    assert any("redstart_samples_not_conflated" in x for x in result["science_source_errors"])


def test_method_results_reverse_is_detected():
    s, f = get_sources()
    s = s.replace(
        "## 3. Empirical methods and scope of inference",
        "## 7. Empirical methods and scope of inference",
    )
    result = audit(s, f)
    assert result["methods_before_results"] is False
    assert "methods do not precede natural results" in result["science_source_errors"]
