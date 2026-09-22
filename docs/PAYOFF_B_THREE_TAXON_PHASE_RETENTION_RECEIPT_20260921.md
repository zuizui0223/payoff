# PAYOFF-B three-taxon direct phase-retention coordinate receipt

Frozen: 2026-09-21
Source-window revalidation updated: 2026-09-22

Status: **descriptive three-taxon coordinate restored after source-faithful wigeon revalidation; universal or measurement-error-corrected lambda not estimated**.

Primary source:

    PAYOFF PR #144
    empirical/movement-phenology-macro-20260918
    head:
        df79ddba9bcf7d8c8f77829fa7e9b8f670b36ff6

Direct registry:

    data/MOVEMENT_PHENOLOGY_DIRECT_CONTROLLER_REGISTRY.csv
    blob:
        dea4917baa362e0805015151ae34c7de4456b1ae

Cross-taxon synthesis implementation:

    analysis/movement_phenology/cross_taxon_phase_retention.py

## 1. Common response coordinate

The source macro programme uses

    E_next
    = a + lambda E_current + error

and reports the absolute retention coordinate

    R_phi = |lambda|.

This is a response coordinate, not a universal mechanistic coefficient.

The direct systems occupy sharply different actuator architectures.

## 2. Mule deer

System:

    Odocoileus hemionus
    Ortega et al. 2023

Direct registry:

    n animal-years:
        152

    individuals:
        72

    lambda:
        0.10734

    |lambda|:
        0.10734

    correction fraction:
        0.89266

Detected actuator architecture:

    movement-speed response:
        detected

    stopover response:
        detected

Interpretation:

    strong distributed phase correction through measured speed + stopover
    channels.

## 3. Barnacle goose

System:

    Branta leucopsis
    Kölzsch et al. 2015

Three direct flyway / route-transition rows are retained within one taxon.

### Svalbard

    lambda = -0.106320907
    |lambda| = 0.106320907

This is a stable overshoot / sign-reversal case.

### Greenland

    lambda = 0.130730883
    |lambda| = 0.130730883

### Barents

    lambda = 0.494113942
    |lambda| = 0.494113942

Taxon-level descriptive median:

    median |lambda|
        = 0.130730883.

Observed within-taxon range:

    |lambda|
        0.106320907 .. 0.494113942.

The three flyways are **not** counted as three independent taxa.

Detected architecture:

    strong route-stage / stopover correction,
    with explicit overshoot or amplification cases retained rather than
    averaged away.

## 4. Eurasian wigeon

System:

    Mareca penelope
    van Toor et al. 2021

The original POWER reconstruction was superseded after a source audit showed
that the published TGS code restricts daily temperatures to January--July
before applying the cumulative-minimum 5 C rule. The corrected reconstruction
was frozen before the corrected lambda was inspected.

Source-faithful prospective third-taxon result:

    transitions:
        224

    individuals:
        28

    lambda_hat:
        0.749768021

    SE:
        0.049905667

    naive p versus lambda_hat=1:
        5.328e-07

    |lambda_hat|:
        0.749768021

    estimator-scale correction fraction:
        0.250231979.

Formal W2 stopover actuator:

    slope:
        -0.0628626 stopover-days / phase-day

    cluster SE:
        0.0277386

    p:
        0.03166

    primary preregistered directional gate:
        PASS

    conventional clustered p:
        0.03166

    fixed p threshold preregistered:
        NO

    secondary 0.3 < g_S < 0.8 band:
        FAIL.

Travel-speed response remains unsupported:

    p:
        0.417.

Distance moderation remains unsupported at p<=0.05.

The corrected wigeon result is therefore

    primary lambda gate:
        PASS

    strong |lambda|<=0.75 point forecast:
        PASS, narrowly

    stopover actuator:
        PASS

    travel-speed actuator:
        NOT SUPPORTED.

The canonical corrected receipt is

    docs/PAYOFF_B_WIGEON_PHASE_RETENTION_REVALIDATED_20260922.md.

## 5. Taxon-level descriptive synthesis

One descriptive naive-estimator record per taxon gives approximately:

    mule deer:
        median |lambda_hat| = 0.10734

    barnacle goose:
        median |lambda_hat| = 0.130730883

    Eurasian wigeon:
        |lambda_hat| = 0.749768021.

Taxon-level observed-|lambda_hat| range:

    0.10734 .. 0.749768021.

All registered direct rows satisfy

    |lambda_hat| < 1,

but these are regression-scale estimands. Differential phase-measurement error
can alter both absolute values and cross-system contrasts, so biological
differences in latent correction strength remain subject to the frozen
measurement-error audit.

A new qualitative pattern is nevertheless visible in the directly measured
actuators:

    mule deer:
        speed + stopover

    barnacle goose:
        stopover / route-stage control

    Eurasian wigeon:
        stopover supported
        travel speed not supported.

Thus stopover / waiting-time adjustment is now a recurrent actuator across the
three taxa, while speed and route-level contributions remain system-dependent.

## 6. Prospective status

The evidence tiers are not identical.

Wigeon is the preregistered third-taxon test and therefore provides the
prospective cross-system extension after source-faithful TGS revalidation.

Mule deer and the barnacle-goose route reconstructions provide the existing
direct empirical coordinate against which the wigeon forecast was generated.

Accordingly:

    prospective third-taxon naive lambda test:
        PASS

    stronger |lambda_hat|<=0.75 point forecast:
        PASS, narrowly

    formal W2 directional stopover prediction:
        PASS

    secondary W2 gain band:
        FAIL

    W3 travel-speed diagnostic:
        NOT SUPPORTED.

This no longer supports a simple "lambda portable / actuator non-portable"
dichotomy. Instead, the data support a common phase coordinate plus a recurrent
stopover/waiting actuator embedded within broader system-specific controller
architectures.

## 7. Why no conventional three-taxon meta-analysis

The source synthesis explicitly reduces repeated barnacle-goose flyways to one
taxon-level descriptive record and does not fit a pooled universal lambda at
n=3 taxa.

Reasons:

- only three taxa;
- different ecological correction opportunities / segment definitions;
- very different actuator architectures;
- wigeon prospectively expands the observed range rather than reproducing a
  common point estimate.

The current PAYOFF-B prospective synthesis architecture is stricter still: any
future pooled confirmatory lambda analysis must predeclare a common phase
coordinate and a common semantic segment-scale contract before outcomes are
opened.

## 8. Retained conclusion

The updated three-taxon result is:

> **phase retention is a portable response coordinate; stopover/waiting is a
> recurrent correction actuator across the three direct taxa, while the full
> controller architecture and estimator-scale retention magnitude are not
> portable constants.**

The biological interpretation of lambda magnitude remains conditional on the
separate errors-in-variables audit.

## 9. Claim ceiling

Licensed:

- direct naive phase-retention estimates exist in three migratory taxa;
- all registered direct rows have |lambda_hat|<1 on their declared intervals;
- the source-faithful wigeon primary prospective gate passes;
- the source-faithful wigeon W2 directional stopover gate passes;
- the secondary wigeon stopover-gain band fails;
- stopover/waiting adjustment recurs across mule deer, barnacle goose and
  wigeon;
- speed and route-level actuator evidence remains heterogeneous;
- one common response coordinate is empirically useful.

Not licensed:

- one universal latent lambda;
- one universal correction strength;
- one universal full actuator architecture;
- treating naive lambda_hat<1 as sufficient proof of latent lambda<1 before
  measurement-error calibration;
- attributing cross-taxon lambda magnitude differences entirely to biology;
- treating three barnacle-goose flyways as three independent taxa;
- a conventional meta-analytic mean at n=3 taxa;
- numerical pooling across segment definitions that were not prospectively
  standardized.
