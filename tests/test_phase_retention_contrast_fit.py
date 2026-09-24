import math

import pytest

from src.phase_retention_contrast_fit import (
    PhasePairRecord,
    fit_phase_retention_contrast,
)


def make_records(
    *,
    animals_per_group=10,
    pairs_per_animal=12,
    lambda_small=0.30,
    lambda_large=0.60,
):
    rows = []
    for group, lam, prefix in (
        ("small", lambda_small, "S"),
        ("large", lambda_large, "L"),
    ):
        for animal_index in range(animals_per_group):
            animal_id = f"{prefix}{animal_index:02d}"
            animal_year = f"{animal_id}_2020"
            intercept = (
                (animal_index - animals_per_group / 2)
                * 0.03
            )
            for pair_index in range(pairs_per_animal):
                before = float(pair_index - pairs_per_animal / 2)
                # Deterministic small residual pattern keeps clustered
                # uncertainty finite without changing the target slopes.
                residual = (
                    ((pair_index % 3) - 1)
                    * 0.02
                    * (1.0 + animal_index / 20.0)
                )
                after = intercept + lam * before + residual
                rows.append(
                    PhasePairRecord(
                        animal_id=animal_id,
                        animal_year=animal_year,
                        group=group,
                        phase_before=before,
                        phase_after=after,
                    )
                )
    return rows


def test_support_gate_returns_not_estimable_without_fitting():
    fit = fit_phase_retention_contrast(
        make_records(
            animals_per_group=3,
            pairs_per_animal=5,
        ),
        group_a_value="small",
        group_b_value="large",
        min_animals_per_group=10,
        min_pairs_per_group=100,
    )

    assert not fit.estimable
    assert fit.lambda_a is None
    assert fit.lambda_b is None
    assert fit.p_difference is None
    assert any(
        "animal support" in reason
        for reason in fit.reasons
    )
    assert any(
        "transition support" in reason
        for reason in fit.reasons
    )


def test_clustered_fixed_effect_fit_recovers_registered_lambda_contrast():
    pytest.importorskip("numpy")
    pytest.importorskip("statsmodels")

    fit = fit_phase_retention_contrast(
        make_records(),
        group_a_value="small",
        group_b_value="large",
        min_animals_per_group=10,
        min_pairs_per_group=100,
    )

    assert fit.estimable
    assert fit.support.group_a_animals == 10
    assert fit.support.group_b_animals == 10
    assert fit.support.group_a_pairs == 120
    assert fit.support.group_b_pairs == 120
    assert fit.lambda_a == pytest.approx(
        0.30,
        abs=0.01,
    )
    assert fit.lambda_b == pytest.approx(
        0.60,
        abs=0.01,
    )
    assert fit.delta_lambda_b_minus_a == pytest.approx(
        0.30,
        abs=0.015,
    )
    assert fit.delta_lambda_se is not None
    assert math.isfinite(fit.delta_lambda_se)
    assert fit.p_difference is not None
    assert fit.p_difference < 0.05


def test_unknown_non_target_group_is_ignored_not_relabelled():
    rows = make_records()
    rows.append(
        PhasePairRecord(
            animal_id="X",
            animal_year="X_2020",
            group="other",
            phase_before=1.0,
            phase_after=99.0,
        )
    )

    fit = fit_phase_retention_contrast(
        rows,
        group_a_value="small",
        group_b_value="large",
        min_animals_per_group=50,
        min_pairs_per_group=1000,
    )

    assert fit.total_pairs == 240
    assert not fit.estimable


def test_identical_group_values_are_rejected():
    with pytest.raises(ValueError):
        fit_phase_retention_contrast(
            make_records(
                animals_per_group=1,
                pairs_per_animal=3,
            ),
            group_a_value="small",
            group_b_value="small",
        )
