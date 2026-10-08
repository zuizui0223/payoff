"""Tests for the post-outcome phase-transfer kinematic identity."""

import pytest
from src.v7r_phase_identity import PhaseTransition, decompose_phase_transfer


def _make(x, *, stop_slope=-0.4, transit_slope=0.1, climate_slope=-0.2):
    origin=100.0+x
    stop=10.0+stop_slope*x
    transit=5.0+transit_slope*x
    delta_season=-3.0+climate_slope*x
    dest_arrival=origin+stop+transit
    dest_phase=x+stop+transit+delta_season
    return PhaseTransition(
        origin_arrival_doy=origin,
        destination_arrival_doy=dest_arrival,
        origin_phase=x,
        destination_phase=dest_phase,
        origin_stopover_days=stop,
        transit_days=transit,
    )


def test_four_term_phase_slope_identity():
    out=decompose_phase_transfer([_make(x) for x in (-2.,-1.,0.,1.,2.)])
    assert out.n==5
    assert out.b_stopover==pytest.approx(-0.4)
    assert out.b_transit==pytest.approx(0.1)
    assert out.b_interregional_season==pytest.approx(-0.2)
    assert out.lambda_observed==pytest.approx(0.5)
    assert out.lambda_reconstructed==pytest.approx(0.5)
    assert out.slope_identity_error<1e-10


def test_full_phase_contraction_can_arise_without_duration_adjustment():
    rows=[_make(x,stop_slope=0.0,transit_slope=0.0,climate_slope=-1.0)
          for x in (-2.,-1.,0.,1.,2.)]
    out=decompose_phase_transfer(rows)
    assert out.b_stopover==pytest.approx(0.0)
    assert out.b_transit==pytest.approx(0.0)
    assert out.b_interregional_season==pytest.approx(-1.0)
    assert out.lambda_observed==pytest.approx(0.0,abs=1e-10)


def test_inconsistent_chronology_fails_closed():
    rows=[_make(x) for x in (-2.,-1.,0.,1.,2.)]
    r=rows[0]
    rows[0]=PhaseTransition(
        r.origin_arrival_doy,r.destination_arrival_doy+1.0,
        r.origin_phase,r.destination_phase,r.origin_stopover_days,r.transit_days,
    )
    with pytest.raises(ValueError,match="chronology"):
        decompose_phase_transfer(rows)


def test_constant_origin_phase_does_not_have_an_estimable_lambda():
    with pytest.raises(ValueError,match="lacks variation"):
        decompose_phase_transfer([_make(0.) for _ in range(5)])
