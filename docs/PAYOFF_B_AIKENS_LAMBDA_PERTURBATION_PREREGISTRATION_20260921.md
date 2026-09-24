# PAYOFF-B Aikens mule-deer lambda perturbation preregistration

Frozen: 2026-09-21

Status: **prospective within-taxon forcing test; lambda outcome not yet observed**.

## 1. Motivation

Aikens et al. (2022) reported that industrial development within a mule-deer
migration corridor altered movement and decoupled migrating deer from the green
wave.

The existing PAYOFF-B source-backed perturbation receipt independently shows
lower local movement-control permeability in the large-development population:

    median G small-development:
        1.656

    median G large-development:
        1.037

    centered large-development log-G shift:
        -0.4763
        p = 0.0172.

Those results motivate, but do not determine, the following lambda prediction.

No phase-retention estimate from this industrial dataset has been inspected in
PAYOFF-B before freezing this registration.

## 2. Prospective question

Holding taxon fixed:

> does stronger industrial-development forcing increase phase retention?

The primary prediction is

    lambda_large-development
    >
    lambda_small-development.

Interpretation:

    larger lambda
        more incoming phase mismatch retained per standardized correction
        interval

    smaller lambda
        stronger phase correction.

Thus the prediction states that the large-development population will exhibit
weaker phase correction.

## 3. Frozen phase coordinate

Phase coordinate ID:

    signed_days_relative_to_local_peak_IRG.

At every retained standardized location-time observation,

    E
    =
    observation calendar day
    -
    local calendar day of peak instantaneous rate of green-up (IRG).

Sign convention:

    E < 0
        animal ahead of local peak IRG

    E = 0
        animal at local peak IRG

    E > 0
        animal behind local peak IRG.

The coordinate is therefore a signed phase mismatch, not raw NDVI and not
movement speed.

MODIS-derived vegetation phenology / IRG must be reconstructed independently of
the registered outcome model.

## 4. Frozen segment scale

Segment-scale ID:

    fixed_24h_spring_migration_interval.

For each animal-year:

1. retain the spring-migration interval defined from the archived movement
   source;
2. create a 24-hour target grid;
3. match a GPS location to each target only when a valid location lies within a
   predeclared tolerance of the target time;
4. do not stretch variable-duration raw steps into one common interval without
   resampling;
5. form consecutive E_t -> E_(t+24h) pairs only when both endpoints pass the
   phase-reconstruction gate.

The final tolerance and spatial extraction settings must be frozen in the
analysis script before the lambda outcome is opened.

If the data cannot support a fixed 24-hour interval with adequate sample size,
the result is NOT ESTIMABLE under this preregistration. The segment scale must
not be changed after seeing lambda.

## 5. Primary model

Primary fixed-effect structure:

    E_next
    ~
    E_current
    + E_current : large_development
    + C(animal_year).

Cluster uncertainty by animal ID.

Definitions:

    lambda_small
        coefficient of E_current

    delta_lambda_large
        coefficient of E_current : large_development

    lambda_large
        lambda_small + delta_lambda_large.

Primary registered gate:

    delta_lambda_large > 0

with

    p_difference <= 0.05.

Equivalent PAYOFF-B registration:

    group A:
        small-development WHB

    group B:
        large-development DCC

    expected:
        lambda_B > lambda_A.

No minimum effect size beyond positive direction is registered.

## 6. Sample-support gate

Before evaluating the phase-retention contrast, require at minimum:

    10 animals per development population

and

    100 fixed-24h phase transitions per development population.

If either population fails support:

    PRIMARY LAMBDA CONTRAST:
        NOT ESTIMABLE.

Do not relax support thresholds after seeing the fitted lambdas.

## 7. Environmental reconstruction gate

The phase analysis proceeds only if:

- MODIS-derived phenology can be reconstructed over the retained route and
  years;
- each retained location has a valid local peak-IRG date;
- the reconstruction uses one frozen processing rule across both populations;
- no development-population-specific smoothing or threshold is introduced
  after outcomes are inspected.

The existing movement-permeability G result is not used to construct E_t.

## 8. Primary outcome classes

### PASS

    delta_lambda_large > 0
    and
    p_difference <= 0.05.

Interpretation:

> large-development forcing is associated with weaker phase correction on the
> common within-taxon phase coordinate.

### FAIL — wrong direction

    delta_lambda_large <= 0.

Interpretation:

> reduced movement-control permeability does not translate into greater phase
> retention in the preregistered direction.

### FAIL — insufficient support

    delta_lambda_large > 0
    but
    p_difference > 0.05.

Interpretation:

> the point direction is compatible but the preregistered inferential gate is
> not passed.

### NOT ESTIMABLE

Triggered by support or environmental-reconstruction failure.

No threshold retuning is allowed.

## 9. Relationship to actuator evidence

The source-backed actuator result is frozen separately in

    docs/PAYOFF_B_INDUSTRIAL_MULE_DEER_ACTUATOR_RECEIPT_20260921.md.

That result establishes:

    actuator permeability attenuation:
        supported

    stronger longitudinal deterioration:
        not supported.

The new lambda contrast asks whether that actuator perturbation propagates into
the shared phase-retention coordinate.

Possible informative outcomes include:

    actuator attenuation PASS
    lambda contrast PASS

or

    actuator attenuation PASS
    lambda contrast FAIL.

Either outcome is scientifically useful.

## 10. Why this is stronger than a fourth taxon

This design adds:

    new forcing regime:
        yes

    new taxon:
        no

    prospective lambda-boundary/contrast test:
        yes

    actuator perturbation already independently measured:
        yes.

It therefore tests whether lambda responds to forcing while holding much of the
organismal architecture constant.

This is more diagnostic than adding another taxon merely because another
tracking dataset is available.

## 11. Frozen machine registration

    data/aikens2022_lambda_perturbation_registration_20260921.json

Evaluation CLI:

    python scripts/evaluate_phase_retention_contrast.py ...

No observation JSON exists yet.

Creating the observation file is licensed only after the environmental-phase
reconstruction pipeline is frozen.

## 12. Claim ceiling

This preregistration does not claim:

- that the published 38.65% surfing decline equals a lambda change;
- that control permeability G equals lambda or 1-lambda;
- that development causally changes lambda;
- that the fixed 24-hour phase reconstruction is already complete;
- that the primary prediction will pass.

It freezes a falsifiable within-taxon forcing prediction before the lambda
outcome is reconstructed.
