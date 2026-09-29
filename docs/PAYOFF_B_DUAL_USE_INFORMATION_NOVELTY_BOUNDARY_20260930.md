# PAYOFF-B dual-use information novelty boundary

Date: **2026-09-30**  
Status: **literature-bounded theory positioning**

## Do not claim these ideas as new

### 1. Value of information in sequential decisions

The general value-of-information idea is classical decision analysis. Dynamic
and recourse formulations long predate PAYOFF-B. In environmental decision
science, sequential/adaptive management and value of information are also
established.

Relevant anchors include:

- Avriel & Williams (1970), *Operations Research* 18:947–954,
  DOI 10.1287/opre.18.5.947.
- Williams, Eaton & Breininger (2011), *Ecological Modelling* 222:3429–3436,
  DOI 10.1016/j.ecolmodel.2011.07.003.
- Canessa et al. (2015), *Methods in Ecology and Evolution* 6:1217–1225,
  DOI 10.1111/2041-210X.12423.

Therefore PAYOFF-B must not claim that information can improve a later decision
as a general decision-theoretic novelty.

### 2. Stopovers or intermediate stages as information sources

Bauer, McNamara & Barta (2020), *Proceedings of the Royal Society B*
287:20200622, DOI 10.1098/rspb.2020.0622, explicitly model intermediate
stopovers as information sources and discuss the trade-off between the benefit
of obtaining information and the costs of staging.

PAYOFF-B must not claim that migrants can benefit from waiting/staging to obtain
better information as a new ecological idea.

### 3. En-route temporal compensation

Ortega et al. (2023), *Nature Communications* 14:2008,
DOI 10.1038/s41467-023-37750-z, show that mule deer compensate for phenological
mismatch during migration by altering movement speed and stopover use.

PAYOFF-B must not claim the existence of downstream phenological compensation
as new.

## Candidate contribution

The narrower candidate contribution is the conjunction between an endogenous
information deadline and a cue that also changes the cost of having waited.

The fixed-cost theorem asks whether

[
V_A(q)>D_{mathrm{eff}}.
]

The dual-use extension instead permits

[
D_{mathrm{eff}}=D_{mathrm{eff}}(q)
]

because the focal cue also improves a downstream compensation decision.

Under the declared additive binary model,

[
oxed{
	ext{wait}
iff
V_A(q)+V_C(q)>J+R_{C0}
}
]

or equivalently

[
oxed{
	ext{wait}
iff
V_A(q)>J+R_C(q).
}
]

The same information package therefore affects both sides of the
information-deadline comparison:

- it raises the value of the focal seasonal decision;
- it lowers the avoidable component of the effective waiting cost.

## Exact results that are more specific than generic VOI

### 1. No pure self-rescue

Compensation information alone cannot rationally justify creating a delay only
to learn how to repair that delay. Seasonal-action information value must also
be positive.

### 2. Irreducible direct waiting cost

Even perfect information about compensation cannot remove the direct
nonrecoverable waiting cost (J). Perfect dual-use information is worth waiting
for iff

[
R_{A0}>J.
]

### 3. Exact rescue interval

There is an exact region

[
oxed{
Jin
[
max(0,R_{A0}-R_{C0}),
R_{A0}
)
}
]

in which action information alone can never justify waiting, yet the same cue
becomes worth waiting for because it also identifies a better downstream
compensation response.

This is the strongest candidate novelty statement. It should be presented as a
closed-form ecological specialization of sequential value-of-information
logic, not as a new general theorem about information.

### 4. Pairwise dual-use asynchrony

In the balanced shared-cue specialization, an actor's threshold can be written
as

[
q_i
=
1-
rac{R_{A0}-J_i}{S_A+G_i},
]

when (J_i<R_{A0}). Thus actors can differ in information-use thresholds even
when raw waiting time is identical, purely because direct waiting cost or the
downstream compensation problem differs.

For two actors with finite thresholds, the asynchronous-window width is the
absolute difference in their information headroom:

[
oxed{
Delta q
=
left|
rac{R_{A0}-J_1}{S_A+G_1}
-
rac{R_{A0}-J_2}{S_A+G_2}
ight|.
}
]

This is a candidate PAYOFF-B contribution only as a closed-form ecological
deadline result. Heterogeneous recourse costs in sequential decision problems
are not themselves new.

### 5. Multi-module conditional information

The dual-use result extends to one focal seasonal-action decision plus any
number of cue-informed conditional decisions that exist only if the actor
waits:

[
	ext{wait}
iff
V_A(q)+sum_jV_j(q)
>
J+sum_jR_{j0}.
]

For perfect information, all conditional prior risks cancel. Therefore the
universal feasibility condition remains

[
R_{A0}>J.
]

The exact rescue interval becomes

[
oxed{
Jin
[
max(0,R_{A0}-sum_jR_{j0}),
R_{A0}
)
}.
]

Again, the candidate novelty is the closed-form information-deadline
specialization and its ecological interpretation, not the generic fact that
information can improve multiple later decisions.

### 6. Exogeneity gate for the fixed deadline theorem

The original fixed-(D_{mathrm{eff}}) threshold

[
q_{mathrm{wait}}
=
rac{max(A,L)+D_{mathrm{eff}}}{A+L}
]

is licensed only when the focal cue does not itself materially alter the
downstream compensation policy/cost, or when a cue-independent total effective
cost has already been identified.

If the same cue changes downstream compensation,

[
V_A(q)=D_{mathrm{eff}}(q)
]

must be solved instead.

This gives the natural snow-goose compensation screen a precise role: it is a
one-way screen for violation of the fixed-cost exogeneity assumption, not a
direct proof of the dual-use theorem.

## Safe manuscript language

Recommended:

> Sequential value-of-information and adaptive-recourse ideas are established.
> Our contribution is narrower: embedding a cue-informed downstream response
> inside an ecological information deadline yields an exact regime in which the
> cue becomes worth waiting for only because it improves both the focal seasonal
> action and the consequences of waiting.

Avoid:

- "We introduce the idea that information can improve multiple decisions."
- "We show for the first time that migrants can compensate after mismatch."
- "We introduce dynamic value of information to ecology."
- "Dual-use information is a new general decision-theoretic principle."

## Empirical boundary

Existing migration studies support separate ingredients:

- route/staging information;
- compensation for phenological mismatch;
- fitness costs of timing;
- heterogeneity in cue reliability.

No cited source located in this screen directly tests the PAYOFF-B rescue
interval or jointly estimates the focal cue's action value and its effect on the
effective deadline cost.

The natural test therefore remains prospective.
