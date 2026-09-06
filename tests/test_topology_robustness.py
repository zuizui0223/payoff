from math import isclose

from src.three_function_example import (
    EDGES,
    OPTIMA,
    REFERENCE_COUPLINGS,
    TWO_MODULE,
    WEIGHTS,
)
from src.topology_robustness import (
    global_vertex_reserve,
    local_vertex_reserve,
    topology_robustness_summary,
    vertex_boundary_margins,
)


COSTS = (0.4, 0.4, 0.4)


def test_three_function_global_topology_reserve_is_one_fifteenth():
    receipt = global_vertex_reserve(
        OPTIMA, WEIGHTS, EDGES, REFERENCE_COUPLINGS, COSTS
    )
    assert tuple(int(value) for value in receipt["best_released"]) == TWO_MODULE
    assert tuple(int(value) for value in receipt["second_released"]) == (1, 1, 1)
    assert isclose(float(receipt["global_reserve"]), 1.0 / 15.0, abs_tol=1e-12)


def test_three_function_local_boundary_margins_are_exact():
    margins = vertex_boundary_margins(
        OPTIMA,
        WEIGHTS,
        EDGES,
        REFERENCE_COUPLINGS,
        COSTS,
        TWO_MODULE,
    )
    expected = (
        13.0 / 45.0,
        302.0 / 45.0,
        227.0 / 45.0,
    )
    assert all(
        isclose(observed, target, abs_tol=1e-12)
        for observed, target in zip(margins, expected)
    )
    assert isclose(
        local_vertex_reserve(
            OPTIMA,
            WEIGHTS,
            EDGES,
            REFERENCE_COUPLINGS,
            COSTS,
            TWO_MODULE,
        ),
        13.0 / 45.0,
        abs_tol=1e-12,
    )


def test_global_and_local_reserves_are_distinct_estimands():
    summary = topology_robustness_summary(
        OPTIMA, WEIGHTS, EDGES, REFERENCE_COUPLINGS, COSTS
    )
    assert summary["strict_local_vertex_stability"]
    assert isclose(float(summary["global_reserve"]), 1.0 / 15.0, abs_tol=1e-12)
    assert isclose(float(summary["local_reserve"]), 13.0 / 45.0, abs_tol=1e-12)
    assert float(summary["local_reserve"]) > float(summary["global_reserve"])
