from fractions import Fraction as F
import random

import pytest

from src.frequency_response_holdout import validate_frequency_response_holdouts
from src.payoff_game import payoff_gap


def check(u, v, holdouts):
    return validate_frequency_response_holdouts(
        u, v, holdouts, support_reference="synthetic_holdout",
        resident_contexts_matched_declared=True,
        common_oriented_gap_scale_declared=True,
    )


def test_exact_endpoints_predict_all_interior_points_without_refit():
    phi, eta = F(3, 10), F(-1, 2)
    u, v = phi-eta, -phi-eta
    hs = []
    for p in (F(1, 5), F(1, 2), F(4, 5)):
        y = phi+eta*(2*p-1)
        hs.append((p, (y, y)))
    r = check((u, u), (v, v), hs)
    assert r.all_holdouts_compatible
    assert r.canonical_linear_frequency_response_supported
    assert not r.endpoints_refit_with_holdouts
    assert r.max_registered_frequency_gap_exact == "0"


def test_wrong_interior_curvature_rejects_even_when_endpoints_are_exact():
    r = check((1, 1), (1, 1), [(F(1, 2), (F(1, 10), F(1, 10)))])
    assert not r.all_holdouts_compatible
    assert r.status == "canonical_linear_frequency_response_rejected_by_holdout"
    assert r.holdouts[0].predicted_gap_band_exact == ("0", "0")
    assert r.max_registered_frequency_gap_exact == "1/10"


def test_closed_band_contact_counts_as_compatible():
    r = check((0, 2), (0, 2), [(F(1, 2), (1, 3))])
    # prediction [-1,1], observation [1,3] touches exactly at 1.
    assert r.holdouts[0].compatible
    assert r.holdouts[0].overlap_band_exact == ("1", "1")


def test_prediction_band_formula_matches_corner_enumeration():
    rng = random.Random(202609075)
    for _ in range(250):
        ul = F(rng.randrange(-20, 10), 10)
        uh = ul + F(rng.randrange(0, 10), 10)
        vl = F(rng.randrange(-20, 10), 10)
        vh = vl + F(rng.randrange(0, 10), 10)
        p = F(rng.randrange(1, 100), 100)
        r = check((ul, uh), (vl, vh), [(p, (-100, 100))])
        got = tuple(map(F, r.holdouts[0].predicted_gap_band_exact))
        corners = [(1-p)*u-p*v for u in (ul, uh) for v in (vl, vh)]
        assert got == (min(corners), max(corners))


def test_existing_payoff_gap_roundtrip_at_seeded_parameters():
    rng = random.Random(202609076)
    for _ in range(300):
        phi = F(rng.randrange(-30, 31), 10)
        eta = F(rng.randrange(-30, 31), 10)
        u, v = phi-eta, -phi-eta
        p = F(rng.randrange(1, 100), 100)
        y = F(str(payoff_gap(float(p), float(phi), float(eta))))
        eps = F(1, 10**12)
        r = check((u, u), (v, v), [(p, (y-eps, y+eps))])
        assert r.all_holdouts_compatible


def test_multiple_holdouts_report_any_failure_without_refitting_good_ones():
    r = check((1, 1), (-1, -1), [
        (F(1, 4), (1, 1)),
        (F(1, 2), (1, 1)),  # canonical prediction is 1 throughout here
        (F(3, 4), (2, 2)),
    ])
    assert [h.compatible for h in r.holdouts] == [True, True, False]
    assert not r.canonical_linear_frequency_response_supported
    assert r.max_registered_frequency_gap_exact == "1"


@pytest.mark.parametrize("kwargs", [
    {"support_reference": " "},
    {"resident_contexts_matched_declared": False},
    {"common_oriented_gap_scale_declared": False},
])
def test_contract_guardrails(kwargs):
    args = dict(support_reference="synthetic", resident_contexts_matched_declared=True,
                common_oriented_gap_scale_declared=True)
    args.update(kwargs)
    with pytest.raises(ValueError):
        validate_frequency_response_holdouts((1, 1), (1, 1), [(F(1,2), (0,0))], **args)


@pytest.mark.parametrize("holdouts", [
    [], [(0, (0,0))], [(1, (0,0))], [(F(1,2), (0,0)), (F(1,2), (0,0))],
    [(F(1,2), (1,-1))], [(True, (0,0))],
])
def test_invalid_holdouts_rejected(holdouts):
    with pytest.raises(ValueError):
        check((1,1), (1,1), holdouts)
