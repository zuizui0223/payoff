from dataclasses import asdict
import pytest
from src.empirical_identification import calibrate_triangular, synthetic_example


def data(scale=1.0):
    b = lambda r: scale*(0.5*r-0.5*r*r)
    a = lambda d: scale*2*d*d*max(0.0, 1-d/0.3)
    return dict(
        intrinsic_fit=[(r,b(r)) for r in (0.2,0.4)],
        interaction_fit=[(d,a(d)) for d in (0.05,0.15)],
        common_scale="working units", matched_context="fixed environment",
        matched_contrasts_declared=True,
        intrinsic_holdout=[(0.6,b(0.6))],
        interaction_holdout=[(0.2,a(0.2)),(0.4,a(0.4))],
    )


def test_exact_recovery_and_existing_phase_theorem():
    from src.triangular_kernel_phase_curve import dimensionless_triangular_window
    r = calibrate_triangular(**data())
    assert (r.alpha,r.kappa,r.gamma,r.epsilon) == pytest.approx((0.5,1,-2,0.3))
    assert (r.E,r.g) == pytest.approx((0.6,2))
    window = dimensionless_triangular_window(r.E)
    assert r.frozen_resident_barrier == (window.g_on < r.g < window.g_hi)
    assert not r.mutation_radius_identified


def test_unknown_common_scale_preserves_dimensionless_phase_not_absolute_coefficients():
    a, b = calibrate_triangular(**data()), calibrate_triangular(**data(7))
    assert (a.E,a.g,a.epsilon,a.intrinsic_optimum) == pytest.approx(
        (b.E,b.g,b.epsilon,b.intrinsic_optimum))
    assert b.alpha == pytest.approx(7*a.alpha)
    assert b.parameter_scope == "working_scale_only"


def test_fit_is_not_heldout_validation():
    d=data(); d.update(intrinsic_holdout=(), interaction_holdout=())
    r=calibrate_triangular(**d)
    assert r.status == "calibration_only" and r.frozen_resident_barrier is None


def test_failed_holdout_blocks_phase_report():
    d=data(); d["interaction_holdout"]=[(0.2,0.5),(0.4,0.01)]
    r=calibrate_triangular(**d)
    assert r.status == "holdout_inconsistent" and r.frozen_resident_barrier is None


def test_repeated_distances_are_not_new_identification_directions():
    d=data(); d["interaction_fit"]=[(0.05,0.004),(0.05,0.004)]
    with pytest.raises(ValueError, match="rank"):
        calibrate_triangular(**d)


def test_same_distance_nonidentifiability_witness():
    distance=0.1
    # Distinct G/epsilon pairs generate exactly the same contrast at one distance.
    assert 2*distance**2*(1-distance/0.3) == pytest.approx(
        4*distance**2*(1-distance/0.15))


def test_reused_holdout_and_undeclared_matching_are_rejected():
    d=data(); d["intrinsic_holdout"]=[(0.2,0.08)]
    with pytest.raises(ValueError, match="reuse"):
        calibrate_triangular(**d)
    d=data(); d["matched_contrasts_declared"]=False
    with pytest.raises(ValueError, match="declare"):
        calibrate_triangular(**d)


@pytest.mark.parametrize("bad", [float("nan"),float("inf"),-1.0])
def test_invalid_tolerances(bad):
    with pytest.raises(ValueError):
        calibrate_triangular(**data(), absolute_error_tolerance=bad)


def test_example_is_explicitly_synthetic():
    assert synthetic_example()["data_kind"] == "synthetic_exact_witness"
