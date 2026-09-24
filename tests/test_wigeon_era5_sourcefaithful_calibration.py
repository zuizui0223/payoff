import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "calibrate_wigeon_phase_error_era5.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "calibrate_wigeon_era5", SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, payload, url):
        self._payload = payload
        self.url = url
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
        return FakeResponse(
            self.payload,
            endpoint + "?fake=1",
        )


def hourly_payload(*, latitude=55.0, longitude=8.0):
    start = datetime(2018, 1, 1, tzinfo=timezone.utc)
    timestamps = []
    temperatures = []
    for hour in range(212 * 24):
        ts = start + timedelta(hours=hour)
        timestamps.append(ts.strftime("%Y-%m-%dT%H:%M"))
        day_index = hour // 24
        temperatures.append(0.0 if day_index < 60 else 10.0)
    return {
        "latitude": latitude,
        "longitude": longitude,
        "elevation": 0.0,
        "hourly": {
            "time": timestamps,
            "temperature_2m": temperatures,
        },
    }


def test_era5_request_is_hourly_source_faithful_and_daily_mean_is_local():
    pd = pytest.importorskip("pandas")
    module = load_module()

    staging = pd.DataFrame(
        [
            {
                "individual_id": "A",
                "year": 2018,
                "segment": 1,
                "arrival_doy": 100.0,
                "arrival_phase_days": 40.0,
                "tgs_onset_doy": 60.0,
                "lat": 55.5,
                "lon": 8.3,
            }
        ]
    )
    session = FakeSession(hourly_payload(latitude=55.5, longitude=8.3))
    registration = {
        "replicate_environment_source": {
            "api_endpoint": "https://example.invalid/archive"
        }
    }

    events, request_log = module.extract_era5_events(
        staging,
        registration,
        batch_size=1,
        max_retries=1,
        sleep_seconds=0.0,
        session=session,
    )

    assert len(session.calls) == 1
    params = session.calls[0][1]
    assert params["models"] == "era5"
    assert params["hourly"] == "temperature_2m"
    assert "daily" not in params
    assert params["timezone"] == "GMT"
    assert params["cell_selection"] == "nearest"
    assert params["elevation"] == "nan"
    assert params["start_date"] == "2018-01-01"
    assert params["end_date"] == "2018-07-31"

    row = events.iloc[0]
    assert row["status"] == "PASS"
    assert row["valid_daily_values"] == 212
    assert row["era5_tgs_onset_doy"] == 60
    assert row["era5_phase_days"] == pytest.approx(40.0)
    assert len(request_log) == 1


def test_hourly_aggregation_requires_exactly_24_finite_values_per_day():
    module = load_module()
    payload = hourly_payload()
    payload["hourly"]["temperature_2m"][3] = None
    daily = module.finite_daily_pairs(payload)
    assert len(daily) == 211
    assert daily[0][0] == "2018-01-02"
