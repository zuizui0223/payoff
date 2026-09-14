from math import isclose

from src.architecture_phase_atlas import (
    classify_distribution,
    iterate_dynamics,
    phase_cell,
)


def test_bounded_interaction_epsilon_is_not_inflated_on_tiny_domain():
    scale = 1e-16
    grid = (0.0, scale, 2.0 * scale)
    initial = (0.8, 0.2, 0.0)
    result = iterate_dynamics(
        grid,
        initial,
        alpha=0.0,
        kappa=0.0,
        gamma=1.0 / (scale * scale),
        epsilon=0.5 * scale,
        beta=1.0,
        mutation_rate=0.0,
        jump_radius_bins=1,
        steps=1,
    )
    assert all(isclose(a, b, rel_tol=0.0, abs_tol=1e-15) for a, b in zip(result.density, initial))


def test_endpoint_mass_classification_is_coordinate_scale_invariant():
    density = (0.0, 0.0, 1.0, 0.0, 0.0)
    for scale in (1e-16, 1.0, 1e16):
        grid = tuple(scale * value for value in (0.0, 0.25, 0.5, 0.75, 1.0))
        phase = classify_distribution(grid, density)
        assert phase.regime == "single_cluster"
        assert phase.left_endpoint_mass == 0.0
        assert phase.right_endpoint_mass == 0.0


def test_endpoint_cut_boundary_remains_inclusive_after_rescaling():
    density = (0.4, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.4)
    for scale in (1e-16, 1.0, 1e16):
        grid = tuple(scale * i / 10.0 for i in range(11))
        phase = classify_distribution(grid, density)
        assert phase.regime == "endpoint_coexistence"
        assert isclose(phase.left_endpoint_mass, 0.5, rel_tol=0.0, abs_tol=1e-15)
        assert isclose(phase.right_endpoint_mass, 0.5, rel_tol=0.0, abs_tol=1e-15)


def test_phase_cell_accessibility_is_coordinate_scale_invariant():
    base = phase_cell(
        gamma=-1.0,
        epsilon=0.10,
        jump_radius_bins=1,
        bins=41,
        steps=20,
    )
    assert base.critical_uphill_jump_bins == 2

    scale = 1e-16
    scaled = phase_cell(
        gamma=-1.0 / (scale * scale),
        epsilon=0.10 * scale,
        jump_radius_bins=1,
        alpha=0.5 / scale,
        kappa=1.0 / (scale * scale),
        length=scale,
        bins=41,
        steps=20,
    )
    assert scaled.critical_uphill_jump_bins == base.critical_uphill_jump_bins
