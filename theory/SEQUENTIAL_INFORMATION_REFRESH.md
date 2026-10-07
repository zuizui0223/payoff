# PAYOFF-B sequential information refresh

Date: **2026-10-07**  
Status: **prospective post-V7R theory; V7R null unchanged**

## 1. Why this extension exists

The direct-recourse V7R test asked whether one historical environmental
predictability coordinate Q, multiplied by remaining temporal recourse R,
explains reactive phase correction across barnacle-goose route transitions.

That frozen primary test was not supported.

This note does **not** retune V7R. It opens a different information
architecture:

> a migrant can acquire new environmental information at successive route
> checkpoints instead of carrying one origin forecast all the way to the
> destination.

Generic Markov prediction, Bayesian filtering and sequential cue updating are
established prior art. The ecological purpose is to state exactly why a low
origin-to-destination correlation need not imply that downstream information is
poor.

## 2. Markov seasonal chain

Let standardized seasonal states along an ordered route be

[
X_0,X_1,ldots,X_n,
]

with local dynamics

[
X_{j+1}
=
ho_jX_j
+
sqrt{1-ho_j^2},epsilon_j,
]

where

[
|ho_j|le1
]

and innovations are independent standard normal variables.

Then

[
mathrm{Corr}(X_i,X_k)
=
prod_{j=i}^{k-1}ho_j.
]

## 3. Direct forecast from the origin

If the actor observes only the initial state (X_0), the absolute predictive
connectivity to the destination is

[
Q_{m direct}
=
left|
prod_{j=0}^{n-1}ho_j
ight|.
]

One weak link can make long-range predictability nearly zero.

This is the static information architecture implicitly assumed when a single
origin-to-destination Q is used for the whole decision interval.

## 4. Checkpoint refresh

Suppose the actor reaches checkpoint (m) and obtains a fresh observation of
(X_m) before the remaining route is fixed.

With a perfect checkpoint observation, destination predictability becomes

[
Q_m
=
left|
prod_{j=m}^{n-1}ho_j
ight|.
]

For local links with (|ho_j|le1), deleting earlier factors weakly
increases this quantity as the actor moves downstream.

Therefore:

[
oxed{
Q_{m direct}ll1
quad
otRightarrowquad
Q_mll1.
}
]

A route can be poorly predictable from far away and highly predictable after a
later checkpoint refresh.

## 5. Exact rescue witness

Take three states:

[
X_0	o X_1	o X_2,
]

with

[
ho_0=arepsilon,
qquad
ho_1=1.
]

Then

[
|mathrm{Corr}(X_0,X_2)|
=
arepsilon,
]

which can be arbitrarily close to zero.

But after observing (X_1),

[
|mathrm{Corr}(X_1,X_2)|=1.
]

Thus a near-zero long-range environmental correlation is fully compatible with
perfect final-step predictability after information refresh.

This is a mathematical boundary case, not evidence that real migrants observe
seasonal state perfectly.

## 6. Noisy checkpoint information

Let checkpoint observation be

[
Z_m=X_m+
u_m,
]

with independent noise variance

[
	au_m^2.
]

Then

[
mathrm{Corr}(Z_m,X_m)^2
=
rac{1}{1+	au_m^2}.
]

The squared predictive information about the destination carried by (Z_m) is

[
I_m
=
rac{1}{1+	au_m^2}
prod_{j=m}^{n-1}ho_j^2.
]

This separates:

- checkpoint observation reliability;
- downstream environmental propagation.

## 7. Combine refresh with actionability

Let

[
r_min[0,1]
]

be retained response capacity after checkpoint (m).

A declared reduced-form usable-information coordinate is

[
A_m=r_m I_m.
]

Even if (I_m) increases downstream because forecasts are refreshed, (r_m)
can decline as speed, stopover, route or breeding-timing options disappear.

Therefore (A_m) can peak at an intermediate checkpoint.

This is the sequential analogue of the existing actionability-balance model.

## 8. What this changes empirically

A single historical correlation

[
Q_{m origin,destination}
]

is insufficient to represent the animal's information state when route-stage
observations are possible.

The direct empirical comparison should instead be:

### Origin-only forecast

Predict downstream seasonal phase from information available before the focal
checkpoint.

### Refreshed forecast

Predict the same downstream phase using:

- the same origin information;
- plus environmental information newly available at the checkpoint.

Checkpoint information is useful only if it improves held-out prediction.

The biological control test then asks whether the **incremental predictive
gain** is converted into stronger state-contingent correction when recourse
remains.

## 9. Relation to Kölzsch et al.

Kölzsch et al. established that spring-onset correlations differ among route
links and that migration timing is related to environmental predictability.

The current PAYOFF-B point is narrower:

> pairwise historical predictive connectivity is not automatically identical
> to the information available to an animal after sequential route updates.

The V7R null therefore does not justify redefining Q post hoc. It motivates a
new prospective comparison between origin-only and checkpoint-refreshed
forecast states.

## 10. Relation to prediction-correction substitution

Sequential refresh and prediction-correction substitution are complementary.

A migrant can reduce final mismatch through:

1. better prediction before error occurs;
2. renewed prediction at checkpoints;
3. reactive correction after observing error.

Observed phase retention alone does not identify the allocation among these
channels.

## 11. Falsifiable prediction

For a future or untouched checkpoint dataset:

1. adding checkpoint-local information must improve held-out prediction of the
   downstream seasonal target;
2. that incremental forecast gain should predict a prespecified downstream
   action only when recourse remains;
3. after controlling for refreshed information, static long-range Q should add
   little if it was only a proxy for intermediate updates.

A failure of step 1 closes the sequential-information explanation before
testing behavioral response.

## 12. Claim boundary

Safe:

> In a Markov seasonal chain, sequentially refreshed observations can restore
> high short-range predictive information even when origin-to-destination
> correlation is weak.

Safe:

> A static pairwise environmental correlation need not equal the information
> state available to a migrant at a later checkpoint.

Not licensed:

- real geese implement a Markov model;
- historical spring correlations are neural beliefs;
- V7R null confirms sequential updating;
- a checkpoint cue is useful without held-out predictive improvement;
- this is new generic filtering mathematics.
