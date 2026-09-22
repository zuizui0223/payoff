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

A pre-Aikens recovery layer is now frozen in:

    src/phase_retention_recovery.py
    data/payoff_b_lambda_recovery_validation_contract_20260922.json
    data/payoff_b_lambda_recovery_taxon_registry_20260922.json

Until source-backed phase-error SDs, predictor phase variances, and consecutive
error correlations are calibrated for each system:

    portable phase coordinate:
        RETAINED

    universal lambda:
        NOT CLAIMED

    biological interpretation of cross-system lambda magnitude differences:
        PENDING MEASUREMENT-ERROR AUDIT

    latent lambda < 1 from naive lambda_hat < 1 alone:
        NOT YET LICENSED

The corrected wigeon result is a valid source-faithful estimator-scale result,
but its naive p-value against lambda_hat=1 is not a substitute for a
true-lambda=1 errors-in-variables null. Its observed origin-phase SD is
15.88 d; under the simple equal-independent-error stress model, about 7.94 d of
phase-error SD would be sufficient in expectation to reproduce the observed
lambda_hat from latent lambda=1. That number is a stress threshold, not an
empirical error estimate.

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

The preferred next empirical task is **not** to add a fourth taxon and is now
also **not** to open the Aikens lambda outcome immediately.

The source-faithful wigeon correction shows that environmental observation
details can materially shift both lambda and actuator inference. The next gate
is therefore source-backed phase-error calibration for the direct systems,
with wigeon first because it is the prospective third-taxon test.

Required before biological interpretation of latent lambda:

    observed predictor phase variance:
        source-faithful value frozen

    predictor measurement-error SD:
        PENDING

    outcome measurement-error SD:
        PENDING

    consecutive-error correlation:
        PENDING

    true-lambda=1 observation-scale null:
        PENDING.

The Aikens industrial-development within-mule-deer lambda perturbation remains
preregistered and unopened. It should stay unopened until this recovery/null
layer is frozen enough that the new Aikens result cannot determine how phase
measurement error will be handled.

The Aikens prediction remains

    lambda_large-development
    >
    lambda_small-development

on the preregistered coordinate

    signed_days_relative_to_local_peak_IRG

and segment scale

    fixed_24h_spring_migration_interval.

It remains a within-system lambda perturbation and is not added to the
cross-system lambda synthesis.

More generally, future additional systems should test a new region or boundary
of lambda-space.

Examples of useful future tests include:

- a system predicted to approach lambda ~= 1 under weak control;
- a system predicted to cross lambda=0 into overshoot;
- a forcing regime expected to change lambda while preserving actuator
  architecture;
- two systems with similar lambda but deliberately different actuators;
- one system with a registered actuator switch while lambda remains stable.

These would test the geometry rather than merely replicate taxonomy.

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
