from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_TRACKING_THEORY_V1.md"
PRIOR_ART = ROOT / "docs" / "PAYOFF_B_TRACKING_THEORY_PRIOR_ART_20260924.md"
CLAIM_FREEZE = ROOT / "data" / "payoff_b_tracking_theory_claim_freeze_20260924.json"
FRAMING_AMENDMENT = ROOT / "data" / "payoff_b_tracking_theory_framing_amendment_20260925.json"


def manuscript_text():
    return MANUSCRIPT.read_text(encoding="utf-8")


def test_tracking_theory_manuscript_has_no_control_character_corruption():
    text = manuscript_text()
    illegal = [
        ch for ch in text
        if ord(ch) < 32 and ch not in ("\n", "\t")
    ]
    assert illegal == []
    slash = chr(92)
    assert slash + "n" not in text
    assert slash + "frac" not in text
    assert slash + "beta" not in text
    assert slash + "times" not in text
    assert "rac{" not in text
    assert "Nge" not in text


def test_tracking_theory_manuscript_states_programme_boundary():
    text = manuscript_text()
    assert "separate from the PAYOFF-B GEB empirical phase-retention paper" in text
    assert "no post-2026-09-20 empirical phase-retention result is used" in text.lower()
    assert "environmental mismatch is an outcome of a multi-axis tracking system" in text.lower()
    assert "coordination barriers are therefore a failure mode" in text.lower()


def test_tracking_theory_manuscript_preserves_negative_results():
    text = manuscript_text()
    assert "did not reproduce any gain at or above 0.10" in text
    assert "drift-assisted barrier crossing, not drift rescue" in text
    assert "not intrinsically beneficial or harmful" in text


def test_tracking_theory_prior_art_and_claim_freeze_exist():
    assert PRIOR_ART.exists()
    assert CLAIM_FREEZE.exists()
    assert FRAMING_AMENDMENT.exists()
    prior = PRIOR_ART.read_text(encoding="utf-8")
    assert "do not claim that it is novel" in prior.lower()
    assert "mismatch can be buffered" in prior.lower()
    assert "endpoint mismatch can remain non-identifying" in prior.lower()


def test_tracking_theory_predictions_are_empirically_falsifiable():
    text = manuscript_text()
    section = text.split("## 6. Testable predictions", 1)[1].split(
        "## 7. Scope and limitations", 1
    )[0]
    assert section.count("**Observable:**") == 7
    assert section.count("**Falsified if:**") == 7


def test_tracking_theory_framing_amendment_preserves_scientific_freeze():
    import json

    amendment = json.loads(FRAMING_AMENDMENT.read_text(encoding="utf-8"))
    assert amendment["scientific_evidence_freeze_unchanged"] is True
    assert amendment["new_simulation_added"] is False
    assert amendment["quantitative_claim_changed"] is False
    assert (
        amendment["coordination_barrier_role"]
        == "failure_mode_of_spatiotemporal_buffering"
    )
