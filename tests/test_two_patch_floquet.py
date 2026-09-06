from math import isclose

from src.two_patch_floquet import (
    commutator_scalar,
    floquet_exponent,
    floquet_summary,
    seasonal_matrix_exponential,
    temporal_noncommutativity_effect,
    time_averaged_operator_exponent,
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
    # Each season differs only by a common scalar shift, so all operators commute.
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
