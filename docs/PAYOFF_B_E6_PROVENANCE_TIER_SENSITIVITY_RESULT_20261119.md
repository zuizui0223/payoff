# PAYOFF-B E6 — source-origin tiers and already-published temperature-response gradient

Date: **2026-11-19**. Status: **POST-OPEN NESTED SOURCE-PROVENANCE SENSITIVITY**, **not** independent meta-analysis or a new migration information mechanism.

## Motivation and original data identity

The previously promoted Usui et al. (2017) E6 result had 944 source temperature effects from 28 studies, including **264 known original eBird-dependent effects from Hurlbert & Liang (2012)**. The frozen E6 study×species two-way cluster-robust inverse-variance WLS is reproducible from GitHub Actions original artifact **10953792024** (archive SHA256 `443cab62531d9b633aa6ee67d7baa128043c0c454b4e57885118dff5820f2656dd`). Raw Usui source SHA256 `68816f6cbfccbb9b47b45be0df49f077db914c8e43e567d0ed2cac9bbafde56c`.

Study source verification is based on **original paper methods, published institutional collection descriptions and a source-identifier matching ledger**, not on sign/magnitude of the original temperature-response coefficients. This audit is *after* the original E6 effect was opened, hence must not be treated as a new prospective validation.

## Four nested descriptive panels, identical model formula

| Source inclusion | Source effect rows | Studies | Long−short temperature response (days/°C) | 95% cluster-robust CI |
|---|---:|---:|---:|---|
| Original E6, **includes known eBird source**, provenance only | 944 | 28 | **+0.421476** | [+0.121326, +0.721627] |
| Remove one positively verified eBird study | 680 | 27 | **+0.608389** | [+0.361817, +0.854961] |
| Keep only study samples with published local or named primary observation sources | 676 | 26 | **+0.601850** | [+0.354372, +0.849327] |
| Further exclude Rubolini 2007 and Ahola 2004 (**6 rows**) because the field-log custodian remains insufficiently documented | 670 | 24 | **+0.623883** | [+0.371402, +0.876364] |

Uncertainty uses exactly the already-frozen inverse-variance WLS fit with study×species two-way cluster-robust covariance and conservative Student-t df = min(studies,species)−1. The covariate matrix remains arrival metric, temperature location, arrival location, data source and continent. No interaction, family selection, direction-dependent screen or new taxonomic group pooling is introduced.

**Interpretation:** the sign of the already published long−short phenological temperature-response difference is stable across these nested *same-source* provenance restrictions. This provides a robustness/lineage audit, **not** new independent ecological replication or a proof that long-distance migration causes less access to future climate information.

## Remaining provenance uncertainty

- **4 original effects from Zalakevicius (2002), GeoJournal 57:183–193, Lithuania:** original article abstract does not specify one unambiguous original arrival-observation database/record custodian. These are **SOURCE_UNVERIFIED** and excluded from the 676 panel. Do not replace their source by a guessed Lithuanian monitoring station.
- **6 effects from Rubolini et al. (2007; Italy, 4 effects) and Ahola et al. (2004; Finland, 2 effects):** the published articles describe original site-level seasonal series, but raw field-log custodian and any ancillary sources are not independently verified. Present in 676, absent from 670.
- **670 effects from 24 other original studies** have specifically documented observational programmes or field-record types; **this still does not certify every auxiliary source stream or paper-specific extracted effect as fully eBird independent**. The full text/supplement source inspection is not uniformly possible.
- The panel can therefore be described as **known eBird study excluded, with graded original source provenance**, not as a completely verified eBird-free meta-analysis.

## Ecological boundary

A predictor measured at a research location does **not** establish that a migrant observed that temperature before a seasonal commitment decision. The parent [E6 temperature-location support gate](../docs/PAYOFF_B_CROSS_SYSTEM_INFORMATION_RESULT_20260928.md) and [new PR #403](https://github.com/zuizui0223/payoff/pull/403) show that at most two source studies cross both short/long migration and breeding/passage temperature locations. The predeclared ≥5-study admission gate fails. There is **no** robust, independently supported source-level causal information-distance effect; no actor-level deadline, recourse, feedback, performance, or interactor timing is estimated.

The original V7 goose `historical q × geography-only urgency U` still lacks original year-specific spring-onset and source-station region boundaries, and remains `NOT_ESTIMABLE`.

## Independent original data and reproducibility

- The effect rows are from the exactly checksum-verified 2026-09-28 E6 GitHub artifact; no raw eBird checklists or records were downloaded in this correction.
- Source inventory: `scripts/payoff_b_e6_source_origin_inventory.py` and `docs/PAYOFF_B_E6_STUDY_ORIGIN_PARTIAL_AUDIT_20261119.md`.
- Numerical refit script: `scripts/payoff_b_e6_provenance_tier_sensitivity.py`; synthetic and original-archive CI regression tests: `tests/test_payoff_b_e6_provenance_tier_sensitivity.py`.
- Dedicated workflow `.github/workflows/payoff-b-e6-known-ebird-exclusion.yml` downloads the **same** immutable GitHub E6 artifact, verifies its exact ZIP and contained CSV SHA256, refits all nested source panels, and uploads derived JSON **without** redistributing the excluded eBird source data.

No frozen main paper or original V7 protocol is amended. Keep PR as Draft until CI verifies source-tier archive results and source citations are reviewed.
