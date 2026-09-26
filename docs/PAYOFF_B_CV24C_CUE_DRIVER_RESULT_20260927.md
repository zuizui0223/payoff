# PAYOFF-B long-term cue–driver result

Frozen: **2026-09-27**

## Registered outcome

The preregistered 1980–2010 pied-flycatcher cue–driver lane is
**NO_CUE_DRIVER_REVERSAL**.

The analysis used the published annual standardized selection gradients from
PLOS S1 Data and a fixed Ivory Coast NCEP/NCAR temperature cue: a 20-day mean
beginning 18 February over a fixed 3×3 coarse-grid proxy. Neither the cue window
nor the spatial proxy was selected from the selection outcome.

Predictive connectivity was estimated with the frozen eight-year trailing
window after separately detrending cue and driver within each window.

## What the connectivity series did

The single linear trend across the 25 estimable connectivity years was:

    slope = -0.01739 per year
    AICc  = -64.53.

The best unconstrained two-line fit had a breakpoint at **2001** and improved
AICc by 10.20:

    pre-break slope  = +0.00869
    post-break slope = +0.04944.

So the segmented description is better than one linear trend, but it is not
the registered decline→recovery geometry. The pre-break slope is positive, not
negative, and the declared recovery fraction is therefore undefined.

The history test was consequently **not opened**.

## Why this is not rescued as hysteresis

The raw rolling correlations are visibly nonstationary and include a large
change around 2001, negative correlations in the early 2000s, and a later rise
toward 2010. Those observations are real descriptive features of this chosen
cue/driver coordinate.

But the contract required:

1. a pre-break decline;
2. a post-break slope of the opposite sign;
3. at least 50% recovery of that decline.

Condition 1 failed. Calling the same series a decline–recovery event after
seeing the output would redefine the hypothesis.

Therefore:

> **The 31-year lane shows a strongly nonstationary cue–driver relationship,
> but it does not satisfy the preregistered cue-driver reversal needed to test
> natural path dependence.**

## Scientific consequence

This negative result is actually useful for the PAYOFF-B architecture.

Tomotani et al. (2021) already established cue–driver decoupling as a plausible
mechanism and direct prior art. PAYOFF-B does not need to manufacture a new
long-term reversal from the same system.

The central contribution remains downstream:

    changing cue quality
    × unequal decision deadlines
    -> asynchronous information uptake
    -> transient desynchronization
    -> topology-dependent historical memory.

The direct natural network-hysteresis prediction remains prospective.

## Provenance

- frozen successful workflow: `36270835505`
- source head: `02d11a6bf73777dac1de832cc45dc7f4235ac6ac`
- artifact: `10915252374`
- artifact SHA256:
  `655258a69978e71221e4f80b707a8915d289383ea0bfe036381e80edd0b379fb`
- PLOS S1 SHA256:
  `8c0b5bdb8265a11a41ab01caf98f4dd98cc2d1b677c6de58279b4fd32a1d2a45`

Later additions of an alternate NOAA transport route are reproducibility
infrastructure only and do not define this frozen scientific result.
