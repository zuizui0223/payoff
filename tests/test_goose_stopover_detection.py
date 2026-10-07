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


def test_pairwise_cluster_can_move_more_than_30km_from_first_anchor():
    # Consecutive displacements are <30 km, although the final point is more
    # than 30 km from the first. This is the van-Wijk successive-position rule.
    points = [
        p(0, 50.00, 5.00),
        p(12, 50.18, 5.00),
        p(24, 50.36, 5.00),
        p(36, 50.54, 5.00),
        p(60, 50.72, 5.00),
        p(72, 54.0, 10.0),
    ]
    assert haversine_km(
        points[0].latitude,
        points[0].longitude,
        points[4].latitude,
        points[4].longitude,
    ) > 30
    stops = detect_stopovers(points)
    assert len(stops) == 1
    assert stops[0].duration_hours == pytest.approx(60.0)


def test_one_short_detour_and_return_is_allowed():
    points = [
        p(0, 50.0, 5.0),
        p(12, 50.01, 5.0),
        p(15, 52.0, 8.0),  # detour >30 km
        p(18, 50.0, 5.01),  # returned within 6 h of last in-cluster point
        p(36, 50.01, 5.0),
        p(60, 50.0, 5.0),
        p(72, 53.0, 9.0),
    ]
    stops = detect_stopovers(points)
    assert len(stops) == 1
    assert stops[0].duration_hours == pytest.approx(60.0)
    assert stops[0].detour_points == 1


def test_detour_return_after_eight_hours_terminates_cluster():
    points = [
        p(0, 50.0, 5.0),
        p(24, 50.01, 5.0),
        p(30, 52.0, 8.0),
        p(36, 50.0, 5.01),  # 12 h since last in-cluster fix
        p(60, 50.01, 5.0),
    ]
    assert detect_stopovers(points) == ()


def test_second_detour_terminates_existing_stopover():
    points = [
        p(0, 50.0, 5.0),
        p(12, 50.01, 5.0),
        p(15, 52.0, 8.0),
        p(18, 50.0, 5.01),  # first detour returns
        p(36, 50.01, 5.0),
        p(54, 50.0, 5.0),
        p(57, 52.0, 8.0),   # second detour ends site
        p(60, 50.0, 5.0),
    ]
    stops = detect_stopovers(points)
    assert len(stops) == 1
    assert stops[0].end == points[5].timestamp
    assert stops[0].detour_points == 1


def test_short_residence_is_not_stopover():
    points = [
        p(0, 50.0, 5.0),
        p(12, 50.01, 5.0),
        p(24, 50.0, 5.01),
        p(36, 52.0, 8.0),
        p(48, 53.0, 9.0),
    ]
    assert detect_stopovers(points) == ()


def test_two_spatially_separate_long_clusters_are_two_stopovers():
    points = [
        p(0, 50.0, 5.0),
        p(24, 50.0, 5.0),
        p(48, 50.0, 5.0),
        p(60, 55.0, 10.0),
        p(84, 55.0, 10.0),
        p(108, 55.0, 10.0),
        p(120, 60.0, 15.0),
    ]
    stops = detect_stopovers(points)
    assert len(stops) == 2
    assert stops[0].center_latitude == pytest.approx(50.0)
    assert stops[1].center_latitude == pytest.approx(55.0)


def test_six_hour_sensitivity_can_be_declared_without_changing_other_rules():
    points = [
        p(0, 50.0, 5.0),
        p(24, 50.0, 5.0),
        p(27, 52.0, 8.0),
        p(31, 50.0, 5.0),  # return 7 h after previous inlier
        p(48, 50.0, 5.0),
        p(72, 50.0, 5.0),
        p(84, 53.0, 9.0),
    ]
    assert len(detect_stopovers(points, maximum_detour_hours=8)) == 1
    # With the closely related De Boer 6-h variant the detour does not qualify.
    assert detect_stopovers(points, maximum_detour_hours=6) == ()
