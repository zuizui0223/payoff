# PAYOFF-B V8 prospective contract — degradation of cross-site predictive connectivity

Date: **2026-10-05**

Status: **PREOUTCOME; no broad connectivity-trend result opened**

## 1. Biological question

> **Has climate change degraded the spatial environmental relationships that
> migrants can use to forecast future seasonal conditions?**

The focal object is not bird timing itself. It is the signed interannual
relationship between an environmental state available earlier along a
migration route and the state realized later at a breeding destination.

The user-originating ecological intuition is:

> climate change may not only advance spring; it may make an earlier place a
> worse predictor of the spring that a migrant will encounter later.

## 2. Primary field

- migration ecology;
- information ecology;
- global-change phenology;
- spatial climate / phenology predictability.

This is an environmental-information test, not a new control-theory paper.

## 3. Frozen data source and route geometry

Primary source:
Amaral et al. BirdMigrationSpeed dataset, fixed source commit

`62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`

and Dryad DOI 10.5061/dryad.ttdz08m6w.

Use exactly the source-target mapping already frozen for the 2026-09-26
PAYOFF-B predictive-connectivity analysis:

- target = a species breeding-range cell;
- source = geographically nearest cell for the same species marked as migratory
  range with strictly lower latitude;
- ties resolved by numeric cell id;
- mapping uses only spatial/range metadata.

No bird arrival date, bird speed, mismatch response or fitted bird outcome is
used to select source-target pairs or define connectivity.

## 4. Environmental coordinate

For each species j and frozen source-target cell pair p, use annual green-up day
at source and target cells.

Within each analysis window:
1. regress source green-up separately on year;
2. regress target green-up separately on year;
3. correlate the two residual series.

The primary coordinate is the existing signed detrended Pearson correlation:

[
ho_{jp}.
]

Signed (ho) is retained because it is the empirical coordinate used in the
frozen broad-bird analysis. Negative correlations are not folded to positive
values.

## 5. Non-overlapping climate windows

To avoid the severe serial dependence of rolling 8-year correlations, the
primary analysis uses two fixed, non-overlapping environmental windows:

[
	ext{EARLY}=2002	ext{--}2009
]

and

[
	ext{LATE}=2010	ext{--}2017.
]

These windows are chosen from the declared 2002–2017 source span before
calculating any V8 connectivity change.

Each window requires at least 6 paired annual green-up observations, matching
the original connectivity minimum-pairs rule.

No bird outcome year is excluded because V8 uses only environmental states and
does not fit a contemporaneous bird response.

## 6. Primary estimand

For every source-target pair estimable in both windows:

[
Deltaho_{jp}
=
ho^{late}_{jp}
-
ho^{early}_{jp}.
]

Interpretation:
- (Deltaho<0): the signed predictive relationship weakened;
- (Deltaho=0): no change;
- (Deltaho>0): the signed predictive relationship strengthened.

The primary hypothesis is:

[
oxed{E(Deltaho)<0}.
]

This is a directional hypothesis about the broad multi-species distribution,
not a claim that every route pair degrades.

## 7. Primary inferential unit

Source-target cell pairs within a species are not treated as independent
species replicates.

Primary reporting therefore has two levels:

### Pair-level model
A mixed intercept model for (Deltaho_{jp}) with species as a grouping
factor.

### Species-level robustness
For each species, calculate the mean (Deltaho) across eligible mapped
pairs. Report:
- number of species with negative versus positive species means;
- one-sided sign test for a negative majority;
- mean species-level (Deltaho) with a species bootstrap interval.

The headline conclusion requires the direction to be consistent between the
pair-level mixed estimate and the species-level summary.

## 8. Primary support rule

V8 supports broad degradation only if all are true:

1. the pair-level mean change is negative;
2. its species-cluster bootstrap 95% interval excludes zero;
3. more than half of species have negative species-mean change;
4. the one-sided species sign test is p < 0.05.

If any condition fails:

```text
V8_BROAD_DEGRADATION = NOT_SUPPORTED
```

No window, source mapping, detrending method or species threshold is changed.

## 9. Admission gate

Do not calculate the sign or magnitude of (Deltaho) unless:

- >=100 frozen source-target pairs are estimable in both windows;
- >=20 species have at least one estimable pair;
- >=15 species have at least 3 estimable pairs;
- both windows contain at least 6 annual pairs for every admitted source-target
  pair.

If this gate fails:

```text
V8_PRIMARY_ANALYSIS = NOT_ESTIMABLE
```

and no threshold is lowered.

## 10. Mandatory sensitivities

After the primary result is frozen:

1. Fisher-z change:
   [
   Delta z = operatorname{atanh}(ho_{late}) -
              operatorname{atanh}(ho_{early})
   ]
   using a prespecified numerical clamp at ±0.999 only if needed;
2. exact-complete windows only: require all 8 annual pairs in each window;
3. target-cell equal weighting within species;
4. source-target geographic distance as a prespecified moderator;
5. migration-distance class as a secondary moderator if independently
   available from the frozen Amaral source;
6. leave-one-species-out;
7. raw undetrended correlation as a negative-control coordinate, not as a
   replacement primary analysis;
8. alternative 7-year non-overlapping windows 2002–2008 and 2011–2017.

No sensitivity replaces the primary signed-detrended 8-year result.

## 11. Secondary sign-reversal summary

A descriptive secondary quantity counts pairs that move from:

[
ho_{early}>0
]

to

[
ho_{late}le0.
]

This is motivated by the natural route-level example in Schreven et al. 2026.

No threshold for a "meaningful" reversal is chosen after seeing the
distribution.

## 12. Separation from the existing broad-bird result

The 2026-09-26 registered result asked:

> Is stronger **pre-existing** predictive connectivity associated with smaller
> bird arrival–green-up mismatch?

V8 asks a different upstream environmental question:

> Has predictive connectivity itself changed through time?

The V8 primary analysis uses no bird arrival, speed or mismatch variable.

Only after the V8 environmental result is frozen may a separate, explicitly
secondary analysis ask whether routes with stronger connectivity degradation
also show larger mismatch change.

That downstream analysis is not part of the primary V8 support rule.

## 13. Claim ceiling

A supported primary result licenses:

> Across the sampled migratory-bird route pairs, the signed interannual
> relationship between source and destination spring phenology weakened between
> 2002–2009 and 2010–2017.

It does not license:
- proof that individual birds perceive this correlation;
- proof that climate change is the unique causal driver;
- proof that information quantity universally declined;
- proof that migration fitness declined;
- community-level hysteresis;
- a claim that every species or route degraded.

## 14. Outcome-access rule

Before this contract is merged:

- do not calculate early-window (ho);
- do not calculate late-window (ho);
- do not calculate (Deltaho);
- do not count negative species or sign reversals;
- do not inspect any V8 trend result.

Existing 2026-09-26 connectivity-vs-mismatch outcomes remain known prior
results but are not V8 outcomes.

```text
V8_CONTRACT = FROZEN_PREOUTCOME
V8_ENVIRONMENTAL_CHANGE = UNOPENED
V8_BIRD_OUTCOMES_USED_IN_PRIMARY = NO
```
