from math import isclose

from src.edge_pressure_transfer import (
    edge_signed_disagreements,
    edge_transfer_matrix,
    strongest_positive_cross_transfer,
)
from src.edgewise_modularity import edge_pressures
from src.three_function_example import EDGES, OPTIMA, REFERENCE_COUPLINGS, WEIGHTS


def test_three_function_signed_edge_disagreements_are_exact():
    q = edge_signed_disagreements(OPTIMA, WEIGHTS, EDGES, REFERENCE_COUPLINGS)
    expected = (-1.0 / 4.0, -3.0 / 4.0, -1.0 / 2.0)
    assert all(isclose(a, b, abs_tol=1e-12) for a, b in zip(q, expected))


def test_three_function_transfer_matrix_is_exact_and_symmetric():
    observed = edge_transfer_matrix(OPTIMA, WEIGHTS, EDGES, REFERENCE_COUPLINGS)
    expected = (
        (1.0 / 16.0, 3.0 / 32.0, -1.0 / 16.0),
        (3.0 / 32.0, 9.0 / 16.0, 3.0 / 16.0),
        (-1.0 / 16.0, 3.0 / 16.0, 1.0 / 4.0),
    )
    for i in range(3):
        for j in range(3):
            assert isclose(observed[i][j], expected[i][j], abs_tol=1e-12)
            assert isclose(observed[i][j], observed[j][i], abs_tol=1e-12)


def test_transfer_diagonal_equals_current_edge_pressure():
    transfer = edge_transfer_matrix(OPTIMA, WEIGHTS, EDGES, REFERENCE_COUPLINGS)
    pressures = edge_pressures(OPTIMA, WEIGHTS, EDGES, REFERENCE_COUPLINGS)
    for index in range(3):
        assert isclose(transfer[index][index], pressures[index], abs_tol=1e-12)


def test_first_release_predicts_edge_12_as_strongest_positive_rerouting_target():
    transfer = edge_transfer_matrix(OPTIMA, WEIGHTS, EDGES, REFERENCE_COUPLINGS)
    result = strongest_positive_cross_transfer(transfer, 1)  # release edge 02
    assert result is not None
    edge_index, derivative = result
    assert edge_index == 2  # edge 12
    assert isclose(derivative, 3.0 / 16.0, abs_tol=1e-12)


def test_transfer_matrix_matches_finite_difference_pressure_response():
    transfer = edge_transfer_matrix(OPTIMA, WEIGHTS, EDGES, REFERENCE_COUPLINGS)
    baseline = edge_pressures(OPTIMA, WEIGHTS, EDGES, REFERENCE_COUPLINGS)
    h = 1e-6
    # Decouple edge 02 by h: c_02 = 1-h.
    perturbed_couplings = (1.0, 1.0 - h, 1.0)
    perturbed = edge_pressures(OPTIMA, WEIGHTS, EDGES, perturbed_couplings)
    for target_edge in range(3):
        derivative = (perturbed[target_edge] - baseline[target_edge]) / h
        assert isclose(
            derivative,
            transfer[target_edge][1],
            rel_tol=3e-6,
            abs_tol=3e-8,
        )


def test_transfer_quadratic_forms_are_nonnegative_for_registered_vectors():
    matrix = edge_transfer_matrix(OPTIMA, WEIGHTS, EDGES, REFERENCE_COUPLINGS)
    vectors = [
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
        (1.0, 1.0, 1.0),
        (1.0, -2.0, 0.5),
        (-0.3, 0.7, 1.4),
    ]
    for vector in vectors:
        value = sum(
            vector[i] * matrix[i][j] * vector[j]
            for i in range(3)
            for j in range(3)
        )
        assert value >= -1e-12
