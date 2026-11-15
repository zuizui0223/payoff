# PAYOFF-B: alternative public ecological data sources (2026-11-15)

**Decision:** Monitoring Sites 1000 access remains blocked; switch empirical H1 to NEON public products, retain USA-NPN as geographic replication and Hoge Veluwe as independently verified trophic resource/fitness validation.

## NEON products (official portal)

- Plant phenophase status/intensity: DP1.10055.001, RELEASE-2026, https://data.neonscience.org/data-products/DP1.10055.001/RELEASE-2026 . Repeated tagged individual observations with phenophase intensity, typically several observations/week during transitions; includes through 2025 and core sites thereafter.
- Air temperature: DP1.00002.001. Precipitation: DP1.00006.001. Check product data quality and site-year coverage in the actual files.
- Breeding landbird point counts: DP1.10003.001. Not migration arrival date or breeding fitness.
- Ground beetles: DP1.10022.001. Pitfall activity/counts are not pollinator visitation or prey availability for birds.
- Herbaceous clip harvest: DP1.10023.001. Measures plant biomass, not nectar, caterpillar biomass or bird food.
- Litterfall and woody debris: DP1.10033.001. Resource flux is not directly edible biomass.
- Plant presence/cover: DP1.10058.001. Cover not equivalent to biomass.

Official overview: https://www.neonscience.org/data-collection/terrestrial-plants and https://www.neonscience.org/data-collection/terrestrial-organisms .

## External replication / functional anchor

- USA-NPN observations, REST API and R package: https://data.usanpn.org/ ; https://nps.usanpn.org/data/code . Use for independent continental-scale plant phenology validation with effort-aware records.
- Hoge Veluwe original great-tit fitness and caterpillar peak dataset: https://doi.org/10.5061/dryad.f1vhhmgx6 . Existing PAYOFF-B source certification is stronger than for any new NEON join; prioritize for mismatch–fitness functional validation, but do not conflate peak date with full biomass time series.

## First empirical protocol

1. Retrieve NEON product metadata from the public API, enumerate actual site/month files for DP1.10055.001 and DP1.00002.001; do not assume matching site-years.
2. Fetch a small original sample of flowering status/intensity and temperature; record source URL, file hash, quality flags and actual date/site/individual columns.
3. Audit site-year intersections, revisit frequency and flowering transition interval-censoring. Keep same tagged individuals/sites within years and require adequate repeat years.
4. Test H1 using preregistered seasonal temperature anomalies and phenophase transitions, blocked by site and year. Compare slope heterogeneity and held-out-year prediction. Do not infer pollination or fitness.
5. Only add birds, beetles and biomass where ecological guild, demand and sampling grain support the specific interaction; no generic multi-taxon overlap claim.

**Status:** official catalog product IDs verified, original NEON observations **not yet downloaded**. No climate–phenology coefficient or site-year intersection calculated.
