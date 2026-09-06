from math import isclose

from src.hard_module_accessibility import (
    greedy_hard_split_path,
    split_tree_accessibility,
    target_is_split_accessible,
    tree_split_gains,
)
from src.hard_module_partition import optimal_penalized_partition


def test_three_function_full_separation_accessibility_threshold_is_two():
    theta = [0.0, 1.0, 3.0]
    weights = [1.0, 1.0, 1.0]
    result = split_tree_accessibility(theta, weights, [(0,), (1,), (2,)])
    assert isclose(result["accessibility_threshold"], 2.0, rel_tol=1e-12)
    gains = tree_split_gains(result["tree"])
    assert isclose(min(gains), 2.0, rel_tol=1e-12)
    assert target_is_split_accessible(theta, weights, [(0,), (1,), (2,)], 1.0)
    assert not target_is_split_accessible(theta, weights, [(0,), (1,), (2,)], 2.1)


def test_registered_four_function_greedy_can_miss_accessible_global_optimum():
    theta = [0.0, 1.0, 2.0, 3.0]
    weights = [2.0, 1.0, 1.0, 2.0]
    kappa = 0.75

    global_best = optimal_penalized_partition(theta, weights, kappa)
    assert global_best["modules"] == ((0,), (1, 2), (3,))
    assert isclose(global_best["within_loss"], 0.5, rel_tol=1e-12)
    assert isclose(global_best["architecture_cost"], 1.5, rel_tol=1e-12)

    path = greedy_hard_split_path(theta, weights, kappa)
    assert path[-1]["modules"] == ((0, 1), (2, 3))
    assert len(path) == 2
    assert isclose(path[0]["next_split_gain"], 49.0 / 6.0, rel_tol=1e-12)
    assert path[-1]["next_split_margin"] < 0.0

    access = split_tree_accessibility(theta, weights, global_best["modules"])
    assert isclose(access["accessibility_threshold"], 9.0 / 4.0, rel_tol=1e-12)
    assert target_is_split_accessible(theta, weights, global_best["modules"], kappa)
    gains = sorted(tree_split_gains(access["tree"]))
    assert len(gains) == 2
    assert isclose(gains[0], 9.0 / 4.0, rel_tol=1e-12)
    assert isclose(gains[1], 27.0 / 4.0, rel_tol=1e-12)


def test_accessible_target_need_not_be_global_optimum():
    theta = [0.0, 1.0, 3.0]
    weights = [1.0, 1.0, 1.0]
    kappa = 1.0
    global_best = optimal_penalized_partition(theta, weights, kappa)
    assert global_best["modules"] == ((0, 1), (2,))

    full_separation = [(0,), (1,), (2,)]
    assert target_is_split_accessible(theta, weights, full_separation, kappa)
    access = split_tree_accessibility(theta, weights, full_separation)
    assert isclose(access["accessibility_threshold"], 2.0, rel_tol=1e-12)
