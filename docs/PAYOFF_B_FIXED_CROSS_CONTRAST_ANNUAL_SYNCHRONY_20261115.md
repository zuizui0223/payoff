# PAYOFF-B fixed-panel interannual cross-contrast synchrony: real-data result

**2026-11-15 | PR #360 | original JMA CI https://github.com/zuizui0223/payoff/actions/runs/43670610066 | 97 tests passed**

Correlate 20 annual national mean lag anomalies for the same fixed-composition 20-year windows. Each contrast's fixed station/event-pair panel is internally constant, but **different contrasts do not have identical station sets**, and contrasts share source taxa. The reported r is descriptive, not a climate effect or independent biological synchrony test.

| Cross-contrast annual trajectories | 1961–1980 r | 1981–2000 r | 2001–2020 r |
|---|---:|---:|---:|
| Bird–plant vs insect–plant | +0.277141 | +0.836206 | +0.877316 |
| Bird–insect vs bird–plant | +0.561464 | +0.420610 | −0.119716 |
| Bird–insect vs insect–plant | −0.423351 | −0.097192 | −0.480559 |

Bird–plant vs insect–plant trend-removed r: +0.480143, +0.811186, +0.880280 respectively; same-sign annual anomalies: 10/20, 14/20, 18/20 years. Leave-one-year-out r for 2001–2020: 0.850403–0.925030.

**Key identification warning:** Let B, I and P denote first-sighting/flowering timing; then (B−P) and (I−P) both contain the same negative P component. Positive correlation can arise algebraically from variance in P even when B and I are independent. This is a shared-reference artifact, NOT by itself evidence that bird and insect timing synchronize or share climate cues. The national series also average different species and stations across contrasts. To claim biological co-response, next compare bird vs insect original timing anomalies directly on the same station/year, and implement a disjoint-reference/independent-plant-event control; then fit observed climate anomalies. The bird–insect annual correlations with other contrasts are heterogeneous and sometimes negative.

No weather, precipitation, snow, radiation, NDVI, biomass or fitness coefficient is fitted; no causal phenology mismatch demonstrated.
