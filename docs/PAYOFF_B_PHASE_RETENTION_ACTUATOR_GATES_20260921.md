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

## 5. Manuscript hierarchy

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

## 6. Relationship to existing PAYOFF-B controller theory

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

## 7. Wigeon interpretation

Current project interpretation supplied by the ongoing wigeon analysis:

    strong lambda prediction:
        supported;

    shared actuator predictions:
        not supported.

The retained scientific consequence is:

> phase retention is a stronger candidate for the cross-system coordinate than
> a universal actuator rule.

Until the numerical wigeon analysis is frozen in its own source-backed receipt,
this statement is architectural motivation rather than a quantitative
meta-analytic datum.

## 8. Taxon inclusion rule

A new taxon should be added when at least one of the following is true:

1. it provides a genuinely independent lambda test;
2. it occupies a forcing regime not represented by existing systems;
3. it tests a predicted boundary or sign change in lambda;
4. it provides a prospective actuator test that discriminates among competing
   mechanisms within that system.

A taxon should not be added merely because another movement dataset is
available.

## 9. Code contract

Common-coordinate implementation:

    src/phase_retention_gate.py

CLI:

    python scripts/evaluate_phase_retention_gate.py ...

System-specific actuator gate:

    python scripts/evaluate_actuator_gate.py ...

The two outputs remain separate.

There is intentionally no combined pass/fail score.

## 10. Claim boundary

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
