# GEB movement–phenology submission readiness

Status date: 2026-09-21.

## Scientific gates

~~~text
broad universal-optimum test:
  COMPLETE — universal natural optimum not supported

direct phase-retention taxa:
  3 — PASS

within-species route replication:
  PASS — three barnacle-goose flyways

prospective third-taxon test:
  PASS for lambda < 1
  FAIL for stronger |lambda| < 0.75 forecast

common reactive actuator:
  NOT SUPPORTED / intentionally not claimed

environmental-information vs feedback separation:
  PASS as mechanistic decomposition
  positive predictability -> stronger feedback hypothesis NOT supported

quantitative actuation perturbation:
  PASS for cross-sectional attenuation
  stronger longitudinal deterioration prediction NOT supported

structured GEB novelty screen:
  PASS with conservative wording
~~~

## Submission-format gates

~~~text
structured abstract:
  PASS

abstract <=300 words:
  PASS

keywords 6–10:
  PASS

display pieces 6–8:
  PASS

blinded-text identity scan:
  PASS

citation/reference consistency:
  PASS

reference core:
  PASS for initial-submission completeness;
  final copy-edit bibliography expansion may still be useful

figure build:
  PASS

figure manual QA:
  PASS for current Fig.4 and Fig.5

figure mechanical QA:
  IMPLEMENTED — CI result required on latest head
~~~

## Human-input gates still open

~~~text
final author list / order
affiliations
corresponding author
funding
conflicts of interest
CRediT contributions
acknowledgements
anonymous reviewer hosting / access test
all-author approval
portal metadata
~~~

## Submission route

Primary:

> **Global Ecology and Biogeography — Research Article**
>
> Special issue: **Scaling Up Individual-Based Ecology: Macroecological Insights Gained from the Biologging Revolution**

Working title:

> **Migration timing as phase control: environmental information and phase retention across migratory taxa**

## Current go/no-go

~~~text
SCIENCE:
  GO

MANUSCRIPT STRUCTURE:
  GO

BLINDED MAIN-TEXT FORMAT:
  GO

FIGURES:
  GO — latest mechanical QA PASS

HUMAN METADATA:
  OPEN

ANONYMOUS REVIEWER SNAPSHOT BUILD:
  GO — CI-built, identity scan PASS, immutable checksum recorded

ANONYMOUS REVIEWER HOST / ACCESS TEST:
  OPEN

PORTAL SUBMISSION:
  NOT YET
~~~

The project is now in submission assembly rather than exploratory analysis.


## Reviewer-snapshot assembly receipt

The anonymous reviewer package is now generated reproducibly by:

~~~text
scripts/build_movement_phenology_reviewer_snapshot.py
.github/workflows/build-movement-phenology-reviewer-snapshot.yml
~~~

Latest validated package:

~~~text
files = 74
identity / secret hits = 0
raw tracking data included = false
Git history included = false
title page included = false
public author-repository link included = false

archive SHA-256 =
f3d1a08f746f0c5dc81d49261c11855a200a1f0327154711f506c266de120ce4
~~~

This closes the snapshot-construction blocker. The remaining reviewer-code
blocker is external delivery only: place the frozen archive on an anonymous
reviewer-access host and verify that opening the link does not expose account
ownership.
