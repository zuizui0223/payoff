from datetime import datetime, timedelta

from src.fixed_interval_gps_targets import (
    GPSObservation,
    select_fixed_interval_gps_targets,
)
from src.fixed_target_phase import (
    attach_phase_to_fixed_targets,
    build_adjacent_phase_pairs,
)
from src.phase_environment_join import PeakIRGRecord


def gps(obs, hour, pixel="p", group="small"):
    return GPSObservation(
        observation_id=obs,
        animal_id="A",
        animal_year="A_2020",
        group=group,
        timestamp=datetime(2020, 4, 1) + timedelta(hours=hour),
        pixel_id=pixel,
    )


def peak(pixel, day=1):
    return PeakIRGRecord(
        pixel_id=pixel,
        year=2020,
        modis_product="MOD09Q1.061",
        reconstruction_lane="v061_primary_successor_after_v006_decommission",
        peak_irg_date=f"2020-04-{day:02d}",
    )


def test_fixed_target_selection_happens_before_environmental_validity():
    selection = select_fixed_interval_gps_targets(
        [
            gps("o0", 0, "p0"),
            gps("near24", 23, "missing"),
            gps("far24", 26, "valid"),
            gps("o48", 48, "p48"),
        ],
        target_interval_seconds=24 * 3600,
        max_target_deviation_seconds=3 * 3600,
    )

    by_index = {
        row.target_index: row
        for row in selection.selected_targets
    }
    assert by_index[1].observation_id == "near24"

    audit = attach_phase_to_fixed_targets(
        selection.selected_targets,
        [peak("p0"), peak("valid"), peak("p48")],
        required_modis_product="MOD09Q1.061",
    )
    annotated = {
        row.target_index: row for row in audit.targets
    }

    assert annotated[1].observation_id == "near24"
    assert annotated[1].phase_valid is False
    assert all(row.observation_id != "far24" for row in audit.targets)


def test_invalid_environment_breaks_pair_chain_without_reselecting_gps():
    selection = select_fixed_interval_gps_targets(
        [
            gps("o0", 0, "p0"),
            gps("o24", 24, "missing"),
            gps("o48", 48, "p48"),
            gps("o72", 72, "p72"),
        ],
        target_interval_seconds=24 * 3600,
        max_target_deviation_seconds=3 * 3600,
    )
    audit = attach_phase_to_fixed_targets(
        selection.selected_targets,
        [peak("p0"), peak("p48"), peak("p72")],
        required_modis_product="MOD09Q1.061",
    )
    pairs = build_adjacent_phase_pairs(audit.targets)

    assert [(p.start_target_index, p.start_target_index + 1) for p in pairs] == [
        (2, 3)
    ]


def test_target_windows_are_anchored_to_earliest_raw_observation():
    start = datetime(2020, 4, 1, 5)
    observations = [
        GPSObservation("o0", "A", "A_2020", "small", start, "p0"),
        GPSObservation(
            "o1",
            "A",
            "A_2020",
            "small",
            start + timedelta(hours=25),
            "p1",
        ),
    ]
    selection = select_fixed_interval_gps_targets(
        observations,
        target_interval_seconds=24 * 3600,
        max_target_deviation_seconds=3 * 3600,
    )
    assert selection.selected_targets[0].target_timestamp == start
    assert selection.selected_targets[1].target_timestamp == (
        start + timedelta(hours=24)
    )
