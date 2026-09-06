from math import isclose

from src.invasion import identify_phi_eta, invasion_margins, invasion_regime


def test_two_edge_identification_is_exact():
    for phi, eta in [(-0.7, -1.2), (0.0, 0.3), (0.8, 0.0), (0.4, 1.1)]:
        delta0 = phi - eta
        delta1 = phi + eta
        recovered_phi, recovered_eta = identify_phi_eta(delta0, delta1)
        assert isclose(recovered_phi, phi, abs_tol=1e-12)
        assert isclose(recovered_eta, eta, abs_tol=1e-12)


def test_negative_frequency_dependence_gives_mutual_invasion_wedge():
    assert invasion_regime(phi=0.2, eta=-1.0) == "mutual_invasion"
    d_margin, s_margin = invasion_margins(phi=0.2, eta=-1.0)
    assert d_margin > 0
    assert s_margin > 0


def test_positive_frequency_dependence_gives_mutual_noninvasion_wedge():
    assert invasion_regime(phi=0.2, eta=1.0) == "mutual_noninvasion"
    d_margin, s_margin = invasion_margins(phi=0.2, eta=1.0)
    assert d_margin < 0
    assert s_margin < 0


def test_negative_feedback_can_rescue_d_inside_static_balance():
    # phi<0 says shared wins in the frequency-independent comparison,
    # but a sufficiently negative eta lets rare D invade.
    phi, eta = -0.2, -1.0
    d_margin, _ = invasion_margins(phi, eta)
    assert phi < 0
    assert d_margin > 0


def test_positive_feedback_can_block_d_inside_static_bita():
    # phi>0 says differentiated wins statically,
    # but positive frequency dependence can block invasion when D is rare.
    phi, eta = 0.2, 1.0
    d_margin, _ = invasion_margins(phi, eta)
    assert phi > 0
    assert d_margin < 0


def test_invasion_boundaries():
    assert invasion_regime(phi=1.0, eta=1.0) == "invasion_boundary"
    assert invasion_regime(phi=-1.0, eta=1.0) == "invasion_boundary"
