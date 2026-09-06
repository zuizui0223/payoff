from math import isclose

from src.environment_mosaic import (
    critical_migration_rate,
    d_invasion_exponent,
    graph_laplacian,
    heterogeneous_mean_selection,
    invasion_exponent,
    invasion_margins,
    largest_symmetric_eigenvalue,
    patch_phi,
    s_invasion_exponent,
    source_sink_summary,
    two_patch_invasion_exponent,
    two_patch_rescue_threshold,
)


def test_patch_phi_bridge():
    phis = patch_phi(
        conflict_loads=[2.0, 3.0, 1.0],
        separation_fractions=[0.5, 0.25, 1.0],
        architecture_costs=[0.7, 0.5, 1.2],
    )
    expected = [0.3, 0.25, -0.2]
    assert all(isclose(a, b, abs_tol=1e-12) for a, b in zip(phis, expected))


def test_heterogeneous_mean_selection_decomposition_exact():
    p = [0.05, 0.2, 0.55, 0.9]
    phi = [0.4, -0.2, 0.7, -0.5]
    eta = [-0.6, 0.3, 1.1, -0.4]
    result = heterogeneous_mean_selection(p, phi, eta)
    assert isclose(
        result["mean_selection"],
        result["reconstructed_mean_selection"],
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_invasion_margins_are_reciprocal_endpoints():
    d, s = invasion_margins([0.4, -0.2], [0.1, -0.3])
    assert all(isclose(a, b, abs_tol=1e-12) for a, b in zip(d, [0.3, 0.1]))
    assert all(isclose(a, b, abs_tol=1e-12) for a, b in zip(s, [-0.5, 0.5]))


def test_laplacian_and_jacobi_eigen_solver():
    adjacency = [[0.0, 1.0], [1.0, 0.0]]
    lap = graph_laplacian(adjacency)
    assert lap == [[1.0, -1.0], [-1.0, 1.0]]
    assert isclose(largest_symmetric_eigenvalue(lap), 2.0, abs_tol=1e-12)


def test_two_patch_exponent_matches_general_solver():
    adjacency = [[0.0, 1.0], [1.0, 0.0]]
    r1, r2 = 0.7, -1.3
    for m in [0.0, 0.1, 0.5, 3.0]:
        general = invasion_exponent([r1, r2], adjacency, m)
        exact = two_patch_invasion_exponent(r1, r2, m)
        assert isclose(general, exact, rel_tol=1e-11, abs_tol=1e-11)


def test_two_patch_source_sink_threshold_exact():
    r1, r2 = 0.5, -1.5
    mc = two_patch_rescue_threshold(r1, r2)
    assert isclose(mc, 0.75, abs_tol=1e-12)
    assert two_patch_invasion_exponent(r1, r2, mc * 0.9) > 0.0
    assert abs(two_patch_invasion_exponent(r1, r2, mc)) < 1e-12
    assert two_patch_invasion_exponent(r1, r2, mc * 1.1) < 0.0


def test_general_critical_migration_matches_two_patch_formula():
    adjacency = [[0.0, 1.0], [1.0, 0.0]]
    margins = [0.5, -1.5]
    numeric = critical_migration_rate(margins, adjacency)
    exact = two_patch_rescue_threshold(*margins)
    assert isclose(numeric, exact, rel_tol=1e-8, abs_tol=1e-8)


def test_principal_exponent_decreases_toward_mean_margin():
    adjacency = [
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ]
    margins = [1.0, -0.4, -1.2]
    values = [invasion_exponent(margins, adjacency, m) for m in [0.0, 0.1, 1.0, 10.0, 1000.0]]
    assert all(values[i] > values[i + 1] for i in range(len(values) - 1))
    assert isclose(values[0], max(margins), abs_tol=1e-12)
    assert abs(values[-1] - sum(margins) / len(margins)) < 1e-3


def test_static_average_balance_can_have_low_migration_d_rescue():
    # eta=0 so local D margins are exactly the static phi_j.
    phis = [0.6, -1.0]
    etas = [0.0, 0.0]
    adjacency = [[0.0, 1.0], [1.0, 0.0]]
    assert sum(phis) / 2.0 < 0.0
    assert d_invasion_exponent(phis, etas, adjacency, 0.05) > 0.0
    assert d_invasion_exponent(phis, etas, adjacency, 2.0) < 0.0


def test_no_source_means_no_invasion_for_any_migration():
    adjacency = [
        [0.0, 1.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0],
    ]
    margins = [-0.1, -0.4, 0.0]
    for m in [0.0, 0.01, 1.0, 100.0]:
        assert invasion_exponent(margins, adjacency, m) <= 1e-12


def test_reciprocal_spatial_invasion_exponents():
    phis = [0.5, -0.2, 0.1]
    etas = [-0.4, -0.4, -0.4]
    adjacency = [
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ]
    d = d_invasion_exponent(phis, etas, adjacency, 0.2)
    s = s_invasion_exponent(phis, etas, adjacency, 0.2)
    assert d > 0.0
    assert s > 0.0


def test_source_sink_summary_endpoints():
    summary = source_sink_summary([0.8, -0.2, -1.1])
    assert summary["max_local_margin"] == 0.8
    assert summary["min_local_margin"] == -1.1
    assert isclose(summary["mean_local_margin"], -1.0 / 6.0, abs_tol=1e-12)
