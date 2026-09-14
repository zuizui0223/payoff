import pytest

from src.interaction_kernel_robustness import kernel_weight


SCALES = (1e-200, 1e-100, 1.0, 1e100, 1e200)


def test_hard_kernel_inside_boundary_outside_are_scale_invariant():
    for scale in SCALES:
        epsilon = scale
        assert kernel_weight(0.5 * scale, epsilon=epsilon, kernel="hard") == 1.0
        assert kernel_weight(1.0 * scale, epsilon=epsilon, kernel="hard") == 1.0
        assert kernel_weight(2.0 * scale, epsilon=epsilon, kernel="hard") == 0.0


def test_tiny_clear_outside_point_is_not_swallowed_by_absolute_slack():
    assert kernel_weight(2e-16, epsilon=1e-16, kernel="hard") == 0.0


def test_distance_sign_does_not_change_hard_kernel_weight():
    for scale in SCALES:
        assert kernel_weight(-0.5 * scale, epsilon=scale, kernel="hard") == 1.0
        assert kernel_weight(-2.0 * scale, epsilon=scale, kernel="hard") == 0.0


def test_nonfinite_distance_fails_closed():
    for value in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(ValueError, match="finite"):
            kernel_weight(value, epsilon=1.0, kernel="hard")
