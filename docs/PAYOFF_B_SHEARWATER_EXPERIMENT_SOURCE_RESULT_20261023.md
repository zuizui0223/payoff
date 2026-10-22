# PAYOFF-B experimental cue source — original quality and selection verdict

Date: 2026-10-23. Movebank Data Repository DOI 10.5441/001/1.tc76g560, public CC0. Published source: Pollonara et al. (2015), Scientific Reports, DOI 10.1038/srep16486. The published work displaced Calonectris diomedea around 400 km and compared control, magnetic disruption and temporary olfactory deprivation. **The navigational effects are prior art; this is source quality auditing, NOT a new biological effect test.**

## Original source verification

The original publisher GPS, Argos, reference and README files passed exact original MD5/byte-length checks in both CI workflows. The original 32-reference animal mapping uses treatment comments: control n=9, magnetic disruption n=9 and olfactory deprivation n=14. The original table misspells anosmic as **asnomic**, which is explicitly normalized; the source manipulation-type category alone is insufficient to distinguish the three groups.

| Original treatment arm | Reference birds | Birds with GPS | Valid GPS fixes | GPS birds with >=24h observed continuous segment, adjacent fixes <=6h | Birds with Argos |
| --- | ---: | ---: | ---: | ---: | ---: |
| Control | 9 | 8 | 6,039 | 8 | 0 |
| Magnetic disruption | 9 | 9 | 5,381 | 8 | 0 |
| Olfactory deprivation | 14 | 6 | 11,594 | 6 | 5 |

Original Argos: 147 valid fixes all in the olfactory-deprived arm, and zero original Argos tracks with a comparable continuous 24h segment under the same <=6h adjacent fix criterion. None of the 5 Argos animal IDs are identical to the 6 GPS animal IDs in that treatment group; 3 reference birds in that group and one control bird have neither publicly recorded stream in this original package. The distinct animal populations from each sensor were matched through the *publisher reference*, not inferred from trajectories.

## What the QC demonstrates

A controlled intervention does not automatically create a uniformly observed movement response. GPS sample coverage is 8/9, 9/9 and 6/14 across control, magnetic and olfactory arms. Argos sampling is entirely within the last arm. Therefore a naive comparison of pooled GPS+Argos record-level route curvature, departure time, or correction speed would mix sensory treatment with sensor modality, completeness, positional error and selective track loss.

All three treatment groups do contain at least five original GPS animals with >=24h continuous observation (8/8/6), satisfying the **source-only** pre-specified measurement gate. But sample sizes are small and original tracking attrition is treatment-dependent. No source ID, ring, location or exact event time is exported.

## PAYOFF-B scientific relevance and novelty ceiling

The published original paper already examined orientation, route efficiency, coast proximity, navigation decision points and breeding success. Reproducing the authors' anosmia effect would not be a novel PAYOFF-B discovery. A genuinely new general claim would require prospective, distinct experiments plus a new separable response: predecision access to information, independently estimated remaining feasible steering/time correction, and a downstream phase/fitness outcome. No such joint causal mechanism has yet been identified in this source.

Use this experiment **as a mechanistic prior-art calibration**, not as an independent positive test of PAYOFF-B's migration phenology information×recourse claim. Original non-supported V7R/V8 and stork 53-season tests remain unchanged.

Original source CI: https://github.com/zuizui0223/payoff/actions/runs/39864324003
Sensor-quality CI: https://github.com/zuizui0223/payoff/actions/runs/39865026438
Machine-readable audit: data/payoff_b_shearwater_experiment_sensor_coverage_20261023.json
