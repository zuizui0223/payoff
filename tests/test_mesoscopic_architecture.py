from src.mesoscopic_architecture import (
    architecture_payoff,
    bounded_interaction_payoff,
    mean_architecture,
    mesoscopic_step,
    minimum_jump_to_better_state,
    small_jump_mutation,
)


def test_small_jump_identity_and_mass_conservation():
    f = (0.0, 1.0, 0.0, 0.0)
    assert small_jump_mutation(f, radius_bins=0, mutation_rate=0.7) == f
    moved = small_jump_mutation(f, radius_bins=1, mutation_rate=0.4)
    assert abs(sum(moved) - 1.0) < 1e-12
    assert moved[3] == 0.0
    assert moved[0] == 0.2
    assert moved[2] == 0.2


def test_bounded_kernel_excludes_distant_architectures():
    grid = (0.0, 0.5, 1.0)
    f = (1.0, 0.0, 0.0)
    local = bounded_interaction_payoff(grid, f, gamma=2.0, epsilon=0.4)
    global_ = bounded_interaction_payoff(grid, f, gamma=2.0, epsilon=None)
    assert local[2] == 0.0
    assert global_[2] == -2.0


def test_mesoscopic_step_preserves_probability_mass():
    grid = (0.0, 0.25, 0.5, 0.75, 1.0)
    step = mesoscopic_step(
        grid,
        (0.1, 0.2, 0.4, 0.2, 0.1),
        alpha=0.8,
        kappa=1.0,
        gamma=-0.7,
        epsilon=0.5,
        beta=0.5,
        mutation_rate=0.1,
        jump_radius_bins=1,
    )
    assert abs(sum(step.density_after_mutation) - 1.0) < 1e-12
    assert all(x >= 0.0 for x in step.density_after_mutation)


def test_intrinsic_selection_moves_mean_toward_higher_payoff():
    grid = (0.0, 0.5, 1.0)
    f = (1 / 3, 1 / 3, 1 / 3)
    before = mean_architecture(grid, f)
    step = mesoscopic_step(
        grid, f, alpha=1.0, kappa=1.0, beta=2.0, mutation_rate=0.0
    )
    after = mean_architecture(grid, step.density_after_mutation)
    assert after > before


def test_minimum_jump_diagnostic():
    grid = (0.0, 0.25, 0.5, 0.75, 1.0)
    payoff = (0.0, -1.0, -0.5, 0.2, 1.0)
    assert minimum_jump_to_better_state(grid, payoff, 0) == 3
    assert minimum_jump_to_better_state(grid, payoff, 4) is None


def test_global_zero_gamma_reduces_to_intrinsic_payoff():
    grid = (0.0, 0.5, 1.0)
    f = (0.2, 0.3, 0.5)
    assert architecture_payoff(
        grid, f, alpha=1.0, kappa=2.0, gamma=0.0, epsilon=0.1
    ) == (0.0, 0.25, 0.0)
