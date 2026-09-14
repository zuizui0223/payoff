from src.payoff_game import classify_phase
from src.topology_game import classify_pairwise_topology_game, pairwise_payoff_parameters


S = (0, 0)
T = (1, 0)
SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)

PHASE_TO_TOPOLOGY = {
    "stable_architecture_coexistence": "stable_pairwise_coexistence",
    "differentiated_dominance": "t_dominance",
    "shared_dominance": "s_dominance",
    "coordination_bistability": "coordination_bistability",
    "neutral_architecture_boundary": "boundary",
    "nonhyperbolic_phase_boundary": "boundary",
}


def _classification(phi: float, eta: float, scale: float, offset_factor: float = 0.0):
    offset = offset_factor * scale
    payoff_s = offset
    payoff_t = offset + phi * scale
    gamma = eta * scale  # q(S,T)=1 for the chosen pair.
    observed = classify_pairwise_topology_game(payoff_s, payoff_t, S, T, gamma)
    realized_phi, realized_eta = pairwise_payoff_parameters(payoff_s, payoff_t, S, T, gamma)
    expected = PHASE_TO_TOPOLOGY[classify_phase(realized_phi, realized_eta)]
    return observed, expected


def test_pairwise_topology_labels_match_canonical_phase_across_payoff_scales():
    cases = (
        (0.2, -1.0, "stable_pairwise_coexistence"),
        (0.2, 1.0, "coordination_bistability"),
        (2.0, 0.5, "t_dominance"),
        (-2.0, 0.5, "s_dominance"),
        (1.0, 1.0, "boundary"),
        (0.0, 0.0, "boundary"),
    )
    for scale in SCALES:
        for phi, eta, label in cases:
            observed, expected = _classification(phi, eta, scale)
            assert observed == expected == label


def test_common_intrinsic_payoff_offset_does_not_change_pairwise_phase():
    for scale in SCALES:
        for offset_factor in (-1e6, 0.0, 1e6):
            observed, expected = _classification(0.2, -1.0, scale, offset_factor)
            assert observed == expected == "stable_pairwise_coexistence"

            observed, expected = _classification(2.0, 0.5, scale, offset_factor)
            assert observed == expected == "t_dominance"


def test_tiny_strict_dominance_is_not_collapsed_to_boundary():
    scale = 1e-16
    observed, expected = _classification(2.0, 0.5, scale)
    assert observed == expected == "t_dominance"
