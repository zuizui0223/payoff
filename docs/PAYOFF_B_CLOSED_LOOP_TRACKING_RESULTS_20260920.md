# PAYOFF-B closed-loop movement--phenology tracking receipt

Frozen: 2026-09-20

Status: **exact local control theory + synthetic numerical witness**.

This receipt adds a closed-loop controller layer to the migration--phenology
tracking framework.

It is distinct from the explicit landscape model:

- the landscape asks how fixed tracking controls perform in space;
- the closed-loop model asks how current mismatch feeds back onto corrective
  movement and timing.

## 1. Exact recurrence

Let e_t be climate-equivalent mismatch and r the residual environmental forcing
remaining after baseline tracking.

Let q_m be movement-mediated feedback and q_h timing-mediated feedback.

Then

    e_(t+1)
    = (1 - q_m - q_h) e_t + r.

For the existing PAYOFF-B timing rate h,

    q_h = 1 - exp(-h).

Define

    K = q_m + q_h.

The local dynamics therefore depend on movement and timing feedback only
through their sum K before costs, ceilings, route geometry, or partner effects
are added.

## 2. Exact stability boundary

The multiplier is

    1-K.

Hence:

    0 < K < 1
        stable monotone correction;

    K = 1
        one-step deadbeat correction;

    1 < K < 2
        stable alternating / overshooting correction;

    K = 2
        neutral two-cycle;

    K > 2
        oscillatory instability.

The stable equilibrium mismatch is

    e* = r/K.

Thus stronger restoring feedback is not universally beneficial in discrete
time: total gain above 2 destabilizes the local controller.

## 3. Exact space-time feedback substitutability

Any two local controller architectures satisfying

    q_m + q_h = K

have the same mismatch recurrence.

Therefore movement-mediated feedback and timing-mediated feedback are exactly
substitutable in the declared local linear controller before their different
costs and constraints are applied.

This is the null theorem underlying the more complicated spatial results.

## 4. Minimum-cost allocation

For quadratic feedback costs

    C
    = 0.5 c_m q_m^2
      + 0.5 c_h q_h^2,

the minimum-cost allocation at fixed K is

    q_m*
    = K c_h/(c_m+c_h),

    q_h*
    = K c_m/(c_m+c_h).

The effective cost coefficient is

    c_eff
    = c_m c_h/(c_m+c_h).

With steady mismatch penalty

    0.5 A e*^2,

the unconstrained optimal total gain is

    K*
    = [A r^2 / c_eff]^(1/4).

This interior optimum is usable only when

    K* < 2

and, for the existing finite timing-rate channel,

    q_h* < 1.

## 5. Equal-cost synthetic witness

Workflow run:

    35495157481

Equal feedback costs:

    c_m = 1
    c_h = 1
    A   = 1.

Forcing r=0.05:

    K*  = 0.265914794847
    q_m = 0.132957397424
    q_h = 0.132957397424
    e*  = 0.188030154654.

Forcing r=0.2:

    K*  = 0.531829589694
    q_m = 0.265914794847
    q_h = 0.265914794847
    e*  = 0.376060309309.

Forcing r=1:

    K*  = 1.189207115
    q_m = 0.594603557501
    q_h = 0.594603557501
    e*  = 0.840896415254.

Forcing r=4:

    K*  = 2.37841423001
    q_m = 1.189207115
    q_h = 1.189207115
    e*  = 1.68179283051.

The last unconstrained optimum is outside both relevant feasibility regions:

    K*>2
        -> local discrete-time instability;

    q_h*>1
        -> not representable by any finite PAYOFF-B h.

Thus high forcing can push the unconstrained economic optimum outside the
dynamically or biologically realizable controller region.

The equal-cost phase grid contains all declared controller classes:

    no feedback,
    stable monotone,
    deadbeat,
    stable oscillatory,
    neutral two-cycle,
    oscillatory unstable.

## 6. Cost-asymmetry witness

Movement expensive:

    c_m = 4
    c_h = 1.

At r=0.2:

    K*  = 0.472870804502
    q_m = 0.0945741609003
    q_h = 0.378296643601.

Thus 80% of the optimal feedback budget is assigned to the cheaper timing
channel.

At r=1:

    q_m = 0.211474252688
    q_h = 0.845897010752.

Phenology expensive:

    c_m = 1
    c_h = 4.

The allocation mirrors exactly.

At r=0.2:

    q_m = 0.378296643601
    q_h = 0.0945741609003.

At r=1:

    q_m = 0.845897010752
    q_h = 0.211474252688.

The controller therefore allocates restoring effort toward the cheaper axis,
while total restoring gain is determined by forcing, mismatch cost, and the
combined effective controller cost.

## 7. Relationship to Aikens 2022

The published Aikens phase-controller analysis provides empirical evidence for
context-dependent restoring or non-restoring route-distance controllers.

For a local route model

    de/dx = -kappa_x e,

a forward displacement Delta x corresponds, under a local exponential
approximation, to step feedback

    q_controller
    = 1 - exp(-kappa_x Delta x).

This bridge is implemented, but numeric conversion requires confirmed distance
units and a declared distance per model decision interval.

The Aikens route slope therefore motivates and constrains the sign/strength of
movement-mediated feedback. It does not identify the independent timing-axis
h.

## 8. Relationship to fixed movement capacity

The feedback gain q_m is not the fixed migration rate m.

The two objects are:

    m:
        baseline redistribution capacity under the declared movement kernel;

    q_m:
        state-dependent correction of current mismatch through movement.

A species can have high movement capacity and weak controller response, or low
baseline movement with strong state dependence.

This distinction is required for empirical interpretation.

## 9. Provenance

Equal-cost witness:

    workflow run:
        35495157481

    artifact:
        10600532697

    sha256:
        a60b5b99da70e80ec5dfd0ccf6cf815d85477edd356396869d4448dc5e489ed5

Movement-expensive witness:

    artifact:
        10599788900

    sha256:
        274d69410980560fffbbf036ce951b4577deb88ae3aefc77da68ba937d72563d

Phenology-expensive witness:

    artifact:
        10599359831

    sha256:
        df0c97911395753e336a55e789da0174fb80ffd84c750fdcbd3b82bbd9904e0e

Core implementation:

    src/closed_loop_tracking.py

Tests:

    tests/test_closed_loop_tracking.py

Sweep:

    scripts/closed_loop_tracking_phase_sweep.py

Theory:

    theory/CLOSED_LOOP_MOVEMENT_PHENOLOGY_TRACKING.md

## 10. Retained interpretation

The retained local-control result is:

> movement-mediated and timing-mediated feedback are exact substitutes in the
> local first-order mismatch equation, but cost asymmetry allocates restoring
> effort between them and excessive total feedback can cross a discrete-time
> stability boundary.

This extends PAYOFF-B from an open-loop adaptive-axis model to a closed-loop
tracking-controller model.

## 11. Claim boundary

These are exact statements for the declared local linear recurrence and
quadratic controller costs.

They are not natural estimates of controller gain or climate tolerance.

In particular this receipt does not establish:

- that route-distance controller response is globally linear;
- that movement-controller gain is constant across individuals or contexts;
- that timing and movement are globally interchangeable in fragmented
  landscapes;
- that controller instability occurs in the mule-deer systems;
- that the synthetic cost coefficients are empirical.

The explicit spatial model remains necessary once route geometry, barriers,
finite timing capacity, demography, and partner matching matter.
