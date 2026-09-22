# PAYOFF-B Aikens industrial mule-deer IRG reconstruction handoff

Frozen: 2026-09-21

Status: **fixed-target execution v2 frozen; exact 64,539-point source manifest ready; AppEEARS execution blocked only by missing GitHub Actions credentials**.

## 1. Why this handoff exists

The Aikens industrial-development mule-deer analysis is already preregistered
as a within-taxon phase-retention perturbation test.

Frozen prediction:

    lambda_large-development
    >
    lambda_small-development

on the phase coordinate

    signed_days_relative_to_local_peak_IRG

and the segment scale

    fixed_24h_spring_migration_interval.

The movement source is already reconstructed. The remaining blocker is the
local annual date of peak instantaneous rate of green-up at the retained GPS
locations.

No lambda outcome is opened until this environmental layer passes.

## 2. Movement source already recovered

Source:

    Aikens et al. 2022
    Nature Ecology & Evolution 6:1733-1741
    DOI 10.1038/s41559-022-01887-9

Dryad:

    DOI 10.5061/dryad.7d7wm37z5

PAYOFF source workflow:

    Movement-phenology industrial mule deer Dryad audit
    run 35558837950
    head df79ddba9bcf7d8c8f77829fa7e9b8f670b36ff6

Frozen artifact:

    artifact 10621500814
    sha256
    4e7071281487c29da107f135f9c388edd4eef836eecce1ba7401878038bdce10

The artifact contains:

    64,539 GPS points
    64,286 valid movement steps
    253 animal-years
    137 animals

and both development footprints.

Direct inspection of the archived source schema shows no vegetation, NDVI, or
IRG field. Therefore the current phase blocker is environmental reconstruction,
not movement-data availability.

## 3. Environmental reconstruction target

The study-family green-wave workflow uses MODIS surface reflectance to derive
annual NDVI and instantaneous rate of green-up.

The reconstruction contract in PAYOFF uses the Aikens / Merkle / Bischof
workflow family:

1. surface-reflectance bands 1 and 2;
2. NDVI at approximately 250 m and 8-day temporal resolution;
3. quality screening;
4. winter snow handling;
5. snow-free lower 2.5% NDVI as winter baseline;
6. floor winter / lower observations to that baseline;
7. three-observation moving median;
8. upper 92.5% reference for annual 0-1 scaling;
9. annual double-logistic fit;
10. first derivative of the fitted curve;
11. day of maximum positive first derivative = peak IRG.

The offline implementation is:

    src/irg_reconstruction.py

CLI:

    python scripts/fit_peak_irg_from_ndvi.py ...

The nonlinear fit uses the optional project dependency group:

    irg

so core PAYOFF remains dependency-free.

## 4. Double-logistic model

The annual curve is represented as

    NDVI(t)
    =
    alpha
    + (beta-alpha)
      [
        1/(1+exp[-gamma(t-delta)])
        + 1/(1+exp[epsilon(t-theta)])
        - 1
      ].

Parameters:

    alpha
        lower annual asymptote

    beta
        upper annual asymptote

    gamma
        spring green-up rate

    delta
        spring logistic midpoint

    epsilon
        autumn dry-down rate

    theta
        autumn logistic midpoint.

Peak IRG is the calendar day maximizing the analytic first derivative.

The fitter also reports

    spring_scale_days = log(3)/gamma

as a descriptive logistic time scale.

## 5. MODIS product-version firewall

The original study-family reconstruction used MODIS Version 6 products.

NASA LP DAAC decommissioned MODIS Version 6 land-product distribution on
2023-07-31 and recommends Version 6.1 for current access.

Therefore PAYOFF defines two distinct lanes.

### Lane A — study-faithful

    MOD09Q1.006

Output label:

    study_faithful_v006

This is the preferred historical reconstruction when the exact V006 source can
be materialized from an archive or retained source.

### Lane B — current-product sensitivity

    MOD09Q1.061

Output label:

    v061_sensitivity_only

This lane is useful for robustness / compatibility checks.

It must not be described as a bit-for-bit replication of the original V006
environmental product.

No result may silently substitute V061 for V006 while retaining a
study-faithful label.

## 6. Input contract

The offline fitter accepts a table with one row per retained pixel-year
composite:

    pixel_id
    year
    doy
    ndvi
    snow_free
    quality_good

The product version is supplied explicitly on the command line.

Example:

    python scripts/fit_peak_irg_from_ndvi.py \
      sampled_mod09q1_ndvi.csv \
      --modis-product MOD09Q1.006 \
      --output outputs/aikens_peak_irg.csv

The fitter fails closed when:

- snow flags are missing in the strict study-faithful lane;
- too few valid composites remain;
- no valid two-consecutive-composite snow release is found;
- annual NDVI scaling collapses;
- the nonlinear fit fails;
- seasonal ordering is invalid.

## 7. Required handoff into the lambda test

The peak-IRG output is not itself a phase-retention result.

After peak IRG is reconstructed, execution follows the frozen v2 ordering:

1. convert the exact GPS-to-MODIS links into identity-preserving raw GPS keys;
2. select the 24 h target grid **before** environmental availability is used:

       scripts/select_fixed_interval_gps_targets.py

3. freeze the nearest raw GPS observation within the preregistered ±3 h window
   for each target;
4. attach local peak IRG to those already selected targets:

       scripts/attach_peak_irg_to_fixed_targets.py

5. if a selected target lacks valid environmental reconstruction, mark that
   target invalid; do not select a replacement GPS observation;
6. build pairs only from adjacent valid target indices:

       scripts/build_phase_pairs_from_fixed_targets.py

7. verify the support gate separately in WHB and DCC;
8. fit the frozen phase-retention contrast model;
9. only then create the observation JSON for

       scripts/evaluate_phase_retention_contrast.py.

This ordering prevents environmental missingness from changing which GPS
observation represents a registered 24 h target.

The primary test remains

    delta_lambda_large > 0
    AND
    p_difference <= 0.05.

## 8. Support gate remains frozen

Minimum support per population:

    >= 10 animals

and

    >= 100 fixed-24h phase transitions.

If either group fails:

    NOT ESTIMABLE.

Do not:

- widen the temporal matching window after seeing support;
- switch segment scale after seeing lambda;
- tune IRG smoothing separately by development population;
- change product version after observing the contrast;
- use the previously observed movement-permeability result to construct phase.

## 9. Frozen pair-level lambda contrast fitter

The statistical layer downstream of the fixed 24-hour phase pairs is now
implemented explicitly rather than left as a manual analysis step.

Implementation:

    src/phase_retention_contrast_fit.py

CLI:

    scripts/fit_aikens_phase_retention_contrast.py

Optional dependency group:

    empirical

with

    numpy
    statsmodels.

The frozen model is the preregistered design:

    E_next
    ~
    E_current
    + E_current : large_development
    + C(animal_year)

with cluster-robust uncertainty by animal ID.

The fitter reports:

    lambda_small
    SE(lambda_small)

    delta_lambda_large
    SE(delta_lambda_large)

    lambda_large
    SE(lambda_large)

    p_difference.

It applies the frozen support gate **before fitting**:

    >=10 animals per development population
    >=100 fixed-24h transitions per development population.

If support fails, the fitter returns

    NOT ESTIMABLE

with no lambda coefficients.

If support passes, the CLI writes the exact observation JSON consumed by

    scripts/evaluate_phase_retention_contrast.py

using the frozen registration

    data/aikens2022_lambda_perturbation_registration_20260921.json.

A dedicated CI workflow now validates the complete statistical handoff on a
synthetic known-contrast fixture:

    .github/workflows/payoff-b-aikens-phase-contrast.yml

The synthetic fixture contains 10 animals and 120 transitions per group with

    lambda_small ~= 0.30
    lambda_large ~= 0.60

and is required to recover a positive supported contrast and pass the same
preregistered gate used by the future empirical observation.

This workflow is a regression test for the statistical implementation only. It
does not open the empirical Aikens lambda outcome.

## 10. Pipeline validation provenance

The complete offline environmental handoff has been validated end to end on a
synthetic annual NDVI curve.

GitHub Actions:

    workflow:
        payoff-b IRG reconstruction

    run:
        35603379065

    head:
        ed3a9aec4fd952c932dea9cebcff677ec9084553

Frozen artifact:

    artifact:
        10640161096

    sha256:
        9659fac9a34cf39102675ab283474d025fcffe71eef2dbca16e5b79402840483

The successful workflow executes, in order:

    optional IRG dependency installation
    -> IRG unit tests
    -> synthetic MODIS-like annual NDVI construction
    -> double-logistic peak-IRG reconstruction
    -> synthetic GPS pixel mapping
    -> peak-IRG to GPS environmental join
    -> fixed 24-hour phase-pair reconstruction.

All steps completed successfully.

This receipt validates the computational handoff. It does not validate the
Aikens environmental source reconstruction itself.

## 11. AppEEARS request-preparation layer

The current-product sensitivity extraction is now implemented up to the
authenticated network boundary.

### Raw movement geometry

The previously frozen movement artifact proves that the source contains

    64,539 raw GPS points

across

    253 animal-years
    137 animals
    9 observed years
    both WHB and DCC populations.

The raw GPS re-export is now complete.

Source workflow:

    run:
        35605623469

    source branch:
        empirical/movement-phenology-macro-20260918

    source commit:
        0a934adbeaa386edf27fcfaabff9ca7837a2382b

Frozen artifact:

    artifact:
        10643405042

    sha256:
        1f0d706dc6a102261009b7099c748dcce40abb2adedf7b88828395a1d392cfa0

Exact raw file:

    stage3_industrial_mule_deer_gps.csv

    sha256:
        03426804557a0244be3ed6eb9f461db578d3ce26fa2b28637f8e98bee9f09466

The table contains exactly

    64,539 GPS points
    137 animals
    253 animal-years

with both

    small
    large

development groups and the frozen year set.

The canonical source-identity gate therefore passes.

### Midpoint-only preflight

To size the extraction before raw GPS re-export completes, the 64,286 valid
step midpoints were projected to the standard MODIS 250 m sinusoidal grid.

This proxy gives approximately

    unique 250 m cells:
        11,414

    unique cell-years:
        20,327

    year-scoped tasks at 1000 cells/task:
        25.

Frozen receipt:

    data/payoff_b_aikens_appeears_preflight_20260921.json

This is an operational preflight only. It is explicitly rejected by the final
source-identity gate because

    64,286 != 64,539.

The midpoint geometry is now superseded by the exact raw-GPS manifest.

### Frozen exact raw-GPS manifest

The canonical builder has now been run on the full 64,539-point source.

Frozen receipt:

    data/payoff_b_aikens_exact_manifest_status_20260921.json

Exact request geometry:

    GPS observations:
        64,539

    unique MODIS 250 m cells:
        10,899

    unique cell-years:
        19,500

    year-scoped tasks
    at 1000 cells/task:
        24.

Frozen SHA256 values:

    manifest:
        d50e69a20d6e65ec3426a8c938d1dea9d4e2f836c9bf07e02d30c560f5fa8463

    cells table:
        3570bc04dfef9da677954246b636a99fa069c4b2e5b0020dd9ac1c4ee9dc8d02

    GPS-to-cell links:
        ef7445152bf2217a81088e1765cd215dfafb87036366c8f789e6ebe3747cbff1.

This exact manifest supersedes the midpoint preflight counts

    11,414 cells
    20,327 cell-years
    25 tasks.

The difference is operational only. No lambda or IRG outcome is opened.

### Exact manifest builder

Implementation:

    src/appeears_modis_request.py

CLI:

    scripts/build_aikens_appeears_manifest.py

The builder:

1. transforms projected GPS coordinates to MODIS sinusoidal coordinates;
2. assigns the standard 250 m global cell;
3. deduplicates repeated GPS observations to cells;
4. retains observation-to-cell links;
5. counts unique cell-years;
6. creates year-scoped AppEEARS point tasks;
7. requests current-product V061 sensitivity layers only.

The current V061 task layers are:

    MOD09Q1.061
        sur_refl_b01
        sur_refl_b02
        sur_refl_qc_250m
        sur_refl_state_250m

    MOD10A2.061
        Maximum_Snow_Extent
        Eight_Day_Snow_Cover.

### Source-identity gate

Implementation:

    src/appeears_manifest_gate.py

CLI:

    scripts/evaluate_aikens_appeears_manifest.py

The canonical Aikens gate requires exactly

    64,539 GPS observations

and the frozen year set

    2005
    2006
    2008
    2009
    2010
    2015
    2016
    2017
    2018

with both

    small
    large

development groups represented.

This prevents the 64,286 midpoint proxy, an accidental subset, or a
single-population extraction from being submitted as the canonical request.

### Authenticated AppEEARS operational client

Implementation:

    src/appeears_client.py

CLI:

    scripts/run_appeears_manifest.py

Default behavior is dry-run only.

Authenticated submission requires explicit

    --submit

and reads credentials only from environment variables:

    APPEEARS_TOKEN

or

    EARTHDATA_USERNAME
    EARTHDATA_PASSWORD.

The client implements the official flow

    login
    -> submit task
    -> retrieve task status
    -> list bundle
    -> download bundle files.

Credential values are never serialized to request receipts.

The dedicated CI workflow is

    .github/workflows/payoff-b-appeears-manifest.yml

and tests request construction, source coverage gating, authenticated-client
logic using a fake session, and dry-run task selection without contacting
AppEEARS.

### Version boundary remains unchanged

This operational layer prepares

    MOD09Q1.061 / MOD10A2.061

as

    v061_sensitivity_only.

It does not promote V061 to the study-faithful lane.

A historical V006 source remains preferred for the primary reconstruction if it
can be materialized independently.

## 12. Current blocker

The movement archive, raw GPS re-export, source-identity gate, exact MODIS
cell/year manifest, V061 primary-successor amendment, and fixed-target execution
v2 are complete.

A live AppEEARS smoke test was executed in GitHub Actions:

    workflow:
        payoff-b Aikens AppEEARS live smoke

    run:
        35612310294

    outcome:
        SKIPPED_NO_APPEEARS_CREDENTIALS.

No network extraction was performed.

The required credential is one of:

    APPEEARS_TOKEN

or

    EARTHDATA_USERNAME
    EARTHDATA_PASSWORD.

These values are read only from GitHub Actions secrets or the process
environment; they are never written into PAYOFF receipts.

Once credentials are configured, the frozen operational sequence is:

    exact manifest
    -> AppEEARS V061 extraction
    -> IRG reconstruction
    -> environment-independent 24 h GPS target selection
    -> attach phase to those frozen targets
    -> invalidate missing environmental targets without replacement
    -> adjacent valid target pairs
    -> frozen clustered lambda contrast
    -> preregistered outcome class
    -> outcome-specific manuscript rendering and submission audit.

Thus the current blocker is operational credential configuration, not an
unresolved analysis choice.

The lambda outcome remains unopened.

## 13. Why this is preferred over adding a fourth taxon

This design holds taxon largely fixed while changing forcing regime.

It tests:

    actuator attenuation
    -> does lambda itself change?

Possible informative outcomes include:

    actuator attenuation PASS
    lambda contrast PASS

and

    actuator attenuation PASS
    lambda contrast FAIL.

Either result is more diagnostic of the controller architecture than adding a
fourth species solely because another tracking dataset exists.

## 14. Claim ceiling

Licensed now:

- public industrial mule-deer GPS and development footprints are recovered;
- the phase-retention perturbation is preregistered;
- the fixed-24h phase-pair reconstruction is implemented;
- the offline peak-IRG reconstruction is implemented;
- product-version lanes are separated.

Not yet licensed:

- a reconstructed industrial-mule-deer peak-IRG table;
- small- or large-development lambda;
- a lambda contrast;
- any statement that development changes lambda.

Those outcomes remain closed until the environmental source layer is
materialized and the frozen reconstruction pipeline passes.
