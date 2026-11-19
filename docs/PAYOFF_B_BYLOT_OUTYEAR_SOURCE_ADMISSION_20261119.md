# PAYOFF-B — Bylot Island independent source gate and time-order audit

Date: **2026-11-19**. Scientific state: **NO NEW OUTCOME OPENED / STRONG OUT-YEAR TEST FAILS NOMINAL SUPPORT**.

## Task and current decision

After Usui E6's **published** short–long-distance temperature-response gradient survived a stricter within-original-study comparison (13 independent original studies; 444 source effects; beta long-minus-short +0.525 d/°C), the next *distinct* biological question is **whether temperature available before the breeding decision predicts phenological adjustment and ultimate fitness**. Neither Usui E6 nor the existing wigeon/greater-snow-goose evidence proves that information available *before commitment* drives later compensation.

Official 2026 public records identify new Bylot original datasets. However, **source access terms, source grain, time overlap, and the 2020 published fitness prior art have to be checked before using those records in a new natural effect fit**.

### Four original data roles

1. [Nordicana D41 v1.2](https://nordicana.cen.ulaval.ca/en/publication?doi=10.5885%2F45570CE-2D00DCA728074FA7), Gauthier/Cadieux/Legagneux 2026, DOI `10.5885/45570CE-2D00DCA728074FA7`: nest summary for 1989–2025; reported no data for **2020, 2021 and 2024**. Nested records and published 2020 fitness paper cover source periods already investigated. **The official per-nest visit dataset currently lists data only through August 2019**, even though the summary ZIP is updated through 2025. Laying date, clutch, hatching and *nesting success* are documented; this does not measure young surviving to age one.
2. [Nordicana D2 v1.13.0](https://nordicana.cen.ulaval.ca/en/publication?doi=45039SL-EE76C1BDAADC4890), DOI `10.5885/45039SL-EE76C1BDAADC4890`: Bylot Lac du camp **BYLCAMP mean air temperature**, official ZIP `ds_000634180.zip`, **August 1993–July 2023**. This implies first potentially complete May 1–15 window is **1994**, not 1993. Original daily rows, station QC and nest-site spatial mapping are NOT opened or verified.
3. [Movebank Greater snow goose migration](https://www.movebank.mpg.de/cms/movebank-content/audubon-mbi-collection), original study **1442516400**, 75 GPS birds in collection summary, **2019–2023**. **A public summary does not grant access to raw fixes**; owner permissions and CC BY-NC sharing terms apply. No verified bird-to-nest original identifier key is available. It must not be inferred from simultaneous years.
4. [Reséndiz-Infante & Gauthier 2024](https://doi.org/10.3389/fbirs.2024.1307628): 1979–2018 historical interregional temperature correlations (St. Lawrence→Nunavik→Baffin→Bylot). This is *published information-predictability prior art*, not individual animal use of a cue or a newly identified 2019–2023 q contrast.

## Material prior art

Existing PAYOFF-B already cites [Reséndiz-Infante & Gauthier (2020), Scientific Reports](https://doi.org/10.1038/s41598-020-78565-y), [`docs/PAYOFF_B_GREATER_SNOW_GOOSE_FITNESS_LOSS_ANCHOR_20260929.md`](PAYOFF_B_GREATER_SNOW_GOOSE_FITNESS_LOSS_ANCHOR_20260929.md). That paper analyzed **1991–2015** and estimated a two-sided relative-laying-date fitness curve and the cost of waiting to increase clutch size. Thus fitting 1994–2015 Bylot laying-date / temperature / success relations would substantially **reuse known biological work**. It cannot be promoted as an independent new replication without a distinct, predeclared question.

The registered prospective [2019–2023 greater-snow-goose departure cue gate](PAYOFF_B_GREATER_SNOW_GOOSE_GPS_CUE_UPTAKE_REGISTRATION_20260929.md) also remains **UNOPENED**. No weather or breeding data are allowed to redefine its original departure cues, movement segmentation, route contexts or predeclared thresholds.

## Source-only calendar crosswalk (no biological rows inspected)

Using the original 2026 metadata, not guessed values:

| Window / relation | Candidate years, only if source rows are complete | Nominal number of years |
|---|---|---:|
| D41 nest summary × D2 BYLCAMP May 1–15 temperature, existing published 2020 fitness era | **1994–2015** | 22 |
| Post-2015 D41 nest summary × same D2 weather source | **2016, 2017, 2018, 2019, 2022, 2023** | **6** |
| Individual D41 nest *visits* × 2019–2023 Movebank GPS year range | **2019** | **1** |
| D41 nest *summary* × Movebank GPS year range | **2019, 2022, 2023** | **3**, but NOT individual matches |

Dates 2020, 2021 and 2024 are explicitly absent from D41; 2025 extends the D41 summaries but not D2's listed weather time series. These are **maximum calendar intersections, not guaranteed data samples**. Actual May climate completeness, D41 sampling-stratum comparability and overlap of true GPS individuals have not been evaluated.

## Predeclared no-leakage test and immediate stop

Proposed secondary ecological question only (not a cue-use theorem test): does **calendar May 1–15** local temperature add *future-year* prediction of annual median laying date beyond a past-trained calendar baseline?

- Primary time unit = **source calendar year**, not nests/fixes. The date window is fixed before access to the original new outcome rows.
- Need **≥10 genuinely held-out post-2015 years**, verified original climate date coverage ≥12/15 days and D41-specific nest definitions / monitoring strata and common station/nest geography.
- Given **at most six** candidate source-overlap post-2015 years, the 10-year generalization test is **NOT ESTIMABLE from currently documented source windows**. Do not lower the minimum after inspecting data, or treat annual nest count as sample size to hide the 6-year limit.
- A descriptive retrospective 1994–2023 year-level analysis could be attempted only under a separate, openly labeled post-publication *prior-art* question after source rights, raw schema and measurement comparability are verified. It is not a new independent out-of-year test. No result has been fitted here.

Original **habitat/method-based nest sampling** must also be retained: intensive core plot vs random plots vs neck-collared female searches differ in selection process, and nesting success may depend on predators, food, snowmelt and density. Annual site aggregate phenology vs success is not a causal selection/fitness gradient unless those confounding/sampling processes can be identified. A better fit with a future-weather variable is not a prospective "cue" gain.

## Access and permissions

The official Nordicana **download** pages request acceptance of use terms before releasing the ZIP files. The present run **did not accept terms, download files behind the agreement, invent source checksums, or extract original nesting/weather rows**. Public HTML metadata alone does not prove raw access or unrestricted redistribution. Movebank similarly requires owner terms/permissions; a study title, number of birds, or published movement summary does not establish individual GPS access or ID matching. The assistant has not acted on behalf of the user to accept legal terms.

The deterministic source-only gate and five regression tests are:
- `data/payoff_b_bylot_independent_outyear_source_contract_20261119.json`
- `scripts/payoff_b_bylot_independent_outyear_source_gate.py`
- `tests/test_payoff_b_bylot_independent_outyear_source_gate.py`

They guard the four provider identities, calendar windows, absent data, original source-file SHA256 unknown status, limited six post-2015 years and lack of GPS individual crosswalk. All source-readiness booleans remain false; no real biological rows are used and successful CI is **source-schema contract validation**, not independent empirical confirmation.

## Path after source access

Only after properly licensed *original* D41 ZIP, D2 ZIP and accompanying field codebooks are legitimately obtained: verify full file SHA256 and source documentation; map original fields without guessing; audit whether June laying is measured comparably across source years and sites; validate May daily weather continuity; then revisit **source eligibility**, without modifying the frozen V7 goal. Individual movement-to-fitness requires a separate **true original GPS-to-D41 bird/nest identifier crosswalk**, a within-year assignment rule and independent enough individuals and years. Without these, report `FITNESS_LEVEL_OBSERVATIONAL_ONLY` and `BEHAVIOR_FITNESS_JOIN_NOT_ESTIMABLE`.

This source gate does not block or reclassify the already accepted exact-theory short paper, the synthetic moving-landscape mechanism or the source-compliant E6 metadata sensitivity. No manuscript retuning or main merge is authorized.
