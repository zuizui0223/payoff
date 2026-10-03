# PAYOFF-B mule-deer phase-sense prior-art boundary — 2026-10-03

Status: **source-backed literature boundary; frozen GEB V2 unchanged**

## Source

Ortega AC, Aikens EO, Merkle JA, Monteith KL, Kauffman MJ (2023).
*Migrating mule deer compensate en route for phenological mismatches.*
Nature Communications 14:2008.
DOI: 10.1038/s41467-023-37750-z.

## What the source already establishes

The source already goes substantially beyond a generic statement that mule deer
"track spring."

Published results include:

- 72 adult female mule deer and 152 animal-years;
- spring-migration start ranging from about 70 d ahead to 52 d behind peak
  green-up;
- mean completion of migration within a roughly 6 d window despite strongly
  asynchronous starts;
- early migrants moved about 2.9 km d-1 and used about 36 d of high-use
  stopovers;
- late migrants moved about 7.1 km d-1 and used about 10 d of high-use
  stopovers;
- 93% of deer starting ahead of the green wave fully or partially compensated,
  mainly by decelerating;
- 90% of deer starting behind fully or partially compensated, mainly by
  accelerating;
- each additional day of initial mismatch increased the odds of full
  compensation by about 1.21;
- the paper explicitly interprets the pattern as evidence that deer may
  recognize their temporal position relative to the green wave and gather
  information en route.

Therefore PAYOFF-B must **not** claim novelty for:

- discovering that mule deer can sense whether they are early or late relative
  to resource phenology;
- discovering bidirectional temporal compensation;
- discovering that speed and stopover duration can resynchronize migration;
- discovering population-level convergence from asynchronous departure toward
  more synchronized arrival;
- first proposing a cognitive "phase sense" in this system.

## What remains distinct in PAYOFF-B

The prospective PAYOFF-B contribution is the formal generalization and
identification problem.

### 1. Information × actionability

The model asks why better information can become less behaviorally useful when
remaining correction opportunities are disappearing.

### 2. Mean-retention decomposition

Under perfect phase information, the declared route controller gives

    lambda = phi (1-g).

With noisy checkpoint information the observed regression-scale retention is

    lambda = phi (1-gK),

so passive carry-over, information quality and active feedback are confounded
unless additional quantities are independently identified.

### 3. Variance-funnel fingerprint

The population model predicts

    P_next
      = phi^2 P [1-K g(2-g)] + Q,

whereas a common open-loop correction predicts

    P_next_open
      = phi^2 P + Q.

This supplies an explicit statistical contrast between a shared timing programme
and individualized state-dependent feedback.

### 4. Phase-sense inverse

With noisy checkpoint information define

    d = 1 - lambda/phi

and

    v = (P_next-Q)/(phi^2 P).

Then the declared Gaussian controller gives

    K = d^2 / (v - 1 + 2d),

    g = d/K.

Thus, with independent passive-retention and process-innovation references,
mean plus variance retention can prospectively separate an effective
information weight from a feedback gain. Ortega et al. did not frame their
analysis this way.

### 5. Cross-species coordination

PAYOFF-B links within-individual information/control differences to
between-species seasonal mismatch and to the possibility that restoring
environmental information does not restore coordinated information use.

## Why the published 6-day convergence is not itself a direct variance-funnel test

The paper provides a strong descriptive convergence pattern, but the PAYOFF-B
feedback fingerprint is stricter.

- early/mid/late classes were defined from quartiles of migration start date;
- published group summaries are not a substitute for individual continuous
  phase transitions;
- a raw start-versus-end spread can be affected by measurement error,
  conditioning, environmental variance and selective route completion;
- the open-loop comparator and passive-retention reference are not identified
  by the published summary alone.

The published result is therefore a **natural anchor for convergence and signed
compensation**, not a direct estimate of \(K\), \(\phi\), \(g\), or the
variance-funnel excess over an open-loop null.

## Safest novelty wording

> Mule deer already demonstrate that migrants can resynchronize large initial
> phenological errors through bidirectional en-route adjustment. PAYOFF-B asks
> the more general identification question: how can repeated information
> acquisition, remaining actionability and individualized feedback be separated
> mathematically, and when do differences in those control channels generate
> mismatch between interacting species?
