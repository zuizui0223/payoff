import pytest

from src.reciprocal_sign_partial_identification import (
    identify_phase_from_sign_evidence,
)


def receipt(u, v):
    return identify_phase_from_sign_evidence(
        u, v, support_reference="TEST_V1"
    )


def test_all_four_strict_sign_pairs_recover_existing_phase_map():
    expected = {
        ("positive", "positive"): "stable_architecture_coexistence",
        ("negative", "negative"): "coordination_bistability",
        ("positive", "negative"): "differentiated_dominance",
        ("negative", "positive"): "shared_dominance",
    }
    for pair, phase in expected.items():
        r = receipt(*pair)
        assert r.strict_phase_certified
        assert r.certified_strict_phase == phase
        assert r.compatible_strict_phases == (phase,)
        assert not r.boundary_compatible
        assert len(r.excluded_strict_phases) == 3


def test_unresolved_d_in_s_with_positive_s_in_d_partially_identifies_phase():
    r = receipt("unresolved", "positive")
    assert not r.strict_phase_certified
    assert r.certified_strict_phase is None
    assert r.boundary_compatible
    assert set(r.compatible_strict_phases) == {
        "shared_dominance",
        "stable_architecture_coexistence",
    }
    assert set(r.excluded_strict_phases) == {
        "coordination_bistability",
        "differentiated_dominance",
    }


def test_positive_d_in_s_with_unresolved_s_in_d_has_mirrored_partial_set():
    r = receipt("positive", "unresolved")
    assert set(r.compatible_strict_phases) == {
        "differentiated_dominance",
        "stable_architecture_coexistence",
    }
    assert set(r.excluded_strict_phases) == {
        "coordination_bistability",
        "shared_dominance",
    }
    assert r.boundary_compatible


def test_both_unresolved_leave_all_strict_phases_and_boundaries_compatible():
    r = receipt("unresolved", "unresolved")
    assert len(r.compatible_strict_phases) == 4
    assert r.excluded_strict_phases == ()
    assert r.boundary_compatible
    assert not r.strict_phase_certified


def test_exact_zero_is_boundary_only_for_that_oriented_margin():
    r = receipt("zero", "positive")
    assert r.compatible_strict_phases == ()
    assert len(r.excluded_strict_phases) == 4
    assert r.boundary_compatible
    assert not r.strict_phase_certified


def test_sign_categories_do_not_claim_phi_eta_or_fixation_or_history():
    r = receipt("positive", "positive")
    assert not r.numerical_phi_eta_identified
    assert not r.finite_population_fixation_identified
    assert not r.historical_causation_identified


@pytest.mark.parametrize(
    "u,v",
    [
        ("maybe", "positive"),
        ("positive", "nonsignificant"),
        (1, "positive"),
    ],
)
def test_invalid_sign_evidence_rejected(u, v):
    with pytest.raises(ValueError):
        receipt(u, v)


def test_missing_provenance_rejected():
    with pytest.raises(ValueError):
        identify_phase_from_sign_evidence(
            "positive", "positive", support_reference=" "
        )
