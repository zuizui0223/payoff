from math import isclose, isfinite

import pytest

from src.payoff_game import n_function_conflict


BASE_WEIGHTS = (1.0, 2.0, 3.0)
BASE_OPTIMA = (-1.0, 0.5, 2.0)


def _scaled(q: float):
    coefficient_scale = q * q
    return (
        tuple(w / coefficient_scale for w in BASE_WEIGHTS),
        tuple(theta * q for theta in BASE_OPTIMA),
    )


def test_n_function_conflict_identity_is_coordinate_unit_invariant():
    z0, variance0, pairwise0 = n_function_conflict(BASE_WEIGHTS, BASE_OPTIMA)
    assert z0 == 1.0
    assert variance0 == 7.5
    assert pairwise0 == 7.5

    for q in (1e-150, 1e-100, 1.0, 1e100, 1e150):
        weights, optima = _scaled(q)
        z, variance_load, pairwise_load = n_function_conflict(weights, optima)
        assert all(isfinite(value) for value in (z, variance_load, pairwise_load))
        assert isclose(z / q, z0, rel_tol=4e-12, abs_tol=0.0)
        assert isclose(variance_load, variance0, rel_tol=4e-12, abs_tol=0.0)
        assert isclose(pairwise_load, pairwise0, rel_tol=4e-12, abs_tol=0.0)
        assert isclose(variance_load, pairwise_load, rel_tol=4e-12, abs_tol=0.0)


def test_pairwise_form_does_not_underflow_when_weight_products_do():
    weights, optima = _scaled(1e150)
    assert weights[0] * weights[1] == 0.0
    _, variance_load, pairwise_load = n_function_conflict(weights, optima)
    assert isclose(variance_load, 7.5, rel_tol=4e-12, abs_tol=0.0)
    assert isclose(pairwise_load, 7.5, rel_tol=4e-12, abs_tol=0.0)


def test_variance_form_does_not_overflow_when_raw_coordinate_square_would():
    weights, optima = _scaled(1e-150)
    raw_delta = optima[0] - optima[2]
    assert isfinite(raw_delta)
    # Weight magnitudes are close to the top of the float range, while the
    # physical weighted squared difference remains ordinary.
    _, variance_load, pairwise_load = n_function_conflict(weights, optima)
    assert isclose(variance_load, 7.5, rel_tol=4e-12, abs_tol=0.0)
    assert isclose(pairwise_load, 7.5, rel_tol=4e-12, abs_tol=0.0)


def test_n_function_conflict_rejects_nonfinite_inputs():
    with pytest.raises(ValueError):
        n_function_conflict((1.0, float("inf")), (0.0, 1.0))
    with pytest.raises(ValueError):
        n_function_conflict((1.0, 2.0), (0.0, float("nan")))
