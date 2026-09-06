from fractions import Fraction as F
import random

import pytest

from src.bounded_error_identification import certify_bounded_triangular, _box_phase, _discriminant
from src.empirical_identification import calibrate_triangular


def example(error="0.0001", *, G="2", ranges=("0.05", "0.15"), scale="1"):
    u, g, c = F(error), F(G), F(scale)
    b = lambda x: x/2-x*x/2
    a = lambda x: g*x*x*max(F(0), 1-x/F("0.3"))
    band = lambda x, fun: (F(x), c*(fun(F(x))-u), c*(fun(F(x))+u))
    return dict(
        intrinsic_fit=[band(x, b) for x in ("0.2", "0.4")],
        interaction_fit=[band(x, a) for x in ranges],
        intrinsic_holdout=[band("0.6", b)],
        interaction_holdout=[band(x, a) for x in ("0.2", "0.4") if x not in ranges],
        common_scale="declared shared units", matched_context="synthetic",
        matched_contrasts_declared=True,
    )


def test_exact_zero_error_recovers_existing_inverse_and_phase():
    kwargs = example("0")
    r = certify_bounded_triangular(**kwargs)
    exact = calibrate_triangular(
        [(float(x), float(lo)) for x, lo, _ in kwargs['intrinsic_fit']],
        [(float(x), float(lo)) for x, lo, _ in kwargs['interaction_fit']],
        intrinsic_holdout=[(float(x), float(lo)) for x, lo, _ in kwargs['intrinsic_holdout']],
        interaction_holdout=[(float(x), float(lo)) for x, lo, _ in kwargs['interaction_holdout']],
        common_scale="test", matched_context="test", matched_contrasts_declared=True,
    )
    assert r.frozen_resident_barrier is True
    assert exact.frozen_resident_barrier is True
    for key, expected in (("alpha", F(1, 2)), ("kappa", F(1)), ("G", F(2)),
                          ("epsilon", F(3, 10)), ("E", F(3, 5)), ("g", F(2))):
        assert tuple(map(F, r.exact_bounds[key])) == (expected, expected)
        assert F(r.bounds[key][0]) <= expected <= F(r.bounds[key][1])


@pytest.mark.parametrize('G,box,phase', [('0.5','certified_no_ridge',False),
                                       ('2','certified_barrier',True),
                                       ('5','certified_ridge_not_below_outside_optimum',False)])
def test_three_distinct_regimes(G, box, phase):
    r = certify_bounded_triangular(**example("0.00001", G=G))
    assert r.box_status == box
    assert r.frozen_resident_barrier is phase


def test_small_error_certifies_but_large_error_abstains():
    small = certify_bounded_triangular(**example("0.0001"))
    large = certify_bounded_triangular(**example("0.001"))
    assert small.frozen_resident_barrier is True
    assert large.frozen_resident_barrier is None
    assert large.status == "bounded_error_audit_complete"
    assert large.box_status == "unresolved_outer_box"
    assert not small.mutation_radius_identified


def test_common_scale_including_error_bounds_cancels():
    a = certify_bounded_triangular(**example(scale="1"))
    b = certify_bounded_triangular(**example(scale="17"))
    for key in ("E", "g", "epsilon", "rstar"):
        assert a.exact_bounds[key] == b.exact_bounds[key]
    assert a.box_status == b.box_status


def test_inconsistent_bands_do_not_license_vacuous_phase():
    k = example()
    k['intrinsic_holdout'] = [(F('0.6'), F('5'), F('6'))]
    r = certify_bounded_triangular(**k)
    assert r.status == "inconsistent_response_bands"
    assert r.frozen_resident_barrier is None


def test_missing_holdouts_cannot_license_phase():
    k = example()
    k['interaction_holdout'] = []
    r = certify_bounded_triangular(**k)
    assert r.box_status == "certified_barrier"
    assert r.frozen_resident_barrier is None
    assert not r.holdout_coverage


def test_repeated_coordinate_is_not_more_identification():
    k = example()
    k['interaction_fit'][1] = k['interaction_fit'][0]
    with pytest.raises(ValueError, match='distinct'):
        certify_bounded_triangular(**k)


@pytest.mark.parametrize('bad', [float('nan'),float('inf'),None,True,complex(1,1)])
def test_invalid_bounds_rejected(bad):
    k = example()
    k['intrinsic_fit'][0] = ('0.2', bad, '1')
    with pytest.raises(ValueError):
        certify_bounded_triangular(**k)


def test_overlap_and_reversed_band_rejected():
    k = example()
    k['intrinsic_holdout'] = [k['intrinsic_fit'][0]]
    with pytest.raises(ValueError, match='reuse'):
        certify_bounded_triangular(**k)
    k = example()
    k['intrinsic_fit'][0] = ('0.2','1','0')
    with pytest.raises(ValueError, match='lower'):
        certify_bounded_triangular(**k)


def test_sign_ambiguity_is_unresolved_not_false():
    r = certify_bounded_triangular(**example('0.1'))
    assert r.status == 'positive_interior_calibration_not_certified'
    assert r.frozen_resident_barrier is None


def test_exact_discriminant_matches_original_boundary_away_from_equality():
    from math import sqrt
    rng = random.Random(914)
    for _ in range(300):
        E = F(rng.randint(1,99),100)
        g = F(rng.randint(1,500),50)
        x = 4*float(E)/(3+sqrt(9-8*float(E)))
        upper = (1-x)*(3-x)/(2*x*x)
        expected = 1/float(E)-1 < float(g) < upper
        # Exact lower-bound equality is excluded in the reference float check.
        if g == 1/E-1:
            continue
        assert (_box_phase((E,E),(g,g)) == 'certified_barrier') == expected


def test_random_rectangles_certify_only_uniform_regimes():
    rng = random.Random(211)
    for _ in range(150):
        el = F(rng.randint(2,75),100)
        eh = el+F(rng.randint(0,20),100)
        gl = F(rng.randint(1,100),20)
        gh = gl+F(rng.randint(0,50),20)
        result = _box_phase((el,eh),(gl,gh))
        if not result.startswith('certified_'):
            continue
        for i in range(11):
            E = el+(eh-el)*F(i,10)
            for j in range(11):
                g = gl+(gh-gl)*F(j,10)
                inside = g > 1/E-1 and _discriminant(E,g) < 0
                assert inside == (result == 'certified_barrier')


def test_validation_bands_condition_the_set_instead_of_demanding_midpoint_fit():
    k = example('0.0001')
    x,lo,hi = k['intrinsic_fit'][0]
    k['intrinsic_fit'][0] = (x,lo,hi+F('0.0001'))
    # The center of the enlarged band changes, but the old generating model
    # still satisfies the tight independent validation band.
    x=F('0.6'); y=x/2-x*x/2
    k['intrinsic_holdout'] = [(x,y,y)]
    r=certify_bounded_triangular(**k)
    assert r.feasible_witness_compatible
    assert r.frozen_resident_barrier is True


def test_exact_polygon_intersection_handles_segments_and_points():
    from src.bounded_error_identification import _clip, _convex_hull
    square=_convex_hull(((F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))))
    segment=_clip(square,F(1),F(0),F(0))
    assert set(segment)=={(F(0),F(0)),(F(0),F(1))}
    point=_clip(segment,F(0),F(1),F(0))
    assert point==((F(0),F(0)),)
    assert _clip(point,F(1),F(1),F(-1))==()
