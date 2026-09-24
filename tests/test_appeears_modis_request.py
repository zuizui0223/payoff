from datetime import datetime

import pytest

from src.appeears_modis_request import (
    ProjectedGPSObservation,
    build_appeears_v061_tasks,
    deduplicate_to_modis_250m_cells,
)


pytest.importorskip("pyproj")


def observation(
    observation_id,
    x,
    y,
    *,
    year=2020,
    animal_id="A",
    animal_year="A_2020",
    group="small",
):
    return ProjectedGPSObservation(
        observation_id=observation_id,
        animal_id=animal_id,
        animal_year=animal_year,
        group=group,
        timestamp=datetime(year, 4, 1, 12, 0, 0),
        x=x,
        y=y,
    )


def test_deduplication_collapses_nearby_projected_points_to_same_modis_cell():
    rows = (
        observation("o1", 500000.0, 4700000.0),
        observation("o2", 500010.0, 4700010.0),
        observation("o3", 501000.0, 4700000.0),
    )
    dedup = deduplicate_to_modis_250m_cells(
        rows,
        source_crs="EPSG:32613",
    )

    assert dedup.gps_observations == 3
    assert dedup.unique_cells <= 3
    assert dedup.unique_cells >= 2
    assert dedup.unique_cell_years == dedup.unique_cells
    assert 0.0 < dedup.compression_ratio <= 1.0
    assert len(dedup.links) == 3


def test_cell_year_count_distinguishes_same_cell_in_multiple_years():
    rows = (
        observation("o1", 500000.0, 4700000.0, year=2020),
        observation(
            "o2",
            500000.0,
            4700000.0,
            year=2021,
            animal_year="A_2021",
        ),
    )
    dedup = deduplicate_to_modis_250m_cells(
        rows,
        source_crs="EPSG:32613",
    )

    assert dedup.unique_cells == 1
    assert dedup.unique_cell_years == 2


def test_appeears_manifest_is_year_scoped_and_chunked():
    rows = (
        observation("o1", 500000.0, 4700000.0, year=2020),
        observation("o2", 501000.0, 4700000.0, year=2020),
        observation(
            "o3",
            500000.0,
            4700000.0,
            year=2021,
            animal_year="A_2021",
        ),
    )
    dedup = deduplicate_to_modis_250m_cells(
        rows,
        source_crs="EPSG:32613",
    )
    manifest = build_appeears_v061_tasks(
        dedup,
        task_prefix="test_task",
        max_points_per_task=1,
    )

    assert manifest["reconstruction_lane"] == "v061_sensitivity_only"
    assert manifest["years"] == [2020, 2021]
    assert manifest["task_count"] == dedup.unique_cell_years
    assert manifest["operational_max_points_per_task"] == 1

    for task_row in manifest["tasks"]:
        task = task_row["task"]
        assert task["task_type"] == "point"
        assert task["task_name"].startswith("test_task_")
        assert task_row["cell_count"] == 1
        assert len(task["params"]["coordinates"]) == 1
        assert len(task["params"]["layers"]) == 6
        assert task["params"]["dates"][0]["startDate"].endswith(
            str(task_row["year"])
        )


def test_manifest_never_claims_study_faithful_v006():
    rows = (
        observation("o1", 500000.0, 4700000.0),
    )
    dedup = deduplicate_to_modis_250m_cells(
        rows,
        source_crs="EPSG:32613",
    )
    manifest = build_appeears_v061_tasks(dedup)

    assert manifest["status"] == "appeears_v061_sensitivity_manifest"
    assert "V061" in manifest["claim_boundary"]
    assert "study-faithful" in manifest["claim_boundary"]
