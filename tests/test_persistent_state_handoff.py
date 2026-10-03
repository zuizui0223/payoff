import pytest

from src.persistent_state_handoff import (
    downstream_state_coefficient,
    handoff_kernel,
    persistent_state_closed_form,
    persistent_state_step,
    pure_entry_only_special_case,
    state_half_life_checkpoints,
)


def test_one_step_persistent_state_update():
    r=persistent_state_step(
        10.0,2.0,
        phase_retention=0.5,
        state_persistence=0.8,
        state_to_phase_effect=-1.5,
        phase_innovation=1.0,
    )
    assert r.next_phase_error == pytest.approx(3.0)
    assert r.next_physiological_state == pytest.approx(1.6)


def test_handoff_kernel_matches_explicit_sum():
    lam=0.6
    rho=0.8
    n=4
    explicit=sum(lam**(n-1-j)*rho**j for j in range(n))
    assert handoff_kernel(
        phase_retention=lam,
        state_persistence=rho,
        steps=n,
    ) == pytest.approx(explicit)


def test_equal_lambda_rho_limit():
    assert handoff_kernel(
        phase_retention=0.5,
        state_persistence=0.5,
        steps=3,
    ) == pytest.approx(3*0.5**2)


def test_closed_form_matches_iteration():
    e=7.0
    s=3.0
    lam=0.7
    rho=0.6
    beta=-0.4
    for _ in range(5):
        step=persistent_state_step(
            e,s,
            phase_retention=lam,
            state_persistence=rho,
            state_to_phase_effect=beta,
        )
        e,s=step.next_phase_error,step.next_physiological_state

    closed=persistent_state_closed_form(
        7.0,3.0,
        phase_retention=lam,
        state_persistence=rho,
        state_to_phase_effect=beta,
        steps=5,
    )
    assert closed.final_phase_error == pytest.approx(e)


def test_pure_entry_only_is_beta_zero_special_case():
    closed=persistent_state_closed_form(
        8.0,5.0,
        phase_retention=0.4,
        state_persistence=0.9,
        state_to_phase_effect=0.0,
        steps=3,
    )
    assert closed.final_phase_error == pytest.approx(
        pure_entry_only_special_case(
            8.0,
            phase_retention=0.4,
            steps=3,
        )
    )


def test_persistent_state_predicts_downstream_phase_after_conditioning_on_entry():
    coeff=downstream_state_coefficient(
        phase_retention=0.5,
        state_persistence=0.8,
        state_to_phase_effect=-2.0,
        steps=2,
    )
    # H_2 = lambda + rho = 1.3
    assert coeff == pytest.approx(-2.6)


def test_zero_persistence_affects_only_first_post_entry_step():
    c1=downstream_state_coefficient(
        phase_retention=0.6,
        state_persistence=0.0,
        state_to_phase_effect=2.0,
        steps=1,
    )
    c3=downstream_state_coefficient(
        phase_retention=0.6,
        state_persistence=0.0,
        state_to_phase_effect=2.0,
        steps=3,
    )
    assert c1 == pytest.approx(2.0)
    assert c3 == pytest.approx(2.0*0.6**2)


def test_state_half_life():
    assert state_half_life_checkpoints(0.5) == pytest.approx(1.0)


def test_steps_zero_has_no_state_carryover():
    closed=persistent_state_closed_form(
        3.0,4.0,
        phase_retention=0.7,
        state_persistence=0.9,
        state_to_phase_effect=2.0,
        steps=0,
    )
    assert closed.handoff_kernel == pytest.approx(0.0)
    assert closed.final_phase_error == pytest.approx(3.0)
