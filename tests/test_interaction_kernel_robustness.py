from src.architecture_phase_atlas import regular_grid
from src.interaction_kernel_robustness import (
    compare_kernel_accessibility,
    kernel_accessibility,
    kernel_weight,
)


def test_compact_smooth_kernels_are_continuous_at_cutoff():
    for kernel in ("triangular", "cosine"):
        assert kernel_weight(0.0, epsilon=0.2, kernel=kernel) == 1.0
        assert kernel_weight(0.2, epsilon=0.2, kernel=kernel) == 0.0
        assert kernel_weight(0.21, epsilon=0.2, kernel=kernel) == 0.0


def test_gaussian_has_no_hard_cutoff():
    assert kernel_weight(0.2, epsilon=0.2, kernel="gaussian") > 0.0
    assert kernel_weight(1.0, epsilon=0.2, kernel="gaussian") > 0.0


def test_hard_cutoff_barrier_can_disappear_under_smoothing_at_same_parameters():
    grid = regular_grid(1.0, 161)
    results = compare_kernel_accessibility(
        grid,
        ("hard", "triangular", "cosine", "gaussian"),
        alpha=0.5,
        kappa=1.0,
        gamma=-1.0,
        epsilon=0.1,
    )
    by_kernel = {result.kernel: result for result in results}
    assert by_kernel["hard"].critical_jump_bins > 1
    assert by_kernel["triangular"].critical_jump_bins == 1
    assert by_kernel["cosine"].critical_jump_bins == 1
    assert by_kernel["gaussian"].critical_jump_bins == 1


def test_smooth_compact_kernel_can_still_generate_a_finite_jump_barrier():
    grid = regular_grid(1.0, 161)
    triangular = kernel_accessibility(
        grid,
        alpha=0.5,
        kappa=1.0,
        gamma=-2.0,
        epsilon=0.3,
        kernel="triangular",
    )
    cosine = kernel_accessibility(
        grid,
        alpha=0.5,
        kappa=1.0,
        gamma=-3.0,
        epsilon=0.3,
        kernel="cosine",
    )
    assert triangular.critical_jump_distance > 0.05
    assert cosine.critical_jump_distance > 0.05


def test_strong_narrow_gaussian_feedback_can_create_a_smooth_barrier():
    grid = regular_grid(1.0, 161)
    gaussian = kernel_accessibility(
        grid,
        alpha=0.5,
        kappa=1.0,
        gamma=-20.0,
        epsilon=0.05,
        kernel="gaussian",
    )
    assert gaussian.critical_jump_distance >= 0.05
