# Theoretical Ecology portal handoff — PAYOFF-B

This file freezes the current journal-facing submission requirements without expanding the theorem.

## Target and article-type routing

```text
JOURNAL = Theoretical Ecology
SCIENCE_SOURCE = manuscript/PAYOFF_B_THEORETICAL_ECOLOGY_BRIEF_V1.md
PREFERRED_SHORT_FORMAT = Brief Communication, only if offered by the live portal
FALLBACK_PORTAL_TYPE = Original Paper
```

The current public Submission Guidelines do not list a separate Brief Communication format, although the journal has published Brief Communications historically. Therefore do not block submission on the label. If the live submission portal offers Brief Communication, use it. If it does not, select Original Paper and submit the same concise theorem manuscript rather than forcing an obsolete article type.

## Current mandatory preparation requirements

- Word manuscript plus a PDF version when submitting Word;
- concise title;
- title page containing author names, affiliations, corresponding-author email, and ORCID(s) where available;
- abstract between 150 and 250 words;
- 4–6 keywords;
- automatic page numbering;
- editable source files;
- Statements and Declarations covering at least funding and competing interests, plus other relevant declarations;
- author contribution and competing-interest information entered in the submission interface;
- five potential reviewers suggested in the cover letter.

## Submission-source overlay

The frozen science manuscript remains the theorem source. `scripts/build_payoff_b_submission_source.py` creates the journal-facing pre-metadata source by:

1. removing the internal `Target:` line;
2. expanding the abstract just enough to satisfy the current 150-word lower bound without changing the result;
3. inserting the title-page metadata template;
4. appending the Statements and Declarations template.

The overlay must not change the proof, prior-art boundary, asymptotics, or figure claims.

## Human-controlled fields

Before actual upload, replace every author-control token in:

- `submission/PAYOFF_B_TITLE_PAGE_TEMPLATE.md`;
- `submission/PAYOFF_B_DECLARATIONS_TEMPLATE.md`;
- `submission/PAYOFF_B_COVER_LETTER_V1.md`.

Required human decisions include:

- author list/order;
- affiliations;
- corresponding author and active email;
- ORCIDs;
- acknowledgments;
- funding/grant statement;
- competing interests;
- author contributions;
- exact AI-use disclosure;
- five real reviewer suggestions with conflict checks;
- all-author approval;
- confirmation of no simultaneous submission.

## AI transparency

The current journal instructions state that LLM use beyond AI-assisted copy editing should be documented in the Methods section or a suitable alternative part of the manuscript. The declarations template therefore contains an author-review-required disclosure starting point. Do not submit it unchanged unless it accurately describes actual use.

## Claim ceiling

The submission may claim only:

- one unique positive migration optimum for every nonzero contrast in the declared symmetric two-patch/two-season anti-phase model;
- the one-parameter scaling curve `u*(v)`;
- the weak-contrast constant and strong-contrast asymptotics.

It may not claim the known closed-form growth exponent as new, nor general uniqueness for arbitrary periodic, asymmetric, stochastic, multi-patch, or nonlinear systems.

## Final gate

```text
SCIENCE = FROZEN
JOURNAL_REQUIREMENT_OVERLAY = AUTOMATABLE
ABSTRACT_150_250 = MUST_PASS_GENERATED_SOURCE
KEYWORDS_4_6 = MUST_PASS_GENERATED_SOURCE
DECLARATIONS = TEMPLATE_READY_AUTHOR_CONFIRMATION_REQUIRED
TITLE_PAGE = TEMPLATE_READY_AUTHOR_METADATA_REQUIRED
COVER_LETTER = READY_EXCEPT_AUTHOR_CONFIRMATION_AND_REVIEWERS
REVIEWER_SUGGESTIONS = FIVE_REQUIRED_EXTERNAL_INPUTS
ARTICLE_TYPE = CHECK_LIVE_PORTAL
ALL_AUTHOR_APPROVAL = REQUIRED
PORTAL_UPLOAD = REQUIRED
```
