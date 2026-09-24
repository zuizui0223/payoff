from datetime import datetime, timedelta

import pytest

from src.fixed_interval_phase_pairs import (
    PhaseLocation,
    reconstruct_fixed_interval_phase_pairs,
)


def loc(
    hour,
    *,
    peak_hour=24,
    animal="A",
    animal_year="A_2020",
    group="small",
):
    origin = datetime(2020, 4, 1, 0, 0, 0)
    return PhaseLocation(
        animal_id=animal,
        animal_year=animal_year,
        group=group,
        timestamp=origin + timedelta(hours=hour),
        local_peak_timestamp=origin + timedelta(hours=peak_hour),
    )


def test_exact_daily_grid_builds_adjacent_phase_pairs():
    rows = [
        loc(0, peak_hour=24),
        loc(24, peak_hour=24),
        loc(48, peak_hour=24),
    ]
    result = reconstruct_fixed_interval_phase_pairs(
        rows,
        target_interval_seconds=86400.0,
        max_target_deviation_seconds=10800.0,
    )

    assert result.matched_phase_points == 3
    assert len(result.phase_pairs) == 2
    assert result.phase_pairs[0].phase_before == pytest.approx(-1.0)
    assert result.phase_pairs[0].phase_after == pytest.approx(0.0)
    assert result.phase_pairs[1].phase_before == pytest.approx(0.0)
    assert result.phase_pairs[1].phase_after == pytest.approx(1.0)


def test_nearest_fix_within_three_hours_is_accepted():
    rows = [
        loc(0),
        loc(26),
        loc(48),
    ]
    result = reconstruct_fixed_interval_phase_pairs(
        rows,
        target_interval_seconds=86400.0,
        max_target_deviation_seconds=10800.0,
    )

    assert len(result.phase_pairs) == 2
    # The 24-hour target uses the fix at hour 26.
    assert result.phase_pairs[0].phase_after == pytest.approx(2.0 / 24.0)


def test_fix_outside_tolerance_creates_gap_and_does_not_stretch_pair():
    rows = [
        loc(0),
        loc(29),
        loc(48),
        loc(72),
    ]
    result = reconstruct_fixed_interval_phase_pairs(
        rows,
        target_interval_seconds=86400.0,
        max_target_deviation_seconds=10800.0,
    )

    # Target index 1 (24 h) is missing because the nearest fix is 5 h away.
    # Therefore no 0->48 h stretched pair is created.
    assert len(result.phase_pairs) == 1
    pair = result.phase_pairs[0]
    assert pair.start_target_index == 2
    assert (
        pair.end_timestamp - pair.start_timestamp
    ).total_seconds() == pytest.approx(86400.0)


def test_target_windows_must_not_overlap():
    with pytest.raises(ValueError, match="must not overlap"):
        reconstruct_fixed_interval_phase_pairs(
            [loc(0), loc(24)],
            target_interval_seconds=86400.0,
            max_target_deviation_seconds=43200.0,
        )


def test_animal_year_cannot_mix_population_groups():
    rows = [
        loc(0, group="small"),
        loc(24, group="large"),
    ]
    with pytest.raises(ValueError, match="multiple groups"):
        reconstruct_fixed_interval_phase_pairs(rows)


def test_animal_year_cannot_mix_animal_ids():
    rows = [
        loc(0, animal="A"),
        loc(24, animal="B"),
    ]
    with pytest.raises(ValueError, match="multiple animal IDs"):
        reconstruct_fixed_interval_phase_pairs(rows)


def test_multiple_animal_years_are_reconstructed_independently():
    rows = [
        loc(0, animal="A", animal_year="A_2020", group="small"),
        loc(24, animal="A", animal_year="A_2020", group="small"),
        loc(
            5,
            animal="B",
            animal_year="B_2020",
            group="large",
            peak_hour=29,
        ),
        loc(
            29,
            animal="B",
            animal_year="B_2020",
            group="large",
            peak_hour=29,
        ),
    ]
    result = reconstruct_fixed_interval_phase_pairs(rows)

    assert result.animal_years_seen == 2
    assert result.animal_years_with_pairs == 2
    assert len(result.phase_pairs) == 2
    assert set(result.groups) == {"small", "large"}
