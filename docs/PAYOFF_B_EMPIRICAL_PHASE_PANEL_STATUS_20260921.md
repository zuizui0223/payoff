# PAYOFF-B empirical phase-retention panel status

Frozen: 2026-09-21

> **2026-09-22 revalidation update:** source-faithful wigeon reconstruction is
> complete. The published TGS contract restricts temperatures to January--July
> before applying the 5 C cumulative-minimum rule. The corrected prospective
> estimate is `lambda_hat=0.749768` (SE 0.049906; naive p versus 1 =
> 5.33e-07). The formal W2 stopover prediction now passes
> (slope=-0.06286, p=0.0317), while travel speed remains unsupported.
> The old `lambda=0.85994 / actuator FAIL` classification is superseded.
> See `docs/PAYOFF_B_WIGEON_PHASE_RETENTION_REVALIDATED_20260922.md`.

## Current panel

Direct phase-retention coordinate currently contains three taxa:

1. mule deer
   - taxon: Odocoileus hemionus
   - direct lambda ~= 0.107
   - measured speed + stopover compensation

2. barnacle goose
   - taxon: Branta leucopsis
   - three route/flyway rows
   - lambda values:
       -0.106, 0.131, 0.494
   - route-stage / stopover architecture
   - repeated flyways are treated as within-taxon replication, not extra taxa

3. Eurasian wigeon
   - taxon: Mareca penelope
   - preregistered prospective third-taxon result, source-window revalidated
   - 224 consecutive staging transitions / 28 individuals
   - naive lambda_hat = 0.749768
   - SE = 0.049906
   - naive p versus lambda_hat=1 = 5.33e-07
   - primary lambda<1 prediction PASS
   - stronger |lambda|<=0.75 point forecast PASS, narrowly
   - primary directional stopover actuator PASS
   - secondary 0.3<g_S<0.8 band FAIL
   - travel-speed actuator NOT SUPPORTED
   - distance moderation NOT SUPPORTED

## What is established

The current direct empirical panel supports:

> phase retention is a portable response coordinate across migratory systems.

It does not support:

> one universal retention coefficient.

It does not support:

> one universal full actuator architecture.

The source-faithful wigeon result adds a different pattern from the previously
promoted analysis. The preregistered stopover/waiting **direction** is now
prospectively supported
in wigeon and is also observed in mule deer and barnacle geese, making it a
recurrent cross-system actuator. Travel-speed and route-level contributions
remain system-dependent.

## Measurement-error audit added 2026-09-22

The direct lambda values above are naive regression-scale estimates. Because
phase is reconstructed and appears on the predictor axis, predictor measurement
error can attenuate lambda toward zero.

The observation-error recovery layer is frozen in:

    src/phase_retention_recovery.py
    data/payoff_b_lambda_recovery_validation_contract_20260922.json
    data/payoff_b_lambda_recovery_taxon_registry_20260922.json

The registered wigeon POWER-versus-ERA5-Land event-level replicate calibration
was executed on 2026-09-23.

Registered calibration outcome:

    paired events:
        220 / 256

    paired fraction:
        0.859375

    frozen minimum fraction:
        0.90

    minimum count >=200:
        PASS

    published phase validation:
        PASS

    full-224 POWER identity:
        PASS

    REGISTERED CALIBRATION:
        FAIL
        reason = event coverage below frozen 0.90 threshold

The coverage threshold is not relaxed.

The incomplete calibration is nevertheless informative as a sensitivity lane.

Paired-event disagreement:

    median:
        0 d

    SD:
        5.434 d

Paired 181-transition controller comparison:

    POWER lambda_hat:
        0.83796

    ERA5-Land lambda_hat:
        0.86516

    difference:
        +0.02720

True-lambda=1 sensitivity using the frozen full-224 POWER signal:

    equal-independent-replicate error SD = 3.842 d
        lower-tail probability at observed lambda_hat:
            0.000300

    discrepancy-correlation proxy rho = 0.288
        lower-tail probability:
            0.000100

    deliberately conservative full-disagreement SD = 5.434 d
        null 2.5% quantile:
            0.74839

        observed source-faithful lambda_hat:
            0.74977

        lower-tail probability:
            0.0266

These values are **incomplete-calibration robustness diagnostics**, not a final
measurement-error correction. They show that the source-faithful wigeon
estimate is not trivially reproduced by the observed POWER--ERA5-Land
disagreement scales, while preserving the registered calibration FAIL.

Current measurement-error claim state:

    portable phase coordinate:
        RETAINED

    universal lambda:
        NOT CLAIMED

    biological interpretation of cross-system lambda magnitude differences:
        PENDING COMPLETE RELIABILITY AUDIT

    final measurement-error-corrected wigeon latent lambda:
        NOT LICENSED

    wigeon source-faithful estimator-scale contraction:
        RETAINED

Machine receipt:

    data/wigeon_era5land_calibration_result_20260923.json

A post-hoc coastal-mask diagnostic now tests why 36 registered nearest-cell
ERA5-Land requests returned HTTP 200 but no finite Jan--Jul temperatures.
Because the primary registration froze cell_selection=nearest, that diagnostic
cannot retroactively convert the calibration FAIL to PASS.


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

## Broad falsification retained

The movement-phenology macro branch also retains the earlier broad-bird
falsification:

    5,816 observations
    55 migratory bird species

do not support one universal natural movement-speed / environmental-wave-speed
optimum.

This negative result is not rescued by the direct controller systems.

The empirical programme therefore moved from

    universal speed optimum

to

    common phase-retention coordinate
    + recurrent stopover/waiting correction
    + system-dependent speed / route components.

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

The preferred next task remains **not** to add a fourth taxon.

The immediate sequence is:

    1. complete the post-hoc wigeon coastal-mask diagnostic;
    2. preserve the registered nearest-cell ERA5-Land calibration as FAIL;
    3. use the replicate-disagreement simulations only as a robustness/claim
       audit unless a new independently frozen calibration lane is justified;
    4. keep Aikens lambda unopened until its registered environmental extraction
       is executable.

The wigeon source correction and error audit show that environmental observation
details can move both lambda and actuator inference. Generality should therefore
be expanded by increasing **inferential coverage**, not by mechanically
increasing taxon count.


## Frozen references

Wigeon corrected quantitative receipt:

    docs/PAYOFF_B_WIGEON_PHASE_RETENTION_REVALIDATED_20260922.md

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
- a conventional three-taxon meta-analytic mean;
- a fourth-taxon expansion before the inclusion gate identifies a new
  inferential contribution.

Preferred:

> Direct movement systems occupy a common phase-retention coordinate.
> Stopover/waiting compensation recurs across all three direct taxa, whereas
> movement-speed and route-level contributions remain system-dependent.
> Magnitude comparisons among naive lambda estimates remain conditional on the
> frozen measurement-error audit.
