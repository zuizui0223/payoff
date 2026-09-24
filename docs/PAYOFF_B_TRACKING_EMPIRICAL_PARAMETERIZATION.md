# PAYOFF-B migration–phenology empirical parameterization handoff

Status: implemented algebraic observation-to-model bridge. This is not yet a
named-system calibration.

## Purpose

The moving-landscape model now has enough synthetic robustness that the next
step should not be another arbitrary parameter sweep. The empirical handoff
instead asks:

> Which PAYOFF-B tracking parameters are directly recoverable from movement,
> environmental-wave and phenology observations under the declared kernel?

The implementation is
`src/tracking_empirical_parameterization.py`, with a CLI at
`scripts/parameterize_migration_phenology_tracking.py`.

## 1. Movement kernel

For the current one-step anisotropic nearest-neighbor kernel, let

    f = 1 - exp(-m)

be the fraction moving one patch per generation. Let the x/y axis weights be
w_x and w_y, and patch spacing be d. Then

    Var_x
    = f * w_x/(w_x+w_y) * d^2

    Var_y
    = f * w_y/(w_x+w_y) * d^2.

Therefore

    f = (Var_x + Var_y)/d^2

and

    m = -log(1-f).

The movement anisotropy is identified from the variance shares:

    w_x : w_y = Var_x : Var_y.

Only the ratio matters to the simulator. The implementation normalizes the
returned weights to sum to one.

### Refusal condition

The inverse requires

    0 <= (Var_x + Var_y)/d^2 < 1.

If the observed variance exceeds that support, the correct response is not to
clip the data. It means the one-patch kernel is too narrow and a wider or
continuous movement kernel is required.

When both variances are zero, m=0 is identified but the x/y anisotropy is not.

### Directional movement extension

Migratory GPS tracks can have non-zero mean displacement on the declared
decision interval. That does not have to be forced into the symmetric kernel.

The 2D simulator now also allows directional biases

    b_x, b_y in [-1,1].

For a biased nearest-neighbor kernel,

    E[X]
    = f s_x b_x d,

    E[X^2]
    = f s_x d^2,

and equivalently for Y. Therefore fixed-interval projected moments identify

    f
    = [E[X^2]+E[Y^2]] / d^2,

    b_x
    = E[X] d / E[X^2],

    b_y
    = E[Y] d / E[Y^2].

The previous symmetric kernel is the special case

    b_x=b_y=0.

This inverse is implemented in

    scripts/parameterize_directional_movement_kernel.py.

If an identified bias lies outside [-1,1], or if the total second moment exceeds
one-patch support, the one-step kernel is rejected rather than clipped.

### Projected coordinates are mandatory

Longitude/latitude degrees are not accepted as metric x/y for the exact
movement inverse. The source table must first be projected into declared
distance units.

The source-file inspector distinguishes:

    metric x/y columns
    versus
    geographic longitude/latitude.

A lon/lat-only file is therefore not marked movement-ready.

## 2. Phenology response

The model uses

    q_h = 1 - exp(-h)

as the fraction of current climate-equivalent residual corrected per generation.

Thus an observed correction fraction q_h gives

    h = -log(1-q_h).

Equivalently, when spatial state is held fixed and the residual follows one
monotone first-order correction,

    e_after = exp(-h) e_before,

so

    h = -log(e_after/e_before).

Sign reversal, amplification or overshoot are rejected by this exact inverse.
They indicate that the simple first-order response is not adequate for that
transition.

### Phase-error compression is not automatically h

For migratory systems, a Days-From-Peak residual can shrink because the animal
changes movement speed, stopover use, route, or timing. Therefore

    phase-error compression
    !=
    timing-axis phenology rate h.

The interval-level audit

    scripts/audit_interval_tracking_calibration.py

reports phase-error log compression descriptively, but licenses h only when the
timing axis has been independently isolated from spatial movement and other
correction pathways.

This distinction is especially important for the Ortega et al. mule-deer
system, where the published mechanism is movement-speed and stopover adjustment
along the green wave.

## 3. Moving-environment velocity

If the environmental wave moves at physical speed c and the spatial
environmental gradient is g, the model coordinate velocity is

    v = g c.

This is a unit conversion, not an estimated ecological law.

## 4. Phenology scale and limit

The user must declare a conversion

    s = climate-coordinate units / phenology unit,

so that a phenological shift z contributes s z to tracking.

The finite phenology limit

    |z| <= z_max

should come from the biological or empirical support of the timing shift. It
must not be tuned after seeing which value rescues the model.

## 5. Fitness terms require different evidence

Movement and timing observations do **not** identify:

- baseline low-density growth;
- abiotic mismatch strength;
- interaction mismatch strength;
- migration architecture cost;
- phenology architecture cost;
- joint architecture cost;
- density regulation;
- local carrying capacity.

For the declared quadratic penalties, matched growth contrasts can identify
individual coefficients when other terms are held fixed. For example,

    growth_loss = 0.5 A e^2

implies

    A = 2 growth_loss / e^2.

Likewise an isolated quadratic tracking cost

    growth_cost = c r^2

gives

    c = growth_cost / r^2.

These are design equations, not permission to infer costs from movement
variance alone.

A six-contrast exact identification route is implemented in

    scripts/parameterize_migration_phenology_fitness.py

using one common reference plus isolated abiotic, interaction, migration-cost,
phenology-cost, and joint-cost contrasts. If any identified penalty coefficient
is negative, the default behavior is to reject the declared non-negative
penalty model rather than silently truncate the coefficient.

## 6. Recommended empirical data contract

A minimum direct tracking receipt should declare:

1. time unit and generation/decision interval;
2. projected metric spatial coordinate system;
3. patch spacing d;
4. fixed-interval movement component means and second moments, or variances when
   a symmetric kernel is independently justified;
5. climate-axis orientation used to rotate movement components;
6. environmental gradient g in compatible units;
7. environmental/resource-wave speed c;
8. interval-level phase residuals;
9. whether the timing axis is independently isolated from movement;
10. phenology scale s;
11. predeclared maximum supported phenology shift z_max.

Then run, for example:

    python scripts/parameterize_migration_phenology_tracking.py \
      --variance-x 0.08 \
      --variance-y 0.02 \
      --patch-spacing 0.5 \
      --spatial-gradient 0.2 \
      --wave-speed 0.3 \
      --phenology-correction-fraction 0.25 \
      --phenology-scale 0.1 \
      --max-abs-phenology-shift 20

The JSON output explicitly lists the directly identified subset and the terms
that remain unidentified.

For interval/GPS-level data, first run

    python scripts/inspect_mule_deer_source_csv.py <source.csv>

and then, only if projected fixed-interval columns are present,

    python scripts/audit_interval_tracking_calibration.py <source.csv> \
      --target-interval-hours <hours> \
      --patch-spacing <distance> \
      --climate-axis-angle-degrees <angle>.

The second command audits both the symmetric and directional movement kernels.
It also reports phase-error compression while keeping the timing-axis h
unlicensed unless explicitly isolated.

## 7. Relationship to the mule-deer / bird phase-locking programme

The existing movement–phenology phase-locking programme provides observational
evidence that organisms can adjust movement speed and stopover behavior as a
function of phase error.

That programme and the current moving-landscape model are related but not yet
the same estimand.

The empirical controller

    phase error
    -> movement/stopover adjustment
    -> phase-error correction

is now represented as a separate estimand rather than being folded into h.
The first published controller receipt is

    docs/PAYOFF_B_AIKENS_2022_PHASE_CONTROLLER_RECEIPT.md

with implementation

    src/phase_error_controller.py
    scripts/audit_aikens_2022_phase_controller.py.

For a local route-distance regression

    e(x)=beta0+beta1*x,

the controller is restoring when

    beta0*beta1 < 0.

When beta0 is known, the local fractional relaxation coefficient

    -beta1/beta0

can be reported in the native regression-distance unit. This quantity describes
downstream phase-error recovery and remains distinct from the independent
timing-axis h.

The published Aikens et al. (2022) text supports restoring controllers in
4 of 8 footprint x development conditions and no detected downstream phase
change in the other 4. This is a context-specific published evidence receipt,
not a prevalence estimate.

The controller can inform correction behavior and directional movement
summaries.

It does not by itself identify the two-species interaction strength, tracking
architecture costs, or a population persistence frontier.

A named-system PAYOFF-B calibration should therefore preserve the separation:

    empirical controller identification
    -> observation-to-tracking parameter map
    -> independently measured fitness terms
    -> out-of-sample landscape prediction.

The first named-system readiness audit is frozen in

    docs/PAYOFF_B_MULE_DEER_PARAMETERIZATION_READINESS_20260920.md.

For the published mule-deer group means, the repository also runs

    python scripts/audit_mule_deer_phase_summary.py

as a refusal audit. With negative Days-From-Peak meaning ahead of peak IRG and
positive meaning behind, the published early and mid start/end means cross
zero and therefore violate the simple monotone first-order residual inverse.
The late group compresses from approximately +20 to +11 days and is
mathematically monotone, but that change spans an entire migration rather than
one declared PAYOFF-B decision interval. It is recorded as whole-route
compression, not inserted as a per-step phenology rate.

## 8. Claim boundary

This handoff licenses algebraic parameter recovery under the declared kernel.
It does not establish that the kernel is correct for any named species.

The next empirical upgrade requires either:

- a dataset whose spatial displacement distribution is compatible with the
  declared kernel; or
- replacing the kernel with one appropriate for the observed movement process
  and deriving a new observation map.

The correct failure mode is model rejection, not parameter clipping.
