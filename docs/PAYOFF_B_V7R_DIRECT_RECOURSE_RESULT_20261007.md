# PAYOFF-B V7R direct-recourse result

Date: **2026-10-07**  
Status: **PRIMARY NOT SUPPORTED**

## Primary question

Is barnacle-goose phase correction strongest on route transitions where both:

1. historical spring phenology is strongly predictable; and
2. substantial downstream temporal recourse remains?

The direct-recourse contract and Q/R source receipt were frozen before joining
the transition-level phase-retention outcome.

## Source gate

The frozen panel contains 10 transition types across all three flyways.

Primary environmental information strength:

[
Q_e=|r_{m phenology,e}|.
]

Primary remaining recourse:

[
R_j
=
rac{	ext{latest feasible remaining arrival}
      -	ext{earliest feasible remaining arrival}}
     {	ext{initial-route arrival window}},
]

using Q10--Q90 empirical transition-duration envelopes and only route-graph
edges with at least three observed transitions.

Across the ten focal transitions, Q and R are not strongly collinear
((rapprox-0.154)).

## Phase-retention identity

Nine focal transition lambdas already existed in frozen Stage-3 controller
outputs.

Re-fitting the same within-transition arrival-phase slope reproduced all nine
to numerical precision:

[
max |Deltalambda|=1.11	imes10^{-15}.
]

The additional Barents R5 -> R7 transition gives

[
lambda=0.832858.
]

Correction score is

[
C_e=1-|lambda_e|.
]

## Primary result

Frozen flyway-fixed-effect meta-model:

[
C_e
=
alpha_{m flyway}
+eta_QQ_e
+eta_RR_e
+eta_{QR}Q_eR_e
+epsilon_e.
]

Observed interaction:

[
oxed{eta_{QR}=+1.3733}.
]

The direction matches the preregistered PAYOFF prediction.

However, exact permutation of Q labels within flyway gives:

[
N_{m perm}=2880,
]

[
oxed{p_{m one-sided}=0.56994}.
]

The observed interaction is below the permutation median
((1.6330)) and is therefore not unusual under the frozen null.

**Primary verdict: NOT SUPPORTED.**

## Sensitivities

The positive coefficient direction is not driven by one transition:

- transition-n weighted: (+0.906)
- Q20--Q80 recourse window: (+1.151)
- signed phenology r: (+1.371)
- phenology (r^2): (+1.088)
- exclude Barents R5 -> R7 low-individual-support row: (+1.436)

Leave-one-transition-out estimates are all positive:

[
0.539 le eta_{QR}^{(-e)} le 4.895.
]

But one mandatory sensitivity is especially important:

- **local one-step duration-window recourse:** (eta_{QR}=+0.0245)

So the magnitude depends strongly on defining recourse as a **remaining-route
window**, not merely immediate local timing slack.

Using raw signed lambda rather than (1-|lambda|) gives essentially no
interaction ((+0.0084)).

No sensitivity overrides the failed primary permutation test.

## Biological interpretation

The simplest multiplicative story

[
	ext{predictive connectivity}
	imes
	ext{remaining recourse}
ightarrow
	ext{stronger reactive phase correction}
]

is not supported by this transition panel.

This matters because adding a more direct recourse coordinate does **not**
rescue the earlier simple prediction that higher environmental predictability
should imply stronger correction.

Several transitions show why a one-channel interpretation is inadequate. Strong
phase contraction can occur on links with weak historical spring
predictability, while some highly predictable links retain or amplify phase
error.

That pattern is compatible with the existing prospective
**prediction--correction substitution** framework:

- prediction before error and
- reactive correction after error

are distinct control channels and need not covary positively.

The present V7R result does not confirm that substitution theorem, because the
alternative interpretation was already available before this analysis and the
transition lambdas were previously known. It does, however, prospectively
reject the attempted **direct-recourse rescue** of the positive Q -> correction
prediction.

## Consequence for PAYOFF-B

The result narrows the next empirical target.

Do not infer reactive control strength from historical environmental
predictability, even after multiplying by a route-level recourse proxy.

A stronger test needs to separate:

1. pre-correction mismatch risk;
2. checkpoint information actually available to the migrant;
3. correction cost / feasible actuator set;
4. realized signed actuator response;
5. downstream phase.

In shorthand:

[
Q_{m historical}

eq
	ext{the animal's full checkpoint information state}.
]

This moves PAYOFF-B away from a one-dimensional "better cue = stronger
correction" model and toward the already declared three-stage architecture:

[
	ext{prediction}
ightarrow
	ext{commitment}
ightarrow
	ext{reactive correction}.
]

## Claim boundary

Safe:

> In a prospectively frozen ten-transition barnacle-goose test, adding an
> independently constructed remaining-route recourse coordinate did not support
> a positive predictability-by-recourse effect on phase correction.

Safe:

> The positive interaction estimate was not unusual under exact within-flyway
> permutation.

Not licensed:

- predictability is irrelevant to migration;
- recourse is irrelevant;
- prediction--correction substitution is confirmed;
- R is exact physiological actionability;
- a horse-racing analogy validates the biological mechanism.
