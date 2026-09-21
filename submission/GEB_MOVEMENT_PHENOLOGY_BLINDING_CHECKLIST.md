# GEB double-anonymous submission and reviewer-snapshot checklist

Status: executable handoff checklist. Do not mark a gate PASS until the corresponding artifact exists.

## A. Blinded main manuscript

Current source:

~~~text
manuscript/PAYOFF_B_MOVEMENT_PHENOLOGY_GEB_V2.md
~~~

Automated gate:

~~~text
scripts/audit_movement_phenology_geb.py
.github/workflows/audit-movement-phenology-geb.yml
~~~

Required before upload:

- [x] structured abstract present
- [x] abstract <=300 words
- [x] 6–10 keywords
- [x] 6–8 display pieces
- [x] author-year citation/reference consistency
- [x] no author name detected
- [x] no author email detected
- [x] no public author-identifying GitHub URL detected
- [ ] export final journal-upload file and re-run the same identity scan on the exported file

Do not add acknowledgements, author contributions, ORCIDs, affiliations or public author-owned repository URLs to the blinded manuscript.

## B. Separate title page

Template:

~~~text
submission/GEB_MOVEMENT_PHENOLOGY_TITLE_PAGE_TEMPLATE.md
~~~

Still requires human input:

- [ ] complete author list
- [ ] affiliations
- [ ] corresponding author
- [ ] funding
- [ ] conflicts of interest
- [ ] CRediT contributions
- [ ] acknowledgements

These fields must not be invented from repository history.

## C. Cover letter

Draft:

~~~text
submission/GEB_MOVEMENT_PHENOLOGY_COVER_LETTER_DRAFT.md
~~~

Before submission:

- [ ] confirm manuscript is not under consideration elsewhere
- [ ] confirm all authors approve
- [ ] replace editor/date/corresponding-author placeholders
- [ ] verify special-issue title against the current portal
- [ ] keep journal-significance paragraph <250 words

## D. Anonymous reviewer code/data snapshot

The public author-owned repository must not be the link supplied in the blinded manuscript.

Create a frozen reviewer snapshot containing only material needed to reproduce the submitted paper:

~~~text
manuscript/
  blinded submitted manuscript source

analysis/movement_phenology/
  scripts used by submitted results

scripts/
  figure builder
  manuscript and figure audits

data/
  derived registries only
  no restricted raw data

docs/
  source receipts needed to understand reconstruction and claim ceilings

environment/
  dependency lock or reproducible environment instructions
~~~

Exclude:

~~~text
.git history revealing author identity
unrelated PAYOFF modules
personal paths
emails
author names
private credentials
raw data whose licence forbids redistribution
~~~

Reviewer snapshot gates:

- [ ] anonymous/private reviewer link exists
- [ ] link opens without revealing account owner
- [ ] README reproduces Figures 4–5 and all promoted numeric receipts
- [ ] original public datasets are fetched from source DOIs rather than redistributed when required
- [ ] checksum / immutable snapshot identifier recorded internally
- [ ] public repository link withheld until unblinding / acceptance as appropriate

## E. Figure package

Automated figure build:

~~~text
scripts/build_movement_phenology_macro_figures.py
~~~

Automated QA:

~~~text
scripts/audit_movement_phenology_figures.py
~~~

Current manual visual QA:

~~~text
Fig.4 PASS
Fig.5 PASS
~~~

Before final upload:

- [ ] use the latest CI-generated PDF/SVG for vector submission where accepted
- [ ] confirm all final panel labels match manuscript legends
- [ ] verify no author-identifying metadata are embedded in exported files
- [ ] retain PNG at >=300 dpi for reviewer preview

## F. Claim-control freeze

The submission must preserve these negative results:

- broad 55-species test does **not** support one universal natural speed optimum
- wigeon supports lambda < 1 but **not** the stronger |lambda| < 0.75 forecast
- wigeon stopover and travel-speed actuator predictions are unsupported
- environmental predictability does **not** show the preregistered positive relationship with feedback strength
- industrial-development actuation contrast is supported, but the stronger longitudinal deterioration prediction is unsupported

Do not remove these outcomes to sharpen the story.

## G. Final go/no-go

Submission-ready when:

~~~text
GEB manuscript hard audit       PASS
figure hard audit               PASS
main scientific CI              PASS
title page                      COMPLETE
cover letter                    COMPLETE
anonymous reviewer snapshot     ACCESS TESTED
all authors                     APPROVED
~~~
