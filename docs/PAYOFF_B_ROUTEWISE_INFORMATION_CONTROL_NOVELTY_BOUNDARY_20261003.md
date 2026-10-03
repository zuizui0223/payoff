# PAYOFF-B route-wise information-control novelty boundary — 2026-10-03

Status: **post-freeze literature audit; frozen GEB V2 unchanged**

## Prior art that PAYOFF-B must not claim

### Sequential stopover and dynamic-state migration models

Dynamic programming and optimal migration theory have long treated migration as
a sequence of state-dependent stopover, fuelling, departure and route
decisions.  PAYOFF-B must not claim that stagewise migration decisions or
dynamic programming along a route are new.

Representative prior work includes Houston & McNamara's state-dependent
framework and the stopover / optimal-migration literature summarized by
Alerstam and collaborators.

### En-route updating under phenological change

Taylor (2016), *Journal of Animal Ecology*, DOI
10.1111/1365-2656.12494, explicitly modelled migratory populations responding
to phenological change and noted that migrants can adjust migration speed en
route, with updating ability depending on stopover frequency.

Therefore PAYOFF-B must not claim that:
- en-route timing adjustment is newly proposed;
- stopovers are newly interpreted as opportunities for timing update;
- migration speed can compensate for departure mismatch is a new idea.

### Partial information and optimal switching

Chu, Lam, Wang & Wang (2026), *Numerical Algebra, Control and Optimization*,
DOI 10.3934/naco.2025026, formulate bird migration as a stochastic optimal
switching problem with waiting, detour and direct-flight states.  Their model
explicitly considers destination information before arrival and analyzes both
perfect- and partial-information cases.

Therefore PAYOFF-B must not claim:
- the first optimal-control model of migration with destination information;
- the first partial-information migration controller;
- the first formal model in which stopover/waiting choices depend on uncertain
  destination conditions.

### Bayesian filtering and feedback control

Kalman filtering, partially observed control, LQG/certainty equivalence,
Bayesian stopping, recourse and feedback stabilization are established control
and decision-theory results.

The equations used by PAYOFF-B are ecological specializations and bridges, not
generic mathematical inventions.


### Mule-deer temporal phase sense and bidirectional compensation

Ortega et al. (2023) already show that Red Desert mule deer can begin migration
far ahead or behind peak green-up, alter speed and stopover use in opposite
directions, and substantially resynchronize by the end of migration. The paper
explicitly discusses the possibility that deer recognize their position in
space and time relative to the green wave and gather information en route.

PAYOFF-B therefore must not claim discovery of:
- a temporal phase sense in mule deer;
- bidirectional en-route compensation;
- convergence from asynchronous departure toward synchronized arrival.

The separate source boundary is recorded in
\`docs/PAYOFF_B_MULE_DEER_PHASE_SENSE_PRIOR_ART_20261003.md\`.

## Candidate contribution that remains after the audit

The strongest contribution is the **specific ecological conjunction**, not any
one generic control ingredient:

1. environmental information can improve through a seasonal route while the
   remaining actionability decays;
2. this produces an exact ecological balance between information-value gain
   and optionality loss;
3. under the declared exponential reduced model, optimal information use has
   the closed form

       t* = log(1 + alpha/beta) / alpha;

4. actors seeing the same improving cue can optimally commit at different
   stages solely because their actionability decays at different rates;
5. signed phase error is propagated through route checkpoints and corrected in
   both directions;
6. the existing empirical phase-retention coordinate can be related to a
   simple feedback representation through

       lambda = phi (1-g),

   while explicitly refusing to identify lambda with actionability or control
   gain without additional information;
7. mean and variance retention can be combined, with an independent passive
   reference, to identify an effective checkpoint-information weight under the
   declared Gaussian controller;
8. these within-actor information/control differences are then connected to
   **between-actor seasonal mismatch and coordination recovery**, including the
   exact Paper-2 result that restored information need not restore coordinated
   information use.

The novelty claim should therefore be framed as an ecological
information-actionability-control synthesis with exact reduced-model
predictions, not as invention of optimal control for migration.

## Safest headline

> Seasonal mismatch can arise because interacting organisms differ not only in
> what they can learn about a future seasonal state, but in how long that
> information remains actionable and how strongly they can correct phase error
> after learning it.

## Direct empirical gap

No current PAYOFF-B natural dataset identifies, in one system, all of:

    checkpoint cue quality
    -> posterior / updated phase estimate
    -> signed actuator response
    -> outgoing phase error
    -> independently measured remaining actionability.

That full route-wise controller remains the prospective empirical target.
