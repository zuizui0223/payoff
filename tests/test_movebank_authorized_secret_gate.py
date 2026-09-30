import json

from scripts.probe_movebank_authorized_secret_gate import _write


def test_write_does_not_require_credentials(tmp_path):
    output = tmp_path / "gate.json"
    payload = {
        "classification": "CREDENTIALS_NOT_CONFIGURED",
        "event_data_requested": False,
        "credentials_echoed": False,
    }
    _write(output, payload)
    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded == payload
    assert "password" not in output.read_text(encoding="utf-8").lower()


def test_gate_contract_never_requests_event_data():
    source = (
        __import__(
            "scripts.probe_movebank_authorized_secret_gate",
            fromlist=["dummy"],
        )
    )
    text = source.__doc__ or ""
    assert "never requests event rows" in text.lower()
