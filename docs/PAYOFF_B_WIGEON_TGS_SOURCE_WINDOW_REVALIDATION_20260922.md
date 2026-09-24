# PAYOFF-B wigeon TGS source-window revalidation amendment

Frozen: **2026-09-22**

Status: **old wigeon lambda suspended pending source-faithful reconstruction**.

## Source audit

The published environmental preparation code for van Toor et al. (2021)
constructs the daily TGS input only after:

```r
days <- days[month(days)<8]
```

and then applies the 5 C cumulative-minimum rule.

Published supplementary source:

`Additional file 3: Environmental data preparation`

https://media.springernature.com/original/springer-static/esm/art%3A10.1186%2Fs40462-021-00296-0/MediaObjects/40462_2021_296_MOESM3_ESM.html

## Difference found in PAYOFF-B reconstruction

The promoted NASA POWER reconstruction had applied the same cumulative-minimum
rule to the **full calendar year**.

That difference matters in cold northern cell-years. When the cumulative
temperature anomaly continues falling into autumn/winter, the full-year
minimum can occur on day 365 or 366. Such a value is then misread as a thermal
growing-season onset and can create arrival phases near -200 d.

The existing workflow artifact contains these end-of-year TGS values, so this
is not a hypothetical edge case.

## Immediate claim action

The previously promoted result

```text
lambda_hat = 0.85994
SE = 0.04509
p versus naive lambda=1 = 0.00190
n transitions = 224
n individuals = 28
```

is now:

```text
SUPERSEDED_PENDING_SOURCE_FAITHFUL_RECONSTRUCTION
```

It must not be used as prospective cross-system support until the Jan-Jul
reconstruction is complete.

This amendment was frozen before inspecting the corrected lambda.

## What remains unchanged

The correction changes only the environmental input window.

Unchanged:

- original movement source and HMM reconstruction;
- staging-event definition;
- 5 C TGS threshold;
- cumulative-minimum TGS rule;
- phase-controller model;
- route-progress and endpoint-distance covariates;
- individual-clustered uncertainty;
- environmental validation gates;
- stronger-forecast and actuator logic;
- Aikens preregistration and unopened outcome.

No corrected-result threshold may be tuned after the new lambda is observed.

## Relationship to measurement-error audit

The source-window problem is upstream of the new errors-in-variables analysis.

The order is now:

```text
source-faithful Jan-Jul TGS reconstruction
-> corrected naive lambda
-> observed predictor-phase variance
-> source-backed measurement-error calibration
-> true-lambda=1 observation-error null
```

Measurement-error correction must not be used to rescue a result generated from
a source-inconsistent TGS reconstruction.
