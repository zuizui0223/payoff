# PAYOFF-B Svalbard barnacle-goose ERA5 reliability replication

Frozen registration: **2026-09-24**  
ERA5 outcome opened after registration: **2026-09-24**

Status: **negative phase-retention / overshoot sign and stopover response reproduced under ERA5**.

## 1. Frozen target

The reliability test was restricted before ERA5 outcomes to the existing
Svalbard primary fixed transition:

```text
R2 -> R4
n transitions = 16
n individuals = 15
```

The POWER result was already known:

```text
lambda_hat = -0.106320907
stopover slope = -0.588996
```

No alternative Svalbard route was eligible for promotion after seeing ERA5.

## 2. Why anchor uncertainty does not change this estimand

The broader Svalbard reconstruction uses region-specific mean spring-onset
anchors for absolute phase interpretation.

For a fixed origin/destination transition, adding a constant to all origin
phase values or all destination phase values changes the regression intercept,
not the slope.

Therefore the ERA5 reliability lane uses:

```text
arrival phase
=
arrival DOY
-
source-specific annual onset anomaly
```

and does not use the uncertain absolute mean anchors.

## 3. Environmental reconstruction contract

Both POWER and ERA5 use the same phenology transform:

```text
baseline = 1982--2011
30 years per region

T_base = -0.25 * latitude + 13 C
daily GDU = max(Tmean - T_base, 0)
cumulative GDD from Jan 1
logistic cumulative-GDD fit
minimum R^2 = 0.95
spring onset = early positive maximum of logistic third derivative
annual anomaly = annual onset - source-specific regional mean
```

Independent replicate source:

```text
Open-Meteo ERA5 hourly 2 m temperature
GMT daily arithmetic means
nearest ERA5 grid cell
```

All four eligible regions passed all 30 annual fits.

## 4. POWER identity

The anomaly-only refit reproduces the frozen source result:

```text
POWER lambda_hat = -0.106320907
SE = 0.259474379
p versus lambda=1 = 2.01e-05

POWER stopover slope = -0.588995506
SE = 0.087602740
p = 9.73e-06
```

This passes the preregistered POWER identity and sample-size gates.

## 5. ERA5 result

On the same 16 R2->R4 transitions:

```text
ERA5 lambda_hat = -0.286983400
SE = 0.366875667
p versus lambda=1 = 0.000452

ERA5 stopover slope = -0.621530081
SE = 0.084175973
p = 3.44e-06
```

Thus the exact numerical lambda changes, but the biologically distinctive
feature is retained:

```text
lambda < 0
stable contraction with overshoot / sign reversal
```

The negative stopover response also reproduces.

## 6. Replicate disagreement

Across 4 regions x 30 years:

```text
paired region-year onset anomalies = 120

POWER--ERA5 anomaly disagreement SD
= 2.82594 d

equal-independent-replicate sensitivity scale
= 1.99824 d
```

This is an assumption-conditional sensitivity scale, not a gold-standard
measurement-error estimate.

## 7. Why the negative sign matters

Under the simple classical errors-in-variables model with

```text
true lambda = 1
independent additive predictor error
nonnegative error variance
```

the expected naive slope is attenuated from one toward zero but does not cross
below zero.

Therefore the replicated negative Svalbard lambda cannot be generated as the
large-sample expectation of that simple attenuation mechanism alone.

This does not prove a unique biological mechanism, but it makes Svalbard a
particularly useful boundary case for the measurement-error audit.

## 8. Three-flyway reliability consequence

The highlighted direct barnacle-goose transitions now all have independent
POWER-to-ERA5 reliability checks:

```text
Greenland R2 -> R3:
    lambda 0.131 -> 0.144
    stopover negative/support -> negative/support

Barents R1 -> R2:
    lambda 0.494 -> 0.515
    stopover negative/support -> negative/support

Svalbard R2 -> R4:
    lambda -0.106 -> -0.287
    stopover negative/support -> negative/support
```

The full controller magnitudes are not universal, but both phase transformation
and the stopover actuator are robust to this environmental-source substitution
in all three highlighted barnacle-goose flyways.

## 9. Machine result

Registration:

```text
data/svalbard_barnacle_phase_error_era5_registration_20260924.json
```

Result:

```text
data/svalbard_barnacle_era5_reliability_result_20260924.json
```

Execution:

```text
workflow run = 35975472359
artifact = 10796909675
artifact SHA256 =
6155a9efe854167883190db7410ce60c151721e4569d564f23bc01a555013825
```

The Aikens lambda outcome remained unopened.
