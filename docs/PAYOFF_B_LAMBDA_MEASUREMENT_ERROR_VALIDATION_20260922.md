# PAYOFF-B lambda measurement-error validation

Frozen: **2026-09-22**

Status: **pre-Aikens-outcome validation layer; wigeon replicate calibration and SIMEX v2 complete, cross-taxon reliability incomplete**.

## Why this layer exists

The GEB programme estimates phase retention from

```text
E_next = a + lambda E_current + error.
```

The existing migration–phenology tracking model provides a direct generating
interpretation. After one local correction step with migration rate `m` and
phenology rate `h`,

```text
lambda_true = exp[-(m+h) dt].
```

This makes the simulation useful for the GEB paper in a narrower and more
important role than another large ecological parameter sweep: **validate the
observation and estimation layer when true lambda is known**.

## Regression dilution is a first-order risk

Let latent incoming phase have variance `Vx`. Let the phase estimates at the
start and end of a correction interval contain errors `u` and `v`. Under the
frozen additive model,

```text
E_current_obs = E_current_true + u
E_next_obs    = E_next_true    + v
```

and the large-sample naive slope is

```text
E[lambda_hat]
=
(lambda_true * Vx + Cov(u,v))
/
(Vx + Var(u)).
```

For independent errors, `Cov(u,v)=0`, so the slope is attenuated toward zero.
For latent phase SD 10 d and equal independent measurement-error SDs, the
analytic reference grid is:

| true lambda | error SD 0 d | 3 d | 6 d | 10 d |
| ---: | ---: | ---: | ---: | ---: |
| 0.10 | 0.100 | 0.092 | 0.074 | 0.050 |
| 0.50 | 0.500 | 0.459 | 0.368 | 0.250 |
| 0.86 | 0.860 | 0.789 | 0.632 | 0.430 |
| 1.00 | 1.000 | 0.917 | 0.735 | 0.500 |

Therefore a naive estimate below one is not, by itself, sufficient evidence
against a no-correction latent process when the predictor phase is measured
with error.

## Correlated phase errors matter

The independent-error case is not automatically appropriate. Consecutive phase
estimates may share environmental reconstruction error. If start and end phase
errors are positively correlated, the attenuation is weaker because
`Cov(u,v)>0`.

For the special case

```text
lambda_true = 1
latent phase SD = 10 d
start error SD = end error SD = 10 d
```

the expected naive slope is:

```text
rho(error_start,error_end)=0 -> 0.50
rho(error_start,error_end)=1 -> 1.00
```

So a defensible lambda=1 null must specify not only error magnitude but also
its consecutive-observation correlation.

## What is frozen now

Implemented:

- exact tracking-rate to latent-lambda bridge;
- analytic attenuation expectation;
- seed-explicit Monte Carlo recovery;
- true-lambda=1 lower-tail null comparison;
- errors-in-variables correction when error moments are independently known;
- tests reproducing the 0/3/6/10 d reference attenuation table.

Frozen registry entries carry the actual empirical sample sizes and ecological
intervals already used by the direct systems.

Current empirical calibration state:

### Eurasian wigeon — source-backed sensitivity complete

A separately frozen source-faithful ERA5 hourly reconstruction now covers all
256/256 staging events and all 224 controller transitions. On the identical
transitions:

```text
POWER lambda_hat = 0.749768
ERA5  lambda_hat = 0.811312
```

POWER-versus-ERA5 phase disagreement has SD 7.086 d. Under the equal-independent-
replicate sensitivity interpretation this corresponds to 5.010 d per replicate;
the observed consecutive discrepancy correlation is 0.3666.

The complete event-structure SIMEX v2 gives frozen extrapolations:

```text
0.7979 .. 0.9354
```

and all three frozen scenarios remain below one. These values are **sensitivity
diagnostics, not corrected truth**, because replicate disagreement does not
identify a gold-standard source-specific measurement-error distribution.

Sources:

```text
data/wigeon_era5_sourcefaithful_calibration_result_20260924.json
data/wigeon_phase_simex_era5_complete_result_20260924.json
```

The earlier registered ERA5-Land lane remains a coverage failure at 220/256
events and is not retroactively repaired.

### Barnacle goose — two preregistered replicate calibrations complete

A separately frozen ERA5 reconstruction repeated the exact POWER GDD-jerk
phenology transform over the same 1982--2013 baseline for two transitions chosen
before ERA5 outcomes were opened.

```text
Greenland R2 -> R3
    POWER lambda_hat = 0.130731
    ERA5  lambda_hat = 0.144204
    ERA5 - POWER     = +0.013473

    POWER stopover slope = -0.5242, p=0.00339
    ERA5  stopover slope = -0.3789, p=0.00802

Barents R1 -> R2
    POWER lambda_hat = 0.494114
    ERA5  lambda_hat = 0.515329
    ERA5 - POWER     = +0.021215

    POWER stopover slope = -0.5915, p=0.000988
    ERA5  stopover slope = -0.5738, p=0.000995
```

The corresponding POWER--ERA5 region-year onset-anomaly disagreement SDs are
4.227 d (Greenland) and 2.839 d (Barents). Their equal-independent-replicate
sensitivity scales are 2.989 d and 2.007 d respectively.

These values are assumption-conditional replicate calibrations, not
source-specific gold-standard measurement-error distributions. Svalbard remains
outside this lane because it uses a separate anchor-sensitive construction.

Source:

```text
data/barnacle_era5_reliability_result_20260924.json
docs/PAYOFF_B_BARNACLE_ERA5_RELIABILITY_20260924.md
```

### Mule deer and Svalbard goose — source-specific error still pending

For mule deer and the Svalbard direct transition, source-backed predictor phase
error distributions and consecutive-error correlations have not yet been
identified.

Consequently:

```text
three-taxon estimator-scale lambda coordinate:
    LICENSED

wigeon assumption-conditional replicate calibration:
    COMPLETE

barnacle Greenland/Barents assumption-conditional replicate calibration:
    COMPLETE

source-specific measurement-error identification for all taxa:
    INCOMPLETE

cross-taxon latent biological lambda magnitude comparison:
    HOLD
```

This separation is machine-enforced by
`src/cross_system_lambda_reliability.py`.

## Why environmental innovation SD cannot fill this field

The existing barnacle-goose `environmental_innovation_sd_days` measures
unpredictable downstream environmental timing after conditioning on the origin.
It is a biological process-noise term.

It is **not** uncertainty in the reconstructed phase coordinate and therefore
must not be substituted for measurement-error SD.

## Confirmatory sequence

Before changing the GEB contraction claim:

```text
1. freeze source-backed uncertainty estimator for each direct system
2. estimate predictor phase variance + measurement-error moments
3. run taxon/route-specific recovery at the observed n and interval
4. simulate true lambda = 1 under exactly the same observation model
5. compare observed lambda_hat with that null
6. only then consider EIV / SIMEX corrected values
```

No error SD or correlation may be tuned after comparing the simulated null with
the observed lambda.

## Aikens boundary

The Aikens lambda outcome remains unopened at this freeze.

The registered Aikens primary contrast is not replaced by a measurement-error
corrected analysis. The recovery layer is a parallel validation/sensitivity
layer whose calibration rules are frozen before the primary outcome is opened.

## Separation from the tracking-theory paper

The coevolution, finite-N, 2D landscape and demographic tracking simulations
remain a separate theoretical programme. They should not be expanded merely to
increase run count for the GEB paper.

For GEB, the simulation has one focused role:

> **Can the estimator recover lambda, and can a true no-correction process look
> like contraction under the actual observation process?**
