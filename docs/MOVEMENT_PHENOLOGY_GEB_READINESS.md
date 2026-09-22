# GEB movement–phenology submission readiness

Status date: **2026-09-22**.

Status: **SCIENCE HOLD — measurement-error calibration required before submission**.

## Why the former GO status was withdrawn

The source-faithfulness audit of the Eurasian-wigeon environmental
reconstruction found that the first NASA POWER implementation omitted the
published January--July window applied before the 5 C cumulative-minimum TGS
calculation.

The corrected source-faithful reconstruction is now complete and passes its
movement/environmental validation gates. It changes the wigeon result from:

```text
old, superseded:
lambda_hat = 0.85994
stopover p = 0.972
strong |lambda|<0.75 forecast = FAIL
```

to:

```text
source-faithful:
lambda_hat = 0.749768
SE = 0.049906
naive p versus lambda_hat=1 = 5.33e-07

primary lambda<1 gate = PASS
strong |lambda|<0.75 point gate = PASS, narrowly

W2 directional stopover gate = PASS
stopover slope = -0.06286 d/d
cluster p = 0.0317
secondary 0.3<g_S<0.8 band = FAIL

travel-speed diagnostic = NOT SUPPORTED
```

The correction also exposed a higher-value inferential issue: phase is measured
with error on the predictor axis, so naive lambda can be attenuated toward zero.

## Current scientific gates

```text
broad universal-optimum test:
  COMPLETE — universal natural optimum not supported

direct phase-retention taxa:
  3 source-faithful naive estimators — PASS

within-species route replication:
  PASS — three barnacle-goose flyways

prospective wigeon estimator-scale test:
  lambda_hat < 1                      PASS
  stronger |lambda_hat| < 0.75       PASS, narrowly
  W2 directional stopover            PASS
  secondary W2 gain band             FAIL
  travel speed                       NOT SUPPORTED

environmental-information vs feedback separation:
  retained as conceptual decomposition

quantitative industrial actuation perturbation:
  PASS for cross-sectional attenuation
  stronger longitudinal deterioration prediction NOT SUPPORTED

measurement-error recovery layer:
  IMPLEMENTED

taxon-specific source-backed error calibration:
  OPEN

true-lambda=1 observation-scale null:
  OPEN pending error calibration

Aikens lambda perturbation:
  preregistered
  outcome UNOPENED
```

## Why measurement error is now a hard pre-submission gate

For the corrected wigeon transitions:

```text
observed origin-phase SD = 15.88 d
lambda_hat = 0.749768
```

Under a simple equal independent-error model with true latent lambda=1, an
error SD of about **7.94 d** would be sufficient in expectation to reproduce a
naive slope near 0.75.

That is only a stress threshold, not an empirical error estimate. But it is
small enough relative to the observed phase spread that the latent-correction
claim should not be submitted before source-backed phase-error calibration.

The same audit must distinguish:

```text
process innovation
!=
phase measurement error
```

so the existing barnacle-goose environmental-innovation SD values cannot be
reused as measurement-error SDs.

## Submission gate

```text
SCIENCE / CLAIM CEILING:
  HOLD

SOURCE-FAITHFUL WIGEON RECONSTRUCTION:
  PASS

GEB MANUSCRIPT STRUCTURE:
  AVAILABLE BUT REQUIRES UPDATED CLAIMS

FIGURES:
  REQUIRE REBUILD WITH corrected wigeon lambda/actuator result

MEASUREMENT-ERROR CALIBRATION:
  REQUIRED BEFORE GO

Aikens outcome:
  REMAINS UNOPENED

HUMAN METADATA:
  OPEN

ANONYMOUS REVIEWER HOST:
  OPEN
```

## Conditions for returning to GO

All of the following are required:

1. freeze a source-backed definition of phase measurement error for each direct
   system;
2. estimate or bound predictor phase variance, predictor/outcome error SDs, and
   consecutive-error correlation without tuning to the observed lambda;
3. run the already frozen parameter-recovery and true-lambda=1 null simulations
   at the actual sample sizes / intervals;
4. update the manuscript to distinguish naive estimator-scale lambda from any
   error-corrected latent quantity;
5. rebuild figures and reviewer snapshot from the corrected wigeon registry;
6. keep the Aikens preregistration and outcome closed until its own execution
   contract is satisfied.

## Current interpretation

The source-faithful direct data support a useful empirical coordinate and now
suggest a recurrent **waiting / stopover** actuator across mule deer, barnacle
geese and wigeon. Movement-speed and route-level contributions remain
system-dependent.

What remains unresolved is whether the magnitude of naive lambda differences,
and in particular latent lambda<1 for the weak/moderate cases, survives a
source-backed errors-in-variables audit.

Until that question is closed, GEB submission is intentionally held.
