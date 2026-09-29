# PAYOFF-B direct empirical test of the information-deadline theorem

Date: **2026-09-29**  
Status: **v2 prospective measurement contract; no current natural dataset qualifies as a direct test**  
Contract: `data/payoff_b_effective_deadline_threshold_contract_v2_20260929.json`  
Provenance: v1 raw-`D` contract retained unchanged as the pre-compensation specification.

## What is already verified

The theoretical implication is already exact for the declared binary-cue model:

[
q_i = \frac{\max(A,L)+D_{eff,i}}{A+L}
]

whenever (D_{eff,i}<R_0). Therefore, for two otherwise identical actors,

[
D_{eff,1}<D_{eff,2}
\Rightarrow
q_1<q_2
]

and, when both eventually use the cue,

[
\Delta q=q_2-q_1
=\frac{D_{eff,2}-D_{eff,1}}{A+L}.
]

The repository already checks this identity against the implemented decision
rule and the canonical numerical witness. This is **not** an unverified
theoretical arrow.

The open question is natural instantiation:

> Do measured differences in the opportunity cost of waiting predict measured
> differences in the cue reliability at which interacting organisms begin to
> use information?

## What counts as a direct empirical test

A qualifying dataset must measure, independently of the focal cue-use outcome:

1. **Cue reliability (q)** before commitment: the probability that the cue
   correctly classifies the later state relevant to fitness.
2. **Effective delay/opportunity cost (D_eff,i)**: the total fitness-equivalent cost of postponing commitment, including any nonrecoverable direct waiting cost plus optimally compensated downstream timing cost. It may be estimated as a total causal effect or decomposed into direct cost, raw delay, compensation and residual timing loss.
3. **State-mismatch losses (C_F,C_M)** and the prior state probability
   (pi), sufficient to construct
   (A=(1-pi)C_F) and (L=pi C_M).
4. **Cue use**: an observed choice or behavioural response that distinguishes
   committing before the cue from waiting for/conditioning on the cue.

Migration distance, raw waiting days, departure date, source--target distance, temperature sensitivity, phase correction and predictive connectivity are informative auxiliary quantities, but none is (D_eff) or cue-use status by definition.

## Hidden-deadline rule

If the realised cost of waiting depends on a future environmental state, the
quantity entering the theorem is **not the cost reconstructed after that state
is revealed**.

At commitment, the relevant quantity is

[
\bar D_{eff,i}(\mathcal I_i)
=
E[D_{eff,i}(H)\mid\mathcal I_i],
]

where (\mathcal I_i) is the information actually available when the actor must
decide whether to commit or wait.

Under additive expected loss, the exact threshold becomes

[
q_{i,pred}
=
\frac{
\max(A,L)+E[D_{eff,i}(H)\mid\mathcal I_i]
}{
A+L
}.
]

Therefore:

- a harsh future year may produce a large realised delay cost without changing
  the rational threshold if that harshness was not predictable at commitment;
- a threshold may vary across individuals or years only when pre-commitment
  information changes their conditional expected effective waiting cost;
- post-hoc breeding-ground conditions must not be substituted for
  (E[D_{eff}\mid\mathcal I]) in the threshold equation.

This rule is implementation-tested in
`src/state_dependent_information_deadline.py`.

## Direct-plus-compensated deadline rule

If waiting creates raw delay (\delta), let (J(\delta)) be a direct
nonrecoverable waiting cost. The actor may then recover (c) time units at
compensation cost (K(c)), while residual delay carries fitness loss
(M(\delta-c)). The theorem input is

[
D_{eff}
=
J(\delta)
+
\min_{0\le c\le\min(C,\delta)}
[K(c)+M(\delta-c)].
]

The earlier compensation-only formula is the exact special case
(J(\delta)=0). Raw delay is therefore not itself the empirical theorem cost,
and even complete timing recovery does not imply (D_{eff}=0) if direct waiting
cost remains.

With state-dependent conditions, the commitment-time object is the appropriate
expectation of this total effective cost.

This reduction is implementation-tested in
`src/compensated_information_deadline.py`.

## Focal-cue exogeneity gate

The fixed effective-cost threshold

[
q_{wait}
=
\frac{\max(A,L)+D_{eff}}{A+L}
]

assumes that the focal cue changes the seasonal action but **does not itself
change the effective cost of waiting**.

Before using that closed form, ask whether the same cue also changes the
downstream compensation policy or expected compensation loss conditional on
waiting.

If not, fixed (D_{eff}) is licensed.

If yes, then

[
D_{eff}=D_{eff}(q)
]

and the correct threshold solves

[
V_A(q)=D_{eff}(q).
]

In the additive binary dual-use special case,

[
D_{eff}(q)=J+R_C(q)
]

and

[
\boxed{
\text{wait}
\iff
V_A(q)+V_C(q)>J+R_{C0}.
}
]

This case is implementation-tested in
`src/dual_use_information_value.py`.

Two consequences follow.

1. The simple pairwise identity
   (
   \Delta q=|D_{eff,2}-D_{eff,1}|/(A+L)
   )
   is licensed only when the relevant actor-specific effective costs are fixed
   with respect to the focal cue.
2. The inverse identity
   (
   D^{eff}_{revealed}=q_{wait}(A+L)-\max(A,L)
   )
   still recovers the **effective cost at the observed threshold**, but it must
   not be interpreted as a cue-independent actor trait when the cue itself
   changes compensation.

## Two valid empirical routes to D_eff

### Route A — total causal effect

Let (Y(0)) be expected fitness under immediate commitment and
(Y(\delta,adapt)) expected fitness when waiting is imposed but ordinary
downstream compensation is allowed. A biologically faithful waiting
intervention identifies

[
D^{causal}_{eff}(\delta)
=
E[Y(0)]-E[Y(\delta,adapt)].
]

This route estimates the total cost directly and does not require separate
identification of (J), (K) and (M).

### Route B — mechanistic decomposition

Alternatively, independently estimate:

1. direct waiting cost (J(\delta));
2. compensatory capacity (C);
3. compensation cost (K(c));
4. residual timing-loss function (M(\delta-c)).

Then reconstruct the optimized total.

Both routes require treatment fidelity. A manipulation that adds
treatment-specific handling, confinement or other stress estimates the cost of
that manipulation, not automatically the natural cost of waiting for
information.

## Primary falsifiable predictions

### P1. Actor-level threshold

For actor (i), with fixed or commitment-time expected effective delay cost,

[
q_{i,pred}
=
\frac{\max(A,L)+D_{eff,i}}{A+L}.
]

With the implemented tie rule, cue use occurs only for

[
q>q_{i,pred}.
]

Observed use/non-use decisions therefore bracket an empirical switch interval.
A direct test asks whether the independently predicted (q_{i,pred}) lies
inside that interval.

### P2. Deadline ordering

For actors sharing the same state-loss structure,

[
D_{eff,1}<D_{eff,2}
\Rightarrow
q_1<q_2.
]

For state-dependent deadlines, use the conditional expectation of each actor's optimized effective cost available at commitment.

### P3. Window width

When both actors eventually use the cue,

[
q_2-q_1
=
\frac{D_{eff,2}-D_{eff,1}}{A+L}.
]

With hidden deadline states this becomes

[
q_2-q_1
=
\frac{
E[D_{eff,2}\mid\mathcal I_2]-E[D_{eff,1}\mid\mathcal I_1]
}{
A+L
}.
]

The strongest test therefore compares an independently estimated
commitment-time deadline gap with the observed width of the asynchronous
cue-use region.

### P4. Behaviour inside and outside the window

For a shared cue:

- (q\le q_1): both commit before the cue;
- (q_1<q\le q_2): exactly one actor uses the cue;
- (q>q_2): both use the cue.

A direct natural or experimental test must observe the middle regime itself.
Showing only different phenological slopes is insufficient.

### P5. Ex-post reversal without irrationality

If the actor waits because

[
V(q)>E[D_{eff}\mid\mathcal I],
]

but a subsequently revealed harsh state has

[
D_{eff}(H)>V(q),
]

then waiting is worse **ex post** even though it was optimal **ex ante**.

Natural data should therefore distinguish an information failure from an
apparently maladaptive outcome that arose because the cost state itself was
unpredictable.

## Inverse test — reveal D from an observed threshold

The theorem is invertible. For an interior information-use threshold,

[
\boxed{
D^{eff}_{revealed}
=
q_{wait}(A+L)-\max(A,L)
}
]

so an observed switch interval for (q_{wait}) maps directly to an interval for
the deadline cost implied by the model.

For the canonical example, an observed threshold bracket

[
0.81\le q_{wait}<0.82
]

implies

[
0.096\le D^{eff}_{revealed}<0.112,
]

which contains the generating effective cost (D_eff=0.10).

This creates a stronger empirical design than testing threshold ordering alone:
estimate (q_{wait}) from behavior, infer (D^{eff}_{revealed}) from the theorem,
then compare it with an **independent** estimate of the effective fitness cost of postponing commitment after feasible compensation. Agreement is a quantitative out-of-sample test
of the deadline mechanism. Using the same behavior to estimate both quantities would be circular, and comparing this inferred fitness cost directly with raw days delayed is also not licensed.

## Minimum experimental design

The cleanest design manipulates cue reliability and delay cost orthogonally.

For each actor or actor class:

- estimate (D_eff,i), or its commitment-time expectation when state-dependent, either from a biologically faithful total-effect waiting intervention or from a preregistered decomposition of direct waiting cost, raw delay, downstream compensation and residual timing loss;
- record exactly which predictors of future delay cost were available before
  the wait/commit decision;
- expose decisions to at least five cue-reliability levels spanning below,
  between and above the predicted thresholds;
- replicate each level enough to estimate stochastic departures from the
  deterministic rule;
- record the commitment/use decision before revealing the later ecological
  state;
- estimate (C_F,C_M,pi) without using the focal threshold outcome.

The deterministic theorem is the preregistered core. A hierarchical logistic
soft-threshold model may be added for biological noise, but it must not replace
the exact directional and window-width predictions after outcomes are seen.

## Current PAYOFF-B datasets: why none is direct

### Broad migratory birds

The Amaral-derived lane estimates pre-outcome source--destination predictive
connectivity and realized arrival--green-up mismatch. It supplies a natural
information-quality coordinate, but it does not independently measure (D_eff,i)
or binary cue uptake.

### Eurasian wigeon

The wigeon lane supplies route-level predictive connectivity and phase
correction across 224 transitions. The registered connectivity x phase-error
interaction was not supported. Phase correction is not equivalent to the
decision to wait for/use a cue, and route progress or migration distance must
not be relabelled as (D).

### Pied flycatcher manipulation

The manipulation shows that heterospecific seasonal information can be
unavailable to an earlier decision and relevant to a later one. It anchors
decision-time information availability, but it does not sweep cue reliability
or estimate a pair of information-use thresholds.

### Greater snow goose

The same ecological lineage now supplies q-like route predictability,
perturbation-cost evidence, two-sided timing-fitness loss and downstream
buffering evidence. Historical tracking shows that some raw timing delay can be
compressed during migration and after arrival. Captivity experiments show a
different feature: reproductive or breeding costs can remain even when detected
breeders show little corresponding shift in arrival or laying date.

This combination motivates both the recoverable timing component and a possible
direct nonrecoverable (J) component, but does not identify natural (D_eff).
Captivity duration mixes elapsed time with handling/confinement stress, so it is
not a biologically faithful information-waiting intervention. The exact theorem
therefore requires either an independent total causal waiting effect or a
pre-commitment estimate of the decomposed effective
(E[D_eff\mid\mathcal I]).

## Fail-closed promotion rule

PAYOFF-B may claim a **direct natural information-deadline test** only if a
single qualifying system supplies the four measured quantities above and the
analysis was specified before the focal cue-use outcomes were examined.

Until then the correct hierarchy is:

[
\text{exact theorem}
\;>\;
\text{natural evidence for separate links}
\;>\;
\text{prospective direct mechanism test}.
]

The pairwise arrow

[
D_{eff,2}-D_{eff,1}
\rightarrow
q_2-q_1
\rightarrow
q_1<q\le q_2
\rightarrow
\text{asynchronous cue use}
]

is therefore **theoretically verified but not yet directly instantiated in a
natural system**.
