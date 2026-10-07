import math

import pytest

from src.qb_local_observability import (
    PixelNDVI,
    RegionCenter,
    RegionComposite,
    aggregate_region_composites,
    build_appeears_manifest,
    build_region_lattice,
    fit_region_observability,
)


def test_lattice_has_center_plus_eight_fixed_radial_points():
    region = RegionCenter("x", "R1", 60.0, 10.0)
    points = build_region_lattice(region)
    assert len(points) == 9
    assert points[0].distance_km == pytest.approx(0.0)
    assert {p.bearing_degrees for p in points[1:]} == {
        0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0
    }


def test_manifest_is_year_scoped_and_environment_only():
    regions = [
        RegionCenter("a", "R1", 55.0, 5.0),
        RegionCenter("b", "R2", 65.0, 15.0),
    ]
    out = build_appeears_manifest(regions, years=[2001, 2002])
    assert out["region_count"] == 2
    assert out["total_points"] == 18
    assert out["task_count"] == 2
    assert out["environment_only"] is True
    assert all(row["cell_count"] == 18 for row in out["tasks"])


def test_region_composite_requires_five_quality_good_points():
    rows = [
        PixelNDVI("p1", "x:R1", 2001, 100, 0.1, True),
        PixelNDVI("p2", "x:R1", 2001, 100, 0.2, True),
        PixelNDVI("p3", "x:R1", 2001, 100, 0.3, True),
        PixelNDVI("p4", "x:R1", 2001, 100, 0.4, True),
        PixelNDVI("p5", "x:R1", 2001, 100, 0.5, True),
        PixelNDVI("p6", "x:R1", 2001, 100, 0.9, False),
    ]
    out = aggregate_region_composites(rows)
    assert len(out) == 1
    assert out[0].ndvi_median == pytest.approx(0.3)
    assert out[0].valid_points == 5


def _synthetic_region(region, slope, noise_scale):
    rows = []
    onset = {}
    for year in range(2001, 2010):
        onset[(region, year)] = 100.0
        for doy in (80, 88, 96, 104, 112, 120):
            tau = doy - 100.0
            noise = noise_scale * ((year + doy) % 3 - 1)
            rows.append(
                RegionComposite(
                    region_key=region,
                    year=year,
                    doy=doy,
                    ndvi_median=0.4 + 0.002 * (year - 2001) + slope * tau + noise,
                    valid_points=9,
                )
            )
    return rows, onset


def test_observability_recovers_higher_information_for_steeper_cleaner_curve():
    one, onset1 = _synthetic_region("x:R1", 0.01, 0.005)
    two, onset2 = _synthetic_region("x:R2", 0.004, 0.015)
    out = fit_region_observability(one + two, onset1 | onset2)
    by_region = {row.region_key: row for row in out}
    assert by_region["x:R1"].fisher_information > by_region["x:R2"].fisher_information
    assert by_region["x:R1"].q_b_z > by_region["x:R2"].q_b_z
    assert by_region["x:R1"].admitted_years == 9


def test_observability_fails_closed_when_year_support_is_too_low():
    rows, onset = _synthetic_region("x:R1", 0.01, 0.005)
    rows = [row for row in rows if row.year <= 2005]
    with pytest.raises(ValueError, match="admitted years"):
        fit_region_observability(rows, onset)
