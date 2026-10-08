# PAYOFF-B: independent spring energetics to breeding-fitness source gate

Date: 2026-10-08
Status: **PINNED AUTHOR RAW DATA VERIFIED AGAINST DRYAD DIGEST; NO NEW FITNESS MODEL FITTED; BIOLOGICAL CAUSAL GATES HOLD**

## Rationale

V8 bird evidence concerns range-based phenological matching proxies, not survival or reproduction. Schindler et al. (2024), *Proceedings of the Royal Society B*, DOI 10.1098/rspb.2023.2016, report a published fitness benchmark in Greenland white-fronted geese (Anser albifrons flavirostris), public data DOI https://doi.org/10.5061/dryad.2547d7wzn.

Original authors already established:
- 28 successful, 73 unsuccessful and 7 deferred reproductive attempts;
- individuals feeding longer and expending less energy during spring were more likely to reproduce successfully;
- high energy expenditure with little feeding was associated with breeding deferral;
- the spring SUBSEASON of these behaviours did not detectably change their reproductive effects. This does NOT mean migration arrival timing never matters.

Related prior art: Cunningham et al. (2023), Oecologia, DOI 10.1007/s00442-022-05300-x, studied daily weather, energy, feeding and breeding deferral in white-fronted geese. VonBank et al. (2024) studied 56 greater white-fronted geese and identified geographic differences in timing without strong migration-characteristic effects on breeding; those are distinct cohorts and measures, not data replicates for pooling.

## Exact source audit

Script: scripts/audit_payoff_b_goose_fitness_source.py
GitHub Actions source-only run: 37745434937 (successful source-access accounting; not successful data ingestion). Synthetic ZIP/CSV schema test: PASS. Public Dryad metadata and version file manifest: PASS. Bulk original data ZIP: HTTP 401 Unauthorized, **ACCESS HOLD**.

Metadata: dataset version 5.
- spring_data.csv: 51,561 bytes; SHA256 9ef98e6b5e979e93476ed076a018db13bdf03aab6dcc5ca728b5fd866e79c1bd
- autumn_data.csv: 40,894 bytes; SHA256 4dc6fe4e91b2130596bb5d5a2c3620fc183ce5e4809ab4c7d80cf2e2d9f34288
- README.md: 4,421 bytes; SHA256 948f71afb90ae03fd85298ebebb96b6f4e210fd1f9322cf7a1474fa95a0e0ab6

The **bulk Dryad API** still returns HTTP 401 without authorization.
However, the authors' own public GitHub repository
https://github.com/aschindler23/Schindler_etal_2024_ProcB
contains `spring_data.csv` and `autumn_data.csv` at pinned commit
`2171bcd36bf37022c8716e15c0f75412103b0f3f`. The source-only GitHub
Actions audit, run **37753387925**, verified that converting the author's
LF newline encoding to CRLF produces **exactly the two SHA256 checksums
published in Dryad's version-5 file manifest**. This is a legitimate public
author-hosted copy, not an authentication bypass.

The source structure is now independently established:
- Spring: **642 rows**, **49 birds**, **107 distinct bird-years**, with all
  six sub-seasons present for every bird-year, no duplicate
  (id,year,sub_season) and no reverse stage-date ordering. From first
  migration-flight onset (stage 2) to early breeding (stage 6), the recorded
  differences range **13–61 days**.
- Autumn: **494 rows**, **41 birds**, **84 bird-years**, of which **79**
  have all six stages, with no duplicated stage keys or reversed stage order.
- These records are **not 642 and 494 independent reproductive attempts**.
  An appropriate fertility/survival analysis has bird-year as its outcome
  grain with repeated individual and year effects.

The original article reports 108 breeding-season outcome observations
(28 successes, 73 failures, 7 deferrals), while this author-hosted spring
table has only **107 bird-years**. The exact reason for the one-record
difference has not been established, so these totals must NOT be silently
equated or a synthetic observation added. No new reproductive outcome
association has been fitted or claimed in this audit.

Original author model code already includes the beginning of early breeding
(stage-6 `first_day`, renamed `arrival_day`) alongside sub-season
feeding/ODBA predictors in the Bernoulli breeding-success model. Therefore
a simple "timing plus energetic condition predicts breeding" association
is itself **prior-art territory**, not automatically a new PAYOFF-B result.
The related Zenodo record hosts the author analysis code as well.

## Independently checked data structure and source distinctions

Fields include id, year coded 1–5 (= 2018–2022), sub_season 1–6 (late winter; flight; two spring-staging halves; flight; early breeding), first_day of subseason, log_ODBA energy expenditure proxy, num_feed_fixes and num_ACC_fixes for feeding fraction, weather and land-cover covariates, breeding_outcome (success/failure/deferral), and breeding_success (binary).

One bird-year reproductive outcome can be repeated across up to six subseason rows. Do not count each row as a separate reproductive attempt. The author-repository source admission has checked table hierarchy and stage chronology; any new outcome analysis must separately audit response-category consistency, missingness and time ordering before fitting. Training on subseasons to predict the same breeding outcome without bird-year clustering would be pseudoreplication.

## Biological construct gate

| Needed variable | Evidence | Verdict |
|---|---|---|
| Spring feeding and energy | SHA-verified original author CSV and publication | SOURCE PASS; interpretation as physiological cost HOLD |
| Genuine reproductive outcome | Individual-year binary/categories in author CSV, not yet modeled here | SOURCE PASS; new outcome inference NOT OPENED |
| Individual predecision remote environmental prediction | No historical cue-to-destination model observed | NOT IDENTIFIED |
| Individual incoming resource phase error | No independently defined phase-error time series in described data | NOT IDENTIFIED |
| Independent downstream correction capacity | ODBA is energy expense, not maximum movement adjustment | NOT IDENTIFIED |
| Novel spring energy to reproduction relationship | Already established by Schindler et al. 2024 | PRIOR ART COLLISION |
| Paired interspecific seasonal coordination | Study involves a single bird taxon | NOT IDENTIFIED |

## Implication for PAYOFF-B

The published ecology supplies a natural check: successful timing correction and actual fitness recovery are NOT equivalent; feeding and energy expenditure may constrain reproductive value independently of timing. PAYOFF-B's cost K(c) is a hypothesis until independently measured. This source does not estimate K, information quality at choice time, or a causal correction-to-breeding effect.

This benchmark has been added to Paper 2 V4 with original-study attribution. The **source acquisition blocker is resolved** via the public author repository and verified Dryad checksums. The substantive blocker remains: no independent green-up phase reference, prospective information state, maximum remaining actionability, or exogenous correction-cost variation is identified merely from these sub-season summaries. Reproducing the original breeding model cannot establish the missing mechanism. See `data/payoff_b_goose_author_mirror_source_eligibility_20261008.json`.
