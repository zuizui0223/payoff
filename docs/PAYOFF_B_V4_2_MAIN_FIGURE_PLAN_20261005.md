# PAYOFF-B V4.2 main-figure plan — 2026-10-05

Status: MAIN-TEXT FIGURE STRATEGY

The main manuscript should use three figures. Each figure corresponds to one
step of the ecological argument rather than one dataset or one analysis family.

## Figure 1 — When information becomes actionable

Purpose:
Show the core theoretical prediction visually before introducing empirical
systems.

Panels:
A. Cue reliability q(t) increases through the seasonal sequence.
B. Retained actionability r(t) decreases through the same sequence.
C. Their decision value r(t)V_A(q(t)) is hump-shaped, defining three regions:
   too early to know; actionable-information window; too late to change.
D. Two actors with the same q(t) but different rates of actionability loss have
   different optimal commitment times.

Required annotation:
t* = log(1 + alpha/beta) / alpha for the exponential special case.

Reader takeaway:
The best forecast can arrive after the best time to use it.

Do not include:
- full Gaussian filtering;
- network Laplacian;
- coordination game;
- additional theory extensions.

## Figure 2 — Better environmental predictability did not yield better tracking

Purpose:
Use the bird analysis as a falsification of the simple information-degradation
story, not as proof of actionability loss.

Panels:
A. Early versus late source-destination spring correlation, with the shift from
   mean rho 0.284 to 0.653.
B. Distribution or species-level summary of delta-rho, emphasizing mean
   +0.369 and 26/28 positive species means.
C. Dependence-aware robustness: source cluster, target cluster, two-way
   source-target, 5-degree block, 10-degree block, and leave-one-year-out
   summaries shown as intervals or compact coefficient plot.
D. Registered transfer result: observed delta-mismatch ~ delta-rho coefficient
   alongside the fixed-arrival structural null and permutation-null range.

Reader takeaway:
The environmental forecasting coordinate improved strongly, but the predicted
improvement in realized mismatch did not follow.

Critical visual rule:
Do not plot the raw positive transfer slope as a biological effect without the
structural null on the same panel.

## Figure 3 — Seasonal trajectories can correct phase after entry

Purpose:
Show the biological reality of the downstream controller using the mule-deer
source-data reanalysis.

Panels:
A. Start and end Days-From-Peak distributions or paired phase funnel:
   SD 26.41 d -> 13.17 d; variance ratio 0.249.
B. Start phase versus movement rate:
   +0.0683 km/day per phase day.
C. Start phase versus stopover use:
   -0.4919 d per phase day.
D. Compact serial schematic:
   entry phase -> signed correction -> end phase.

Reader takeaway:
Departure timing is not arrival timing; individuals can measure signed temporal
error indirectly through local resource phase and alter progression en route.

Claim boundary:
The figure shows phase-dependent correction and convergence. It does not show
direct estimates of q(t), r(t), internal belief, or the theoretical t*.

## Main-text narrative across the figures

Figure 1: why better information can fail in principle.
Figure 2: the simple information-loss explanation fails prospectively in birds.
Figure 3: downstream phase correction is biologically real in an independent
natural system.

Together:
forecast -> commit -> correct.

## Supplementary figures

Move all of the following out of the main figure sequence:
- raw versus detrended V8 sensitivity;
- alternate windows;
- species leave-one-out;
- Fisher-z transfer;
- matched between-within decomposition;
- green-up support diagnostic;
- mule-deer year-centered sensitivities;
- IFBFat channel-dissociation sensitivity;
- failed speed-change actuator gate;
- wigeon and hysteresis/reversal nulls.

Three main figures are sufficient for the current American Naturalist route.
