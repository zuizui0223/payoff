# PAYOFF-B Eurasian wigeon source-faithful revalidation

Frozen source-window amendment: **2026-09-22**  
Corrected workflow result: **2026-09-22**

Status: **source-faithful POWER result retained; complete ERA5 reliability audit and SIMEX v2 completed**.

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

The preregistered primary W2 prediction was directional:

    S'(E) < 0.

No fixed p-value threshold was preregistered. A secondary magnitude forecast
was frozen separately:

    0.3 < g_S < 0.8.

Under the registered POWER phase surface:

    slope = -0.062863 d / phase-day
    cluster SE = 0.027739
    conventional clustered p = 0.03166.

Therefore the frozen POWER directional W2 gate passes. The secondary gain band
fails because g_S=0.062863.

This remains the correct prospective outcome for the registered POWER analysis.

A separately frozen source-faithful ERA5 reconstruction provides an independent
robustness test, not a rewrite of that preregistration. On the same 224
transitions:

    ERA5 stopover slope = -0.024182 d / phase-day
    clustered p = 0.3104.

Thus the POWER stopover association is not replicated under ERA5. The current
interpretation distinguishes:

    registered POWER W2 directional gate:
        PASS

    independent ERA5 actuator replication:
        NOT SUPPORTED

    reconstruction-robust wigeon stopover mechanism:
        NOT ESTABLISHED.

## 6. Secondary actuator diagnostics

Travel speed remains unsupported under both environmental reconstructions.

POWER:

    log-speed slope = +0.002757
    p = 0.417.

ERA5:

    log-speed slope = +0.004076
    p = 0.248.

Distance moderation remains unsupported at the registered descriptive level in
the POWER analysis.

The wigeon actuator picture is therefore reconstruction-sensitive: the POWER
phase surface supports a negative stopover response, whereas the ERA5 phase
surface does not; travel speed is unsupported in both.

## 7. Cross-system interpretation

The common response coordinate remains lambda, but the complete ERA5 follow-up
changes the actuator story.

Phase retention is reproduced across the two wigeon environmental surfaces:

    POWER lambda_hat = 0.749768
    ERA5  lambda_hat = 0.811312.

Both estimates are below one on the identical 224 transitions.

By contrast, the stopover association is supported only under POWER. This makes
wigeon a direct demonstration of why PAYOFF-B separates a response-coordinate
gate from actuator-specific gates.

The defensible synthesis is:

> phase retention provides a common response coordinate; actuator inference is
> less portable and can depend on the environmental phase reconstruction.

This no longer licenses a claim that stopover/waiting is robustly recurrent
across all three taxa, although stopover compensation remains strong in mule
deer and barnacle geese and is prospectively detected in the registered POWER
wigeon analysis.

## 8. Measurement-error calibration and SIMEX v2

The corrected POWER lambda is a naive errors-in-variables estimator.

A first registered ERA5-Land calibration failed its frozen coverage gate at
220/256 events and remains a formal FAIL.

A separately frozen source-faithful ERA5 hourly follow-up then achieved:

    256 / 256 paired events
    224 / 224 complete transitions
    coverage gate PASS
    published phase validation PASS
    POWER identity PASS.

Across all paired events:

    ERA5 - POWER phase median = 1 d
    disagreement SD = 7.086 d
    equal-independent replicate sensitivity SD = 5.010 d
    consecutive discrepancy correlation = 0.3666.

On the identical 224 transitions:

    POWER lambda_hat = 0.749768
    ERA5  lambda_hat = 0.811312.

True-lambda=1 sensitivities are assumption-dependent:

    equal-independent replicate scale:
        lower-tail p = 0.00990

    discrepancy-correlation proxy:
        lower-tail p = 0.000500

    conservative full-disagreement-as-each-source-error:
        lower-tail p = 0.40086.

The complete-calibration event-structure SIMEX v2 gives:

    equal-independent replicate:
        lambda_SIMEX = 0.8412

    discrepancy-correlation proxy:
        lambda_SIMEX = 0.7979

    conservative full disagreement:
        lambda_SIMEX = 0.9354.

All frozen SIMEX v2 values are above the naive 0.7498 estimate and below one.
However, the conservative scenario approaches complete retention, demonstrating
material uncertainty in correction magnitude.

Therefore PAYOFF-B currently licenses:

- the registered POWER W1 PASS;
- estimator-scale contraction independently reproduced under ERA5;
- the registered POWER W2 directional PASS as a source-specific prospective
  result;
- explicit reconstruction sensitivity of the wigeon stopover association;
- complete-calibration measurement-error sensitivity.

It does not license:

- one uniquely corrected biological lambda;
- a reconstruction-robust wigeon stopover mechanism;
- attributing cross-taxon lambda magnitude differences entirely to biology.

Primary reliability receipts:

    data/wigeon_era5_sourcefaithful_calibration_result_20260924.json
    docs/PAYOFF_B_WIGEON_ERA5_SOURCEFAITHFUL_CALIBRATION_20260924.md
    data/wigeon_phase_simex_era5_complete_result_20260924.json
    docs/PAYOFF_B_WIGEON_ERA5_SIMEX_V2_20260924.md.
