from math import isclose

from src.edge_pressure_transfer import edge_transfer_matrix
from src.edgewise_modularity import optimized_phenotype
from src.three_function_example import EDGES, OPTIMA, REFERENCE_COUPLINGS, WEIGHTS


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)


def _scaled(values, scale):
    return tuple(scale * value for value in values)


def test_common_weight_coupling_rescaling_preserves_phenotype():
    reference = optimized_phenotype(
        OPTIMA,
        WEIGHTS,
        EDGES,
        REFERENCE_COUPLINGS,
    )
    for scale in SCALES:
        observed = optimized_phenotype(
            OPTIMA,
            _scaled(WEIGHTS, scale),
            EDGES,
            _scaled(REFERENCE_COUPLINGS, scale),
        )
        assert all(
            isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-14)
            for actual, expected in zip(observed, reference)
        )


def test_transfer_hessian_covaries_inversely_with_weight_coupling_scale():
    reference = edge_transfer_matrix(
        OPTIMA,
        WEIGHTS,
        EDGES,
        REFERENCE_COUPLINGS,
    )
    for scale in SCALES:
        observed = edge_transfer_matrix(
            OPTIMA,
            _scaled(WEIGHTS, scale),
            EDGES,
            _scaled(REFERENCE_COUPLINGS, scale),
        )
        for i in range(len(reference)):
            for j in range(len(reference)):
                assert isclose(
                    observed[i][j] * scale,
                    reference[i][j],
                    rel_tol=1e-11,
                    abs_tol=1e-13,
                )


def test_tiny_positive_definite_architecture_matrix_is_not_false_singular():
    scale = 1e-16
    observed = edge_transfer_matrix(
        OPTIMA,
        _scaled(WEIGHTS, scale),
        EDGES,
        _scaled(REFERENCE_COUPLINGS, scale),
    )
    assert len(observed) == len(EDGES)
    assert all(len(row) == len(EDGES) for row in observed)
