# PAYOFF-B empirical phase-retention panel status

Frozen: 2026-09-21

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
   - preregistered prospective third-taxon result
   - 224 consecutive staging transitions / 28 individuals
   - lambda = 0.85994
   - SE = 0.04509
   - p versus lambda=1 = 0.00190
   - primary lambda<1 prediction PASS
   - stronger |lambda|<0.75 forecast FAIL
   - stopover actuator NOT SUPPORTED
   - travel-speed actuator NOT SUPPORTED

## What is established

The current direct empirical panel supports:

> phase retention is a portable response coordinate across migratory systems.

It does not support:

> one universal retention coefficient.

It also does not support:

> one universal speed / stopover / route-reset actuator.

The wigeon prospective result is especially informative because it expands the
observed direct coordinate into a weak-correction regime while failing the
stronger cross-system correction forecast.

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

    common phase-retention coordinate + system-specific actuator.

## Confirmatory versus descriptive evidence

The three-taxon direct coordinate is descriptive.

The wigeon third-taxon lambda test is prospective.

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

The preferred next empirical task is therefore not

    find another migratory species.

It is

    find a system that tests a new region or boundary of lambda-space.

Examples of useful future tests include:

- a system predicted to approach lambda ~= 1 under weak control;
- a system predicted to cross lambda=0 into overshoot;
- a forcing regime expected to change lambda while preserving actuator
  architecture;
- two systems with similar lambda but deliberately different actuators;
- one system with a registered actuator switch while lambda remains stable.

These would test the geometry rather than merely replicate taxonomy.

## Frozen references

Wigeon quantitative receipt:

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

> Direct movement systems occupy a common phase-retention coordinate but differ
> strongly in correction strength and actuator architecture; the prospective
> wigeon test supports the common coordinate while falsifying a stronger
> correction forecast and shared actuator expectation.
