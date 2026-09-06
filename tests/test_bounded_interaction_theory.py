from src.architecture_phase_atlas import (
    minimum_uphill_jump_radius_to_global,
    regular_grid,
)
from src.bounded_interaction_theory import (
    hard_cutoff_interface_jump,
    local_mutant_curvature,
    locally_branching_compatible,
    negative_feedback_interface_escape_infimum,
)
from src.mesoscopic_architecture import architecture_payoff


def test_local_branching_threshold_is_unchanged_for_positive_epsilon_neighbourhood():
    assert local_mutant_curvature(kappa=1.0, gamma=-0.75) == 0.5
    assert locally_branching_compatible(kappa=1.0, gamma=-0.75)
    assert local_mutant_curvature(kappa=1.0, gamma=-0.5) == 0.0
    assert not locally_branching_compatible(kappa=1.0, gamma=-0.5)


def test_hard_cutoff_interface_jump_has_expected_sign():
    assert hard_cutoff_interface_jump(gamma=-1.0, epsilon=0.1) == -0.01
    assert hard_cutoff_interface_jump(gamma=2.0, epsilon=0.1) == 0.02


def test_negative_feedback_shared_resident_escape_has_exact_infimum():
    result = negative_feedback_interface_escape_infimum(
        alpha=0.5,
        kappa=1.0,
        gamma=-1.0,
        epsilon=0.1,
    )
    assert abs(result.inside_boundary_payoff - 0.055) < 1e-12
    assert abs(result.outside_boundary_payoff - 0.045) < 1e-12
    assert abs(result.interface_jump + 0.01) < 1e-12
    assert abs(result.equal_payoff_origin_side - 0.08309518948453) < 1e-12
    assert abs(result.escape_jump_infimum - 0.01690481051547) < 1e-12


def test_finite_grid_uphill_threshold_approaches_continuous_escape_infimum():
    theory = negative_feedback_interface_escape_infimum(
        alpha=0.5,
        kappa=1.0,
        gamma=-1.0,
        epsilon=0.1,
    )
    grid = regular_grid(1.0, 161)
    resident = (1.0,) + (0.0,) * 160
    payoff = architecture_payoff(
        grid,
        resident,
        alpha=0.5,
        kappa=1.0,
        gamma=-1.0,
        epsilon=0.1 + 1e-12,
    )
    critical_bins = minimum_uphill_jump_radius_to_global(payoff, 0)
    critical_distance = critical_bins * (grid[1] - grid[0])
    assert critical_distance >= theory.escape_jump_infimum
    assert critical_distance - theory.escape_jump_infimum < 0.01
