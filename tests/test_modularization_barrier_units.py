import pytest

from src.modularization_barrier import (
    generic_decoupling_thresholds,
    two_function_classify_cost,
    two_function_release_thresholds,
)


def test_all_cost_regimes_are_invariant_to_trait_units():
    expected = (
        "locally_accessible_release",
        "local_neutral_boundary",
        "finite_jump_barrier",
        "global_endpoint_neutral_boundary",
        "retained_coupling",
    )

    for trait_scale in (1e-8, 1.0, 1e8):
        gap = 2.0 * trait_scale
        summary = two_function_release_thresholds(1.0, 1.0, gap, 1.0)
        local = summary["local_threshold"]
        global_threshold = summary["global_threshold"]
        costs = (
            0.5 * local,
            local,
            0.5 * (local + global_threshold),
            global_threshold,
            2.0 * global_threshold,
        )
        observed = tuple(
            two_function_classify_cost(1.0, 1.0, gap, 1.0, cost)
            for cost in costs
        )
        assert observed == expected


def test_convex_threshold_ordering_fails_closed_at_tiny_units():
    for scale in (1e-16, 1.0, 1e16):
        # k_local = 2*scale, k_global = (2*scale)/2 = scale.
        # The ordering violation is the same at every common recovery scale.
        with pytest.raises(ValueError, match="convex-recovery ordering"):
            generic_decoupling_thresholds(
                initial_marginal_recovery=2.0 * scale,
                full_recovery=2.0 * scale,
                max_decoupling=2.0,
            )
