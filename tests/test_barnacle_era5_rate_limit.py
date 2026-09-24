import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "calibrate_barnacle_phase_error_era5.py"

spec = importlib.util.spec_from_file_location("barnacle_era5_script", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class FakeResponse:
    def __init__(self, status_code, payload=None, headers=None):
        self.status_code = status_code
        self._payload = payload
        self.headers = headers or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"http {self.status_code}")

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def get(self, *args, **kwargs):
        self.calls += 1
        return self.responses.pop(0)


def one_day_payload():
    times = [f"1990-01-01T{hour:02d}:00" for hour in range(24)]
    return {
        "hourly": {
            "time": times,
            "temperature_2m": [10.0] * 24,
        }
    }


def test_retry_delay_prefers_retry_after_header():
    response = FakeResponse(429, headers={"Retry-After": "7"})
    assert module._retry_delay(response, 0) == 7.0


def test_retry_delay_caps_large_retry_after():
    response = FakeResponse(429, headers={"Retry-After": "999"})
    assert module._retry_delay(response, 0) == 60.0


def test_era5_request_recovers_after_rate_limit():
    session = FakeSession([
        FakeResponse(429, headers={"Retry-After": "0.01"}),
        FakeResponse(429),
        FakeResponse(200, payload=one_day_payload()),
    ])
    sleeps = []

    rows = module.request_era5_daily(
        session,
        "https://example.test/archive",
        64.0,
        36.0,
        1990,
        1990,
        max_attempts=5,
        sleep_fn=sleeps.append,
    )

    assert session.calls == 3
    assert rows == [("1990-01-01", 10.0)]
    assert sleeps[0] == pytest.approx(0.01)
    assert sleeps[1] == pytest.approx(10.0)
    assert sleeps[-1] == pytest.approx(0.5)


def test_era5_request_reports_attempt_count_after_exhaustion():
    session = FakeSession([
        FakeResponse(429),
        FakeResponse(429),
        FakeResponse(429),
    ])

    with pytest.raises(RuntimeError, match="after 3 attempts"):
        module.request_era5_daily(
            session,
            "https://example.test/archive",
            64.0,
            36.0,
            1990,
            1990,
            max_attempts=3,
            sleep_fn=lambda _: None,
        )

    assert session.calls == 3
