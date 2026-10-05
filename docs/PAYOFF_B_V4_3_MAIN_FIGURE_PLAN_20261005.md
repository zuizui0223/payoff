# PAYOFF-B V4.3 main-figure plan — 2026-10-05

Status: **CURRENT V4.3 FIGURE STRATEGY**

The main paper should use three figures. The figures follow the ecological
sequence:

    forecast value -> actionability -> correction.

## Figure 1 — Information value is not correlation

Purpose:
Separate standardized coupling, absolute forecast risk, and retained
actionability before showing empirical results.

Panels:

A. Prediction-risk decomposition under squared loss:

    R0 = sigma_Y^2
    G  = sigma_Y^2 rho^2
    R1 = sigma_Y^2 (1-rho^2)

with R0 = G + R1.

B. Two environmental states illustrating that rho and G can increase while
absolute residual risk R1 also stays high or increases when sigma_Y^2 grows.

C. Retained actionability r(t) declines through a seasonal sequence while
decision-scale information value G(t) changes. Net usable value is

    N(t) = r(t) G(t) - C(t).

D. Exponential special case showing an intermediate actionable-information
maximum and the existing closed-form t*.

Reader takeaway:
A cue can become more valuable without making the future absolutely less
variable, and valuable information still matters only while useful responses
remain available.

Do not make generic value of information or feedforward/feedback the novelty.
Those are established prior art.

## Figure 2 — Cross-site information gained value as destination spring became more variable

Purpose:
Show the posthoc scale decomposition alongside the preregistered correlation
result without mixing their evidence status.

Panels:

A. Preregistered environmental coordinate:
mean detrended source-destination rho 0.284 -> 0.653.
Annotate clearly: preregistered primary result.

B. Posthoc absolute environmental scale:
destination anomaly SD 2.41 -> 4.66 d.

C. Posthoc leave-one-year-out forecast comparison:
- source-informed RMSE 4.11 -> 4.17 d;
- target-trend-only RMSE 3.18 -> 5.86 d;
- source forecast skill -0.93 -> +1.70 d.

Show dependence-aware interval for the +2.63-d skill gain.

D. Bird tracking on the same day scale:
absolute arrival-green-up mismatch
- unweighted 8.42 -> 8.07 d;
- equal-species 9.04 -> 8.42 d.

Reader takeaway:
The destination became more variable, but cross-site information became much
more useful for held-out prediction and bird mismatch showed no corresponding
deterioration.

Critical claim boundary:
Do not infer that birds used the fitted source cue or that source information
caused mismatch stability.

Move the registered delta-rho -> delta-mismatch transfer and its structural
nulls to Supplementary Information. They remain important transparency checks,
but delta-rho is no longer treated as a complete decision-scale exposure.

## Figure 3 — Post-entry correction is biologically real

Purpose:
Use the mule-deer system as the independent natural anchor for the downstream
correction layer.

Panels:

A. Start/end signed Days-From-Peak distributions:
SD 26.41 d -> 13.17 d; variance ratio 0.249.

B. Starting phase vs movement rate:
+0.0683 km/d per phase day.

C. Starting phase vs stopover duration:
-0.4919 d per phase day.

D. Minimal serial schematic:

    entry phase -> phase information -> signed actuator -> end phase.

Reader takeaway:
Forecasting before commitment is not the only way to obtain seasonal precision;
post-entry correction can strongly compress inherited timing error.

Claim boundary:
The mule-deer data establish signed compensation and phase convergence, not
direct estimates of G(t), r(t), internal belief, or the theoretical optimum.

## Supplement

Move to supplement:
- pair/species rho sensitivities;
- source/target/two-way/spatial-block diagnostics;
- raw-vs-detrended and alternate windows;
- in-window fitted RMSE;
- delta-rho transfer and structural nulls;
- matched between-within result;
- green-up support diagnostics;
- mule-deer year-centered sensitivities;
- IFBFat channel-dissociation sensitivities;
- failed actuator-speed and hysteresis/reversal gates.

## Main message across figures

Figure 1:
what environmental information value means.

Figure 2:
its value can rise under increasing environmental variability.

Figure 3:
remaining error can also be corrected after commitment.

The main paper should not claim that Figure 2 identifies Figure 3 as the
mechanism in birds.
