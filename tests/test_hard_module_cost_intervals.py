from math import isclose

from src.hard_module_cost_intervals import (
    common_kappa_interval,
    interval_gap,
    intervals_overlap,
    partition_kappa_interval,
    predicted_margin_interval,
)


def test_partition_kappa_interval_propagation():
    interval = partition_kappa_interval(
        recovery_interval=(4.0, 4.3),
        direct_margin_interval=(3.0, 3.3),
        module_count=2,
    )
    assert isclose(interval[0], 0.7, rel_tol=1e-12)
    assert isclose(interval[1], 1.3, rel_tol=1e-12)


def test_common_kappa_interval_is_exact_intersection():
    result = common_kappa_interval(
        recovery_intervals=[(4.0, 4.3), (4.5, 4.8)],
        direct_margin_intervals=[(3.0, 3.3), (2.5, 2.8)],
        module_counts=[2, 3],
    )
    assert result["compatible"] is True
    assert isclose(result["common_lower"], 0.85, rel_tol=1e-12)
    assert isclose(result["common_upper"], 1.15, rel_tol=1e-12)


def test_disjoint_partition_cost_intervals_reject_common_kappa():
    result = common_kappa_interval(
        recovery_intervals=[(4.0, 4.1), (4.5, 4.6)],
        direct_margin_intervals=[(3.8, 3.9), (1.5, 1.6)],
        module_counts=[2, 3],
    )
    assert result["compatible"] is False
    assert result["common_lower"] > result["common_upper"]


def test_heldout_margin_interval_and_overlap_diagnostics():
    predicted = predicted_margin_interval(
        recovery_interval=(4.5, 4.8),
        kappa_interval=(0.85, 1.15),
        module_count=3,
    )
    assert isclose(predicted[0], 2.2, rel_tol=1e-12)
    assert isclose(predicted[1], 3.1, rel_tol=1e-12)

    assert intervals_overlap(predicted, (2.8, 3.2))
    assert isclose(interval_gap(predicted, (2.8, 3.2)), 0.0, abs_tol=1e-12)

    assert not intervals_overlap(predicted, (3.3, 3.5))
    assert isclose(interval_gap(predicted, (3.3, 3.5)), 0.2, rel_tol=1e-12)
