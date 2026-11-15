# PAYOFF-B annual synchrony: shared-plant-reference falsification

**2026-11-15 | PR #361 | original-data CI https://github.com/zuizui0223/payoff/actions/runs/43670929865 | 98 tests passed**

Original JMA event dates, fixed 20-year station/event panels, directly matched station-years, leap-year normalized. Only bird/insect first sightings and plant flowering, all original rm codes (uncertified).

| Period | Direct bird–insect annual event anomaly r (matched stations) | (Bird−plant A) vs (insect−plant B) r (matched stations) |
|---|---|---|
| 1961–1980 | +0.520648 (36) | −0.026035 (33) |
| 1981–2000 | +0.628986 (54) | +0.498936 (53) |
| 2001–2020 | +0.796201 (33) | +0.031927 (33) |

Trend-removed direct bird–insect r: +0.687263, +0.574903, +0.796310. Trend-removed disjoint-reference r: +0.148722, +0.635755, +0.030989.

The prior high correlation between bird−plant and insect−plant national lag trajectories (+0.877316 in 2001–2020) **is not robust to using disjoint plant references** (+0.031927 in the same period). Thus it cannot be used as independent evidence of coordinated resource mismatch; common reference variance is a plausible explanation, though changing reference composition also matters.

Direct bird–insect annual event-date anomalies remain positively correlated in all three periods, including after detrending. This is a stronger *descriptive* co-fluctuation observation but is still vulnerable to shared observer effort, climate co-forcing, source-event composition and spatial dependence. Source-event files are held constant across years within each station, but the direct annual series are national averages and do not imply identical bird and insect phenological cues or direct trophic interactions.

Plant A/B split: sort original source file IDs and alternate membership. This single deterministic split is **not** a randomization distribution or comprehensive sensitivity analysis; future tests should repeat disjoint splits and compute same-station-year paired plant reference effects. No independent measured weather/NDVI/biomass/fitness data have been fitted.

**Paper implication:** frame primary empirical finding as interannual bird–insect timing co-fluctuation with an explicit negative control against apparent mismatch synchrony from shared plant references, not as proof of cross-taxon ecological mismatch or adaptation.
