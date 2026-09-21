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

It should be added only if the taxon-inclusion gate identifies at least one
new inferential contribution while preserving the common phase coordinate and
segment-scale contract:

- a new prospectively registered independent lambda test;
- a genuinely new forcing regime;
- a predeclared lambda boundary or sign-change test;
- a prospective actuator discriminator that separates competing mechanisms.

Until such a candidate exists, adding another taxon would increase panel size
without materially strengthening the central claim.

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

Taxon inclusion implementation:

    src/taxon_inclusion_gate.py

    scripts/evaluate_taxon_inclusion.py

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
