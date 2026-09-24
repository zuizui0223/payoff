# PAYOFF-B barnacle-goose ERA5 reliability replication

Frozen registration: **2026-09-24**  
ERA5 outcome opened after registration: **2026-09-24**

Status: **two preregistered fixed-transition reconstructions reproduced across POWER and ERA5; replicate disagreement is sensitivity evidence, not corrected truth**.

## 1. Why this analysis was added

The PAYOFF-B GEB programme compares phase retention through

```text
E_next = a + lambda E_current + error.
```

After the wigeon source audit showed that environmental reconstruction can alter
both lambda magnitude and actuator inference, the same reliability question was
asked for the existing barnacle-goose direct systems.

Only two transitions were selected before ERA5 outcomes were opened:

```text
Greenland R2 -> R3
Barents   R1 -> R2
```

No additional transition may be promoted from this ERA5 exercise after seeing
its result.

## 2. Frozen reconstruction contract

Source movement / POWER artifact:

```text
PR #144
branch:
  empirical/movement-phenology-macro-20260918

workflow run:
  35742152966

artifact:
  10700391090
  movement-phenology-barnacle-multiflyway

artifact SHA256:
  8e720be44e0ef2e3e497786c9241c6625b4b14c46506fbb30ea027dcdf36749f
```

Replicate environmental source:

```text
Open-Meteo Historical Weather API
ERA5 hourly 2 m temperature
GMT daily arithmetic mean
nearest provider grid cell
no API key
```

Phenology transform is identical for POWER and ERA5:

```text
1982--2013 baseline
T_base = -0.25 * latitude + 13 C
daily GDU = max(Tmean - T_base, 0)
cumulative GDD from January 1
logistic cumulative-GDD fit
R^2 >= 0.95
spring onset = early positive maximum of logistic third derivative
annual anomaly = annual onset - source-specific region mean onset
```

For a fixed origin/destination region pair, the unknown regional mean onset
changes the intercept but not the lambda slope.

## 3. Greenland R2 -> R3

Frozen POWER identity:

```text
n transitions = 6
n individuals = 6

POWER lambda_hat = 0.1307308835
SE = 0.0828436927
p versus lambda=1 = 9.31e-26

POWER stopover slope = -0.5241744704
p = 0.00339
```

Independent ERA5 reconstruction:

```text
ERA5 lambda_hat = 0.1442035301
SE = 0.0586163474
p versus lambda=1 = 2.81e-48

ERA5 stopover slope = -0.3789417683
p = 0.00802
```

Difference:

```text
ERA5 - POWER lambda_hat = +0.0134726466
```

All four eligible regions had all 32 baseline years successfully reconstructed.

Region-year POWER--ERA5 onset-anomaly disagreement:

```text
SD = 4.22687 d

equal-independent-replicate sensitivity scale:
SD / sqrt(2) = 2.98885 d
```

## 4. Barents R1 -> R2

Frozen POWER identity:

```text
n transitions = 12
n individuals = 8

POWER lambda_hat = 0.4941139415
SE = 0.1293528584
p versus lambda=1 = 9.20e-05

POWER stopover slope = -0.5914512617
p = 0.000988
```

Independent ERA5 reconstruction:

```text
ERA5 lambda_hat = 0.5153286022
SE = 0.1285807992
p versus lambda=1 = 0.000164

ERA5 stopover slope = -0.5738036992
p = 0.000995
```

Difference:

```text
ERA5 - POWER lambda_hat = +0.0212146607
```

All six eligible regions had all 32 baseline years successfully reconstructed.

Region-year POWER--ERA5 onset-anomaly disagreement:

```text
SD = 2.83895 d

equal-independent-replicate sensitivity scale:
SD / sqrt(2) = 2.00744 d
```

## 5. What replicated

For both preregistered transitions:

```text
phase-retention contraction:
    POWER -> ERA5
    REPLICATED

negative stopover response:
    POWER -> ERA5
    REPLICATED
```

The lambda shifts are small relative to the differences among the highlighted
direct systems.

This differs from the wigeon reliability result, where lambda contraction
reproduced under POWER and ERA5 but the POWER stopover association did not.

The current empirical pattern is therefore:

```text
response-coordinate reliability:
    system dependent in magnitude
    but qualitatively replicated in tested wigeon and barnacle lanes

actuator reliability:
    barnacle highlighted transitions -> replicated
    wigeon stopover -> reconstruction-sensitive
```

## 6. Measurement-error interpretation

POWER--ERA5 disagreement is a **replicate disagreement distribution**.

It is not:

- a gold-standard measurement-error distribution;
- proof that either POWER or ERA5 is unbiased;
- a license to report one corrected latent lambda.

For the recovery registry, the equal-independent-replicate values

```text
Greenland = 2.98885 d
Barents   = 2.00744 d
```

are therefore recorded only as assumption-conditional sensitivity scales.

Svalbard remains outside this ERA5 replication lane and retains its separate
anchor-sensitive reconstruction.

## 7. Consequence for the cross-system claim

The strengthened claim is:

> A common phase-retention coordinate is not merely a consequence of one
> environmental product. In wigeon, contraction reproduces under POWER and
> ERA5 while one proposed actuator does not; in two preregistered
> barnacle-goose transitions, both phase retention and stopover response are
> stable across the same environmental-source substitution.

This supports treating **response coordinate, actuator, and reliability state
as separate empirical layers**.

It still does not license:

- one universal latent lambda;
- a corrected cross-taxon ranking of lambda magnitude;
- one universal actuator;
- treating route rows as independent taxa.

## 8. Machine result

```text
data/barnacle_phase_error_era5_registration_20260924.json
data/barnacle_era5_reliability_result_20260924.json
```

Execution:

```text
workflow run:
    35974167089

artifact:
    10797665905

artifact SHA256:
    c37502b116f4170760e0fbf5029fe1804999def4de3f702cdb5bf61e61b8606f
```

The Aikens lambda outcome remained unopened throughout this analysis.
