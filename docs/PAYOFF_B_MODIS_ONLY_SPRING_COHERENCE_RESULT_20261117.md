# PAYOFF-B MODIS-only spring coherence: complete original-source exploratory result

Date: 2026-11-17. **Output is an eBird-free environmental descriptive analysis, not a bird migration or fitness result, and not a confirmatory directional test.**

## Why this separate analysis was required

An earlier PAYOFF-B V8 script selected 166 source–destination links using `mig_cell` and `breed_cell` species range masks from Amaral's `data/final.rds`. Amaral et al.'s original code derives the bird arrival/range data from Youngflesh's **eBird-based** arrival estimates. Although the analyzed `gr_mn` vegetation value was from MODIS, **the V8 link selection was bird/eBird-conditioned** and conflicts with the project's prohibition on eBird data. The +0.369 eBird-conditioned estimate is therefore **QUARANTINED: not an accepted eBird-free PAYOFF finding, not to be used in a main manuscript claim**, regardless of its stable computational bootstrap. Do not conflate source-specific selections.

## Independent satellite-only input

Public pinned original source `br-amaral/BirdMigrationSpeed`, commit `62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`, **only** `data/for_green-up_dl.rds`, file SHA256 `8989bf98752cf23a6be237332e35c44abff5a39d2a00d5bd1f65cce732cf6199` and length 15,579 bytes. These are the published MODIS MCD12Q2 forest mid-greenup records: no bird species, dates of arrival, eBird occurrences, migration/breeding-range masks, `species_Grid`, or tracking data were read by the new R script.

Source table from original 106 Eastern North American geographical hexagonal cells, **2002–2017 inclusive**, **1,696 cell×years** all 106×16 observed. No duplicated cell-year or coordinate conflicts. The minimum reported original good-quality forest greenup pixels is 20,799, above the original author's 10,000-pixel threshold. Latitude 25.98–59.11°N, longitude −94.68–−54.37°E [longitude is WEST / negative], so this is **not global**.

Original source QA: https://github.com/zuizui0223/payoff/actions/runs/44011312092

## Fixed geographic design and observation unit

This analysis was explicitly frozen after the earlier eBird-conditioned V8 sign was known, in `docs/PAYOFF_B_MODIS_ONLY_SPRING_COHERENCE_FREEZE_20261117.md`. Hence no independent confirmation is available. The single non-optimized pairing rule uses only input latitude/longitude: for each target, select its nearest cell strictly farther south, maximum 800 km, tied by numeric cell ID. Require ≥30 such links and ≥15 unique source cells, full original quality screen `gr_ncell>10000`, ≥6 annual source-target observations in both 8-year windows.

**Admission:** all 106 satellite source cells eligible; **104** nearest-southern links, **88** distinct source cells. All links have full 8/8 years in both windows. No birds or environmental correlation outcomes entered the link selection. For each link, linear-detrend the source and target vegetation midgreenup calendar dates separately against year in EARLY 2002–2009 and LATE 2010–2017; signed Pearson correlation r. Inferential unit = environmental source-target link, with 10,000 **source-cell-block** bootstrap replicates, seed 20261117, resampling every link of a given source cell together. Source and target pairs can still be environmentally dependent at regional scales, beyond this bootstrap design.

## Actual original-data results (not simulated)

| Environmental quantity | Original result |
|---|---:|
| Source pairs | **104** |
| Mean pair correlation, 2002–09 | **+0.7985937** |
| Mean pair correlation, 2010–17 | **+0.8791639** |
| Mean change Δr = later − earlier | **+0.08057016** |
| 95% source-cell-block bootstrap interval | **[+0.02409762, +0.1391265]** |
| Diagnostic unclustered pair bootstrap interval | [+0.0251559, +0.1396429] |
| Pair correlations declining | **45/104** |
| Exactly 8+8 observed years | 104/104 |
| Mean change under 7-year windows 2002–08 and 2011–17 | **+0.03998701** |
| Undetrended mean correlation change | **+0.09067732** |
| Mean number of original good forest pixels per cell, early vs late | **278,556.7 → 281,280.4** (≈1% higher) |

These are estimates of **spatial phenological covariation of vegetation**, not climate change causality, actual cue perception, field food quantity, individual migration decisions, route recourse or fitness. The 7-year alternative reduced the positive mean about half, so magnitude depends on time-window choice even though sign remained positive. 45 of 104 links went in the opposite direction, showing genuine geographic heterogeneity.

**Comparison to quarantined result:** the earlier eBird-conditioned linkage changed by +0.369, substantially larger than the pure satellite geographic +0.081. The link populations, distances, species masks and weighting differ, so the difference is **not a causal estimate of eBird bias**. It does demonstrate that generalizing the +0.369 as a purely geographic environmental pattern was unwarranted.

This finding does not independently test PAYOFF-B's information-by-urgency thesis. The frozen Kölzsch 2015 three-flyway V7 had 52,443 GPS fixes with verified individual IDs and geographic positions but is still missing the independent 1982–2011 GDD-jerk regional historical q source (original Wiley supplement not retrieved, HTTP 403). No V7 q×U coefficient has been fitted; do not infer "information lost" or "information used" from this MODIS-only result.

## Reproducible original outputs

Primary original-data workflow **https://github.com/zuizui0223/payoff/actions/runs/44011549509** completed successfully: pure satellite schema QA, synthetic algebra gate, original source SHA256, and 104-pair bootstrapped estimates. Artifact contains `payoff_b_modis_source_quality.csv`, `payoff_b_modis_only_geographic_summary.csv`, and `payoff_b_modis_only_geographic_pairs.csv`. Source file itself is not re-published.

Scripts:
- `analysis/movement_phenology/payoff_b_modis_source_quality_20261117.R`
- `analysis/movement_phenology/payoff_b_modis_only_geographic_synchrony_20261117.R`

**Publication status: exploratory background only, main-line PAYOFF information×recourse interaction remains NOT_ESTIMABLE.** No further same-source window optimization or ad-hoc pair re-selection should be used to chase a direction.
