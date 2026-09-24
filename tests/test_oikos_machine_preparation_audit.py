from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "submission" / "OIKOS_MACHINE_PREPARATION_AUDIT_20260924.md"


def test_oikos_machine_preparation_audit_is_frozen():
    text = AUDIT.read_text(encoding="utf-8")
    assert "35999337326" in text
    assert "2df627ecce2f27d884f617d7b0e2898b10fcfb68" in text
    assert "10807716748" in text
    assert "10807746767" in text
    assert "10807602200" in text
    assert "062262cafba85c7957094173075964aa0e3d5d2ac775da3335724aaafd4f17da" in text
    assert "d75d914ff2e05d25a4fa571d8a48b0dec5bd3d34416132a7ab2eccaf67fa9d4a" in text
    assert "payload files: **40**" in text
    assert "payload files: **58**" in text
    assert "empirical-programme paths: **0**" in text
    assert "Introduction: begins on page 2" in text
    assert "pages: **27**" in text
    assert "pages: **10**" in text
    assert "No additional synthetic simulation is licensed by this audit." in text
