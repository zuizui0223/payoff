import math

import pytest

from src.topology_mutation import is_single_edge_local_optimum


SOURCE = (0, 0)
UPHILL = (1, 0)
OTHER = (0, 1)
SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)


def test_strict_one_edge_improvement_is_detected_at_every_payoff_scale():
    for scale in SCALES:
        payoffs = {
            SOURCE: 0.0,
            UPHILL: 1.0 * scale,
            OTHER: -1.0 * scale,
        }
        assert is_single_edge_local_optimum(SOURCE, payoffs) is False


def test_exact_ties_and_downhill_neighbors_remain_local_optimum_compatible():
    for scale in SCALES:
        tied = {
            SOURCE: 2.0 * scale,
            UPHILL: 2.0 * scale,
            OTHER: 1.0 * scale,
        }
        assert is_single_edge_local_optimum(SOURCE, tied) is True

        downhill = {
            SOURCE: 2.0 * scale,
            UPHILL: 1.0 * scale,
            OTHER: 0.0,
        }
        assert is_single_edge_local_optimum(SOURCE, downhill) is True


def test_local_optimum_decision_is_invariant_to_common_payoff_offset():
    # A large common baseline is irrelevant to topology ranking. The difference
    # remains representable, but an uncentered relative tolerance would scale
    # with the arbitrary baseline and could hide the uphill neighbor.
    for scale in SCALES:
        offset = 1e15 * scale
        payoffs = {
            SOURCE: offset,
            UPHILL: offset + scale,
            OTHER: offset - scale,
        }
        assert payoffs[UPHILL] > payoffs[SOURCE]
        assert is_single_edge_local_optimum(SOURCE, payoffs) is False


def test_nonfinite_local_payoff_fails_closed():
    payoffs = {
        SOURCE: 0.0,
        UPHILL: math.nan,
        OTHER: -1.0,
    }
    with pytest.raises(ValueError, match="finite"):
        is_single_edge_local_optimum(SOURCE, payoffs)
