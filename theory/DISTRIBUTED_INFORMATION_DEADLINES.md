# PAYOFF-B distributed information deadlines

Date: **2026-09-29**  
Status: **exact population-level observation model; supporting bridge, not a new headline theorem**

## Why this extension is needed

The individual information-deadline theorem is deterministic:

\[
\text{wait}
\iff
D<V(q).
\]

Natural populations need not share a single delay cost \(D\). Body condition,
age, competitive status, reproductive state, route position and environmental
context can all generate individual heterogeneity in the cost of waiting.

That does not require a new decision rule. It only requires integrating the
existing rule over the distribution of \(D\).

## Proposition — the population uptake curve is the delay-cost CDF

Let \(D\ge0\) vary among individuals with distribution \(F_D\). Define

\[
A=(1-\pi)C_F,
\qquad
L=\pi C_M,
\qquad
S=A+L,
\]

and

\[
q_0=\frac{\max(A,L)}{S}.
\]

The exact information value is

\[
V(q)=
\max\left[
0,\,
Sq-\max(A,L)
\right].
\]

Therefore the population fraction using the later cue is

\[
\boxed{
G(q)
=
P(\text{wait}\mid q)
=
P[D<V(q)].
}
\]

For a continuous delay-cost distribution,

\[
G(q)=F_D(V(q)).
\]

Above the actionable-information boundary,

\[
q>q_0,
\]

we have

\[
V(q)=S(q-q_0),
\]

so

\[
\boxed{
G(q)=F_D\!\left(S(q-q_0)\right).
}
\]

Thus a smooth empirical cue-uptake curve can arise even though every individual
uses an exact deterministic threshold. The smoothness reflects heterogeneity in
deadlines, not necessarily stochastic decision-making.

## Individual thresholds are an affine transform of delay cost

For every actor with \(D<R_0\),

\[
q_{\mathrm{wait}}
=
q_0+\frac{D}{S}.
\]

Hence

\[
\boxed{
D
=
S(q_{\mathrm{wait}}-q_0).
}
\]

The distribution of finite information-use thresholds is therefore an affine
transformation of the distribution of delay costs.

This gives a direct empirical interpretation to a fitted threshold
distribution. If \(A,L\) are independently identified, observed
\(q_{\mathrm{wait}}\) values can be converted to the corresponding \(D\)
scale. If the state-loss scale is not identified, the threshold distribution
still identifies the normalized delay coordinate \(D/S\).

## Hard deadlines create incomplete uptake even at perfect information

At \(q=1\),

\[
V(1)=R_0.
\]

Therefore

\[
\boxed{
G(1)=P(D<R_0).
}
\]

Any mass with

\[
D\ge R_0
\]

never waits, even under perfect cue accuracy. Population cue use can therefore
saturate below one without implying that some individuals failed to perceive
the cue.

This is a distinct empirical prediction from a simple noisy-response model.

## Pairwise asynchronous uptake

Let

\[
G_1(q)=P(I_1=1),
\qquad
G_2(q)=P(I_2=1),
\]

where \(I_i=1\) denotes cue use.

For two conditionally independent actors drawn from the two deadline
distributions,

\[
\boxed{
P(I_1\ne I_2)
=
G_1(1-G_2)
+
(1-G_1)G_2.
}
\]

Equivalently,

\[
P(I_1\ne I_2)
=
G_1+G_2-2G_1G_2.
\]

If the two actors have the same uptake curve \(G(q)\),

\[
P(I_1\ne I_2)
=
2G(q)[1-G(q)],
\]

which reaches its maximum at

\[
G(q)=\frac12.
\]

This is the population-level counterpart of the network-cut result: exposure to
asynchronous information use is greatest around the middle of the uptake
transition.

## Correlated deadlines

Deadline costs can be correlated because interacting actors share weather,
resource conditions or demographic context.

Let

\[
G_{12}(q)
=
P(I_1=1,I_2=1).
\]

Then without assuming independence,

\[
\boxed{
P(I_1\ne I_2)
=
G_1(q)+G_2(q)-2G_{12}(q).
}
\]

Positive correlation in cue uptake generally reduces asynchronous exposure
relative to the independent case because both actors tend to switch together.

## Empirical role

This result supplies the missing observation model between the exact individual
theorem and biological data.

It licenses a hierarchy:

\[
\text{individual }D_i
\rightarrow
q_{\mathrm{wait},i}
\rightarrow
\text{population uptake curve }G(q)
\rightarrow
\text{pairwise asynchronous-use probability}.
\]

A hierarchical or smooth empirical uptake curve should therefore not be treated
as a relaxation of the theory. Under heterogeneous deadlines, such a curve is
what the exact threshold theory predicts.

## Claim boundary

This extension is algebraic and should remain supporting material rather than a
new headline theorem.

It does **not** identify \(D\) from phenology alone. Conversion from observed
thresholds to absolute delay costs requires the state-loss scale \(A+L\) and
the actionable threshold \(q_0\), or independent equivalents.

Likewise, a logistic-looking uptake curve does not by itself demonstrate a
logistic delay-cost distribution or conscious assessment of cue reliability.
