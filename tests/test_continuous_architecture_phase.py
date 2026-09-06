from math import isclose

from src.continuous_architecture import endpoint_mixture_frequency
from src.continuous_architecture_phase import (
    branching_feedback_threshold,
    classify_global_phase,
    endpoint_frequency_from_alpha,
    endpoint_polymorphism_midpoint,
    endpoint_polymorphism_width,
    strong_feedback_alpha_boundaries,
)


def test_branching_line_joins_intrinsic_boundaries():
    L = 2.0
    kappa = 1.0
    assert isclose(branching_feedback_threshold(kappa), -0.5)

    # Just below the threshold the strong-feedback wedge tends to [0,kappa L].
    lower, upper = strong_feedback_alpha_boundaries(L, kappa, -0.500000001)
    assert abs(lower) < 1e-8
    assert isclose(upper, kappa * L, rel_tol=1e-8, abs_tol=1e-8)


def test_strong_feedback_wedge_width_and_midpoint():
    L = 3.0
    kappa = 1.2
    gamma = -1.0
    lower, upper = strong_feedback_alpha_boundaries(L, kappa, gamma)
    assert isclose(upper - lower, 2.0 * abs(gamma) * L)
    assert isclose(
        0.5 * (lower + upper),
        endpoint_polymorphism_midpoint(L, kappa),
    )
    assert isclose(endpoint_polymorphism_width(L, kappa, gamma), 6.0)


def test_global_phase_classification_across_feedback_regions():
    L = 2.0
    kappa = 1.0

    # Variance-penalizing side.
    assert classify_global_phase(-0.1, L, kappa, 0.0) == "shared_monomorph"
    assert classify_global_phase(0.6, L, kappa, 0.0) == "partial_monomorph"
    assert classify_global_phase(2.2, L, kappa, 0.0) == "full_monomorph"

    # Threshold.
    assert classify_global_phase(-0.1, L, kappa, -0.5) == "shared_endpoint"
    assert classify_global_phase(0.6, L, kappa, -0.5) == "neutral_variance_manifold"
    assert classify_global_phase(2.2, L, kappa, -0.5) == "full_endpoint"

    # Strong dissimilarity feedback expands polymorphism beyond [0,kappa L].
    gamma = -1.0
    lower, upper = strong_feedback_alpha_boundaries(L, kappa, gamma)
    assert lower < 0.0
    assert upper > kappa * L
    assert classify_global_phase(lower - 0.1, L, kappa, gamma) == "shared_endpoint"
    assert classify_global_phase(0.6, L, kappa, gamma) == "endpoint_polymorphism"
    assert classify_global_phase(upper + 0.1, L, kappa, gamma) == "full_endpoint"


def test_phase_frequency_formula_matches_continuous_model():
    L = 2.0
    kappa = 1.0
    gamma = -0.8
    c1 = 0.4
    alpha = 1.0 - c1
    phase_p = endpoint_frequency_from_alpha(alpha, L, kappa, gamma)
    model_p = endpoint_mixture_frequency(L, c1, kappa, gamma)
    assert isclose(phase_p, model_p, rel_tol=1e-12, abs_tol=1e-12)


def test_endpoint_frequency_moves_toward_half_under_stronger_dissimilarity():
    L = 2.0
    kappa = 1.0
    alpha = 0.6
    p1 = endpoint_frequency_from_alpha(alpha, L, kappa, -0.6)
    p2 = endpoint_frequency_from_alpha(alpha, L, kappa, -1.0)
    p3 = endpoint_frequency_from_alpha(alpha, L, kappa, -10.0)
    assert abs(p2 - 0.5) < abs(p1 - 0.5)
    assert abs(p3 - 0.5) < abs(p2 - 0.5)
