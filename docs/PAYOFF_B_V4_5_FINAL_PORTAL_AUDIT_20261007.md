# PAYOFF-B V4.5 final portal audit — 2026-10-07

Status: **INDEPENDENT ARTIFACT QA PASSED — SCIENCE CLOSED**

This audit was performed after the final green-build receipt and portal handoff.
It does not reopen any ecological or statistical analysis.

## 1. Anonymous review DOCX — independent render QA

Artifact:
- workflow run: 37562979913
- artifact id: 11457418624
- digest: sha256:29d51b8a0d6038190de76603cf7ccf55261b23d19da3ebb6c74d4a49a4ae5f9a

The artifact was downloaded, extracted and independently rendered with the
repository-external DOCX rendering workflow.

Rendered pages:
**30**

All 30 pages were visually inspected.

Passed:
- anonymous title page;
- title / short title / six keywords / word count / article type / manuscript
  elements present;
- Abstract starts on its own page;
- main text starts on its own page;
- continuous line numbers visible;
- page numbers visible;
- double-spaced review layout;
- equations readable;
- no text clipping;
- no overlapping text;
- no orphan blank page;
- Methods precede Natural evidence;
- AI-assisted-development disclosure visible in Methods;
- Literature Cited followed by Figure Legends;
- all three legends present and legible.

No layout repair is required before portal upload.

## 2. Anonymous reviewer package — physical-content audit

Artifact:
- workflow run: 37562980001
- artifact id: 11456869372
- digest: sha256:4e790b88d90955a6318f291e8b67c9a6fcb4ce15aaecbce876b4f4f6f356823e

The archive was downloaded and extracted.

Reviewer-facing contents:
- anonymous manuscript source;
- Supporting Information;
- figure legends;
- Figure 1;
- Figure 2;
- Figure 3;
- package manifest.

Identity scan:
**PASS**

No occurrence was found for submitter name variants or the repository-account
identifier used in the private development repository.

Internal journal-facing label scan:
**PASS**

No PAYOFF-B / V4.5 / post-freeze / audit-branch labels were found in the
reviewer-facing package.

## 3. Anonymous reproducibility archive — physical-content audit

Artifact:
- workflow run: 37562808347
- artifact id: 11456844175
- digest: sha256:b190078595ee4ba4f026f600a1b8d26b068c7e21edb5a6f8f3924ee8e618975d

The archive was downloaded and extracted.

Contents include:
- manuscript-specific bird R scripts;
- mule-deer Python reanalysis scripts;
- analysis contracts;
- frozen figure-data manifest;
- selected tests;
- anonymous review README;
- manifest.

Identity scan:
**PASS**

No submitter name variant or private repository-account identifier was found in
the extracted archive.

Internal analysis filenames are retained for reproducibility and are not
journal-facing scientific claims.

## 4. Publication-status consistency

The Paper-2 status heading was corrected from the obsolete
ACCESS_BLOCKED wording to:

**PORTAL_READY submission state**

This is a documentation-only change after the frozen science build.

## 5. Current portal state

Scientific analysis:
**FROZEN**

Anonymous manuscript:
**PASS**

Main figures:
**PASS**

Supporting Information:
**PASS**

Anonymous data/code archive:
**PASS**

Repository-wide tests:
**PASS**

Remaining actions are human metadata / portal actions only:
- author order;
- affiliations;
- corresponding author and email;
- ORCID;
- funding;
- conflicts of interest;
- author contributions;
- acknowledgments;
- preprint declaration if applicable;
- upload files;
- inspect the portal-generated PDF;
- click Submit.

## Stop rule

Do not modify analysis, figures, claims or manuscript science during portal
entry unless the portal rendering reveals a real defect or a substantive
validity error is discovered.

Current state:
**READY_TO_UPLOAD — NO SCIENTIFIC OR PACKAGE BLOCKER**
