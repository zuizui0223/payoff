# PAYOFF-B wigeon source-faithful ERA5 calibration

Frozen contract: **2026-09-24**  
Workflow: **35941774903**  
Status: **COMPLETE — 256/256 event coverage**.

## Why this is a separate lane

The prior registered replicate used ERA5-Land and failed its frozen 90% event
coverage gate (220/256 events). That failure is retained.

The original wigeon paper describes hourly **ERA5** 2 m temperature, not
ERA5-Land. Before opening this follow-up result, PAYOFF-B froze a new independent
lane using Open-Meteo's explicit ERA5 model, hourly temperature, GMT daily
aggregation, the published January--July window, and the same TGS/controller
rules.

This is a new source-faithful follow-up; it does not retroactively convert the
ERA5-Land calibration to PASS.

## Coverage and source validation

```text
paired events:             256 / 256
paired fraction:           1.000
complete transitions:      224 / 224
coverage gate:             PASS
POWER lambda identity:     PASS
ERA5 TGS >= day 300:       0
```

ERA5 arrival-phase validation:

```text
median = 23.96 d
Q1     = 15.16 d
Q3     = 38.88 d

published:
median = 22.5 d
Q1     = 13.0 d
Q3     = 35.3 d
```

All registered phase-validation checks pass.

## Replicate disagreement

For all 256 events:

```text
ERA5 phase - POWER phase

mean     = 3.418 d
median   = 1.0 d
SD       = 7.086 d
IQR      = 0 .. 8 d
2.5--97.5% = -14.5 .. 19 d
```

The equal-independent-replicate sensitivity scale is:

```text
7.0855 / sqrt(2) = 5.0102 d
```

The consecutive origin--destination discrepancy correlation is:

```text
r = 0.3666
p = 1.56e-08
```

These are replicate-disagreement quantities, not a gold-standard source-specific
measurement-error distribution.

## Lambda reproduces across the two environmental surfaces

On the exact same 224 transitions:

```text
POWER:
    lambda_hat = 0.74977
    SE         = 0.04991
    naive p(lambda=1) = 5.33e-07

ERA5:
    lambda_hat = 0.81131
    SE         = 0.04478
    naive p(lambda=1) = 2.51e-05

ERA5 - POWER lambda_hat = +0.06154
```

Thus the numeric coefficient is reconstruction-sensitive, but the estimator-
scale contraction is reproduced by the environmental dataset family used in the
original study.

## The actuator result is less portable than lambda

POWER reconstruction:

```text
stopover slope = -0.06286
p = 0.0317
```

ERA5 reconstruction:

```text
stopover slope = -0.02418
p = 0.310
```

Travel-speed response is unsupported in both reconstructions.

Therefore the defensible wigeon statement is now:

> phase-retention contraction replicates across POWER and ERA5, but the
> stopover-actuator evidence is sensitive to the environmental phase surface.

This is stronger support for the lambda coordinate and weaker support for a
recurrent wigeon stopover mechanism.

## True-lambda=1 observation-error sensitivity

Using the full 224-transition POWER signal and process-noise scales:

| scenario | error SD | rho | P(lambda_hat <= 0.74977 | true lambda=1) | EIV sensitivity |
| --- | ---: | ---: | ---: | ---: |
| equal independent replicates | 5.010 d | 0 | 0.00990 | 0.849 |
| equal-replicate correlation proxy | 5.010 d | 0.367 | 0.000500 | 0.801 |
| full disagreement as each-source error | 7.086 d | 0 | 0.40086 | 0.980 |

The first two frozen replicate-error interpretations make the observed naive
coefficient unusual under true lambda=1. The deliberately conservative third
scenario does not.

Accordingly, the calibration does **not** identify one corrected true lambda.
It does identify the assumption boundary at which the no-correction latent
process becomes plausible.

## Claim ceiling

Licensed:

- complete 256-event POWER-versus-ERA5 replicate calibration;
- source-faithful ERA5 phase validation;
- same-transition lambda comparison;
- estimator-scale contraction under both POWER and ERA5;
- reconstruction sensitivity of the wigeon stopover association;
- explicitly assumption-conditional true-lambda=1 sensitivity.

Not licensed:

- a gold-standard measurement-error SD;
- one definitive corrected latent lambda;
- claiming the POWER stopover actuator replicated under ERA5;
- changing or erasing the old ERA5-Land registered FAIL;
- any change to the still-unopened Aikens lambda outcome.
