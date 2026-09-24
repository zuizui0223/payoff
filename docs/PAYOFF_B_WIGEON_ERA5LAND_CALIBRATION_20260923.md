# PAYOFF-B wigeon ERA5-Land phase-error calibration — run 4

Frozen: **2026-09-23**

Status: **REGISTERED CALIBRATION FAIL; informative measurement-error sensitivity retained separately**.

## Registered outcome

The preregistered POWER-versus-ERA5-Land event-level replication reached:

```text
paired events:        220 / 256
paired fraction:      0.859375
minimum events:       200       PASS
minimum fraction:     0.90      FAIL

published-phase validation:
    PASS

full-224 POWER identity:
    PASS
```

Therefore the registered calibration is **FAIL**. The 0.90 event-coverage
threshold is not relaxed.

## What the incomplete calibration nevertheless shows

Across the 220 paired events:

```text
ERA5-Land phase - POWER phase
mean     = 2.014 d
median   = 0 d
SD       = 5.434 d
IQR      = 0 .. 2 d
2.5--97.5% = -6.1 .. 18 d
```

On the identical 181 complete staging transitions:

```text
POWER lambda_hat      = 0.83796
ERA5-Land lambda_hat  = 0.86516
difference            = +0.02720
```

So the two environmental reconstructions give similar phase-retention slopes on
the common paired subset.

## True-lambda=1 sensitivity

These simulations do **not** repair the failed calibration. They ask how easily
the observed full-sample naive lambda could arise from a latent
`lambda_true=1` process under explicitly declared replicate-error assumptions.

### Equal independent replicate interpretation

```text
error SD = disagreement SD / sqrt(2)
         = 3.842 d

null mean lambda_hat = 0.9304
null 2.5% quantile   = 0.8257
P(lambda_hat <= 0.749768 | true lambda=1)
    = 0.000300
```

### Equal-replicate correlation proxy

Using the observed consecutive discrepancy correlation `rho=0.2881`:

```text
null mean lambda_hat = 0.9512
null 2.5% quantile   = 0.8538
lower-tail probability
    = 0.000100
```

### Deliberately conservative full-disagreement scale

Treating the entire POWER--ERA5-Land disagreement SD, 5.434 d, as the error SD:

```text
null mean lambda_hat = 0.8619
null 2.5% quantile   = 0.74839
observed lambda_hat  = 0.74977
lower-tail probability
    = 0.0266
```

This is the stress boundary: the observed wigeon estimate lies almost exactly
at the lower 2.5% edge of this deliberately conservative null.

## Interpretation

The current evidence does **not** license a final measurement-error-corrected
wigeon lambda because the registered replicate calibration failed its coverage
gate.

It does show that the source-faithful `lambda_hat=0.749768` is not trivially
explained by the amount of POWER--ERA5-Land disagreement observed in the 220
paired events. Even the full-disagreement sensitivity produces a lower-tail
probability of about 0.027.

The next question is why 36 registered nearest-cell ERA5-Land queries returned
HTTP 200 but no finite Jan--Jul daily values. Because ERA5-Land masks oceans
and many missing events lie near coasts, a separate post-hoc land-cell diagnostic
is now run **without changing the registered nearest-cell calibration**.

## Claim ceiling

Licensed:

- registered calibration coverage FAIL;
- the paired-event disagreement distribution;
- paired-subset POWER and ERA5-Land lambda comparison;
- explicitly labeled incomplete-calibration true-lambda=1 sensitivities.

Not licensed:

- calling the registered calibration PASS;
- replacing the registered `nearest` grid-cell rule after seeing the outcome;
- a gold-standard error SD;
- a final corrected latent lambda;
- using the post-hoc land-cell diagnostic to retroactively satisfy the primary gate.

Machine receipt:

`data/wigeon_era5land_calibration_result_20260923.json`.
