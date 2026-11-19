# PAYOFF-B E6 — temperature measurement-location modifier: NOT IDENTIFIABLE in existing source table

Date: **2026-11-19**. Original source audit **completed**; no new phenological response coefficient or direct information-use effect fitted. Source analysis code: `scripts/payoff_b_e6_temperature_location_support.py`. Result: `data/payoff_b_e6_temperature_location_support_result_20261119.json`.

## Source and source-policy correction

The original Usui et al. (2017), *Journal of Animal Ecology* meta-analysis [DOI 10.1111/1365-2656.12612](https://doi.org/10.1111/1365-2656.12612) distinguishes (i) location of measured temperature: breeding, passage, non-breeding; and (ii) the population's source-coded migration-distance class. It explicitly warns that temperature-measurement location and arrival location are correlated, and the published main temperature slope did not differ materially among those location categories. Thus an interaction is not guaranteed to be separately identifiable; it also could not establish which cues an individual migratory bird could actually observe.

The original, source-hash-verified Usui CSV was downloaded from [Zenodo record 4970634](https://zenodo.org/records/4970634) in [Actions run 44478528312](https://github.com/zuizui0223/payoff/actions/runs/44478528312). The frozen E6 selection was reproduced exactly (944 rows, 28 original studies, 279 species). That initial **source-only** check was successful: 4 distinct literal temperature-location levels and 6 possible pairs were identified, with **at most 2** studies containing all short/long × two-location cells. Original data and source-derived 944 row effects are **not** committed here.

A separately discovered source-provenance issue requires correction: 264 existing E6 effects from Hurlbert & Liang (2012), PLoS ONE [DOI 10.1371/journal.pone.0031662](https://doi.org/10.1371/journal.pone.0031662), are from a study explicitly using eBird checklists. The initial 944-row E6 cannot be described as eBird-free. The support-audit implementation was therefore amended **after inspecting the initial source-level counts**, on source-provenance grounds independent of coefficient signs or new model fits. The entire known eBird-derived study is excluded before interpreting the study-crossing gate; the other 27 source studies still require independent provenance audit.

## Corrected study-support counts (680 effects, 27 studies, 279 species)

| Verbatim source temperature-location label | Effect rows | Original studies | Studies with short and long migrants in that label |
|---|---:|---:|---:|
| breeding | 155 | 9 | 4 |
| passage | 146 | 6 | 3 |
| passage or breeding | 286 | 15 | 8 |
| wintering | 93 | 1 | 1 |

The original `passage or breeding` category cannot be split post-hoc into either geographic regime: **286 rows after removal** (550 original) have an ambiguous source label; this is not individual cue availability. Wintering temperature is represented by only **one** source study.

Among all six unordered pairs of source temperature-location labels, the *only* pair with any fully crossed within-study short/long × location support is:

- **breeding × passage: 2 original studies**;
- **all other pairs: 0 fully crossed studies**.

The pre-specified minimum was **5 distinct fully crossed studies**. Thus **0/6 candidate location contrasts pass the source-only gate**, before worrying about phylogeny, publication bias, latent cues, environmental predictability, individual cue acquisition or fitness.

**Gate decision:** `FAIL_DO_NOT_FIT_TEMPERATURE_LOCATION_BY_MIGRATION_DISTANCE_INTERACTION`.

## What is established / not established

**Established as a design fact:** Original E6 published data lack within-study crossed evidence for a portable migration-distance × temperature-measurement-location effect under the predeclared criteria. Excluding the known eBird-based study does not rescue it. The updated gate is a legitimate methodological stop, not a p-value of a biological null.

**Not established:** migration distance's effect is caused by information distance, temperature measurement location is actual cue exposure, all remaining studies are eBird-free, or the announced q×U mechanism is observed. The canonical E6 short/long gradient persists in a separately audited forced exclusion [PR #404](https://github.com/zuizui0223/payoff/pull/404), but does not fill the missing within-study 2×2 data. Original frozen V7 stays `NOT_ESTIMABLE`.

## Next biological requirement

A new independent monitoring dataset must measure (a) actual pre-decision information exposure at origin/stopover; (b) an independent future target spring onset or resource state; (c) individual's migration decision and downstream adjustment; and ideally (d) reproductive fitness. Simply adding more pooled temperature-response slopes without matched cue contexts does not identify the information deadline mechanism.

No changes to the frozen V2/V7 manuscripts, and no eBird checklists downloaded.
