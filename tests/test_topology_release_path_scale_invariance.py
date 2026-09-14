from math import isclose

from src.topology_release_path import connected_components, greedy_positive_pressure_path


OPTIMA = (0.0, 1.0, 3.0)
WEIGHTS = (1.0, 1.0, 1.0)
EDGES = ((0, 1), (0, 2), (1, 2))
COUPLINGS = (1.0, 1.0, 1.0)
COSTS = (0.4, 0.4, 0.4)


def test_connected_components_is_invariant_to_common_coupling_scale():
    edges = ((0, 1), (1, 2))
    for scale in (1e-16, 1e-8, 1.0, 1e8, 1e16):
        assert connected_components(
            3,
            edges,
            (1.0 * scale, 0.0),
        ) == ((0, 1), (2,))


def test_meaningfully_negative_coupling_fails_at_every_scale():
    edges = ((0, 1),)
    for scale in (1e-16, 1.0, 1e16):
        try:
            connected_components(2, edges, (-0.1 * scale,))
        except ValueError as exc:
            assert "non-negative" in str(exc)
        else:
            raise AssertionError("negative coupling must fail closed")


def test_greedy_release_path_is_invariant_to_trait_and_cost_units():
    reference_signature = None
    for q in (1e-8, 1.0, 1e8):
        optima = tuple(q * value for value in OPTIMA)
        costs = tuple(q * q * value for value in COSTS)
        path = greedy_positive_pressure_path(
            optima,
            WEIGHTS,
            EDGES,
            COUPLINGS,
            costs,
        )
        signature = tuple(
            (
                row["released"],
                row["components"],
                row["next_edge_index"],
            )
            for row in path
        )
        if reference_signature is None:
            reference_signature = signature
        else:
            assert signature == reference_signature

        assert len(path) == 3
        assert tuple(row["next_edge_index"] for row in path) == (1, 2, None)
        assert path[-1]["released"] == (False, True, True)
        assert path[-1]["components"] == ((0, 1), (2,))

        # Payoff-valued outputs follow the expected q^2 transformation.
        assert isclose(float(path[0]["pressures"][1]) / (q * q), 9.0 / 16.0, rel_tol=1e-11)
        assert isclose(float(path[1]["pressures"][2]) / (q * q), 49.0 / 64.0, rel_tol=1e-11)


def test_small_positive_margin_is_not_swallowed_by_absolute_payoff_floor():
    q = 1e-8
    optima = tuple(q * value for value in OPTIMA)
    costs = tuple(q * q * value for value in COSTS)
    path = greedy_positive_pressure_path(
        optima,
        WEIGHTS,
        EDGES,
        COUPLINGS,
        costs,
    )
    first_margin = float(path[0]["margins"][1])
    assert 0.0 < first_margin < 1e-12
    assert path[0]["next_edge_index"] == 1


def test_exact_release_bookkeeping_does_not_depend_on_coupling_units():
    for coupling_scale in (1e-16, 1.0, 1e16):
        couplings = tuple(coupling_scale * value for value in COUPLINGS)
        # Scale trait weights with couplings so the optimized phenotype and edge
        # pressures remain unchanged; costs therefore stay unchanged as well.
        weights = tuple(coupling_scale * value for value in WEIGHTS)
        path = greedy_positive_pressure_path(
            OPTIMA,
            weights,
            EDGES,
            couplings,
            COSTS,
        )
        assert tuple(row["next_edge_index"] for row in path) == (1, 2, None)
        assert path[1]["released"] == (False, True, False)
        assert path[2]["released"] == (False, True, True)
