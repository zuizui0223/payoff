import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_oikos_supporting_information import build_supporting_rtf

BS = chr(92)


def test_oikos_supporting_rtf_contains_frozen_sections():
    text = build_supporting_rtf()
    assert text.startswith("{" + BS + "rtf1")
    for section in range(1, 9):
        assert f"S{section}." in text
    assert "2026-09-20" in text


def test_oikos_supporting_rtf_preserves_core_negative_result():
    text = build_supporting_rtf()
    assert "independent replication" in text
    assert "0.09375" in text
    assert "failed pilot" in text
    assert "drift-assisted barrier crossing, not drift rescue" in text


def test_oikos_supporting_rtf_is_anonymous():
    text = build_supporting_rtf()
    for token in ["ZHANG RUIQI", "rachelzhang0223", "zuizui0223"]:
        assert token not in text
