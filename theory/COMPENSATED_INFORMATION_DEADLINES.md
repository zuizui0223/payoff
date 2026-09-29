# PAYOFF-B compensated information deadlines

Date: **2026-09-29**  
Status: **exact reduction plus linear closed form**

## Motivation

The information-deadline theorem uses a fitness-equivalent cost \(D\) for
waiting until a later cue becomes available. Raw elapsed time is generally not
that cost.

Waiting can create two qualitatively different losses:

1. **direct waiting cost** \(J(\delta)\): costs incurred while waiting that
   cannot be undone by later timing compensation, such as physiological stress,
   lost territorial opportunity or energetic depletion;
2. **downstream timing cost**: the actor may recover some of the raw delay by
   migrating faster, compressing stopovers or shortening a later pre-breeding
   interval, but this compensation can itself be costly.

The theorem therefore requires the total fitness loss remaining after optimal
compensation, not days delayed.

Greater snow goose illustrates both pieces. Historical tracking shows that later
departure can coincide with shorter migration duration, so departure delay and
arrival delay are not interchangeable. Separately, captivity experiments show
that longer perturbation can reduce later breeding propensity even when detected
breeders do not show a corresponding delay in arrival or laying date. This
combination is exactly why raw delay cannot be equated with \(D\).

## Proposition — effective deadline cost

Let waiting for information create raw temporal delay

\[
\delta \ge 0.
\]

Let \(J(\delta)\ge0\) be a direct, non-recoverable cost of waiting. After
waiting, the actor can compensate by \(c\) time units, with

\[
0\le c\le \min(C,\delta),
\]

where \(C\) is compensatory capacity. Let \(K(c)\) be the cost of compensation
and \(M(\delta-c)\) the fitness loss from residual timing delay.

Define

\[
\boxed{
D_{\mathrm{eff}}(\delta,C)
=
J(\delta)
+
\min_{0\le c\le\min(C,\delta)}
\left[
K(c)+M(\delta-c)
\right].
}
\]

Under additive expected loss, the information-deadline theorem applies
unchanged after

\[
D\longrightarrow D_{\mathrm{eff}}.
\]

Thus, whenever \(D_{\mathrm{eff}}<R_0\),

\[
\boxed{
q_{\mathrm{wait}}
=
\frac{\max(A,L)+D_{\mathrm{eff}}}{A+L}.
}
\]

The earlier compensation-only expression is the exact special case
\(J(\delta)=0\).

## Immediate consequences

Because zero compensation is feasible,

\[
D_{\mathrm{eff}}
\le
J(\delta)+M(\delta).
\]

Increasing the feasible compensation set cannot increase
\(D_{\mathrm{eff}}\). Therefore, holding direct waiting cost fixed, greater
downstream compensatory capacity weakly lowers the information-use threshold.

For two actors with finite thresholds,

\[
\Delta q
=
\frac{
|D_{\mathrm{eff},2}-D_{\mathrm{eff},1}|
}{
A+L
}.
\]

Actors can therefore use the same cue asynchronously even when their raw
waiting time is identical. Differences in direct waiting cost, compensatory
capacity, compensation cost or residual timing-loss sensitivity can each create
threshold heterogeneity.

The reverse warning is equally important: rankings in raw delay need not equal
rankings in effective deadline cost.

### Raw-delay rank is not threshold rank

For finite thresholds and a shared state-loss scale,

[
q_{wait,i}<q_{wait,j}
\iff
D_{eff,i}<D_{eff,j}.
]

No corresponding equivalence exists for raw delays \(\delta_i\) unless the
compensation and direct-cost structures are sufficiently homogeneous.

Two consequences follow.

**Rank erasure.** Actor 1 can wait 0.20 time units with no compensation while
actor 2 waits 0.40 but recovers 0.20 for free. Both then have
\(D_{eff}=0.20\) and the same cue-use threshold.

**Rank reversal.** Under the canonical loss scale, an actor with raw delay 0.20
and no compensation has \(D_{eff}=0.20\) and \(q_{wait}=0.875\). A second
actor with raw delay 0.40, full free timing compensation and direct waiting
cost rate \(\omega=0.05\) has only \(D_{eff}=0.02\), hence
\(q_{wait}=0.7625\). The actor that waits twice as long rationally uses
information at *lower* cue reliability.

Thus migration distance, travel duration or calendar delay can fail even as
ordinal proxies for an information deadline when compensatory capacity differs
among actors. A raw-delay gradient is interpretable as a deadline gradient only
under an additional homogeneity assumption about \(J,K,M\) and \(C\).


## Linear closed form

Let

\[
J(\delta)=\omega\delta,\qquad
K(c)=\kappa c,\qquad
M(r)=\mu r,
\]

with all marginal costs non-negative.

Then

\[
D_{\mathrm{eff}}
=
\omega\delta
+
\min_c
\left[
\kappa c+\mu(\delta-c)
\right].
\]

If \(\kappa\ge\mu\), compensation is not worthwhile:

\[
c^*=0,
\qquad
D_{\mathrm{eff}}=(\omega+\mu)\delta.
\]

If \(\kappa<\mu\),

\[
c^*=\min(C,\delta),
\]

and

\[
\boxed{
D_{\mathrm{eff}}
=
\omega\delta
+
\kappa\min(C,\delta)
+
\mu\max(\delta-C,0).
}
\]

With \(S=A+L\), the cue threshold has a capacity kink:

\[
\frac{\partial q_{\mathrm{wait}}}{\partial\delta}
=
\begin{cases}
(\omega+\kappa)/S, & \delta<C,\\
(\omega+\mu)/S, & \delta>C,
\end{cases}
\qquad
(\kappa<\mu).
\]

Direct waiting cost \(\omega\) raises both slopes. Compensation can remove the
timing component of waiting cost, but it cannot remove \(J\).

## Numerical witnesses

Use the canonical PAYOFF-B loss scale

\[
\pi=0.4,\quad C_F=2,\quad C_M=1,
\quad A+L=1.6,
\quad \max(A,L)=1.2.
\]

### Compensation-only special case

Let raw delay be \(\delta=0.30\), with \(J=0\). With no compensatory capacity,

\[
D_{\mathrm{eff}}=0.30,
\qquad
q_{\mathrm{wait}}=0.9375.
\]

With \(C=0.20,\ \kappa=0.20,\ \mu=1\),

\[
c^*=0.20,\qquad
D_{\mathrm{eff}}=0.14,
\qquad
q_{\mathrm{wait}}=0.8375.
\]

Thus two actors with the same raw delay but different downstream capacity can
have different information-use thresholds.

### Full timing recovery with non-zero direct cost

Let \(C=0.30,\ \kappa=0,\ \mu=1\), so the entire timing delay can be recovered
for free, but let \(\omega=0.40\). Then

\[
c^*=0.30,\qquad
\delta-c^*=0,
\]

yet

\[
D_{\mathrm{eff}}
=
0.40(0.30)
=
0.12.
\]

Therefore

\[
q_{\mathrm{wait}}
=
\frac{1.2+0.12}{1.6}
=
0.825,
\]

which remains above the cue-actionability boundary \(q_0=0.75\). Perfect
timing compensation does not erase a direct cost of waiting.

## Hidden deadline states and information about compensation

Suppose the direct cost, compensation cost or residual timing-loss surface
depends on a future state \(H\).

If compensation can be selected after \(H\) is known, define

\[
D_{\mathrm{eff}}(H)
=
J(\delta,H)
+
\min_c
\left[
K(c,H)+M(\delta-c,H)
\right],
\]

and the wait/commit decision made earlier uses

\[
E[D_{\mathrm{eff}}(H)\mid\mathcal I].
\]

If one compensation plan must instead be chosen before \(H\) is known, the
relevant expected cost is

\[
E[J(\delta,H)\mid\mathcal I]
+
\min_c
E[
K(c,H)+M(\delta-c,H)
\mid\mathcal I
].
\]

Because

\[
E[\min_c L(c,H)\mid\mathcal I]
\le
\min_c E[L(c,H)\mid\mathcal I],
\]

later information that permits state-contingent compensation can lower the
effective deadline cost. Information can therefore have value twice: first for
choosing the seasonal action, and again for choosing how to compensate for
having waited.

## Ecological interpretation

A direct estimate of \(D_{\mathrm{eff}}\) should separate four components:

1. raw delay \(\delta\) created by waiting for information;
2. direct waiting cost \(J(\delta)\) that cannot be recovered later;
3. downstream compensation \(c\) and its fitness/energetic cost \(K(c)\);
4. residual timing loss \(M(\delta-c)\).

In a multi-stage life cycle, downstream compensation can itself occur in
several steps. For migration, one might distinguish migration-speed/stopover
compensation from post-arrival pre-breeding buffering. Observed correlations
between sequential dates cannot simply be multiplied into a causal
\(D_{\mathrm{eff}}\); the stagewise mapping must be specified independently.

## Empirical identification: direct and decomposed routes

The decomposition above is not the only way to estimate \(D_{\mathrm{eff}}\).

Let \(Y(0)\) denote expected fitness when commitment is not postponed, and let
\(Y(\delta,\mathrm{adapt})\) denote expected fitness when the actor is forced to
wait by \(\delta\) but is then allowed to use its ordinary downstream
compensatory responses. On a common additive fitness-loss scale, a randomized
naturalistic waiting intervention identifies

\[
\boxed{
D_{\mathrm{eff}}^{\mathrm{causal}}(\delta)
=
E[Y(0)]-
E[Y(\delta,\mathrm{adapt})].
}
\]

This total causal effect already includes direct waiting cost, compensation
cost and residual timing loss. The \(J+K+M\) decomposition is needed only when
the goal is to explain *why* the total effective cost has its observed value.

Two empirical routes are therefore valid:

1. **total-effect route** — randomize a biologically faithful waiting period,
   allow downstream compensation, and measure final expected fitness;
2. **mechanistic route** — independently estimate \(J\), \(K\), compensation
   capacity and \(M\), then reconstruct the optimized total.

Both routes require the waiting treatment to represent the ecological act of
waiting for information. A manipulation that adds treatment-specific stress or
constraint identifies the effective cost of that manipulation, not
automatically the natural information-waiting cost.

## Greater snow goose boundary

Three source-backed findings motivate the decomposition without identifying its
parameters:

- Bêty, Giroux & Gauthier (2004) found that later departure was associated
  with shorter migration duration, while departure and arrival timing were only
  weakly coupled;
- Bêty, Gauthier & Giroux (2003) found that later arrival was associated with a
  shorter pre-laying interval and a less-than-one-for-one shift in laying date;
- Legagneux et al. (2012) and Grandmont et al. (2023) found carry-over costs of
  captivity duration, while Grandmont et al. reported no detectable captivity
  effect on arrival date or laying date among females detected on the breeding
  grounds.

The first two are buffering anchors; the last shows that a direct waiting cost
can remain even when downstream timing delay is small or compensated. None of
these studies alone identifies \(J,K,M\), or numerical \(D_{\mathrm{eff}}\) on
the theorem's common utility scale.

In the downstream coordination game, player-specific \(D_i\) should likewise
be interpreted as \(D_{\mathrm{eff},i}\) whenever compensation or direct
waiting costs are relevant.

## Claim boundary

The reduction is exact under the declared additive model. Natural observations
currently support the existence of its components, not their joint causal
identification.

The direct natural target is

\[
\boxed{
D_{\mathrm{eff},i}
\rightarrow
q_{\mathrm{wait},i}
\rightarrow
\text{asynchronous cue use}.
}
\]

Raw waiting duration alone is not the theorem's empirical predictor.
