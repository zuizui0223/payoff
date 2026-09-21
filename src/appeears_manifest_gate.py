"""Coverage gate for AppEEARS request manifests.

This gate prevents proxy geometries, accidental subsets, or missing
development groups/years from being submitted as the canonical Aikens
environmental extraction.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppEEARSCoverageExpectation:
    expected_gps_observations: int | None = None
    required_years: tuple[int, ...] = ()
    required_groups: tuple[str, ...] = ()
    exact_year_set: bool = False
    min_unique_cells: int = 1
    min_unique_cell_years: int = 1

    def __post_init__(self) -> None:
        if (
            self.expected_gps_observations is not None
            and self.expected_gps_observations <= 0
        ):
            raise ValueError(
                "expected_gps_observations must be positive when supplied"
            )
        if self.min_unique_cells <= 0:
            raise ValueError("min_unique_cells must be positive")
        if self.min_unique_cell_years <= 0:
            raise ValueError(
                "min_unique_cell_years must be positive"
            )
        if len(self.required_years) != len(set(self.required_years)):
            raise ValueError("required_years must be unique")
        if len(self.required_groups) != len(set(self.required_groups)):
            raise ValueError("required_groups must be unique")


@dataclass(frozen=True)
class AppEEARSCoverageGate:
    passed: bool
    gps_count_passed: bool
    year_coverage_passed: bool
    group_coverage_passed: bool
    cell_coverage_passed: bool
    observed_gps_observations: int
    observed_years: tuple[int, ...]
    observed_groups: tuple[str, ...]
    observed_unique_cells: int
    observed_unique_cell_years: int
    reasons: tuple[str, ...]


def evaluate_appeears_manifest_coverage(
    manifest: dict,
    expectation: AppEEARSCoverageExpectation,
) -> AppEEARSCoverageGate:
    """Evaluate whether a manifest can be treated as the canonical extraction."""

    if manifest.get("status") != "appeears_v061_sensitivity_manifest":
        raise ValueError(
            "manifest is not an AppEEARS V061 sensitivity manifest"
        )

    observed_gps = int(manifest.get("gps_observations", 0))
    observed_cells = int(
        manifest.get("unique_modis250_cells", 0)
    )
    observed_cell_years = int(
        manifest.get("unique_modis250_cell_years", 0)
    )
    observed_years = tuple(
        sorted(int(value) for value in manifest.get("years", []))
    )

    coverage = manifest.get("coverage") or {}
    group_counts = (
        coverage.get("gps_observations_by_group")
        or {}
    )
    observed_groups = tuple(
        sorted(
            str(group)
            for group, count in group_counts.items()
            if int(count) > 0
        )
    )

    reasons: list[str] = []

    if expectation.expected_gps_observations is None:
        gps_count_passed = observed_gps > 0
    else:
        gps_count_passed = (
            observed_gps
            == expectation.expected_gps_observations
        )
        if not gps_count_passed:
            reasons.append(
                "GPS observation count differs from frozen source expectation"
            )

    required_years = set(expectation.required_years)
    observed_year_set = set(observed_years)
    if expectation.exact_year_set:
        year_coverage_passed = observed_year_set == required_years
    else:
        year_coverage_passed = required_years.issubset(
            observed_year_set
        )
    if not year_coverage_passed:
        reasons.append(
            "manifest year coverage does not satisfy frozen expectation"
        )

    required_groups = set(expectation.required_groups)
    observed_group_set = set(observed_groups)
    group_coverage_passed = required_groups.issubset(
        observed_group_set
    )
    if not group_coverage_passed:
        reasons.append(
            "manifest development-group coverage is incomplete"
        )

    cell_coverage_passed = (
        observed_cells >= expectation.min_unique_cells
        and observed_cell_years
        >= expectation.min_unique_cell_years
    )
    if not cell_coverage_passed:
        reasons.append(
            "manifest MODIS cell coverage is below frozen minimum"
        )

    passed = (
        gps_count_passed
        and year_coverage_passed
        and group_coverage_passed
        and cell_coverage_passed
    )

    return AppEEARSCoverageGate(
        passed=passed,
        gps_count_passed=gps_count_passed,
        year_coverage_passed=year_coverage_passed,
        group_coverage_passed=group_coverage_passed,
        cell_coverage_passed=cell_coverage_passed,
        observed_gps_observations=observed_gps,
        observed_years=observed_years,
        observed_groups=observed_groups,
        observed_unique_cells=observed_cells,
        observed_unique_cell_years=observed_cell_years,
        reasons=tuple(reasons),
    )


def canonical_aikens_coverage_expectation() -> AppEEARSCoverageExpectation:
    """Frozen movement-source identity for the Aikens spring-migration archive."""

    return AppEEARSCoverageExpectation(
        expected_gps_observations=64539,
        required_years=(
            2005,
            2006,
            2008,
            2009,
            2010,
            2015,
            2016,
            2017,
            2018,
        ),
        required_groups=("large", "small"),
        exact_year_set=True,
        min_unique_cells=1,
        min_unique_cell_years=1,
    )
