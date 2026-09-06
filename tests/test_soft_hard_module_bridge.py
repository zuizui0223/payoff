from math import isclose

from src.edgewise_modularity import optimized_loss, optimized_phenotype
from src.hard_module_partition import hard_partition_loss, weighted_shared_loss


def test_three_function_soft_module_converges_to_hard_partition():
    theta = [0.0, 1.0, 3.0]
    weights = [1.0, 1.0, 1.0]
    edges = [(0, 1)]
    hard = hard_partition_loss(theta, weights, [(0, 1), (2,)])
    assert isclose(hard, 0.5, rel_tol=1e-12)

    losses = [
        optimized_loss(theta, weights, edges, [coupling])
        for coupling in [0.0, 1.0, 10.0, 1e6]
    ]
    assert isclose(losses[0], 0.0, abs_tol=1e-12)
    assert isclose(losses[1], 1.0 / 3.0, rel_tol=1e-12)
    assert losses[0] < losses[1] < losses[2] < losses[3] < hard
    assert isclose(losses[3], hard, rel_tol=1e-6, abs_tol=1e-6)


def test_hard_recovery_is_lower_bound_on_soft_recovery_for_same_grouping():
    theta = [0.0, 1.0, 3.0]
    weights = [1.0, 1.0, 1.0]
    full_shared = weighted_shared_loss(theta, weights)
    hard_loss = hard_partition_loss(theta, weights, [(0, 1), (2,)])
    hard_recovery = full_shared - hard_loss

    for coupling in [0.1, 1.0, 5.0, 100.0]:
        soft_loss = optimized_loss(theta, weights, [(0, 1)], [coupling])
        soft_recovery = full_shared - soft_loss
        assert soft_recovery >= hard_recovery - 1e-12


def test_registered_soft_flexibility_reserve_at_unit_coupling():
    theta = [0.0, 1.0, 3.0]
    weights = [1.0, 1.0, 1.0]
    hard_loss = hard_partition_loss(theta, weights, [(0, 1), (2,)])
    soft_loss = optimized_loss(theta, weights, [(0, 1)], [1.0])
    assert isclose(hard_loss - soft_loss, 1.0 / 6.0, rel_tol=1e-12)
    phenotype = optimized_phenotype(theta, weights, [(0, 1)], [1.0])
    assert all(
        isclose(value, expected, rel_tol=1e-12, abs_tol=1e-12)
        for value, expected in zip(phenotype, [1.0 / 3.0, 2.0 / 3.0, 3.0])
    )
