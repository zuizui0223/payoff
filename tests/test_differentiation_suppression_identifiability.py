from fractions import Fraction

import pytest

from src.differentiation_suppression_identifiability import (
    DifferentiationSuppressionReceipt,
    adjudicate_differentiation_suppression,
    observed_specialist_fraction,
    realization_ratio_for_same_observed_fraction,
)


def full_receipt(**overrides):
    data = dict(
        system_id="TEST_SYSTEM",
        perturbation_id="TEST_PERTURBATION",
        support_reference="TEST_SUPPORT",
        observed_specialist_frequency_reduced_declared=True,
        direct_generation_rate_measured_declared=True,
        generation_rate_reduced_declared=True,
        post_generation_survival_or_realization_matched_declared=True,
        generalist_growth_matched_declared=True,
        generalist_sporulation_matched_declared=True,
        net_task_preserved_declared=True,
        ecological_context_matched_declared=True,
        background_matched_declared=True,
        focal_differentiation_mechanism_isolated_declared=True,
        stable_or_heritable_unit_declared=True,
        independent_of_game_result_declared=True,
        independent_of_raw_availability_declared=True,
    )
    data.update(overrides)
    return DifferentiationSuppressionReceipt(**data)


def test_observed_fraction_bookkeeping_is_exact():
    assert observed_specialist_fraction(Fraction(1, 10), Fraction(1, 2)) == Fraction(1, 19)
    assert observed_specialist_fraction(Fraction(1, 10), 1) == Fraction(1, 10)


def test_same_observed_fraction_can_arise_from_different_generation_rates():
    f = Fraction(1, 100)
    pairs = []
    for mu in (Fraction(1, 50), Fraction(1, 20), Fraction(1, 10), Fraction(1, 5)):
        r = realization_ratio_for_same_observed_fraction(f, mu)
        pairs.append((mu, r))
        assert observed_specialist_fraction(mu, r) == f
    assert len({mu for mu, _ in pairs}) == 4
    assert len({r for _, r in pairs}) == 4


def test_lower_final_specialist_fraction_does_not_by_itself_identify_lower_generation():
    baseline = observed_specialist_fraction(Fraction(1, 100), 1)
    # Same generation fraction, but poorer specialist realization.
    filtered = observed_specialist_fraction(Fraction(1, 100), Fraction(1, 10))
    assert filtered < baseline


def test_full_clean_suppression_candidate_can_certify():
    result = adjudicate_differentiation_suppression(full_receipt())
    assert result.generation_suppression_identified
    assert result.matched_s_candidate_certified
    assert result.blockers == ()
    assert not result.generic_game_promoted
    assert not result.architecture_frequency_claim_promoted


def test_frequency_reduction_without_direct_generation_measurement_is_not_suppression():
    result = adjudicate_differentiation_suppression(
        full_receipt(
            direct_generation_rate_measured_declared=False,
            generation_rate_reduced_declared=False,
        )
    )
    assert not result.generation_suppression_identified
    assert not result.matched_s_candidate_certified
    assert "DIRECT_DIFFERENTIATION_GENERATION_RATE_NOT_MEASURED" in result.blockers
    assert "DIFFERENTIATION_GENERATION_REDUCTION_NOT_SHOWN" in result.blockers


def test_survivor_filter_is_not_a_matched_s_even_when_observed_frequency_falls():
    result = adjudicate_differentiation_suppression(
        full_receipt(
            direct_generation_rate_measured_declared=False,
            generation_rate_reduced_declared=False,
            post_generation_survival_or_realization_matched_declared=False,
        )
    )
    assert not result.generation_suppression_identified
    assert "POST_GENERATION_SURVIVAL_OR_REALIZATION_NOT_MATCHED" in result.blockers


def test_growth_or_sporulation_pleiotropy_blocks_matched_s():
    result = adjudicate_differentiation_suppression(
        full_receipt(
            generalist_growth_matched_declared=False,
            generalist_sporulation_matched_declared=False,
        )
    )
    assert result.generation_suppression_identified
    assert not result.matched_s_candidate_certified
    assert "GENERALIST_GROWTH_NOT_MATCHED" in result.blockers
    assert "GENERALIST_SPORULATION_NOT_MATCHED" in result.blockers


def test_game_or_raw_dependent_architecture_mapping_is_rejected():
    with pytest.raises(ValueError):
        adjudicate_differentiation_suppression(
            full_receipt(independent_of_game_result_declared=False)
        )
    with pytest.raises(ValueError):
        adjudicate_differentiation_suppression(
            full_receipt(independent_of_raw_availability_declared=False)
        )


@pytest.mark.parametrize(
    "mu,r",
    [
        ("-1/10", "1"),
        ("11/10", "1"),
        ("1/2", "-1"),
    ],
)
def test_invalid_bookkeeping_inputs_rejected(mu, r):
    with pytest.raises(ValueError):
        observed_specialist_fraction(mu, r)
