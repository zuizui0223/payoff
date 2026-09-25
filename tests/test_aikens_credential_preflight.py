from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "payoff-b-aikens-credential-preflight.yml"


def test_aikens_credential_preflight_never_opens_data() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "network_submission_performed" in text
    assert '"environmental_values_opened": False' in text
    assert '"lambda_outcome_opened": False' in text
    assert "run_appeears_manifest.py" not in text
    assert "--submit" not in text
    assert "credential_values_recorded" in text
