# GEB movement–phenology portal handoff

Status: **SCIENCE HOLD — DO NOT SUBMIT**  
Status date: 2026-09-22

The former submission-ready package is superseded. The source-faithful wigeon
Jan--Jul reconstruction changed both lambda and the stopover actuator result.
Submission is blocked until the frozen measurement-error calibration and
true-lambda=1 observation-scale null are completed. The historical V2
manuscript and reviewer snapshot must not be uploaded to the journal.

## Submission target

~~~text
Journal:
  Global Ecology and Biogeography

Article type:
  Research Article

Special issue:
  Scaling Up Individual-Based Ecology:
  Macroecological Insights Gained from the Biologging Revolution

Working title:
  Migration timing as phase control:
  environmental information and phase retention across migratory taxa
~~~

## Scientific state

The submission is no longer exploratory.

Core empirical results are frozen as:

~~~text
broad 55-species bird test:
  no universal natural movement/phenology speed optimum

direct phase-retention taxa:
  mule deer
  barnacle goose
  Eurasian wigeon
  -> three-taxon gate PASS

barnacle-goose route replication:
  Svalbard
  Greenland
  Barents
  -> within-species route gate PASS

prospective wigeon test:
  lambda < 1
  -> PASS

stronger preregistered wigeon forecast:
  |lambda| < 0.75
  -> NOT SUPPORTED

common reactive actuator:
  NOT SUPPORTED / NOT CLAIMED

information-versus-retention decomposition:
  PASS as organizing mechanism
  predictability -> stronger feedback prediction NOT SUPPORTED

industrial actuation perturbation:
  cross-sectional attenuation PASS
  stronger longitudinal deterioration NOT SUPPORTED
~~~

The manuscript should preserve these negative results explicitly.

## Primary submission files

Blinded manuscript:

~~~text
manuscript/PAYOFF_B_MOVEMENT_PHENOLOGY_GEB_V2.md
~~~

Cover letter draft:

~~~text
submission/GEB_MOVEMENT_PHENOLOGY_COVER_LETTER_DRAFT.md
~~~

Title-page template:

~~~text
submission/GEB_MOVEMENT_PHENOLOGY_TITLE_PAGE_TEMPLATE.md
~~~

Double-anonymous checklist:

~~~text
submission/GEB_MOVEMENT_PHENOLOGY_BLINDING_CHECKLIST.md
~~~

Submission checklist:

~~~text
docs/MOVEMENT_PHENOLOGY_GEB_SUBMISSION_CHECKLIST.md
~~~

Scientific readiness receipt:

~~~text
docs/MOVEMENT_PHENOLOGY_GEB_READINESS.md
~~~

Novelty boundary:

~~~text
docs/MOVEMENT_PHENOLOGY_SYSTEMATIC_NOVELTY_SEARCH_20260920.md
docs/MOVEMENT_PHENOLOGY_FLAGSHIP_NOVELTY_AUDIT.md
~~~

Direct-result audit:

~~~text
docs/MOVEMENT_PHENOLOGY_DIRECT_CONTROLLER_AUDIT.md
data/MOVEMENT_PHENOLOGY_DIRECT_CONTROLLER_REGISTRY.csv
~~~

## Reviewer-code snapshot

The reviewer snapshot is generated in CI by:

~~~text
scripts/build_movement_phenology_reviewer_snapshot.py
.github/workflows/build-movement-phenology-reviewer-snapshot.yml
~~~

Latest validated construction receipt:

~~~text
files included            = 74
identity / secret hits    = 0
raw tracking data         = excluded
Git history               = excluded
title page                = excluded
public author repo link   = excluded

archive SHA-256:
f3d1a08f746f0c5dc81d49261c11855a200a1f0327154711f506c266de120ce4
~~~

Before portal submission, place this exact frozen archive on an anonymous
reviewer-access host and verify the URL in a logged-out/private browser session.

Do not substitute a public author-linked GitHub repository URL in the blinded
manuscript.

## Human metadata still required

Do not infer or auto-fill these fields.

~~~text
final author list and order
all affiliations
corresponding-author identity and email
ORCID values if used
funding statement
conflicts-of-interest statement
CRediT contribution statement
acknowledgements
data/code availability wording after anonymous-host URL is known
all-author approval
portal-specific suggested/excluded reviewers if requested
~~~

The title-page template is the single source of truth for these fields.

## Portal sequence

1. Freeze the final author-approved manuscript text.
2. Fill the title page with final author metadata.
3. Fill funding / conflicts / CRediT / acknowledgements.
4. Upload the frozen reviewer snapshot to an anonymous host.
5. Test that URL while logged out and confirm it exposes no owner identity.
6. Replace the reviewer-code placeholder in the manuscript/data-availability text.
7. Run the GEB submission audit one final time.
8. Run figure QA one final time.
9. Confirm the blinded manuscript contains no title-page metadata.
10. Upload manuscript, figures, title page and required supplementary material.
11. Copy portal metadata from the title-page template rather than retyping from memory.
12. Preserve the final submitted files/checksums in a submission receipt.

## Claim ceiling for portal text

Use:

> We introduce a common empirical phase-retention coordinate for comparing how
> phenological deviation is transformed across ecologically meaningful movement
> intervals, and separate this retention from environmental timing innovation.

Do not use:

~~~text
first control theory of migration
universal migration optimum in nature
universal phase-control law
all migrants use reactive feedback
predictability causes stronger feedback
first evidence that migrants compensate for phenology
~~~

## Current repository go/no-go

~~~text
SCIENCE                            GO
BLINDED MANUSCRIPT                 GO
FIGURES                            GO
NOVELTY POSITIONING                GO FOR GEB
REVIEWER SNAPSHOT BUILD            GO
REPOSITORY CI                      GO

HUMAN METADATA                     REQUIRED
ANONYMOUS EXTERNAL HOST TEST       REQUIRED
PORTAL ACTION                      REQUIRED
~~~

No additional biological dataset is required for a first GEB submission under
the current claim ceiling.
