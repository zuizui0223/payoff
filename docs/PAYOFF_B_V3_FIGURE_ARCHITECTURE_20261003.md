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

### Panel B — Entry timer and decision controller hand off control

**B1. Entry/readiness timer**

\[
\dot z=v(E_t,z),
\qquad
\tau=\inf\{t:z(t)\ge\Theta\}.
\]

The physiological/developmental timer determines **when the trajectory starts**
and therefore the entry phase \(e_0\).  Across partners it can create
\(\Delta_0\).

**B2. Post-entry decision controller**

After entry,

\[
e_k
\rightarrow
I_k
\rightarrow
\hat e_k
\rightarrow
u_k
\rightarrow
e_{k+1}.
\]

Use early/late arrows:
- late -> speed up / shorter stopover;
- early -> slow down / longer stopover.

Label the hand-off:

> **entry timer sets the initial error; decision controller sets its retention.**

Add a **dashed carry-over arrow** from physiological state \(s_0\) across the
handoff into later phase:

\[
s_{k+1}=\rho s_k,
\qquad
e_{k+1}=\lambda e_k+\beta s_k+w_k.
\]

The dashed arrow means that mechanism control has shifted but physiological
state can persist. It is explicitly post-hoc and should not be drawn as a
confirmed mule-deer pathway.

A concurrent readiness gate is an optional extension, not the default
post-entry assumption.

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

### Panel D — Exact timer–controller mismatch decomposition

For two actors after \(n\) checkpoints show

\[
\boxed{
\Delta_n
=
(\lambda_1^n-\lambda_2^n)m_0
+
\frac{\lambda_1^n+\lambda_2^n}{2}\Delta_0.
}
\]

Color the two terms separately:

- **controller-generated mismatch**:
  \((\lambda_1^n-\lambda_2^n)m_0\);
- **timer-propagated mismatch**:
  \(\frac{\lambda_1^n+\lambda_2^n}{2}\Delta_0\).

Add the precision corollary:

\[
V_n=\lambda^{2n}V_0.
\]

Visual message:

> A noisy entry timer can be rescued by strong downstream feedback, whereas
> weak feedback makes precise initial timing much more valuable.

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

The formal reading order is:

\[
(z,\tau)
\rightarrow
(e_0,\Delta_0)
\rightarrow
(\hat e,u,\lambda)
\rightarrow
\Delta_n.
\]

“Schrödinger's spring” and “Shinkansen” belong in the caption / talk version,
not as formal variable names.

## Figure 2 — Empirical evidence hierarchy

Keep empirical modules visually separated by inferential status:

- preregistered broad-bird predictive-connectivity result;
- reconstructed migration-distance response contrast;
- Ortega continuous source-data phase funnel plus the same-population timer–controller channel-dissociation anchor;
- wigeon preregistered null;
- negative natural reversal gates.

Use explicit labels such as PREREGISTERED, SOURCE-DATA REANALYSIS,
PUBLISHED ANCHOR, POST-HOC THEORY, and PROSPECTIVE.

This prevents the new theoretical synthesis from making old data look
prospectively selected.

## Supporting-theory placement

Clock-portfolio optimization, opportunity-loss fragility and cryptic portfolio
divergence are no longer main-figure material for V3. They remain prospective
supporting/future theory until a natural design independently identifies the
required precision-allocation and opportunity-loss quantities.
