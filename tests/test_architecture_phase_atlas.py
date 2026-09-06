from src.architecture_phase_atlas import (
    build_phase_atlas,
    classify_distribution,
    minimum_uphill_jump_radius_to_global,
    phase_cell,
    regular_grid,
)


def test_distribution_classifier_separates_endpoint_and_interior_clusters():
    grid = regular_grid(1.0, 11)
    endpoint = (0.4, 0.1, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.4)
    interior = (0, 0, 0.4, 0.1, 0, 0, 0, 0.1, 0.4, 0, 0)
    assert classify_distribution(grid, endpoint).regime == "endpoint_coexistence"
    assert classify_distribution(grid, interior).regime == "interior_multicluster"


def test_minimum_uphill_jump_detects_valley_skipping_threshold():
    # 0 -> 1 is uphill, 1 -> 2 is downhill, and radius 2 can jump 1 -> 3.
    payoff = (0.0, 0.10, 0.09, 0.20)
    assert minimum_uphill_jump_radius_to_global(payoff, 0) == 2


def test_global_negative_feedback_reaches_endpoint_coexistence():
    cell = phase_cell(
        gamma=-1.0,
        epsilon=None,
        jump_radius_bins=1,
        bins=41,
        steps=800,
    )
    assert cell.dynamical_regime == "endpoint_coexistence"
    assert len(cell.peak_locations) >= 2
    assert cell.left_endpoint_mass > 0.10
    assert cell.right_endpoint_mass > 0.10


def test_narrow_bounded_interaction_suppresses_global_branching_pattern():
    narrow = phase_cell(
        gamma=-2.0,
        epsilon=0.05,
        jump_radius_bins=1,
        bins=41,
        steps=800,
    )
    wider = phase_cell(
        gamma=-2.0,
        epsilon=0.40,
        jump_radius_bins=1,
        bins=41,
        steps=800,
    )
    assert narrow.dynamical_regime == "single_cluster"
    assert wider.dynamical_regime == "interior_multicluster"


def test_bounded_interaction_creates_a_small_jump_accessibility_overlay():
    radius1 = phase_cell(
        gamma=-1.0,
        epsilon=0.10,
        jump_radius_bins=1,
        bins=41,
        steps=200,
    )
    radius2 = phase_cell(
        gamma=-1.0,
        epsilon=0.10,
        jump_radius_bins=2,
        bins=41,
        steps=200,
    )
    assert radius1.critical_uphill_jump_bins == 2
    assert radius1.small_jump_trapped
    assert radius2.critical_uphill_jump_bins == 2
    assert not radius2.small_jump_trapped


def test_atlas_cartesian_product_is_deterministic():
    cells = build_phase_atlas(
        gammas=(-1.0, 0.0),
        epsilons=(0.1, None),
        jump_radii_bins=(1, 2),
        bins=21,
        steps=30,
    )
    assert len(cells) == 8
    assert [cell.to_dict() for cell in cells] == [cell.to_dict() for cell in cells]
