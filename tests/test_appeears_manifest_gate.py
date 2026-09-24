from src.appeears_manifest_gate import (
    AppEEARSCoverageExpectation,
    canonical_aikens_coverage_expectation,
    evaluate_appeears_manifest_coverage,
)


def manifest(
    *,
    gps=64539,
    years=(2005, 2006, 2008, 2009, 2010, 2015, 2016, 2017, 2018),
    groups=("small", "large"),
    cells=12000,
    cell_years=21000,
):
    return {
        "status": "appeears_v061_sensitivity_manifest",
        "gps_observations": gps,
        "unique_modis250_cells": cells,
        "unique_modis250_cell_years": cell_years,
        "years": list(years),
        "coverage": {
            "gps_observations_by_group": {
                group: 1 for group in groups
            }
        },
    }


def test_canonical_aikens_manifest_identity_passes():
    gate = evaluate_appeears_manifest_coverage(
        manifest(),
        canonical_aikens_coverage_expectation(),
    )

    assert gate.passed
    assert gate.gps_count_passed
    assert gate.year_coverage_passed
    assert gate.group_coverage_passed
    assert gate.cell_coverage_passed
    assert gate.reasons == ()


def test_step_midpoint_proxy_count_is_rejected_as_final_manifest():
    gate = evaluate_appeears_manifest_coverage(
        manifest(gps=64286),
        canonical_aikens_coverage_expectation(),
    )

    assert not gate.passed
    assert not gate.gps_count_passed
    assert any("GPS observation count" in reason for reason in gate.reasons)


def test_missing_large_development_group_is_rejected():
    gate = evaluate_appeears_manifest_coverage(
        manifest(groups=("small",)),
        canonical_aikens_coverage_expectation(),
    )

    assert not gate.passed
    assert not gate.group_coverage_passed
    assert any("group coverage" in reason for reason in gate.reasons)


def test_missing_year_is_rejected_under_exact_year_contract():
    gate = evaluate_appeears_manifest_coverage(
        manifest(
            years=(2005, 2006, 2008, 2009, 2010, 2015, 2016, 2017)
        ),
        canonical_aikens_coverage_expectation(),
    )

    assert not gate.passed
    assert not gate.year_coverage_passed


def test_generic_manifest_can_use_subset_year_requirement():
    gate = evaluate_appeears_manifest_coverage(
        manifest(
            gps=100,
            years=(2020, 2021),
            groups=("A",),
            cells=10,
            cell_years=20,
        ),
        AppEEARSCoverageExpectation(
            expected_gps_observations=100,
            required_years=(2020,),
            required_groups=("A",),
            exact_year_set=False,
            min_unique_cells=5,
            min_unique_cell_years=10,
        ),
    )

    assert gate.passed


def test_wrong_manifest_type_is_rejected():
    wrong = manifest()
    wrong["status"] = "not_appeears"
    try:
        evaluate_appeears_manifest_coverage(
            wrong,
            canonical_aikens_coverage_expectation(),
        )
    except ValueError as exc:
        assert "not an AppEEARS" in str(exc)
    else:
        raise AssertionError("expected ValueError")
