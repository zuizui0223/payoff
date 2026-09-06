from src.architecture_phase_atlas import regular_grid
from src.kernel_accessibility_envelope import kernel_accessibility_envelope


KERNELS = ("hard", "triangular", "cosine", "gaussian")


def test_zero_feedback_is_accessible_for_all_kernels():
    env = kernel_accessibility_envelope(
        regular_grid(1.0, 161),
        KERNELS,
        alpha=0.5,
        kappa=1.0,
        gamma=0.0,
        epsilon=0.1,
        declared_jump_radius_bins=1,
    )
    assert env.robustness_class == "all_accessible"
    assert set(env.accessible_kernels) == set(KERNELS)
    assert not env.trapped_kernels


def test_moderate_negative_feedback_can_be_kernel_sensitive():
    env = kernel_accessibility_envelope(
        regular_grid(1.0, 161),
        KERNELS,
        alpha=0.5,
        kappa=1.0,
        gamma=-1.0,
        epsilon=0.1,
        declared_jump_radius_bins=1,
    )
    assert env.robustness_class == "kernel_sensitive"
    assert "hard" in env.trapped_kernels
    assert "triangular" in env.accessible_kernels
    assert "cosine" in env.accessible_kernels
    assert "gaussian" in env.accessible_kernels


def test_strong_narrow_feedback_can_be_robustly_trapped_across_kernel_family():
    env = kernel_accessibility_envelope(
        regular_grid(1.0, 161),
        KERNELS,
        alpha=0.5,
        kappa=1.0,
        gamma=-30.0,
        epsilon=0.05,
        declared_jump_radius_bins=1,
    )
    assert env.robustness_class == "all_trapped"
    assert not env.accessible_kernels
    assert set(env.trapped_kernels) == set(KERNELS)
    assert env.min_critical_jump_distance > env.declared_jump_distance
