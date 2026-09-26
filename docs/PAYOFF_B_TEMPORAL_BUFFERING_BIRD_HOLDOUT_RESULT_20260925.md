# PAYOFF-B temporal-buffering bird holdout result

Frozen: **2026-09-25**  
Registration: `payoff_b_temporal_buffering_bird_holdout_v1_20260925`  
Result: **FAIL_WRONG_DIRECTION**

Machine receipt:

`data/payoff_b_temporal_buffering_bird_holdout_result_20260925.json`

## Registered prediction

Using 2002–2009 only, estimate species-level timing responsiveness of arrival
date to green-up timing. Then ask in the independent 2010–2017 holdout whether
species with greater historical timing responsiveness have a flatter
mismatch-versus-speed-ratio curve.

Registered primary parameter:

```text
I(log_speed_ratio^2) × z_timing_gain
```

Prediction:

```text
coefficient < 0
```

Support required correct direction and p < 0.05.

## Sample

```text
calibration = 2002–2009
holdout = 2010–2017
timing-gain eligible species = 39
holdout species = 39
holdout rows = 3,268
holdout years = 8
estimability gate = PASS
```

## Primary result

```text
beta_q2_x_timing_gain = +0.03506
SE = 0.02889
t = 1.214
p = 0.2249
registered direction = negative
classification = FAIL_WRONG_DIRECTION
```

The registered natural-data substitution prediction therefore failed. Species
with stronger historical timing responsiveness did **not** show weaker later
dependence of phase mismatch on the movement-speed ratio.

No alternate chronological split, timing-gain definition, trait set, response,
quadratic term or support threshold is licensed.

## Secondary descriptive pattern

The same frozen model contains a descriptive timing-gain main effect:

```text
z_timing_gain = -0.300 ± 0.105
p = 0.0043
```

Thus historically more timing-responsive species had lower holdout phase
deviation on average, conditional on the frozen model covariates.

This term was **not** the registered primary hypothesis and cannot be promoted
to a replacement confirmatory result.

The fitted quadratic curvature was:

```text
z_timing_gain = -1: 0.0262
z_timing_gain = +1: 0.0963
```

The interaction uncertainty is too large to turn this opposite-signed pattern
into a positive claim that timing and movement are complementary.

## Ecological interpretation

The natural holdout result does not support a simple substitution story in
which historical timing flexibility makes later movement-speed matching less
important.

Combined with the synthetic result, the licensed conclusion is narrower and
clearer:

> **Timing can improve environmental tracking, but the natural-data holdout
> provides no evidence that timing responsiveness substitutes for spatial
> tracking.**

The synthetic moving landscapes still establish finite temporal buffering and
later spatial re-entry within the declared model. The archived bird result now
places an empirical ceiling on extrapolation: latent spatial tracking demand is
a mechanistic interpretation of the synthetic system, not a quantity already
demonstrated across natural bird species.

This failed registered test must remain visible in the integrated manuscript if
the temporal-buffering mechanism remains the headline.

## Provenance

```text
workflow_run = 36122102742
artifact_id = 10857712843
artifact_sha256 = a0147a378927b3fdc29fac790bc606ddb7d2c64ff23875592ce04f98eb446a0f
retuning_permitted = false
```
