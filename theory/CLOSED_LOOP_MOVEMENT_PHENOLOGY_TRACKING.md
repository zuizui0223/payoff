# Closed-loop movement--phenology tracking

## Question

The main moving-landscape model treats migration and phenology response rates as
fixed heritable tracking controls.

The empirical controller literature adds a different mechanism:

> organisms can change movement or stopover behavior as a function of current
> phase mismatch.

This file isolates the minimal local feedback problem.

It is not a replacement for the explicit landscape. It is the analytically
closed local controller sitting underneath it.

## 1. Mismatch recurrence

Let

    e_t

be climate-equivalent mismatch at decision interval t.

After baseline tracking of the moving environment, let

    r

be the residual forcing still added each interval.

Let

    q_m >= 0

be movement-mediated feedback gain: the fraction of current mismatch corrected
through state-dependent movement.

Let

    q_h >= 0

be timing-mediated feedback gain.

For the existing PAYOFF-B phenology rate h,

    q_h = 1 - exp(-h).

The local closed-loop recurrence is

    e_(t+1)
    = e_t + r - q_m e_t - q_h e_t

or

    e_(t+1)
    = (1-K)e_t + r,

with

    K = q_m + q_h.

Thus spatial/behavioral feedback and timing feedback enter one exact local
restoring budget.

## 2. Exact stability classes

The multiplier is

    a = 1-K.

The equilibrium is dynamically stable iff

    |1-K| < 1,

equivalently

    0 < K < 2.

Therefore:

    K = 0
        no feedback;

    0 < K < 1
        stable monotone correction;

    K = 1
        one-step / deadbeat correction;

    1 < K < 2
        stable alternating overshoot;

    K = 2
        neutral two-cycle;

    K > 2
        oscillatory instability.

The exact stable equilibrium mismatch is

    e* = r/K.

This creates a sharp distinction absent from the open-loop capacity model:

> more total feedback reduces steady mismatch only until excessive discrete
> feedback creates oscillatory instability.

## 3. Exact local space-time substitutability

For any two controller architectures satisfying

    q_m + q_h = K,

the mismatch recurrence is identical.

Hence, before costs, ceilings, route geometry, or partner effects are added,

    movement feedback
    and
    timing feedback

are exactly substitutable in the local linear mismatch dynamics.

This is stronger than saying they are correlated or qualitatively redundant.

It is an equality of the declared local control system.

The explicit landscape breaks this exact equivalence through:

- movement geometry;
- habitat barriers;
- direction-specific dispersal;
- finite phenological shift capacity;
- different architecture costs;
- interaction-partner matching.

So the local theorem provides the null model against which those departures are
measured.

## 4. Minimum-cost allocation at fixed total feedback

Assume quadratic controller costs

    C
    = 0.5 c_m q_m^2
      + 0.5 c_h q_h^2,

with

    c_m > 0,
    c_h > 0.

At fixed total feedback K,

    q_m + q_h = K,

the unique unconstrained minimum-cost allocation is

    q_m*
    = K c_h/(c_m+c_h),

    q_h*
    = K c_m/(c_m+c_h).

Thus the more expensive movement feedback becomes, the more of the required
restoring gain is assigned to timing, and vice versa.

The minimized feedback cost is

    C_min(K)
    = 0.5 c_eff K^2,

where

    c_eff
    = c_m c_h/(c_m+c_h).

The two feedback channels therefore combine like parallel cost pathways: adding
a second usable axis reduces the effective cost of generating a given total
restoring gain.

## 5. Closed-form optimal total feedback

Add a steady mismatch penalty

    0.5 A e*^2

with

    A > 0.

Since

    e* = r/K,

the minimized steady objective is

    J(K)
    = 0.5 A r^2/K^2
      + 0.5 c_eff K^2.

The unconstrained interior optimum satisfies

    K*^4
    = A r^2/c_eff,

so

    K*
    = [A r^2/c_eff]^(1/4).

The corresponding controller allocation is

    q_m*
    = K* c_h/(c_m+c_h),

    q_h*
    = K* c_m/(c_m+c_h).

This interior solution must still pass two gates:

1. dynamic stability:

       K* < 2;

2. finite timing-rate feasibility:

       q_h* < 1

   because finite PAYOFF-B h generates

       q_h = 1-exp(-h) < 1.

When either condition fails, the constrained optimum lies on a boundary and the
explicit finite-capacity model must be used.

## 6. Scaling with forcing

The unconstrained total controller gain obeys

    K*
    proportional to
    |r|^(1/2).

So the optimal feedback strength grows only with the square root of residual
forcing under the declared quadratic mismatch / quadratic control-cost model.

The equilibrium mismatch at the optimum is

    |e*|
    = |r|/K*
    proportional to
    |r|^(1/2).

Thus stronger environmental forcing raises both optimal controller strength and
remaining mismatch.

The controller does not make arbitrary forcing free.

## 7. Relationship to the Aikens phase-error controller

The Aikens empirical layer estimates local route-distance mismatch correction.

For local route coordinate x, write

    de/dx
    = -kappa_x e.

Then after forward displacement Delta x,

    e_after/e_before
    = exp(-kappa_x Delta x).

The equivalent one-step feedback fraction is

    q_controller
    = 1-exp(-kappa_x Delta x).

The implementation exposes this bridge through

    route_relaxation_to_step_feedback(...).

This conversion is licensed only when:

- the regression distance unit is confirmed;
- a forward distance per PAYOFF-B decision interval is declared;
- the local exponential approximation is accepted.

The published Aikens controller sign evidence alone therefore identifies
restoring versus non-restoring behavior, not a calibrated q_m.

## 8. Relationship to fixed migration rate

The closed-loop q_m is not the same object as the fixed migration-rate parameter
m used by the explicit landscape kernel.

They answer different questions:

    m:
        how strongly individuals redistribute spatially per step under the
        declared movement kernel;

    q_m:
        how strongly current mismatch feeds back onto corrective movement.

A named empirical system can have:

    large m but weak feedback,
    small m but strong state dependence,
    or both.

Conflating those quantities would erase the empirical distinction between
movement capacity and movement control.

## 9. Relationship to phenology h

The existing timing rate h maps exactly to

    q_h = 1-exp(-h).

Thus h is an intrinsic timing-axis response parameter in the current model.

A movement-mediated phase controller does not identify h.

This preserves the empirical separation already frozen in the mule-deer and
Aikens receipts:

    movement / stopover controller
    !=
    independent timing-axis response.

## 10. Reproduce

Core implementation:

    src/closed_loop_tracking.py

Tests:

    tests/test_closed_loop_tracking.py

Phase sweep:

    python scripts/closed_loop_tracking_phase_sweep.py

The sweep records:

- residual forcing;
- movement feedback gain;
- phenology rate and feedback fraction;
- total feedback gain;
- stability class;
- exact equilibrium mismatch;
- simulated mismatch;
- steady quadratic objective.

It also writes the closed-form unconstrained optimum for each forcing level.

## 11. Claim boundary

The exact results above hold for the declared local linear recurrence.

They do not establish that:

- natural movement controllers are linear in phase error;
- movement and phenology are globally interchangeable across real landscapes;
- published route-distance slopes directly equal q_m;
- controller gains are constant across environmental contexts;
- the quadratic controller costs are empirically correct;
- a stable local controller guarantees demographic persistence.

Preferred:

> In the declared local tracking model, movement-mediated and
> phenology-mediated feedback enter the same restoring gain, while costs and
> capacity constraints determine their allocation.

Avoid:

> Animals can always replace migration with phenology under climate change.

Preferred:

> Excessive combined feedback can cross the discrete-time stability boundary
> and produce alternating mismatch.

Avoid:

> Stronger behavioral response is always better.
