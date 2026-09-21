# PAYOFF-B three-taxon direct phase-retention coordinate receipt

Frozen: 2026-09-21

Status: **descriptive cross-taxon coordinate established; universal lambda not estimated**.

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

Prospective third-taxon direct result:

    transitions:
        224

    individuals:
        28

    lambda:
        0.859942433

    SE:
        0.045093213

    p versus lambda=1:
        0.001896645

    |lambda|:
        0.859942433

    correction fraction:
        0.140057567.

Measured stopover and travel-speed actuator predictions were not supported.

Wigeon therefore expands the direct coordinate into a weak-correction regime
without reproducing the mule-deer / goose actuator architecture.

## 5. Taxon-level descriptive synthesis

One descriptive record per taxon gives approximately:

    mule deer:
        median |lambda| = 0.10734

    barnacle goose:
        median |lambda| = 0.130730883

    Eurasian wigeon:
        median |lambda| = 0.859942433.

Taxon-level median-|lambda| range:

    0.10734 .. 0.859942433.

All registered direct rows satisfy

    |lambda| < 1,

but the strength of retention correction is highly heterogeneous.

This is why the licensed cross-system statement is not

> migrants share one universal correction coefficient.

It is

> direct migratory systems with different actuator architectures can be placed
> on a common phase-retention response coordinate.

## 6. Prospective status

The evidence tiers are not identical.

Wigeon is the preregistered third-taxon test and therefore provides the
prospective cross-system extension.

Mule deer and the barnacle-goose route reconstructions provide the existing
direct empirical coordinate against which the wigeon forecast was generated.

Accordingly:

    prospective third-taxon lambda test:
        PASS

    stronger |lambda|<0.75 forecast:
        FAIL

    common actuator forecast:
        NOT SUPPORTED.

This combination is the empirical reason for separating lambda and actuator
gates.

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

The frozen three-taxon result is:

> **phase retention is a portable response coordinate; actuator architecture
> and correction strength are not portable constants.**

This conclusion survives the wigeon partial falsification because the wigeon
primary lambda<1 prediction passes while the stronger common-strength and
shared-actuator predictions do not.

## 9. Claim ceiling

Licensed:

- direct phase-retention estimates exist in three migratory taxa;
- all registered direct rows have |lambda|<1;
- taxon-level retention strength spans a wide range;
- wigeon is a prospective third-taxon extension;
- actuator architectures differ;
- one common response coordinate is empirically useful.

Not licensed:

- one universal lambda;
- one universal correction strength;
- one universal actuator;
- treating three barnacle-goose flyways as three independent taxa;
- a conventional meta-analytic mean at n=3 taxa;
- numerical pooling across segment definitions that were not prospectively
  standardized.
