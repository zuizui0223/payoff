from pathlib import Path


def test_payoff_does_not_replace_sister_validation():
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "SISTER_PROGRAM_SEPARATION_V1.md").read_text(encoding="utf-8")
    assert "must not replace" in text
    assert "SCH causal shared-coordinate conflict" in text
    assert "BALANCE direct sandwiched-world occupancy" in text
    assert "BITA causal dimensional release" in text
    assert "eta != 0" in text
