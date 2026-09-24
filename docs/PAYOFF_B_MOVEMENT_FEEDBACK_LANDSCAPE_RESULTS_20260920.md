# PAYOFF-B state-dependent movement-feedback landscape receipt

Frozen: 2026-09-20

Status: **explicit-landscape synthetic controller result**.

This receipt connects the exact local closed-loop theory to the explicit 2D
moving-landscape model.

The local theorem uses an abstract movement-feedback gain q_m. The explicit
landscape instead lets current mismatch alter the actual movement-kernel rate:

    m_eff(t)
    = clip[m_0 + k_m e_t, m_min, m_max].

Positive mismatch means the population lags the moving environmental demand,
so positive controller gain increases the movement rate. Negative mismatch
slows movement toward the lower bound. The directional movement biases
themselves remain fixed.

This is an Aikens-like state-dependent movement controller, but the synthetic
gain k_m is not an empirical estimate from Aikens et al.

## 1. Declared pilot design

Workflow run:

    35495412741

Artifact:

    10599954360

SHA256:

    9d4ef34759f0fc7c69a17a38f34693455307dc3bed897258ef051966f5c228cd

Grid:

    climate velocity:
        0.02, 0.03, 0.04, 0.05, 0.06

    controller gain:
        0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6

    independent timing rate h:
        0, 0.25, 0.5

    baseline migration rate:
        0.1

    movement-rate ceiling:
        1.5

    migration cost:
        0.05

    timing cost:
        0.03

    phenology limit:
        4

    spatial movement:
        fully biased in the positive climate-axis direction

    landscape:
        open 31 x 15 regular grid

    simulation:
        100 steps
        20-step burn-in.

There are

    5 x 7 x 3
    = 105

synthetic cells.

## 2. Weak forcing: feedback is unnecessary

At climate velocity 0.02, the growth-optimal feedback gain is zero for all
three timing rates.

Examples:

    h=0:
        gain 0 growth 0.267099
        RMS mismatch 0.406617

    h=0.25:
        gain 0 growth 0.265653

    h=0.5:
        gain 0 growth 0.261119.

Thus mismatch-dependent movement has no payoff advantage in this weak-forcing
slice once the baseline movement rate is already sufficient.

At v=0.03, feedback is selected only in the h=0 slice:

    h=0:
        best gain 1.6
        growth 0.269765
        versus fixed 0.268037

        RMS mismatch
        0.392935
        versus 0.397354.

The gain is real but small.

## 3. Intermediate forcing: controller value emerges

At v=0.04:

    h=0:
        best gain 0.8
        growth 0.222613
        versus fixed 0.209869

        RMS mismatch
        0.483597
        versus 0.515529

        mean effective migration
        0.298649.

With timing response:

    h=0.25:
        best gain 1.6
        growth 0.271955
        versus fixed 0.265953

        mean effective migration
        0.184523.

    h=0.5:
        best gain 1.6
        growth 0.262597
        versus fixed 0.260810

        mean effective migration
        0.154113.

Thus timing does not simply add another benefit. It changes how much movement
the state-dependent controller must realize.

## 4. Strong forcing: movement feedback alone cannot rescue the system

At v=0.05 with h=0:

    every sampled controller gain:
        non-persistent.

The best low-density-growth controller is

    gain 0.4

with

    growth:
        -0.062513

    versus fixed-rate growth:
        -0.071324

    RMS mismatch:
        0.892125
        versus 0.907520.

The controller improves mismatch and growth, but the system still collapses.

At v=0.06 with h=0:

    every sampled controller gain:
        non-persistent.

Best:

    gain 0.2

    growth:
        -0.678401

    versus fixed:
        -0.688356

    RMS mismatch:
        1.423869
        versus 1.433004.

Again, movement feedback alone is insufficient.

## 5. Timing restores persistence in the same high-forcing slices

At both v=0.05 and v=0.06:

    h=0:
        0/7 controller-gain cells persist

whereas

    h=0.25:
        7/7 persist

    h=0.5:
        7/7 persist.

Importantly, persistence at h>0 is already present at gain 0 in this pilot.
Therefore the correct claim is not:

    movement feedback + timing uniquely rescues persistence.

Instead:

> timing capacity crosses the persistence boundary, while state-dependent
> movement feedback further improves mismatch and low-density growth within
> the persistent timing-enabled regime.

This distinction is retained deliberately.

## 6. Timing sharply reduces movement-controller demand

The strongest sampled feedback gain provides a direct comparison at fixed
controller architecture:

    k_m = 1.6.

At v=0.05:

    h=0:
        mean effective m = 0.751685
        ceiling fraction = 0.2875
        growth = -0.086343
        non-persistent

    h=0.25:
        mean effective m = 0.250782
        ceiling fraction = 0
        growth = 0.280116
        persistent

    h=0.5:
        mean effective m = 0.191582
        ceiling fraction = 0
        growth = 0.269134
        persistent.

At v=0.06:

    h=0:
        mean effective m = 0.947854
        ceiling fraction = 0.45
        growth = -0.713611
        non-persistent

    h=0.25:
        mean effective m = 0.325324
        ceiling fraction = 0
        growth = 0.284509
        persistent

    h=0.5:
        mean effective m = 0.231577
        ceiling fraction = 0
        growth = 0.275850
        persistent.

Thus the independent timing axis sharply unloads the movement controller under
strong forcing.

At v=0.06 and gain=1.6, increasing h from 0 to 0.25 reduces mean effective
movement by about 66%, and h=0.5 reduces it by about 76%, while also removing
all movement-ceiling contact in the sampled run.

## 7. Controller benefit within a timing-enabled regime

Even when timing alone already permits persistence, movement feedback can still
raise low-density growth and reduce mismatch.

At v=0.06:

    h=0.25:
        gain 1.6 growth = 0.284509
        gain 0   growth = 0.269907

        delta growth = +0.014602

        RMS mismatch:
        0.332533
        versus 0.387250.

    h=0.5:
        gain 1.6 growth = 0.275850
        gain 0   growth = 0.261500

        delta growth = +0.014350

        RMS mismatch:
        0.353445
        versus 0.398660.

At v=0.05 the same qualitative pattern occurs.

Therefore the explicit landscape produces a layered result:

    timing capacity
        -> persistence boundary

    state-dependent movement feedback
        -> additional tracking-quality / growth improvement

within the timing-enabled region.

## 8. Relationship to the local closed-loop theorem

The local linear null says

    q_m + q_h

is one exact restoring budget.

The explicit landscape breaks that equivalence because:

- timing changes mismatch without requiring spatial movement;
- movement incurs route redistribution and migration cost;
- the movement-rate controller has a finite ceiling;
- the fixed phenological channel has its own cost and finite shift limit;
- selection acts through the spatial abundance distribution.

The result is not a contradiction of the local theorem.

Instead:

> exact local substitutability becomes state- and forcing-dependent
> complementarity once spatial mechanics and finite capacities are restored.

In this pilot, timing can move the system across the persistence boundary while
movement feedback then improves performance inside that persistent regime.

## 9. Relationship to Aikens 2022

The Aikens receipt shows context-dependent empirical evidence that phase
mismatch affects downstream movement/stopover behavior.

The current explicit controller is a synthetic mechanism that implements the
same causal direction:

    mismatch
    -> movement response
    -> changed subsequent mismatch.

It does not numerically calibrate the Aikens controller gain.

A numeric bridge still requires:

- confirmed route-distance units;
- a decision-interval forward distance;
- interval-level movement data for the movement kernel;
- independent fitness/demographic terms.

## 10. Claim boundary

This pilot supports:

> in the declared explicit moving landscape, mismatch-dependent movement
> feedback becomes valuable as forcing increases, while an independent timing
> response can substantially reduce the movement effort needed for successful
> tracking.

It does not establish:

- a natural controller-gain optimum;
- that movement feedback universally rescues high forcing;
- that h=0.25 or h=0.5 represent mule-deer timing responses;
- that Aikens controller slopes equal the synthetic gain k_m;
- that the persistence boundary is a natural climate threshold.

The sampled high-forcing result is especially asymmetric:

    movement feedback alone:
        improves tracking but does not restore persistence;

    timing response:
        permits persistence;

    movement feedback within the timing-enabled regime:
        further improves mismatch and low-density growth.
