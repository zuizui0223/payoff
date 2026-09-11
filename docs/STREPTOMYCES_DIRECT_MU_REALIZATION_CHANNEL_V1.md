# Streptomyces direct-mu realization channel v1

Lane: **A mechanism-measurement sublane only**.

Status: **prospective / pre-outcome**.

The DNA-state marker panel and 72->120 h state interval are already frozen. This document freezes the preferred strategy for the remaining realization channel. It does not report a measured realization value and does not recover the missing matched generalist/shared architecture.

## 1. Preferred absolute-state-mass route

The registered two-state model is

```text
G1 = (1 - mu) * g * G0
D1 = d * D0 + mu * g * G0
```

where `G` and `D` are compatible calibrated chromosome-equivalent masses in the intact and registered deletion states.

Define

```text
N = D1 - d * D0.
```

Under the registered model,

```text
N = mu * g * G0.
```

Therefore

```text
mu = N / (G1 + N)
g  = (G1 + N) / G0.
```

The important design consequence is that **the intact realization `g` does not need a separate independent assay** if compatible absolute state masses are available. Only the realization `d` of material already in the registered deletion state at 72 h must be supplied independently.

The older fraction-only route

```text
mu = f1 - (d/g) * f0 * (1-f1)/(1-f0)
```

remains valid and is retained as an optional/secondary route, but it requires the ratio `r=d/g` and is not the preferred primary route.

## 2. Absolute state-mass unit

The primary mass unit is

```text
CALIBRATED_CORE_CHROMOSOME_EQUIVALENTS.
```

The state panel determines what fraction of that compatible chromosome-equivalent mass belongs to intact `G` versus registered-entry `D`.

The state definitions remain:

```text
G: SCO7662/cmlR2 retained after genotype-time dosage calibration
D: SCO7662/cmlR2 lost after genotype-time dosage calibration
```

SCO7350 and SCO7036/argG remain severity markers inside `D`, not additional entry events.

## 3. Independent D-realization panel

The quantity

```text
d = D core-equivalent mass at 120 h / D core-equivalent mass at 72 h
```

must be measured using material that is already verified as `D` at the beginning of the 72->120 h interval.

It must not be inferred from the final mixed-state fraction in the congener experiment.

Because published terminal-deletion mutants show large realization/fitness heterogeneity, one convenient isolate cannot define `d`.

The pre-outcome reference panel therefore contains at least two independent references in each registered deletion-severity class:

```text
ENTRY:
    SCO7662 absent
    SCO7350 present
    SCO7036/argG present

INTERMEDIATE:
    SCO7662 absent
    SCO7350 absent
    SCO7036/argG present

DEEP:
    SCO7662 absent
    SCO7350 absent
    SCO7036/argG absent
```

All references use the same medium, ecological context, and 72->120 h horizon as the congener state channel.

## 4. Conservative realization band

Each qualified reference provides a closed uncertainty band for `d_i`.

The registered `d` band is the conservative envelope

```text
[d_L, d_H]
=
[min_i lower(d_i), max_i upper(d_i)]
```

across all qualified predeclared references and all three severity classes.

This deliberately does not pool toward a favorable mean. The purpose is to keep uncertainty in pre-existing `D` realization from being mistaken for new entry into `D`.

## 5. Exact absolute-mass uncertainty projection

For closed bands on

```text
G1, D0, D1, d,
```

define

```text
N = D1 - d*D0.
```

The physical model requires `N >= 0`.

`mu=N/(G1+N)` is increasing in `N` and decreasing in `G1`. Thus the exact Cartesian-box projection is obtained from the corresponding extrema after intersecting the `N` interval with the physical half-line `N>=0`.

Important boundaries are handled explicitly:

```text
N=0, G1>0  -> mu=0
G1=0, N>0  -> mu=1
G1=N=0     -> no output; mu not identified
```

No numerical optimizer or favorable post-hoc corner selection is permitted.

## 6. Design freeze is not reference-panel recovery

Current status is deliberately split:

```text
REALIZATION_DESIGN_FROZEN_PREOUTCOME = TRUE
REFERENCE_PANEL_MATERIALIZED = FALSE
REFERENCE_PANEL_QUALIFIED = FALSE
D_BAND_AVAILABLE = FALSE
ABSOLUTE_MASS_ROUTE_READY = FALSE
DIRECT_MU_OUTCOME_AVAILABLE = FALSE
```

Thus the design has advanced, but the biological evidence has not yet been collected.

## 7. Remaining blockers before direct-mu use

Before a direct-`mu` outcome can be used, the programme still needs:

```text
materialized D reference panel;
qualified marker-defined D references;
closed d band;
predeclared uncertainty construction for absolute state masses;
direct-mu materiality threshold.
```

The overall congener programme additionally still lacks a response-blind qualified primary genotoxicity scale and its threshold.

## 8. Claim ceiling

Neither this algebra nor a future measured `d` band automatically recovers:

```text
matched generalist/shared architecture;
matched S comparator;
architecture mapping;
frequency-dependent architecture payoff;
PAYOFF eta;
E1.
```

The architecture-specific claim ceiling is unchanged.
