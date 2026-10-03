import pytest

from src.persistent_state_two_clock import (
    geometric_convolution,
    ideal_conditional_state_coefficient,
    pair_persistent_mismatch,
    persistent_state_phase,
    persistent_state_variance,
)


def test_geometric_convolution_matches_direct_sum():
    lam=0.7
    rho=0.4
    n=5
    direct=sum(lam**(n-1-j)*rho**j for j in range(n))
    assert geometric_convolution(lam,rho,steps=n)==pytest.approx(direct)


def test_equal_retention_limit_is_exact():
    assert geometric_convolution(0.5,0.5,steps=4)==pytest.approx(4*0.5**3)


def test_zero_state_effect_recovers_pure_serial_handoff():
    r=persistent_state_phase(
        entry_phase=10.0,
        state_0=3.0,
        phase_retention=0.6,
        state_retention=0.8,
        state_effect=0.0,
        steps=3,
    )
    assert r.persistent_state_component==pytest.approx(0.0)
    assert r.final_phase==pytest.approx(0.6**3*10.0)


def test_persistent_state_adds_direct_downstream_component():
    r=persistent_state_phase(
        entry_phase=4.0,
        state_0=2.0,
        phase_retention=0.5,
        state_retention=1.0,
        state_effect=-1.5,
        steps=3,
    )
    h=sum(0.5**(2-j) for j in range(3))
    assert r.persistent_state_component==pytest.approx(-1.5*h*2.0)
    assert r.final_phase==pytest.approx(0.5**3*4.0-1.5*h*2.0)


def test_conditional_state_coefficient_equals_structural_carryover():
    coef=ideal_conditional_state_coefficient(
        phase_retention=0.7,
        state_retention=0.9,
        state_effect=-2.0,
        steps=2,
    )
    assert coef==pytest.approx(-2.0*(0.7+0.9))


def test_variance_formula_matches_linear_combination():
    r=persistent_state_variance(
        entry_variance=9.0,
        state_variance=4.0,
        entry_state_covariance=1.5,
        phase_retention=0.5,
        state_retention=0.8,
        state_effect=0.4,
        steps=2,
    )
    A=0.5**2
    H=0.5+0.8
    B=0.4*H
    expected=A*A*9.0+B*B*4.0+2*A*B*1.5
    assert r.final_variance==pytest.approx(expected)


def test_invalid_covariance_is_rejected():
    with pytest.raises(ValueError,match="Cauchy"):
        persistent_state_variance(
            entry_variance=1.0,
            state_variance=1.0,
            entry_state_covariance=2.0,
            phase_retention=0.5,
            state_retention=0.5,
            state_effect=1.0,
            steps=1,
        )


def test_pair_mismatch_has_third_persistent_state_component():
    r=pair_persistent_mismatch(
        actor_1_entry_phase=5.0,
        actor_2_entry_phase=5.0,
        actor_1_state=2.0,
        actor_2_state=0.0,
        lambda_1=0.6,
        lambda_2=0.6,
        rho_1=0.9,
        rho_2=0.9,
        psi_1=1.0,
        psi_2=1.0,
        steps=2,
    )
    assert r.serial_component==pytest.approx(0.0)
    assert r.persistent_state_component==pytest.approx((0.6+0.9)*2.0)
    assert r.final_mismatch==pytest.approx(r.persistent_state_component)
