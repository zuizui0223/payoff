from math import isclose, inf

from src.hard_module_partition import (
    between_module_recovery,
    fixed_k_loss_curve,
    hard_partition_loss,
    hard_partition_recovery,
    module_count_intervals,
    optimal_contiguous_partition_fixed_k,
    optimal_penalized_partition,
    pairwise_module_recovery,
    split_gain,
    weighted_shared_loss,
)


def test_partition_recovery_equals_between_and_pairwise_module_forms():
    theta = [0.0, 1.0, 3.0, 4.0]
    weights = [1.0, 2.0, 1.5, 0.5]
    partition = [(0, 1), (2, 3)]
    direct = hard_partition_recovery(theta, weights, partition)
    between = between_module_recovery(theta, weights, partition)
    pairwise = pairwise_module_recovery(theta, weights, partition)
    assert isclose(direct, between, rel_tol=1e-12, abs_tol=1e-12)
    assert isclose(direct, pairwise, rel_tol=1e-12, abs_tol=1e-12)


def test_split_gain_is_exact_weighted_variance_decomposition():
    theta = [0.0, 1.0, 3.0]
    weights = [1.0, 1.0, 1.0]
    whole = hard_partition_loss(theta, weights, [(0, 1, 2)])
    split = hard_partition_loss(theta, weights, [(0, 1), (2,)])
    gain = split_gain(theta, weights, (0, 1), (2,))
    assert isclose(whole - split, gain, rel_tol=1e-12, abs_tol=1e-12)
    assert isclose(gain, 25.0 / 6.0, rel_tol=1e-12, abs_tol=1e-12)


def test_registered_three_function_fixed_k_losses_and_partitions():
    theta = [0.0, 1.0, 3.0]
    weights = [1.0, 1.0, 1.0]
    curve = fixed_k_loss_curve(theta, weights)
    assert len(curve) == 3
    assert isclose(curve[0]["within_loss"], 14.0 / 3.0, rel_tol=1e-12)
    assert curve[0]["modules"] == ((0, 1, 2),)
    assert isclose(curve[1]["within_loss"], 0.5, rel_tol=1e-12)
    assert curve[1]["modules"] == ((0, 1), (2,))
    assert isclose(curve[2]["within_loss"], 0.0, abs_tol=1e-12)
    assert curve[2]["modules"] == ((0,), (1,), (2,))


def test_penalized_three_function_phase_regions():
    theta = [0.0, 1.0, 3.0]
    weights = [1.0, 1.0, 1.0]

    low = optimal_penalized_partition(theta, weights, 0.2)
    assert low["module_count"] == 3
    assert low["modules"] == ((0,), (1,), (2,))

    middle = optimal_penalized_partition(theta, weights, 1.0)
    assert middle["module_count"] == 2
    assert middle["modules"] == ((0, 1), (2,))

    high = optimal_penalized_partition(theta, weights, 5.0)
    assert high["module_count"] == 1
    assert high["modules"] == ((0, 1, 2),)


def test_module_count_intervals_match_registered_thresholds():
    theta = [0.0, 1.0, 3.0]
    weights = [1.0, 1.0, 1.0]
    intervals = {row["module_count"]: row for row in module_count_intervals(theta, weights)}
    assert set(intervals) == {1, 2, 3}

    assert isclose(intervals[3]["lower_cost"], 0.0, abs_tol=1e-12)
    assert isclose(intervals[3]["upper_cost"], 0.5, rel_tol=1e-12)

    assert isclose(intervals[2]["lower_cost"], 0.5, rel_tol=1e-12)
    assert isclose(intervals[2]["upper_cost"], 25.0 / 6.0, rel_tol=1e-12)
    assert intervals[2]["modules"] == ((0, 1), (2,))

    assert isclose(intervals[1]["lower_cost"], 25.0 / 6.0, rel_tol=1e-12)
    assert intervals[1]["upper_cost"] == inf


def test_penalized_boundaries_are_ties():
    theta = [0.0, 1.0, 3.0]
    weights = [1.0, 1.0, 1.0]
    shared = weighted_shared_loss(theta, weights)

    # At kappa=1/2, two and three modules tie in net gain.
    kappa = 0.5
    best2 = optimal_contiguous_partition_fixed_k(theta, weights, 2)
    best3 = optimal_contiguous_partition_fixed_k(theta, weights, 3)
    phi2 = shared - best2["within_loss"] - kappa * (2 - 1)
    phi3 = shared - best3["within_loss"] - kappa * (3 - 1)
    assert isclose(phi2, phi3, rel_tol=1e-12, abs_tol=1e-12)

    # At kappa=25/6, one and two modules tie.
    kappa = 25.0 / 6.0
    best1 = optimal_contiguous_partition_fixed_k(theta, weights, 1)
    phi1 = shared - best1["within_loss"] - kappa * 0
    phi2 = shared - best2["within_loss"] - kappa * 1
    assert isclose(phi1, phi2, rel_tol=1e-12, abs_tol=1e-12)


def test_unsorted_input_maps_back_to_original_function_indices():
    theta = [3.0, 0.0, 1.0]
    weights = [1.0, 1.0, 1.0]
    result = optimal_contiguous_partition_fixed_k(theta, weights, 2)
    # Sorted theta order is original indices 1,2,0; best blocks are {1,2}|{0}.
    assert result["sorted_order"] == (1, 2, 0)
    assert result["modules"] == ((1, 2), (0,))
    assert isclose(result["within_loss"], 0.5, rel_tol=1e-12)
