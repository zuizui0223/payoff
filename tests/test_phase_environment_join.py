from datetime import datetime

import pytest

from src.phase_environment_join import (
    GPSPhaseKey,
    PeakIRGRecord,
    attach_peak_irg_to_gps,
)


def gps(obs_id, group, day, pixel):
    return GPSPhaseKey(
        observation_id=obs_id,
        animal_id=group + "_animal",
        animal_year=group + "_2020",
        group=group,
        timestamp=datetime(2020, 4, day, 12, 0, 0),
        pixel_id=pixel,
    )


def irg(pixel, product="MOD09Q1.006"):
    lane = (
        "study_faithful_v006"
        if product == "MOD09Q1.006"
        else "v061_sensitivity_only"
    )
    return PeakIRGRecord(
        pixel_id=pixel,
        year=2020,
        modis_product=product,
        reconstruction_lane=lane,
        peak_irg_date="2020-04-15",
    )


def test_environment_join_tracks_group_specific_coverage():
    audit = attach_peak_irg_to_gps(
        [
            gps("a1", "small", 1, "p1"),
            gps("a2", "small", 2, "p2"),
            gps("b1", "large", 1, "p1"),
        ],
        [
            irg("p1"),
        ],
    )

    assert audit.gps_observations == 3
    assert audit.matched_observations == 2
    assert audit.missing_observations == 1
    assert audit.matched_fraction == pytest.approx(2 / 3)
    assert dict(audit.matched_by_group) == {
        "large": 1,
        "small": 1,
    }
    assert dict(audit.missing_by_group) == {
        "small": 1,
    }


def test_environment_join_can_enforce_predeclared_coverage_threshold():
    with pytest.raises(ValueError, match="matched fraction"):
        attach_peak_irg_to_gps(
            [
                gps("a1", "small", 1, "p1"),
                gps("a2", "small", 2, "missing"),
            ],
            [irg("p1")],
            minimum_matched_fraction=0.9,
        )


def test_environment_join_rejects_duplicate_pixel_year_records():
    with pytest.raises(ValueError, match="duplicate"):
        attach_peak_irg_to_gps(
            [gps("a1", "small", 1, "p1")],
            [irg("p1"), irg("p1")],
        )


def test_environment_join_rejects_mixed_product_versions():
    with pytest.raises(ValueError, match="mix MODIS"):
        attach_peak_irg_to_gps(
            [
                gps("a1", "small", 1, "p1"),
                gps("a2", "small", 2, "p2"),
            ],
            [
                irg("p1", "MOD09Q1.006"),
                irg("p2", "MOD09Q1.061"),
            ],
        )


def test_required_product_treats_other_version_as_unmatched():
    audit = attach_peak_irg_to_gps(
        [
            gps("a1", "small", 1, "p1"),
            gps("a2", "small", 2, "p2"),
        ],
        [
            irg("p1", "MOD09Q1.006"),
            irg("p2", "MOD09Q1.061"),
        ],
        required_modis_product="MOD09Q1.006",
    )

    assert audit.matched_observations == 1
    assert audit.missing_observations == 1
    assert audit.products == ("MOD09Q1.006",)
    assert audit.reconstruction_lanes == (
        "study_faithful_v006",
    )


def test_peak_record_rejects_product_lane_disagreement():
    with pytest.raises(ValueError, match="disagree"):
        PeakIRGRecord(
            pixel_id="p1",
            year=2020,
            modis_product="MOD09Q1.061",
            reconstruction_lane="study_faithful_v006",
            peak_irg_date="2020-04-15",
        )


def test_primary_successor_v061_lane_is_valid_for_v061_product():
    record = PeakIRGRecord(
        pixel_id="p1",
        year=2020,
        modis_product="MOD09Q1.061",
        reconstruction_lane="v061_primary_successor_after_v006_decommission",
        peak_irg_date="2020-04-15",
    )
    audit = attach_peak_irg_to_gps(
        [gps("a1", "small", 1, "p1")],
        [record],
        required_modis_product="MOD09Q1.061",
        minimum_matched_fraction=1.0,
    )
    assert audit.matched_fraction == 1.0
    assert audit.reconstruction_lanes == (
        "v061_primary_successor_after_v006_decommission",
    )


def test_environment_join_can_audit_below_threshold_without_raising():
    audit = attach_peak_irg_to_gps(
        [
            gps("a1", "small", 1, "p1"),
            gps("a2", "small", 2, "missing"),
        ],
        [irg("p1")],
        minimum_matched_fraction=1.0,
        enforce_minimum=False,
    )
    assert audit.matched_fraction == pytest.approx(0.5)
    assert audit.missing_observations == 1
