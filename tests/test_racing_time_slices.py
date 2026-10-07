from datetime import datetime, timedelta, timezone

import pytest

from src.racing_time_slices import (
    OddsSnapshot,
    select_last_preclose_slice,
    select_primary_time_slices,
    select_target_slice,
)


def _snapshot(post, minutes, a=2.0, b=3.0):
    return OddsSnapshot(
        observed_at=post - timedelta(minutes=minutes),
        decimal_odds={"A": a, "B": b},
    )


def test_target_slice_never_uses_future_snapshot():
    post = datetime(2026, 10, 4, 15, 40, tzinfo=timezone.utc)
    snaps = [
        _snapshot(post, 35),
        _snapshot(post, 28),
    ]
    out = select_target_slice(
        post_time=post,
        snapshots=snaps,
        minutes_before_post=30,
        max_staleness_minutes=10,
    )
    assert out is not None
    assert out.observed_at == post - timedelta(minutes=35)
    assert out.staleness_minutes == pytest.approx(5.0)


def test_target_slice_fails_when_previous_snapshot_is_too_stale():
    post = datetime(2026, 10, 4, 15, 40)
    snaps = [_snapshot(post, 45), _snapshot(post, 20)]
    out = select_target_slice(
        post_time=post,
        snapshots=snaps,
        minutes_before_post=30,
        max_staleness_minutes=10,
    )
    assert out is None


def test_last_is_latest_strictly_pre_post_snapshot():
    post = datetime(2026, 10, 4, 15, 40)
    snaps = [_snapshot(post, 10), _snapshot(post, 3), _snapshot(post, 6)]
    out = select_last_preclose_slice(post_time=post, snapshots=snaps)
    assert out.label == "LAST"
    assert out.observed_at == post - timedelta(minutes=3)


def test_complete_primary_panel_requires_every_target():
    post = datetime(2026, 10, 4, 15, 40)
    snaps = [
        _snapshot(post, 65),
        _snapshot(post, 60),
        _snapshot(post, 35),
        _snapshot(post, 30),
        _snapshot(post, 20),
        _snapshot(post, 15),
        _snapshot(post, 10),
        _snapshot(post, 5),
        _snapshot(post, 2),
    ]
    out = select_primary_time_slices(
        post_time=post,
        snapshots=snaps,
        max_staleness_minutes=10,
    )
    assert out is not None
    assert set(out) == {"T-30", "T-15", "T-10", "T-5", "LAST"}


def test_timezone_awareness_mismatch_fails_closed():
    aware_post = datetime(2026, 10, 4, 15, 40, tzinfo=timezone.utc)
    naive_snap = OddsSnapshot(
        observed_at=datetime(2026, 10, 4, 15, 30),
        decimal_odds={"A": 2.0, "B": 3.0},
    )
    with pytest.raises(ValueError, match="timezone awareness"):
        select_last_preclose_slice(
            post_time=aware_post,
            snapshots=[naive_snap],
        )
