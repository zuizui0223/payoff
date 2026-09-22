# PAYOFF-B lambda measurement-error validation

Frozen: **2026-09-22**

Status: **pre-Aikens-outcome validation layer**.

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

Not yet filled:

- empirical predictor phase SD;
- predictor measurement-error SD;
- outcome measurement-error SD;
- start/end error correlation.

Those fields remain `PENDING_SOURCE_BACKED_CALIBRATION`.

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
