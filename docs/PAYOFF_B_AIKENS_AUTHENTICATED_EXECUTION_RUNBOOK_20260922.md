# PAYOFF-B Aikens authenticated execution runbook

Frozen: 2026-09-22

Purpose: execute the preregistered Aikens within-mule-deer phase-retention
perturbation **without changing any scientific decision after credentials are
configured**.

## 1. Current readiness

Already frozen and validated:

- exact 64,539-GPS source identity;
- exact MODIS-250 m cell/year manifest;
- V061 primary-successor product amendment;
- fixed 24 h target grid and +/-3 h matching tolerance;
- deterministic target tie-break;
- environment-independent target selection;
- pre-environment support ceiling;
- IRG reconstruction implementation;
- fixed-target phase attachment;
- adjacent-valid-pair construction;
- animal-year-FE / animal-clustered contrast model;
- support thresholds;
- p-value threshold;
- outcome interpretation contract;
- outcome-blind manuscript renderer and submission audit.

Pre-environment support ceiling:

    large-development:
        48 animals
        1,022 maximum possible adjacent pairs

    small-development:
        89 animals
        4,434 maximum possible adjacent pairs.

Registered final threshold per group:

    >=10 animals
    >=100 adjacent valid phase pairs.

Therefore the registered test is support-feasible before environmental
filtering.

An outcome-blind robustness envelope has now been computed on the same frozen
targets. Under the synthetic assumption that each selected target independently
has valid environmental phase with common probability p, the exact dynamic
programme gives a 95% joint support threshold at

    p = 0.34198.

At that threshold:

    large-development:
        support probability = 0.95002
        expected valid adjacent pairs = 119.5
        expected animals with valid pairs = 34.2

    small-development:
        support probability ~= 1
        expected valid adjacent pairs = 518.6
        expected animals with valid pairs = 71.3.

Frozen receipt:

    docs/PAYOFF_B_AIKENS_IID_TARGET_COVERAGE_SUPPORT_20260922.md

This is a robustness envelope, not a guarantee: real environmental failures can
be correlated by pixel-year, snow/quality state, date, or geography.

## 2. Current external blocker

A live GitHub Actions smoke test found no configured AppEEARS/Earthdata
credential.

    workflow run:
        35612310294

    status:
        SKIPPED_NO_APPEEARS_CREDENTIALS.

An independent anonymous AWS S3 test also failed:

    workflow run:
        35686454317

    MOD09Q1.061:
        Requester Pays / anonymous AccessDenied

    MOD10A2.061:
        Requester Pays / anonymous AccessDenied.

Authenticated environmental access is therefore required.

## 3. Credential contract

The workflow accepts either:

    APPEEARS_TOKEN

or both:

    EARTHDATA_USERNAME
    EARTHDATA_PASSWORD.

Credential values must exist only in the workflow secret/environment layer.
They must not be committed, printed into receipts, or added to repository
files.

The repository records only whether a credential route was available.

## 4. Workflow to execute

Manual workflow:

    .github/workflows/payoff-b-aikens-appeears-full-extraction.yml

Displayed workflow name:

    payoff-b Aikens V061 primary lambda test

No alternative analysis workflow should be substituted after credentials are
configured.

## 5. Frozen execution order

The workflow order is:

    frozen raw GPS source
    -> exact GPS-to-MODIS manifest
    -> manifest SHA verification
    -> V061 primary-successor amendment verification
    -> raw GPS phase keys
    -> fixed 24 h GPS target selection
    -> pre-environment support-ceiling gate
    -> credential gate
    -> AppEEARS V061 extraction
    -> task merge
    -> IRG-input materialization
    -> peak-IRG reconstruction
    -> phase attachment to already frozen targets
    -> invalid environmental targets remain missing
    -> adjacent valid target pairs only
    -> registered support gate
    -> frozen clustered lambda contrast
    -> registered result classification
    -> outcome-specific manuscript rendering
    -> GEB submission audit.

Environmental availability may invalidate a selected target but may never
cause a replacement GPS observation to be selected.

## 6. Frozen statistical contract

Phase coordinate:

    signed_days_relative_to_local_peak_IRG

Segment scale:

    fixed_24h_spring_migration_interval

Group A:

    small development / WHB

Group B:

    large development / DCC

Registered directional prediction:

    lambda_large-development > lambda_small-development.

Model:

    E_next
    ~ E_current
      + E_current:large_development
      + C(animal_year)

Uncertainty:

    clustered by animal_id.

Support threshold per group:

    >=10 animals
    >=100 adjacent valid phase pairs.

Significance threshold:

    p <= 0.05.

These values must not be changed after environmental extraction.

## 7. Licensed outcome classes

### PASS

The registered direction and support criterion pass.

Licensed interpretation:

> greater phase retention under large-development forcing is consistent with
> movement-control attenuation propagating into realized phase correction.

Not licensed:

> the movement-permeability proxy G equals lambda mechanistically.

### FAIL_WRONG_DIRECTION

The contrast is estimable but the registered direction is wrong.

Licensed interpretation:

> the previously observed actuator attenuation does not propagate into greater
> phase retention as predicted.

No retuning follows.

### FAIL_INSUFFICIENT_SUPPORT

The fitted direction may be nominally positive, but the registered inferential
support criterion fails.

Licensed interpretation:

> no supported lambda shift under the preregistered criterion.

No weaker post-hoc p-value or effect threshold is substituted.

### NOT_ESTIMABLE

The frozen environmental reconstruction or sample-support gate does not provide
the registered test.

Licensed interpretation:

> the perturbation test remains unresolved under the frozen design.

No product, interval, tolerance, target rule, or sample-support threshold is
changed to rescue estimability.

## 8. Technical failure versus scientific result

These are scientific workflow completions:

    PASS
    FAIL_WRONG_DIRECTION
    FAIL_INSUFFICIENT_SUPPORT
    NOT_ESTIMABLE.

These are technical failures:

- credential/authentication error;
- network/task failure;
- source/hash mismatch;
- contract mismatch;
- malformed extraction output;
- software exception.

A scientific FAIL must not be converted into a failing GitHub Action merely
because the biological prediction failed.

## 9. Required final artifact

The workflow uploads:

    payoff-b-aikens-appeears-full-extraction

including:

- exact manifest / source receipts;
- AppEEARS submission receipt;
- merged MOD09Q1/MOD10A2 tables;
- V061 IRG input and peak-IRG receipts;
- fixed GPS target receipt;
- pre-environment support ceiling;
- target-level phase validity receipt;
- adjacent valid phase-pair receipt;
- lambda fit / observation / result receipts;
- claim-state receipt;
- rendered GEB manuscript;
- GEB submission audit;
- frozen amendments / execution contracts.

## 10. Post-run rule

After one valid authenticated run:

1. freeze the workflow run ID, artifact ID, artifact digest and head SHA;
2. freeze the scientific result receipt unchanged;
3. update the canonical manuscript from the outcome-blind renderer output;
4. do not rerun with altered scientific thresholds;
5. any rerun is allowed only for a documented technical failure using the same
   frozen analysis contract.

## 11. Current claim state

Before authenticated execution:

    AIKENS_LAMBDA_OUTCOME:
        UNOPENED

    PRE_ENV_SUPPORT:
        PASS

    ENVIRONMENTAL_EXTRACTION:
        BLOCKED_BY_AUTHENTICATION

    FOURTH_TAXON_EXPANSION:
        HOLD

The Aikens perturbation is the preferred next empirical test because it
interrogates whether an externally constrained actuator changes lambda within a
taxon, rather than adding another taxon mechanically.
