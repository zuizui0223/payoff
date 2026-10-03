import pytest

from src.controller_network_mismatch import (
    binary_controller_cut_identity,
    complete_graph_controller_variance_identity,
    controller_network_mismatch,
)


def path_edges(n):
    return [(i, i + 1, 1.0) for i in range(n - 1)]


def complete_edges(n):
    return [(i, j, 1.0) for i in range(n) for j in range(i + 1, n)]


def test_constant_controller_field_has_zero_network_mismatch():
    result = controller_network_mismatch(
        [0.4, 0.4, 0.4],
        complete_edges(3),
        common_phase_error=10.0,
    )
    assert result.controller_dirichlet_energy == pytest.approx(0.0)
    assert result.induced_mean_squared_edge_mismatch == pytest.approx(0.0)


def test_network_mismatch_scales_with_squared_common_error():
    edges = complete_edges(3)
    a = controller_network_mismatch(
        [0.2, 0.5, 0.8],
        edges,
        common_phase_error=2.0,
    )
    b = controller_network_mismatch(
        [0.2, 0.5, 0.8],
        edges,
        common_phase_error=6.0,
    )
    assert b.induced_mean_squared_edge_mismatch == pytest.approx(
        9.0 * a.induced_mean_squared_edge_mismatch
    )


def test_complete_graph_dirichlet_energy_matches_controller_variance_identity():
    direct, closed = complete_graph_controller_variance_identity(
        [0.1, 0.3, 0.7, 0.9]
    )
    assert direct == pytest.approx(closed)


def test_binary_controller_field_recovers_network_cut_identity():
    edges = [
        (0, 1, 2.0),
        (1, 2, 1.0),
        (2, 3, 3.0),
        (0, 3, 4.0),
    ]
    direct, closed = binary_controller_cut_identity(
        [0, 0, 1, 1],
        edges,
        retention_0=0.2,
        retention_1=0.8,
    )
    assert direct == pytest.approx(closed)


def test_same_controller_distribution_can_have_different_topological_mismatch():
    edges = path_edges(4)

    # Same multiset {0,0,1,1}; clustered assignment has only one crossing edge.
    clustered = controller_network_mismatch(
        [0.0, 0.0, 1.0, 1.0],
        edges,
        common_phase_error=1.0,
    )

    # Alternating assignment has all three path edges crossing.
    alternating = controller_network_mismatch(
        [0.0, 1.0, 0.0, 1.0],
        edges,
        common_phase_error=1.0,
    )

    assert clustered.controller_dirichlet_energy == pytest.approx(1.0)
    assert alternating.controller_dirichlet_energy == pytest.approx(3.0)
    assert alternating.induced_mean_squared_edge_mismatch == pytest.approx(
        3.0 * clustered.induced_mean_squared_edge_mismatch
    )


def test_duplicate_undirected_edges_are_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        controller_network_mismatch(
            [0.2, 0.8],
            [(0, 1, 1.0), (1, 0, 1.0)],
            common_phase_error=1.0,
        )
