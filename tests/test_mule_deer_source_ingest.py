from scripts.inspect_mule_deer_source_csv import (
    calibration_readiness,
    infer_grain,
    resolve_aliases,
)


def test_animal_year_summary_does_not_license_direct_tracking_inverse():
    headers = [
        "Animal_ID",
        "Year",
        "Migration_Distance",
        "Movement_Rate",
        "Start_Days_From_Peak",
        "End_Days_From_Peak",
    ]
    rows = [
        {
            "Animal_ID": "A",
            "Year": "2020",
            "Migration_Distance": "200",
            "Movement_Rate": "4",
            "Start_Days_From_Peak": "-20",
            "End_Days_From_Peak": "5",
        },
        {
            "Animal_ID": "B",
            "Year": "2020",
            "Migration_Distance": "220",
            "Movement_Rate": "5",
            "Start_Days_From_Peak": "10",
            "End_Days_From_Peak": "6",
        },
    ]
    resolved = resolve_aliases(headers)
    grain = infer_grain(rows, resolved)
    readiness = calibration_readiness(resolved, grain)

    assert grain["label"] == "animal_year_summary"
    assert readiness["route_summary_analysis_ready"]
    assert not readiness["movement_kernel_direct_inverse_ready"]
    assert not readiness["phenology_step_inverse_ready"]
    assert not readiness["full_direct_tracking_inverse_ready"]


def test_interval_level_table_can_license_direct_tracking_inverse():
    headers = [
        "animal_id",
        "year",
        "timestamp",
        "utm_x",
        "utm_y",
        "days_from_peak",
    ]
    rows = []
    for animal in ("A", "B"):
        for step in range(20):
            rows.append(
                {
                    "animal_id": animal,
                    "year": "2020",
                    "timestamp": f"2020-04-01T{step:02d}:00:00",
                    "utm_x": str(step * 100),
                    "utm_y": str(step * 20),
                    "days_from_peak": str(10 - step / 4),
                }
            )

    resolved = resolve_aliases(headers)
    grain = infer_grain(rows, resolved)
    readiness = calibration_readiness(resolved, grain)

    assert grain["label"] == "candidate_interval_or_gps_level"
    assert readiness["movement_kernel_direct_inverse_ready"]
    assert readiness["phenology_step_inverse_ready"]
    assert readiness["full_direct_tracking_inverse_ready"]


def test_geographic_lonlat_require_projection_before_movement_inverse():
    headers = [
        "animal_id",
        "year",
        "timestamp",
        "longitude",
        "latitude",
    ]
    rows = []
    for step in range(20):
        rows.append(
            {
                "animal_id": "A",
                "year": "2020",
                "timestamp": f"2020-04-{step+1:02d}",
                "longitude": str(-110 + step * 0.01),
                "latitude": str(42 + step * 0.001),
            }
        )

    resolved = resolve_aliases(headers)
    grain = infer_grain(rows, resolved)
    readiness = calibration_readiness(resolved, grain)

    assert not readiness["movement_kernel_direct_inverse_ready"]
    assert not readiness["phenology_step_inverse_ready"]
    assert not readiness["full_direct_tracking_inverse_ready"]
    assert any(
        "metric projection" in blocker
        for blocker in readiness["blockers"]
    )


def test_projected_metric_coordinates_can_license_movement_without_phenology():
    headers = [
        "animal_id",
        "year",
        "timestamp",
        "utm_x",
        "utm_y",
    ]
    rows = []
    for step in range(20):
        rows.append(
            {
                "animal_id": "A",
                "year": "2020",
                "timestamp": f"2020-04-{step+1:02d}",
                "utm_x": str(step * 100.0),
                "utm_y": str(step * 20.0),
            }
        )

    resolved = resolve_aliases(headers)
    grain = infer_grain(rows, resolved)
    readiness = calibration_readiness(resolved, grain)

    assert readiness["movement_kernel_direct_inverse_ready"]
    assert not readiness["phenology_step_inverse_ready"]
    assert not readiness["full_direct_tracking_inverse_ready"]
