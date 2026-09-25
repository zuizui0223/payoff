# PAYOFF-B empirical phase-retention panel status

Frozen: 2026-09-21

> **2026-09-25 synthesis update:** the registered 55-species speed-ratio test
> is now the primary cross-system result and rejects one universal natural
> movement-speed/environmental-wave-speed optimum. The three direct taxa are
> retained as a mechanistic panel. Raw lambda is a segment-scale estimator,
> not a portable biological rate. A pre-Aikens secondary standardization now
> reports equivalent interval decay and cumulative retained-memory summaries.
> Wigeon POWER/ERA5 contraction remains replicated, all three highlighted
> barnacle-goose transitions have POWER/ERA5 assumption-conditional
> reliability checks, and mule-deer reliability remains pending. Aikens lambda
> remains unopened.
>
## Current panel

Direct phase-retention coordinate currently contains three taxa:

1. mule deer
   - taxon: Odocoileus hemionus
   - direct lambda ~= 0.107
   - measured speed + stopover compensation

2. barnacle goose
   - taxon: Branta leucopsis
   - three route/flyway rows
   - lambda values: -0.106, 0.131, 0.494
   - route-stage / stopover architecture
   - repeated flyways are within-taxon replication, not extra taxa

3. Eurasian wigeon
   - taxon: Mareca penelope
   - preregistered prospective third-taxon result
   - 224 consecutive staging transitions / 28 individuals
   - POWER lambda_hat = 0.749768
   - POWER SE = 0.049906
   - POWER primary lambda<1 gate PASS
   - POWER strong |lambda|<0.75 point forecast PASS, narrowly
   - independent ERA5 lambda_hat = 0.811312
   - ERA5 SE = 0.044777
   - contraction replicated across POWER and ERA5
   - registered POWER W2 stopover directional gate PASS
   - ERA5 stopover association NOT SUPPORTED (p=0.310)
   - travel-speed actuator NOT SUPPORTED under either reconstruction

## What is established

The primary generality result is the broad falsification:

> Across 5,816 observations from 55 migratory bird species, the registered
> analysis does not support one universal natural movement-speed /
> environmental-wave-speed optimum.

The direct three-taxon panel then asks what replaces that failed universal
rule. Mule deer, barnacle goose and wigeon can all be written with the same
phase-retention estimator form, but **raw lambda magnitudes are interval-scale
dependent** and are not ranked as portable biological constants. System-specific
actuators and environmental-reconstruction reliability are evaluated
separately.

The wigeon replicate calibration sharpens the distinction. Phase-retention
contraction is reproduced under two independently reconstructed environmental
surfaces, while the POWER stopover association is not reproduced under ERA5.
Thus the response coordinate is empirically more reconstruction-stable than the
proposed actuator in this system.

A separately preregistered POWER-to-ERA5 reconstruction for two highlighted
barnacle-goose transitions gives a complementary reliability result:

    Greenland R2 -> R3:
        POWER lambda_hat = 0.130731
        ERA5  lambda_hat = 0.144204
        delta = +0.013473

        POWER stopover p = 0.00339
        ERA5  stopover p = 0.00802

    Barents R1 -> R2:
        POWER lambda_hat = 0.494114
        ERA5  lambda_hat = 0.515329
        delta = +0.021215

        POWER stopover p = 0.000988
        ERA5  stopover p = 0.000995

Thus both the phase-retention response and the negative stopover actuator
replicate across environmental surfaces in these two preregistered goose
transitions.

A separately frozen Svalbard R2 -> R4 ERA5 replication extends this result to
the overshoot boundary:

    POWER lambda_hat = -0.106321
    ERA5  lambda_hat = -0.286983

    POWER stopover slope = -0.588996
        p = 9.73e-06

    ERA5 stopover slope = -0.621530
        p = 3.44e-06.

The negative lambda sign therefore survives environmental-source substitution.
All three highlighted barnacle-goose flyways now reproduce both phase
transformation and the negative stopover response under POWER and ERA5.
Reliability is not a property of lambda alone: it is a system-by-estimand
property that must be audited separately.

## Measurement-error audit updated 2026-09-24

The direct lambda values are regression-scale estimates and can be attenuated by
predictor phase error.

The original preregistered POWER-versus-ERA5-Land calibration remains:

    220 / 256 paired events
    paired fraction = 0.859375
    frozen minimum = 0.90
    REGISTERED ERA5-LAND CALIBRATION = FAIL.

That failure is not relaxed or erased.

A separately frozen source-faithful ERA5 hourly follow-up used the environmental
dataset family described by the original wigeon study and retained the same
coverage, phase-validation, controller and POWER-identity gates.

Complete ERA5 follow-up:

    paired events = 256 / 256
    complete transitions = 224 / 224
    coverage gate = PASS
    published phase validation = PASS
    POWER identity = PASS.

Replicate disagreement:

    median ERA5 - POWER phase = 1 d
    SD = 7.086 d
    equal-independent-replicate sensitivity SD = 5.010 d
    consecutive discrepancy correlation rho = 0.3666.

Same-transition controller comparison:

    POWER lambda_hat = 0.749768
    ERA5 lambda_hat = 0.811312
    difference = +0.061544.

True-lambda=1 sensitivity:

    equal-independent replicate scale:
        lower-tail p = 0.00990

    equal-replicate correlation proxy:
        lower-tail p = 0.000500

    deliberately conservative full-disagreement-as-each-source-error:
        lower-tail p = 0.40086.

Complete-calibration event-structure SIMEX v2:

    equal-independent replicate:
        lambda_SIMEX = 0.8412

    discrepancy-correlation proxy:
        lambda_SIMEX = 0.7979

    conservative full disagreement:
        lambda_SIMEX = 0.9354.

These results show that measurement error materially changes estimated
correction strength. They do not identify one corrected true lambda.

Current measurement-error claim state:

    common phase-retention estimator form:
        RETAINED

    raw cross-system lambda magnitude as common biological rate:
        NOT LICENSED

    interval-standardized secondary comparison:
        FROZEN PRE-AIKENS

    wigeon contraction across POWER and ERA5:
        REPLICATED ON ESTIMATOR SCALE

    barnacle-goose highlighted transition reconstruction sensitivity:
        COMPLETE / ASSUMPTION-CONDITIONAL

    taxa with any reliability calibration:
        2 / 3

    taxa with source-specific gold-standard phase-error identification:
        0 / 3

    unique corrected latent wigeon lambda:
        NOT LICENSED

    cross-taxon biological magnitude ranking:
        NOT LICENSED.

Machine receipts:

    data/wigeon_era5land_calibration_result_20260923.json
    data/wigeon_era5_sourcefaithful_calibration_result_20260924.json
    data/wigeon_phase_simex_era5_complete_result_20260924.json

## Interval standardization frozen before Aikens outcome

The secondary interval-standardization result is frozen in

    data/payoff_b_phase_retention_interval_standardization_result_20260925.json

and does not alter any primary raw-lambda analysis.

Reference median interval lengths are:

    mule deer whole migration: 47.0 d
    Svalbard goose R2 -> R4: 14.8 d
    Greenland goose R2 -> R3: 18.5 d
    Barents goose R1 -> R2: 26.6 d
    wigeon consecutive staging transition: 1.06 d.

For wigeon, the 224 transitions are distributed across 32 animal-years from
28 unique individuals. The observed mean and median are both seven transitions
per animal-year, so the representative homogeneous retained-memory summary is

    POWER R_path(7) = 0.133
    ERA5  R_path(7) = 0.231.

These are the same order as the retrospective mule-deer whole-migration
retention R=0.107. The conservative wigeon SIMEX sensitivity gives
R_path(7) about 0.627, so no universal 80--90% migration-wide correction
fraction is licensed.

The goose rows remain fixed-transition evidence. Whole-route products are not
constructed post hoc.
## Additional within-taxon actuator evidence

The empirical evidence base now contains an additional source-backed
within-taxon perturbation without increasing the direct phase-retention taxon
count.

Industrial-development mule deer:

    taxon:
        Odocoileus hemionus

    forcing:
        industrial-development route boundary

    direct lambda:
        NOT MEASURED

    primary movement-control permeability contrast:
        supported

    median G small-development:
        1.656

    median G large-development:
        1.037

    centered large-development log-G shift:
        -0.4763
        p = 0.0172

    stronger year x large-development deterioration:
        NOT SUPPORTED
        p = 0.327.

This result is frozen in

    docs/PAYOFF_B_INDUSTRIAL_MULE_DEER_ACTUATOR_RECEIPT_20260921.md.

It contributes:

    +1 actuator / forcing evidence unit

and contributes:

    +0 lambda tests
    +0 taxa.

This is the intended alternative to mechanical panel expansion: increase
inferential coverage before increasing taxonomy.

## Broad falsification is the primary cross-system result

The movement-phenology macro branch also retains the earlier broad-bird
falsification:

    5,816 observations
    55 migratory bird species

do not support one universal natural movement-speed / environmental-wave-speed
optimum.

This negative result is not rescued by the direct controller systems. It is the
primary macroecological conclusion. The direct systems instead provide the
mechanistic decomposition:

    universal speed optimum
        -> rejected in 55 species

    shared phase-retention estimator form
        + explicit interval scale
        + actuator-specific tests
        + reconstruction/reliability audits.

The direct panel therefore explains how phase correction can occur after the
universal speed rule fails; it does not replace the 55-species test as the
main generality evidence.

The wigeon result shows that actuator evidence can be less reconstruction-stable
than the phase-retention response itself.

## Confirmatory versus descriptive evidence

The three-taxon direct coordinate is descriptive.

The source-faithful wigeon third-taxon lambda test and W2 stopover prediction
are prospective.

Retrospective or previously reconstructed systems remain visible, but they do
not count as additional prospective lambda support merely because they can be
placed on the same axis.

This distinction is enforced by the prospective registration and
cross-system-synthesis code.

## Fourth-taxon policy

Current status:

    FOURTH_TAXON:
        HOLD.

A fourth taxon is not justified by data availability alone.

A fourth taxon should be added only if the evidence-inclusion gate identifies
a registered endpoint with genuine incremental value.

For lambda evidence this requires:

- a new prospectively registered independent lambda test or lambda-boundary
  test;
- the common phase coordinate;
- the common segment scale.

For actuator-only evidence, a same-taxon perturbation can be included without
a lambda coordinate, but it adds zero lambda support.

A new forcing regime by itself is not enough.

Until a fourth taxon offers an inferential contribution that cannot be obtained
from existing systems or within-taxon perturbations, adding it would increase
panel size without materially strengthening the central claim.

## Current preferred next empirical move

The preferred next task remains not to add a fourth taxon.

Wigeon reliability work has now reached a useful stopping point:

    source-faithful POWER:
        complete

    old registered ERA5-Land lane:
        FAIL retained

    source-faithful ERA5 hourly follow-up:
        COMPLETE / PASS

    complete-calibration SIMEX v2:
        COMPLETE.

The current priority therefore returns to the preregistered Aikens within-taxon
forcing test, while keeping its lambda outcome unopened until the registered
environmental extraction is executable.

No additional wigeon error model should be tuned merely to narrow the SIMEX
range. The complete ERA5 result already establishes the relevant boundary:
phase-retention contraction replicates across environmental surfaces, whereas
the POWER stopover association does not.

## Frozen references

Wigeon corrected quantitative receipt:

    docs/PAYOFF_B_WIGEON_PHASE_RETENTION_REVALIDATED_20260922.md

Complete source-faithful ERA5 calibration:

    docs/PAYOFF_B_WIGEON_ERA5_SOURCEFAITHFUL_CALIBRATION_20260924.md

Complete-calibration SIMEX v2:

    docs/PAYOFF_B_WIGEON_ERA5_SIMEX_V2_20260924.md

Historical superseded receipt:

    docs/PAYOFF_B_WIGEON_PHASE_RETENTION_RECEIPT_20260921.md

Three-taxon direct coordinate receipt:

    docs/PAYOFF_B_THREE_TAXON_PHASE_RETENTION_RECEIPT_20260921.md

Gate contract:

    docs/PAYOFF_B_PHASE_RETENTION_ACTUATOR_GATES_20260921.md

Evidence inclusion implementation:

    src/taxon_inclusion_gate.py

    scripts/evaluate_evidence_inclusion.py

Industrial mule-deer actuator receipt:

    docs/PAYOFF_B_INDUSTRIAL_MULE_DEER_ACTUATOR_RECEIPT_20260921.md

## Claim ceiling

Do not report:

- taxon number as the primary measure of generality;
- one pooled universal lambda;
- one pooled actuator success rate;
- a robust recurrent wigeon stopover mechanism across environmental surfaces;
- a conventional three-taxon meta-analytic mean;
- a fourth-taxon expansion before the inclusion gate identifies a new
  inferential contribution.

Preferred:

> The registered 55-species analysis rejects one universal natural migration-
> phenology speed optimum. Direct systems nevertheless admit a common
> phase-retention estimator form, but raw lambda magnitude depends on interval
> scale. In wigeon, contraction replicates under POWER and ERA5 while the
> stopover association does not; interval-standardized retained memory is a
> secondary comparison and remains measurement-error-sensitive.
