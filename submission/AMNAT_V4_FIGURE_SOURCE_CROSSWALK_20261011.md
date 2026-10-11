# The American Naturalist — Paper 2 main-figure evidence and provenance lock

**Date:** 2026-10-11
**Status:** proposed four-figure editorial plan only. No publication figures are asserted generated, validated or deposited by this file.
**Source:** manuscript/PAYOFF_B_INFORMATION_CONTROL_V4_V8_INTEGRATED.md on PR #326.
**Journal:** The American Naturalist, Major Article; at most six combined figures/tables in main text. Figure legends generally <=100 words.

## Proposed Figure 1 — The serial timer and controller (theory, not natural evidence)

Show a biological entry/readiness threshold, the signed phase-error state, route-stage cue acquisition, and subsequent feasible positive/negative corrections. Distinguish:
- informative cues vs *usable* decision-time cues;
- an initial timing deviation vs downstream phase-retention mechanisms;
- physical actionability vs the ecological incentive to exercise it;
- the exact two-actor no-innovation identity
  Delta_n = ((lambda_1^n+lambda_2^n)/2) Delta_0 + (lambda_1^n-lambda_2^n) m_0.

**Source:** manuscript theory sections 2.1–2.8; docs/PAYOFF_B_V3_FIGURE_ARCHITECTURE_20261003.md; corresponding mathematical/source scripts as documented in that theoretical program.

**What the figure may NOT imply:** direct measurement of an animal's posterior cue belief, true physiological readiness gate, or experimentally identified information value. All q/r routes are schematic or synthetic. In particular, free optional information cannot have negative optimal individual value under unchanged options.

**Renderer state:** no verified final publication file or full legend available on this PR.

## Proposed Figure 2 — Environmental connectivity moved opposite to the registered hypothesis

Display registered earlier/later signed detrended green-up correlations and pair-level change, not a fictitious species-independent sample. Source-range mapping is geographical, not an observed individual's path.

**Frozen outcomes:**
- 166 unique spatial source–target pairs from 28 bird species;
- early 2002–2009, late 2010–2017;
- mean unique-pair delta-rho +0.3690 (95% pair bootstrap +0.2984 to +0.4365);
- equal-species exposure mean +0.3364 (+0.2628 to +0.4312);
- 26/28 species mean signs positive.

**Sources:** 
- Frozen primary/sensitivity outcome receipts are documented in the linked result file; no checked-in JSON matching the former example filename exists on this branch. Recover exact numeric plotting inputs from the verified CI artifact and registered analysis, not an invented repository path;
- docs/PAYOFF_B_V8_PRIMARY_AND_SENSITIVITY_RESULT_20261005.md;
- docs/PAYOFF_B_V8_DEPENDENCY_CORRECTION_20261005.md;
- analysis/movement_phenology/payoff_b_v8_primary.R.

**Allowed:** the registered broad degradation hypothesis was not supported, and the sign instead went positive.

**Forbidden:** climate change was uniquely responsible for the change; individual birds received better information; cross-site correlation is demonstrated cue calibration.

**Renderer state:** result/analysis source paths established; final figure/checksum unverified.

## Proposed Figure 3 — Transfer to bird matching was unsupported and subject to a structural null

Panels: pair-/species-aware scatter and CI of the registered transfer estimate; overlay fixed-bird-arrival null and the within-window permutation distribution as separate representations.

**Frozen outcomes:**
- 150 species–target rows, 72 unique environmental pairs, 22 species;
- registered transfer beta +0.06244, CI -0.01411 to +0.13635 (negative direction NOT_SUPPORTED);
- fixed-arrival null beta +0.04742, observed-minus-null increment +0.01502 (CI -0.05212 to +0.10273);
- arrival-permutation null median +0.04677; 2,000 within-window permutations.

**Sources:**
- docs/PAYOFF_B_V8_DOWNSTREAM_TRANSFER_PRIMARY_RESULT_20261005.md;
- docs/PAYOFF_B_V8_TRANSFER_STRUCTURAL_NULL_RESULT_20261005.md;
- analysis/movement_phenology/payoff_b_v8_downstream_transfer_primary.R;
- analysis/movement_phenology/payoff_b_v8_transfer_structural_null_audit.R.

**Allowed:** larger connectivity gains failed to predict the registered improvement in matching.

**Forbidden:** the positive observed slope establishes worse bird tracking caused by improving predictability, a decline in individual fitness, or failure to perceive better information.

**Renderer state:** final figure/checksum unverified.

## Proposed Figure 4 — Same-population mule-deer phase changes and mechanism ceiling

Panels: full 152-animal-year paired start/end signed Days-From-Peak distribution; signed speed and stopover associations; a separate **conservative** predeparture-condition subset (not treated as all 152 records).

**Frozen descriptive results:**
- 152 animal-years / 72 adult female deer; variance ratio 0.2489, CI 0.1667 to 0.3617;
- within-year variance ratio 0.2940, CI 0.2060 to 0.4049;
- 107/152 animal-years finished closer in absolute phase;
- March IFBFat predeparture subset 62 animal-years / 40 deer; later stopover sample smaller;
- condition-by-incoming-phase interaction on speed and stopover NOT SUPPORTED.

**Sources:**
- Ortega et al. (2023), publicly released supplementary workbook 41467_2023_37750_MOESM4_ESM.xlsx, SHA256 in docs/PAYOFF_B_ORTEGA_VARIANCE_FUNNEL_RESULT_20261003.md;
- scripts/payoff_b_ortega_variance_funnel.py;
- scripts/payoff_b_mule_deer_two_clock_channel.py;
- docs/PAYOFF_B_ORTEGA_VARIANCE_FUNNEL_RESULT_20261003.md;
- docs/PAYOFF_B_MULE_DEER_TWO_CLOCK_CHANNEL_RESULT_20261003.md;
- docs/PAYOFF_B_MULE_DEER_H2_PROXY_RESULT_20261003.md.

**Allowed:** quantitative descriptive phase convergence and oppositely signed actuator associations reproduce and extend the published-source portrayal.

**Forbidden:** distinct latent cue/response gains separately estimated; IFBFat causally gates reactive phase control; compensation necessarily improved survival/reproduction; original Ortega discovery credited to PAYOFF-B.

**Renderer state:** final figure/checksum unverified.

## Prior-art and negative evidence for text/supplement only

Usui 944 source-table effects; wigeon prospective null; two unsuccessful information-reversal gates; godwit, pink-footed goose, American-redstart, pied-flycatcher and great-tit literature examples belong in transparently sourced narrative/supporting text, not as additional unvalidated causal figure panels. The American-redstart movement vs survival estimates came from **different individual samples** and must not be combined into one data panel implying a direct speed–survival link.

## Reviewer package final gates

- Verify each cited path actually exists and each final panel can be recreated from fixed source bytes/code, with a run manifest, versions, plotted points and confidence interval procedure.
- Match every panel to exactly one main-text result and its preregistered or post-freeze epistemic status.
- No post-hoc adjustment of data windows, sample inclusion, or plotting groups to rescue a negative hypothesis.
- Supply title, full author-year Literature Cited, complete source citations and DOI, legends under journal guidance, line-numbered double-spaced anonymous main PDF, private reviewer-accessible data/code archive and README.
- Do not claim **SUBMISSION_READY** until files, anonymization and source archive have been verified. Source-only methods edits do not meet these requirements.
