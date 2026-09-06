from src.triangular_kernel_barrier import triangular_feedback_window
from src.triangular_kernel_phase_curve import (
    dimensionless_triangular_window,
    interaction_range_window_at_feedback,
    narrow_range_asymptotic_ratios,
    near_intrinsic_optimum_asymptotic_ratios,
)


def test_dimensionless_curve_reproduces_dimensional_registered_window():
    row = dimensionless_triangular_window(0.6)
    dimensional = triangular_feedback_window(
        alpha=0.5,
        kappa=1.0,
        epsilon=0.3,
    )
    assert abs(row.g_on - dimensional.ridge_onset_G) < 1e-12
    assert abs(row.g_hi - dimensional.global_better_upper_G) < 1e-12
    assert abs(row.contact_x * 0.5 - dimensional.upper_contact_location) < 1e-12


def test_barrier_window_is_strictly_positive_across_declared_interaction_ranges():
    for E in (0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.95):
        row = dimensionless_triangular_window(E)
        assert row.g_hi > row.g_on > 0.0
        assert row.width > 0.0


def test_fixed_feedback_has_intermediate_interaction_range_window():
    window = interaction_range_window_at_feedback(2.0)
    assert abs(window.E_lower - 1.0 / 3.0) < 1e-12
    assert abs(window.E_upper - 0.6595648100573256) < 1e-12
    assert window.E_lower < 0.6 < window.E_upper

    inside = dimensionless_triangular_window(0.6)
    too_narrow = dimensionless_triangular_window(0.3)
    too_wide = dimensionless_triangular_window(0.7)
    assert inside.g_on < 2.0 < inside.g_hi
    assert 2.0 < too_narrow.g_on
    assert 2.0 > too_wide.g_hi


def test_fixed_feedback_half_case_uses_regular_linear_contact_root():
    window = interaction_range_window_at_feedback(0.5)
    assert abs(window.contact_x_upper - 0.75) < 1e-12
    assert abs(window.E_lower - 2.0 / 3.0) < 1e-12
    assert abs(window.E_upper - 0.84375) < 1e-12


def test_near_intrinsic_optimum_window_collapses_linearly():
    ratios = near_intrinsic_optimum_asymptotic_ratios(0.999999)
    assert abs(ratios[0] - 1.0) < 1e-5
    assert abs(ratios[1] - 2.0) < 2e-5
    assert abs(ratios[2] - 1.0) < 2e-5


def test_narrow_interaction_range_requires_diverging_feedback_with_quadratic_upper_boundary():
    ratios = narrow_range_asymptotic_ratios(1e-5)
    assert abs(ratios[0] - 1.0) < 2e-5
    assert abs(ratios[1] - 27.0 / 8.0) < 2e-4
    assert abs(ratios[2] - 27.0 / 8.0) < 3e-4
