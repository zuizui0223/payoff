# PAYOFF-B: ecological discrimination gate — mismatch, information failure, and fitness-optimal undertracking

**Date:** 2026-10-10  
**Status:** Source-led research audit / prospective admission plan. No new natural outcomes analysed.  
**Branch basis:** `analysis/payoff-b-paper2-ecological-boundary-20261008`.  
**Freeze:** V3 / V7R / V8 estimates, code, primary decisions, and the V4 post-V8 integrated manuscript are unchanged.

## 1. Ecological question

**When a seasonal actor fails to follow the contemporaneous resource peak, is this informational maladaptation, an inability to revise an earlier decision, or fitness-optimal timing under ecological costs?**

These hypotheses are observationally confounded by timing data alone. The central distinction is between (i) deviation from the resource peak and (ii) regret against the actor's feasible, informed, fitness-maximizing alternative. A nonzero phenological gap is NOT evidence of positive fitness regret.

For actor i in season t, record:
- H_it: biologically relevant resource or interaction state/peak, not an arbitrary green-up proxy;
- A_it: observed migration, nesting, flowering, or other commitment;
- I_it: information that was demonstrably available *before* that decision;
- F_it: independently measured set of feasible actions and subsequent corrections;
- W_it: survival, recruitment, reproductive success, or other fitness component, including movement/arrival costs.

A descriptive mismatch can be M_it = |A_it - H_it| where a common timing axis is defensible. A **conceptual** feasible-information fitness regret is

    Regret_it = max_{a in F_it} E[W_it(a) | I_it] - E[W_it(A_it) | I_it].

This is NOT directly identified from a resource time series or an observed arrival date. Identifying the counterfactual fitness surface requires suitable experimental, quasi-experimental, or independently defensible causal evidence. In particular, do not conflate a posteriori knowledge of H with what was knowable at action time.

## 2. Competing explanations to distinguish prospectively

| Explanation | Mechanism | Signature needed beyond raw mismatch | Primary rival |
|---|---|---|---|
| H_info: obsolete/insufficient forecast | Decisions follow an old or poorly calibrated cue -> future resource forecast | A dated, truly available remote cue, heldout historical-policy forecast error, and corresponding *signed* decision update or systematically erroneous commitment | Direct local forcing, calendar, costly optimum |
| H_cap: actionability limit | Better information arrives after an irreversible action, or feasible correction saturates | Independently measured movement/development/fuel boundary is hit; cue update would change optimal action but cannot move it | Inertia/calendars and deliberately costly nonresponse |
| H_cost: fitness-optimal undertracking | Actor knows enough but matching the peak incurs arrival, travel, predation, competition, or reproductive costs | A counterfactual fitness optimum away from the resource peak *inside* the independently feasible action set; no positive regret at observed action | Bad forecast and physical constraint |
| H_null: calendar / immediate physical forcing | Timing follows photoperiod or current thermal/fuel effects, without using predictions of remote spring | Historical clock and local forcing predict the next decision at least as well as conditional forecast innovation | H_info and H_cap |

A signed checkpoint innovation–behavior association is still not exclusive evidence of forecast-based decision making if that checkpoint weather directly affects fuel or flight. Distinguishing informational from direct forcing generally needs an intervention, exogenous signal separation, or an exceptionally strong natural design.

**Critical design principle:** all models receive the same source-defined decision dates, season blocks, individual structure, ecological targets, and outcome exclusions. Do not select the best mechanism by retrofitting unregistered proxies to V7R/V8.

## 3. New public-source triage (metadata / published abstract only)

### A. Lany et al. (2015/2016), black-throated blue warbler — direct fitness counterexample

- Dryad: https://doi.org/10.5061/dryad.g1m27
- Paper: https://doi.org/10.1111/oik.02412
- Archived file: `BTBW_data_Dryad.csv`; described as 25 annual summaries (1986–2010), including median arrival, first-clutch initiation, sugar-maple budburst / canopy phenology, caterpillar biomass, nest survival, and mean fledged young.
- **Published finding:** breeding tracked leaf phenology imperfectly, but the realized timing pattern maximized mean annual reproductive success in the authors' analysis; predation was a major fitness component. This is ALREADY IN PRIOR ART. PAYOFF-B cannot claim to discover that partial matching can be adaptive.
- Potential use: an independent ecological *negative control* against automatically scoring non-1:1 leaf-out tracking as maladaptation.
- Cannot provide: individually observed predeparture forecast, independent individual route recourse, or identified within-individual information-updating decisions.
- **Admission:** literature benchmark, not mechanistic PAYOFF confirmation. Raw file has not been fetched or reanalysed in this audit.

### B. Visser et al. (2015), pied flycatcher — arrival-temperature cost rival

- Dryad: https://doi.org/10.5061/dryad.cv24c
- Paper: https://doi.org/10.1371/journal.pbio.1002120
- 31-year population data link lay date and offspring with temperature and recruitment; published analysis identifies early cold-arrival costs as a possible influence on selection.
- Already known in PAYOFF-B's CV24C lane. Reuse only as an independently published **costly-undertracking rival**; not evidence of an informational timing mechanism.
- **Admission:** source-level comparison only; actual prior PAYOFF-B CV24C gate/receipt controls any further analysis.

### C. Nicolau et al. (2020/2021), pied flycatcher — arrival-to-breeding buffer

- Dryad: https://doi.org/10.5061/dryad.1g1jwsttq
- Paper: https://doi.org/10.1111/jav.02646
- Public description includes large-scale arrival and nesting phenology, 1986–2018 Devon timing, geolocator material, and fecundity analysis. The published study found timing changes without evidence that arrival-to-laying interval shortened, and no detected fecundity effect.
- Potential use: demonstrates that the arrival-to-laying stage itself needs explicit measurement; departure is not the only clock.
- **Admission:** descriptive comparator only; source-specific join keys, fitness measurement and actual cue dates not audited.

### D. Stehelin & Schmiegelow (2026), two aerial insectivorous birds — interaction-specific target check

- Dryad: https://doi.org/10.5061/dryad.sj3tx96hx
- Publicly listed files include `individualoffsets.csv`, `insect.csv` and fledging/survival inputs for olive-sided flycatcher and western wood-pewee. The source concerns fledging success, breeding stages and insect biomass.
- Potential use: test whether the *assumed resource peak* is truly the reproductive fitness optimum; do not treat insect biomass peak as synonymous with maximum fitness.
- **Admission:** source candidate only; no raw-data ingestion, no independent remote cue or route recourse verified.

**Source-status rule:** A Dryad landing page establishes the stated public archive and published-study context, not that raw files have been downloaded, joined or validated by PAYOFF-B. This note asserts no new coefficients or replicated published effects.

## 4. One ecology-first admission ladder

**Gate A — relevant target and realised fitness.** A named interacting resource and a reproductive/survival endpoint must be present. If only NDVI or departure/arrival is available, the analysis is a phase description, not a test of adaptive fitness.

**Gate B — time-valid information.** Prospective prediction uses only cues available at the individual's commitment time. Compare heldout climatology, calendar/photoperiod, direct local forcing, original-cue forecast, and original-plus-checkpoint conditional innovations. A retrospectively measured annual target is not a cue.

**Gate C — physiological action set.** Estimate correction feasibility from independent route/fuel/developmental constraints. Do not use stopover-vs-phase regression or population timing spread as the causal response boundary: fixed schedules can generate the same slopes.

**Gate D — behavioural discrimination.** Prespecify the next reversible action, its signed response to a verified forecast update, and direct-weather/calendar rival terms. Model within-individual and within-year dependence. A cross-site correlation is not a behavioural update.

**Gate E — counterfactual fitness.** Estimate whether the observed response was worse than a genuinely feasible, better-informed alternative after movement and early-arrival costs. If the causal fitness surface cannot be estimated, classify the result as mismatch/behaviour, not biological maladaptation.

**Stop immediately** if any required gate lacks independent evidence; do not increase taxon counts to compensate for a missing causal variable. Source material may still contribute to the paper as a documented falsification or prior-art constraint.

## 5. Fixed readout, without retrofitting

A prospective empirical readout must report separately:
1. seasonal resource matching (days or an overlap measure);
2. out-of-time origin and checkpoint **forecast skill** (bias/MSE and calibrated uncertainty);
3. independently measured allowable corrections and their realized use;
4. an estimated cost-adjusted fitness optimum, or explicit `NOT_IDENTIFIED`;
5. comparison with fixed-calendar and direct-current-environment models.

The decisive ecology-first result is **not** just a correlation between stronger information and less mismatch. It would demonstrate when a statistically apparent mismatch constitutes positive counterfactual fitness regret, and why: unavailable information, unusable action, or costly rational restraint.

There is no universal additive identity “capacity deficit + coordination deficit + information deficit” without fixed counterfactual ordering and interaction assumptions. Distinct constraints can interact, so any decomposition needs an explicitly defined reference state or ordered/Shapley convention.

## 6. PAYOFF-B integration decision

- V8's registered environmental **degradation** hypothesis failed: 166 spatial pairs, mean change in signed detrended correlation +0.3690 (pair-bootstrap 95% CI +0.2984 to +0.4365).
- Its preregistered better-connectivity -> better-matching transfer was not supported (beta +0.06244; 95% CI -0.01411 to +0.13635); structural controls prohibit reading the positive slope as bird response.
- V7R's Q×route-recourse interaction was not supported (10 transitions; exact within-flyway one-sided p=0.56994).
- Neither failed prediction proves H_info, H_cap or H_cost. The existing V4 manuscript's theory-led **The American Naturalist** positioning remains appropriate; no Nature/PNAS/Ecology Letters upgrade is licensed by this source audit.
- The newly screened Lany source should be used to clarify the ecological question (fitness regret versus geometric matching), *not* as an invented new natural PAYOFF result.
- No frozen estimate/manuscript was changed; if any new source is admitted, freeze all temporal windows, source joins, targets, rival models and exclusions **before** opening its new outcome.

## References / audit trail

- Lany et al., *Oikos*, https://doi.org/10.1111/oik.02412 and Dryad https://doi.org/10.5061/dryad.g1m27
- Visser et al., *PLOS Biology*, https://doi.org/10.1371/journal.pbio.1002120 and Dryad https://doi.org/10.5061/dryad.cv24c
- Nicolau et al., *Journal of Avian Biology*, https://doi.org/10.1111/jav.02646 and Dryad https://doi.org/10.5061/dryad.1g1jwsttq
- Stehelin & Schmiegelow (2026), Dryad https://doi.org/10.5061/dryad.sj3tx96hx
- Kharouba & Wolkovich (2020), *Nature Climate Change*, https://doi.org/10.1038/s41558-020-0752-x — review on theory/data disconnect and fitness-based testing.
- Existing PAYOFF-B: `docs/PAYOFF_B_PAPER2_ECOLOGICAL_BOUNDARY_AND_PRIOR_ART_20261008.md`, `docs/PAYOFF_B_V8_POSTOUTCOME_PUBLICATION_DECISION_20261005.md`, `docs/PAYOFF_B_V7R_DIRECT_RECOURSE_RESULT_20261007.md`, `docs/PAYOFF_B_DECISION_TIME_FORECAST_GATE_20261008.md` (last document on separate prospective branch).
