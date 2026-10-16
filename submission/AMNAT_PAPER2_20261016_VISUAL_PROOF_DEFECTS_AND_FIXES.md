# Paper 2 anonymous PDF: independent visual editorial findings and repair contract

**Date:** 2026-10-16. **Status:** VISUAL DEFECTS VERIFIED / corrected source pushed / new PDF CI pending. This is an editorial consistency audit; the original V8, S2/S3 and Ortega scientific results, tests and exploratory-status classification are unchanged.

## Exact original material inspected

Recovered the canonical scientific-review artifact from [run 38699554487](https://github.com/zuizui0223/payoff/actions/runs/38699554487/artifacts/11955491813). Inspected all four original contact sheets covering **41 pages** and expanded the title, theory, case-study prose and figure pages (1, 5, 10, 14, 17, 25, 33, 35–41) directly from the recovered PDF. Original 41-page PDF SHA256: `0b04ff4ccadf96b1c6a6b61789ebba4d6797923c50ab45c1bf5ecb1c93488226`.

The previous all-page CI only checked mechanical clipping, empty pages, glyph substitution, image count and identifying metadata; it had **not** checked figure-page isolation, correct source labels or malformed anonymization grammar. These failures were visible despite that CI passing.

### Confirmed original defects

1. Original page **39** has headings **Figure 2**, **Figure 3**, **Figure 4** without the corresponding figures; the images were typeset on following pages. A claim also states all panels are only source-frozen summaries rather than plots of actual source–target pairs.
2. Original page **40** contains both empirical Figure 2 and Figure 3, each occupying only part of the paper page with small data-axis labels. Figure 2–3 legends are literally `Source-frozen Figure N summary preview`, which is **false** for the independently source-verified 166 original environmental pair rows and 150 species-target bird rows.
3. Original page **33** says `after the present the bird-data test integration`, a sentence corrupted by the automatic V8-token pseudonymization. The operational discussion of a prior Dryad HTTP 401 download attempt is out of place in the ecological argument. The underlying source-admission limitation remains recorded in project-side audit files and is **not** erased from scientific provenance.
4. The figure legend for Figure 4 remains appropriately *descriptive* (Ortega published-source 152 animal-years/72 deer); Figure 1 remains *theoretical*. These must not be relabeled observed individual-cue/fitness tests.

## Exact non-statistical repairs

- `scripts/build_amnat_v4_anonymous_preview.py`: one **nonfloating**, full-width empirical figure per page using LaTeX `\\clearpage` and `\\includegraphics`, with genuine distinct captions and an explicit evidence-type distinction.
- `manuscript/PAYOFF_B_INFORMATION_CONTROL_V4_V8_INTEGRATED.md`: remove one obsolete internal HTTP 401 source-admission paragraph while preserving the original registered findings, design, numerical values and all cited social-cue prior art. Operational provenance remains in independent source-gate documentation.
- `scripts/audit_amnat_v4_figure_page_and_caption_qc.py`: new PDF-content gate checks four separate image-bearing pages, each with the matching caption *on the same page*, exact source-group units (166 pairs, 150 bird species-target observations, 72 environment pairs, 152 animal-years), preservation of S3 scientific context, and absence of the misleading summary-only footer and source-access paragraph.
- The final source-replayed anonymous 75-file S3 archive workflow now **requires and includes** the figure-layout-specific QC JSON. Scientific replay is still required; the new journal archive is NOT deemed submitted or author-approved by CI.

## Editorial remaining gates

- Rebuild and verify the full anonymous PDF and reviewer-candidate ZIP from the scientific source branch; old 41-page PDF should not be presented as the final visually corrected document.
- Reinspect all figure pages from the new PDF. Human author final full-resolution proofreading, copyright/permissions, anonymous reviewer deposit and author declarations remain separate, human approval and external journal actions.
- No reanalysis of environmental/bird/deer source records, no late hypothesis selection and no causal information-use claim is authorised by this visual-proof repair.
