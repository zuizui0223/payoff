# Oikos submission requirements audit — PAYOFF-B tracking theory

Checked: **2026-09-24**

This audit records current Oikos / Nordic Society Oikos submission requirements
relevant to the frozen PAYOFF-B tracking-theory package.

Official sources:

- https://nso-journals.org/oikos-for-authors
- https://nso-journals.org/author-guidelines

## Article type and fit

Prepare as an **Oikos Research Paper**.

Oikos Research Papers report original research across ecology and should target
a broad ecological readership. Oikos explicitly welcomes new theory and gives
priority to work that can change or substantially improve understanding of
ecological mechanisms, processes or patterns.

Tracking-paper fit:

- theoretical research: yes;
- ecological mechanism rather than taxon extension: yes;
- broad mechanism: adaptive capacity versus unilateral accessibility;
- named-species empirical calibration: intentionally not required for this
  synthetic theory manuscript.

## Initial-submission file structure

### 1. Title page file — separate

Must contain:

- manuscript title;
- author list;
- affiliations.

Author details are also entered in ScholarOne.

Current repo file:

- `submission/PAYOFF_B_TRACKING_TITLE_PAGE_TEMPLATE.md`

Status: **template ready; verified author metadata still required.**

### 2. Main text file — anonymous

Oikos uses **double-anonymized peer review**. The main text file must contain no
author names or affiliations.

First page:

- title;
- abstract.

Introduction begins on page 2.

Current repo file:

- `manuscript/PAYOFF_B_TRACKING_THEORY_V1.md`

Status: **scientific content frozen; export must preserve anonymity.**

### 3. Abstract

Requirement:

- no more than **300 words**;
- summarizes the main results;
- no references;
- no unexplained abbreviations/acronyms.

Action before portal upload:

- run a word-count contract on the frozen abstract;
- expand all unexplained abbreviations if any;
- do not add literature citations to the abstract.

### 4. Main-text formatting

Initial submission may use flexible formatting provided it is suitable for
double-anonymized review.

Required/recommended:

- single column;
- double-spaced;
- continuous page numbers;
- continuous line numbers;
- no more than 3 heading levels.

Action:

- these are export/layout requirements, not scientific edits.

### 5. Figures

At initial submission, figures can be embedded in the main text and/or uploaded
separately; embedding is preferred for peer review.

Current package:

- six audited SVG figures;
- separate caption file.

Action:

- retain vector masters;
- export peer-review copies in the format accepted by the submission system;
- if figures are embedded for review, do not alter scientific content.

### 6. Data and code

If a manuscript relies on data and/or custom code, Oikos requires these at
**initial submission** either as uploaded anonymous review files or through an
anonymous repository link.

After acceptance, data/code must be public in a suitable archive and citable
with a persistent identifier such as a DOI.

Current package:

- frozen synthetic JSON receipts;
- theory documents;
- scripts and tests in repository;
- deterministic submission ZIP with SHA256 manifest/receipt.

Action:

- for first submission, prepare an anonymous review-access route for code and
  synthetic data;
- before/after acceptance as required, mint a persistent archive DOI.

### 7. Data Availability Statement

Required at submission.

Draft only after the actual anonymous archive/review-access route is chosen.
Do not insert a fake DOI or repository URL.

### 8. AI-use disclosure

NSO requires authors to disclose which AI tools were used and for what purpose,
following Wiley AI guidance. The statement is added at the end of the main
text.

Current status:

- **required administrative disclosure not yet finalized**.

Use a verified factual statement only. It should describe the actual use of
AI-assisted drafting, coding, editing, or other tasks as applicable, and state
the authors' responsibility for validation and final content. Do not list an AI
tool as an author.

### 9. Supporting Information

Supporting information should be uploaded as separate file(s). It is published
as received and is not copy-edited.

Current repo:

- `submission/PAYOFF_B_TRACKING_SUPPLEMENT_MAP.md`

Status:

- supplement structure S1–S6 is frozen;
- a portal-ready Supporting Information document still needs to be assembled
  from those frozen contents.

This is **packaging work only**; it must not introduce new simulations.

### 10. ORCID and CRediT

- corresponding author must provide ORCID at submission;
- co-author ORCID linkage is strongly encouraged;
- CRediT roles are mandatory by revision, although not required for initial
  submission.

Current title-page template already includes placeholders.

### 11. Conflict, ethics, funding and acknowledgments

ScholarOne requires statements/fields covering:

- conflict of interest;
- ethics, if applicable;
- funding;
- acknowledgments;
- significance of the research;
- data availability.

These are author/admin metadata. Do not infer them from repository contents.

## Oikos-specific remaining checklist

Scientific analysis is frozen. Remaining Oikos preparation tasks are:

1. assemble a portal-ready Supporting Information file from S1–S6;
2. create anonymous main-text export with page + continuous line numbers;
3. verify abstract <=300 words and citation/acronym rules;
4. prepare anonymous code/data review-access route;
5. finalize Data Availability Statement;
6. finalize factual AI-use disclosure;
7. fill title-page author/affiliation/ORCID metadata;
8. enter conflict/funding/ethics/acknowledgment fields in ScholarOne.

None of these tasks justifies new synthetic parameter sweeps.
