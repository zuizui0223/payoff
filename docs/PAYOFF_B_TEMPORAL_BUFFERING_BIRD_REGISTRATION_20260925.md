# PAYOFF-B temporal-buffering bird holdout registration

Frozen: **2026-09-25**  
Status: **FROZEN BEFORE HOLDOUT READOUT**

Machine contract:

`data/payoff_b_temporal_buffering_bird_holdout_registration_20260925.json`

## Question

The integrated PAYOFF-B paper now makes one ecological mechanism primary:

> **Temporal adjustment can buffer spatial tracking demand, but cannot replace
> movement indefinitely under sustained environmental change.**

The existing 55-species analysis rejects one universal movement-speed rule but
does not directly test whether historical timing responsiveness moderates later
dependence on movement speed.

This fresh archived-data test asks:

> **Do species that historically adjust arrival timing more strongly to green-up
> show a flatter mismatch-versus-speed-ratio relationship in later years?**

A flatter later relationship is the natural-data signature expected if timing
can absorb part of the tracking burden that would otherwise be expressed
through movement speed.

## Response-blind chronological split

Unique observed calendar years are sorted ascending.

```text
calibration = first floor(n_years / 2) unique years
holdout     = all remaining later years
```

The split rule is frozen before year counts are inspected. Metadata-only
preflight may report year/species/cell coverage but may not inspect arrival
mismatch, migration speed, speed ratio or any fitted response relationship.

## Calibration-only timing responsiveness

For each species:

1. estimate a calibration mean arrival date within each species × cell;
2. estimate a calibration mean green-up date within each cell;
3. define arrival and green-up anomalies relative to those calibration means;
4. fit `arrival_anomaly ~ greenup_anomaly`;
5. retain the green-up slope as the species timing gain.

Species eligibility is frozen at:

- >=60 calibration observations;
- >=5 calibration cells;
- >=5 calibration years;
- finite timing-gain slope.

The timing gain is standardized across eligible species using calibration-only
mean and SD.

No migration-speed variable is allowed into the calibration timing-gain model.

## Holdout response

For each eligible species × cell, calibration years define the baseline phase:

```text
baseline_lag = mean(arrival date - green-up date)
```

requiring >=3 calibration observations.

For later holdout years:

```text
holdout phase deviation
    = (arrival date - green-up date) - calibration baseline_lag

response
    = |holdout phase deviation|
```

Thus the holdout response is not used to estimate timing responsiveness.

## Primary model

The frozen primary model is:

```text
abs_lag_deviation_holdout ~
    log_speed_ratio
  + log_speed_ratio^2
  + z_timing_gain
  + log_speed_ratio × z_timing_gain
  + log_speed_ratio^2 × z_timing_gain
  + log_speed_scale
  + alignment
  + cell_latitude
  + greenup_date_anomaly_from_calibration
  + migration-cell flag
  + breeding-cell flag
  + species random intercept
  + species×cell random intercept
  + year random intercept
```

Primary parameter:

```text
beta_q2_x_timing_gain
```

Prediction:

```text
beta_q2_x_timing_gain < 0
```

because greater timing responsiveness should flatten the later mismatch curve
along the movement-speed axis.

Support requires both:

```text
coefficient < 0
p < 0.05
```

## Estimability gate

The result is `NOT_ESTIMABLE` if any of the following fail:

- >=15 eligible species;
- >=1000 holdout observations;
- >=5 holdout years;
- positive SD among calibration timing-gain slopes;
- successful frozen model fit.

No threshold may be relaxed after preflight or readout.

## Interpretation

This is a **fresh split-sample secondary test in an archived dataset**, not part
of the original Amaral Stage-1 confirmatory family.

It can strengthen the natural-data connection to temporal buffering, but even a
PASS does not directly estimate “latent spatial tracking demand” as a state
variable.

A failure does not reopen the synthetic mechanism result or license alternative
splits, traits or models.
