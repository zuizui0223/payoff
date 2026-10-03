# PAYOFF-B V3 main-figure architecture — 2026-10-03

Status: **post-freeze manuscript design; frozen GEB V2 figures unchanged**

## Figure 1 — From a latent spring to interaction mismatch

The first figure should carry the entire Paper-2 mechanism without requiring
the railway metaphor in the formal labels.

### Panel A — Information improves while actionability declines

Horizontal axis: route stage / decision time.

Show:
- cue quality \(q(t)\) increasing;
- retained actionability \(r(t)\) decreasing;
- actionable information value
  \(N(t)=r(t)[Sq(t)-B]-C(t)\) peaking at an intermediate stage \(t^*\).

Annotation:

> Best information use can occur before best information.

The “Schrödinger's spring” intuition can appear only in the caption or graphical
motif: the future target becomes clearer as the route progresses.

### Panel B — Two clock layers

Split the panel vertically.

**B1. Developmental / physiological timer**

\[
\dot z=v(E_t,z),
\qquad
z\rightarrow\Theta\rightarrow\text{readiness/event}.
\]

Use emergence/diapause as the visual example. Label this as a
**rate-to-threshold clock**, not universally as a molecular clock.

**B2. Inferential decision controller**

\[
e_t
\rightarrow
I_t
\rightarrow
\hat e_t
\rightarrow
u_t
\rightarrow
e_{t+1},
\]

with

\[
e_{t+1}=\phi_t(e_t-u_t)+w_t.
\]

Use two miniature paths:
- late \(e_t>0\) -> speed up / shorter stopover;
- early \(e_t<0\) -> slow down / longer stopover.

A migratory bird can contain both panels: an endogenous readiness programme
opens the decision window, then repeated route checkpoints provide
state-dependent control. The informal “Mikawa-Anjo clock” refers only to B2.

### Panel C — Natural mule-deer phase funnel

Use the post-freeze Ortega Source Data audit:

- \(n=152\) animal-years, 72 deer;
- start SD \(=26.41\) d;
- end SD \(=13.17\) d;
- variance ratio \(=0.249\);
- within-year ratio \(=0.294\);
- whole-route \(\lambda=0.107\);
- 70.4% ended closer to peak green-up.

Add signed actuator arrows:

\[
DFP_{start}\uparrow
\Rightarrow
speed\uparrow
\]

and

\[
DFP_{start}\uparrow
\Rightarrow
stopover\downarrow.
\]

Caption boundary:

> The natural convergence and bidirectional compensation are Ortega et al.
> prior art; PAYOFF-B uses the continuous source data as a quantitative anchor,
> not as an independent confirmation of the new controller theory.

### Panel D — Mean and variance signatures separate information from gain

Show:

\[
\lambda=\phi(1-gK)
\]

and

\[
P_{t+1}
=
\phi^2P_t[1-Kg(2-g)]+Q.
\]

With independently identified \(\phi,Q\),

\[
d=1-\lambda/\phi,
\qquad
v=(P_{t+1}-Q)/(\phi^2P_t),
\]

\[
K=\frac{d^2}{v-1+2d},
\qquad
g=\frac dK.
\]

Visual message:

> The same mean phase retention can hide different information × control
> architectures.

This panel is prospective identification theory, not a current natural
parameter estimate.

### Panel E — Controller asymmetry converts common error into mismatch

Two actors start synchronized:

\[
e_{1,t}=e_{2,t}=m_t.
\]

Give them different effective retentions \(\lambda_1,\lambda_2\).

Then

\[
\boxed{
\Delta_{t+1}
=
(\lambda_1-\lambda_2)m_t.
}
\]

For general states:

\[
\Delta_{t+1}
=
(\lambda_1-\lambda_2)m_t
+
\frac{\lambda_1+\lambda_2}{2}\Delta_t
+
\delta w_t.
\]

Graphically:
one shared climate arrow enters both actors; two different controller boxes
produce diverging timing trajectories.

This is the main ecological result of the post-freeze integration.

### Panel F — Recovery can fail in two distinct ways

Branch the final mismatch state into:

1. **physical/actionability loss**
   - accurate information arrives after useful actions disappear;
2. **strategic coordination trap**
   - correction remains physically possible but unilateral change is costly.

Caption:

> Controller asymmetry explains mismatch generation; irreversibility and
> coordination explain failure of recovery.

## Main-figure rule

Do not put every theorem into Figure 1.

The visual reading order should be:

\[
\text{learn}
\rightarrow
\text{correct}
\rightarrow
\text{diverge}
\rightarrow
\text{fail to recover}.
\]

The formal labels are:

\[
(q,r)
\rightarrow
(e,\hat e,u)
\rightarrow
\lambda
\rightarrow
\Delta.
\]

“Schrödinger's spring” and “Shinkansen” belong in the caption / talk version,
not as formal variable names.

## Figure 2 — Empirical map of the two clock layers

Use a 2D evidence map rather than a taxonomic comparison.

Horizontal axis:

\[
T0 \rightarrow T1 \rightarrow T2 \rightarrow T3
\]

for developmental/physiological timer evidence.

Vertical axis:

\[
D0 \rightarrow D1 \rightarrow D2 \rightarrow D3
\]

for information-dependent decision-control evidence.

Plot current systems with explicit evidence-status labels:

- **Ortega mule deer:** T0 / D2 — strongest signed feedback geometry;
- **Eurasian wigeon:** T0 / D2-compatible — correction present, registered
  information-link null;
- **pink-footed goose:** T1 / D1 — route-stage cue-dependent departure;
- **greater snow goose:** T1 / prospective decision lane;
- **bar-tailed godwit:** T0 / D1-compatible;
- **American redstart:** T0 / D1-compatible;
- **Osmia lignaria greenhouse:** T1 / D0;
- **Pulsatilla–Osmia grasslands:** T1 / D0;
- **Corydalis–bumblebee:** T2-candidate / D0;
- **European tit–flycatcher laying dates:** T1 / decision unidentifed;
- **pied-flycatcher settlement manipulation:** timer unidentifed / D1.

The upper-right corner, **T3 + D3 with H2 readiness-gated feedback**, is empty.

Main visual message:

> Existing systems identify either readiness/event timing or signed decision
> feedback well, but no current PAYOFF-B natural system identifies both clock
> layers and their gating interaction in the same individuals.

Use shape or border style to distinguish:
- PREREGISTERED;
- SOURCE-DATA REANALYSIS;
- PUBLISHED ANCHOR;
- PROSPECTIVE.

This figure prevents “bee = timer, bird = decision” from becoming a taxonomic
claim. Clock architecture is an evidence classification, not a species label.

## Figure 3 —## Figure 3 — Pairwise controller phase diagram

A compact theoretical comparison can show stationary mismatch

\[
\Delta^*
=
w\,
\frac{\lambda_1-\lambda_2}
{(1-\lambda_1)(1-\lambda_2)}
\]

over \((\lambda_1,\lambda_2)\) inside the stable square
\((-1,1)^2\).

Key visual:
- diagonal \(\lambda_1=\lambda_2\): zero mismatch under shared forcing;
- divergence away from diagonal;
- amplification near weak-restoring boundaries \(\lambda_i\to1\).

This figure makes the general ecological prediction independent of any one
taxon.
