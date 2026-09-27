import pytest

from src.information_uptake_network import (
    adoption_cut_change,
    complete_graph_cut_fraction,
    complete_graph_maximum_cut_fraction,
    complete_graph_weights,
    evaluate_network_uptake,
    random_mixing_asynchronous_pair_fraction,
    weighted_information_cut,
)


def chain_weights(n):
    rows = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n - 1):
        rows[i][i + 1] = 1.0
        rows[i + 1][i] = 1.0
    return tuple(tuple(row) for row in rows)


def test_complete_graph_cut_is_maximal_near_half_adoption():
    assert complete_graph_cut_fraction(4, 0) == pytest.approx(0.0)
    assert complete_graph_cut_fraction(4, 1) == pytest.approx(0.5)
    assert complete_graph_cut_fraction(4, 2) == pytest.approx(2.0 / 3.0)
    assert complete_graph_cut_fraction(4, 3) == pytest.approx(0.5)
    assert complete_graph_cut_fraction(4, 4) == pytest.approx(0.0)
    assert complete_graph_maximum_cut_fraction(4) == pytest.approx(2.0 / 3.0)


@pytest.mark.parametrize("n", [3, 4, 5, 10, 21])
def test_complete_graph_maximum_occurs_at_floor_or_ceil_half(n):
    maximum = complete_graph_maximum_cut_fraction(n)
    values = [complete_graph_cut_fraction(n, k) for k in range(n + 1)]
    assert maximum == pytest.approx(max(values))


def test_random_mixing_async_pair_fraction_peaks_at_half():
    values = [
        random_mixing_asynchronous_pair_fraction(step / 100.0)
        for step in range(101)
    ]
    assert max(values) == pytest.approx(0.5)
    assert random_mixing_asynchronous_pair_fraction(0.5) == pytest.approx(0.5)
    assert random_mixing_asynchronous_pair_fraction(0.0) == pytest.approx(0.0)
    assert random_mixing_asynchronous_pair_fraction(1.0) == pytest.approx(0.0)


def test_adoption_cut_change_identity_on_chain():
    weights = chain_weights(5)
    all_old = (False, False, False, False, False)

    # Central first adopter exposes two edges.
    assert adoption_cut_change(2, all_old, weights) == pytest.approx(2.0)

    after_center = (False, False, True, False, False)
    # Adjacent adopter repairs one old cut but creates one new cut: net zero.
    assert adoption_cut_change(1, after_center, weights) == pytest.approx(0.0)

    after_center_left = (False, True, True, False, False)
    # Peripheral adoption next to an informed node repairs one edge.
    assert adoption_cut_change(0, after_center_left, weights) == pytest.approx(-1.0)


def test_same_delay_distribution_has_different_network_cut_when_deadlines_are_rearranged():
    weights = chain_weights(5)
    q = 0.80

    peripheral_first = evaluate_network_uptake(
        prior_early=0.40,
        false_early_cost=2.0,
        missed_early_cost=1.0,
        cue_accuracy=q,
        delay_costs=(0.05, 0.10, 0.20, 0.30, 0.35),
        weights=weights,
    )
    central_first = evaluate_network_uptake(
        prior_early=0.40,
        false_early_cost=2.0,
        missed_early_cost=1.0,
        cue_accuracy=q,
        delay_costs=(0.30, 0.20, 0.05, 0.10, 0.35),
        weights=weights,
    )

    # At q=.80, V=.08, so only D=.05 adopts under strict waiting.
    assert peripheral_first.informed_count == 1
    assert central_first.informed_count == 1
    assert peripheral_first.cut_fraction == pytest.approx(0.25)
    assert central_first.cut_fraction == pytest.approx(0.50)
    assert (
        central_first.expected_edge_mismatch_fraction
        > peripheral_first.expected_edge_mismatch_fraction
    )


def test_complete_graph_four_actor_mismatch_peaks_during_middle_adoption():
    delays = (0.05, 0.15, 0.25, 0.35)
    weights = complete_graph_weights(4)

    low = evaluate_network_uptake(
        prior_early=0.40,
        false_early_cost=2.0,
        missed_early_cost=1.0,
        cue_accuracy=0.80,
        delay_costs=delays,
        weights=weights,
    )
    middle = evaluate_network_uptake(
        prior_early=0.40,
        false_early_cost=2.0,
        missed_early_cost=1.0,
        cue_accuracy=0.875,
        delay_costs=delays,
        weights=weights,
    )
    high = evaluate_network_uptake(
        prior_early=0.40,
        false_early_cost=2.0,
        missed_early_cost=1.0,
        cue_accuracy=1.0,
        delay_costs=delays,
        weights=weights,
    )

    assert low.informed_count == 1
    assert middle.informed_count == 2
    assert high.informed_count == 4
    assert middle.cut_fraction > low.cut_fraction
    assert high.cut_fraction == pytest.approx(0.0)
    assert middle.expected_edge_mismatch_fraction > low.expected_edge_mismatch_fraction
    assert high.expected_edge_mismatch_fraction == pytest.approx(0.0)


def test_weighted_cut_rejects_asymmetric_network():
    with pytest.raises(ValueError, match="symmetric"):
        weighted_information_cut(
            (True, False),
            ((0.0, 1.0), (0.0, 0.0)),
        )
