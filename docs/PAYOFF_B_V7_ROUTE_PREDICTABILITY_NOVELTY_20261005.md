# PAYOFF-B V7 route-predictability novelty boundary — 2026-10-05

Status: **PREOUTCOME; SCHEMA GATE ONLY**

## Biological question

> **Does the historical predictability of spring progression along a migration
> segment determine how strongly individual songbirds catch up to spring en
> route?**

This question returns PAYOFF-B to the user's original ecological intuition:
migrants act before directly observing future conditions, but may obtain more
or less useful information from conditions encountered earlier in the route.

## Why this is a real field question

Nemes et al. (2024) tracked individual Nearctic-Neotropical songbirds with Motus
and showed that birds caught up to the green wave as they moved north through
North America.

Their Discussion explicitly states that correlation in environmental
conditions along a route should affect the reliability of information about
future phenology, but that the study **did not measure phenological
predictability** and therefore could not assess how well Gulf Coast spring
predicted spring conditions farther north.

V7 is a direct follow-up to that declared limitation.

## Prior art that is not V7 novelty

- Kölzsch et al. (2015): route phenological predictability and migration timing
  in an avian herbivore.
- Bauer, McNamara & Barta (2020): theory of environmental variability,
  information reliability and migration timing.
- Nemes et al. (2024): individual songbirds catch up to spring en route.
- PAYOFF-B broad-bird result: pooled association between predictive
  connectivity and realized mismatch.
- PAYOFF-B preregistered wigeon result: predictive-connectivity by incoming
  phase did **not** support stronger post-error correction.

Therefore V7 cannot claim:
- environmental predictability is a new concept;
- migrants use en-route information for the first time;
- songbirds catch up to spring for the first time;
- predictive connectivity universally strengthens correction.

## Candidate contribution

The candidate contribution is deliberately narrow:

> Reanalyse the same paired individual songbird movements used by Nemes et al.
> while independently reconstructing **pre-outcome historical predictability**
> between each bird's southern and northern receiver environments, then test
> whether route predictability explains variation in how much phenological lag
> is closed en route.

The environmental predictor is estimated from years before the focal migration,
so it is not defined from the same year's catch-up outcome.

## Primary environmental quantity

For a bird moving from receiver pair (s,n) in focal year y, define

[
q_{sn,y}
=
operatorname{cor}
left(
P_{s,t},P_{n,t}
ight),
qquad
t<y,
]

where P is annual first-leaf spring-onset anomaly.

Primary source:
USA National Phenology Network historical annual First Leaf Spring Index
anomaly.

The focal migration year is excluded from q.

## Primary response

Let

[
L_S
=
D_S-P_S
]

and

[
L_N
=
D_N-P_N
]

be phenological lags at south and north receivers.

Define

[
R=L_S-L_N.
]

Positive R means that the bird reduced its lag relative to spring while moving
north.

Nemes et al. already established the average catch-up pattern. V7 asks whether
**between-route/individual variation in that catch-up** is associated with
historical predictability.

## Critical confounding boundary

Predictability may covary with migration distance. V7 therefore always adjusts
for route distance.

Actual green-wave speed in the focal year is also distinct from historical
predictability and remains a covariate.

The analysis must not reinterpret simple spatial autocorrelation as cognition.

## Negative prior

The preregistered PAYOFF-B wigeon test did not support a
predictive-connectivity by incoming-phase correction interaction.

This negative result is part of the V7 prior evidence and must remain visible
regardless of the Nemes result.

A positive V7 result would therefore support system dependence, not a universal
law.

## Schema-first rule

Before any focal association is opened, the Zenodo RDS files may be inspected
only for:
- columns;
- row counts;
- individual count;
- species;
- years;
- receiver/site-pair structure;
- coordinates;
- missingness needed for admission.

No catch-up values, predictability values or effect signs may be summarized in
the schema stage.

## Publication threshold

V7 is not automatically a paper if H1 is supported.

The result becomes publication-worthy only if:
1. the schema gate passes;
2. historical predictability can be reconstructed independently for a
   substantial fraction of birds;
3. the effect survives distance/year/species controls and leave-one-species-out;
4. the novelty search remains clear of a direct post-2023 collision;
5. interpretation remains movement/information ecology rather than generic
   control theory.

Otherwise V7 is closed and retained as a source-faithful reanalysis attempt.
