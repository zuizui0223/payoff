# PAYOFF-B Scotland nestling v1 body-mass contact pilot: null result (2026-11-16)

**Status:** original-data fit complete; frozen overall gate **HOLD**. Do not tune demand window, nestling age, peak-only features or multiple comparisons in response to this null. See source pre-fit freeze `docs/PAYOFF_B_SCOTLAND_NESTLING_V1MASS_RESOURCE_FREEZE_20261116.md`.

**Evidence:** source-verified CI https://github.com/zuizui0223/payoff/actions/runs/43885792204, 6 synthetic unit tests passed, original UKCEH EIDC DOI 10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3. Original file SHA256 verifies bird/nestling/resource/site/climate CSV bytes. Source pre-fit admission: 137 unique site-years, 44 sites, 4 years (2018–21), 420 unmanipulated blue tit nests, **3,085 first-visit nestling mass rows**. Date stage is first visit **5–9 days after first-recorded hatch**, not exact physiological age. Original brood success was *not* used to select this body-mass panel, preventing a specific selective-survival leakage. Still, only nestlings alive at v1 can have v1 mass; this is a selection limitation.

Outcome per independent site-year = equal-nest mean of first-visit nestling mass in **grams per chick**. Pre-visit caterpillar availability = uniform hatch day through +4 days, complete direct-support interpolation and no future food; grams and counts per standardized 30-hit branch beating remain distinct. Original `<0.02` mass is treated as [0,0.02]g bounds, missing positive-count mass is excluded. Only 2017+ measured-prey years used.

## Frozen models

- **A:** year, latitude, elevation, mean hatch DOY, mean clutch, mean observed v1 visit offset days, source March–Apr temperature, observed caterpillar seasonal peak count, signed peak-to-hatch interval.
- **B:** A + log1p(5-day **caterpillar count** per beating).
- **C lower/upper:** A + log1p(5-day source-measured **caterpillar mass g** per beating) for censored lower/upper.
- **D lower/upper:** B + same 5-day source-measured mass censored lower/upper.

Frozen ridge penalty 1 with train-only feature standardization, intercept unpenalized. Hold out full calendar years LOYO and full sites LOSO. Model MSE units are **squared nestling body mass g²** and are not comparable numerically to previous fledged/clutch MSE, which is squared proportion.

| Model | LOYO equal-year MSE (g²) | LOSO equal-site MSE (g²) |
|---|---:|---:|
| A | **0.866272** | 0.603527 |
| B count | 0.883993 | **0.575454** |
| C lower / upper | 0.891252 / 0.886259 | 0.603370 / 0.605428 |
| D count + mass lower / upper | 0.948125 / 0.945084 | 0.593247 / 0.595444 |

**Null:** no mass-specific incremental predictive benefit over B in either holdout scheme. In the year-heldout LOYO, adding mass made prediction markedly worse and did not beat A. The predefined conjunctive gate failed in **0 of 4 years**. Individual year D vs B LOYO MSE gains for lower/upper censor bounds: 2018 +0.004101/+0.005794; 2019 −0.148663/−0.151193; 2020 −0.018372/−0.016638; 2021 −0.093594/−0.082329.

### Source-relevant COVID-year sensitivity (prelisted)

Dropping 2020 leaves 116 site-years, 304 nests and 3 years. LOYO: A 0.872394, B 0.781770, D 0.789394 / 0.786436 — mass conditional on B still worsens. LOSO: A 0.604638, B 0.569821, D 0.587138 / 0.589623 — mass conditional on B still worsens. The original all-year null remains the main result.

## Ecological interpretation and theory-to-data boundary

The earlier site-year fledging outcome had an exploratory conditional **count + mass** predictive improvement in 2018–21, but that difference **does not propagate** to this earlier nestling first-visit mass endpoint under the fixed 5-day support definition. These analyses use different outcome biology, temporal windows (14 days versus 5 days), and partly different nest sets. No mediation, prey size compensation, causal body-mass development, energy transfer, or trophic resource-conversion mechanism is established. Failure is consistent with multiple unresolved alternatives: variation in nestling stage; adult diet choice and alternative prey; later food supply; predation; number of nestlings; habitat confounding; source selection; unobserved density dependence.

PAYOFF-B's information-commitment-recourse theoretical mechanism is **not tested** by Scottish resident blue tit resource phenology. Actual causal interaction requires, at minimum, independent timed food intake/feeding observations or manipulation and the individual's cue/decision state. Neither a high resource peak, a count-based temporal overlap nor a positive fitted mass coefficient alone would identify it.

**Stop:** Preserve both positive-and-negative observational receipts. Do not further optimize stage windows to rescue a hypothesis on this dataset. Future source gate for within-nest longitudinal change (v1 to v2) would require conditioning on measured age and explicitly modelling selective nestling mortality; do not assume first-visit mass equals growth rate. This narrow stage test is already complete.
