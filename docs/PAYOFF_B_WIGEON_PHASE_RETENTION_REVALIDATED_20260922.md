# PAYOFF-B Eurasian wigeon source-faithful revalidation

Frozen source-window amendment: **2026-09-22**  
Corrected workflow result: **2026-09-22**

Status: **source-faithful naive estimator restored; measurement-error audit still pending**.

## 1. Why the previous result was superseded

The original independent NASA POWER reconstruction applied the published 5 C
cumulative-minimum TGS rule over the full calendar year.

The published supplementary environmental code instead first restricts the
daily series to:

```r
days <- days[month(days)<8]
```

that is, January through July.

The mismatch allowed cold northern cell-years to return day 365/366 as an
apparent TGS onset and created phase values near -200 d. The correction rule was
frozen before inspecting the corrected lambda.

## 2. Corrected source provenance

```text
source PR:        #144
source branch:    empirical/movement-phenology-macro-20260918
source head:      906aa634ff260ee2f8dfe8a42bcdd60cc7f0f907
workflow run:     35689856130
artifact:         10678143392
artifact SHA256:  d61afae4a4dcf62f0947c5ec49684aeb4cebad18fabde9b8eb74035fe4326388
```

The movement source, HMM, staging-site reconstruction, controller model,
covariates and clustering rule were unchanged.

## 3. Environmental reconstruction after the fix

The corrected POWER reconstruction gives:

```text
staging events total:             256
staging events with TGS:          256
TGS onset >= day 300:               0

arrival phase median:            21.97 d
arrival phase Q1:                13.18 d
arrival phase Q3:                34.25 d

published median:                22.5 d
published Q1:                    13.0 d
published Q3:                    35.3 d
```

All retained environmental validation gates pass.

The origin-phase SD across the 224 controller transitions changes from the
inflated full-year value of about 78.6 d to **15.88 d**.

## 4. Corrected W1 phase-retention result

The frozen primary controller model still uses 224 consecutive staging
transitions from 28 individuals.

```text
beta_E = -0.250232
cluster SE = 0.049906
cluster p = 2.93e-05

lambda_hat = 1 + beta_E
           = 0.749768

SE(lambda_hat) = 0.049906

naive test against lambda_hat=1:
p = 5.33e-07
```

Therefore the original registered estimator-scale primary gate remains:

```text
lambda < 1:
    PASS
```

The stronger frozen point-estimate forecast also changes class:

```text
|lambda| <= 0.75:
    PASS
```

because the corrected estimate is 0.749768. This is only about 0.00023 inside
the frozen boundary, so the result is reported as a mechanical point-estimate
gate rather than promoted as evidence for a universal strong-correction
constant.

## 5. Corrected W2 stopover actuator result

The preregistered W2 prediction was:

```text
stopover_duration decreases with later phase
and p <= 0.05
```

Corrected source-faithful result:

```text
slope = -0.062863 stopover-days / phase-day
cluster SE = 0.027739
p = 0.03166
```

Therefore:

```text
W2 STOPOVER ACTUATOR:
    PASS
```

The previous near-zero estimate and p=0.972 are superseded.

This means the corrected wigeon case is no longer
`LAMBDA_PASS_ACTUATOR_FAIL`. Under the frozen formal gates it is:

```text
LAMBDA_PASS_ACTUATOR_PASS
```

## 6. Secondary actuator diagnostics

Travel speed remains unsupported:

```text
log-speed slope = +0.002757
p = 0.417
```

Distance moderation also remains unsupported at the registered descriptive
level:

```text
direct endpoint-distance moderation:
    p = 0.0823

route-progress x endpoint-distance phase term:
    p = 0.252
```

Thus the corrected actuator picture is specific rather than omnibus:

```text
stopover:
    supported

between-staging travel speed:
    not supported

distance moderation:
    not supported
```

## 7. Cross-system interpretation

The source correction changes the biological story in a useful way.

The common response coordinate remains lambda, while a **recurrent waiting-time
actuator** is now prospectively supported in wigeon as well as being observed
in mule deer and barnacle geese. Movement-speed compensation is still not
portable across all systems.

The defensible synthesis is therefore no longer:

> common lambda but wholly system-specific actuators.

It is closer to:

> phase retention provides a common response coordinate; stopover/waiting is a
> recurrent correction actuator across distinct migrants, while speed and
> route-level contributions remain system-dependent.

Effect magnitudes should not be pooled across the very different ecological
intervals without an explicit scale map.

## 8. Measurement-error ceiling remains active

The corrected lambda is still a naive errors-in-variables estimator.

For the source-faithful transitions:

```text
observed predictor phase SD = 15.88 d
```

Under the simple equal-error, independent-error, true-lambda=1 stress model,
an error SD of about **7.94 d** would be sufficient in expectation to attenuate
the observed estimator to approximately 0.75.

That 7.94 d value is a stress threshold, **not an empirical error estimate**.

Therefore PAYOFF-B currently licenses:

- the corrected estimator-scale lambda;
- the registered primary W1 PASS;
- the registered W2 stopover PASS;
- the corrected source-faithful environmental reconstruction.

It does not yet license:

- a measurement-error-corrected biological lambda;
- the claim that latent lambda is below one after accounting for phase error;
- attributing cross-taxon lambda differences entirely to biology.

The next empirical task is source-backed phase-error calibration, especially
for the wigeon system.
