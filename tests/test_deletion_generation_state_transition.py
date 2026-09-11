from fractions import Fraction

import pytest

from src.deletion_generation_state_transition import (
    classify_generation_reduction,
    deletion_odds,
    generation_fraction_band_from_states,
    generation_fraction_from_states,
)


def _forward_fraction(f0: Fraction, mu: Fraction, r: Fraction) -> Fraction:
    """Exact forward map implied by the registered two-state transition."""
    x0 = f0 / (1 - f0)
    x1 = (r * x0 + mu) / (1 - mu)
    return x1 / (1 + x1)


def test_point_formula_roundtrips_exact_registered_transition():
    cases = (
        (Fraction(1, 5), Fraction(1, 10), Fraction(1, 2)),
        (Fraction(1, 20), Fraction(1, 4), Fraction(3, 5)),
        (Fraction(2, 5), Fraction(1, 20), Fraction(4, 3)),
        (Fraction(0), Fraction(2, 7), Fraction(5, 4)),
    )
    for f0, mu, r in cases:
        f1 = _forward_fraction(f0, mu, r)
        assert generation_fraction_from_states(f0, f1, r) == mu


def test_deletion_odds_are_exact():
    assert deletion_odds(Fraction(1, 5)) == Fraction(1, 4)
    assert deletion_odds("3/7") == Fraction(3, 4)


def test_band_projection_matches_all_cartesian_corners():
    f0_band = (Fraction(1, 10), Fraction(1, 5))
    f1_band = (Fraction(1, 4), Fraction(1, 3))
    r_band = (Fraction(1, 2), Fraction(3, 4))
    receipt = generation_fraction_band_from_states(f0_band, f1_band, r_band)

    corner_values = [
        generation_fraction_from_states(f0, f1, r)
        for f0 in f0_band
        for f1 in f1_band
        for r in r_band
    ]
    assert receipt.raw_mu_projection == (min(corner_values), max(corner_values))
    assert receipt.transition_model_compatible
    assert receipt.biological_mu_band is not None


def test_impossible_state_transition_is_rejected_by_biological_mu_intersection():
    receipt = generation_fraction_band_from_states(
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(1)),
    )
    assert receipt.raw_mu_projection == (Fraction(-1), Fraction(-1))
    assert not receipt.transition_model_compatible
    assert receipt.biological_mu_band is None
    assert not receipt.point_identified


def test_point_band_is_point_identified():
    f0 = Fraction(1, 5)
    mu = Fraction(1, 10)
    r = Fraction(1, 2)
    f1 = _forward_fraction(f0, mu, r)
    receipt = generation_fraction_band_from_states((f0, f0), (f1, f1), (r, r))
    assert receipt.transition_model_compatible
    assert receipt.biological_mu_band == (mu, mu)
    assert receipt.point_identified


def test_generation_reduction_uses_strict_material_threshold():
    reduced = classify_generation_reduction(
        (Fraction(3, 10), Fraction(2, 5)),
        (Fraction(1, 10), Fraction(3, 20)),
        material_reduction=Fraction(1, 10),
    )
    assert reduced.guaranteed_reduction_lower_bound == Fraction(3, 20)
    assert reduced.generation_result == "reduced"

    excluded = classify_generation_reduction(
        (Fraction(1, 5), Fraction(1, 4)),
        (Fraction(4, 25), Fraction(19, 100)),
        material_reduction=Fraction(1, 10),
    )
    assert excluded.possible_reduction_upper_bound == Fraction(9, 100)
    assert excluded.generation_result == "material_reduction_excluded"

    boundary = classify_generation_reduction(
        (Fraction(1, 4), Fraction(7, 20)),
        (Fraction(3, 20), Fraction(1, 5)),
        material_reduction=Fraction(1, 20),
    )
    assert boundary.guaranteed_reduction_lower_bound == Fraction(1, 20)
    assert boundary.generation_result == "unresolved"


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        generation_fraction_from_states(Fraction(1), Fraction(1, 2), Fraction(1))
    with pytest.raises(ValueError):
        generation_fraction_from_states(Fraction(1, 2), Fraction(1, 3), Fraction(-1, 2))
    with pytest.raises(ValueError):
        generation_fraction_band_from_states((Fraction(1, 2), Fraction(1, 3)), (0, 0), (0, 1))
    with pytest.raises(ValueError):
        classify_generation_reduction((0, 1), (0, 1), material_reduction=Fraction(-1, 10))
