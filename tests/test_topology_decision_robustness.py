from math import isclose

from src.topology_decision_robustness import (
    decision_robustness_summary,
    first_edge_decision_radius,
    global_best_decision_radius,
)


def test_three_function_first_edge_radius_is_five_thirty_seconds():
    margins = (-27.0 / 80.0, 13.0 / 80.0, -3.0 / 20.0)
    receipt = first_edge_decision_radius(margins)
    assert receipt["best_edge_index"] == 1
    assert isclose(float(receipt["best_margin"]), 13.0 / 80.0, abs_tol=1e-12)
    assert isclose(float(receipt["second_margin"]), -3.0 / 20.0, abs_tol=1e-12)
    assert isclose(float(receipt["ranking_gap"]), 5.0 / 16.0, abs_tol=1e-12)
    assert isclose(
        float(receipt["uniform_margin_perturbation_radius"]),
        5.0 / 32.0,
        abs_tol=1e-12,
    )


def test_global_best_uniform_payoff_radius_is_half_global_reserve():
    assert isclose(global_best_decision_radius(1.0 / 15.0), 1.0 / 30.0, abs_tol=1e-12)


def test_summary_keeps_edge_and_global_radii_distinct():
    summary = decision_robustness_summary(
        (-27.0 / 80.0, 13.0 / 80.0, -3.0 / 20.0),
        1.0 / 15.0,
    )
    assert isclose(
        float(summary["uniform_margin_perturbation_radius"]),
        5.0 / 32.0,
        abs_tol=1e-12,
    )
    assert isclose(
        float(summary["uniform_topology_payoff_perturbation_radius"]),
        1.0 / 30.0,
        abs_tol=1e-12,
    )
    assert float(summary["uniform_margin_perturbation_radius"]) > float(
        summary["uniform_topology_payoff_perturbation_radius"]
    )


def test_radius_requires_positive_unique_first_edge():
    for margins in [(0.0, -1.0), (-0.1, -0.2), (1.0, 1.0)]:
        try:
            first_edge_decision_radius(margins)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
