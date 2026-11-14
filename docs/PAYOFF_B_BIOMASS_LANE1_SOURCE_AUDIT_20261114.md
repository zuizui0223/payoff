# PAYOFF-B biomass Lane-1: source-field audit and source triage

**2026-11-14 | source documentation verified; no new biomass–fitness coefficient fitted**

## Critical distinction

The word *biomass* in an archive filename or a paper does not certify that the **distributed data table** contains absolute prey biomass, a complete seasonal curve or per-nest food exposure. The admission rule is based on source file columns and sampling units, not on article topic.

| Candidate | Verified data available | Missing for biomass-exposure estimand | Gate |
| --- | --- | --- | --- |
| Hoge Veluwe Visser Dryad 10.5061/dryad.f1vhhmgx6, `Tbl_PeakDate_Biomass_HVLim.xlsx` | Source-verified 35 annual records, 1985–2020 except 1991; fields `Year`, `MidDate` | No certified magnitude, effort-standardized daily biomass curve or per-brood biomass exposure in this **specific** table | **PEAK_DATE_ONLY** |
| Hoge Veluwe great tit `Tbl_Fitness_GT_HV_FirstClutches_CSNot0_YrLargerThan1973_IncludeIs1.xlsx` | Source-verified `YearOfBreeding`, `LayDateApril`, `NumberRecruitsAllBroodsSummed` | No paired direct resource biomass **amount** or migrant arrival in this table | **FITNESS_COMPONENT_PRESENT / RESOURCE_AMOUNT_MISSING** |
| Burgess et al. Edinburgh DataShare 10.7488/ds/2215 `oakandfrass.txt` | Repository R code explicitly reads `phenology.lower`, `phenology.upper`, `species`, `mean.centre.latitude`, `grid_50km`, `grid_5km`, `year`, `tray`; README describes first oak leaf and peak frass *dates* | No demonstrated frass dry mass/time or resource biomass magnitude in inspected published code or dataset description; no redistributable bird fitness rows | **PHENOLOGY_ONLY_UNTIL_RAW_SCHEMA_VERIFIED** |
| Wytham Woods frass sampling described in published methodological studies | Dried frass measured repeatedly and temperature-corrected to infer caterpillar biomass; explicit trap area and collection intervals | Original raw time-series, licensing and exact nest linkage **not yet source-file-verified in PAYOFF** | **PROMISING_NOT_ADMITTED** |
| PAYOFF-B existing GPS cohorts: stork, goose, curlew | Source-verified movement and prior-weather features, some stork reproductive output | No directly matched source-verified daily insect/plant/benthic resource biomass at used locations and decision windows | **MOVEMENT_ONLY_FOR_THIS_QUESTION** |

## Verified public-source pointers

- Edinburgh archive: https://doi.org/10.7488/ds/2215 ; dataset titled *Spatiotemporal data on pedunculate oak leafing and peak frass dates for the UK* (1998–2016). Its description is explicitly *phenology*, not a biomass-magnitude series; published archive notes ask data users to contact collectors. Original example analysis code: https://github.com/allyphillimore/birds_frass_oak/blob/master/Rcode_oak_frass_analysis.R
- Hoge Veluwe previously source-certified SHA256 for the peak-date file: `9f113eb3f95d239ac31652c4083a159d82dacb61355b03fa2f355a2733a0b984`. This is a field-level provenance result from the existing Gate-A audit; the present note does not re-download it.
- Visser et al. methodological description of Hoge Veluwe frass collection: https://pmc.ncbi.nlm.nih.gov/articles/PMC7078916/ . Dry frass is temperature-corrected and tree-level curves averaged before estimating dates and amounts. **Methods demonstrating original measurement do not imply the specific archived `MidDate` file contains that measurement.**
- Published Wytham frass methods and temporal measurements: https://www.journals.uchicago.edu/doi/full/10.1086/681572 . Potential high-value source; requires original table and permissions before use.
- Original Burgess paper: DOI 10.1038/s41559-018-0543-1. Its published bird-caterpillar temporal slopes are prior art and do not estimate food amount → fitness.

## Source selection decision

**NO-GO for a new biomass quantity × migratory fitness model using only currently verified PAYOFF data.** The original evidence supports bird–resource **peak timing** and a separate great-tit **recruitment** field, not a verified resource biomass **amount** per demand window for migrants.

The highest-value next source task is to locate and checksum original repeated frass dry-mass (with trap area, interval and temperature) together with nestling food-demand and breeding outcomes at matching site/year. If found, verify source identity, units, dates, effort and legal use before any effect model. If only peak dates are available, keep the question explicitly about phenological timing.

## Falsifiable mechanistic comparison once admitted

At the same destination green-up and with equivalent weather and nesting conditions, test whether (1) measured **demand-window food biomass** predicts recruitment more strongly than (2) resource peak date or vegetation green-up alone, with out-of-year and out-of-site validation. This is an empirical comparison, not a priori guaranteed. Only separately test information × feasible migration recourse when actual cue chronology and route options are observed.

**Do not** interpret positive associations as causal food limitation without controls for habitat, competition, detection and the observation process. No reopened Hoge Veluwe Gate-C hysteresis test; the registered Gate-B reversal was negative.
