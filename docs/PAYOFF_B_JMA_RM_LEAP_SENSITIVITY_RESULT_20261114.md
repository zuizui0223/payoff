# PAYOFF-B JMA cross-taxon coupling: rm-code and leap-day sensitivity

**2026-11-14 | PR #351 | original-data CI https://github.com/zuizui0223/payoff/actions/runs/43604843238 | 71 tests passed**

Original 160,367 calendar-valid JMA event cells. Exclude 88 Feb-29 rows; convert leap-year March–December day-of-year to a common 365-day scale, leaving 160,279 cells. Retain original `rm` codes without asserting any quality meaning. Split all observations, rm=8, rm=9, rm in {8,9}; calculate event-pair within-station correlations on >=10 shared years, then equally weight station means.

| Groups | All rm | rm=8 | rm=9 | rm in {8,9} |
|---|---:|---:|---:|---:|
| Amphibian–insect | +0.152411 | +0.170926 | +0.125457 | +0.161662 |
| Amphibian–plant/unclassified | +0.131851 | +0.172837 | +0.181611 | +0.127283 |
| Insect–plant/unclassified | +0.112870 | +0.115704 | +0.159910 | +0.111269 |
| Amphibian–bird | +0.110405 | +0.126479 | +0.107345 | +0.104760 |
| Bird–plant/unclassified | +0.090526 | +0.093613 | +0.124524 | +0.091115 |
| Bird–insect | +0.080510 | +0.085417 | +0.089311 | +0.083375 |

Original source rm counts after excluding Feb 29: code 8=116,822; 9=35,728; 6=4,625; 7=1,957; 3=1,103; 4=44. In each of the six group contrasts, both rm=8 and rm=9 strata retain positive station-balanced mean correlations. **This is robustness of descriptive observed-event association, not a quality-filtered or causal result**: code meanings are unverified, the strata differ in stations/years/event composition, and observed phenological events are not direct measurements of biomass or fitness.

Important next step: verify original `rm` meanings and phenology event types, then obtain actual JMA weather series and test whether temperature, precipitation, snow, humidity, radiation or wind explain station-year anomaly covariance. NDVI and independently measured biomass remain separate data layers; neither has been fitted.
