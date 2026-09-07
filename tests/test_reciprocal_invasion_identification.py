from fractions import Fraction as F
import random

import pytest

from src.payoff_game import classify_phase, invasion_margins
from src.reciprocal_invasion_identification import identify_from_reciprocal_invasion


def identify(u, v, common=True):
    return identify_from_reciprocal_invasion(
        u, v, support_reference="synthetic_test",
        resident_contexts_matched_declared=True,
        common_scale_declared=common,
    )


def test_four_strict_sign_quadrants_are_exactly_the_four_phases():
    cases = [
        ((1, 2), (3, 4), "stable_architecture_coexistence"),
        ((-2, -1), (-4, -3), "coordination_bistability"),
        ((1, 2), (-4, -3), "differentiated_dominance"),
        ((-2, -1), (3, 4), "shared_dominance"),
    ]
    for u, v, expected in cases:
        r = identify(u, v)
        assert r.phase_certified_from_signs
        assert r.certified_strict_phase == expected


def test_touching_or_crossing_zero_refuses_strict_phase_promotion():
    for u, v in [((0, 1), (1, 2)), ((-1, 1), (1, 2)), ((0, 0), (-2, -1))]:
        r = identify(u, v)
        assert not r.phase_certified_from_signs
        assert r.certified_strict_phase is None


def test_common_scale_reconstructs_exact_phi_eta_and_vertices():
    r = identify((F(1, 5), F(1, 5)), (F(2, 5), F(2, 5)))
    assert r.phi_band_exact == ("-1/10", "-1/10")
    assert r.eta_band_exact == ("-3/10", "-3/10")
    assert r.eta_nonzero_certified is True
    assert r.eta_sign_certified == "negative"
    assert set(r.phi_eta_vertices_exact) == {("-1/10", "-3/10")}


def test_separate_unknown_positive_scales_preserve_phase_but_not_coordinates():
    r = identify((2, 4), (7, 9), common=False)
    assert r.certified_strict_phase == "stable_architecture_coexistence"
    assert r.phi_band_exact is None
    assert r.eta_band_exact is None
    assert r.phi_eta_vertices_exact is None
    assert r.eta_nonzero_certified is None
    assert r.eta_sign_certified is None


def test_eta_can_be_certified_in_dominance_without_phase_mixture():
    r = identify((4, 5), (-1, 0))
    assert r.certified_strict_phase is None  # second band touches boundary
    assert r.eta_band_exact == ("-5/2", "-3/2")
    assert r.eta_nonzero_certified
    assert r.eta_sign_certified == "negative"


def test_bounded_linear_transform_contains_all_corner_and_random_points():
    r = identify((F(-3, 10), F(7, 10)), (F(-2, 5), F(4, 5)))
    plo, phi = map(F, r.phi_band_exact)
    elo, ehi = map(F, r.eta_band_exact)
    rng = random.Random(202609073)
    for _ in range(200):
        a, b = rng.randrange(101), rng.randrange(101)
        u = F(-3, 10) + F(a, 100) * F(1)
        v = F(-2, 5) + F(b, 100) * F(6, 5)
        p, e = (u-v)/2, -(u+v)/2
        assert plo <= p <= phi
        assert elo <= e <= ehi


def test_random_exact_margins_invert_existing_payoff_game_and_phase():
    rng = random.Random(202609074)
    for _ in range(300):
        phi = F(rng.randrange(-40, 41), 10)
        eta = F(rng.randrange(-40, 41), 10)
        if phi in (eta, -eta):
            continue
        u = phi-eta
        v = -phi-eta
        r = identify((u, u), (v, v))
        assert r.phi_band_exact == (str(phi), str(phi))
        assert r.eta_band_exact == (str(eta), str(eta))
        expected = classify_phase(float(phi), float(eta), tol=0.0)
        assert r.certified_strict_phase == expected


def test_existing_invasion_margin_adapter_matches_inverse_map():
    for L, s, K, eta in [(2.0, .5, .3, -.4), (3.0, .2, .8, .6), (1.0, .9, .1, -.2)]:
        u, v = invasion_margins(L, s, K, eta)
        r = identify((str(u), str(u)), (str(v), str(v)))
        phi = s*L-K
        assert abs(float(F(r.phi_band_exact[0]))-phi) < 1e-12
        assert abs(float(F(r.eta_band_exact[0]))-eta) < 1e-12


@pytest.mark.parametrize("kwargs", [
    {"support_reference": " "},
    {"resident_contexts_matched_declared": False},
    {"common_scale_declared": 1},
])
def test_contract_guardrails(kwargs):
    args = dict(support_reference="synthetic", resident_contexts_matched_declared=True,
                common_scale_declared=True)
    args.update(kwargs)
    with pytest.raises(ValueError):
        identify_from_reciprocal_invasion((1, 2), (3, 4), **args)


@pytest.mark.parametrize("u,v", [((2, 1), (3, 4)), ((1,), (3, 4)), ((True, 1), (3, 4)), ((1, 2), ("nan", 4))])
def test_invalid_bands_are_rejected(u, v):
    with pytest.raises(ValueError):
        identify_from_reciprocal_invasion(u, v, support_reference="synthetic",
            resident_contexts_matched_declared=True, common_scale_declared=True)
