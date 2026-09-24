import importlib.util
from datetime import date, timedelta
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "diagnose_wigeon_era5land_coastal_mask.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "diagnose_wigeon_coastal_mask",
        SCRIPT,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload
        self.url = "https://example.invalid/archive?cell_selection=land"
        self.status_code = 200

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []
        self.headers = {}

    def get(self, endpoint, *, params, timeout):
        self.calls.append((endpoint, params, timeout))
        return FakeResponse(self.payload)


def daily_payload():
    start = date(2018, 1, 1)
    dates = [
        (start + timedelta(days=index)).isoformat()
        for index in range(212)
    ]
    return {
        "latitude": 55.6,
        "longitude": 8.4,
        "elevation": 3.0,
        "daily": {
            "time": dates,
            "temperature_2m_mean": (
                [0.0] * 60
                + [10.0] * (len(dates) - 60)
            ),
        },
    }


def test_posthoc_land_cell_diagnostic_never_changes_registered_nearest_contract():
    pd = pytest.importorskip("pandas")
    module = load_module()
    events = pd.DataFrame(
        [
            {
                "individual_id": "A",
                "year": 2018,
                "segment": 3,
                "arrival_doy": 110.0,
                "event_lat": 55.515522,
                "event_lon": 8.311833,
                "status": "INSUFFICIENT_JAN_JUL_DAILY_DATA",
                "reason": "valid_days=0",
            }
        ]
    )
    session = FakeSession(daily_payload())
    registration = {
        "replicate_environment_source": {
            "api_endpoint": "https://example.invalid/archive"
        }
    }

    diagnostic, request_log = module.diagnose_missing_events(
        events,
        registration,
        max_retries=1,
        sleep_seconds=0.0,
        session=session,
    )

    assert len(session.calls) == 1
    params = session.calls[0][1]
    assert params["models"] == "era5_land"
    assert params["start_date"] == "2018-01-01"
    assert params["end_date"] == "2018-07-31"
    assert params["cell_selection"] == "land"
    assert params["elevation"] == "nan"

    row = diagnostic.iloc[0]
    assert row["registered_nearest_status"] == (
        "INSUFFICIENT_JAN_JUL_DAILY_DATA"
    )
    assert row["diagnostic_cell_selection"] == "land"
    assert row["land_status"] == "PASS"
    assert row["land_valid_daily_values"] == 212
    assert request_log[0]["cell_selection"] == "land"


def test_diagnostic_queries_only_failed_primary_events():
    pd = pytest.importorskip("pandas")
    module = load_module()
    events = pd.DataFrame(
        [
            {
                "individual_id": "A",
                "year": 2018,
                "segment": 2,
                "arrival_doy": 100.0,
                "event_lat": 55.0,
                "event_lon": 8.0,
                "status": "PASS",
                "reason": None,
            },
            {
                "individual_id": "A",
                "year": 2018,
                "segment": 3,
                "arrival_doy": 110.0,
                "event_lat": 55.5,
                "event_lon": 8.3,
                "status": "INSUFFICIENT_JAN_JUL_DAILY_DATA",
                "reason": "valid_days=0",
            },
        ]
    )
    session = FakeSession(daily_payload())
    registration = {
        "replicate_environment_source": {
            "api_endpoint": "https://example.invalid/archive"
        }
    }
    diagnostic, _ = module.diagnose_missing_events(
        events,
        registration,
        max_retries=1,
        sleep_seconds=0.0,
        session=session,
    )
    assert len(diagnostic) == 1
    assert int(diagnostic.iloc[0]["segment"]) == 3
