# PAYOFF-B state-dependent information-deadline extension

Date: **2026-09-29**  
Status: **exact extension of the declared binary-cue model**

## Motivation

The original information-deadline theorem treats the opportunity cost of
waiting, (D), as fixed. Ecologically, the realised cost of losing time can
depend on environmental state, demographic context, body condition or later
breeding conditions.

The crucial distinction is:

[
\text{realised cost of waiting}
\neq
\text{cost expected when the wait/commit decision is made}.
]

Greater snow goose is a useful motivating boundary case. Experimental
perturbation duration during spring migration had context-dependent later
reproductive consequences, while southern-route temperatures were weak
predictors of later Arctic and Bylot conditions. The manipulation mixes elapsed
time with captivity/handling stress and therefore does **not** identify natural
PAYOFF-B (D); it motivates the extension only.

## Proposition — hidden state-dependent waiting cost

Let the realised waiting cost be (D(H)), where (H) is a future deadline
state. At commitment the actor has information set (mathcal I), but need not
know (H).

Define

[
\bar D(\mathcal I)
=
E[D(H)\mid\mathcal I].
]

Under the same additive, risk-neutral expected-loss criterion as the original
theorem, expected risk after waiting is

[
R_{cue}(q)+\bar D(\mathcal I).
]

Therefore the exact waiting rule remains

[
V(q)>\bar D(\mathcal I).
]

When (ar D(mathcal I)<R_0),

[
oxed{
q_{wait}(mathcal I)
=
\frac{\max(A,L)+\bar D(\mathcal I)}{A+L}
}.
]

When (ar D(mathcal I)ge R_0), the actor never waits even under perfect
information.

The original fixed-cost theorem is recovered when (D(H)=D) for all states.

## Binary deadline-state special case

If the same early/normal state used by the seasonal model also determines the
waiting cost,

[
D_N
quad\text{and}quad
D_E,
]

then before observing the future state,

[
\bar D
=
(1-\pi)D_N+\pi D_E.
]

This is a special case of (E[D(H)midmathcal I]), not a different theorem.

## Two interacting actors

For actors (i=1,2), define their commitment-time expected waiting costs

[
\bar D_i
=
E[D_i(H)\mid\mathcal I_i].
]

If both eventually wait, the exact asynchronous-information window has width

[
oxed{
\Delta q
=
\frac{|\bar D_2-\bar D_1|}{A+L}.
}
]

A common shift in expected deadline cost moves both thresholds together but
does not change (Delta q). A differential shift changes the window itself.

Thus environmental deterioration can widen information-induced
desynchronization without changing cue reliability when it raises the expected
cost of waiting more strongly for one interaction partner than another.

## Corollary 1 — post-hoc harshness is not a threshold predictor

Suppose two years realise different waiting costs but are indistinguishable at
commitment:

[
P(H\mid\mathcal I_{t=1})
=
P(H\mid\mathcal I_{t=2}).
]

Then

[
\bar D(\mathcal I_{t=1})
=
\bar D(\mathcal I_{t=2}),
]

so their rational information-use thresholds are identical.

Observing after the fact that delay was especially costly in a harsh year does
**not** justify assigning that year a higher (q_{wait}). Threshold movement
requires at least partial pre-commitment predictability of the deadline state.

## Corollary 2 — predictable deadline state moves the threshold

If an early signal (z) changes expected waiting cost,

[
E[D\mid z_2]>E[D\mid z_1],
]

then, while both thresholds remain finite,

[
q_{wait}(z_2)-q_{wait}(z_1)
=
\frac{
E[D\mid z_2]-E[D\mid z_1]
}{A+L}.
]

This creates a second empirical information target: a pre-commitment variable
that predicts the **cost of delay**, rather than only the future ecological
state to be matched.

## Corollary 3 — ex-post reversal without irrationality

An actor can rationally wait because

[
V(q)>E[D\mid\mathcal I],
]

yet later encounter a state with

[
D(H)>V(q).
]

Waiting is then worse conditional on the revealed state even though it was
Bayes-optimal at commitment. The reverse can occur for a rational early
commitment followed by a benign realised deadline state.

Thus an apparently maladaptive outcome can be an **ex-post reversal**, not
evidence that the actor ignored available information.

## Ecological interpretation

The information problem can contain two hidden future quantities:

1. **future ecological state** — what timing should ultimately be matched?
2. **future deadline state** — how costly will it be to wait long enough to
   obtain better information?

Climate change can alter coordination through either predictability channel:

[
\text{current cue}
\rightarrow
\text{future ecological state}
]

and

[
\text{pre-commitment information}
\rightarrow
\text{future cost of delay}.
]

The original information-deadline theorem concerns the first axis conditional
on (D). This extension shows when (D) itself becomes an
information-dependent quantity.

## Greater snow goose interpretation

The current source-backed bridge establishes only that:

- an experimental spring-migration perturbation can carry later reproductive
  consequences;
- the strength of those consequences differs among environmental contexts;
- southern migration-stage temperature is a weak predictor of later breeding
  conditions.

This is consistent with a hidden deadline state: the realised consequence of
delaying migration can be state-dependent while the state governing that
consequence is poorly known earlier along the route.

It does **not** demonstrate that geese adjust an information-use threshold in
response to expected deadline cost. A direct test requires an independently
estimated (E[D\midmathcal I]) and observed cue-use switching in the same
decision system.

## Direct empirical target

The strongest natural test would estimate before the focal behavioural outcome:

[
q_{wait,i,t}
=
\frac{
\max(A,L)+E[D_{i,t}\mid\mathcal I_{i,t}]
}{
A+L
}.
]

It may also distinguish:

[
q^{state}
=
\text{predictability of the future ecological state}
]

from

[
q^{deadline}
=
\text{predictability of the future cost of delaying commitment}.
]

## Claim boundary

This extension assumes:

- additive waiting costs;
- risk-neutral expected loss;
- the waiting decision precedes observation of the later cue;
- the declared binary state and symmetric-cue model.

Variance in waiting cost has no independent effect once its conditional
expectation is fixed under this linear criterion. Risk sensitivity or nonlinear
fitness requires a different model.

No current PAYOFF-B natural dataset directly identifies
(E[D_i(H)\mid\mathcal I_i]) together with the predicted actor-specific
cue-use switch. The result is therefore an exact theoretical extension with
empirical motivation, not a natural confirmation.
