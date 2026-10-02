# PAYOFF-B route-wise phase-control empirical contract

Date: **2026-10-02**  
Status: **prospective post-freeze contract; no new natural outcome opened**

## Question

Do migrating animals repeatedly estimate signed seasonal phase error and correct
it at successive route checkpoints?

The direct observational unit is a transition

    checkpoint t -> checkpoint t+1,

not the whole migration.

## Required variables

For each animal-transition:

1. incoming phase error
       e_in = animal phase - local resource-wave phase;
2. information available by the checkpoint
       local temperature / green-up / other source-backed cue;
3. actuator response after the checkpoint
       movement speed, stopover duration, route choice, or a declared composite;
4. outgoing phase error
       e_out at the next checkpoint;
5. remaining actuator capacity measured independently of e_out where possible.

Do not estimate the cue from the same response used to define correction.

## Primary signed-feedback prediction

With sign convention e>0 = late:

- e_in > 0 predicts advancement:
  faster movement and/or shorter stopover;
- e_in < 0 predicts delay:
  slower movement and/or longer stopover.

The primary test is a signed continuous association, not an early/late
post-hoc split.

## Primary phase-contraction prediction

Conditional on route stage and resource-wave movement, active feedback predicts

    e_out = a + lambda e_in + error

with a contraction relative to passive carry-over.

The direct mechanistic target is not merely lambda<1.  Under the route-wise
model,

    lambda = phi (1-g),

so identification of active gain g requires an independent passive-retention
reference phi or an intervention / natural contrast that changes actuator
availability without redefining phase.

## Strong falsifiers

The controller interpretation is weakened if an independent dataset shows any
of the following:

1. signed phase error does not predict correction direction despite measurable
   unused actuator capacity;
2. late and early errors produce the same directional actuator response;
3. removing actuator availability does not increase retained phase error when
   cue quality is unchanged;
4. a departure-only model predicts held-out downstream phase as well as a
   checkpoint-update model despite informative intermediate cues;
5. correction magnitude is unrelated to the posterior/locally updated phase
   estimate after controlling for route stage.

## Information-update prediction

If checkpoint cues improve phase estimation, uncertainty about downstream
seasonal phase should decline after informative stops.  The strongest test
compares held-out prediction of e_out using:

    origin-only information

versus

    origin + checkpoint information.

A route-stage cue is useful only if it improves out-of-sample prediction or
changes a prespecified downstream action; correlation with local conditions
alone is insufficient.

## Actionability prediction

Cue responsiveness need not peak at the final or most informative checkpoint.
If remaining correction capacity declines along the route, the strongest
behavioral response can occur at an intermediate stage.

This is the empirical counterpart of the actionability-balance theorem.

## Current source anchors

Existing PAYOFF-B evidence supplies motivation but is not counted as a new
prospective confirmation:

- mule deer: signed early/late differences in speed and stopover use;
- bar-tailed godwit: earlier departure can be absorbed by longer later
  stopovers;
- pink-footed goose: cue relevance changes along the migration route;
- barnacle goose / Eurasian wigeon / mule deer: segment-scale phase-retention
  coordinates already reconstructed;
- American redstart: compensation after delayed departure can carry survival
  cost.

## Claim boundary

A successful future test would support a route-wise ecological feedback
controller.  It would not show that animals explicitly compute probabilities,
Kalman gains, train-like schedules, or the PAYOFF-B equations neurally.

The "Mikawa-Anjo clock" is therefore a falsifiable functional claim:

> animals behave as if they repeatedly update an internal phase estimate and
> use remaining actuators to reduce signed seasonal error.
