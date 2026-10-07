from datetime import datetime, timedelta, timezone

import pytest

from src.goose_route_timing import (
    remaining_schedule_from_stopovers,
    remaining_schedule_to_curated_arrival,
    select_breeding_endpoint,
)
from src.goose_stopover_detection import Stopover


UTC = timezone.utc


def stop(start_day, duration_days, lat=70.0, lon=20.0, month=5):
    start = datetime(2020, month, start_day, tzinfo=UTC)
    return Stopover(
        start=start,
        end=start + timedelta(days=duration_days),
        center_latitude=lat,
        center_longitude=lon,
        inlier_points=20,
    )


def test_last_7_to_26_day_stop_before_end_june_is_breeding_endpoint():
    stops = [
        stop(1, 4, month=4),
        stop(10, 9, month=5),
        stop(5, 12, month=6),
    ]
    out = select_breeding_endpoint(stops, year=2020)
    assert out is not None
    assert out.stopover_index == 2
    assert out.residence_days == pytest.approx(12.0)


def test_breeding_stay_can_extend_into_july_if_reached_before_end_june():
    stops = [
        stop(25, 15, month=6),
    ]
    out = select_breeding_endpoint(stops, year=2020)
    assert out is not None
    assert out.arrival.month == 6
    assert out.departure.month == 7


def test_stop_arriving_after_june_is_not_breeding_endpoint():
    july = Stopover(
        start=datetime(2020, 7, 1, tzinfo=UTC),
        end=datetime(2020, 7, 10, tzinfo=UTC),
        center_latitude=70,
        center_longitude=20,
        inlier_points=20,
    )
    assert select_breeding_endpoint([july], year=2020) is None


def test_residence_outside_7_to_26_days_does_not_qualify():
    stops = [
        stop(1, 6, month=6),
        stop(10, 27, month=5),
    ]
    assert select_breeding_endpoint(stops, year=2020) is None


def test_remaining_schedule_uses_departure_to_breeding_arrival():
    first = Stopover(
        start=datetime(2020, 4, 1, tzinfo=UTC),
        end=datetime(2020, 4, 4, tzinfo=UTC),
        center_latitude=50,
        center_longitude=5,
        inlier_points=20,
    )
    second = Stopover(
        start=datetime(2020, 5, 1, tzinfo=UTC),
        end=datetime(2020, 5, 5, tzinfo=UTC),
        center_latitude=60,
        center_longitude=10,
        inlier_points=20,
    )
    breeding_stop = Stopover(
        start=datetime(2020, 6, 1, tzinfo=UTC),
        end=datetime(2020, 6, 11, tzinfo=UTC),
        center_latitude=70,
        center_longitude=20,
        inlier_points=20,
    )
    stops = [first, second, breeding_stop]
    breeding = select_breeding_endpoint(stops, year=2020)
    assert breeding is not None
    rows = remaining_schedule_from_stopovers(stops, breeding)
    assert len(rows) == 2
    assert rows[0].remaining_days == pytest.approx(58.0)
    assert rows[1].remaining_days == pytest.approx(27.0)


def test_breeding_stop_itself_is_not_a_remaining_schedule_stage():
    breeding_stop = stop(1, 10, month=6)
    breeding = select_breeding_endpoint([breeding_stop], year=2020)
    assert breeding is not None
    assert remaining_schedule_from_stopovers([breeding_stop], breeding) == ()



def test_does_not_fall_back_to_earlier_staging_site_when_last_site_is_too_long():
    earlier = Stopover(
        start=datetime(2020, 5, 1, tzinfo=UTC),
        end=datetime(2020, 5, 16, tzinfo=UTC),
        center_latitude=65.5,
        center_longitude=-20.0,
        inlier_points=20,
    )
    arctic_long_stay = Stopover(
        start=datetime(2020, 5, 25, tzinfo=UTC),
        end=datetime(2020, 7, 20, tzinfo=UTC),
        center_latitude=74.0,
        center_longitude=-24.0,
        inlier_points=100,
    )
    assert (
        select_breeding_endpoint(
            [earlier, arctic_long_stay],
            year=2020,
        )
        is None
    )



def test_curated_arrival_is_independent_of_later_detected_long_cluster():
    first = Stopover(
        start=datetime(2020, 5, 1, tzinfo=UTC),
        end=datetime(2020, 5, 10, tzinfo=UTC),
        center_latitude=65,
        center_longitude=10,
        inlier_points=20,
    )
    last_staging = Stopover(
        start=datetime(2020, 5, 15, tzinfo=UTC),
        end=datetime(2020, 5, 20, tzinfo=UTC),
        center_latitude=68,
        center_longitude=20,
        inlier_points=20,
    )
    broad_arctic_cluster = Stopover(
        start=datetime(2020, 5, 25, tzinfo=UTC),
        end=datetime(2020, 7, 20, tzinfo=UTC),
        center_latitude=75,
        center_longitude=25,
        inlier_points=100,
    )
    curated = datetime(2020, 5, 25, tzinfo=UTC)
    rows = remaining_schedule_to_curated_arrival(
        [first, last_staging, broad_arctic_cluster],
        breeding_arrival=curated,
    )
    assert len(rows) == 2
    assert rows[-1].remaining_days == pytest.approx(5.0)
    assert all(row.breeding_arrival == curated for row in rows)
