from math import isclose, sqrt

import pytest

from src.environment_mosaic import invasion_exponent, largest_symmetric_eigenvalue


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)


def test_two_by_two_offdiagonal_eigenvalue_survives_common_rescaling():
    for scale in SCALES:
        observed = largest_symmetric_eigenvalue(
            ((0.0, scale), (scale, 0.0))
        )
        assert isclose(observed / scale, 1.0, rel_tol=1e-12, abs_tol=0.0)


def test_three_by_three_largest_eigenvalue_is_scale_covariant():
    base = (
        (2.0, 1.0, 0.0),
        (1.0, 2.0, 1.0),
        (0.0, 1.0, 2.0),
    )
    expected = 2.0 + sqrt(2.0)
    for scale in SCALES:
        matrix = tuple(tuple(scale * value for value in row) for row in base)
        observed = largest_symmetric_eigenvalue(matrix)
        assert isclose(
            observed / scale,
            expected,
            rel_tol=1e-12,
            abs_tol=1e-14,
        )


def test_invasion_exponent_covaries_with_common_rate_scale():
    adjacency = ((0.0, 1.0), (1.0, 0.0))
    base_margins = (0.5, -1.5)
    base_migration = 0.2
    reference = invasion_exponent(base_margins, adjacency, base_migration)

    for scale in SCALES:
        observed = invasion_exponent(
            tuple(scale * value for value in base_margins),
            adjacency,
            scale * base_migration,
        )
        assert isclose(
            observed / scale,
            reference,
            rel_tol=1e-12,
            abs_tol=1e-14,
        )


def test_material_asymmetry_is_rejected_at_every_matrix_scale():
    for scale in SCALES:
        with pytest.raises(ValueError, match="symmetric"):
            largest_symmetric_eigenvalue(
                ((0.0, scale), (2.0 * scale, 0.0))
            )


def test_nonfinite_matrix_entry_fails_closed():
    with pytest.raises(ValueError, match="finite"):
        largest_symmetric_eigenvalue(((0.0, float("nan")), (float("nan"), 0.0)))


def test_zero_matrix_is_exactly_zero():
    assert largest_symmetric_eigenvalue(((0.0, 0.0), (0.0, 0.0))) == 0.0
