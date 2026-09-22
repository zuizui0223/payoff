# Eurasian-wigeon direct phase-retention receipt

Status: **source-faithful third-taxon revalidation complete; measurement-error calibration pending**.

Primary source: van Toor et al. (2021), *Movement Ecology* 9:61, DOI 10.1186/s40462-021-00296-0.

Tracking source: Movebank DOI 10.5441/001/1.dv5mm289.

Environmental source: NASA POWER daily T2M used as an independent reconstruction of the published ERA5-based thermal-growing-season analysis.

## Source-faithfulness correction

A 2026-09-22 audit of Additional file 3 recovered a preprocessing step that
had been omitted from the first POWER reconstruction. The published code
restricts the temperature series before estimating TGS:

```r
days <- days[month(days)<8]
```

so TGS is estimated from **January through July**, not the full calendar year.

The earlier full-year reconstruction could place the cumulative minimum at
day 365/366 in cold northern cell-years, producing artificial phase values near
-200 d. That result is superseded.

The movement source, HMM, staging reconstruction, controller formula,
route covariates, and individual clustering were unchanged.

## Movement reconstruction gate

```text
reconstructed spring trajectories = 33
reconstructed individuals         = 29

published trajectories            = 35
published individuals             = 31

reconstructed median endpoint distance = 1911 km
published median endpoint distance     = 1899 km
```

All registered movement gates pass.

## Source-faithful environmental validation

```text
staging events total          = 256
events with reconstructed TGS = 256
TGS onset >= day 300          = 0

arrival phase median = 21.97 d
Q1 / Q3             = 13.18 / 34.25 d

published median    = 22.5 d
published Q1 / Q3   = 13.0 / 35.3 d
```

The event-count, median-phase, IQR-overlap, and source-window gates all pass.

The predictor phase SD across the 224 controller transitions is **15.88 d**;
the old full-year reconstruction produced about 78.6 d because of the
end-of-year TGS artefact.

## W1 — preregistered phase-retention test

For consecutive staging events:

[
E_{i+1}-E_i
=
eta_EE_i
+	ext{route covariates}
+epsilon,
qquad
lambda=1+eta_E.
]

Data:

```text
N transitions = 224
N individuals = 28
```

Corrected result:

```text
beta_E = -0.250232
cluster SE = 0.049906
cluster p = 2.93e-05

lambda_hat = 0.749768
SE         = 0.049906

naive H0: lambda_hat = 1
p = 5.33e-07
```

The registered estimator-scale primary prediction

[
lambda<1
]

**passes**.

The stronger frozen point-estimate forecast

[
|lambda|<0.75
]

also **passes narrowly** because the corrected estimate is 0.749768. This
boundary result is retained mechanically and is not promoted as evidence for a
universal strong-correction constant.

## W2 — preregistered stopover direction

Primary preregistered W2 prediction:

[
S'(E)<0.
]

No fixed p-value threshold was preregistered for this primary directional gate.

Corrected result:

```text
stopover slope = -0.0628626 d / phase-day
cluster SE     =  0.0277386
p              =  0.03166
```

Therefore the **formal directional W2 gate passes**. The conventional
individual-clustered p-value is also compatible with a nonzero negative slope,
but it is supporting evidence rather than a retrospectively imposed
preregistered threshold.

The secondary registered gain band

[
0.3<g_S<0.8
]

fails because

[
g_S=0.06286.
]

## Secondary actuator diagnostics

Between-staging travel speed remains unsupported:

```text
log-speed slope = +0.002757
cluster p       = 0.417
```

Distance moderation remains unsupported at p<=0.05:

```text
origin phase x endpoint distance p = 0.0823
route-progress x endpoint-distance p = 0.252
```

## Cross-system consequence

The corrected wigeon result no longer supports the simple classification

```text
lambda PASS / actuator FAIL
```

used by the superseded full-year reconstruction.

The source-faithful result is:

```text
primary lambda gate:          PASS
strong |lambda|<0.75 gate:    PASS, narrowly
W2 directional stopover:      PASS
W2 secondary gain band:       FAIL
travel speed:                 NOT SUPPORTED
distance moderation:          NOT SUPPORTED
```

Across the direct taxa, stopover/waiting adjustment is therefore a recurrent
actuator, while speed and route-level contributions remain system-dependent.

## Measurement-error ceiling

The corrected lambda remains a **naive errors-in-variables estimator**.

For the source-faithful transition set:

```text
observed predictor phase SD = 15.881 d
```

Under a simple true-lambda=1, equal independent predictor/outcome error model,
an error SD of about **7.94 d** would be sufficient in expectation to attenuate
the naive slope to approximately 0.75. This is a stress threshold, not an
empirical error estimate.

Therefore the source analysis currently licenses:

- a source-faithful estimator-scale lambda;
- W1 primary PASS;
- W2 directional stopover PASS;
- the secondary gain-band FAIL;
- continued failure of the travel-speed diagnostic.

It does **not** yet license:

- measurement-error-corrected latent lambda;
- proof that latent lambda<1 after phase-reconstruction error;
- attribution of cross-taxon lambda magnitude differences entirely to biology.

The next validation task is source-backed phase-error calibration and a
true-lambda=1 observation-scale null.
