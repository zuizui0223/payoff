# PAYOFF-B V8 stagewise retention identifiability result — 2026-10-06

Status: **RETENTION SLOPE NOT FULLY IDENTIFIABLE; RAW STRUCTURAL-NULL ATTENUATION NOT LICENSED**

## Background

A posthoc stagewise structural-null analysis fit annual population-front phase retention in the restricted 31-pair / 14-species subset:

    target phase ~ source phase + route fixed effects + year fixed effects.

Raw retention slopes were 0.250 early and 0.575 late. A fixed-arrival environmental-only null gave 0.507 early and 0.720 late. Pair bootstraps and arrival permutations initially suggested lower observed retention.

However, source phase is an estimated predictor containing source arrival date, and arrival posterior uncertainty differs strongly between periods. Classical predictor measurement error can therefore attenuate the raw slope.

## Errors-in-variables identifiability audit

After residualizing source phase on route and year fixed effects, the observed source-phase sum of squares was compared with the expected residual measurement-error sum of squares implied by the reported arrival posterior SD.

### Early period

- rows = **389**;
- units = **56**;
- years = **8**;
- raw retention beta = **0.2497**;
- fixed-arrival null beta = **0.5069**;
- observed residual source-phase SS = **2592.8**;
- expected predictor measurement-error SS = **3937.6**;
- error / observed SS ratio = **1.519**;
- latent source-phase SS estimate = **-1344.8**.

Therefore the early errors-in-variables corrected retention slope is **not identified** under this approximation.

### Late period

- rows = **432**;
- units = **56**;
- years = **8**;
- raw retention beta = **0.5745**;
- fixed-arrival null beta = **0.7197**;
- observed residual source-phase SS = **2819.4**;
- expected predictor measurement-error SS = **610.3**;
- error / observed SS ratio = **0.216**;
- latent source-phase SS estimate = **2209.1**;
- EIV-corrected beta = **0.7333**.

Thus the late-period corrected slope is approximately the same as the fixed-arrival environmental-null slope.

## Decision

The raw retention structural-null result is **not licensed as evidence of biological phase attenuation**.

Do not claim:
- bird arrival dynamics reduced phase retention relative to environmental geometry;
- phase-retention gain is identified in the bird system;
- early versus late retention coefficients measure controller strength.

The apparent raw attenuation is compatible with predictor measurement error, and the early retention slope is not identifiable under the reported posterior uncertainty.

## What survives

The separate mean stage-transformation result remains usable because it does not depend on regressing an uncertain source-phase predictor:

- source phase shift = +3.50 d;
- target phase shift = +2.13 d;
- downstream transformation change = -1.37 d;
- pair-bootstrap 95% CI -2.36 to -0.36 d;
- posterior-normal propagation around arrival means retains a negative mean change in all 5,000 simulations;
- inverse-variance reweighting retains a negative point estimate but its interval crosses zero.

Licensed same-system wording:

> Population-level relative timing changed across the mapped migration stages rather than being passively identical at source and target.

Not licensed:

> Individual birds used feedback to attenuate phase error.

## Method boundary

The identifiability calculation treats reported posterior SD as a classical predictor-error variance for sensitivity purposes and does not model unknown covariance or systematic bias. Those unresolved features reinforce rather than weaken the conclusion that the latent retention coefficient is not cleanly identified.

## Provenance

Identifiability workflow:
- run: 37402200051
- artifact: 11386065638
- artifact SHA256: 58e3947f6e747981d96ab1118c6c932ca1bb34aa16692b458b0b44c327aeb85b

Script: analysis/movement_phenology/payoff_b_v8_stagewise_retention_identifiability.R

Related raw structural-null workflow:
- run: 37401617653
- artifact: 11385546593
- artifact SHA256: e6cf3ff8cf6a25a1519c9c7876a3df2f441c1e87d5a441d8a0dafbc1d787a4df