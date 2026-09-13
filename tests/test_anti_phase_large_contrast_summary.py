from math import isfinite

from src.anti_phase_temporal import anti_phase_summary


def test_summary_survives_large_contrast_exact_optimum_path() -> None:
    summary = anti_phase_summary(
        mean_margin=-0.2,
        contrast_half_amplitude=400.0,
        migration_rate=1.0,
        season_duration=1.0,
    )
    assert isfinite(summary["floquet_exponent"])
    assert isfinite(summary["temporal_premium"])
    assert isfinite(summary["exact_optimal_migration"])
    assert isfinite(summary["exact_max_premium"])
