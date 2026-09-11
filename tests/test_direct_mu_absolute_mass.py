from fractions import Fraction

import pytest

from src.deletion_generation_state_transition import generation_fraction_from_states
from src.direct_mu_absolute_mass import (
    direct_mu_from_absolute_masses,
    project_direct_mu_absolute_bands,
)


def test_point_identification_recovers_registered_mu_and_g():
    # G0=10, D0=2, g=3, d=1/2, mu=1/5
    # G1=(4/5)*3*10=24; D1=(1/2)*2+(1/5)*3*10=7
    mu, g = direct_mu_from_absolute_masses(10, 2, 24, 7, Fraction(1, 2))
    assert mu == Fraction(1, 5)
    assert g == Fraction(3)


def test_absolute_mass_and_fraction_only_routes_are_algebraically_consistent():
    G0, D0, G1, D1 = map(Fraction, (10, 2, 24, 7))
    d = Fraction(1, 2)
    mu_abs, g = direct_mu_from_absolute_masses(G0, D0, G1, D1, d)
    f0 = D0 / (G0 + D0)
    f1 = D1 / (G1 + D1)
    r = d / g
    mu_fraction = generation_fraction_from_states(f0, f1, r)
    assert mu_abs == Fraction(1, 5)
    assert mu_fraction == mu_abs


def test_no_new_D_yields_mu_zero():
    mu, g = direct_mu_from_absolute_masses(5, 2, 10, 4, 2)
    assert mu == 0
    assert g == 2


def test_all_new_output_enters_D_yields_mu_one():
    mu, g = direct_mu_from_absolute_masses(5, 1, 0, 7, 2)
    assert mu == 1
    assert g == 1


def test_inherited_D_exceeding_observed_D_is_incompatible():
    with pytest.raises(ValueError):
        direct_mu_from_absolute_masses(10, 4, 10, 1, 1)


def test_exact_band_projection_matches_monotone_corners():
    result = project_direct_mu_absolute_bands(
        G1_band=(20, 24),
        D0_band=(1, 2),
        D1_band=(6, 8),
        d_band=(Fraction(1, 2), 1),
    )
    # N in [6-1*2, 8-(1/2)*1] = [4, 15/2]
    assert result.physical_model_compatible
    assert result.new_D_low == 4
    assert result.new_D_high == Fraction(15, 2)
    assert result.mu_low == Fraction(4, 28)
    assert result.mu_high == Fraction(15, 55)


def test_band_crossing_zero_new_D_clips_physical_projection_at_zero():
    result = project_direct_mu_absolute_bands(
        G1_band=(10, 12),
        D0_band=(1, 3),
        D1_band=(2, 5),
        d_band=(1, 2),
    )
    assert result.physical_model_compatible
    assert result.new_D_low == 0
    assert result.mu_low == 0
    assert result.mu_high > 0


def test_wholly_negative_new_D_band_is_incompatible():
    result = project_direct_mu_absolute_bands(
        G1_band=(10, 12),
        D0_band=(3, 4),
        D1_band=(0, 1),
        d_band=(1, 2),
    )
    assert not result.physical_model_compatible


def test_zero_intact_output_with_positive_new_D_forces_mu_one():
    result = project_direct_mu_absolute_bands(
        G1_band=(0, 0),
        D0_band=(1, 1),
        D1_band=(3, 4),
        d_band=(1, 1),
    )
    assert result.physical_model_compatible
    assert result.mu_low == 1
    assert result.mu_high == 1


def test_zero_new_D_with_G_band_touching_zero_still_identifies_mu_zero():
    result = project_direct_mu_absolute_bands(
        G1_band=(0, 5),
        D0_band=(2, 2),
        D1_band=(4, 4),
        d_band=(2, 2),
    )
    assert result.physical_model_compatible
    assert result.new_D_low == 0
    assert result.new_D_high == 0
    assert result.mu_low == 0
    assert result.mu_high == 0


def test_all_zero_output_is_incompatible():
    result = project_direct_mu_absolute_bands(
        G1_band=(0, 0),
        D0_band=(0, 0),
        D1_band=(0, 0),
        d_band=(0, 0),
    )
    assert not result.physical_model_compatible
