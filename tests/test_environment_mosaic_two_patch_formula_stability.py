from math import isclose, isfinite

from src.environment_mosaic import (
    two_patch_invasion_exponent,
    two_patch_rescue_threshold,
)


SCALES = (1e-200, 1e-100, 1.0, 1e100, 1e200)
R1 = 0.5
R2 = -1.5
MIGRATION = 0.2
BASE_EXPONENT = two_patch_invasion_exponent(R1, R2, MIGRATION)
BASE_THRESHOLD = two_patch_rescue_threshold(R1, R2)


def test_two_patch_invasion_exponent_covaries_across_extreme_scales():
    for scale in SCALES:
        observed = two_patch_invasion_exponent(
            scale * R1,
            scale * R2,
            scale * MIGRATION,
        )
        assert isfinite(observed)
        assert isclose(
            observed / scale,
            BASE_EXPONENT,
            rel_tol=1e-12,
            abs_tol=1e-14,
        )


def test_two_patch_rescue_threshold_covaries_across_extreme_scales():
    for scale in SCALES:
        observed = two_patch_rescue_threshold(scale * R1, scale * R2)
        assert isfinite(observed)
        assert observed > 0.0
        assert isclose(
            observed / scale,
            BASE_THRESHOLD,
            rel_tol=1e-12,
            abs_tol=0.0,
        )


def test_tiny_rescue_threshold_does_not_underflow_to_zero():
    scale = 1e-200
    observed = two_patch_rescue_threshold(scale * R1, scale * R2)
    assert observed > 0.0
    assert isclose(observed / scale, BASE_THRESHOLD, rel_tol=1e-12)


def test_large_invasion_norm_does_not_overflow():
    scale = 1e200
    observed = two_patch_invasion_exponent(
        scale * R1,
        scale * R2,
        scale * MIGRATION,
    )
    assert isfinite(observed)
    assert isclose(observed / scale, BASE_EXPONENT, rel_tol=1e-12)
