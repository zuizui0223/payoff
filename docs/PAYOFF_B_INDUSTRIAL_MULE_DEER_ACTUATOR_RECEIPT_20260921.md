# PAYOFF-B industrial mule-deer actuator-perturbation receipt

Frozen: 2026-09-21

Status: **source-backed within-taxon actuator perturbation; phase-retention lambda not identified**.

## 1. Source provenance

Primary PAYOFF source:

    PR #144
    empirical/movement-phenology-macro-20260918
    head:
        df79ddba9bcf7d8c8f77829fa7e9b8f670b36ff6

Source receipt:

    docs/MOVEMENT_PHENOLOGY_INDUSTRIAL_MULE_DEER_RECEIPT.md
    blob:
        40fd458a3185270c98e8a5cbbb60976feb5b295d

Analysis:

    analysis/movement_phenology/stage3_industrial_mule_deer_permeability.py
    blob:
        8cd42ef65c9165f1be79e9629919f5796ba7d355

Registered sensitivity table:

    data/MOVEMENT_PHENOLOGY_INDUSTRIAL_PERMEABILITY_REGISTRY.csv
    blob:
        fc6de2f32539fbe6d1f9c76587687f2b8f92729a

Biological source:

    Aikens et al. (2022)
    Nature Ecology & Evolution 6:1733–1741
    DOI 10.1038/s41559-022-01887-9

Public data:

    Dryad DOI 10.5061/dryad.7d7wm37z5

## 2. Why this system belongs in the actuator layer

The Ortega mule-deer system supplies a direct phase-controller signature:

    phase lag
    -> faster movement
    -> reduced stopover
    -> phase-error reduction.

The industrial-development system asks a different question:

> does a large development footprint reduce the realized ability to express
> movement control near a route boundary?

The registered response is therefore an actuator-permeability quantity, not
phase-retention lambda.

For each animal-year,

    G
    =
    median movement speed near development boundary
    /
    median movement speed far from development boundary.

Primary registered spatial contrast:

    near <= 2 km
    far >= 10 km
    minimum 3 movement steps per zone.

This is a within-animal-year relative movement response.

It does not estimate

    e_out = r + lambda e_in.

Accordingly this receipt contributes **zero additional lambda tests** to the
cross-system phase-retention synthesis.

## 3. Source reconstruction

Public GPS reconstruction:

    GPS points:
        64,539

    valid movement steps:
        64,286

    GPS animal-years:
        253

    GPS animals:
        137

    study years:
        9
        (2005, 2006, 2008, 2009, 2010, 2015, 2016, 2017, 2018)

Primary G analysis:

    analyzable animal-years:
        188

    animals:
        103.

## 4. Primary actuator-permeability result

Median G:

    small-development population:
        1.656

    large-development population:
        1.037.

Clustered longitudinal model at centered study year:

    large-development shift in log G:
        beta = -0.4763

    SE:
        0.1967

    p:
        0.0172.

On the multiplicative G scale,

    exp(-0.4763) ~= 0.621.

Thus the fitted relative near-boundary movement response is about 38% lower in
the large-development population at the centered study year.

This percentage is specific to the PAYOFF-B G metric and must not be described
as a direct replication of the published route-scale 38.65% surfing decline.

## 5. Registered spatial sensitivity

The qualitative small-versus-large contrast is stable across all eight
registered near/far definitions.

Selected median G values:

    edge/far km     small      large

    1 / 5           2.137      1.123
    1 / 10          2.157      0.966
    1 / 20          2.340      0.841

    2 / 5           1.685      1.115
    2 / 10          1.656      1.037
    2 / 20          1.790      0.941

    5 / 10          1.453      0.889
    5 / 20          1.517      0.808.

The large-development intercept shift is negative throughout the registered
grid.

## 6. Step-level actuator result

Within-animal-year step model:

    near-boundary edge effect:
        beta = +0.1963
        p = 4.59e-5

    edge x large-development:
        beta = -0.1518
        p = 0.0382

    edge x year:
        beta = -0.0260
        p = 0.00106

    edge x large-development x year:
        beta = +0.0146
        p = 0.226.

The negative edge x large-development interaction is consistent with attenuated
local movement response in the large-development population.

Because the response is log(1+speed), these coefficients are not raw-speed
percentage effects.

## 7. Stronger longitudinal forecast — failed

The stronger registered prediction was:

> control permeability should deteriorate more strongly through time in the
> large-development population.

Observed:

    year x large-development
        beta = +0.0405
        SE = 0.0411
        p = 0.327.

Therefore:

    LONGITUDINAL DETERIORATION FORECAST:
        NOT SUPPORTED.

This negative result is retained.

## 8. Two-gate interpretation

This system illustrates a different empirical quadrant from wigeon.

Wigeon:

    lambda:
        measured and primary prediction PASS

    measured stopover / travel-speed actuators:
        NOT SUPPORTED.

Industrial mule deer:

    lambda:
        NOT MEASURED by this analysis

    actuator-permeability perturbation:
        SUPPORTED cross-sectionally

    stronger longitudinal actuator forecast:
        NOT SUPPORTED.

Therefore the actuator layer has empirical content that is not reducible to
cross-system lambda.

Conversely, actuator evidence from this system must not be counted as an
additional lambda test.

This is the practical reason PAYOFF-B keeps the two gates separate.

## 9. Relationship to taxon inclusion

This result adds inferential coverage without adding a taxon.

The taxon is already represented by mule deer.

What is new is a forcing regime:

    industrial-development route perturbation.

Thus PAYOFF-B gains information by adding a **within-taxon perturbation**, not
by adding another species name.

This is exactly the preferred alternative to mechanical taxon expansion.

## 10. Claim ceiling

Licensed:

- archived GPS and development footprints are directly reanalyzed;
- near-boundary movement response is lower in the large-development population;
- the direction is stable across all registered spatial sensitivity choices;
- the within-animal-year step model independently detects attenuation;
- the result supports reduced movement-control permeability;
- the stronger longitudinal deterioration prediction is not supported.

Not licensed:

- a direct phase-retention lambda;
- treating G as lambda or 1-lambda;
- a causal development effect;
- universal interpretation of all route barriers through G;
- a new taxon-level lambda replication;
- claiming that the large-development population necessarily has weaker
  phase correction without a direct phase-retention analysis.
