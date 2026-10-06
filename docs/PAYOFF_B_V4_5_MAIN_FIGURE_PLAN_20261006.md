# PAYOFF-B V4.5 main-figure plan — 2026-10-06

Status: **CURRENT MAIN-TEXT FIGURE STRATEGY**

The paper should use three main figures following:

    forecastability -> accessibility -> actionability -> correction.

## Figure 1 — Forecastability is not usable biological information

Purpose:
Define the conceptual hierarchy before showing natural systems.

Panel A:
Environmental forecastability for an ideal observer.

Under squared loss:
    R0 = sigma_Y^2
    G_E = sigma_Y^2 rho^2
    R1 = sigma_Y^2 (1-rho^2)

Panel B:
Organismal information access.

Show:
    I_O(t) subset of I_E(t)
    G_O(t) <= G_E(t)

Label this as established decision-theoretic monotonicity, not a novelty claim.

Panel C:
Actionability.

    N(t) = r(t) G_O(t) - C(t)

Show declining r(t) and an intermediate maximum in usable information.

Panel D:
Downstream phase correction:

    e_(t+1) = phi_t [e_t - u_t] + w_t.

Reader takeaway:
Forecastable environmental structure is only the first stage; organisms must
access information and retain correction options.

## Figure 2 — Bird system: forecastability increased without proportional arrival adjustment

Purpose:
Separate the external environment from population timing without claiming cue
use.

Panel A — preregistered environmental coupling
- rho 0.284 -> 0.653.
- clearly label preregistered.

Panel B — posthoc forecastability on decision-loss scale
- target anomaly SD 2.41 -> 4.66 d;
- G_CV -16.1 -> +16.0 d^2;
- delta +32.1 d^2;
- 139/166 pairs positive;
- 25/28 species positive.
Use distribution + interval rather than only bars.

Caption sensitivity:
- climatology baseline +22.37 d^2;
- rank 1/2/3 all positive;
- nearest > third-nearest on equal-species contrast.

Panel C — observability boundary
Use the restricted 31-pair/14-species stage subset.

Stacked event-order proportions by period:
- source mid-green-up before source-front arrival;
- between source and target front arrivals;
- after target-front arrival.

Annual-row proportions:
early:
  29.8% / 29.6% / 41.6%.
late:
  45.8% / 18.3% / 36.1%.

Reader takeaway:
the reconstructed predictor is retrospectively forecastable but is not a
demonstrated online cue at the mapped source stage.

Panel D — realized population timing
- target green-up shift -2.31 d;
- bird arrival shift -0.19 d;
- signed lag shift +2.12 d.

Optional small inset:
restricted stagewise transformation -3.57 -> -4.95 d, with explicit
measurement-uncertainty caveat.

Do not use the raw delta-G_CV transfer slope as a biological result. Put the
structural-null transfer in supplement.

## Figure 3 — Mule deer: individual downstream correction is real

Panel A:
start and end signed Days-From-Peak:
SD 26.41 -> 13.17 d;
variance ratio 0.249.

Panel B:
start phase vs movement rate:
+0.0683 km/d per phase day.

Panel C:
start phase vs stopover:
-0.492 d per phase day.

Panel D:
serial schematic:
entry phase -> accessible local phase information -> signed actuator -> end phase.

Reader takeaway:
downstream correction is a real individual-level mechanism, even though the
bird analyses do not identify it.

## Supplementary figures

Move out of main sequence:
- source/target/two-way/spatial-block rho dependence;
- alternate windows and Fisher-z;
- in-window RMSE;
- climatology baseline;
- source-rank full results;
- exact-complete and year-leverage G_CV;
- delta-G_CV transfer structural nulls and permutations;
- broad source-to-arrival lead result;
- stagewise subset representativeness;
- stagewise measurement propagation;
- inverse-variance sensitivity;
- non-identifiable retention slopes;
- readiness / IFBFat sensitivities;
- failed speed-change and hysteresis gates.

## Main-text logic

Figure 1:
what must be separated.

Figure 2:
the bird data estimate external forecastability and population timing, while
revealing that the reconstructed predictor is not equivalent to an observed
cue.

Figure 3:
an independent natural system shows what true individual downstream correction
looks like.

No figure should imply that the mule-deer mechanism caused the bird pattern.
