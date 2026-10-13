# PAYOFF-B Paper 2 — source-frozen figure-preview execution receipt

Date: 2026-10-13
Status: **SUMMARY_FIGURES_VERIFIED / SUBMISSION_HOLD**
Head commit: f332c591765927f6bc776e2fa3a14bab9484cf78
Draft PR: https://github.com/zuizui0223/payoff/pull/327
Unchanged scientific base: PR #326 (analysis/payoff-b-paper2-reviewer-claim-boundaries-20261011)

## Executed and verified

GitHub Actions run: https://github.com/zuizui0223/payoff/actions/runs/38361963848

- Dedicated renderer/unit CI conclusion: SUCCESS
- Source-reading/source-drift/determinism/inference-limit tests: 6 PASSED
- Renderer output status: VERIFIED_SUMMARY_FIGURE_PREVIEW_SUBMISSION_HOLD
- 4 source-bounded, deterministic SVG images (Figure 1 theoretical schematic; Figures 2–4 frozen summary data)
- LEGENDS.md with four captions
- TABLE_S1_ACTUATORS.md with frozen mule-deer speed and stopover coefficients and their clustered intervals
- figure_manifest.json with input-file SHA256 and image SHA256
- deterministic ZIP enclosing the same seven preview files

Uploaded artifact:
https://github.com/zuizui0223/payoff/actions/runs/38361963848/artifacts/11794833776

Artifact ID: 11794833776
Artifact-archive SHA256 as reported by GitHub Actions: 91c63524310676d86171d1544f86840e441f44b0a807be3fe9b5ba62dd6134f8
Artifact upload: 8 files (7 outputs plus deterministic preview ZIP).

**This verifies software output construction, not the visual quality of a rendered publication page, or microdata/independent source regeneration.**

## Evidence and figure limits

1. Figure 1 is schematic and does not identify real animal beliefs, readiness or fitness.
2. Figure 2 plots two frozen summary means and 95% pair-bootstrap intervals: 166 unique environmental pairs and equal-species exposure over 28 species. It does NOT show 166 observed pair points or prove improved migrant-perceived information.
3. Figure 3 shows the unsupported registered transfer (beta +0.06244), a fixed-arrival environmental-geometric null (+0.04742), and no detected bird-specific increment (+0.01502; CI spans 0). The permutation null is text with a central range, not a CI. Positive transfer is not a causal worsening bird response.
4. Figure 4 plots the source-frozen Ortega mule-deer descriptive phase summaries and variance ratios (152 animal-years / 72 animals). TABLE_S1 lists speed/stopover coefficient estimates from the *same* frozen receipt without inventing individual trajectories or conditioning on lifetime fitness.
5. No V3/V7R/V8 preregistered outcome was changed; no new ecological effects were fitted.

## Submission status still blocked by explicit omissions

- Complete Literature Cited, author-year in-text reference verification and data DOI checks.
- Source-verified individual and pair-level input records, immutable hashes and rerun scripts, with an anonymous reviewer-accessible archive. Frozen numerical summaries alone do not reproduce the underlying biological fits.
- Visually inspected high-resolution/publishing-quality figures, final legend language/figure numbering.
- Double-spaced line-numbered anonymous manuscript PDF.
- Real author metadata, funding/COI/contribution and AI-use disclosure, approved for the destination journal.

Do not call this artifact a complete anonymous review ZIP, a full data/code repository, a published submission package, or a natural information-deadline mechanism confirmation.
