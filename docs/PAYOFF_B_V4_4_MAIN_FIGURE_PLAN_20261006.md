# PAYOFF-B V4.4 main-figure plan — 2026-10-06

Status: **CURRENT MAIN-TEXT FIGURE STRATEGY**

The main manuscript should use three figures following one biological sequence:

    forecast opportunity -> access/commitment -> correction.

## Figure 1 — From environmental signal to usable information

Purpose:
Define the layers that the empirical analyses keep separate.

Panel A — environmental forecast value

Under squared loss:

    R0 = sigma_Y^2
    G  = sigma_Y^2 rho^2
    R1 = sigma_Y^2 (1-rho^2)

with

    R0 = G + R1.

Show that higher rho need not imply lower absolute residual risk when
sigma_Y^2 changes.

Panel B — decision-scale forecast value

Define:

    G(t) = L0(t) - L1(t).

Clarify:
- G is expected-loss reduction on a declared decision scale;
- empirical G_CV is a cross-validated forecast-value proxy, not fitness VOI.

Panel C — retained correction opportunity

Reduced form:

    N(t) = r(t)G(t) - C(t).

Show increasing G(t), declining r(t), and an intermediate usable-information
maximum.

Panel D — serial correction after commitment

Minimal phase transition:

    e_(t+1) = phi_t(e_t-u_t) + w_t.

Reader takeaway:

> informative environments, temporal access, and corrective capacity are
> different stages of seasonal tracking.

Novelty boundary:
generic VOI, optimal stopping, feedforward/feedback and variance decomposition
are prior art.

## Figure 2 — Environmental forecast opportunity increased while bird arrival changed little

Purpose:
Make the bird result biological rather than a catalogue of sensitivities.

Panel A — the environmental target became more variable while coupling increased

Show:
- preregistered rho: 0.284 -> 0.653;
- target anomaly SD: 2.41 -> 4.66 d.

Label preregistered rho separately from posthoc SD.

Panel B — nonlocal source signal gained cross-validated forecast value

Primary trend-baseline G_CV:
- -16.1 -> +16.0 d^2;
- delta +32.1 d^2;
- 139/166 pairs positive;
- equal-species delta +20.87 d^2;
- 25/28 species positive.

Display:
- paired/distribution representation of delta G_CV;
- dependence-aware interval;
- small annotation that climatology-baseline delta remains +22.37 d^2.

Do not use a simple two-bar plot alone.

Panel C — the reconstructed signal became earlier relative to arrival

Show source-to-arrival lead:
- 5.47 -> 7.95 d;
- delta +2.48 d;
- 95% CI +1.91 to +3.05;
- equal-species delta +2.37 d;
- 21/22 species positive.

Annotate decomposition:
- source green-up shifted about -2.86 d;
- arrival shifted about -0.38 d in this subset.

Label this:
**temporal availability proxy**, not actionability.

Panel D — target phenology moved; bird arrival largely did not

Same frozen transfer sample:
- target green-up shift = -2.31 d;
- bird arrival shift = -0.19 d;
- signed lag arrival-minus-green-up:
  -7.81 -> -5.69 d;
  delta +2.12 d.

Show target and arrival period shifts on the same calendar-day axis.
The visual should make it obvious that the relative-timing change is produced
mainly by target movement.

Add one compact annotation:
delta-G_CV -> mismatch bird-specific increment after fixed-arrival null =
-0.56 d, CI -2.39 to +0.55.

Reader takeaway:

> the environmental signal became more valuable and earlier, but the estimated
> population arrival front remained comparatively rigid.

Do NOT use the absolute mismatch decline as a headline panel.

## Figure 3 — Downstream phase correction exists in a natural trajectory

Purpose:
Show the independent natural correction mechanism.

Mule-deer panels:

A. signed phase funnel:
- SD 26.41 -> 13.17 d;
- variance ratio 0.249.

B. start phase -> movement rate:
- +0.0683 km/d per phase day.

C. start phase -> stopover:
- -0.4919 d per phase day.

D. serial conceptual bridge:

    entry phase
      -> local phase information
      -> signed actuator
      -> end phase.

Reader takeaway:

> post-entry correction can transform initial timing error, even though the bird
> analysis does not identify this mechanism.

## Supplementary figures

Move to supplement:
- all pair/species rho sensitivity variants;
- source/target/two-way/spatial-block coefficient audits;
- alternate windows and raw correlations;
- in-window fitted residual RMSE;
- full trend-versus-climatology baseline comparison;
- year-leverage table;
- delta-rho transfer;
- delta-G_CV transfer and structural nulls;
- matched between-within analysis;
- green-up pixel-support audit;
- source-target temporal-order details;
- bird absolute mismatch sensitivity;
- mule-deer year-centered and IFBFat sensitivities;
- failed actuator-speed and hysteresis gates.

## Main narrative across figures

Figure 1:
what must happen between an environmental signal and realized timing.

Figure 2:
environmental forecast opportunity increased, but bird arrival adjustment was
limited.

Figure 3:
one biologically real route for downstream correction.

The main paper must not imply that Figure 3 is the mechanism causing Figure 2.
