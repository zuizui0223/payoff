# PAYOFF-B original NEON API product availability overlap — 2026-11-15

Original public NEON API queried successfully in CI: https://github.com/zuizui0223/payoff/actions/runs/43683164542

| Product | Product ID | Available site-months | Phenology shared sites | Phenology shared site-months | Shared years |
|---|---|---:|---:|---:|---|
| Plant phenology | DP1.10055.001 | 4,275 | 47 | 4,275 | 2013–2026 |
| Single aspirated air temperature | DP1.00002.001 | 9,419 | 47 | **4,004** | 2014–2026 |
| Breeding landbird point counts | DP1.10003.001 | 596 | 45 | **484** | 2015–2026 |
| Herbaceous clip harvest | DP1.10023.001 | 1,110 | 47 | **914** | 2014–2026 |
| Precipitation | DP1.00006.001 | unknown | unknown | **not estimable** | API siteCodes=null |

**Interpretation:** these are product-level site-month metadata intersections, **not raw observational sample joins**. A product available for a month may not have a valid flowering transition, daily weather, bird count or biomass observation on the same plot or date. Precipitation siteCodes=null is **missing availability metadata**, not zero sites or a negative ecological result. Raw API responses are SHA256-hashed and the JSON evidence receipt is uploaded to the workflow.

**Next data step:** query `/api/v0/data/DP1.10055.001/{site}/{YYYY-MM}` for one observed site-month (e.g. ABBY 2020-05), inspect file manifest and original CSV headers, download bounded original data with digest, then join corresponding temperature observations by exact site/day and plot. Do not fit an ecological coefficient until QA and phenophase definitions are certified.
