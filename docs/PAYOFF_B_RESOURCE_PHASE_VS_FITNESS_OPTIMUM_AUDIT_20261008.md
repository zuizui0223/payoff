# PAYOFF-B ecology audit: resource-marker phase is not the fitness-optimal phase

Date: 2026-10-08
Status: **conceptual correction with published ecological anchors; no new measured fitness optimum in PAYOFF-B**.
Scope: manuscript V4 on draft PR #318. Frozen V3, V7R, V8 environmental results and all demographic receipts are unchanged.

## The unrecognized construct ambiguity

The original controller used e_t as error relative to a "seasonal optimum" while citing animal movement relative to a remotely sensed green-up peak. These are not the same construct. What an instrument observes is often a resource-centred deviation r_t; what a fitness-gradient model assumes is an organism-, life-stage- and context-specific optimum.

Let:

    r_t = animal or event date - measured resource-marker date
    delta_t = fitness-optimal event date - measured resource-marker date
    e_t = r_t - delta_t.

If the measured resource phase follows r_next = phi*(r - u) + w, then
the fitness-centred equivalent is:

    e_next = phi*(e - u) + (w + phi*delta_t - delta_next).

This is **simple exact change of coordinates**, not novel mathematics. It is crucial biologically: if delta is unobserved, fitting lambda for r cannot by itself determine lifetime-fitness tracking or the realized fitness effect of correction. The term involving changes in delta can produce apparent innovations without a change in physical resource phenology.

### Concrete witness (not new data)

In the experimentally studied winter moth–oak system (van Dis et al. 2023), the published composite fitness maximum was around **two days after** budburst. Under the reported marker convention, r=0 means hatching on budburst, but e=r-delta=-2 days relative to that experimental fitness peak. Thus "zero mismatch to oak budburst" does not equal zero experimental fitness-optimum error.

Aikens et al. (2021) provide a different stage-specific trade-off in Wyoming mule deer: short-distance migrants generally gave birth earlier than long-distance migrants, sacrificing some coincidence with resource phenology but plausibly allowing offspring additional time to grow before winter. The latter fitness benefit was proposed, **not established by offspring survival measurements**, and no numerical delta can be recovered from that publication alone. The sample is not assumed to be the same animals as Ortega et al. (2023).

Schindler et al. (2024) demonstrate that spring energetic expenditure and time spent feeding are associated with later breeding outcome in Greenland white-fronted geese. This is an independent source-backed reason why correcting calendar phase need not restore fitness. Their results were already published and should not be recast as a PAYOFF-B discovery.

## Direct prior-art collision

Torstenson & Shaw (2025, Oikos, doi:10.1111/oik.10862) already explicitly separate cue **accuracy** (timing relative to an optimum) from cue **efficacy** (fitness captured), and show reversals in relative cue-type performance under seasonality differences. Jonzén et al. (2007) had already demonstrated optimal incomplete tracking under biological arrival costs. PAYOFF-B cannot claim either distinction or a generic optimal mismatch as new.

## Implications for existing PAYOFF-B endpoints

| Dataset/theory endpoint | Observed coordinate | Fitness inference licensed? |
|---|---|---|
| V8 bird arrival - remote-sensing green-up | resource-alignment proxy, with range-derived source/target mapping | NO: no cue uptake, individual recourse, breeding/survival |
| Ortega 2023 mule deer Days-From-Peak (DFP) | resource-alignment phase on route | NO: speed/stopover compensation and convergence, not direct demographic fitness gradient |
| Schindler 2024 goose breeding outcomes | reproductive categories after spring feeding/energy data | Original ecological association yes; PAYOFF-B new effect NO (raw CSV access authorization HOLD) |
| van Dis 2023 winter moth experiment | manipulated hatch-to-budburst offset, survival/pupal-weight endpoints | Original experiment identifies a composite fitness optimum; not migrant cue use |
| Aikens 2021 mule deer reproduction | birth date, green-up, fetal development, birth mass; possible offspring growth season trade-off | Earlier birth timing observed, survival benefit of the early-birth strategy not identified |
| PAYOFF-B quadratic controller | theoretical e=event date - fitness-optimal target | Conditional model only; shape/scale of survival or reproduction loss not calibrated |

A common "greenness mismatch" response is not a universal fitness objective. Neither is a low raw mismatch necessarily optimal if it requires energetically costly migration or reduces offspring growth duration.

## What must be measured in a future decisive study

- A resource marker and fitness endpoints on **the same individuals and seasons**, with information on the relevant later-life deadline.
- Independently identified timing actions and their energetic or demographic costs; do not infer K(c) from covariance between stopover and arrival timing.
- Decision-time environmental cue availability, and whether the animal could plausibly perceive the cue, separate from retrospectively reconstructed green-up.
- Sufficient stage and life-history variation to estimate delta(context), including whether it changes sign; known phase error relative to one common marker is not enough.
- A direct competitor: a fully informed, costly-optimal actor. An imperfect match can be rational even without forecast failure.
- Source grain, repeated animals and overlapping climate fields accounted for; cohorts from different papers must not be pseudo-joined.

A potential substantive ecological advance would show a predictive *change in the relative fitness value of timing strategies*, rather than simply documenting another instance of mismatch. The natural dataset required for that claim has NOT been admitted in this repo.

## Sources

- Aikens EO et al. 2021. Migration distance and maternal resource allocation determine timing of birth in a large herbivore. Ecology. https://doi.org/10.1002/ecy.3334
- van Dis NE et al. 2023. Phenological mismatch affects individual fitness and population growth in the winter moth. Proc R Soc B. https://doi.org/10.1098/rspb.2023.0414
- Schindler AR et al. 2024. Energetic trade-offs in migration decision-making, reproductive effort and subsequent parental care in a long-distance migratory bird. Proc R Soc B. https://doi.org/10.1098/rspb.2023.2016
- Torstenson M & Shaw AK. 2025. Strength of seasonality and type of migratory cue determine the fitness consequences of changing phenology for migratory animals. Oikos. https://doi.org/10.1111/oik.10862
- Jonzén N et al. 2007. Climate change and the optimal arrival of migratory birds. Proc R Soc B. https://pmc.ncbi.nlm.nih.gov/articles/PMC1685845/
- Ortega AC et al. 2023. Migrating mule deer compensate en route for phenological mismatches. Nat Commun. https://doi.org/10.1038/s41467-023-37750-z

**Claim ceiling:** a source-backed modelling construct correction and ecological synthesis. No measured cross-species causal law, correction-to-fitness gain or direct fitness-optimum offset from PAYOFF-B is established.
