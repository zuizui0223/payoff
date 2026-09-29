# PAYOFF-B state-dependent information-deadline extension

Date: **2026-09-29**  
Status: **exact extension of the declared binary-cue model**

## Motivation

The original information-deadline theorem assumes a fixed opportunity cost of
waiting, (D). Ecologically, that need not be constant. The cost of losing one
day can differ among years, environmental states or demographic contexts.

The greater-snow-goose perturbation literature motivates this possibility:
effects of the same 0-4 day spring manipulation differed strongly among years,
with particularly strong reproductive suppression under poor breeding-ground
conditions. That experiment mixes elapsed time and captivity stress, so it does
**not** identify natural (D). Its role here is motivation only.

## Hidden state-dependent waiting cost

Let the future seasonal state be normal or early, with

[
P(E)=\pi.
]

Suppose waiting incurs

[
D_N
]

in the normal state and

[
D_E
]

in the early state.

The actor decides whether to wait **before** observing the later cue. Under the
same risk-neutral expected-loss criterion as the original theorem, its expected
waiting cost is therefore

[
\bar D
=
(1-\pi)D_N+\pi D_E.
]

The information value (V(q)) is unchanged. Hence the exact decision rule is

[
V(q)>\bar D.
]

When (ar D<R_0),

[
\boxed{
q_{wait}
=
\frac{\max(A,L)+\bar D}{A+L}
}
]

and when (ar D\ge R_0), the actor never waits even under perfect
information.

The fixed-cost theorem is recovered exactly when

[
D_N=D_E=D.
]

## Ecological interpretation

The actor can be uncertain about two things at once:

1. **which future seasonal state will occur**;
2. **how costly it will prove to have delayed commitment in that state**.

Under expected payoff, only the expected waiting cost enters the threshold, but
that expectation can still move the information-use boundary.

Thus climate change can alter information use not only by changing cue quality
(q), but also by changing the cost surface against which information is
valued.

## Two interacting actors

For actors (i=1,2), define

[
\bar D_i
=
(1-\pi)D_{i,N}+\pi D_{i,E}.
]

If both eventually wait, their asynchronous-information window has exact width

[
\boxed{
\Delta q
=
\frac{|\bar D_2-\bar D_1|}{A+L}.
}
]

This gives two distinct effects of environmental context.

### Common shift

If the context adds the same amount to both actors' expected waiting costs,
both thresholds shift together but (Delta q) is unchanged.

### Differential shift

If the context changes one actor's cost more strongly than the other's,

[
|\bar D_2-\bar D_1|
]

changes and the asynchronous window itself widens or narrows.

That generates a new comparative prediction:

> Environmental deterioration can increase phenological desynchronization even
> without changing cue reliability if it increases deadline costs
> asymmetrically across interacting actors.

## Claim boundary

This result assumes:

- additive waiting costs;
- risk-neutral expected loss;
- the waiting decision precedes observation of the later cue;
- the binary state and symmetric cue model used by the original theorem.

Variance in waiting cost has no independent effect under linear expected loss
once its expectation is fixed. Risk sensitivity or nonlinear fitness would
require a different model.

No current PAYOFF-B natural dataset directly estimates (D_N,D_E). The result
is therefore an exact theoretical extension with empirical motivation, not a
natural confirmation.
