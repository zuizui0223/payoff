# Primula frequency-feedback reanalysis readiness v1

Status: prospective reanalysis handoff for the *Primula farinosa* frequency-dependent floral-display system.

This document freezes the questions and claim ceiling before inspecting any supporting-data file contents.

## Primary evidence already established

Toräng, Ehrlén & Ågren (2008), Ecology 89:1564–1572, DOI `10.1890/07-1283.1`, studied a genetically based long- versus short-scaped floral-display polymorphism in *Primula farinosa*.

The audited and publisher-reported result is that pollination success and seed predation depended on morph frequency and that the resulting frequency-dependent selection varied in sign across years and populations, including rare-morph advantage in some contexts.

The publisher page also reports supporting research data in a Figshare collection (`10.6084/m9.figshare.c.3300383`).

Ågren et al. (2013), PNAS, DOI `10.1073/pnas.1301421110`, independently documents large among-population variation in morph frequencies and relative fitness, plus replicated pollinator/grazer manipulations and eight-year morph-frequency change.

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
population_or_patch_id
year
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

## Prospective analysis order

### Gate 1 — frequency support

Record the observed support of `p` by year/population. Do not extrapolate rare-invasion endpoints beyond the data range.

### Gate 2 — common-scale relative margin

Construct `Delta(p)` only if the long and short morph outcomes are commensurable.

### Gate 3 — context heterogeneity before pooling

Because the published effect changes sign among years and populations, first estimate context-specific responses.

A single pooled `eta` is allowed only after demonstrating that pooling does not erase real sign heterogeneity.

### Gate 4 — no-refit holdout

If a context has enough distinct frequency support, freeze endpoint or designated training frequencies and evaluate predeclared interior frequencies as holdouts.

Do not use all frequencies to fit `phi,eta` and then call the same points validation.

### Gate 5 — nonlinear residual

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
PRIMULA_PRIMARY_FREQUENCY_FEEDBACK_EVIDENCE_RECOVERED
PRIMULA_SUPPORTING_DATA_REPORTED_BY_PUBLISHER
PRIMULA_RAW_SUPPORTING_FILE_CONTENTS_NOT_YET_INSPECTED
PRIMULA_GENERIC_PAYOFF_COORDINATE_REANALYSIS_PREDECLARED
PRIMULA_ARCHITECTURE_MAPPING_NOT_ESTABLISHED
```
