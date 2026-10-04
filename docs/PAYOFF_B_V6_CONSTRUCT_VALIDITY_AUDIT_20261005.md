# PAYOFF-B V6 construct-validity audit — 2026-10-05

Status: **FAIL-CLOSED BEFORE SPECIES MATCH OR FOCAL OUTCOME ACCESS**

## Trigger

V6 was prospectively defined to test whether species with more repeatable
individual migration timing show slower long-term population-level phenological
advancement.

Before opening the Franklin–Liu species match, the predictor itself was audited.

## Core problem

Migration-timing repeatability is

[
R = rac{V_{mathrm{between}}}
         {V_{mathrm{between}} + V_{mathrm{within}}}.
]

A high value can therefore arise from:
- low within-individual variability;
- high between-individual variability;
- or both.

It is not a direct measure of "rigidity", lack of plasticity or inability of an
individual to change its timing.

Franklin et al. (2022) explicitly emphasize that population-level phenological
change can arise through both:
- individuals changing their own timing; and
- changing frequencies of individuals with different stable timings.

They therefore encourage reporting the underlying within- and between-individual
variance components.

## Prior-art warning

Several single-system studies already demonstrate that repeatability and
population phenological change cannot be interpreted as a simple rigidity
continuum.

Examples include:
- Fraser et al. 2019, where purple martins showed moderate repeatability but
  broad within-individual timing variation sufficient to plausibly explain
  long-term population advancement;
- Gill et al. / black-tailed godwit work showing population-level advancement
  despite highly consistent individual timing, through recruitment/composition
  change;
- individual-cue studies showing repeatable cue use can itself generate
  adaptive population-level timing responses.

Therefore a cross-species regression of published (R) against timing-shift
rate would have a clear numerical estimand but an ambiguous biological
mechanism.

## Franklin public-data audit

The public Franklin et al. meta-analysis contains:

```text
TOTAL_REPEATABILITY_EFFECTS = 177
TOTAL_SPECIES_ROWS = 48 taxon labels (47 biological species in the publication)
EFFECTS_FLAGGED_WITH_UNSTANDARDIZED_VARIANCE_COMPONENTS = 52
SPECIES_WITH_UNSTANDARDIZED_VARIANCE_COMPONENTS = 13
SOURCE_PAPERS_WITH_UNSTANDARDIZED_VARIANCE_COMPONENTS = 13
```

Event counts among those 52 effects:

```text
Depart_breed = 13
Nonbreed_arrival = 11
Nonbreed_depart = 12
Arrival_breed = 16
```

Thus the stronger biological quantity—within-individual timing variance—is
available for only 13 species in the released extraction table.

## Consequence for the frozen V6 gate

V6 required at least 20 matched species overall before the primary comparative
analysis could run.

The mechanistically defensible replacement predictor,
(V_{mathrm{within}}), cannot meet that threshold from the currently extracted
Franklin corpus without reopening primary papers and reconstructing missing
variance components.

The weaker published-repeatability predictor can meet a larger sample size, but
does not support the intended "individual rigidity constrains climate response"
interpretation.

## Decision

No Franklin–Liu species match was opened.

No repeatability–timing-shift association was calculated.

No population-trend model was run.

```text
V6_SPECIES_MATCH = NOT_OPENED
V6_H1 = NOT_RUN
V6_DEMOGRAPHIC_EXTENSION = NOT_RUN
V6_REPEATABILITY_AS_RIGIDITY = INVALID_STRONG_INTERPRETATION
V6_WITHIN_INDIVIDUAL_VARIANCE_SPECIES = 13
V6_MINIMUM_REQUIRED_SPECIES = 20
V6_PRIMARY_ROUTE = CLOSE_CONSTRUCT_VALIDITY_AND_DATA_LIMIT
```

## Why this is not rescued by a non-directional association

One could still ask whether (R) is statistically associated with long-term
timing change without assigning a rigidity mechanism.

That would be a legitimate descriptive analysis, but it is not sufficient to
justify PAYOFF-B as an independent ecological paper because:
- one-species studies already connect individual variability to long-term
  population timing change;
- the sign of an (R)-shift association has multiple opposing biological
  interpretations;
- the strongest mechanistic predictor is unavailable at the declared sample
  threshold.

The route is therefore closed rather than weakened after the outcome.

## Reopening rule

A future cross-species analysis can reopen only if a dataset supplies, for at
least 20 species:

- directly comparable within-individual timing variance or reaction-norm
  plasticity;
- corresponding long-term population timing change;
- annual-cycle stage identity;
- and a clear independence / taxonomic mapping.

Repeatability alone does not satisfy this rule.

## Project-level implication

This audit reinforces the broader PAYOFF-B lesson from V4 and V5:

> Do not manufacture novelty by assigning a new mechanistic meaning to a
> familiar summary statistic.

The ecological question—how individual flexibility contributes to
population-level climate response—is genuine and actively studied.

The currently available comparative data are not sufficient for the intended
causal/mechanistic version of that question.
