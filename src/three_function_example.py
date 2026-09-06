"""Exact three-function worked example used by PAYOFF documentation/tests.

Reference problem:
    theta=(0,1,3), a_i=1,
    edges=(01,02,12), c_e=1,
    common linear release cost k per fully released edge.

The unique global vertex topology has three exact cost phases:
    k<1/3          full release 111,
    1/3<k<19/12   two-module release 011 = {0,1}|{2},
    k>19/12        fully coupled reference 000.

Inside the two-module phase, accessibility from 000 separates again:
    k<9/16        infinitesimal pressure-driven release is available,
    9/16<k<9/8   infinitesimal release blocked but a full 02 edge flip is uphill,
    9/8<k<19/12  every one-edge flip is downhill; a fitness valley is required.
"""

from __future__ import annotations

from typing import Dict, Tuple

from src.edgewise_modularity import enumerate_vertex_topologies
from src.topology_mutation import intrinsic_valley_depth, is_single_edge_local_optimum

Topology = Tuple[int, int, int]

OPTIMA = (0.0, 1.0, 3.0)
WEIGHTS = (1.0, 1.0, 1.0)
EDGES = ((0, 1), (0, 2), (1, 2))
REFERENCE_COUPLINGS = (1.0, 1.0, 1.0)

FULLY_COUPLED: Topology = (0, 0, 0)
TWO_MODULE: Topology = (0, 1, 1)
FULLY_RELEASED: Topology = (1, 1, 1)

K_FULL_TO_MODULE = 1.0 / 3.0
K_LOCAL_PRESSURE = 9.0 / 16.0
K_SINGLE_EDGE_FLIP = 9.0 / 8.0
K_MODULE_TO_REFERENCE = 19.0 / 12.0


def intrinsic_topology_payoffs(edge_cost: float) -> Dict[Topology, float]:
    """Return intrinsic net payoff for all 8 release topologies."""

    if edge_cost < 0.0:
        raise ValueError("edge_cost must be non-negative")
    rows = enumerate_vertex_topologies(
        OPTIMA,
        WEIGHTS,
        EDGES,
        REFERENCE_COUPLINGS,
        (edge_cost, edge_cost, edge_cost),
    )
    return {
        tuple(int(value) for value in row["released"]): float(row["net_gain"])
        for row in rows
    }


def global_topology_phase(edge_cost: float, tol: float = 1e-12) -> str:
    """Return full differentiation / two-module / full coupling / boundary."""

    if edge_cost < 0.0:
        raise ValueError("edge_cost must be non-negative")
    if abs(edge_cost - K_FULL_TO_MODULE) <= tol:
        return "full_vs_two_module_boundary"
    if abs(edge_cost - K_MODULE_TO_REFERENCE) <= tol:
        return "two_module_vs_reference_boundary"
    if edge_cost < K_FULL_TO_MODULE:
        return "full_differentiation"
    if edge_cost < K_MODULE_TO_REFERENCE:
        return "two_module"
    return "fully_coupled"


def module_accessibility_regime(edge_cost: float, tol: float = 1e-12) -> str:
    """Classify accessibility inside the two-module global-optimum phase."""

    phase = global_topology_phase(edge_cost, tol)
    if phase != "two_module":
        return "outside_two_module_phase"
    if abs(edge_cost - K_LOCAL_PRESSURE) <= tol:
        return "infinitesimal_release_boundary"
    if abs(edge_cost - K_SINGLE_EDGE_FLIP) <= tol:
        return "single_edge_flip_boundary"
    if edge_cost < K_LOCAL_PRESSURE:
        return "infinitesimal_pressure_path"
    if edge_cost < K_SINGLE_EDGE_FLIP:
        return "finite_edge_flip_path"
    return "single_edge_fitness_valley"


def reference_is_single_edge_local_optimum(edge_cost: float) -> bool:
    """Return whether every complete one-edge release lowers intrinsic payoff."""

    payoffs = intrinsic_topology_payoffs(edge_cost)
    return is_single_edge_local_optimum(FULLY_COUPLED, payoffs)


def reference_to_module_valley_depth(edge_cost: float) -> float:
    """Exact single-edge mutation valley depth from 000 to global module 011."""

    payoffs = intrinsic_topology_payoffs(edge_cost)
    return intrinsic_valley_depth(FULLY_COUPLED, TWO_MODULE, payoffs)


def exact_reference_to_module_valley_depth(edge_cost: float) -> float:
    """Closed form max(0,k-9/8) within the two-module global phase."""

    if edge_cost < 0.0:
        raise ValueError("edge_cost must be non-negative")
    if global_topology_phase(edge_cost) != "two_module":
        raise ValueError("closed-form accessibility receipt is registered inside two-module phase")
    return max(0.0, edge_cost - K_SINGLE_EDGE_FLIP)


def worked_example_summary(edge_cost: float) -> Dict[str, object]:
    """Return compact phase/accessibility diagnostics for one edge cost."""

    payoffs = intrinsic_topology_payoffs(edge_cost)
    best = max(payoffs, key=payoffs.get)
    return {
        "edge_cost": edge_cost,
        "global_phase": global_topology_phase(edge_cost),
        "best_topology": best,
        "best_payoff": payoffs[best],
        "accessibility": module_accessibility_regime(edge_cost),
        "reference_single_edge_local_optimum": reference_is_single_edge_local_optimum(edge_cost),
        "reference_to_module_valley_depth": reference_to_module_valley_depth(edge_cost),
    }
