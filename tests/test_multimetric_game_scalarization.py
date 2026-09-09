import pytest

from src.multimetric_game_scalarization import adjudicate_multimetric_sign


def rec(states):
    return adjudicate_multimetric_sign(
        states,
        support_reference="TEST_MULTIMETRIC",
        orientation_frozen_declared=True,
    )


def test_positive_weak_pareto_dominance_has_weight_invariant_positive_sign():
    r = rec({"a": "positive", "b": "zero", "c": "positive"})
    assert r.weight_invariant_scalar_sign == "positive"
    assert r.pareto_relation == "candidate_weakly_pareto_dominates"
    assert not r.scalarization_required


def test_negative_weak_pareto_dominance_has_weight_invariant_negative_sign():
    r = rec({"a": "negative", "b": "zero", "c": "negative"})
    assert r.weight_invariant_scalar_sign == "negative"
    assert r.pareto_relation == "comparator_weakly_pareto_dominates"
    assert not r.scalarization_required


def test_mixed_signs_force_scalarization_and_refuse_a_canonical_gap_sign():
    r = rec({"yield": "positive", "growth_rate": "negative"})
    assert r.weight_invariant_scalar_sign is None
    assert r.pareto_relation == "tradeoff_non_dominance"
    assert r.scalarization_required


def test_mixed_signs_are_already_decisive_even_with_an_unresolved_metric():
    r = rec({"yield": "positive", "growth_rate": "negative", "other": "unresolved"})
    assert r.weight_invariant_scalar_sign is None
    assert r.pareto_relation == "tradeoff_non_dominance"
    assert r.scalarization_required
    assert r.unresolved_metrics_present


def test_unresolved_metric_prevents_sign_when_known_metrics_do_not_conflict():
    r = rec({"yield": "positive", "other": "unresolved"})
    assert r.weight_invariant_scalar_sign is None
    assert r.pareto_relation == "unresolved"
    assert r.scalarization_required


def test_all_zero_metrics_return_zero_without_game_promotion():
    r = rec({"a": "zero", "b": "zero"})
    assert r.weight_invariant_scalar_sign == "zero"
    assert r.pareto_relation == "all_registered_metrics_tied"
    assert not r.generic_frequency_game_identified
    assert not r.architecture_mapping_identified
    assert not r.architecture_specific_claim_licensed


def test_beck_weak_buffer_published_metric_directions_are_tradeoff_non_dominant():
    r = rec(
        {
            "final_biomass_titer": "positive",
            "total_glucose_catabolized": "positive",
            "biomass_per_glucose": "unresolved",
            "biomass_per_proton": "positive",
            "low_byproduct_accumulation": "positive",
            "specific_growth_rate": "negative",
        }
    )
    assert r.pareto_relation == "tradeoff_non_dominance"
    assert r.weight_invariant_scalar_sign is None
    assert r.scalarization_required
    assert not r.generic_frequency_game_identified


def test_beck_strong_buffer_published_metric_directions_are_also_tradeoff_non_dominant():
    r = rec(
        {
            "final_biomass_titer": "negative",
            "total_glucose_catabolized": "negative",
            "biomass_per_glucose": "negative",
            "biomass_per_proton": "negative",
            "low_byproduct_accumulation": "positive",
            "specific_growth_rate": "negative",
        }
    )
    assert r.pareto_relation == "tradeoff_non_dominance"
    assert r.weight_invariant_scalar_sign is None
    assert r.scalarization_required


@pytest.mark.parametrize(
    "states",
    [
        {},
        {"": "positive"},
        {"a": "better"},
    ],
)
def test_invalid_metric_contracts_are_rejected(states):
    with pytest.raises(ValueError):
        rec(states)


def test_orientation_must_be_frozen_before_adjudication():
    with pytest.raises(ValueError):
        adjudicate_multimetric_sign(
            {"a": "positive"},
            support_reference="TEST",
            orientation_frozen_declared=False,
        )
