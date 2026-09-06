from math import isclose

from src.edgewise_modularity import (
    best_vertex_topology,
    edge_pressures,
    enumerate_vertex_topologies,
    optimized_loss,
    optimized_phenotype,
)
from src.topology_release_path import greedy_positive_pressure_path


OPTIMA = (0.0, 1.0, 3.0)
WEIGHTS = (1.0, 1.0, 1.0)
EDGES = ((0, 1), (0, 2), (1, 2))
COUPLINGS = (1.0, 1.0, 1.0)
COSTS = (0.4, 0.4, 0.4)


def test_reference_solution_and_edge_pressures_are_exact():
    phenotype = optimized_phenotype(OPTIMA, WEIGHTS, EDGES, COUPLINGS)
    assert all(
        isclose(observed, expected, abs_tol=1e-12)
        for observed, expected in zip(phenotype, (1.0, 1.25, 1.75))
    )
    assert isclose(
        optimized_loss(OPTIMA, WEIGHTS, EDGES, COUPLINGS),
        3.5,
        abs_tol=1e-12,
    )
    pressures = edge_pressures(OPTIMA, WEIGHTS, EDGES, COUPLINGS)
    expected = (1.0 / 16.0, 9.0 / 16.0, 1.0 / 4.0)
    assert all(
        isclose(observed, target, abs_tol=1e-12)
        for observed, target in zip(pressures, expected)
    )
    assert pressures[1] > COSTS[1]
    assert pressures[0] < COSTS[0]
    assert pressures[2] < COSTS[2]


def test_first_release_reroutes_pressure_to_edge_12():
    couplings_after_02 = (1.0, 0.0, 1.0)
    phenotype = optimized_phenotype(
        OPTIMA, WEIGHTS, EDGES, couplings_after_02
    )
    assert all(
        isclose(observed, expected, abs_tol=1e-12)
        for observed, expected in zip(phenotype, (5.0 / 8.0, 5.0 / 4.0, 17.0 / 8.0))
    )
    pressures = edge_pressures(
        OPTIMA, WEIGHTS, EDGES, couplings_after_02
    )
    assert isclose(pressures[0], 25.0 / 64.0, abs_tol=1e-12)
    assert isclose(pressures[2], 49.0 / 64.0, abs_tol=1e-12)
    assert pressures[0] < COSTS[0]
    assert pressures[2] > COSTS[2]


def test_greedy_pressure_path_predicts_accessible_module_partition():
    path = greedy_positive_pressure_path(
        OPTIMA, WEIGHTS, EDGES, COUPLINGS, COSTS
    )
    assert len(path) == 3

    assert path[0]["released"] == (False, False, False)
    assert path[0]["next_edge_index"] == 1
    assert path[0]["components"] == ((0, 1, 2),)

    assert path[1]["released"] == (False, True, False)
    assert path[1]["next_edge_index"] == 2
    assert isclose(float(path[1]["net_gain"]), 29.0 / 40.0, abs_tol=1e-12)

    assert path[2]["released"] == (False, True, True)
    assert path[2]["next_edge_index"] is None
    assert path[2]["components"] == ((0, 1), (2,))
    assert isclose(float(path[2]["net_gain"]), 71.0 / 30.0, abs_tol=1e-12)
    assert isclose(float(path[2]["pressures"][0]), 1.0 / 9.0, abs_tol=1e-12)
    assert float(path[2]["pressures"][0]) < COSTS[0]


def test_accessible_module_partition_is_global_vertex_optimum():
    best = best_vertex_topology(OPTIMA, WEIGHTS, EDGES, COUPLINGS, COSTS)
    assert best["released"] == (False, True, True)
    assert isclose(float(best["recovery"]), 19.0 / 6.0, abs_tol=1e-12)
    assert isclose(float(best["architecture_cost"]), 4.0 / 5.0, abs_tol=1e-12)
    assert isclose(float(best["net_gain"]), 71.0 / 30.0, abs_tol=1e-12)

    rows = enumerate_vertex_topologies(
        OPTIMA, WEIGHTS, EDGES, COUPLINGS, COSTS
    )
    full_release = next(row for row in rows if row["released"] == (True, True, True))
    assert isclose(float(full_release["net_gain"]), 23.0 / 10.0, abs_tol=1e-12)
    assert isclose(
        float(best["net_gain"]) - float(full_release["net_gain"]),
        1.0 / 15.0,
        abs_tol=1e-12,
    )


def test_joint_release_recovery_is_strongly_nonadditive():
    rows = {
        row["released"]: row
        for row in enumerate_vertex_topologies(
            OPTIMA, WEIGHTS, EDGES, COUPLINGS, COSTS
        )
    }
    r_02 = float(rows[(False, True, False)]["recovery"])
    r_12 = float(rows[(False, False, True)]["recovery"])
    r_joint = float(rows[(False, True, True)]["recovery"])
    assert isclose(r_02, 9.0 / 8.0, abs_tol=1e-12)
    assert isclose(r_12, 1.0 / 2.0, abs_tol=1e-12)
    assert isclose(r_joint, 19.0 / 6.0, abs_tol=1e-12)
    assert isclose(r_joint - r_02 - r_12, 37.0 / 24.0, abs_tol=1e-12)
