from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_INFORMATION_COORDINATION_V2_PREOUTCOME.md"
THEORY = ROOT / "theory" / "STATE_DEPENDENT_INFORMATION_DEADLINES.md"


def _non_whitespace_control_codes(text: str):
    return [
        (i, ord(ch))
        for i, ch in enumerate(text)
        if (ord(ch) < 32 and ch not in "\t\n\r") or ord(ch) == 127
    ]


def test_canonical_manuscript_has_no_corrupted_control_characters():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert _non_whitespace_control_codes(text) == []
    assert "\\boxed{" in text
    assert "\\frac" in text
    assert "\\right" in text


def test_hidden_deadline_uses_commitment_time_conditional_expectation():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    theory = THEORY.read_text(encoding="utf-8")

    expected = r"E[D(H)\mid\mathcal I]"
    assert expected in manuscript
    assert expected in theory

    # The old special-case binary average may be discussed elsewhere, but it
    # must not be presented in Discussion 4.2 as the general hidden-deadline
    # definition.
    section = manuscript.split(
        "### 4.2 Better information can transiently worsen coordination",
        1,
    )[1].split("### 4.3 Environmental recovery", 1)[0]
    assert r"(1-\pi)D_N+\pi D_E" not in section
