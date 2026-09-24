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

Independent ERA5 reliability replication was frozen before ERA5 outcomes for
all three highlighted barnacle-goose fixed transitions.

    Greenland R2 -> R3:
        POWER lambda_hat = 0.130731
        ERA5  lambda_hat = 0.144204
        difference = +0.013473

        POWER stopover slope = -0.5242, p=0.00339
        ERA5  stopover slope = -0.3789, p=0.00802

    Barents R1 -> R2:
        POWER lambda_hat = 0.494114
        ERA5  lambda_hat = 0.515329
        difference = +0.021215

        POWER stopover slope = -0.5915, p=0.000988
        ERA5  stopover slope = -0.5738, p=0.000995

    Svalbard R2 -> R4:
        POWER lambda_hat = -0.106321
        ERA5  lambda_hat = -0.286983
        difference = -0.180662

        POWER stopover slope = -0.588996, p=9.73e-06
        ERA5  stopover slope = -0.621530, p=3.44e-06.

The Svalbard reliability lane uses annual onset anomalies only, so uncertain
region-specific absolute anchors alter intercepts but not the fixed-transition
lambda or stopover slopes.

Thus phase transformation and the negative stopover response are
reconstruction-robust in all three highlighted barnacle-goose flyways. The
Svalbard negative lambda sign also survives source substitution, providing a
boundary case that simple independent classical attenuation of a latent
lambda=1 process cannot generate in expectation.

The POWER--ERA5 disagreement remains an assumption-conditional reliability
calibration, not a gold-standard error distribution.

Machine results:

    data/barnacle_era5_reliability_result_20260924.json
    docs/PAYOFF_B_BARNACLE_ERA5_RELIABILITY_20260924.md

    data/svalbard_barnacle_era5_reliability_result_20260924.json
    docs/PAYOFF_B_SVALBARD_ERA5_RELIABILITY_20260924.md.

## 4. Eurasian wigeon

System:

    Mareca penelope
    van Toor et al. 2021

The wigeon environmental reconstruction was first corrected to the published
January--July TGS window before the corrected POWER result was inspected.

Registered POWER result:

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

    primary lambda<1 gate:
        PASS

    strong |lambda_hat|<0.75 POWER point forecast:
        PASS, narrowly.

Under the registered POWER phase surface the W2 directional stopover gate also
passes:

    slope:
        -0.0628626 d / phase-day

    clustered p:
        0.03166

    fixed p threshold preregistered:
        NO

    secondary 0.3 < g_S < 0.8 band:
        FAIL.

A separately frozen source-faithful ERA5 hourly calibration then achieved
256/256 event coverage and reconstructed phase for all 224 transitions.

On the identical transitions:

    ERA5 lambda_hat:
        0.811312288

    SE:
        0.044776883

    naive p versus lambda_hat=1:
        2.509e-05.

Thus estimator-scale phase contraction replicates across POWER and ERA5.

The actuator result does not replicate as cleanly:

    POWER stopover slope:
        -0.0628626
        p = 0.03166

    ERA5 stopover slope:
        -0.0241815
        p = 0.3104

    travel speed:
        unsupported under both reconstructions.

Accordingly:

    registered POWER W1:
        PASS

    registered POWER strong point forecast:
        PASS, narrowly

    registered POWER W2 directional gate:
        PASS

    independent ERA5 lambda replication:
        SUPPORTS CONTRACTION

    independent ERA5 stopover replication:
        NOT SUPPORTED.

The complete ERA5 calibration is frozen in:

    data/wigeon_era5_sourcefaithful_calibration_result_20260924.json
    docs/PAYOFF_B_WIGEON_ERA5_SOURCEFAITHFUL_CALIBRATION_20260924.md.

The current primary measurement-error sensitivity is:

    data/wigeon_phase_simex_era5_complete_result_20260924.json
    docs/PAYOFF_B_WIGEON_ERA5_SIMEX_V2_20260924.md.

Across the three frozen SIMEX v2 scenarios, extrapolated lambda ranges from
0.7979 to 0.9354. These are sensitivity values, not one recovered biological
lambda.

## 5. Taxon-level descriptive synthesis

One descriptive naive-estimator record per taxon gives approximately:

    mule deer:
        median |lambda_hat| = 0.10734

    barnacle goose:
        median |lambda_hat| = 0.130730883

    Eurasian wigeon:
        POWER |lambda_hat| = 0.749768021
        ERA5  |lambda_hat| = 0.811312288.

All highlighted direct systems admit phase-retention estimates below one on
their declared intervals. For wigeon, the qualitative contraction signal is
reproduced across two independently reconstructed environmental surfaces.

The actuator layer is less stable.

    mule deer:
        speed + stopover

    barnacle goose:
        stopover / route-stage control

    Eurasian wigeon:
        POWER stopover direction supported
        ERA5 stopover association not supported
        travel speed unsupported under both.

Therefore the strongest current cross-system pattern is not a recurrent
stopover actuator in all three taxa. It is a common phase-retention response
coordinate whose physical implementation and even actuator detectability are
more system- and reconstruction-dependent.

Numeric lambda magnitudes remain measurement-error-sensitive and should not be
treated as portable biological constants.

## 6. Prospective status

Wigeon remains the prospectively registered third-taxon extension.

The frozen registered POWER gates are reported exactly as executed:

    primary lambda<1:
        PASS

    strong |lambda_hat|<0.75 POWER point forecast:
        PASS, narrowly

    W2 directional stopover prediction on POWER phase:
        PASS

    secondary W2 gain band:
        FAIL

    W3 travel-speed diagnostic:
        NOT SUPPORTED.

The independent ERA5 follow-up does not rewrite those registered outcomes.
Instead it supplies a robustness layer:

    ERA5 lambda_hat<1:
        REPLICATED

    ERA5 stopover association:
        NOT SUPPORTED.

This creates a useful two-level result: the phase-retention response is more
stable to environmental reconstruction than the proposed stopover actuator.

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

> **phase retention is a portable empirical response coordinate, while actuator
> evidence is less portable and can be sensitive to how environmental phase is
> reconstructed.**

In wigeon specifically, contraction is reproduced under both POWER and ERA5,
whereas the POWER stopover association is not reproduced by the ERA5 phase
surface.

The biological magnitude of lambda remains conditional on the separate
errors-in-variables audit.

## 9. Claim ceiling

Licensed:

- direct naive phase-retention estimates exist in three migratory taxa;
- the source-faithful wigeon registered POWER primary lambda gate passes;
- wigeon estimator-scale contraction is independently reproduced with ERA5 on
  the same 224 transitions;
- the registered POWER W2 directional stopover gate passes as a source-specific
  prospective result;
- the independent ERA5 reconstruction does not support the wigeon stopover
  association, demonstrating actuator reconstruction sensitivity;
- movement-speed and route-level actuator evidence remain heterogeneous;
- complete ERA5 calibration and SIMEX v2 quantify observation-error sensitivity
  without defining one true latent lambda;
- one common response coordinate is empirically useful.

Not licensed:

- one universal latent lambda or one universal correction strength;
- one universal full actuator architecture;
- a robust recurrent stopover actuator across all three taxa;
- treating naive lambda_hat<1 as sufficient by itself to identify latent
  lambda<1 without observation-error assumptions;
- treating any SIMEX or EIV sensitivity value as the corrected truth;
- attributing cross-taxon lambda magnitude differences entirely to biology;
- treating three barnacle-goose flyways as independent taxa;
- a conventional three-taxon meta-analytic mean;
- numerical pooling across segment definitions that were not prospectively
  standardized.
