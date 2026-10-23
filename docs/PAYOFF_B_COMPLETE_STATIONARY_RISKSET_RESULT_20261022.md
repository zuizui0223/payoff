# PAYOFF-B full stationary-day risk set: original GPS result (2026-10-22)

Three published public CC0 Movebank GPS sources were read after original checksum validation, using the existing February–May and >=2 different UTC-hour-bin daily observation criteria. The entry rule is **three consecutive observed stationary days**, independent of whether movement will occur later. Actual northern movement is a later two-day LABEL, not an eligibility predictor.

| Taxon | 3-day stationary at-risk opportunities | Two-day northern movement candidates | Two-day nonmovement | Other movement | Future right-censored | Individual-years with risk days |
|---|---:|---:|---:|---:|---:|---:|
| Ciconia ciconia | 1,633 | 156 | 941 | 352 | 184 | 91 |
| Anser albifrons | 2,008 | 111 | 1,456 | 285 | 156 | 51 |
| Numenius arquata | 1,868 | 66 | 1,632 | 90 | 80 | 42 |
| Total | **5,509** | **333** | **4,029** | **727** | **420** | **184** |

Original prior event screening reproduced the same 145/106/59 7-day-deduplicated cases; 333 are unthinned daily candidate labels on overlapping risk sets, **not 333 independent departures**. The within-taxon observable movement proportions from cases divided by cases+stays are stork 14.22%, goose 7.08%, curlew 3.89%; these are source-window metrics under censoring and nonmove definitions, NOT annual migration risks or taxon-specific movement hazard parameters.

Three-day eligibility never uses future location. Day4/day5 future location is used ONLY for the *outcome* labels. Other movements and missing tracking data are separate excluded statuses, not nondepartures. This removes the previous 36-pair pilot's selective assumption that every sampled animal eventually migrated as an admission condition.

**Ecological finding ceiling:** full stationary source availability and heterogeneous recorded calendar timing patterns. No effect of local weather, cue predictability, bird cognition, feasible recourse, breeding benefit, or game-theoretic coordination has yet been estimated in the risk set.

Reproduction: https://github.com/zuizui0223/payoff/actions/runs/39721821673

Full counts by taxon-month and taxon-year:
`data/payoff_b_complete_stationary_riskset_20261022.json`.
