"""Persistent physiological-state extension of the serial two-clock model.

Post-freeze PAYOFF-B theory, formulated after the mule-deer pure-handoff audit.

The serial baseline assumes a developmental/physiological clock sets entry phase
e_0 and then hands control fully to a post-entry feedback controller.  This
module allows a physiological state s to persist after entry:

    s_(k+1) = rho s_k
    e_(k+1) = lambda e_k + psi s_k

with no new innovation in the exact witness.

The closed form is

    e_n = lambda^n e_0 + psi H_n(lambda,rho) s_0

where

    H_n = sum_{j=0}^{n-1} lambda^(n-1-j) rho^j
        = (lambda^n-rho^n)/(lambda-rho), lambda != rho.

The pure serial handoff is psi=0.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


_TOL=1e-12


@dataclass(frozen=True)
class PersistentStatePhase:
    steps:int
    entry_phase:float
    state_0:float
    phase_retention:float
    state_retention:float
    state_effect:float
    convolution:float
    propagated_entry_component:float
    persistent_state_component:float
    final_phase:float


@dataclass(frozen=True)
class PersistentStateVariance:
    steps:int
    phase_retention:float
    state_retention:float
    state_effect:float
    convolution:float
    entry_variance:float
    state_variance:float
    entry_state_covariance:float
    entry_component:float
    state_component:float
    covariance_component:float
    final_variance:float


@dataclass(frozen=True)
class PairPersistentMismatch:
    steps:int
    serial_component:float
    persistent_state_component:float
    final_mismatch:float
    actor_1_final_phase:float
    actor_2_final_phase:float


def _finite(name:str,value:float)->float:
    x=float(value)
    if not isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _nonnegative(name:str,value:float)->float:
    x=_finite(name,value)
    if x<0.0:
        raise ValueError(f"{name} must be non-negative")
    return x


def geometric_convolution(
    phase_retention:float,
    state_retention:float,
    *,
    steps:int,
)->float:
    """Return H_n(lambda,rho) for the persistent-state convolution."""

    lam=_finite("phase_retention",phase_retention)
    rho=_finite("state_retention",state_retention)
    n=int(steps)
    if n<0:
        raise ValueError("steps must be non-negative")
    if n==0:
        return 0.0
    if abs(lam-rho)<=_TOL:
        return n*(lam**(n-1))
    return (lam**n-rho**n)/(lam-rho)


def persistent_state_phase(
    *,
    entry_phase:float,
    state_0:float,
    phase_retention:float,
    state_retention:float,
    state_effect:float,
    steps:int,
)->PersistentStatePhase:
    """Return exact phase after n post-entry checkpoints."""

    e0=_finite("entry_phase",entry_phase)
    s0=_finite("state_0",state_0)
    lam=_finite("phase_retention",phase_retention)
    rho=_finite("state_retention",state_retention)
    psi=_finite("state_effect",state_effect)
    n=int(steps)
    if n<0:
        raise ValueError("steps must be non-negative")

    h=geometric_convolution(lam,rho,steps=n)
    entry=(lam**n)*e0
    state=psi*h*s0
    return PersistentStatePhase(
        steps=n,
        entry_phase=e0,
        state_0=s0,
        phase_retention=lam,
        state_retention=rho,
        state_effect=psi,
        convolution=h,
        propagated_entry_component=entry,
        persistent_state_component=state,
        final_phase=entry+state,
    )


def persistent_state_variance(
    *,
    entry_variance:float,
    state_variance:float,
    entry_state_covariance:float,
    phase_retention:float,
    state_retention:float,
    state_effect:float,
    steps:int,
)->PersistentStateVariance:
    """Return exact final variance under the linear persistent-state witness.

    With

        e_n = A e_0 + B s_0,

    A=lambda^n and B=psi H_n. Therefore

        Var(e_n)=A^2 Var(e_0)+B^2 Var(s_0)+2AB Cov(e_0,s_0).
    """

    ve=_nonnegative("entry_variance",entry_variance)
    vs=_nonnegative("state_variance",state_variance)
    cov=_finite("entry_state_covariance",entry_state_covariance)
    lam=_finite("phase_retention",phase_retention)
    rho=_finite("state_retention",state_retention)
    psi=_finite("state_effect",state_effect)
    n=int(steps)
    if n<0:
        raise ValueError("steps must be non-negative")

    max_cov=(ve*vs)**0.5
    if abs(cov)>max_cov+1e-10:
        raise ValueError("entry_state_covariance violates Cauchy-Schwarz bound")

    h=geometric_convolution(lam,rho,steps=n)
    A=lam**n
    B=psi*h
    entry=A*A*ve
    state=B*B*vs
    cross=2.0*A*B*cov
    final=entry+state+cross
    if final<0.0 and final>-1e-10:
        final=0.0
    if final<0.0:
        raise AssertionError("computed negative variance")

    return PersistentStateVariance(
        steps=n,
        phase_retention=lam,
        state_retention=rho,
        state_effect=psi,
        convolution=h,
        entry_variance=ve,
        state_variance=vs,
        entry_state_covariance=cov,
        entry_component=entry,
        state_component=state,
        covariance_component=cross,
        final_variance=final,
    )


def ideal_conditional_state_coefficient(
    *,
    phase_retention:float,
    state_retention:float,
    state_effect:float,
    steps:int,
)->float:
    """Return ideal structural coefficient of s_0 conditional on e_0."""

    lam=_finite("phase_retention",phase_retention)
    rho=_finite("state_retention",state_retention)
    psi=_finite("state_effect",state_effect)
    return psi*geometric_convolution(lam,rho,steps=steps)


def pair_persistent_mismatch(
    *,
    actor_1_entry_phase:float,
    actor_2_entry_phase:float,
    actor_1_state:float,
    actor_2_state:float,
    lambda_1:float,
    lambda_2:float,
    rho_1:float,
    rho_2:float,
    psi_1:float,
    psi_2:float,
    steps:int,
)->PairPersistentMismatch:
    """Decompose pairwise mismatch into serial and persistent-state terms."""

    a1=persistent_state_phase(
        entry_phase=actor_1_entry_phase,
        state_0=actor_1_state,
        phase_retention=lambda_1,
        state_retention=rho_1,
        state_effect=psi_1,
        steps=steps,
    )
    a2=persistent_state_phase(
        entry_phase=actor_2_entry_phase,
        state_0=actor_2_state,
        phase_retention=lambda_2,
        state_retention=rho_2,
        state_effect=psi_2,
        steps=steps,
    )
    serial=(float(lambda_1)**int(steps))*float(actor_1_entry_phase) - (float(lambda_2)**int(steps))*float(actor_2_entry_phase)
    persistent=a1.persistent_state_component-a2.persistent_state_component
    final=a1.final_phase-a2.final_phase
    if abs(final-(serial+persistent))>1e-10:
        raise AssertionError("persistent-state mismatch identity failed")
    return PairPersistentMismatch(
        steps=int(steps),
        serial_component=serial,
        persistent_state_component=persistent,
        final_mismatch=final,
        actor_1_final_phase=a1.final_phase,
        actor_2_final_phase=a2.final_phase,
    )
