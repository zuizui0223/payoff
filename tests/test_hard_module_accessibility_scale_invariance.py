from math import isclose

from src.hard_module_accessibility import (
    greedy_hard_split_path,
    split_tree_accessibility,
    target_is_split_accessible,
)


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)


def _scaled_weights(scale: float):
    return [scale, scale, scale]


def _root_children(tree):
    children = tree["children"]
    assert children is not None
    left, right = children
    return tuple(left["module"]), tuple(right["module"])


def test_target_accessibility_and_threshold_are_invariant_to_payoff_scale():
    theta = [0.0, 1.0, 3.0]
    target = [(0,), (1,), (2,)]

    for scale in SCALES:
        weights = _scaled_weights(scale)
        result = split_tree_accessibility(theta, weights, target)
        assert isclose(
            result["accessibility_threshold"] / scale,
            2.0,
            rel_tol=1e-12,
        )
        assert target_is_split_accessible(theta, weights, target, 1.0 * scale)
        assert not target_is_split_accessible(theta, weights, target, 2.0 * scale)
        assert not target_is_split_accessible(theta, weights, target, 2.1 * scale)


def test_greedy_split_sequence_is_invariant_to_payoff_scale():
    theta = [0.0, 1.0, 3.0]

    reference_modules = None
    reference_splits = None
    for scale in SCALES:
        path = greedy_hard_split_path(
            theta,
            _scaled_weights(scale),
            1.0 * scale,
        )
        modules = tuple(row["modules"] for row in path)
        splits = tuple(row["next_split"] for row in path)
        if reference_modules is None:
            reference_modules = modules
            reference_splits = splits
        else:
            assert modules == reference_modules
            assert splits == reference_splits

        assert len(path) == 2
        assert path[-1]["modules"] == ((0, 1), (2,))
        assert path[0]["next_split_gain"] / scale > 1.0
        assert path[-1]["next_split_margin"] / scale < 0.0


def test_maximin_witness_tree_is_invariant_when_better_cut_arrives_later():
    # cut=1 is visited first but has threshold 0.5; cut=2 has threshold 2.0.
    # A fixed absolute 1e-15 tie band incorrectly keeps cut=1 at tiny scales.
    theta = [0.0, 2.0, 3.0]
    target = [(0,), (1,), (2,)]

    for scale in SCALES:
        result = split_tree_accessibility(theta, _scaled_weights(scale), target)
        assert isclose(
            result["accessibility_threshold"] / scale,
            2.0,
            rel_tol=1e-12,
        )
        assert _root_children(result["tree"]) == ((0, 1), (2,))


def test_single_module_target_is_always_accessible_for_finite_nonnegative_cost():
    theta = [0.0, 1.0, 3.0]
    target = [(0, 1, 2)]
    for scale in SCALES:
        assert target_is_split_accessible(
            theta,
            _scaled_weights(scale),
            target,
            10.0 * scale,
        )
