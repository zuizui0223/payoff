# Primula frequency-feedback reanalysis readiness v1

Status: prospective reanalysis handoff for the *Primula farinosa* frequency-dependent floral-display system.

This document freezes the questions and claim ceiling before inspecting any supporting-data file contents.

## Primary evidence already established

Toräng, Ehrlén & Ågren (2006), Ecology 87:2113–2117, DOI `10.1890/0012-9658(2006)87[2113:FIAIHW]2.0.CO;2`, experimentally tested whether seed production in the short-scaped morph varied with local morph frequency and vegetation height. In tall vegetation, short-scaped plants in polymorphic populations produced more fruit and tended to produce more seeds than short-scaped plants in monomorphic populations; this population-composition effect was not significant in low vegetation. This is a causal frequency-context anchor for one morph, but it does not by itself provide reciprocal long-versus-short invasion margins.

Toräng, Ehrlén & Ågren (2008), Ecology 89:1564–1572, DOI `10.1890/07-1283.1`, studied the same genetically based long- versus short-scaped floral-display polymorphism.

The audited and publisher-reported result is that pollination success and seed predation depended on morph frequency and that the resulting frequency-dependent selection varied in sign across years and populations, including rare-morph advantage in some contexts.

The publisher page also reports supporting research data in a Figshare collection (`10.6084/m9.figshare.c.3300383`).

Ågren et al. (2013), PNAS, DOI `10.1073/pnas.1301421110`, independently documents large among-population variation in morph frequencies and relative fitness, plus replicated pollinator/grazer manipulations and eight-year morph-frequency change.

The three studies are complementary rather than interchangeable:

```text
2006 -> experimental local-frequency effect on short-morph reproductive output
2008 -> direct context-dependent frequency-dependent selection on morphs
2013 -> causal mutualist/grazer selection mosaic and long-term morph-frequency evolution.
```

## What can be tested if the supporting data contain the required fields

The strongest justified reanalysis is a **generic two-morph PAYOFF-coordinate analogue**, not a shared-versus-differentiated architecture identification.

Let

```text
p = frequency of the long-scaped morph
Delta(p) = relative fitness_long(p)-relative fitness_short(p).
```

If one common fitness scale is reconstructable for both morphs across frequency contexts, then the following can be tested prospectively:

```text
Delta(p)=phi+eta(2p-1).
```

The resulting `phi` and `eta` would be coordinates of the *Primula* two-morph game only. They must not be interpreted as the architecture `phi=sL-K` and architecture feedback `eta` of the SCH/BALANCE/BITA bridge.

## Frozen extraction requirements

A usable record must contain or permit reconstruction of:

```text
study_year_or_experiment
population_or_patch_id
year
vegetation_or_grazing_context
long_morph_frequency
long_morph_fitness_or_components
short_morph_fitness_or_components
sample_sizes_or_weights
pollination_component_if_available
seed_predation_component_if_available
grazing_component_if_available
uncertainty_or_raw_counts_if_available
```

A common net-fitness scale is preferred. If only component-specific outcomes are available, analyse them separately and do not silently combine them into one fitness margin without an explicit biological aggregation rule.

The 2006 experiment may remain one-sided if only short-morph output was recorded across composition treatments. Such a result can validate a population-composition effect but cannot be converted into reciprocal `u,v` margins without data for the long morph on the same scale.

## Prospective analysis order

### Gate 1 — frequency support

Record the observed support of `p` by year/population/experimental treatment. Do not extrapolate rare-invasion endpoints beyond the data range.

### Gate 2 — common-scale relative margin

Construct `Delta(p)` only if the long and short morph outcomes are commensurable.

### Gate 3 — context heterogeneity before pooling

Because the published effect changes with vegetation context and changes sign among years and populations, first estimate context-specific responses.

A single pooled `eta` is allowed only after demonstrating that pooling does not erase real interaction or sign heterogeneity.

### Gate 4 — reciprocal endpoint sufficiency

Do not label an assay reciprocal merely because morph frequency was manipulated. Both long-versus-short relative margins must be available near opposite resident-frequency contexts for a reciprocal phase claim.

A one-sided composition experiment is retained as frequency-feedback evidence without promotion to P2.

### Gate 5 — no-refit holdout

If a context has enough distinct frequency support, freeze endpoint or designated training frequencies and evaluate predeclared interior frequencies as holdouts.

Do not use all frequencies to fit `phi,eta` and then call the same points validation.

### Gate 6 — nonlinear residual

Report whether the affine law is compatible over the observed support and quantify any residual curvature or context dependence. A rejected affine law is a valid empirical result.

## What this reanalysis cannot establish even if successful

Even a clean affine two-morph fit would not establish:

```text
that long and short scapes are shared versus differentiated architectures;
that SCH conflict generated the morph dimorphism;
that BITA dimensional release produced the two morphs;
that phi=sL-K for this system;
that historical branching occurred through the PAYOFF mechanism.
```

The allowed ecological conclusion would instead be:

> A real mutualist-antagonist floral polymorphism can be represented, over the observed frequency range and contexts where the fit survives holdout validation, by the same minimal two-strategy frequency-response coordinates used by PAYOFF.

That would validate transportability of the **game layer**, not the upstream architecture mechanism.

## Current readiness label

```text
PRIMULA_2006_EXPERIMENTAL_COMPOSITION_EFFECT_RECOVERED
PRIMULA_2008_PRIMARY_FREQUENCY_FEEDBACK_EVIDENCE_RECOVERED
PRIMULA_2013_CAUSAL_FREQUENCY_TRAJECTORY_EVIDENCE_RECOVERED
PRIMULA_SUPPORTING_DATA_REPORTED_BY_PUBLISHER
PRIMULA_RAW_SUPPORTING_FILE_CONTENTS_NOT_YET_INSPECTED
PRIMULA_GENERIC_PAYOFF_COORDINATE_REANALYSIS_PREDECLARED
PRIMULA_RECIPROCAL_MARGIN_SUFFICIENCY_NOT_YET_ESTABLISHED
PRIMULA_ARCHITECTURE_MAPPING_NOT_ESTABLISHED
```
