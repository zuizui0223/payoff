# PAYOFF-B phase-retention and actuator gate contract

Frozen: 2026-09-21

## 1. Why the empirical architecture changes

PAYOFF-B should not gain apparent generality by mechanically adding taxa and
requiring them to share the same physical actuator.

The cross-system question is narrower:

> Does a system retain or erase phase mismatch in the predicted way?

The common coordinate is therefore the signed phase-retention coefficient

    e_out = r + lambda e_in,

where

    e_in
        signed phase mismatch entering the declared interval / segment;

    e_out
        signed phase mismatch leaving it;

    r
        residual forcing / intercept on the same coordinate;

    lambda
        retained fraction of phase mismatch.

The actuator question is separate:

> By what system-specific mechanism was that retention achieved?

Possible actuator observables include:

- movement speed;
- stopover duration;
- route reset / rerouting;
- directional movement;
- timing change;
- other system-specific behavioral or developmental controls.

Those variables are not required to share a universal coefficient across taxa.

## 2. Gate 1 — phase retention

For each system, estimate

    lambda

from a predeclared common phase coordinate.

The implementation fits

    e_out = r + lambda e_in

with an intercept.

Structural interpretation:

    lambda < 0
        sign reversal / overshoot;

    0 <= lambda < 1
        restoring phase retention;

    lambda = 1
        no net phase correction;

    lambda > 1
        mismatch amplification.

Under the local closed-loop PAYOFF-B recurrence

    e_(t+1) = (1-K)e_t + r,

the exact relationship is

    lambda = 1-K

and therefore

    K = 1-lambda.

This identifies total local restoring gain only. It does not identify how K is
partitioned among movement, stopover, route resetting, timing, or other
actuators.

### Cross-system claim

The strongest cross-system empirical test is therefore a prediction interval or
ordering for lambda on a shared coordinate.

New taxa are valuable when they provide an independent lambda test in a new
forcing, life-history, or movement regime.

Taxon count by itself is not the target.

## 3. Gate 2 — system-specific actuator prediction

Only after the lambda gate is evaluated should a system-specific actuator gate
be tested.

Each actuator prediction must be prospective within that system, for example:

    higher phase error
    -> faster movement

or

    higher phase error
    -> reduced stopover

or

    route obstruction
    -> route reset probability increases.

No rule requires the same actuator to exist or have the same sign/magnitude in
another taxon.

Actuator predictions are evaluated separately and are never folded back into
the lambda gate.

## 4. Four possible outcomes

### lambda PASS / actuator PASS

The common phase-retention coordinate is supported and the declared
system-specific mechanism is also supported.

### lambda PASS / actuator FAIL

The common phase-retention prediction is supported, but the physical mechanism
was predicted incorrectly.

This is not a failure of the shared lambda coordinate.

It is evidence that

    shared controller geometry
    !=
    shared actuator.

The current wigeon result motivates this architecture: the strong lambda
prediction was retained while the common actuator predictions did not hold.
The numerical wigeon receipt remains separate and should be frozen only from
its source analysis.

### lambda FAIL / actuator PASS

The proposed actuator responds as predicted, but the common phase-retention
law or prediction fails.

This rejects the cross-system lambda prediction even if a local mechanism is
present.

### lambda FAIL / actuator FAIL

Neither the common coordinate nor the declared system-specific mechanism is
supported for that system.

## 5. Cross-system synthesis contract

The repository now has an explicit synthesis layer:

    src/cross_system_phase_synthesis.py

and

    scripts/synthesize_cross_system_phase.py.

The synthesis unit is an **independent lambda test**, not a taxon label and not
an actuator prediction.

Every system entry must declare:

    independent_test_id
    phase_coordinate_id
    segment_scale_id
    forcing_regime.

The first field prevents the same data from being relabeled and counted more
than once.

The next two fields are stricter. Cross-system synthesis is refused unless all
systems share one predeclared

    phase_coordinate_id

and one predeclared

    segment_scale_id.

This is necessary because lambda is interval- and segment-dependent. Two
systems can use the same algebraic equation but still have incomparable lambda
values if one coefficient describes a one-day transition and another describes
an entire migration.

Therefore standardization must happen **before** synthesis.

The cross-system output reports:

- the number of independent lambda tests;
- lambda PASS / FAIL counts;
- lambda values and descriptive range/median;
- retention-class counts;
- forcing regimes represented;
- systems in the lambda PASS / actuator FAIL quadrant;
- systems in the lambda FAIL / actuator PASS quadrant;
- actuator results system by system.

It intentionally does **not** report:

- a pooled actuator pass rate;
- a taxon-level actuator score;
- an omnibus lambda + actuator score.

The API raises an error if a caller requests an actuator omnibus score.

## 6. Prospective registration contract

Confirmatory PAYOFF-B evidence is now required to pass through a frozen
registration before observations are evaluated.

The implementation separates:

    prediction registration
    -> later observations
    -> evaluation receipt.

Phase-retention registration freezes:

    system_name
    independent_test_id
    forcing_regime
    phase_coordinate_id
    segment_scale_id
    lambda_low
    lambda_high
    minimum pair count
    optional required retention class.

Actuator registration freezes:

    system_name
    independent_test_id
    forcing_regime
    actuator names
    predicted directions
    zero tolerances.

The registration object contains **no observed effect sizes**.

After observations arrive, evaluation requires exact matching of:

    system_name
    independent_test_id

and, for lambda,

    phase_coordinate_id
    segment_scale_id.

For actuator evaluation, the set of observed actuator names must exactly equal
the registered names. Missing registered actuators and extra post-hoc actuator
variables are both rejected.

Confirmatory cross-system synthesis accepts prospective evidence only when the
phase and actuator receipts explicitly record that the prospective contract was
satisfied. Retrospective analyses can remain visible as a separate evidence
tier but do not inflate prospective lambda support.

Code:

    src/prospective_tracking_registry.py
    src/prospective_tracking_evaluation.py

CLIs:

    scripts/evaluate_registered_phase_retention.py
    scripts/evaluate_registered_actuators.py

## 7. Manuscript hierarchy

The manuscript should therefore use the hierarchy

    common phase coordinate
        -> lambda prediction
        -> independent cross-system test

followed by

    system-specific actuator
        -> prospective mechanism prediction
        -> local falsification / support.

Do not use

    number of taxa with the same speed/stopover response

as the main measure of generality.

A system can strengthen the paper even when its actuator gate fails, provided
it gives an informative independent lambda test.

## 8. Relationship to existing PAYOFF-B controller theory

The existing closed-loop model writes

    e_(t+1)
    = (1-q_m-q_h)e_t + r.

Therefore its multiplier is exactly

    lambda
    = 1-q_m-q_h.

Earlier local theory often emphasized the decomposition

    q_m + q_h.

For cross-system empirical synthesis, the safer identifiable target is instead

    lambda.

The decomposition belongs to the actuator layer and requires system-specific
data.

This prevents the empirical program from relabeling:

- movement-mediated phase correction as intrinsic phenology h;
- stopover control as a universal movement coefficient;
- route resetting as the same actuator as continuous speed adjustment.

## 9. Wigeon quantitative result

The preregistered Eurasian-wigeon analysis is now frozen in

    docs/PAYOFF_B_WIGEON_PHASE_RETENTION_RECEIPT_20260921.md.

Source-backed prospective result:

    consecutive staging transitions:
        224

    individuals:
        28

    lambda:
        0.85994

    SE:
        0.04509

    p versus lambda=1:
        0.00190.

Thus the preregistered primary prediction

    lambda < 1

passes.

The stronger preregistered / exploratory forecast

    |lambda| < 0.75

fails.

Measured actuator tests also fail to reproduce the mule-deer / goose
architecture:

    stopover slope:
        -0.000140
        p = 0.972

    log travel-speed gain / phase-day:
        +0.00109
        p = 0.197.

This is therefore the observed prospective example of

    lambda PASS
    actuator FAIL.

The retained scientific consequence is:

> phase retention is a stronger candidate for the cross-system coordinate than
> a universal actuator rule.

A separate descriptive receipt freezes the existing three-taxon direct
coordinate in

    docs/PAYOFF_B_THREE_TAXON_PHASE_RETENTION_RECEIPT_20260921.md.

That three-taxon receipt does not estimate one universal lambda and does not
convert repeated barnacle-goose flyways into independent taxa.

## 10. Taxon inclusion rule

A new taxon should be added when at least one of the following is true:

1. it provides a genuinely independent prospectively registered lambda test;
2. it occupies a forcing regime not represented by existing systems;
3. it tests a predeclared boundary or sign change in lambda;
4. it provides a prospective actuator test that discriminates among competing
   mechanisms within that system.

A taxon should not be added merely because another movement dataset is
available.

This policy is executable in:

    src/taxon_inclusion_gate.py
    scripts/evaluate_taxon_inclusion.py.

Every candidate declares the proposed independent test ID, common phase
coordinate, common segment scale, forcing regime, and which inferential
contribution it adds.

Hard blockers are:

    PHASE_COORDINATE_INCOMPATIBLE
    SEGMENT_SCALE_INCOMPATIBLE
    INDEPENDENT_TEST_ID_ALREADY_USED
    NO_NEW_INFERENTIAL_CONTRIBUTION.

Raw-data availability is recorded but never counts as an inferential
contribution by itself.

The purpose is to prevent a large comparative panel from becoming a mechanical
taxon-count exercise. Generality is earned by independent tests of the common
lambda geometry and by prospective mechanism discrimination, not by adding
another species label.

## 11. Code contract

Common-coordinate implementation:

    src/phase_retention_gate.py

CLI:

    python scripts/evaluate_phase_retention_gate.py ...

System-specific actuator gate:

    python scripts/evaluate_actuator_gate.py ...

Cross-system lambda synthesis:

    python scripts/synthesize_cross_system_phase.py ...

The synthesis manifest must declare one common phase-coordinate ID and segment-
scale ID. The lambda and actuator outputs remain separate.

There is intentionally no combined pass/fail score.

## 12. Claim boundary

The phase-retention coefficient is not automatically scale-free across arbitrary
time intervals or route segments.

Cross-system lambda comparisons require:

- a declared signed phase coordinate;
- comparable definition of the input and output segment;
- predeclared interval / segment scale;
- no post-hoc selection of segments to improve lambda agreement.

Likewise, actuator tests require prospectively declared system-specific
observables and directions.

Preferred:

> Across systems, PAYOFF-B compares phase retention on a shared mismatch
> coordinate, while the mechanisms that realize that retention are tested
> prospectively within each system.

Avoid:

> Different taxa should all speed up, reduce stopovers, or reset routes in the
> same way when phase mismatch increases.
