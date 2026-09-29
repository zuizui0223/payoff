import pandas as pd
import pytest

from src.movebank_event_hygiene import clean_movebank_gps_events


def row(
    *,
    t="2020-05-01 00:00:00.000",
    lon=-75.0,
    lat=60.0,
    individual=1,
    visible="true",
    tag=10,
):
    return {
        "timestamp": t,
        "location_long": lon,
        "location_lat": lat,
        "individual_id": individual,
        "individual_local_identifier": f"bird-{individual}",
        "tag_id": tag,
        "tag_local_identifier": f"tag-{tag}",
        "visible": visible,
    }


def test_visible_false_is_excluded_before_movepp():
    data = pd.DataFrame(
        [
            row(t="2020-05-01 00:00:00", visible="true"),
            row(t="2020-05-01 01:00:00", visible="false"),
        ]
    )
    clean, audit = clean_movebank_gps_events(data)
    assert len(clean) == 1
    assert audit.visible_true_retained == 1
    assert audit.visible_false_excluded == 1


def test_exact_duplicate_is_collapsed_and_audited():
    r = row()
    clean, audit = clean_movebank_gps_events(pd.DataFrame([r, r]))
    assert len(clean) == 1
    assert audit.exact_duplicates_collapsed == 1


def test_conflicting_same_individual_timestamp_fails_closed():
    data = pd.DataFrame(
        [
            row(lon=-75.0),
            row(lon=-74.9),
        ]
    )
    with pytest.raises(ValueError, match="conflicting Movebank rows"):
        clean_movebank_gps_events(data)


@pytest.mark.parametrize(
    "lon,lat",
    [
        (181.0, 60.0),
        (-181.0, 60.0),
        (-75.0, 91.0),
        (-75.0, -91.0),
        (float("nan"), 60.0),
    ],
)
def test_invalid_visible_coordinate_fails_closed(lon, lat):
    data = pd.DataFrame([row(lon=lon, lat=lat)])
    with pytest.raises(ValueError, match="invalid coordinate"):
        clean_movebank_gps_events(data)


def test_invalid_coordinate_on_invisible_row_is_not_primary_input():
    data = pd.DataFrame(
        [
            row(t="2020-05-01 00:00:00", lon=-75.0, visible="true"),
            row(
                t="2020-05-01 01:00:00",
                lon=999.0,
                visible="false",
            ),
        ]
    )
    clean, audit = clean_movebank_gps_events(data)
    assert len(clean) == 1
    assert audit.visible_false_excluded == 1


def test_output_is_sorted_and_movepp_named():
    data = pd.DataFrame(
        [
            row(t="2020-05-02 00:00:00", individual=2),
            row(t="2020-05-01 02:00:00", individual=1),
            row(t="2020-05-01 01:00:00", individual=1),
        ]
    )
    clean, audit = clean_movebank_gps_events(data)
    assert list(clean.columns[:4]) == ["individual", "time", "lon", "lat"]
    assert list(clean["individual"]) == ["1", "1", "2"]
    assert clean["time"].dt.tz is not None
    assert audit.year_counts == {2020: 3}


def test_unknown_visible_value_fails():
    with pytest.raises(ValueError, match="unrecognized Movebank visible"):
        clean_movebank_gps_events(pd.DataFrame([row(visible="maybe")]))
