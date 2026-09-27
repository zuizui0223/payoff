# PAYOFF-B Hoge Veluwe network-hysteresis assembly contract

Date: **2026-09-27**  
Status: **PREOUTCOME — source assembly registered, joined outcome unopened**

## Why this is a genuinely new lane

The frozen CV24C lane asked whether a fixed Ivory Coast cue showed a
decline→recovery relationship with the **annual pied-flycatcher selection
gradient**. It failed its registered reversal gate and remains
`NO_CUE_DRIVER_REVERSAL`.

This contract does not retune that result.

A separate public-data route now exists for the missing interaction layer at
the same Hoge Veluwe study system:

- Tomotani et al. provide long-term pied-flycatcher timing at Hoge Veluwe,
  including female nest-building as an arrival proxy from 1980–2015;
- the Visser et al. Dryad archive provides first-clutch great-tit phenology from
  the same Hoge Veluwe population;
- the same archive provides observed caterpillar biomass peak dates from
  1985–2020, excluding 1991.

The joined outcome has **not** been inspected.

## Frozen primary overlap

Primary source-overlap span:

```text
1985–2015
exclude 1991 from the resource series
```

With the frozen 8-year trailing connectivity window, current year excluded and
a minimum of six paired cue-resource years per window, the first eligible
history year is 1992. The preregistered primary history span is therefore:

```text
1992–2015 = 24 annual history outcomes
```

This is fixed from source availability and the predeclared window rule, not by
any observed PAYOFF-B outcome.

## Four required coordinates

### 1. Pre-commitment cue

Reuse the already frozen Ivory Coast temperature coordinate:

```text
fixed 20-day mean beginning 18 February
fixed 3×3 coarse-grid Ivory Coast proxy
no outcome-selected weather window
```

The reconstruction rule must be extended source-faithfully through 2015.
Failure to do so closes the lane.

### 2. Later destination/resource state

Primary resource state:

```text
annual observed Hoge Veluwe caterpillar biomass peak date
Dryad DOI: 10.5061/dryad.f1vhhmgx6
file: Tbl_PeakDate_Biomass_HVLim.xlsx
```

1991 is not imputed.

### 3. Migrant timing

Primary migrant coordinate:

```text
annual arithmetic mean of individual female pied-flycatcher nest-building start dates
role: source-defined proxy for female arrival
source period: 1980–2015
paper DOI: 10.1111/gcb.14006
archive: Marine Data Archive
```

The arithmetic mean is fixed from the published Methods, which states that
female individual arrival was proxied by nest-building start and that analyses
used annual means of annual-cycle stages. Median, quantile, first-arrival and
model-derived replacements are not allowed after source inspection.

Calculated male arrival is a predeclared secondary lane only.

### 4. Resident partner timing

Primary resident coordinate:

```text
annual unweighted mean laying date of included first great-tit clutches
same Hoge Veluwe population
Dryad DOI: 10.5061/dryad.f1vhhmgx6
file: Tbl_Fitness_GT_HV_FirstClutches_CSNot0_YrLargerThan1973_IncludeIs1.xlsx
```

The annual coordination coordinate is the signed calendar-day difference:

```text
female flycatcher nest-building onset
-
great-tit first-clutch laying date
```

A constant stage offset is irrelevant to branch contrasts and will not be
post-hoc estimated away.

## Gate A — source readiness

Before any joined outcome is calculated:

1. materialize the declared source files;
2. record immutable hashes;
3. verify exact Hoge Veluwe identity and year columns;
4. verify the primary overlap and missingness;
5. verify the source overlap through 2015;
6. verify that connectivity construction yields the frozen 1992–2015 history
   span (24 annual outcomes);
7. verify at least six valid cue-resource pairs in every eight-year
   connectivity window.

Any source/schema failure stops the lane.

## Gate B — information degradation and recovery

The history test is not opened unless the environmental information coordinate
itself shows the registered decline→recovery geometry.

For each year, predictive connectivity is the signed Pearson correlation
between the fixed African cue and caterpillar peak over the preceding eight
years after separately detrending both variables on year. The current year is
excluded.

A single segmented fit must satisfy all of:

```text
segmented AICc <= linear AICc - 4
pre-break slope < 0
post-break slope > 0
endpoint recovery >= 50% of the pre-break-to-break decline
```

AICc counts 2 parameters for the single line and **5** for the segmented
candidate: two intercepts, two slopes and the selected breakpoint. If candidate
segmented AICc values tie within 1e-12, the earlier break year is chosen.
Because adjacent connectivity years share most of their trailing 8-year
history, the full-sample reversal must also pass a predeclared
leave-one-history-year-out stability gate: at least 80% of leave-one-year-out
fits must retain the negative/positive slope signs, and at least 80% must place
the breakpoint within ±2 years of the full-fit breakpoint. Failure is
`UNSTABLE_CUE_RESOURCE_REVERSAL` and Gate C remains closed. All leave-one-year
diagnostics are reported.

The breakpoint is selected from the **cue–resource connectivity series only**.
Flycatcher and great-tit timing cannot define it.

Failure state:

```text
NO_CUE_RESOURCE_REVERSAL
```

If this occurs, the history test remains unopened.

## Gate C — prospective history test

Only if Gate B passes:

1. define decline and recovery branches from the frozen connectivity
   breakpoint;
2. retain only the connectivity range represented on both branches;
3. require at least six annual observations per branch;
4. fit

```text
resident_migrant_mismatch
~ centered_connectivity
+ branch
+ centered_connectivity:branch
```

Predictive connectivity is centered at the mean of the connectivity range
represented on both branches. Primary support requires the **Newey–West HAC,
lag 7 (= 8-year window − 1), finite-sample-corrected 95% CI** for the branch
coefficient to exclude zero at that point. HAC(2) and HC3 are reported as
sensitivities only. This tests whether coordination differs at comparable
information quality depending on the path by which that information state was
reached while accounting for the seven shared calendar years between adjacent
8-year connectivity estimates.

## Claim ceiling

A positive result would support:

> **natural path dependence in resident–migrant seasonal coordination
> conditional on a recovered environmental-information coordinate.**

It would **not** by itself establish:

- the exact Nash mechanism;
- intentional use of the declared temperature cue;
- a natural singleton rescue species;
- a one-species management intervention.

A negative result remains negative; no alternative breakpoint, climate window,
partner aggregation, or migrant timing coordinate may be selected after seeing
the joined outcome.

## Source provenance

- Tomotani et al. 2018, DOI: 10.1111/gcb.14006
- Tomotani Marine Data Archive record:
  http://mda.vliz.be/directlink.php?fid=VLIZ_00000444_5dd3fba4f38f8
- Visser et al. 2021 Dryad:
  https://doi.org/10.5061/dryad.f1vhhmgx6
- Existing frozen cue contract:
  `data/payoff_b_cv24c_cue_driver_contract_20260927.json`

The purpose of this file is to freeze the analysis **before** the cross-source
joined response is opened.
