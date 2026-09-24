# PAYOFF-B cross-system lambda reliability stress

Frozen: **2026-09-24**

Status: **diagnostic null boundary; not an error calibration**.

## Question

For each highlighted direct phase-retention system, ask the deliberately simple
question:

> If latent `lambda = 1` and the only problem were equal, independent,
> classical measurement error in the phase coordinate, how large would the
> error SD have to be to produce the observed naive `lambda_hat` in
> expectation?

For predictor error SD `sigma_e`, latent predictor variance `V`, and
`rho=0`,

```text
lambda_hat = V / (V + sigma_e^2)
```

under the true-`lambda=1` null. Relative to the **observed** predictor SD, the
required error fraction is therefore

```text
sigma_e / SD(E_observed) = sqrt(1 - lambda_hat).
```

This is a stress threshold, not an estimate of real measurement error.

## Source-backed predictor scales

The predictor phase SDs were recovered from the frozen analysis artifacts, not
chosen for the stress calculation.

| system | n | observed lambda_hat | observed predictor SD | error SD required under rho=0 true-lambda=1 |
| --- | ---: | ---: | ---: | ---: |
| mule deer, whole migration | 152 | 0.1073 | 26.41 d | 24.95 d (94.5% of observed SD) |
| Svalbard goose, R2→R4 | 16 | -0.1063 | 9.07 d | no finite nonnegative classical-attenuation solution |
| Greenland goose, R2→R3 | 6 | 0.1307 | 12.49 d | 11.64 d (93.2%) |
| Barents goose, R1→R2 | 12 | 0.4941 | 27.77 d | 19.75 d (71.1%) |
| Eurasian wigeon, staging step | 224 | 0.7498 | 15.88 d | 7.94 d (50.0%) |

Machine receipt:

```text
data/payoff_b_lambda_classical_error_stress_20260924.json
```

## Interpretation

The simple null is most threatening to the weak wigeon contraction. That is
exactly the system for which PAYOFF-B now has a complete POWER-versus-ERA5
replicate calibration and event-structure SIMEX sensitivity.

The strongest mule-deer and positive goose contractions require error variance
to consume most of the observed predictor variance under the same independent
classical-error model. The Svalbard negative lambda cannot be the
large-sample expectation of true `lambda=1` under this specific attenuation
model because nonnegative independent predictor error only moves a positive
slope toward zero, not through zero.

This does **not** prove those systems are free of measurement error. Correlated
errors, nonclassical errors, phase-anchor uncertainty, small-sample behavior,
and reconstruction choices can alter the null distribution.

## Current evidence hierarchy

```text
estimator-scale common lambda coordinate:
    LICENSED

wigeon:
    source-faithful POWER + ERA5 replication
    + complete assumption-conditional error sensitivity

mule deer / barnacle goose:
    source-backed signal scale
    + classical-error stress boundary
    but no source-specific phase-error calibration

cross-taxon latent lambda magnitude ranking:
    HOLD
```

This hierarchy is enforced separately by:

```text
src/cross_system_lambda_reliability.py
data/payoff_b_cross_system_lambda_reliability_gate_20260924.json
```

## Claim ceiling

Licensed:

- compare how much independent classical error would be required to mimic each
  observed estimator-scale lambda;
- state that wigeon is the most vulnerable highlighted positive system under
  this specific null and has therefore received the strongest reliability
  audit;
- state that the low mule-deer / goose coefficients require much larger error
  relative to their observed phase signal under this null.

Not licensed:

- treat the required SDs as empirical measurement-error estimates;
- conclude measurement error is negligible in mule deer or geese;
- rank corrected biological lambda across taxa;
- use this diagnostic to bypass source-backed reliability calibration.
