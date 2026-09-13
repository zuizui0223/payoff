from math import isclose, isfinite

from src.anti_phase_temporal import anti_phase_floquet_exponent
from src.two_patch_floquet import two_season_closed_form, two_season_temporal_premium


def test_large_antiphase_closed_form_matches_stable_specialization() -> None:
    for contrast in (400.0, 1000.0):
        seasons = [
            (contrast, -contrast, 1.0),
            (-contrast, contrast, 1.0),
        ]
        observed = two_season_closed_form(seasons, 1.0)
        expected = anti_phase_floquet_exponent(0.0, contrast, 1.0, 1.0)
        assert isfinite(observed)
        assert isclose(observed, expected, rel_tol=2e-13, abs_tol=2e-13)


def test_large_antiphase_temporal_premium_stays_finite() -> None:
    seasons = [(400.0, -400.0, 1.0), (-400.0, 400.0, 1.0)]
    premium = two_season_temporal_premium(seasons, 1.0)
    assert isfinite(premium)
    assert premium > 0.0


def test_zero_traceless_season_avoids_matrix_exponential_fallback() -> None:
    seasons = [(0.0, 0.0, 1.0), (1000.0, -1000.0, 1.0)]
    observed = two_season_closed_form(seasons, 0.0)
    assert isfinite(observed)
    assert isclose(observed, 500.0, rel_tol=0.0, abs_tol=1e-12)
