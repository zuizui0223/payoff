# PAYOFF-B experience reversal: independent prior-art and source-gate decision

Date: 2026-10-08
Decision: **HOLD / NOT PUBLICATION-READY**. No independent ecological experience-reversal endpoint, no claim of causality or realized fitness. This decision does not change frozen V7R or V8 outcomes.

## Evidence from primary literature (not simulations)

1. **Abrahms et al. (2021), Nature Communications 12:7326** (https://doi.org/10.1038/s41467-021-27626-5): 105 satellite-tagged reintroduced whooping cranes (ages 1–6) between 2002 and 2018. The work already demonstrates resource-responsive en-route speed, social-learning dominance among subadults and stronger experiential learning among adults. Published aggregate examples: spring NDVI vs movement +27.1 km/day (95% CI 19.4–34.6), subadult group-age-by-environment interaction +29.1 km/day per year of oldest group age (15.8–42.1), age-dependent reduction of cumulative snow exposure -1.8 m per year (95% CI -2.0 to -1.5). The article already addresses adaptive experience; reproducing age-by-weather associations is not PAYOFF-B novelty.

2. **Teitelbaum et al. (2016), Nature Communications** (https://www.nature.com/articles/ncomms12793): older/more experienced cranes established new, more northerly wintering sites and new migration behaviors could spread socially. The strong claim 'experienced adults are behaviorally rigid in climate change' faces **direct counterevidence** in this very system. It does NOT show that adults have zero possible calibration lag in any other condition.

3. **Torstenson & Shaw (2025), Oikos e10862** (https://doi.org/10.1111/oik.10862; first online 2024-10-18): the relative fitness performance of calendar/temporal versus environmental migratory cues can invert as habitat seasonality and phenological shifts change. They **already** distinguish timing/cue accuracy from cue efficacy in fitness and compare migrants with residents in a calculus-based model. General claims of 'previously adaptive cue loses value' or 'a forecast error is equivalent to a fitness loss' are prior-art collisions. Crucially, PAYOFF-B's Gaussian expected squared phase loss is not demographic survival/reproduction evidence.

4. **Jonzén et al. (2007), Proceedings of the Royal Society B** (https://pmc.ncbi.nlm.nih.gov/articles/PMC1685845/): knowing the proper spring schedule does not imply that fitness-optimal migrants should perfectly match it; arrival and migration costs create rational under-tracking. This competes with a presumed 'information failure'.

## Source audit: what is actually available

- Original GitHub https://github.com/briana-abrahms/CraneMigrationSpeed lists ONLY README.md and crane_migration_speed_Github.r. Its script requires 'crane_data.csv'; the file is not hosted there. GitHub repository file listing was independently checked, not inferred from the README.
- Abrahms et al. point to the publicly archived Movebank dataset DOI https://doi.org/10.5441/001/1.t23vm852 (the original publication specified one-year embargo). Actual package events, reference metadata, age/group association fields, and decision-time cue availability have **not** been downloaded/verified for this PAYOFF branch.
- Article Methods: original env variables are MODIS 8-day NDVI and SNODAS daily snow depth annotated at the *observed location*, not a verified predeparture prediction of a distant future spring. Original response is local next-leg latitudinal migration speed. Therefore original weather-age response can arise from direct contemporaneous local forcing rather than updated predictions about remote spring.
- No independent breeding-resource synchronization response or reproductive/survival endpoint has been admitted under a new prospective contract; no empirical learning-rate w was estimated. No regime-shift breakpoint was predeclared using this source.

## Binary admission verdict

| Criterion | Status | Basis |
|---|---|---|
| Named public longitudinal natural system | PASS | 2021 paper and archive DOI |
| Original data actually materialized and checked in PAYOFF | HOLD | archive not yet ingested; original GitHub code-only |
| Decision-time origin forecast known to bird | HOLD | no original prospective remote signal timestamp |
| Checkpoint cue adds out-of-sample forecast value | HOLD | new target/cue audit not run |
| Choice between genuinely independent social and experienced information | HOLD | labels 'young' and 'old' do not identify source quality |
| Climate-shift regime with enough held-out support | HOLD | no independent time-series break validated |
| Physiological recourse separately estimable | HOLD | no independent constraint estimation |
| Individual behavior consistent with old-forecast error and alternative models rejected | HOLD | prior analyses focused local forcing/age |
| Reproductive or survival fitness efficacy demonstrated | HOLD | absent |
| Novelty of generic environmental-cue versus temporal-cue reversal | NO | Torstenson & Shaw (2025) |

## Publication decision

**Do not promote PR #315 into a stand-alone biological paper.** It is a useful conditional counterexample and a transparent negative source/novelty audit, not a new empirical discovery. Stop adding extra Gaussian cue-learning variants in lieu of data. PRs #311/#314 may remain exploratory theoretical tools, and PR #315 must not be merged as a confirmation.

To reopen prospectively, first acquire the original movement and reference data **and** independently dated phenological targets and cue histories. Freeze a training-before-test climate window, unique pair-year dependence and a separately measured behavioral endpoint before seeing its outcome. Establish direct-local-forcing and fully-informed-costly-undertracking rivals before attributing response to information updating.

### Current PAYOFF-B synthesis, without rescue

- V7R's fixed 10-transition Q-by-population-recourse-proxy primary was unsupported (within-flyway permutation p=0.56994). Active behavioral feedback was not identified.
- V8 found historical source-destination environmental correlation strengthened (166 unique spatial pairs, average delta-rho +0.3690) but a registered correlation-change to matching-improvement transfer was unsupported (beta +0.06244, 95% pair-bootstrap CI -0.01411 to +0.13635).
- These outcomes reject two *simple* explanations; they do not demonstrate that source memory, biological actionability or strategic coordination caused missing phenological matching.

**The ecology-first unresolved question:** In genuinely interacting ecological systems, when is imperfect spring matching optimal rather than informationally constrained? Distinguishing those requires predecision actions, independent information and recourse, ecological costs, and downstream biological success. It is a future empirical test, not a novel result already extracted from this dataset.
