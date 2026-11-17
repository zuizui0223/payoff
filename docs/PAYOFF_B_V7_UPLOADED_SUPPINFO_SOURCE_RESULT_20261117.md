# PAYOFF-B V7: original Kölzsch et al. 2015 supporting DOCX — recovered historical q, partial admission, full primary still held

Date: 2026-11-17. **Directly inspected user-supplied original file** \`jane12281-sup-0001-suppinfo.docx\` (729,578 bytes, SHA256 **925e1e5921a4f005b55c5ffb60fa2958bcb29be8c56f4252cd00f66effe91e19**), article DOI 10.1111/1365-2656.12281. The source file is **not redistributed** in the GitHub repository; only aggregate numbers derived from its published tables and audit metadata are committed. The upload resolves the earlier *source DOCX inaccessible* status; it **does not** supply all missing annual spring and GPS regional inputs.

## 1. Exact original source contents — tables, figures and grain

Original DOCX structure: **7 Word tables** and **4 embedded raster figures**, approx. nine printed pages. The publisher labels the supplement S2–S7; the actual caption of the DOCX says **"Tables A2–A7"**. These are not annual site×year data tables.

- **Table S1, page 2:** 16 regional names; each 30-year mean GDD-jerk peak Julian day, original SD in days and average geese stopover duration where provided.
- **Pages 3–4, CORR tables:** 30-year Pearson correlations of spring-onset **anomalies** between region pairs. **23 numerical route-pair q values**: Greenland 7, Svalbard 5, Barents Sea 11. The values can serve as **published historical environmental q candidates** without using goose response dates to estimate q. \`r\` ranges **−0.38 to +0.97**, with four negative pairwise correlations.
- **Pages 3–5, SLOPES tables:** 23 published SMA/SMATR proportionality indices and 95% intervals, distinct from q=r. Some positive published slopes appear alongside negative correlations (four source pairs), and several slope-and-interval values recur across the flyways. We reproduce them as printed, **do not infer a sign correction**, and recommend checking methodological interpretation against the source manuscript before using s as the mandatory sensitivity.
- **Figures S1–S4, pages 6–9:** graph plots of annual regional GDD jerks and site/year GDD curves. **No machine-readable individual 1982–2011 Julian onset values per region per year** are present in this DOCX; the figure is not a source-certified numeric table. Do not assign values by guessing from coloured lines.

The 16 reported Table S1 regional means are **not** the year-specific \`S_{j,y}\` needed to compute registered migration timing error \`|A_{ij} − S_{j,y}|\`. Substituting \`mean(S_j)\` would change the estimand and conflate within-year climate variability with actual timing error.

## 2. The important difference: 23 pairwise coefficients, 13 adjacent route transitions

Route order from the three flyways and matching source tables, without using goose GPS responses:

| Flyway | All 30-year q pairs | Adjacent links | Adjacent q in travel order |
|---|---:|---:|---|
| Greenland | 7 | 4 | IRE→SIC **−0.10**; SIC→NIC **+0.85**; NIC→SGR **−0.38**; SGR→NGR **+0.50** |
| Svalbard | 5 | 3 | SCO→SNO **+0.53**; SNO→NNO **+0.81**; NNO→SVA **+0.45** |
| Barents Sea | 11 | 6 | NLDK→SWE **+0.89**; SWE→BALT **+0.97**; BALT→WS **+0.39**; WS→KAN **+0.72**; KAN→PEKO **+0.93**; PEKO→NSE **+0.53** |
| **Total** | **23** | **13** | |

Not every reported pair is an actual consecutive move: the other ten link nonadjacent region pairs and cannot be counted as independent observed consecutive stopover transitions without additional original migration records.

The codes **NLDK** and **NSE** appear in the Barents pair table but are **not an explicit Table S1 region-name dictionary**. Their probable Table S1 candidates are \`Central Europe\` and \`Novaya Zemlya\`; this is marked \`unverified_code_to_S1_region\` in the stored CSV. The remaining 11 adjacent pairs do not contain either uncertain code and have straightforward context-compatible regional candidate labels. **Even those code↔name expansions have not been validated against an original geospatial polygon shapefile.**

## 3. What frozen V7 gates now pass, and what still blocks the primary outcome

Frozen prospective V7 contract: \`docs/PAYOFF_B_V7_PREDICTABILITY_URGENCY_CONTRACT_20261005.md\`.

**PASS_Q_AGGREGATE_COUNT:** At least **13** adjacent forward-route historical Pearson r quantities are published, of which **11** do not require the two uncertain codes. This meets the numerical ≥10 q-transition minimum *as a potential environmental-predictability input*. Three flyways and ≥3 route positions are represented in the source regional order. All q values were measured independently of the newly downloaded 52,443 geese GPS fixes (PR #395). This does not prove independent GPS stopover-visit support or genuine animal-level predictive cue access.

**HOLD_YEAR_SPECIFIC_S_JY:** The source DOCX does not provide 1982–2011 **region-year spring-onset date values**; the yearly traces are only images. The original 16 Table S1 regional means and SDs cannot be substituted for each focal goose observation's year-specific \`S_{j,y}\`.

**HOLD_EXACT_GPS_REGION_CROSSWALK:** The original Movebank GPS records have locations/time, but this DOCX does not contain polygons, objective centroids or membership rules for its 16 generalized regions. Unverified NLDK/NSE candidate aliases remain separate from licensed region mapping. Do not group points into opportunistically chosen regions after seeing the goose timing outcomes.

**HOLD_GEOMETRY_ONLY_URGENCY:** The frozen independent \`U=1−d_{j,breed}/d_{winter,breed}\` requires source-verified stopover-region geometry and breeding/winter origins. The original S1 average **stopover durations** are bird behaviour, not an independent proxy for actionability or geometric urgency and must not be used in U.

**HOLD_OUTCOME_ADMISSION:** ≥30 *actual* individual stopover visits from at least 2 flyways, correlation |corr(q,U)|<0.90, the original 40 complete migration inclusion rule, distinct region-year spring and predeclared year-flyway reference are not yet audited together. Therefore:

\`\`\`
V7_ORIGINAL_SOURCE_DOCX = SHA256_VERIFIED_PARSED
V7_PUBLISHED_30YEAR_Q_PAIRS = 23
V7_CONSECUTIVE_TRANSITION_Q_PAIRS = 13
V7_CORRELATION_Q_MINIMUM = PASS_AGGREGATES_ONLY
V7_REGION_YEAR_JERK_DATES = NOT_AVAILABLE_AS_SOURCE_TABLE
V7_REGION_GPS_POLYGONS = NOT_AVAILABLE
V7_GEOMETRY_ONLY_U = NOT_IDENTIFIED
V7_PRIMARY_BETA_Q_TIMES_U = UNOPENED_NOT_ESTIMABLE
\`\`\`

## 4. Reproducibility and data rights

Generated source-derived aggregate CSV files:
- \`data/payoff_b_v7_kolzsch_2015_suppinfo_q_20261117.csv\`: all 23 historical correlations, printed SMATR indices and intervals, source page and original SHA256, adjacent route and alias status.
- \`data/payoff_b_v7_kolzsch_2015_suppinfo_S1_20261117.csv\`: 16 published regional mean/SD Julian onset and mean stopover durations, tagged as **aggregate prior art**, not current-year fitness or actual migrants.
- \`scripts/payoff_b_v7_suppinfo_aggregate_gate.py\`: fail-closed reproducibility gate; optional \`--source-docx /path/to/original.docx\` re-reads the original seven tables and checks the **actual DOCX bytes** against this immutable source digest. CI without the user-uploaded DOCX can audit **only** the committed derivative CSVs, not independently reopen the original file; this limit is explicit.
- \`tests/test_payoff_b_v7_suppinfo_aggregate_gate.py\`: original source rows admitted and mutated/duplicate/alias/drift failures.

**Scientific claim ceiling:** The published authors have already reported predictive connectivity and its influence on goose migration; reconstructing those original correlations is NOT an independent finding. This only advances the original-source admission needed for PAYOFF-B's distinct frozen predictability × geometry-only urgency question. It does not identify the animal's mental information, actual cue value, evolutionary payoff, reproductive fitness, or a new game-theory effect.

**Next permissible action:** Obtain actual year-specific GDD-jerk onset per generalized region **with independently grounded region membership** (original author data/algorithm, region centroids or polygons) to compute original V7 \`Y_{ij}\` and \`U_j\`, then check frozen admission thresholds without redefining q, annual sources or movement controls. Do not digitize Figure S1 by hand and call it exact regional climate data.
