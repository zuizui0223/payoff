# PAYOFF-B fixed-composition interannual timing mismatch: original JMA source

**2026-11-15 | PR #359 | original-source CI https://github.com/zuizui0223/payoff/actions/runs/43670092816 | 96 tests passed**

To avoid changing station and event-pair composition across years, require every retained station–source-event pair to have a valid observed event date in **all 20 years** of a fixed block. Use three independently centered blocks: 1961–1980, 1981–2000, 2001–2020. A station's mean is averaged across all of its eligible source pairs, then stations receive equal weight in annual national mean lag anomaly. Leap-year day-of-year normalized; Feb 29 excluded.

| Fixed block | Bird first sighting – plant flowering (stations/pairs) | Insect first sighting – plant flowering | Bird first sighting – insect first sighting |
|---|---|---|---|
| 1961–1980 | 45 / 256 | 49 / 617 | 36 / 76 |
| 1981–2000 | 66 / 551 | 73 / 1161 | 54 / 112 |
| 2001–2020 | 40 / 288 | 43 / 483 | 33 / 53 |

**Actual annual examples, mean station lag anomaly in days:**

- Bird–plant, 1981–2000 fixed panel: 1981 **−8.1128**, 2000 **+5.5849**.
- Insect–plant, 1981–2000 fixed panel: 1981 **−3.4600**, 2000 **+6.2856**.
- Bird–insect, 1961–1980 fixed panel: 1961 **+4.8590**, 1980 **−6.4674**.
- Bird–plant, 2001–2020 fixed panel: 2001 **−5.0719**, 2020 **+1.6852**.

**Interpretation:** Year-to-year variation in relative original event timing persists even after fixing panel composition within each block. This is descriptive, not a significant linear trend, not a demonstrated food-web/resource mismatch, and not yet attributed to climate. Different 20-year panels contain different stations and event pairs, and each block is separately centered; do not compare their mean anomaly levels as one continuous trend.

**Next empirical tests:** calculate cross-contrast synchrony of annual national anomaly series on identical year blocks, fit annual measured climate anomalies using independently verified JMA station/weather records, and validate against out-of-year holdouts. Phenology original `rm` code meanings and observation effort remain unverified; NDVI and actual biomass have not been fitted.
