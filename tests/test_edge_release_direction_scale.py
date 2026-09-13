from src.edgewise_modularity import edge_release_receipt, recovery_gradient


def test_edge_release_direction_is_invariant_to_trait_units():
    weights = [1.0, 1.0]
    edges = [(0, 1)]
    reference = [1.0]
    decoupling = [0.2]

    for trait_scale in (1e-8, 1.0, 1e8):
        optima = [0.0, 2.0 * trait_scale]
        pressure = recovery_gradient(
            optima, weights, edges, reference, decoupling
        )[0]

        more = edge_release_receipt(
            optima, weights, edges, reference, decoupling, [0.5 * pressure]
        )[0]
        less = edge_release_receipt(
            optima, weights, edges, reference, decoupling, [2.0 * pressure]
        )[0]
        balance = edge_release_receipt(
            optima, weights, edges, reference, decoupling, [pressure]
        )[0]

        assert more["direction"] == "favor_more_decoupling"
        assert less["direction"] == "favor_more_coupling"
        assert balance["direction"] == "marginal_balance"


def test_zero_pressure_and_zero_cost_are_exact_marginal_balance():
    receipt = edge_release_receipt(
        [1.0, 1.0],
        [1.0, 1.0],
        [(0, 1)],
        [1.0],
        [0.0],
        [0.0],
    )[0]
    assert receipt["pressure"] == 0.0
    assert receipt["margin"] == 0.0
    assert receipt["direction"] == "marginal_balance"
