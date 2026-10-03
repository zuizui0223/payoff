# PAYOFF-B V5 corpus viability gate — 2026-10-03

Status: **PREOUTCOME STOP RULE**

No V5 timing-propagation coefficient may be interpreted before this gate is
evaluated from schema/count information only.

## Lane G — global harmonized data

Lane G is viable only if, after excluding population-level proxy rows and
records that cannot be assigned to the declared source structure:

- at least **500 individual full-annual-cycle records** remain;
- at least **50 species** remain;
- at least **20 independent source cohorts** contain >=3 individual records;
- all four declared transition classes are represented;
- the paired-source sensitivity contains at least **20 source cohorts with
  >=5 individual records** that contribute both ACTIVE and STATIONARY
  transitions.

If the first four conditions fail:

```text
LANE_G = INSUFFICIENT_HARMONIZED_CORPUS
```

If only the paired-source condition fails, the baseline global model may run
but the paired-source sensitivity is reported as not estimable.

## Lane L — literature transition synthesis

Lane L is viable for the H1 external-validation meta-analysis only if the
preoutcome extraction yields:

- at least **6 independent studies** contributing Tier A/B effects;
- at least **3 independent studies** contributing ACTIVE effects;
- at least **3 independent studies** contributing STATIONARY effects;
- at least **20 Tier A/B transition effects** total;
- no single source study contributes more than **40%** of the primary effects.

If this gate fails:

```text
LANE_L = INSUFFICIENT_IDENTIFIABLE_CORPUS
```

and Lane L cannot be rescued by converting correlations, repeatabilities,
standardized coefficients or population means into (eta_{AB}).

## H2 available-time gate

The primary H2 moderator requires at least:

- **10 stationary transition effects**;
- from **>=5 independent studies/source cohorts**;
- with source-reported or independently reported effect-level stationary-period
  duration.

If this independent-duration gate fails, H2 is not promoted as a primary
result. SAME_SAMPLE_DERIVED durations may be shown only as the prespecified
sensitivity.

## Cross-lane publication states

```text
G_PASS + L_PASS
    -> V5_COMPARATIVE_SYNTHESIS_VIABLE

G_PASS + L_INSUFFICIENT
    -> V5_GLOBAL_REANALYSIS_VIABLE_EXTERNAL_VALIDATION_UNRESOLVED

G_INSUFFICIENT + L_PASS
    -> V5_LITERATURE_SYNTHESIS_ONLY

G_INSUFFICIENT + L_INSUFFICIENT
    -> STOP_V5
```

A directional disagreement between two estimable lanes is a scientific result,
not a reason to remove one lane.

## Why these thresholds exist

The thresholds are design stop rules, not formal power guarantees. They prevent
a binary transition-class claim from being carried by a handful of studies or
one unusually data-rich source and prevent H2 from becoming a same-sample
algebraic artifact.

They were fixed before opening the focal (eta_{AB}) values.
