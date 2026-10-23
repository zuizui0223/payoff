# PAYOFF-B — Sensory experiment: device allocation versus capture (2026-10-23)

Original source: Pollonara et al. (2015), Scientific Reports, DOI https://doi.org/10.1038/srep16486, Movebank CC0 archive https://doi.org/10.5441/001/1.tc76g560. The published navigation findings are **prior art**, not newly established PAYOFF-B effects.

## Critical source correction

The 32 displaced Calonectris diomedea were allocated to control 9, magnetic disruption 9, and olfactory deprivation 14. The paper's *Tracking system* section states that **GPS was equipped on 9/9 control, 9/9 magnetic, but only 9/14 olfactory-deprived birds**. The other **5/14 olfactory-deprived birds received Argos transmitters by design** because GPS device recovery could be difficult if olfaction was impaired. The archive's already MD5-verified reference/telemetry QC gives GPS-captured subjects 8, 9, 6; Argos subjects 0, 0, 5.

| Arm | All birds | Initially GPS-equipped | Valid GPS subjects | Valid GPS per equipped | Argos subjects |
|---|---:|---:|---:|---:|---:|
| Control | 9 | 9 | 8 | 8/9 | 0 |
| Magnetic disruption | 9 | 9 | 9 | 9/9 | 0 |
| Olfactory deprivation | 14 | 9 | 6 | 6/9 | 5 |

The apparent GPS coverage of 6/14 among anosmic birds is **not** a valid GPS device failure rate: 5/14 never had GPS assigned. Among GPS-equipped birds, the respective valid-source rates are 8/9, 9/9 and 6/9.

An exact conditional three-arm 3×2 probability-ordered association test restricted to the **27 GPS-equipped** subjects yields p=0.28 (GPS capture 8/9, 9/9, 6/9). Olfactory versus other GPS-equipped subjects gives two-sided Fisher p=0.0933. This is descriptive, post-source association only. It is **not a randomized test of navigation treatment**, and low n does not establish missing-at-random.

By comparison, all 32 original subjects' GPS yes/no table yields p≈0.0043, but this is dominated by the **treatment-specific preassigned GPS/Argos modalities** and must not be interpreted as olfaction causing GPS failure.

## Consequences for information × recourse research

The original paper's sensor methods explicitly state that a head-mounted magnet could interfere with a magnetic GPS switch, and Argos had a 10h-on/48h-off duty cycle. Tracking modality and temporal resolution are therefore not exchangeable across arms.

For an arbitrary GPS-only per-bird binary outcome, olfactory-arm GPS records exist for only 6/14 subjects. Under no assumption about the 8 unmeasured outcomes (5 Argos-assigned and 3 GPS-equipped but without retained GPS), the full-arm mean is only partially identified over an interval of width 8/14 = 0.5714. Compared with the control arm, the missing-outcome interval width is 8/14+1/9 = 0.6825, regardless of any observed GPS-only binary outcome rates. **This is a mathematical identification limit, not a measured behavioral effect**.

The source can inform the design of a future intervention, but the original study already investigated olfactory/landmark-based route correction. A new PAYOFF-B test must separately define predecision information, independent actionability, and later route/phenology outcomes, with comparable instrument allocation and detection across arms.

### Verification
- Original experiment: https://www.nature.com/articles/srep16486
- Source-verified per-arm sensor coverage: data/payoff_b_shearwater_experiment_sensor_coverage_20261023.json
- Source QC workflow: https://github.com/zuizui0223/payoff/actions/runs/39865026438
