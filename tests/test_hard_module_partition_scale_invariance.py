from math import inf, isclose

from src.hard_module_partition import (
    fixed_k_loss_curve,
    module_count_intervals,
    optimal_contiguous_partition_fixed_k,
    optimal_penalized_partition,
)


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)
THETA = [0.0, 1.0, 3.0]


def _weights(scale: float):
    return [scale, scale, scale]


def test_fixed_k_optimum_and_loss_curve_are_invariant_to_weight_scale():
    for scale in SCALES:
        result = optimal_contiguous_partition_fixed_k(
            THETA,
            _weights(scale),
            2,
        )
        assert result["modules"] == ((0, 1), (2,))
        assert isclose(result["within_loss"] / scale, 0.5, rel_tol=1e-12)
        assert isclose(result["recovery"] / scale, 25.0 / 6.0, rel_tol=1e-12)

        curve = fixed_k_loss_curve(THETA, _weights(scale))
        assert tuple(row["modules"] for row in curve) == (
            ((0, 1, 2),),
            ((0, 1), (2,)),
            ((0,), (1,), (2,)),
        )
        assert isclose(curve[0]["within_loss"] / scale, 14.0 / 3.0, rel_tol=1e-12)
        assert isclose(curve[1]["within_loss"] / scale, 0.5, rel_tol=1e-12)
        assert isclose(curve[2]["within_loss"] / scale, 0.0, abs_tol=1e-15)


def test_penalized_phase_regions_are_invariant_to_common_weight_cost_scale():
    cases = (
        (0.2, 3, ((0,), (1,), (2,))),
        (1.0, 2, ((0, 1), (2,))),
        (5.0, 1, ((0, 1, 2),)),
    )
    for scale in SCALES:
        for base_cost, expected_count, expected_modules in cases:
            result = optimal_penalized_partition(
                THETA,
                _weights(scale),
                base_cost * scale,
            )
            assert result["module_count"] == expected_count
            assert result["modules"] == expected_modules
            assert isclose(
                result["architecture_cost"] / scale,
                base_cost * (expected_count - 1),
                rel_tol=1e-12,
                abs_tol=1e-15,
            )


def test_exact_penalized_ties_keep_fewer_module_preference_at_every_scale():
    for scale in SCALES:
        two_vs_three = optimal_penalized_partition(
            THETA,
            _weights(scale),
            0.5 * scale,
        )
        assert two_vs_three["module_count"] == 2
        assert two_vs_three["modules"] == ((0, 1), (2,))

        one_vs_two = optimal_penalized_partition(
            THETA,
            _weights(scale),
            (25.0 / 6.0) * scale,
        )
        assert one_vs_two["module_count"] == 1
        assert one_vs_two["modules"] == ((0, 1, 2),)


def test_module_count_interval_boundaries_scale_with_payoff_units():
    for scale in SCALES:
        rows = {row["module_count"]: row for row in module_count_intervals(THETA, _weights(scale))}
        assert set(rows) == {1, 2, 3}
        assert rows[1]["modules"] == ((0, 1, 2),)
        assert rows[2]["modules"] == ((0, 1), (2,))
        assert rows[3]["modules"] == ((0,), (1,), (2,))

        assert isclose(rows[3]["lower_cost"] / scale, 0.0, abs_tol=1e-15)
        assert isclose(rows[3]["upper_cost"] / scale, 0.5, rel_tol=1e-12)
        assert isclose(rows[2]["lower_cost"] / scale, 0.5, rel_tol=1e-12)
        assert isclose(rows[2]["upper_cost"] / scale, 25.0 / 6.0, rel_tol=1e-12)
        assert isclose(rows[1]["lower_cost"] / scale, 25.0 / 6.0, rel_tol=1e-12)
        assert rows[1]["upper_cost"] == inf
