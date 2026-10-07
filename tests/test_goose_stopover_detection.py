from datetime import datetime, timedelta, timezone

import pytest

from src.goose_stopover_detection import (
    TrackPoint,
    detect_stopovers,
    haversine_km,
)


UTC = timezone.utc


def p(hours, lat, lon):
    return TrackPoint(
        datetime(2020, 1, 1, tzinfo=UTC) + timedelta(hours=hours),
        lat,
        lon,
    )


def test_haversine_is_zero_for_same_point():
    assert haversine_km(50, 5, 50, 5) == pytest.approx(0.0)


def test_stationary_residence_over_48h_is_one_stopover():
    points = [
        p(0, 50.0, 5.0),
        p(12, 50.01, 5.0),
        p(24, 50.0, 5.01),
        p(48, 50.01, 5.01),
        p(60, 50.0, 5.0),
        p(72, 52.0, 8.0),
        p(84, 53.0, 9.0),
    ]
    stops = detect_stopovers(points)
    assert len(stops) == 1
    assert stops[0].duration_hours >= 48.0


def test_one_outlier_inside_residence_is_allowed():
    points = [
        p(0, 50.0, 5.0),
        p(12, 50.01, 5.0),
        p(24, 52.0, 8.0),  # one outlier
        p(36, 50.0, 5.01),
        p(60, 50.01, 5.0),
        p(72, 53.0, 9.0),
        p(84, 54.0, 10.0),
    ]
    stops = detect_stopovers(points)
    assert len(stops) == 1
    assert stops[0].duration_hours == pytest.approx(60.0)


def test_two_outliers_terminate_candidate():
    points = [
        p(0, 50.0, 5.0),
        p(12, 50.01, 5.0),
        p(24, 52.0, 8.0),
        p(36, 53.0, 9.0),
    ]
    assert detect_stopovers(points) == ()


def test_short_residence_is_not_stopover():
    points = [
        p(0, 50.0, 5.0),
        p(12, 50.01, 5.0),
        p(24, 50.0, 5.01),
        p(36, 52.0, 8.0),
        p(48, 53.0, 9.0),
    ]
    assert detect_stopovers(points) == ()


def test_adjacent_subclusters_of_same_30km_site_are_merged():
    # Two candidate centers separated by less than 60 km and by <=48 h can
    # still be compatible with one underlying 30-km-radius site.
    points = [
        p(0, 50.0, 5.0),
        p(24, 50.0, 5.0),
        p(48, 50.0, 5.0),
        p(60, 51.5, 7.0),  # terminate first candidate
        p(72, 50.25, 5.0),
        p(96, 50.25, 5.0),
        p(120, 50.25, 5.0),
        p(132, 53.0, 9.0),
        p(144, 54.0, 10.0),
    ]
    stops = detect_stopovers(points)
    assert len(stops) == 1
    assert stops[0].start == points[0].timestamp
    assert stops[0].end == points[6].timestamp


def test_widely_separated_stays_are_not_merged():
    points = [
        p(0, 50.0, 5.0),
        p(24, 50.0, 5.0),
        p(48, 50.0, 5.0),
        p(60, 55.0, 10.0),
        p(72, 55.0, 10.0),
        p(96, 55.0, 10.0),
        p(120, 55.0, 10.0),
        p(132, 60.0, 15.0),
        p(144, 61.0, 16.0),
    ]
    stops = detect_stopovers(points)
    assert len(stops) == 2
