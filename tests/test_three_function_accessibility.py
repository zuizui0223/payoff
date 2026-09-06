from math import isclose

from src.three_function_example import (
    FULLY_COUPLED,
    FULLY_RELEASED,
    K_FULL_TO_MODULE,
    K_LOCAL_PRESSURE,
    K_MODULE_TO_REFERENCE,
    K_SINGLE_EDGE_FLIP,
    TWO_MODULE,
    exact_reference_to_module_valley_depth,
    global_topology_phase,
    intrinsic_topology_payoffs,
    module_accessibility_regime,
    reference_is_single_edge_local_optimum,
    reference_to_module_valley_depth,
    worked_example_summary,
)


def test_exact_global_topology_cost_phases():
    assert global_topology_phase(0.2) == "full_differentiation"
    assert global_topology_phase(0.4) == "two_module"
    assert global_topology_phase(1.3) == "two_module"
    assert global_topology_phase(2.0) == "fully_coupled"
    assert global_topology_phase(K_FULL_TO_MODULE) == "full_vs_two_module_boundary"
    assert global_topology_phase(K_MODULE_TO_REFERENCE) == "two_module_vs_reference_boundary"


def test_global_best_topology_matches_phase_representatives():
    low = intrinsic_topology_payoffs(0.2)
    middle = intrinsic_topology_payoffs(0.7)
    high = intrinsic_topology_payoffs(2.0)
    assert max(low, key=low.get) == FULLY_RELEASED
    assert max(middle, key=middle.get) == TWO_MODULE
    assert max(high, key=high.get) == FULLY_COUPLED


def test_accessibility_splits_inside_same_two_module_global_phase():
    assert module_accessibility_regime(0.4) == "infinitesimal_pressure_path"
    assert module_accessibility_regime(0.7) == "finite_edge_flip_path"
    assert module_accessibility_regime(1.3) == "single_edge_fitness_valley"
    assert module_accessibility_regime(K_LOCAL_PRESSURE) == "infinitesimal_release_boundary"
    assert module_accessibility_regime(K_SINGLE_EDGE_FLIP) == "single_edge_flip_boundary"


def test_reference_local_optimum_changes_at_full_edge_flip_threshold():
    assert not reference_is_single_edge_local_optimum(1.0)
    assert reference_is_single_edge_local_optimum(1.2)


def test_valley_depth_is_exact_k_minus_nine_eighths():
    for edge_cost in [1.2, 1.3, 1.5]:
        observed = reference_to_module_valley_depth(edge_cost)
        expected = edge_cost - 9.0 / 8.0
        assert isclose(observed, expected, abs_tol=1e-12)
        assert isclose(
            exact_reference_to_module_valley_depth(edge_cost),
            expected,
            abs_tol=1e-12,
        )


def test_no_single_edge_valley_before_nine_eighths():
    for edge_cost in [0.4, 0.7, 1.0]:
        assert isclose(reference_to_module_valley_depth(edge_cost), 0.0, abs_tol=1e-12)
        assert isclose(
            exact_reference_to_module_valley_depth(edge_cost),
            0.0,
            abs_tol=1e-12,
        )


def test_worked_summary_reports_accessibility_not_just_global_optimum():
    accessible = worked_example_summary(0.4)
    jump = worked_example_summary(0.7)
    trapped = worked_example_summary(1.3)
    assert accessible["best_topology"] == TWO_MODULE
    assert jump["best_topology"] == TWO_MODULE
    assert trapped["best_topology"] == TWO_MODULE
    assert accessible["accessibility"] == "infinitesimal_pressure_path"
    assert jump["accessibility"] == "finite_edge_flip_path"
    assert trapped["accessibility"] == "single_edge_fitness_valley"
    assert float(trapped["reference_to_module_valley_depth"]) > 0.0
