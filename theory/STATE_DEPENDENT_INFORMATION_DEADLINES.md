# PAYOFF-B hidden-deadline extension

Date: **2026-09-29**  
Status: **exact extension of the information-deadline theorem**

## Motivation

The base theorem treats the opportunity cost of waiting, (D), as fixed.
Natural systems can violate that assumption: the fitness consequence of a
given delay can depend strongly on environmental conditions encountered later.

Greater snow goose provides a useful motivating boundary case. Grandmont et al.
(2023) experimentally delayed females during spring migration by holding them
in captivity for up to four days. Longer captivity reduced breeding output in
two of three years, and breeding suppression was strongest in 2009, when
breeding-ground snow conditions were unusually poor. Independently,
Reséndiz-Infante & Gauthier (2024) showed that temperatures encountered at the
southern St. Lawrence staging area were weak predictors of later Arctic and
Bylot conditions.

The key theoretical distinction is therefore:

[
\text{realised cost of waiting}
\neq
\text{cost expected when the wait/commit decision is made}.
]

## Proposition — unresolved state-dependent delay cost

Let the realised opportunity cost of waiting be (D(H)), where (H) is a
future deadline state. At the moment of commitment, the actor has information
set (\mathcal I) but does not necessarily know (H).

Define

[
\bar D(\mathcal I)
=
E[D(H)\mid\mathcal I].
]

Under additive expected loss and risk-neutral choice, the expected risk of
waiting is

[
R_{cue}(q)+\bar D(\mathcal I),
]

where (R_{cue}(q)) is the Bayes risk after the later seasonal cue.

Therefore the exact waiting rule remains

[
V(q)>\bar D(\mathcal I).
]

If (\bar D(\mathcal I)<R_0), the threshold is

[
\boxed{
q_{wait}(\mathcal I)
=
\frac{\max(A,L)+\bar D(\mathcal I)}{A+L}
}.
]

Thus the original theorem survives unchanged after replacing fixed (D) by
the **conditional expected delay cost available at commitment**.

## Corollary 1 — post-hoc harshness is not a threshold predictor

Suppose two years ultimately realise very different delay costs, but the actor
cannot distinguish those years at the commitment stage:

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

so the rational information-use threshold is identical in the two years.

Consequently, observing that delay was much more costly in a harsh year does
**not** justify assigning that year a higher (q_{wait}) after the fact.

For threshold movement, harshness must be at least partly predictable before
commitment.

## Corollary 2 — predictable deadline state moves the threshold

If an early signal (z) changes the expected cost of waiting,

[
E[D\mid z_2]>E[D\mid z_1],
]

then

[
q_{wait}(z_2)-q_{wait}(z_1)
=
\frac{
E[D\mid z_2]-E[D\mid z_1]
}{A+L},
]

provided both thresholds remain finite.

This is a new empirical target: a pre-commitment variable that predicts the
**cost of delay**, not merely the future seasonal state.

## Corollary 3 — Bayes-optimal decisions can look wrong ex post

Let (V(q)) be the value of waiting for the seasonal cue.

An actor may rationally wait because

[
V(q)>E[D\mid\mathcal I],
]

yet later encounter a realised state with

[
D(H)>V(q).
]

The decision was optimal given the information available at commitment but is
suboptimal conditional on the subsequently revealed state.

Likewise, an actor can rationally commit early even though a benign realised
state would have made waiting worthwhile.

This generates **ex-post reversal without irrationality**.

## Ecological interpretation

The information problem now has two hidden quantities:

1. **future ecological state** — what timing should ultimately be matched?
2. **future deadline state** — how costly will it be to wait long enough to
   learn more?

The second quantity matters especially when the consequences of delay are
amplified by breeding-ground conditions, body condition, competition or
resource scarcity.

Climate change can therefore affect seasonal coordination through two distinct
predictability channels:

[
\text{cue} \rightarrow \text{future ecological state}
]

and

[
\text{pre-commitment information}
\rightarrow
\text{future cost of delay}.
]

Loss of either predictability can prevent apparently adequate behavioural
capacity from being used optimally.

## Greater snow goose interpretation

The greater-snow-goose studies support only the following source-backed bridge:

- an experimentally imposed delay can carry a later reproductive cost;
- the strength of that carry-over effect depends on breeding-ground
  environmental conditions;
- southern migration-stage temperature is a weak predictor of later breeding
  conditions.

This combination is consistent with a **hidden deadline state**: the realised
cost of delaying migration can be strongly state-dependent while the state
that determines that cost is poorly known earlier along the route.

It does **not** yet show that geese change their information-use threshold in
response to expected deadline cost. That would require a pre-commitment
predictor of (D) plus observed cue-use switching in the same individuals.

## Consequence for the direct-test programme

The direct empirical target is now sharper.

A full test should measure both:

[
q^{state}
=
\text{predictability of the future ecological state},
]

and

[
q^{deadline}
=
\text{predictability of the future cost of delaying commitment}.
]

The original pairwise theorem concerns the first axis given (D). The
hidden-deadline extension shows when (D) itself must be treated as an
information-dependent quantity.

The strongest natural test would therefore estimate

[
q_{wait,i,t}
=
\frac{
\max(A,L)+E[D_{i,t}\mid\mathcal I_{i,t}]
}{
A+L
}
]

before the focal cue-use outcome is observed.
