from math import isclose, isfinite

from src.two_patch_floquet import (
    floquet_exponent,
    floquet_summary,
    time_averaged_operator_exponent,
    two_season_closed_form,
)


def test_general_floquet_matches_stable_two_season_closed_form_at_large_contrast() -> None:
    seasons = [(400.0, -400.0, 1.0), (-400.0, 400.0, 1.0)]
    observed = floquet_exponent(seasons, 1.0)
    expected = two_season_closed_form(seasons, 1.0)
    assert isfinite(observed)
    assert isclose(observed, expected, rel_tol=2e-13, abs_tol=2e-13)


def test_large_three_season_commuting_path_stays_finite() -> None:
    # Every season has the same patch contrast (800), so the operators commute
    # despite large common shifts. The exact Floquet exponent must therefore
    # equal the time-averaged-operator exponent.
    seasons = [
        (400.0, -400.0, 1.0),
        (500.0, -300.0, 1.0),
        (300.0, -500.0, 1.0),
    ]
    observed = floquet_exponent(seasons, 1.0)
    expected = time_averaged_operator_exponent(seasons, 1.0)
    assert isfinite(observed)
    assert isclose(observed, expected, rel_tol=2e-13, abs_tol=2e-13)


def test_large_general_floquet_summary_stays_finite() -> None:
    seasons = [
        (400.0, -400.0, 0.8),
        (-350.0, 450.0, 1.1),
        (250.0, -550.0, 0.9),
    ]
    summary = floquet_summary(seasons, 0.7)
    assert isfinite(summary["floquet_exponent"])
    assert isfinite(summary["time_averaged_operator_exponent"])
    assert isfinite(summary["temporal_effect"])
    assert isfinite(summary["max_pairwise_commutator_scalar"])
