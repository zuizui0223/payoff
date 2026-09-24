import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_tracking_theory_supporting_information import build_supporting_information


def test_tracking_supporting_information_has_frozen_sections():
    text = build_supporting_information()
    for section in range(1, 7):
        assert f"## S{section}." in text
    assert "## S7. Frozen provenance" in text
    assert "## S8. Claim boundary" in text


def test_tracking_supporting_information_preserves_core_results():
    text = build_supporting_information()
    assert "| 5 | 0.065 | 0.070 |" in text
    assert "22 coordination barriers" in text
    assert "21 persistence rescues" in text
    assert "1.094972" in text
    assert "-5.945681" in text
    assert "| pilot | 32 | 9 | 0.18750 |" in text
    assert "| independent replication | 128 | 0 | 0.09375 |" in text
    assert "drift-assisted barrier crossing, not drift rescue" in text
    assert "0/7 controller gains persist" in text
    assert "7/7 persist" in text


def test_tracking_supporting_information_keeps_claim_boundary():
    text = build_supporting_information().lower()
    assert "introduces no new simulation" in text
    assert "not natural prevalence estimates or empirical thresholds" in text
    assert "later empirical phase-retention programme is outside" in text
    assert "aikens" not in text
    assert "wigeon" not in text
    assert "barnacle" not in text
