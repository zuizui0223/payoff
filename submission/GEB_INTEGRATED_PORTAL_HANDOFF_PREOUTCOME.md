# GEB integrated tracking ecology — portal handoff

Updated: **2026-09-25**

Status: **PREOUTCOME GEB OVERLAY; not final-submission eligible until Aikens adjudication**

## Routing

```text
JOURNAL = Global Ecology and Biogeography
ARTICLE_TYPE = Research Article
SCIENCE_SOURCE = manuscript/PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md
JOURNAL_OVERLAY = scripts/build_geb_integrated_preoutcome_source.py
```

## Current GEB requirements encoded by the overlay

- structured abstract <=300 words with exactly:
  Aim; Location; Time period; Major taxa studied; Methods; Results; Main conclusions;
- roughly <=5,000 main-body words;
- 6–8 display pieces;
- 6–10 alphabetized keywords;
- running title <40 characters;
- double-anonymous main text;
- separate title page;
- data/code access during peer review through an anonymous stable reviewer link;
- stable public archive at publication rather than GitHub alone;
- cover-letter interest paragraph <250 words.

## Generated blinded source

The builder produces a journal-facing source that:

1. removes internal Status / publication-architecture / evidence-boundary lines;
2. replaces the unstructured abstract with the GEB structured abstract;
3. keeps exactly one outcome-blind Aikens marker pair in the structured Results
   field and preserves the Results / Discussion / Conclusion marker pairs;
4. keeps the scientific Introduction–Conclusion unchanged except for moving the
   existing prior-art boundary into Discussion as
   “Relationship to existing literature”;
5. removes internal Figure architecture and Claim ceiling sections;
6. appends GEB-facing data/code availability text and six figure legends.

No numerical result is recalculated.

## PREOUTCOME hard gates

The GEB PREOUTCOME overlay may pass machine preparation while remaining
scientifically blocked from submission.

Required PREOUTCOME state:

```text
structured_abstract = PASS
abstract_words <= 300
main_body_words <= 5000
keywords = 6..10 and alphabetical
running_title_chars < 40
references <= 50
display_pieces = 6
anonymous_text = PASS
aikens_result = UNOPENED
final_submission_eligible = false
```

## Human / external actions after Aikens adjudication

- outcome-render the integrated manuscript and Figure 6;
- rerun the GEB overlay and post-outcome audit;
- create / verify anonymous stable reviewer archive link;
- populate separate title page, author order, affiliation, ORCID and
  corresponding-author metadata;
- confirm funding, competing interests, acknowledgements, CRediT and any
  ethics/permissions statements;
- choose conflict-checked suggested reviewers / handling editors if supplied;
- upload through the live Wiley portal.

Journal routing must not alter the frozen scientific claims.
