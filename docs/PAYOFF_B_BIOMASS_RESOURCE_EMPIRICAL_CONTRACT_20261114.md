# PAYOFF-B: biomass-resource empirical identification contract

**2026-11-14 | pre-analysis design, NOT a new biological result**

## Core biological claim to discriminate

A migrating bird may arrive at a destination when greenness is advanced, but its fitness depends on the *available, digestible resource biomass integrated across the actual demand window*, not merely a remote spring date or peak NDVI.

The target estimand must distinguish:
- resource **peak date** (day of maximum B);
- resource **peak magnitude** (maximum biomass);
- resource **seasonal integral** (area under biomass curve, with standardized sampling effort);
- **available demand-window biomass** integrated over the biologically specified brood-rearing/feeding period;
- resource **quality and accessibility** (e.g. caterpillar size, digestibility, weather-mediated foraging, prey capture) where independently measured.

A biomass peak date alone cannot identify biomass amount, food limitation or fitness.

## Two source-faithful existing bridges

1. Burgess et al. 2018, DOI 10.1038/s41559-018-0543-1: published caterpillar peak versus bird first-egg date slopes 0.510 blue tit, 0.515 great tit and 0.348 pied flycatcher. These are **published results**, not newly fitted raw-data effects. Edinburgh DataShare DOI 10.7488/ds/2215 and GitHub allyPhillimore/birds_frass_oak provide open oak/frass components; bird BTO nest records are not redistributed by PAYOFF.
2. Hoge Veluwe Visser Dryad DOI 10.5061/dryad.f1vhhmgx6, `Tbl_PeakDate_Biomass_HVLim.xlsx`, source-verified sheet `tbl_PeakDate_Biomass_HVLim`, columns `Year` and `MidDate`, 35 years (1985–2020 excluding 1991). The certified file provides **peak timing**, not a verified annual biomass magnitude or daily biomass curve in the current PAYOFF source contract. Great-tit first-clutch records contain `YearOfBreeding`, `LayDateApril` and `NumberRecruitsAllBroodsSummed`, but a year-wise resource-peak association with recruits would be a different observational question from the previously failed cue-reversal gate.
3. The original Hoge Veluwe cue-resource decline-to-recovery Gate B FAILED (both fitted slopes positive); Gate C remains CLOSED. Do not reopen the same hysteresis endpoint by substituting biomass magnitude or dates after seeing that failure.

## Primary independent prospective hypothesis

At fixed destination green-up date and season, birds with greater **predecision-predictable biomass exposure** and greater independently measurable **remaining correction opportunity** will have smaller *resource-weighted brood-demand deficits* than otherwise similar birds.

This is a testable prospective interaction, not a prediction already supported by existing PAYOFF-B tracking results. Distinguish:
- prediction of actual food biomass from remote information trained only on preceding years;
- adjustment of signed arrival/departure/stopover timing *after* cue availability;
- realized exposure during the nestling demand window;
- offspring survival/recruitment or independently measured fitness.

A biomass-related movement response can be driven by energetic state, competition, weather, and spatial foraging without being a response to a learned forecast. Therefore the information mechanism requires a genuinely predecision cue plus independent resource outcome and correction capacity.

## Minimum empirical design and data columns

Study/individual/year IDs, data permissions and source version; original GPS fix timestamps and location with known error; independent site/stopover membership and departure time; remotely available forecast signal at each decision stage; destination or stopover prey-biomass repeated observations with sampling area and effort; brood-demand timing and brood size; resource accessibility/quality; stage-specific *feasible* recourse estimated from independent birds or physical envelopes; final breeding/survival outcomes; shared year/flyway/site weather blocks and censoring.

Define a demand-window resource exposure before fitting:

    E_i = integral_{t in demand window_i} B_site(t) * A_i(t) * Q_site(t) dt

where B is biomass density, A is a declared accessibility factor, and Q is resource quality. A and Q are NOT inferred from the bird's own later behavior. When only biomass is observed, set A=Q=1 as a transparent *biomass-exposure index*, not as energy assimilation.

Specify the demand window from species biology before opening biomass-outcome associations. Treat peak date, peak amount and integral as **distinct predictors**; do not relabel NDVI/green-up as direct insect biomass.

## Non-overlapping empirical lanes

**Lane 1 (immediately feasible source audit):** confirm which original public source archives contain repeated biomass magnitude or density and effort, rather than only peak dates. Audit schemas, dates, units, permissions and missingness. No model fitting until this gate is recorded.

**Lane 2 (resource-phenology bridge):** reuse the already published Burgess bird–caterpillar timing slopes as prior art and independently estimate food-availability curves only where source raw biomass data actually exist. The open oak/frass component may quantify insect resource supply but does not supply redistributable bird individual fitness.

**Lane 3 (fitness linkage):** in independently qualified cohorts, connect resource exposure to nestling growth, recruits or survival with a preregistered model that separates biomass amount from timing and controls habitat, density, season and repeated birds/years. Recruitment is a component of fitness, not lifetime fitness.

**Lane 4 (PAYOFF-B mechanism):** only after separate source gates, estimate predecision predictive information × independently measured remaining recourse and the resulting resource-weighted phase/fitness association. Do not substitute post-outcome movement as an estimator of feasible recourse.

## Negative controls and statistical safeguards

- Compare predecision forecasts with *future-only* resource data as a leakage diagnostic (never include future data as a real predictor).
- Test out-of-year and out-of-site predictive skill; whole-individual CV alone does not validate new spring years.
- Cluster/bootstrap at study/site/year/weather-episode levels as justified; do not count GPS fixes or repeated frass samples as independent taxa.
- Test whether any biomass association survives adjustment for green-up timing, prey quality, vegetation, weather, nesting density and seasonal trends.
- Avoid combining insectivores, herbivorous geese and waders on a single unstandardized biomass scale. Use guild-specific resources (caterpillars/invertebrates, plant forage, benthic invertebrates) and report guild-level heterogeneity.
- Record missing biomass **amount** as NOT MEASURED; never replace with peak date or NDVI without a separately validated calibration.

## Existing evidence verdict

**Supported:** published relative-timing deficits between insectivorous birds and caterpillar biomass peak, with weaker temporal tracking in migrant pied flycatchers than the two resident tit species in the Burgess study.

**Not supported yet:** biomass quantity determines PAYOFF-B information-use thresholds; biomass rescues phenological mismatch; source-weather cue causes migratory adjustment; food-biomass exposure mediates breeding success in a new PAYOFF-B fit; universal cross-guild effects.

This file is an outcome-blind empirical-design extension to Draft PR #341, not a post hoc rescue of the V7R/V8 or Hoge Veluwe negative gates.
