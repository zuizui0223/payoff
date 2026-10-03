# PAYOFF-B mule-deer serial handoff audit

Date: **2026-10-03**  
Status: **post-freeze frozen-within-branch test; frozen GEB V2 unchanged**

## Frozen prediction

The simple serial handoff predicted that, within the temporally safe IFBFat subset, downstream phase should be conditionally associated with entry phase while March IFBFat should add little once entry phase is known:

DFP_End ~ DFP_Start + scaledIFBFat.

The frozen `HANDOFF_COMPATIBLE` rule required a positive DFP_Start coefficient with animal-cluster 95% CI excluding zero and a scaledIFBFat interval spanning zero.

## Result

Sample: **62 animal-years / 40 deer**.

Raw multiple regression:

- DFP_Start coefficient = **+0.215**, animal-cluster 95% CI **[-0.008, +0.422]**;
- scaledIFBFat coefficient = **-2.520**, 95% CI **[-5.807, -0.449]**.

The frozen rule therefore returns:

`SERIAL_HANDOFF_OUTCOME = NOT_COMPATIBLE`

All 40 leave-one-animal-out DFP_Start coefficients remained positive (+0.153 to +0.258), but clustered uncertainty still crossed zero.

After within-year residualization:

- DFP_Start = +0.259, 95% CI [-0.062, +0.515];
- scaledIFBFat = -2.290, 95% CI [-5.585, +0.848].

Thus the raw conditional IFBFat association is not invariant to the year-structure sensitivity.

## Interpretation

The simplest Markov-style handoff—physiological condition affects only entry timing and has no additional association with downstream phase once entry phase is known—is **not supported** by the frozen primary test.

This does not falsify the distinction between an entry clock and a decision controller. At least three explanations remain compatible with the data:

1. physiological state or its consequences persist beyond entry;
2. IFBFat is associated with unmeasured route, energetic or annual factors affecting downstream phase;
3. measurement error in DFP_Start weakens the conditional entry-phase coefficient and leaves residual association with IFBFat.

The year-centered analysis cannot distinguish these explanations because both conditional coefficients are unresolved.

## Claim boundary

This result may motivate a persistent-state extension, but because that extension is formulated after seeing this result, the mule-deer data cannot be used as confirmatory evidence for it.

The licensed natural statement remains:

> Mule deer support coexistence and channel dissociation between a predeparture physiological timing correlate and signed postdeparture behavioral correction, but they do not currently support a pure entry-only Markov handoff.