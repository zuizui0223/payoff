import importlib.util
from datetime import date, timedelta
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "calibrate_wigeon_phase_error_era5land.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "calibrate_wigeon_era5land", SCRIPT
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
    def __init__(self, batch_payload, retry_payload):
        self.batch_payload = batch_payload
        self.retry_payload = retry_payload
        self.calls = []
        self.headers = {}

    def get(self, endpoint, *, params, timeout):
        self.calls.append((endpoint, params, timeout))
        payload = (
            self.batch_payload
            if len(self.calls) == 1
            else self.retry_payload
        )
        return FakeResponse(
            payload,
            endpoint + "?fake_call=" + str(len(self.calls)),
        )


def daily_payload(*, missing=False, latitude=55.0, longitude=8.0):
    start = date(2018, 1, 1)
    dates = [
        (start + timedelta(days=index)).isoformat()
        for index in range(212)
    ]
    if missing:
        temperatures = [None] * len(dates)
    else:
        temperatures = [0.0] * 60 + [10.0] * (len(dates) - 60)
    return {
        "latitude": latitude,
        "longitude": longitude,
        "elevation": 0.0,
        "daily": {
            "time": dates,
            "temperature_2m_mean": temperatures,
        },
    }


def test_batch_empty_event_is_retried_individually_without_changing_contract():
    pd = pytest.importorskip("pandas")
    module = load_module()

    staging = pd.DataFrame(
        [
            {
                "individual_id": "A",
                "year": 2018,
                "segment": 1,
                "arrival_doy": 100.0,
                "arrival_phase_days": 10.0,
                "tgs_onset_doy": 90.0,
                "lat": 55.5,
                "lon": 8.3,
            },
            {
                "individual_id": "B",
                "year": 2018,
                "segment": 1,
                "arrival_doy": 110.0,
                "arrival_phase_days": 20.0,
                "tgs_onset_doy": 90.0,
                "lat": 56.0,
                "lon": 9.0,
            },
        ]
    )
    session = FakeSession(
        [
            daily_payload(missing=True, latitude=55.5, longitude=8.3),
            daily_payload(missing=False, latitude=56.0, longitude=9.0),
        ],
        daily_payload(missing=False, latitude=55.5, longitude=8.3),
    )
    registration = {
        "replicate_environment_source": {
            "api_endpoint": "https://example.invalid/archive"
        }
    }

    events, request_log = module.extract_era5_events(
        staging,
        registration,
        batch_size=2,
        max_retries=1,
        sleep_seconds=0.0,
        session=session,
    )

    assert len(session.calls) == 2
    first_params = session.calls[0][1]
    retry_params = session.calls[1][1]

    # Scientific request contract is unchanged on retry.
    for key in (
        "start_date",
        "end_date",
        "daily",
        "models",
        "timezone",
        "cell_selection",
        "elevation",
        "temperature_unit",
    ):
        if key in ("timezone", "elevation"):
            continue
        assert retry_params[key] == first_params[key]
    assert retry_params["models"] == "era5_land"
    assert retry_params["cell_selection"] == "nearest"
    assert retry_params["start_date"] == "2018-01-01"
    assert retry_params["end_date"] == "2018-07-31"
    assert retry_params["latitude"] == "55.50000000"
    assert retry_params["longitude"] == "8.30000000"
    assert retry_params["timezone"] == "GMT"
    assert retry_params["elevation"] == "nan"

    by_id = {
        row.individual_id: row
        for row in events.itertuples(index=False)
    }
    assert by_id["A"].status == "PASS"
    assert by_id["A"].valid_daily_values == 212
    assert bool(by_id["A"].individual_retry_performed)
    assert by_id["B"].status == "PASS"
    assert not bool(by_id["B"].individual_retry_performed)

    assert len(request_log) == 2
    assert request_log[1]["request_kind"] == "single_location_retry"
    assert request_log[1]["event_identity"] == {
        "individual_id": "A",
        "year": 2018,
        "segment": 1,
    }
