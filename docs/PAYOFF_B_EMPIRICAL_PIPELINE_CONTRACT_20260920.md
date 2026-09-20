# PAYOFF-B empirical tracking pipeline contract receipt

Frozen: 2026-09-20

Status: **synthetic pipeline witness; not an empirical result**.

This receipt freezes the executable path that a real interval-level tracking
dataset must pass before PAYOFF-B makes a named-system prediction.

## 1. Required sequence

The empirical route is now

    projected fixed-interval observations
        ->
    grouped calibration / holdout split
        ->
    movement-kernel audit
        ->
    timing-axis audit
        ->
    frozen tracking controls
        ->
    held-out interval validation
        ->
    predeclared validation gate
        ->
    independently identified fitness terms
        ->
    held-out environmental forcing projection.

The held-out groups never refit the tracking controls.

## 2. Grouped split rule

Cross-validation uses a deterministic SHA256 ranking of group IDs.

Default scientific use:

    split unit = animal

rather than individual GPS rows.

An optional

    animal_year

split is available when the year column is present.

At least one complete group is held out and at least one remains in training.
This prevents row-level leakage among repeated observations from the same
individual.

## 3. Synthetic calibration witness

Canonical CI workflow:

    workflow run 35491555401
    job 106027257212

The fixed-interval calibration fixture contains projected metric x/y locations,
one-hour intervals, symmetric nearest-neighbor movement, and an explicitly
isolated first-order timing signal.

Training-only recovery gives

    migration rate:
        0.287682072452

    x weight:
        0.5

    y weight:
        0.5

    x bias:
        0

    y bias:
        0

    calibration climate velocity:
        0.06

    phenology rate:
        0.693147180560
        = log(2).

The fitness-contract fixture independently identifies

    baseline growth = 0.4
    abiotic mismatch strength = 1.2
    interaction mismatch strength = 0.8
    migration cost = 0.1
    phenology cost = 0.05
    joint cost = 0.035.

These values are deliberately synthetic and analytically recoverable.

## 4. Separate held-out interval file

A different interval file is used for validation.

Canonical result:

    held-out intervals:
        8

    frozen movement moment RMSE:
        0

    phase validation licensed:
        yes

    held-out mean log-compression error:
        0.

This verifies the forward-prediction path:

    calibrated kernel
    -> predicted held-out first and second displacement moments

without re-estimating the kernel on held-out rows.

## 5. Grouped cross-validation witness

The four-individual fixture is split before calibration.

Canonical result:

    training groups:
        2

    held-out groups:
        2

    training intervals:
        8

    held-out intervals:
        8

    held-out movement moment RMSE:
        0

    held-out phase mean-log-compression error:
        0.

The exact zero is expected because the synthetic train and holdout groups were
generated from the same declared kernel. It is a pipeline regression test, not
a target for real data.

## 6. Predeclared held-out validation gate

Held-out diagnostics are not automatically promoted to a validated tracking
controller. A separate gate now requires thresholds to be declared before the
held-out result is interpreted.

The gate can require:

    movement dimensionless moment RMSE <= tau_m,

    held-out movement intervals >= n_m,

and, when the timing axis is part of the claimed controller,

    timing-axis validation licensed,
    phase intervals >= n_h,
    |mean log-compression error| <= tau_h.

The gate does not estimate tau_m or tau_h from held-out performance.

The synthetic CI witness uses

    tau_m = 0.01,
    n_m   = 4,
    require phase validation = yes,
    tau_h = 0.01,
    n_h   = 4.

Because the synthetic held-out fixture is generated from the same declared
kernel, it passes with

    movement RMSE = 0
    phase mean-log-compression error = 0.

Those CI thresholds are pipeline regression settings, not ecological default
acceptance thresholds.

Run:

    python scripts/evaluate_tracking_validation_gate.py \
      --validation-json <heldout.json> \
      --max-movement-moment-rmse <predeclared_tau_m> \
      --min-held-out-intervals <n_m> \
      --require-phase-validation \
      --max-abs-phase-log-error <predeclared_tau_h> \
      --min-phase-intervals <n_h>

A failed gate blocks downstream validated projection. A projection without a
gate can still be run as a mechanistic scenario, but its status is explicitly
labeled unvalidated tracking.

## 7. Frozen-control forcing projection

The biological controls are then frozen and the external environmental wave
speed is changed without refitting.

Canonical synthetic projection:

    calibration climate velocity:
        0.06

    prediction climate velocity:
        0.10

    frozen migration rate:
        0.287682072452

    frozen phenology rate:
        0.693147180560

    projected mean low-density growth:
        0.196379923938

    projected final abundance:
        1829.96049903

    projected persistence:
        yes.

With a passing held-out tracking gate this is labeled

    tracking_controls_validated_held_out_forcing_projection.

Without a gate it is labeled

    held_out_forcing_mechanistic_projection_unvalidated_tracking.

Neither label by itself is ecological outcome validation.

The current projection uses an open regular grid with declared demographic
assumptions. A named-system persistence test additionally requires independent
habitat, demographic, fitness, and held-out outcome data.

## 8. Refusal gates

The pipeline refuses or downgrades claims when:

- the table is animal-year summary grain rather than interval/GPS grain;
- coordinates are longitude/latitude without a declared metric projection;
- no fixed decision interval can be retained;
- observed step moments exceed the one-step kernel support;
- neither symmetric nor directional movement kernel is compatible;
- phase residuals cross zero, amplify, begin at zero, or hit a complete
  one-step correction boundary;
- movement contributes to phase correction and the timing axis is therefore
  not isolated;
- fitness coefficients are inferred from movement data rather than independent
  matched growth contrasts;
- named-system habitat/demographic assumptions are unavailable.

## 9. Mule-deer status

The Ortega et al. public system remains

    PUBLIC_SYSTEM_IDENTIFIED
    DIRECT_TRACKING_CALIBRATION_PENDING_SOURCE_FILE_INGESTION
    FITNESS_PARAMETERIZATION_NOT_IDENTIFIED.

The repository now has the complete downstream analysis path for the source
file once it is available locally.

## 10. Reproduce

Core commands:

    python scripts/inspect_mule_deer_source_csv.py <source.csv>

    python scripts/audit_interval_tracking_calibration.py <training.csv> ...

    python scripts/validate_interval_tracking_controls.py <heldout.csv> ...

    python scripts/evaluate_tracking_validation_gate.py ...

    python scripts/cross_validate_interval_tracking.py <interval.csv> ...

    python scripts/parameterize_migration_phenology_fitness.py ...

    python scripts/predict_empirical_tracking_landscape.py ...

The fixtures used by CI are in

    examples/tracking/fixed_interval_calibration.csv
    examples/tracking/fixed_interval_validation.csv
    examples/tracking/grouped_cross_validation.csv.

## 11. Claim boundary

This receipt proves that the empirical workflow is executable, separated by
estimand, and leakage-resistant under its declared synthetic witness.

It does not show that any real species follows the one-step movement kernel,
that timing-axis h is identifiable in mule deer, that the synthetic fitness
coefficients apply to mule deer, or that the open-grid persistence prediction
has empirical validity.
