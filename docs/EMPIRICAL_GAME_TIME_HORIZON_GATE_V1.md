# Empirical game time-horizon gate v1

PAYOFF's reciprocal-invasion and frequency-response estimands require a declared time horizon over which the competing type definitions and their payoff response are treated as fixed.

This document is a measurement-contract guardrail, not a new population-dynamics theorem.

## 1. Why a time horizon belongs in the estimand

A two-type empirical game writes a relative margin such as

```text
Delta(p) = performance_D(p) - performance_S(p).
```

That expression presumes that `S` and `D` retain the biological properties used to define them while `Delta(p)` is measured.

If one type acquires genetic, phenotypic, developmental, or community-composition changes during the assay that materially alter its resource use or payoff function, then later observations no longer estimate the same frozen two-type game.

Therefore every empirical PAYOFF frequency claim should declare

```text
frequency support
external ecological context
type/architecture definition
measurement scale
assay time horizon.
```

## 2. Three admissibility classes

### H0 — frozen-type window supported

Use the reciprocal-sign / affine-frequency machinery when the design deliberately minimizes type evolution or when independent evidence shows that type identity and relevant payoff traits remain stable over the measurement window.

### H1 — type change detected but bounded after the primary window

The early window can still identify the frozen-type estimand, but later observations must be reported as a separate evolutionary extension.

Do not silently pool H0 and H1 observations into one `phi,eta` estimate.

### H2 — type change occurs within the identification window

A fixed two-type PAYOFF interpretation is not licensed. A model with evolving strategies, changing state variables, or explicitly time-varying payoffs is required before assigning a static phase.

## 3. Pseudomonas stutzeri registered example

Dolinšek, Ramoneda & Johnson (2022), DOI `10.1038/s43705-022-00160-1`, explicitly used the first three serial transfers for reciprocal initial-ratio tests to reduce the probability that genetic and phenotypic changes would emerge while retaining enough timepoints for a trend test.

With 1:100 serial dilution, this is approximately

```text
19.932 generations.
```

At pH 6.5, both rare types increased over this short window, yielding a clean reciprocal-invasion sign receipt.

The authors then extended the experiment to 12 transfers, approximately 80 generations. In treatments initiated with rare specialists, the specialist first rose strongly and then declined while the generalist acquired altered nitrite-consumption phenotypes. The authors' longer-term model required an evolved generalist phenotype to reproduce this deviation.

The correct PAYOFF adjudication is therefore

```text
first 3 transfers:
    H0 / short-window generic reciprocal-invasion estimand supported;

12-transfer evolutionary trajectory:
    H1 / frozen-game extrapolation not supported unchanged.
```

This is not a contradiction. The two observations concern different estimands because the type properties cease to be fixed over the longer horizon.

## 4. Manuscript language

Preferred:

> Reciprocal invasion was identified over a pre-evolution window in which the original study explicitly minimized genetic and phenotypic change; longer propagation produced composition-dependent evolution of the generalist, so we treat the later trajectory as a separate evolving-game regime rather than extrapolating the same fixed payoff coordinates.

Avoid:

> The short-term game predicts the 80-generation outcome.

Avoid also:

> Long-term evolution falsifies the reciprocal-invasion result.

The long-term result instead falsifies an **unlicensed fixed-parameter extrapolation** beyond the declared empirical horizon.

## 5. Status labels

```text
EMPIRICAL_PAYOFF_TIME_HORIZON_REQUIRED
FROZEN_TYPE_SHORT_WINDOW_AND_EVOLVING_LONG_WINDOW_MUST_BE_SEPARATED
PSTUTZERI_SHORT_WINDOW_H0_SUPPORTED
PSTUTZERI_LONG_WINDOW_H1_EVOLVING_GAME_BOUNDARY_RECOVERED
```
