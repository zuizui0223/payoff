from math import isclose, isfinite

from src.spatial_environment_gradient import (
    two_patch_coordination_switch_rate,
    two_patch_midpoint_exponent,
)


SCALES = (1e-200, 1e-100, 1.0, 1e100, 1e200)
PHI_1 = 0.6
PHI_2 = -0.6
ETA = 0.1
MIGRATION = 1.0
BASE_SWITCH = two_patch_coordination_switch_rate(PHI_1, PHI_2, ETA)
BASE_EXPONENT = two_patch_midpoint_exponent(PHI_1, PHI_2, ETA, MIGRATION)


def test_exact_switch_rate_covaries_across_extreme_rate_scales():
    for scale in SCALES:
        observed = two_patch_coordination_switch_rate(
            scale * PHI_1,
            scale * PHI_2,
            scale * ETA,
        )
        assert isfinite(observed)
        assert isclose(
            observed / scale,
            BASE_SWITCH,
            rel_tol=1e-12,
            abs_tol=0.0,
        )


def test_midpoint_exponent_covaries_across_extreme_rate_scales():
    for scale in SCALES:
        observed = two_patch_midpoint_exponent(
            scale * PHI_1,
            scale * PHI_2,
            scale * ETA,
            scale * MIGRATION,
        )
        assert isfinite(observed)
        assert isclose(
            observed / scale,
            BASE_EXPONENT,
            rel_tol=1e-12,
            abs_tol=1e-14,
        )


def test_tiny_switch_rate_does_not_underflow_to_zero():
    scale = 1e-200
    observed = two_patch_coordination_switch_rate(
        scale * PHI_1,
        scale * PHI_2,
        scale * ETA,
    )
    assert observed > 0.0
    assert isclose(observed / scale, BASE_SWITCH, rel_tol=1e-12)


def test_large_midpoint_norm_does_not_overflow():
    scale = 1e200
    observed = two_patch_midpoint_exponent(
        scale * PHI_1,
        scale * PHI_2,
        scale * ETA,
        scale * MIGRATION,
    )
    assert isfinite(observed)
    assert isclose(observed / scale, BASE_EXPONENT, rel_tol=1e-12)
