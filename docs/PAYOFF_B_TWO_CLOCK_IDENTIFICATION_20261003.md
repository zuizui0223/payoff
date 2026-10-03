# PAYOFF-B two-clock empirical identification contract

Date: **2026-10-03**  
Status: **prospective post-freeze identification framework; frozen GEB V2 unchanged**

## 1. The problem

A phenological date by itself does not identify the mechanism that produced it.

The same shift can arise from:

1. a developmental / physiological timer whose rate or threshold changed;
2. an information-dependent decision controller;
3. a hybrid in which physiological readiness gates later decisions.

PAYOFF-B therefore uses evidence grades rather than assigning clock
architecture from taxon identity.

## 2. Timer evidence grades

### T0 — no timer evidence

No internal or event-timing quantity relevant to readiness is observed.

### T1 — event-timing compatible

A once-per-season event such as emergence, flowering, egg laying or migratory
departure is observed and covaries with environmental conditions.

This is compatible with a developmental timer but does not identify one.

### T2 — experimentally or longitudinally entrained event timing

A declared pre-event environmental driver such as temperature, photoperiod,
snowmelt or accumulated thermal exposure predicts or experimentally shifts
threshold-event timing.

This supports a **developmental/physiological timing pathway**, but still does
not imply one molecular oscillator.

### T3 — internal readiness mechanism measured

A physiological, endocrine, molecular, energetic or developmental state is
measured before the event and independently predicts threshold crossing or the
opening/closing of a feasible action.

This is the strongest timer evidence relevant to the PAYOFF-B readiness gate
\(G_t\).

## 3. Decision-controller evidence grades

### D0 — no decision evidence

Only a seasonal event date or endpoint is observed.

### D1 — cue-linked choice

A cue or state predicts a choice among still-available actions: depart/wait,
continue/stop, route A/B, longer/shorter stopover.

This supports decision dependence but not signed phase feedback.

### D2 — signed error-dependent correction

Incoming signed phase error predicts correction direction:

\[
e>0 \Rightarrow \text{advance},
\qquad
e<0 \Rightarrow \text{delay}.
\]

Equivalent continuous evidence is a prespecified action slope with the expected
sign plus support on both sides of zero phase.

### D3 — repeated infer–correct–propagate evidence

The same system supplies repeated checkpoints showing:

\[
e_{in}
\rightarrow
I_t
\rightarrow
u_t
\rightarrow
e_{out},
\]

with checkpoint information improving held-out prediction or prespecified
action, and downstream phase changing consistently with the correction.

D3 is the strongest functional evidence for the "Mikawa-Anjo clock."

## 4. Hybrid evidence

A hybrid classification requires evidence for both layers in the **same
system** and the correct temporal order.

### H1 — timer + decision coexistence

At least T2 and D1 are present, but readiness has not been shown to gate the
decision response.

### H2 — readiness-gated feedback

The signed decision response is weak/absent before readiness and appears after
the physiological gate opens.

Under the reduced linear model,

\[
u_t
=
G_t g_t\hat e_t.
\]

If

\[
E[\hat e_t\mid e_t]
=
K_t e_t,
\]

then the regression-scale phase-to-action slope is

\[
\boxed{
b_{u,e}
=
G_t g_tK_t.
}
\]

Thus a hybrid system predicts a **phase × readiness interaction**:

\[
\frac{\partial E[u_t]}{\partial e_t}
\approx
0
\quad\text{when }G_t\approx0,
\]

but

\[
\frac{\partial E[u_t]}{\partial e_t}
=
g_tK_t
\]

when \(G_t=1\).

This is a sharper empirical discriminator than taxon identity.

## 5. Relationship to phase retention

With readiness-gated decision control,

\[
\lambda_t
=
\phi_t(1-G_tg_tK_t).
\]

Therefore the action slope and mean retention are linked through

\[
\boxed{
\lambda_t
=
\phi_t(1-b_{u,e,t})
}
\]

only when \(u_t\) is expressed on the same phase-correction scale and the
declared linear model applies.

Most published speed and stopover coefficients are not already on that scale,
so the identity must not be applied mechanically.

## 6. Empirical classification of current PAYOFF-B systems

### Mule deer — T0 / D2

Source: Ortega et al. 2023 plus the post-freeze Source Data audit.

Evidence:
- continuous incoming Days-From-Peak phase;
- later animals move faster;
- later animals use shorter stopovers;
- early and late animals compensate in opposite directions in the source
  study;
- start-to-end phase variance contracts strongly.

Classification:

    TIMER = T0
    DECISION = D2
    HYBRID = NOT_IDENTIFIED

The route-wise internal information update is not measured, so D3 is not
claimed.

### Eurasian wigeon — T0 / D2-control-geometry, information link null

Evidence:
- signed phase contracts across consecutive staging transitions;
- historical predictive connectivity is measurable;
- preregistered predictive-connectivity × incoming-phase interaction is not
  supported.

Classification:

    TIMER = T0
    DECISION = D2_COMPATIBLE
    INFORMATION_LINK = REGISTERED_NULL
    HYBRID = NOT_IDENTIFIED

The null prevents treating historical route predictability as the controller's
information weight.

### Pink-footed goose — T1 / D1

Bauer et al. 2008 show that day length, local accumulated temperature and their
interaction predict departure and that cue importance changes along the route.

Classification:

    TIMER = T1_COMPATIBLE
    DECISION = D1
    HYBRID = CANDIDATE_NOT_IDENTIFIED

Day length can contribute to endogenous/photoperiodic timing and also enter a
departure rule. Without an independent physiological readiness state, the two
roles cannot be separated.

### Greater snow goose — T1 / prospective D1–D3 lane

Published route temperature predictability and cue-response literature provide
context; the registered GPS cue-uptake lane asks whether local temperature
weighting depends on independent predictive connectivity.

Classification:

    TIMER = T1_COMPATIBLE
    DECISION = PROSPECTIVE
    HYBRID = PROSPECTIVE

No outcome may be inferred from the registration.

### Bar-tailed godwit — T0 / D1-compatible

Population departure advanced while later stopover duration absorbed the
advance.

Classification:

    TIMER = T0
    DECISION = D1_COMPATIBLE
    HYBRID = NOT_IDENTIFIED

The published population pattern does not demonstrate individual signed phase
estimation.

### American redstart — T0 / D1-compatible

Delayed departure is followed by faster migration and a survival cost.

Classification:

    TIMER = T0
    DECISION = D1_COMPATIBLE
    HYBRID = NOT_IDENTIFIED

Only the delayed side is the relevant natural anchor here; bidirectional D2 is
not claimed.

### Osmia lignaria greenhouse warming — T1 only

The de Manincor et al. system measures emergence as a once-per-season event;
warming did not detectably shift bee emergence in the reported comparison.

Classification:

    TIMER = T1_EVENT_ENDPOINT
    DECISION = D0
    HYBRID = NO_CURRENT_EVIDENCE

The absence of a treatment response is not evidence for a rigid molecular
clock.

### Pulsatilla–Osmia grasslands — T1 only

Kehrberger & Holzschuh measure flowering and bee emergence phenology across a
temperature gradient.

Classification:

    TIMER = T1_EVENT_TIMING
    DECISION = D0
    HYBRID = NO_CURRENT_EVIDENCE

The data establish differential event sensitivity, not the underlying
physiological threshold mechanism.

### Kudo–Cooper Corydalis–bumblebee system — T2 candidate

The source includes long-term phenology plus a snow-removal experiment and
degree-day/snowmelt drivers.

Classification:

    TIMER = T2_CANDIDATE
    DECISION = D0_FOR_CURRENT_ENDPOINTS
    HYBRID = NOT_IDENTIFIED

A direct physiological readiness variable is not part of the current PAYOFF-B
evidence, so T3 is not licensed.

### European tits / flycatchers — T1 plus interaction-response evidence

Laying dates respond differently to temperature and the resident–migrant
laying interval widened through time.

Classification:

    TIMER = T1_EVENT_TIMING
    DECISION = NOT_IDENTIFIED_FROM_LAY_DATE
    INTERACTION_MISMATCH = SUPPORTED

These data support the outer consequence
response-asymmetry -> mismatch, not its decomposition into \(G,K,g,\phi\).

### Pied-flycatcher settlement manipulation — D1

Heterospecific phenology was unavailable to an earlier settlement decision but
affected a later settlement decision in the source-backed manipulation.

Classification:

    TIMER = NOT_IDENTIFIED
    DECISION = D1_INFORMATION_TIMING
    HYBRID = NOT_IDENTIFIED

This is evidence that cue availability depends on decision stage, not evidence
for a physiological gate.

## 7. What would directly separate the two clocks in one system

The clean design measures, on the same individuals:

1. a predecision physiological readiness state \(z_t\);
2. a signed ecological phase error \(e_t\);
3. a checkpoint cue \(I_t\);
4. a choice/actuator \(u_t\);
5. downstream phase \(e_{t+1}\).

Then fit a prespecified interaction such as

\[
u_t
=
a
+
b_e e_t
+
b_G G_t
+
b_{eG} e_tG_t
+
\cdots.
\]

The hybrid prediction is

\[
b_{eG}\ne0,
\]

with weak signed correction before readiness and stronger correction after the
gate opens.

This directly asks whether the physiological clock controls **when correction
becomes possible**, while the decision clock controls **which correction is
chosen**.

## 8. Claim boundary

Do not infer clock type from:
- taxonomy;
- a single phenological date;
- temperature sensitivity alone;
- migration distance;
- phase contraction alone.

The strongest current natural evidence is asymmetric:

- mule deer provide strong decision-feedback geometry but no direct readiness
  mechanism;
- plant/insect emergence and flowering systems provide event-timing/timer-like
  evidence but little or no signed decision feedback;
- no current PAYOFF-B natural system identifies T3 + D3 + H2 together.

That missing hybrid test is now the cleanest prospective empirical target.
