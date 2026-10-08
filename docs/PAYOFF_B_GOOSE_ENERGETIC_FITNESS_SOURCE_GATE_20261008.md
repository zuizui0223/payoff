# PAYOFF-B: independent spring energetics to breeding-fitness source gate

Date: 2026-10-08
Status: **PUBLIC METADATA VERIFIED; ARCHIVE DOWNLOAD AUTHORIZATION HOLD; NO INDIVIDUAL DATA INGESTED**

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

No source CSV bytes were retrieved or parsed. No row or bird-year counts were verified; no outcome estimate was calculated. CI success refers only to correct access logging and a synthetic test. Official Dryad UI or an authorized session would be required for raw data; no login bypass was attempted. The related Zenodo code record 10.5281/zenodo.10581609 hosts analysis scripts, not these original Dryad CSV files.

## Data structure described in authors' README (not independently checked from bytes)

Fields include id, year coded 1–5 (= 2018–2022), sub_season 1–6 (late winter; flight; two spring-staging halves; flight; early breeding), first_day of subseason, log_ODBA energy expenditure proxy, num_feed_fixes and num_ACC_fixes for feeding fraction, weather and land-cover covariates, breeding_outcome (success/failure/deferral), and breeding_success (binary).

One bird-year reproductive outcome can be repeated across up to six subseason rows. Do not count each row as a separate reproductive attempt. Raw admission must check this hierarchy, missingness, time ordering and outcome availability. Training on subseasons to predict the same breeding outcome without bird-year clustering would be pseudoreplication.

## Biological construct gate

| Needed variable | Evidence | Verdict |
|---|---|---|
| Spring feeding and energy | README fields and original publication | Raw source HOLD |
| Genuine reproductive outcome | Published results and README | Publication PASS, raw HOLD |
| Individual predecision remote environmental prediction | No historical cue-to-destination model observed | NOT IDENTIFIED |
| Individual incoming resource phase error | No independently defined phase-error time series in described data | NOT IDENTIFIED |
| Independent downstream correction capacity | ODBA is energy expense, not maximum movement adjustment | NOT IDENTIFIED |
| Novel spring energy to reproduction relationship | Already established by Schindler et al. 2024 | PRIOR ART COLLISION |
| Paired interspecific seasonal coordination | Study involves a single bird taxon | NOT IDENTIFIED |

## Implication for PAYOFF-B

The published ecology supplies a natural check: successful timing correction and actual fitness recovery are NOT equivalent; feeding and energy expenditure may constrain reproductive value independently of timing. PAYOFF-B's cost K(c) is a hypothesis until independently measured. This source does not estimate K, information quality at choice time, or a causal correction-to-breeding effect.

This benchmark has been added to Paper 2 V4 with explicit original-study attribution. Source-data expansion remains on HOLD until a legitimate raw copy and sufficient within-individual decision-time ecology exist. Acquiring the CSV alone would enable reproduction but not identify the missing causal mechanism.
