# PAYOFF-B V8 information-value calendar-year leverage result — 2026-10-06

Status: **POSTHOC YEAR-LEVERAGE DIAGNOSTIC; FROZEN V8 PRIMARY UNCHANGED**

## Purpose

The posthoc metric-scale analysis found a large increase in cross-validated source information value,

    G_CV = MSE(target-trend-only) - MSE(source-informed),

between 2002–2009 and 2010–2017.

Because each window is short, this audit asks whether that increase is driven by one unusually influential calendar year.

## Frozen subset for the leverage test

The audit uses only the **58 source-destination pairs with all 8 years observed in both windows**.

Baseline exact-complete result:

- early mean G_CV = **-2.655 d^2**;
- late mean G_CV = **+25.644 d^2**;
- delta G_CV = **+28.299 d^2**;
- pair-bootstrap 95% CI = **+20.746 to +36.652 d^2**.

## Global calendar-year omission

Each calendar year from 2002 through 2017 was removed globally in turn. For the affected period, cross-validated source and no-source prediction models were recomputed from the remaining seven years.

Results:

- **16/16** omitted-year analyses retained positive mean delta G_CV;
- **16/16** pair-bootstrap 95% intervals remained entirely above zero;
- minimum omitted-year mean delta G_CV = **+23.017 d^2**;
- maximum omitted-year mean delta G_CV = **+36.569 d^2**;
- minimum lower 95% bound across all omissions = **+15.045 d^2**.

The smallest mean occurred after omitting 2014. The largest occurred after omitting 2015.

Omitting 2012 still gave:

- mean delta G_CV = **+27.337 d^2**;
- pair-bootstrap 95% CI = **+21.779 to +33.279 d^2**.

Therefore the increase in cross-validated source information value is not driven by a single calendar year.

## Interpretation

This result strengthens a posthoc diagnostic; it does not convert the information-value analysis into a preregistered result.

Licensed:

> In the exact-complete environmental subset, the increase in held-out source-information value survived omission of every calendar year in both windows.

Not licensed:
- a monotonic long-term climate trend;
- climate-change attribution;
- bird perception or use of the reconstructed source signal;
- actionability as the mechanism producing bird mismatch stability.

## Provenance

Workflow:
- run: 37390021661
- artifact: 11380881660
- artifact SHA256: ffe65dc6706d7f36e3c13461f83ad6c6618da011e156ffe69902585fdf5ffa35

Script: analysis/movement_phenology/payoff_b_v8_information_value_year_leverage.R