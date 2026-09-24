"""Fit the preregistered Aikens within-taxon lambda contrast from phase pairs.

Model:

    E_next
    ~ E_current
      + E_current : large_development
      + animal_year fixed effects

Uncertainty is clustered by animal ID.

The implementation mirrors the frozen Aikens preregistration. It is an
optional empirical layer and loads numpy/statsmodels lazily.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class PhasePairRecord:
    animal_id: str
    animal_year: str
    group: str
    phase_before: float
    phase_after: float

    def __post_init__(self) -> None:
        for name in ("animal_id", "animal_year", "group"):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")
        if not isfinite(self.phase_before):
            raise ValueError("phase_before must be finite")
        if not isfinite(self.phase_after):
            raise ValueError("phase_after must be finite")


@dataclass(frozen=True)
class PhaseContrastSupport:
    group_a_pairs: int
    group_b_pairs: int
    group_a_animals: int
    group_b_animals: int
    group_a_animal_years: int
    group_b_animal_years: int


@dataclass(frozen=True)
class PhaseRetentionContrastFit:
    estimable: bool
    support: PhaseContrastSupport
    total_pairs: int
    total_animals: int
    total_animal_years: int
    lambda_a: float | None
    lambda_a_se: float | None
    lambda_b: float | None
    lambda_b_se: float | None
    delta_lambda_b_minus_a: float | None
    delta_lambda_se: float | None
    p_difference: float | None
    reasons: tuple[str, ...]


def _load_empirical_dependencies():
    try:
        import numpy as np
        import statsmodels.api as sm
    except ImportError as exc:
        raise RuntimeError(
            "phase-retention contrast fitting requires the optional "
            "empirical dependency group"
        ) from exc
    return np, sm


def _support(
    rows: tuple[PhasePairRecord, ...],
    *,
    group_a_value: str,
    group_b_value: str,
) -> PhaseContrastSupport:
    a = tuple(row for row in rows if row.group == group_a_value)
    b = tuple(row for row in rows if row.group == group_b_value)
    return PhaseContrastSupport(
        group_a_pairs=len(a),
        group_b_pairs=len(b),
        group_a_animals=len({row.animal_id for row in a}),
        group_b_animals=len({row.animal_id for row in b}),
        group_a_animal_years=len(
            {row.animal_year for row in a}
        ),
        group_b_animal_years=len(
            {row.animal_year for row in b}
        ),
    )


def fit_phase_retention_contrast(
    records: Iterable[PhasePairRecord],
    *,
    group_a_value: str,
    group_b_value: str,
    min_animals_per_group: int = 10,
    min_pairs_per_group: int = 100,
) -> PhaseRetentionContrastFit:
    """Fit the frozen group-B versus group-A phase-retention contrast."""

    if not group_a_value.strip() or not group_b_value.strip():
        raise ValueError("group values must be non-empty")
    if group_a_value == group_b_value:
        raise ValueError("group_a_value and group_b_value must differ")
    if min_animals_per_group <= 0:
        raise ValueError("min_animals_per_group must be positive")
    if min_pairs_per_group <= 0:
        raise ValueError("min_pairs_per_group must be positive")

    rows = tuple(
        row
        for row in records
        if row.group in (group_a_value, group_b_value)
    )
    if not rows:
        raise ValueError("no records belong to the target groups")

    support = _support(
        rows,
        group_a_value=group_a_value,
        group_b_value=group_b_value,
    )

    reasons: list[str] = []
    if support.group_a_animals < min_animals_per_group:
        reasons.append("group_a animal support below frozen minimum")
    if support.group_b_animals < min_animals_per_group:
        reasons.append("group_b animal support below frozen minimum")
    if support.group_a_pairs < min_pairs_per_group:
        reasons.append("group_a transition support below frozen minimum")
    if support.group_b_pairs < min_pairs_per_group:
        reasons.append("group_b transition support below frozen minimum")

    total_animals = len({row.animal_id for row in rows})
    total_animal_years = len(
        {row.animal_year for row in rows}
    )

    if reasons:
        return PhaseRetentionContrastFit(
            estimable=False,
            support=support,
            total_pairs=len(rows),
            total_animals=total_animals,
            total_animal_years=total_animal_years,
            lambda_a=None,
            lambda_a_se=None,
            lambda_b=None,
            lambda_b_se=None,
            delta_lambda_b_minus_a=None,
            delta_lambda_se=None,
            p_difference=None,
            reasons=tuple(reasons),
        )

    np, sm = _load_empirical_dependencies()

    animal_years = sorted(
        {row.animal_year for row in rows}
    )
    baseline_year = animal_years[0]
    dummy_years = animal_years[1:]

    x_rows = []
    y = []
    clusters = []

    for row in rows:
        large = 1.0 if row.group == group_b_value else 0.0
        design = [
            1.0,
            row.phase_before,
            row.phase_before * large,
        ]
        design.extend(
            1.0 if row.animal_year == year else 0.0
            for year in dummy_years
        )
        x_rows.append(design)
        y.append(row.phase_after)
        clusters.append(row.animal_id)

    X = np.asarray(x_rows, dtype=float)
    y_arr = np.asarray(y, dtype=float)

    # Guard obvious identification failures before asking statsmodels to fit.
    rank = int(np.linalg.matrix_rank(X))
    if rank < X.shape[1]:
        return PhaseRetentionContrastFit(
            estimable=False,
            support=support,
            total_pairs=len(rows),
            total_animals=total_animals,
            total_animal_years=total_animal_years,
            lambda_a=None,
            lambda_a_se=None,
            lambda_b=None,
            lambda_b_se=None,
            delta_lambda_b_minus_a=None,
            delta_lambda_se=None,
            p_difference=None,
            reasons=(
                "registered design matrix is rank deficient",
            ),
        )

    model = sm.OLS(y_arr, X).fit(
        cov_type="cluster",
        cov_kwds={
            "groups": np.asarray(clusters),
        },
    )

    params = np.asarray(model.params, dtype=float)
    cov = np.asarray(model.cov_params(), dtype=float)
    bse = np.asarray(model.bse, dtype=float)
    pvalues = np.asarray(model.pvalues, dtype=float)

    lambda_a = float(params[1])
    delta = float(params[2])
    lambda_b = lambda_a + delta

    lambda_a_se = float(bse[1])
    delta_se = float(bse[2])
    lambda_b_var = (
        cov[1, 1]
        + cov[2, 2]
        + 2.0 * cov[1, 2]
    )
    lambda_b_se = float(
        np.sqrt(max(lambda_b_var, 0.0))
    )

    # baseline_year is intentionally not reported as a biological quantity;
    # it merely defines the omitted animal-year fixed-effect level.
    del baseline_year

    return PhaseRetentionContrastFit(
        estimable=True,
        support=support,
        total_pairs=len(rows),
        total_animals=total_animals,
        total_animal_years=total_animal_years,
        lambda_a=lambda_a,
        lambda_a_se=lambda_a_se,
        lambda_b=lambda_b,
        lambda_b_se=lambda_b_se,
        delta_lambda_b_minus_a=delta,
        delta_lambda_se=delta_se,
        p_difference=float(pvalues[2]),
        reasons=(),
    )
