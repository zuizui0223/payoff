# PAYOFF-B Aikens 2022 phase-controller receipt

Frozen: 2026-09-20

Status: **published aggregate controller evidence identified**.

This receipt separates a movement-mediated phase-error controller from the
independent PAYOFF-B timing-axis phenology parameter.

Primary source:

- Aikens, E. O., Wyckoff, T. B., Sawyer, H. & Kauffman, M. J. 2022.
  *Industrial energy development decouples ungulate migration from the green
  wave*. Nature Ecology & Evolution 6:1733-1741.
- DOI: 10.1038/s41559-022-01887-9.
- Public data DOI: 10.5061/dryad.7d7wm37z5.

## 1. Empirical estimand

For each migrating individual the study fitted a route-level relationship

    signed Days-From-Peak
    =
    beta0
    + beta1 * distance from development.

The reference point

    distance from development = 0

is the development encounter.

The intercept therefore describes phase mismatch when development is
encountered, whereas the slope describes how mismatch changes as migration
continues.

The PAYOFF-B empirical controller layer defines

    controller restoring
    iff
    beta0 * beta1 < 0.

Equivalently, the local derivative of half squared mismatch is

    d[e^2/2]/dx
    = e * beta1,

so restoration means this derivative is negative.

When beta0 is numerically available and nonzero, the local fractional relaxation
coefficient is

    kappa_controller
    = -beta1 / beta0.

This is a route-distance controller coefficient, not the independent timing-axis
phenology rate h.

## 2. Published controller states

### Low development, large footprint

Published values:

    phase at development:
        early

    mean intercept:
        -13.1 days

    mean slope:
        +0.0008

    slope test:
        P = 0.02.

The signs are restoring:

    early
    + positive slope
    -> mismatch approaches zero.

The native-scale local controller diagnostics are

    -beta0*beta1
    = +0.01048

and

    -beta1/beta0
    = 6.1069e-5
      per published regression-distance unit.

The corresponding linear zero-crossing distance is

    16,375 native distance units.

No km conversion is promoted here because the coefficient scaling should be
confirmed from the source analysis table/code before rescaling.

### Low development, small footprint

Published phase state:

    early,

with mean intercept approximately

    -7.6 days.

The route slope did not differ detectably from zero.

Status:

    no_detected_change.

A nonsignificant slope is not converted to an exact zero controller parameter.

### Medium development

Animals were on average late when encountering development.

Published restoring slopes:

    large footprint:
        -0.001
        P < 0.0001

    small footprint:
        -0.0004
        P < 0.0001.

Because

    late
    + negative slope

moves the signed error toward zero, both conditions are classified as

    restoring_controller_detected.

### High development

Animals were descriptively late. The article reports no detected downstream
mismatch reduction for either footprint.

Status:

    no_detected_change.

The large-footprint intercept test itself was marginal (P=0.06), so that phase
state is not promoted as a strict sign identification.

### Sustained high development

Large footprint:

    late
    + slope -0.001
    P < 0.001

    -> restoring_controller_detected.

Small footprint:

    no detected mismatch reduction

    -> no_detected_change.

## 3. Aggregate controller receipt

Across the eight footprint x development conditions described in the article:

    restoring controller detected:
        4/8

    no detected route-phase change:
        4/8.

This count is a summary of published inferential statements, not a prevalence
estimate for mule deer or migratory ungulates generally.

## 4. The important separation

The empirical result exposes two different mechanisms:

    mismatch at barrier encounter
    !=
    ability to reduce mismatch downstream.

At low development, deer in the large footprint encountered development ahead
of the wave and then allowed the wave to catch up.

At medium development they encountered development late but subsequently
reduced mismatch in both footprints.

At high development they were late and no downstream mismatch reduction was
detected.

At sustained high development, downstream recovery reappeared in the large
footprint but not the small footprint.

Thus poor whole-route surfing can coexist with a locally restoring controller
if the initial mismatch burden is already large.

In PAYOFF-B language:

    initial mismatch burden
    x controller recovery strength
    -> realized phase tracking.

This is separate from

    intrinsic spatial tracking capacity,
    independent timing-axis phenology rate,
    and demographic persistence.

## 5. Relationship to movement behavior

The same study reports holding-up before development and increased movement
speed after deer encountered development.

Therefore the published phase-controller slope is naturally interpreted as a
movement-mediated tracking controller.

It must not be relabeled as the PAYOFF-B phenology parameter h.

The raw GPS data would allow the next step:

    fixed-interval projected displacement
    -> directional movement kernel

combined with

    phase error
    -> movement / stopover response.

## 6. Claim boundary

This receipt does not establish:

- a calibrated PAYOFF-B phenology rate;
- a calibrated per-step directional movement kernel;
- a universal development threshold;
- that the published slope coefficients use km as their regression unit;
- a fitness or persistence effect from controller restoration alone.

The retained empirical statement is:

> The published mule-deer study contains context-dependent evidence for a
> route-distance phase-error controller: some development conditions show
> statistically supported restoration toward the green wave, whereas others
> show no detected downstream mismatch reduction.

## 7. Reproduce

Run:

    python scripts/audit_aikens_2022_phase_controller.py

Implementation:

    src/phase_error_controller.py

The receipt intentionally uses only values explicitly reported in the article
text and does not digitize figure points or refit individual trajectories.
