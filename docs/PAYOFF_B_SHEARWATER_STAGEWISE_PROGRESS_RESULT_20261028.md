# PAYOFF-B 2015 experimental shearwater stagewise progress reanalysis

**2026-10-28 | Original CC0 GPS | Exploratory secondary movement proxy, not a new independent biological effect.**

The originally published experiment (Pollonara et al. 2015, Scientific Reports 5:16486, DOI 10.1038/srep16486) already established an olfactory navigation deficit offshore and a coastal-landmark compensation phenomenon. That behavior is **prior art**. This code reports a new mechanical first-versus-second 12-hour physical progress index, without claiming a new sensory or ecological law.

The pre-outcome source gate established high-frequency GPS quality in 22 individuals (8 controls, 8 magnetic disruption, 6 olfactory deprivation), preserving original GPS device-assignment denominators 9/9/9, original experimental denominators 9/9/14 and five anosmic Argos allocations by design. Original GPS/reference MD5 checksums were independently reproduced.

For each retained 12-hour interval since the first valid GPS fix, calculate geodesic length of original GPS path and distance-to-colony progress, using the published Pianosa colony midpoint. The index is (colony distance at start – at end) / travelled path length, in [-1,1]. A positive second-window minus first-window index is only an **arbitrary directional-improvement proxy**.

| Original treatment | Assessable GPS birds | Median early index | Median later index | Median within-bird later-minus-earlier change | Positive within-bird changes |
| --- | ---: | ---: | ---: | ---: | ---: |
| Control | 8 | +0.658 | +0.606 | **−0.046** | 3/8 |
| Magnetic disruption | 8 | +0.607 | +0.442 | **−0.139** | 1/8 |
| Olfactory deprivation | 6 | +0.077 | −0.194 | **−0.241** | 2/6 |

**No within-day timing-rescue or information-access conclusion follows.** In all three groups, observed median change is negative in this selected first 24h source window. The original authors' coastal visual compensation may have occurred at an entirely different stage and is not contradicted by these arbitrary windows.

### Original treatment-denominator missingness bounds

Among all originally treated animals, sharp no-assumption intervals for proportion with a positive early-to-late proxy change are: control 3/9–4/9; magnetic 1/9–2/9; anosmic 2/14–10/14. Corresponding anosmic-minus-control difference is **−0.3016 to +0.3810**; its sign is unidentified. The magnetic-minus-control proxy difference has a negative arithmetic bound, but is neither a prespecified biological treatment effect nor a well-identified measure of magnetic information loss; do not promote it as contradicting the published paper's magnetic navigation results. Arm randomization was not verified and sensor coverage differs.

These bounds treat all unevaluated subjects as potentially positive or negative, without making missing-at-random assumptions or mixing low-resolution Argos with GPS. They do not imply a causal effect of sensory manipulation.

### Identifiability stop

Original experiment and prior source results do **not** directly measure cue-arrival time, when coast/landmarks became perceivable, a feasible remaining route-correction capacity independent of focal future behavior, a flowering/seasonal destination mismatch or subsequent biological fitness. Thus PAYOFF-B information × effective deadline is still untested in nature.

To test the actual theoretical claim, event alignment should be defined by **availability of an alternative cue**, not elapsed hours since first GPS. A new sufficiently powered and comparably instrumented prospective cohort must supply cue access, action, destination mismatch and ideally fitness. Existing V7/V8/stork53 non-support remains unchanged.

Source workflow: https://github.com/zuizui0223/payoff/actions/runs/40534864044
Machine-readable receipt: data/payoff_b_shearwater_stagewise_progress_result_20261028.json
