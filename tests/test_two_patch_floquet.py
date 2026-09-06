from math import isclose
from random import Random

from src.two_patch_floquet import (
    commutator_scalar,
    fast_switching_premium_coefficient,
    floquet_exponent,
    floquet_summary,
    seasonal_matrix_exponential,
    temporal_noncommutativity_effect,
    time_averaged_operator_exponent,
    two_season_closed_form,
    two_season_temporal_premium,
)


def test_zero_duration_exponential_is_identity():
    observed = seasonal_matrix_exponential(1.0, -2.0, 0.3, 0.0)
    assert isclose(observed[0][0], 1.0, abs_tol=1e-12)
    assert isclose(observed[1][1], 1.0, abs_tol=1e-12)
    assert isclose(observed[0][1], 0.0, abs_tol=1e-12)
    assert isclose(observed[1][0], 0.0, abs_tol=1e-12)


def test_commutator_gate_vanishes_for_common_shift():
    m = 0.4
    season_a = (1.2, -0.3, 1.0)
    common_shift = -2.7
    season_b = (season_a[0] + common_shift, season_a[1] + common_shift, 2.0)
    assert isclose(commutator_scalar(season_a, season_b, m), 0.0, abs_tol=1e-12)


def test_commutator_gate_needs_migration_and_contrast_change():
    a = (1.0, -1.0, 1.0)
    b = (-0.5, 0.8, 1.0)
    assert isclose(commutator_scalar(a, b, 0.0), 0.0, abs_tol=1e-12)
    assert abs(commutator_scalar(a, b, 0.3)) > 0.0


def test_common_shift_floquet_equals_time_averaged_operator():
    seasons = [
        (0.8, -0.4, 1.0),
        (1.8, 0.6, 2.0),
        (-0.2, -1.4, 3.0),
    ]
    m = 0.35
    observed = floquet_exponent(seasons, m)
    averaged = time_averaged_operator_exponent(seasons, m)
    assert isclose(observed, averaged, rel_tol=1e-11, abs_tol=1e-11)


def test_noncommuting_seasons_differ_from_time_averaged_operator():
    seasons = [(1.0, -2.0, 1.0), (-2.0, 1.0, 1.0)]
    m = 0.3
    effect = temporal_noncommutativity_effect(seasons, m)
    assert effect > 0.05


def test_exact_temporal_rescue_example():
    seasons = [(-2.5, 1.0, 1.0), (2.0, -1.0, 1.0)]
    m = 0.3
    averaged = time_averaged_operator_exponent(seasons, m)
    floquet = floquet_exponent(seasons, m)
    assert isclose(averaged, -0.1, abs_tol=1e-12)
    assert averaged < 0.0
    assert floquet > 0.0
    assert isclose(floquet, 0.0335279723974975, rel_tol=1e-10, abs_tol=1e-10)


def test_floquet_summary_reports_commutator_and_effect():
    seasons = [(-2.5, 1.0, 1.0), (2.0, -1.0, 1.0)]
    summary = floquet_summary(seasons, 0.3)
    assert summary["max_pairwise_commutator_scalar"] > 0.0
    assert summary["temporal_effect"] > 0.0
    assert isclose(
        summary["temporal_effect"],
        summary["floquet_exponent"] - summary["time_averaged_operator_exponent"],
        abs_tol=1e-12,
    )


def test_two_season_closed_form_matches_period_matrix_result():
    rng = Random(20260906)
    for _ in range(50):
        seasons = [
            (rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0), rng.uniform(0.05, 1.5)),
            (rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0), rng.uniform(0.05, 1.5)),
        ]
        m = rng.uniform(0.01, 1.0)
        assert isclose(
            two_season_closed_form(seasons, m),
            floquet_exponent(seasons, m),
            rel_tol=1e-10,
            abs_tol=1e-10,
        )


def test_two_season_periodic_premium_is_nonnegative():
    rng = Random(78231)
    for _ in range(100):
        seasons = [
            (rng.uniform(-3.0, 3.0), rng.uniform(-3.0, 3.0), rng.uniform(0.02, 1.0)),
            (rng.uniform(-3.0, 3.0), rng.uniform(-3.0, 3.0), rng.uniform(0.02, 1.0)),
        ]
        m = rng.uniform(0.0, 1.2)
        assert two_season_temporal_premium(seasons, m) >= -1e-10


def test_two_season_premium_zero_at_commuting_gates():
    # No migration: seasonal diagonal operators always commute.
    seasons = [(1.0, -2.0, 0.4), (-0.5, 1.7, 0.6)]
    assert isclose(two_season_temporal_premium(seasons, 0.0), 0.0, abs_tol=1e-11)

    # Same patch contrast: operators differ only by a common scalar shift.
    m = 0.4
    seasons = [(1.3, -0.2, 0.3), (-0.7, -2.2, 0.7)]
    assert isclose(
        (seasons[0][0] - seasons[0][1]),
        (seasons[1][0] - seasons[1][1]),
        abs_tol=1e-12,
    )
    assert isclose(two_season_temporal_premium(seasons, m), 0.0, abs_tol=1e-11)


def test_fast_switching_premium_is_quadratic_in_period():
    season_a = (1.2, -0.5)
    season_b = (-0.8, 0.9)
    m = 0.35
    w = 0.4
    coefficient = fast_switching_premium_coefficient(season_a, season_b, m, w)
    assert coefficient > 0.0

    for total_period in [0.1, 0.05, 0.02]:
        seasons = [
            (season_a[0], season_a[1], w * total_period),
            (season_b[0], season_b[1], (1.0 - w) * total_period),
        ]
        observed = two_season_temporal_premium(seasons, m) / total_period**2
        assert isclose(observed, coefficient, rel_tol=5e-4, abs_tol=1e-8)


def test_fast_switching_coefficient_has_commutator_gates():
    a = (1.0, -1.0)
    b = (-0.5, 0.8)
    assert fast_switching_premium_coefficient(a, b, 0.0, 0.5) == 0.0

    same_contrast = (3.0, 1.0)
    assert isclose(
        fast_switching_premium_coefficient(a, same_contrast, 0.4, 0.5),
        0.0,
        abs_tol=1e-15,
    )
