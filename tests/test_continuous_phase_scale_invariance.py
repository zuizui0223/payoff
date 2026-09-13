from __future__ import annotations

import pytest

from src.continuous_architecture_phase import (
    classify_global_phase,
    endpoint_frequency_from_alpha,
    strong_feedback_alpha_boundaries,
)
from src.convex_architecture_local import local_branching_regime


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)


def test_local_branching_regime_is_invariant_to_curvature_units():
    for scale in SCALES:
        curvature = 1.6 * scale
        threshold = -0.8 * scale
        assert local_branching_regime(curvature, threshold + 0.1 * scale) == "local_ess"
        assert local_branching_regime(curvature, threshold) == "second_order_neutral"
        assert local_branching_regime(curvature, threshold - 0.1 * scale) == "branching_compatible"


def test_global_phase_is_invariant_on_variance_penalizing_side():
    L = 2.0
    for scale in SCALES:
        kappa = 1.0 * scale
        gamma = 0.0
        assert classify_global_phase(-0.1 * scale, L, kappa, gamma) == "shared_monomorph"
        assert classify_global_phase(0.6 * scale, L, kappa, gamma) == "partial_monomorph"
        assert classify_global_phase(2.2 * scale, L, kappa, gamma) == "full_monomorph"


def test_global_phase_is_invariant_on_exact_branching_line():
    L = 2.0
    for scale in SCALES:
        kappa = 1.0 * scale
        gamma = -0.5 * scale
        assert classify_global_phase(-0.1 * scale, L, kappa, gamma) == "shared_endpoint"
        assert classify_global_phase(0.6 * scale, L, kappa, gamma) == "neutral_variance_manifold"
        assert classify_global_phase(2.2 * scale, L, kappa, gamma) == "full_endpoint"


def test_strong_feedback_endpoint_polymorphism_geometry_is_scale_invariant():
    L = 2.0
    for scale in SCALES:
        kappa = 1.0 * scale
        gamma = -1.0 * scale
        lower, upper = strong_feedback_alpha_boundaries(L, kappa, gamma)
        assert lower == pytest.approx(-1.0 * scale)
        assert upper == pytest.approx(3.0 * scale)
        assert classify_global_phase(lower - 0.1 * scale, L, kappa, gamma) == "shared_endpoint"
        assert classify_global_phase(0.6 * scale, L, kappa, gamma) == "endpoint_polymorphism"
        assert classify_global_phase(upper + 0.1 * scale, L, kappa, gamma) == "full_endpoint"


def test_endpoint_frequency_is_invariant_to_common_coefficient_rescaling():
    L = 2.0
    expected = endpoint_frequency_from_alpha(0.6, L, 1.0, -0.8)
    for scale in SCALES:
        observed = endpoint_frequency_from_alpha(
            0.6 * scale,
            L,
            1.0 * scale,
            -0.8 * scale,
        )
        assert observed == pytest.approx(expected, rel=2e-15, abs=2e-15)


def test_exact_alpha_endpoints_remain_boundaries_at_every_scale():
    L = 2.0
    for scale in SCALES:
        kappa = 1.0 * scale
        assert classify_global_phase(0.0, L, kappa, 0.0) == "shared_monomorph"
        assert classify_global_phase(kappa * L, L, kappa, 0.0) == "full_monomorph"
        assert classify_global_phase(0.0, L, kappa, -0.5 * scale) == "shared_endpoint"
        assert classify_global_phase(kappa * L, L, kappa, -0.5 * scale) == "full_endpoint"
