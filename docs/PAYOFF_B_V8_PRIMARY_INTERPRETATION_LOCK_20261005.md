# PAYOFF-B V8 primary interpretation lock — 2026-10-05

Status: **WRITTEN BEFORE PRIMARY V8 ENVIRONMENTAL OUTPUT WAS OPENED**

This document fixes the interpretation of the corrected V8 primary support rule
before reading any early/late correlation or correlation-change result.

## Possible outcomes

### SUPPORTED

Required simultaneously:

- unique-spatial-pair mean delta-rho < 0;
- its 95% spatial-pair bootstrap interval is entirely below zero;
- equal-species exposure mean delta-rho < 0;
- its dependency-aware bootstrap interval is entirely below zero.

Licensed conclusion:

> Across the sampled source-destination spring relationships used by migratory
> bird species, signed interannual predictive connectivity weakened from
> 2002–2009 to 2010–2017.

Not licensed:
- every route degraded;
- birds directly perceive the fitted correlations;
- climate change is the unique causal mechanism;
- migration fitness declined;
- bird timing became worse because of the degradation;
- general information loss across all environmental cues.

### NOT_SUPPORTED

If any one of the four support conditions fails:

```text
V8_BROAD_DEGRADATION = NOT_SUPPORTED
```

Licensed conclusion:

> The data do not support a broad directional degradation of cross-site spring
> predictive connectivity under the frozen definition.

Heterogeneity, local sign reversals or individual degrading routes can still be
reported descriptively, but they do not rescue the broad claim.

### GEOGRAPHY/SPECIES DISAGREEMENT

If the unique-pair and equal-species summaries differ in direction or interval
support, the result is **NOT_SUPPORTED**.

The disagreement may be discussed as evidence that geographical relationships
and species-weighted exposure are not equivalent, but no preferred weighting
is selected after outcome access.

### NOT_ESTIMABLE

If finite detrended correlations reduce the eligible sample below the corrected
gate:

```text
V8_PRIMARY_ANALYSIS = NOT_ESTIMABLE
```

No alternative threshold or window replaces the primary analysis.

## Secondary analyses

Mandatory sensitivities and sign-reversal summaries are opened only after the
primary result is frozen.

Bird arrival, migration speed and mismatch outcomes remain excluded from the
primary V8 analysis. Any downstream environment-to-bird consequence analysis
requires its own explicit secondary contract after the environmental result is
frozen.
