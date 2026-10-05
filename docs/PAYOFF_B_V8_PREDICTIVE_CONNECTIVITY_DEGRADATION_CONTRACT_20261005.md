# PAYOFF-B V8 prospective contract — degradation of cross-site predictive connectivity

Date: **2026-10-05**

Status: **PREOUTCOME; no broad connectivity-trend result opened**

**Preoutcome dependency correction:** after the admission gate passed and before any
focal correlation outcome was opened, exact reuse of spatial source-target
pairs across species was identified. Sections 7–8 below supersede the original
species-only clustering rule; see
`docs/PAYOFF_B_V8_DEPENDENCY_CORRECTION_20261005.md`.

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

A preoutcome dependency audit after the outcome-blind admission gate showed
that many species use the same exact environmental source-target cell pair.
Because the environmental correlation is identical for a shared spatial pair,
species-by-pair rows cannot be treated as independent environmental outcomes.

The active dependence correction is recorded in:

`docs/PAYOFF_B_V8_DEPENDENCY_CORRECTION_20261005.md`.

The primary inferential unit is therefore the **unique spatial source-target
pair**.

For each unique spatial pair, calculate exactly one signed correlation change:

```text
delta_rho_pair = rho_late - rho_early
```

Primary reporting has two complementary summaries.

### Unique-spatial-pair summary

Report the unweighted mean correlation change across unique spatial pairs. This
weights each environmental relationship once.

### Equal-species exposure summary

For each species, calculate its mean correlation change across the unique
spatial pairs in its frozen mapping, then average those species means. This
prevents species represented by many breeding cells from dominating the
biological summary.

Species labels define ecological exposure; they do not duplicate the underlying
environmental outcome.

### Dependency-aware bootstrap

Use exactly:

```text
BOOTSTRAP_UNIT = UNIQUE_SPATIAL_PAIR
BOOTSTRAP_REPLICATES = 10000
BOOTSTRAP_SEED = 20261005
```

A sampled spatial pair carries its complete frozen species-incidence set when
the equal-species summary is recomputed.

The number and fraction of species with negative species means are reported
descriptively. The original binomial sign test is not used inferentially
because species means can share the same spatial environmental pairs.

## 8. Primary support rule

V8 supports broad degradation only if all are true:

1. the unique-spatial-pair mean change is negative;
2. its 95% unique-spatial-pair bootstrap interval excludes zero;
3. the equal-species exposure mean change is negative;
4. its dependency-aware bootstrap interval excludes zero.

If any condition fails:

```text
V8_BROAD_DEGRADATION = NOT_SUPPORTED
```

No window, source mapping, detrending method, directional hypothesis or
admission threshold is changed.

This support-rule correction was made before any V8 early/late correlation or
correlation-change outcome was opened.

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
