# Tokyo 2020: first original JMA weather × phenology event-date alignment

**2026-11-15 | PR #357 | original-data run https://github.com/zuizui0223/payoff/actions/runs/43667761160 | 93 tests passed**

Two independent original sources:
1. JMA Tokyo 2020 April daily weather HTML, 30 measured days, SHA-256 `09ba492a8d03c97dedfe9b28cdca54221a27ae617eb4efc1f5b1d84ae5b4a3cd`.
2. JMA official all-taxon 65-event archive, original 2020 station label `東京`, station ID **662**, 19 original calendar-valid biological events (all observed `rm=9`, original code meaning not yet certified).

The weather page URL uses **47662** as its meteorological station identifier; its mapping to biological station ID **662** is **not independently certified**. The same Tokyo name is a candidate matching hint, not a validated historical meteorological-to-phenology station ID crosswalk.

Original phenology events within April:

| Event | Date | April weather days strictly before event | April weather days on/after event |
|---|---|---:|---:|
| のだふじ開花 | 2020-04-07 | 6 | 24 |
| つばめ初見 | 2020-04-09 | 8 | 22 |
| しば発芽 | 2020-04-10 | 9 | 21 |
| いちょう発芽 | 2020-04-14 | 13 | 17 |

**Zero of the 19 phenology events have a complete immediately preceding 30-day weather window from April alone.** An earlier bug counted 30 April days before June events as a full immediate 30-day window; fixed with an exact 30-consecutive-calendar-day requirement and regression test.

This is **source event-date temporal alignment**, not an admitted meteorological explanatory model: original HTML weather quality codes and homogeneity numbers unavailable; precipitation `--` meaning uncertified; weather station code crosswalk unresolved; no NDVI/biomass; no weather effect estimate. Do not infer trophic match or climate causality.

Next minimum real-data action: retrieve original JMA daily March 2020 for Tokyo and certify official station code correspondence; then verify per-variable CSV quality and homogeneity numbers before fitting any pre-event features. For the 4 April events, March+April could cover immediate 30-day windows if original daily values pass those gates.
