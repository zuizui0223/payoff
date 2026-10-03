"""Persistent physiological-state handoff for PAYOFF-B.

Post-hoc post-freeze extension motivated by the mule-deer serial handoff audit.

The pure serial model assumes that physiological readiness affects entry timing
but disappears from the downstream phase dynamics.  This extension allows a
pre-entry physiological state s to persist after entry:

    s_(k+1) = rho s_k
    e_(k+1) = lambda e_k + beta s_k + w_k

where:
- lambda is post-entry phase retention;
- rho is physiological-state persistence;
- beta is the direct downstream effect of the physiological state;
- w_k is new phase innovation.

For w_k=0 and s_0=s,

    e_n = lambda^n e_0 + beta s H_n(lambda,rho)

with

    H_n = sum_{j=0}^{n-1} lambda^(n-1-j) rho^j
        = (lambda^n-rho^n)/(lambda-rho), lambda != rho
        = n lambda^(n-1), lambda = rho.

Thus a physiological variable can predict downstream phase after conditioning
on entry phase without being the same mechanism as the decision controller.

The model is explicitly post hoc relative to the mule-deer handoff audit.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log


_TOL=1e-12


@dataclass(frozen=True)
class PersistentStateStep:
    phase_error: float
    physiological_state: float
    phase_retention: float
    state_persistence: float
    state_to_phase_effect: float
    phase_innovation: float
    next_phase_error: float
    next_physiological_state: float


@dataclass(frozen=True)
class PersistentStateClosedForm:
    steps: int
    initial_phase_error: float
    initial_physiological_state: float
    phase_retention: float
    state_persistence: float
    state_to_phase_effect: float
    handoff_kernel: float
    phase_from_entry_error: float
    phase_from_persistent_state: float
    final_phase_error: float



@dataclass(frozen=True)
class PersistentPairMismatch:
    """Three-component pairwise mismatch decomposition."""

    steps: int
    controller_generated_component: float
    entry_timer_component: float
    persistent_state_component: float
    final_mismatch: float

def _finite(name:str,value:float)->float:
    x=float(value)
    if not isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _nonnegative_int(name:str,value:int)->int:
    x=int(value)
    if x<0 or x!=value:
        raise ValueError(f"{name} must be a non-negative integer")
    return x


def persistent_state_step(
    phase_error:float,
    physiological_state:float,
    *,
    phase_retention:float,
    state_persistence:float,
    state_to_phase_effect:float,
    phase_innovation:float=0.0,
)->PersistentStateStep:
    """Propagate one post-entry checkpoint."""

    e=_finite("phase_error",phase_error)
    s=_finite("physiological_state",physiological_state)
    lam=_finite("phase_retention",phase_retention)
    rho=_finite("state_persistence",state_persistence)
    beta=_finite("state_to_phase_effect",state_to_phase_effect)
    w=_finite("phase_innovation",phase_innovation)

    return PersistentStateStep(
        phase_error=e,
        physiological_state=s,
        phase_retention=lam,
        state_persistence=rho,
        state_to_phase_effect=beta,
        phase_innovation=w,
        next_phase_error=lam*e+beta*s+w,
        next_physiological_state=rho*s,
    )


def handoff_kernel(
    *,
    phase_retention:float,
    state_persistence:float,
    steps:int,
)->float:
    """Return H_n(lambda,rho) for the persistent-state contribution."""

    lam=_finite("phase_retention",phase_retention)
    rho=_finite("state_persistence",state_persistence)
    n=_nonnegative_int("steps",steps)
    if n==0:
        return 0.0
    if abs(lam-rho)<=_TOL:
        return n*(lam**(n-1))
    return (lam**n-rho**n)/(lam-rho)


def persistent_state_closed_form(
    initial_phase_error:float,
    initial_physiological_state:float,
    *,
    phase_retention:float,
    state_persistence:float,
    state_to_phase_effect:float,
    steps:int,
)->PersistentStateClosedForm:
    """Closed form for the zero-innovation persistent-state model."""

    e0=_finite("initial_phase_error",initial_phase_error)
    s0=_finite("initial_physiological_state",initial_physiological_state)
    lam=_finite("phase_retention",phase_retention)
    rho=_finite("state_persistence",state_persistence)
    beta=_finite("state_to_phase_effect",state_to_phase_effect)
    n=_nonnegative_int("steps",steps)

    H=handoff_kernel(
        phase_retention=lam,
        state_persistence=rho,
        steps=n,
    )
    from_entry=(lam**n)*e0
    from_state=beta*s0*H
    return PersistentStateClosedForm(
        steps=n,
        initial_phase_error=e0,
        initial_physiological_state=s0,
        phase_retention=lam,
        state_persistence=rho,
        state_to_phase_effect=beta,
        handoff_kernel=H,
        phase_from_entry_error=from_entry,
        phase_from_persistent_state=from_state,
        final_phase_error=from_entry+from_state,
    )


def state_half_life_checkpoints(state_persistence:float)->float:
    """Return the persistence half-life in checkpoints for 0<rho<1."""

    rho=_finite("state_persistence",state_persistence)
    if rho<=0.0 or rho>=1.0:
        raise ValueError("state_persistence must lie in (0,1)")
    return log(0.5)/log(rho)


def downstream_state_coefficient(
    *,
    phase_retention:float,
    state_persistence:float,
    state_to_phase_effect:float,
    steps:int,
)->float:
    """Coefficient on s0 in e_n conditional on e0 in the linear witness."""

    beta=_finite("state_to_phase_effect",state_to_phase_effect)
    return beta*handoff_kernel(
        phase_retention=phase_retention,
        state_persistence=state_persistence,
        steps=steps,
    )


def pure_entry_only_special_case(
    initial_phase_error:float,
    *,
    phase_retention:float,
    steps:int,
)->float:
    """Pure Markov handoff recovered when beta=0 or no persistent state exists."""

    e0=_finite("initial_phase_error",initial_phase_error)
    lam=_finite("phase_retention",phase_retention)
    n=_nonnegative_int("steps",steps)
    return (lam**n)*e0


def persistent_pair_mismatch_decomposition(
    *,
    initial_mean_error: float,
    initial_mismatch: float,
    lambda_1: float,
    lambda_2: float,
    state_1: float,
    state_2: float,
    state_persistence_1: float,
    state_persistence_2: float,
    state_to_phase_effect_1: float,
    state_to_phase_effect_2: float,
    steps: int,
) -> PersistentPairMismatch:
    """Decompose mismatch into controller, entry-timer and carry-over terms.

    Actor i has zero-innovation solution

        e_i,n
          = lambda_i^n e_i,0
            + beta_i s_i,0 H_n(lambda_i,rho_i).

    Therefore

        Delta_n
          = (lambda_1^n-lambda_2^n)m_0
            + 0.5(lambda_1^n+lambda_2^n)Delta_0
            + beta_1 s_1,0 H_1
            - beta_2 s_2,0 H_2.
    """

    m0=_finite("initial_mean_error",initial_mean_error)
    d0=_finite("initial_mismatch",initial_mismatch)
    l1=_finite("lambda_1",lambda_1)
    l2=_finite("lambda_2",lambda_2)
    s1=_finite("state_1",state_1)
    s2=_finite("state_2",state_2)
    r1=_finite("state_persistence_1",state_persistence_1)
    r2=_finite("state_persistence_2",state_persistence_2)
    b1=_finite("state_to_phase_effect_1",state_to_phase_effect_1)
    b2=_finite("state_to_phase_effect_2",state_to_phase_effect_2)
    n=_nonnegative_int("steps",steps)

    p1=l1**n
    p2=l2**n
    controller=(p1-p2)*m0
    entry=0.5*(p1+p2)*d0

    h1=handoff_kernel(
        phase_retention=l1,
        state_persistence=r1,
        steps=n,
    )
    h2=handoff_kernel(
        phase_retention=l2,
        state_persistence=r2,
        steps=n,
    )
    persistent=b1*s1*h1-b2*s2*h2

    e10=m0+0.5*d0
    e20=m0-0.5*d0
    e1=persistent_state_closed_form(
        e10,s1,
        phase_retention=l1,
        state_persistence=r1,
        state_to_phase_effect=b1,
        steps=n,
    ).final_phase_error
    e2=persistent_state_closed_form(
        e20,s2,
        phase_retention=l2,
        state_persistence=r2,
        state_to_phase_effect=b2,
        steps=n,
    ).final_phase_error
    final=e1-e2

    if abs(final-(controller+entry+persistent))>1e-10:
        raise AssertionError("persistent pairwise decomposition failed")

    return PersistentPairMismatch(
        steps=n,
        controller_generated_component=controller,
        entry_timer_component=entry,
        persistent_state_component=persistent,
        final_mismatch=final,
    )
