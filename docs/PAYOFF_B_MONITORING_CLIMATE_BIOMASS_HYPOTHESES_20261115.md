# PAYOFF-B: Monitoring Sites 1000 × climate × resource biomass integration

**Status: executable evidence gate, NOT a connected empirical dataset.** The Monitoring Sites 1000 actual source files, effort protocols, observation models and compatible biomass series have not been verified or joined in this branch. Do not invent monitoring site coverage, climate effects, or fitness estimates.

## Five preregisterable ecological tests

1. **Shared cue but divergent response (H1).** With fixed site, event and year definitions, estimate taxon-specific response slopes to *pre-specified* seasonal temperature/precipitation/snow/radiation anomalies. Test whether between-taxon slope heterogeneity predicts annual lag variation on held-out years. Control for source phenology observation effort and event-type comparability. This extends original JMA event-date work but is not yet a causal interaction claim.
2. **Resource exposure vs peak-date mismatch (H2).** Compare predictions of independently observed monitoring outcomes from (i) absolute peak-day lag, (ii) demand-weighted biomass exposure and (iii) both. Use the same fixed held-out sites/years and effort-aware outcome models. Existing `integrate_resource_biomass` already forbids substituting NDVI for biomass; `validate_site_year_bundle` now requires independent biomass, source-verified demand and matching site-year.
3. **Remote information disadvantage (H3).** For migratory versus resident birds, test whether predeparture-origin climate predicts destination resource phase less accurately than local pre-event climate, and whether route/stopover adjustment moderates residual arrival mismatch. This tests PAYOFF-B's two-clock readiness/actionability and incomplete-information controller; requires actual origin, departure, arrival and route data.
4. **Community buffering (H4).** Compare single-resource exposure with independently verified portfolio exposure across usable resource guilds. Hypothesis: higher functional redundancy weakens adverse association of one resource's temporal shortfall with abundance/breeding success. Monitoring occurrence counts cannot alone establish alternative resource *use*.
5. **Interannual carryover (H5).** Predict year t+1 abundance/breeding success from prior-year resource exposure, controlling for current climate, baseline population size, observation effort, and temporal autocorrelation. Cross-lag associations alone are not causal carryover.

## Measurement and analysis hierarchy

- **Climate**: original source quality and homogeneity codes, historical station crosswalk, fixed pre-outcome seasonal window; no leakage from using event-date-defined predictor windows in forecast models.
- **Phenology**: original JMA date events and first-sighting detectability; no first sighting = first emergence assumption. Fixed stations/source-event pairs and disjoint plant references.
- **Monitoring Sites 1000**: verify exact monitoring protocol, unit, repeat visits, detectability, observer effort, site-year ID and which outcomes (abundance index, occupancy, breeding success) actually exist.
- **Resource**: independent biomass in g/m², dry/fresh basis, guild, measured seasonal series and consumer demand window; greenness/NDVI remains a distinct proxy.
- **Outcomes**: use source-appropriate hierarchical count, occupancy or reproductive models; include site/event random or fixed effects, blocked holdout years and spatial sensitivity.
- **No claim** of resource mismatch cost without independently measured resource availability, consumer demand and outcome. Correlations between B−P and I−P sharing P can be algebraically inflated; keep the negative controls from PR #361–364.

## Current implementation

`src/payoff_b_monitoring_resource_bridge.py` validates four original-data channels for identical site/year, forbids NDVI substitution and outcome-derived biomass, and computes a demand-weighted mean resource biomass from explicitly dated observations. It does **not** fetch or assert Monitoring Sites 1000 data and does **not** fit climate or outcome effects. Synthetic tests only.

**Next source task:** identify one actual Monitoring Sites 1000 monitoring protocol and raw source archive with repeatable site-year outcomes, independently identify a compatible measured biomass and climate station source, and check overlap before fitting anything. If no overlap exists, treat H2 as not estimable and proceed with H1 only.
