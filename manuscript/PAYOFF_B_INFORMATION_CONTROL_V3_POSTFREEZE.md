# Seasonal clock architecture can convert shared environmental change into phenological mismatch

**PAYOFF-B Paper 2 — V3 post-freeze development draft**  
**Date:** 2026-10-03  
**Status:** post-freeze integration draft; the frozen GEB V2 manuscript and its registered empirical outcomes are unchanged.

## Abstract

**Aim:** Interacting species can experience the same seasonal environmental
change yet become phenologically asynchronous. We ask whether that divergence
can arise from differences in **seasonal clock architecture** rather than from
different external forcing alone.

**Location:** General theory, with empirical modules from migratory birds and
ungulates in North America and Europe.

**Time period:** Dataset-specific; principal reconstructed phenology records
span approximately 1980–2020.

**Major taxa studied:** Migratory birds and mule deer, with plant–pollinator
and resident–migrant interaction studies as independent benchmarks.

**Methods:** We separate a developmental/physiological readiness clock
\(G\) from an information-dependent decision controller with phase-information
weight \(K\) and correction gain \(g\). We combine this two-clock model with
stagewise value-of-information theory, pairwise and network phase-control
models, finite coordination games, preregistered macroecological analyses and
source-backed natural systems.

**Results:** Effective mean phase retention is
\(\lambda_i=\phi_i(1-G_i g_iK_i)\). For two initially synchronized actors
sharing seasonal error \(m_t\), controller asymmetry generates
\(\Delta_{t+1}=(\lambda_1-\lambda_2)m_t\); across an interaction network,
one-step mismatch scales with the graph Dirichlet energy of the controller
field. Information can simultaneously become more accurate and less actionable,
so optimal information use can precede maximal cue accuracy. A post-freeze
reanalysis of 152 mule-deer animal-years shows a start-to-end phase-variance
ratio of 0.249 (95% animal-cluster bootstrap 0.167–0.362) together with signed
speed and stopover compensation, but does not identify the latent two-clock
parameters.

**Main conclusions:** Shared climate forcing need not produce shared timing.
Species can diverge because they differ in when actions become physiologically
available, what they can infer about seasonal phase and how strongly they can
correct error. Mean and variance trajectories can identify information weight
and effective correction, but readiness and decision gain require independent
measurement or manipulation.

**Keywords:** phenological mismatch; biological clocks; migration; information
ecology; feedback control; recourse; climate change

---

## 1. Introduction

Phenological mismatch is usually described as a difference between the timing
of consumers and resources, plants and pollinators, or migrants and seasonal
conditions. The same observed mismatch, however, can arise from distinct
mechanisms: poor prediction of a future state, physiological commitment before
that state is known, limited ability to repair an earlier timing error, or
interaction costs that discourage unilateral adjustment.

Long-distance migration makes these mechanisms visible. A migrant may leave a
wintering site before directly observing destination spring, yet departure is
not the only decision. Speed, stopover duration, route and post-arrival timing
can be altered while new information is acquired. Seasonal migration is
therefore naturally represented as repeated inference and correction rather
than a single departure-date response.

We distinguish two timing layers. A developmental or physiological timer
determines when actions become available; an information-dependent controller
then estimates signed seasonal phase and chooses among those available actions.
This distinction matters because information and actionability can change in
opposite directions. Conditions nearer the destination may improve prediction
while the remaining opportunities to change timing disappear.

The intuition is simple: an organism may know the future best only after it has
become too late to act on that knowledge. In the motivating analogy, a migrant
is a train travelling toward a seasonal timetable that is not yet fully known—
a “Shinkansen to Schrödinger's spring.” The formal model is sequential
inference and feedback control, not a railway analogy.

We first derive when improving information should be used while actionability
declines. We then model readiness, signed phase estimation and repeated
correction, and show exactly how differences between actor-level controllers
convert a shared seasonal error into interaction mismatch. Finally, we retain
the coordination-game result showing why mismatch can persist even after
environmental information improves.

Natural evidence is deliberately layered. Existing data support predictive
connectivity, route-stage updating, bidirectional compensation and
interaction-level response asymmetry, but no current system jointly identifies
all latent readiness, information and control parameters. Our central claim is:

> **Shared environmental change can generate phenological mismatch because
> interacting organisms differ in when they become able to act, what they can
> infer about seasonal phase and how strongly they can correct error.**

## 2. Theory

### 2.1 Information becomes more accurate while actionability can decline

Let the future seasonal state be early or normal. Above the canonical Paper-2 actionability boundary, let the gross value of a cue with reliability (q) be

\[
V_A(q)=Sq-B,
\]

where (S) is the total state-dependent loss scale and (B) is the larger prior action loss.

Let \(r(t)\in[0,1]\) represent retained actionability: the fraction of the full state-contingent response that remains usable at time or route stage (t). Let (C(t)) be cumulative direct cost of waiting. The reduced net value of using information at time (t) is

\[
N(t)=r(t)[Sq(t)-B]-C(t).
\]

For differentiable trajectories, an interior optimum satisfies

\[
rSq'=-r'[Sq-B]+C'.
\]

The left side is the marginal benefit of improving environmental information. The first term on the right is the loss of value as response options disappear; the second is the direct marginal cost of waiting.

When direct marginal waiting cost is zero,

\[
\frac{Sq'}{Sq-B}=-\frac{r'}{r}.
\]

Thus the optimum occurs when the relative gain in information value is exactly balanced by the relative loss of remaining actionability.

For exponential learning and exponential actionability loss,

\[
q(t)=q_0+\Delta q[1-\exp(-\alpha t)]
\]

and

\[
r(t)=\exp(-\beta t),
\]

the unique zero-cost optimum is

\[
t^*=\frac{\log(1+\alpha/\beta)}{\alpha}.
\]

The optimum moves earlier as (\beta) increases. Two actors observing the same environmental-information trajectory can therefore commit at different stages solely because their remaining response options disappear at different rates.

A particularly important consequence is that perfect information can be too late. With \(\alpha=\beta=1\), the optimum is \(t^*=\log 2\), where cue accuracy is only \(q=0.75\) in the symmetric witness even though \(q\to1\) later. Better information is not automatically more useful.

### 2.2 Route-wise phase state

The actionability model determines when information is worth using. It does not by itself describe what happens to the animal's timing error after the organism acts.

We therefore define signed phase error

\[
e_t>0
\]

for an actor that is late relative to the locally relevant seasonal optimum, and

\[
e_t<0
\]

for an actor that is early.

At route stage (t), the actor forms an estimate

\[
\hat e_t=E[e_t\mid I_t],
\]

where (I_t) is the information accumulated by that stage.

A signed correction (u_t) represents the combined timing effect of available actuators:

- (u_t>0): speed up, shorten stopover, skip delay or otherwise advance progress;
- (u_t<0): slow down, lengthen stopover, wait or otherwise delay progress.

The realized phase state then evolves as

\[
\boxed{
e_{t+1}=\phi_t(e_t-u_t)+w_t
}
\]

where \(\phi_t\) is passive phase retention in the absence of active correction and \(w_t\) is change in the local seasonal target between checkpoints.

This matters because even a perfect correction at one checkpoint need not eliminate later mismatch. The resource wave itself can move.

### 2.3 The animal's internal phase estimate

For a transparent stochastic representation, suppose

\[
e_t\sim N(m_t,P_t)
\]

and an intermediate environmental cue obeys

\[
z_t=e_t+\nu_t,\\qquad \nu_t\sim N(0,R_t).
\]

The posterior phase estimate is

\[
K_t=\frac{P_t}{P_t+R_t},
\]

\[
m_t^+=m_t+K_t(z_t-m_t),
\]

\[
P_t^+=(1-K_t)P_t.
\]

The ecological interpretation is simple. An animal need not know its true phase error. It need only behave as if it repeatedly updates an estimate of whether it is too early or too late.

This filtering result is established control theory, not a claim of mathematical novelty.

### 2.4 Signed correction follows estimated phase error

Let correction cost be quadratic and residual phase mismatch costly:

\[
L(u)=\kappa u^2+\mu(e-u)^2.
\]

Conditional on the posterior phase belief,

\[
E[L(u)\mid I_t]
=
\kappa u^2
+
\mu[(m_t^+-u)^2+P_t^+].
\]

Without actuator bounds, the optimal one-step correction is

\[
u_t^*
=
g^*m_t^+,
\]

where

\[
g^*=\frac{\mu}{\kappa+\mu}.
\]

Thus the sign of correction follows the sign of the estimated phase error. Late actors advance; early actors delay. Stronger residual mismatch costs increase the correction gain, whereas more expensive movement or stopover adjustment reduces it.

Finite speed, stopover or route flexibility clips this correction to the feasible interval. The organism can therefore remain mismatched even when it knows the direction of the required correction.

### 2.5 Phase retention decomposes into passive carry-over and active feedback

Under perfect estimation, proportional feedback

\[
u_t=g_te_t,
\]

no actuator clipping and no target shift,

\[
e_{t+1}
=
\phi_t(1-g_t)e_t.
\]

Therefore

\[
\boxed{
\lambda_t=\phi_t(1-g_t).
}
\]

This gives an exact decomposition of segment-scale phase retention.

If \(g_t=0\), the observed phase coefficient is passive carry-over \(\lambda_t=\phi_t\).

If (0<g_t<1), active correction reduces retained phase error.

If (g_t=1), the current phase error is reset at that checkpoint when the target does not move.

If \(g_t>1\), the controller overshoots and \(\lambda_t\) can become negative.

The existing PAYOFF-B closed-loop model

\[
e_{t+1}=(1-K)e_t+r
\]

is recovered exactly by setting \(\phi_t=1\), \(g_t=K\), \(\hat e_t=e_t\) and \(w_t=r\). The route-wise model is therefore an extension of the existing phase controller rather than a separate theory.

The decomposition also establishes an important identification boundary: neither \(1-|\lambda|\) nor \(\lambda\) itself is a direct estimate of recourse, actionability or control gain without an independent estimate of passive retention and an explicit actuator model.

### 2.6 Two timing layers and repeated infer–correct–propagate control

Seasonal timing can be generated by two mechanistically different layers.

A **developmental/physiological timer** carries an internal readiness state
\(z_t\). In a minimal representation,

\[
\dot z=v(E_t,z),
\qquad
G_t=G(z_t)\in[0,1],
\]

where \(G_t\) is a readiness or actuator-availability gate. Threshold events
such as emergence can be represented by \(G_t\) switching when
\(z_t\) reaches a developmental threshold. This is a rate-to-threshold
mechanism and does not require the organism to estimate signed ecological
mismatch.

An **inferential decision controller** uses information to estimate signed
phase error and select a correction:

\[
\hat e_t=E[e_t\mid I_t],
\qquad
u_t=\pi_t(\hat e_t,A_t).
\]

The feasible action set \(A_t\) is constrained by readiness. Thus the full
hybrid architecture is

\[
\boxed{
z_t
\rightarrow
G_t
\rightarrow
A_t
\rightarrow
(\hat e_t,u_t)
\rightarrow
e_{t+1}.
}
\]

Migratory birds can contain both layers: endogenous or photoperiodic programmes
contribute to migratory readiness, while speed, stopover and route decisions
provide repeated feedback after movement begins. The informal “Mikawa-Anjo
clock” refers specifically to the second, decision-controller layer.

The route-wise ecological sequence is therefore

\[
\boxed{
\text{become ready}
\rightarrow
\text{move}
\rightarrow
\text{observe}
\rightarrow
\text{update phase belief}
\rightarrow
\text{correct}
\rightarrow
\text{move again}.
}
\]

Departure error can be large while arrival error is small, and early departure
need not produce early arrival if later stopovers absorb the advance. This
separates **timer plasticity** from **feedback recourse** as distinct components
of seasonal tracking.

### 2.7 Controller asymmetry converts shared seasonal error into interaction mismatch

For actor \(i\), the two-clock representation gives effective regression-scale
mean phase retention

\[
\lambda_i
=
\phi_i(1-G_i g_iK_i),
\]

where \(G_i\in[0,1]\) is the readiness/availability gate generated by the
developmental or physiological clock. The previous decision-only controller is
the special case \(G_i=1\).

Let

\[
m_t=\frac{e_{1,t}+e_{2,t}}{2}
\]

be the common seasonal-error mode and

\[
\Delta_t=e_{1,t}-e_{2,t}
\]

the interaction mismatch. With
\(\bar\lambda=(\lambda_1+\lambda_2)/2\) and
\(\delta\lambda=\lambda_1-\lambda_2\),

\[
m_{t+1}
=
\bar\lambda m_t
+
\frac{\delta\lambda}{4}\Delta_t
+
\bar w_t,
\]

whereas

\[
\boxed{
\Delta_{t+1}
=
\delta\lambda\,m_t
+
\bar\lambda\Delta_t
+
\delta w_t.
}
\]

If the two actors are currently synchronized
\(\Delta_t=0\) and experience the same environmental innovation
\(\delta w_t=0\), then

\[
\boxed{
\Delta_{t+1}
=
(\lambda_1-\lambda_2)m_t.
}
\]

A shared seasonal error is therefore converted into mismatch whenever the two
clock architectures retain or correct that error differently. No difference in
external climate exposure and no initial interaction mismatch are required.

With equal readiness, passive retention and feedback gain, information
asymmetry alone gives

\[
\Delta_{t+1}
=
-\phi Gg(K_1-K_2)m_t.
\]

With equal information and feedback gain, readiness-clock asymmetry alone gives

\[
\Delta_{t+1}
=
-\phi gK(G_1-G_2)m_t.
\]

With equal readiness and information weight, control-gain asymmetry alone gives

\[
\Delta_{t+1}
=
-\phi GK(g_1-g_2)m_t.
\]

Under constant shared forcing \(w\) and stable controllers
\(|\lambda_i|<1\), persistent mismatch is

\[
\boxed{
\Delta^*
=
w\,
\frac{\lambda_1-\lambda_2}
{(1-\lambda_1)(1-\lambda_2)}.
}
\]

For a weighted interaction network with actor retentions
\(\boldsymbol\lambda\), graph Laplacian \(L\), total edge weight \(W\), and
shared incoming error \(m_t\), mean squared edge mismatch is

\[
\boxed{
\mathcal M_{t+1}
=
m_t^2
\frac{
\boldsymbol\lambda^\top L\boldsymbol\lambda
}{W}.
}
\]

Thus community mismatch depends on where clock/controller differences sit in
the interaction network, not only on their marginal variance. Binary
controller states reduce exactly to the earlier network-cut geometry.

This closes the mechanistic bridge from physiological readiness and
information-dependent control to pairwise and community phenological mismatch.

### 2.8 Information recovery can still fail to restore coordination

The route-wise controller describes within-actor correction. The earlier coordination game remains relevant after actors interact.

At perfect information, an obsolete timing convention and an informed convention can both be strict equilibria when the temporary interaction cost of moving first exceeds the individual gain from unilateral information use. Therefore two distinct barriers can prevent recovery.

First, **physical or developmental irreversibility**: accurate information arrives after useful actions have disappeared.

Second, **strategic irreversibility**: actions remain physically possible, but unilateral change is selected against because partners remain in the previous convention.

The first route is a control constraint. The second is a coordination constraint. They should not be conflated.

---

## 3. Natural evidence

### 3.1 Predictive information is associated with realized mismatch

The preregistered broad-bird analysis retains 3,311 observations from 37 migratory bird species after requiring an eight-year trailing information window. Predictive connectivity is the signed correlation between detrended source- and destination-site green-up anomalies before the focal outcome.

The pooled registered GAM gives

\[
\hat\beta_\rho=-0.0462,
\]

with 95% CI ([-0.0870,-0.0054]) and (p=0.0265). Stronger pre-existing predictive connectivity is therefore associated with smaller arrival–green-up mismatch in the declared pooled analysis.

The sign remains negative in all leave-one-species-out and leave-one-year-out fits, but dependence-aware intervals cross zero. The licensed conclusion is a pooled directional macroecological signal, not a universal species-level coefficient.

### 3.2 Long-distance migrants show weaker temperature responsiveness

A separate reconstruction of the Usui et al. source table retains 944 temperature-response effects from 28 studies and 279 species after restricting migration distance to short and long classes.

The adjusted long-minus-short contrast is

\[
+0.421\,\mathrm{d}/{}^\circ\mathrm{C}
\]

with 95% CI (+0.121) to (+0.722) and (p=0.0077). Because negative slopes denote earlier timing in warmer years, long-distance migrants are less temperature-responsive than short-distance migrants in this reconstruction.

This pattern is not uniquely diagnostic of information distance; endogenous timing and photoperiodic control remain alternative explanations.

### 3.3 Mule deer show a continuous phase funnel with signed route compensation

Ortega et al. (2023) already established that Red Desert mule deer can begin
migration far ahead of or behind peak green-up and resynchronize en route by
changing movement speed and stopover use. PAYOFF-B does not claim that
phenomenon as new.

A post-freeze descriptive reanalysis of the public Source Data file uses all
152 animal-years from 72 adult females. Signed Days-From-Peak phase had an
across-animal-year standard deviation of 26.41 d at migration start and 13.17 d
at migration end. The end/start variance ratio was

\[
0.249,
\]

with a 95% animal-cluster bootstrap interval of 0.167–0.362. After removing
year-specific start and end means, the variance ratio remained

\[
0.294
\quad
(95\%\ \mathrm{CI}: 0.206\text{--}0.405).
\]

The whole-route continuous phase-retention slope was

\[
\lambda=0.107
\quad
(95\%\ \mathrm{cluster\ bootstrap}: 0.013\text{--}0.209),
\]

and 107 of 152 animal-years (70.4%) ended closer to peak green-up than they
started. Mean absolute phase error declined from 21.91 d to 11.12 d.

The same individual-level source table gives the expected signed actuator
directions. Each additional day of positive start-phase error was associated
descriptively with \(+0.0683\) km d\(^{-1}\) higher movement rate
(95% animal-cluster bootstrap 0.0554–0.0800) and \(-0.492\) d of stopover use
(95% interval \(-0.569\) to \(-0.412\)). After year centering, the corresponding
slopes remained \(+0.0852\) and \(-0.614\), with both bootstrap intervals
excluding zero.

These results quantify the published convergence in continuous animal-year
data and reproduce the signed actuator geometry required by the route-wise
model. They do **not** identify the internal phase estimate, passive retention,
information weight or feedback gain. Measurement error, passive dynamics,
selection and changing environmental variance remain alternative contributors
to the observed variance funnel.

### 3.4 Bar-tailed godwits absorb early departure later in the route

In bar-tailed godwits migrating from New Zealand through the Yellow Sea to Alaska, departure advanced by about six days over 2008–2020, but Alaska arrival and breeding did not advance correspondingly. Longer later stopovers absorbed the earlier departure.

This supplies the opposite sign of recourse: being early can be corrected by delaying progress later in the route.

Together with mule deer, the two examples show why departure timing alone is not a sufficient measure of downstream seasonal phase.

### 3.5 Pink-footed geese update environmental information en route

In pink-footed geese, the importance of day length, local accumulated temperature and other environmental information changes among successive migration stages. Local accumulated temperature at stopovers informs northward progression.

This is consistent with the route-wise premise that migration itself can expose animals to information unavailable at the origin.

### 3.6 Compensation can restore timing without restoring fitness

American redstarts departing roughly 10 days late migrated about 43% faster, yet the compensatory pattern was associated with a reported 6.3% decrease in annual survival.

Thus temporal recovery and fitness recovery are not equivalent:

\[
\text{phase recovery}
\neq
\text{zero biological cost}.
\]

This supports the effective-deadline concept: a correction can remove downstream timing error while still carrying a cost.

### 3.7 Interaction-level asymmetry changes relative timing

Across 10 European nest-box schemes, resident tits were more temperature-sensitive than migratory flycatchers, and this differential response widened their laying-date interval by 0.94 days per decade. Published UK bird–caterpillar analyses likewise show incomplete temporal tracking by consumers.

These systems support the ecological step from heterogeneous response rules to changing interaction timing. They do not directly estimate the route-wise phase controller.

### 3.8 Negative evidence defines the boundary

The registered Eurasian wigeon test did not support the predicted negative interaction between incoming phase error and predictive connectivity. Predictive connectivity should therefore not be treated as a universal amplifier of post-error correction.

Two preregistered long-term environmental reversal gates also failed before any natural hysteresis analysis was opened. PAYOFF-B consequently does not claim a natural degradation–recovery hysteresis sequence.

These negative results sharpen the distinction between information available before commitment, information acquired during movement, and control after an error has already appeared.

---

## 3.9 Relation to migration-control prior art

Stagewise migration decisions, dynamic programming, stopover optimization and
en-route timing adjustment are established ideas. Taylor (2016) explicitly
linked phenological change to en-route migration-speed adjustment and stopover
frequency, and Chu et al. (2026) formulated migration as a stochastic optimal
switching problem with destination information under both perfect and partial
information. PAYOFF-B therefore does not claim novelty for sequential migration
control, stopover updating, destination information or generic partial-
information optimal control.

The candidate contribution is narrower: an exact ecological
information-actionability balance, its actor-specific desynchronization
consequence, a signed phase-retention bridge to route correction, and the
connection from within-actor control to between-actor seasonal coordination.
The route-wise controller is used to make those predictions operational rather
than to claim a new control-theory class.

---

## 4. Discussion

### 4.1 Seasonal tracking is a control problem, not only a response-rate problem

The main conceptual change is to replace a one-dimensional language of “fast” and “slow” phenological response with a sequence of inference and correction.

Two organisms can have the same observed arrival shift for very different reasons. One may predict the future accurately and require little correction. Another may depart with large timing error but repeatedly compensate en route. A third may receive accurate information only after useful correction has become impossible.

These cases are not equivalent biologically, even if their final timing is similar.

### 4.2 Arrival convergence can hide substantial control

If repeated positive feedback gains reduce phase error, large departure-date variation can converge toward a narrow arrival window. Observing only arrival dates can therefore underestimate the amount of behavioral control used along the route.

The strongest direct empirical design is consequently transition-based:

\[
e_{\mathrm{in}}
\rightarrow
\text{actuator response}
\rightarrow
e_{\mathrm{out}}.
\]

A route-wise analysis should estimate signed incoming error, the information available at the checkpoint, the subsequent speed/stopover/route response and the outgoing error at the next checkpoint.

### 4.3 The two clocks make different empirical predictions

The term “biological clock” should not collapse developmental timing and
state-dependent decisions into one mechanism. Emergence, diapause termination
and similar events are usefully treated as developmental/physiological timers:
temperature, photoperiod, endocrine state and sometimes circadian molecular
pathways can alter readiness, but PAYOFF-B does not assume one universal
molecular oscillator for bee emergence.

The decision-controller layer has a different signature. It predicts that
signed incoming phase changes the direction of subsequent behavior: late
individuals advance, early individuals delay, and repeated correction can
produce a phase-variance funnel. A developmental timer can instead shift event
timing without such signed post-event feedback.

Migrants can use both. Endogenous timing can open a broad migration window,
after which checkpoint information, energetic state and weather influence
departure and pacing decisions. The empirical task is therefore to ask
separately **when an organism becomes able to act** and **how it chooses once
action is possible**.
### 4.4 A variance funnel distinguishes individualized feedback from a common schedule

Mean timing alone cannot distinguish a common timing programme from
individualized correction. If every individual receives the same open-loop
timing shift, that common shift changes the mean but does not selectively
reduce between-individual phase variance.

Under the two-clock Gaussian controller, let

\[
h_t=G_tg_t
\]

be **effective correction gain**: physiological/readiness availability
\(G_t\) multiplied by decision gain \(g_t\). Incoming phase variance \(P_t\),
checkpoint observation variance \(R_t\), posterior weight
\(K_t=P_t/(P_t+R_t)\), passive retention \(\phi_t\), and new process variance
\(Q_t\) then give

\[
P_{t+1}
=
\phi_t^2P_t[1-K_th_t(2-h_t)]+Q_t.
\]

The corresponding common open-loop correction gives

\[
P_{t+1}^{\mathrm{open}}
=
\phi_t^2P_t+Q_t.
\]

Thus, for informative cues and \(0<g_t<2\), individualized phase feedback
predicts additional downstream variance contraction. This creates a functional
signature of the proposed internal phase estimate: early and late individuals
are not merely shifted by the same calendar rule but are pulled toward the
seasonal target according to their own estimated error.

The prediction does not make synchronization itself novel. Mule deer already
provide a striking natural example of wide departure mismatch followed by
narrower arrival timing. The prospective test is stricter: compare a common
schedule model and an individualized feedback model on held-out downstream
phase, using checkpoint information and actuator responses measured
independently.


The mean and variance signatures can also be combined. With noisy checkpoint
information and two clock layers, observed regression-scale phase retention is

\[
\lambda_t=\phi_t(1-h_tK_t),
\qquad
h_t=G_tg_t.
\]

Define

\[
d_t=1-\frac{\lambda_t}{\phi_t}
\]

and

\[
v_t=
\frac{P_{t+1}-Q_t}{\phi_t^2P_t}.
\]

Then the declared Gaussian controller gives

\[
K_t=
\frac{d_t^2}{v_t-1+2d_t},
\qquad
h_t=\frac{d_t}{K_t}.
\]

Thus, if passive retention \(\phi_t\) and process innovation \(Q_t\) are
identified independently, mean retention plus the variance funnel separates
an effective checkpoint-information weight \(K_t\) from **effective
correction** \(h_t=G_tg_t\). It does **not** separate physiological readiness
\(G_t\) from decision gain \(g_t\) unless one of those layers is independently
measured or manipulated. This is a prospective functional inverse, not
evidence that animals explicitly compute Bayesian weights.

### 4.5 The most informative checkpoint need not be the most important checkpoint

The actionability theorem predicts an intermediate-stage peak in behavioral cue responsiveness. Early in the route, the signal can be too poor to guide correction. Late in the route, the signal can be excellent but response options can be exhausted.

The ecologically important checkpoint is therefore where information gain and remaining correction capacity jointly make information most valuable.

This prediction differs from a simple “closer cues are better” model.

### 4.6 Phase retention is a useful coordinate but not a mechanism by itself

The empirical phase-retention coefficient \(\lambda\) is valuable because it
quantifies how strongly incoming seasonal error persists to a later stage.
Under perfect phase information and full readiness \(G=1\),

\[
\lambda=\phi(1-g).
\]

With partial readiness and noisy individualized phase estimation,

\[
\lambda=\phi(1-GgK)
=
\phi(1-hK).
\]

Thus the same \(\lambda\) can arise from different combinations of passive
persistence, information quality and active feedback. Negative retention can
arise from overshoot, anticipation, target movement or coordinate changes.
Direct mechanistic inference therefore requires actuator and environmental
information in addition to \(\lambda\).

### 4.7 Prediction and reactive correction can be substitute control channels

The controller also changes how cross-route comparisons should be interpreted.
Conditional on the relevant actuator being available, let (R(q)) be mismatch
risk remaining after the actor has used available pre-commitment information,
and let downstream reactive gain (g) reduce that error at quadratic cost
(c g^2/2):

\[
L(g;q)=(1-g)^2R(q)+\frac{c}{2}g^2.
\]

The unique optimum is

\[
g^*(q)=\frac{2R(q)}{c+2R(q)},
\qquad
\lambda^*(q)=\frac{c}{c+2R(q)}.
\]

If better prediction lowers the mismatch reaching the feedback stage while
correction cost is fixed, optimal downstream correction becomes weaker. Strong
pre-commitment prediction and strong post-error correction are therefore
substitutes in this reduced model, not necessarily positively correlated
traits.

More generally, if cue quality also changes the effective cost of correction,
the sign is determined by

\[
\frac{d}{dq}\log\frac{g^*}{1-g^*}
=
\frac{R'}{R}-\frac{c'}{c}.
\]

Prediction dominates when mismatch risk falls proportionally faster than
correction cost; cue-informed correction dominates when correction becomes
cheap or targeted faster than pre-correction risk falls.

This result was derived after the barnacle-goose descriptive screen and the
registered wigeon null were known. Those outcomes are therefore motivation,
not confirmation. The ecological consequence is nevertheless important:
**prediction before error and correction after error are separate control
channels and should be estimated separately.**

### 4.8 Climate change can damage both prediction and control

Climate change can affect the framework through at least two distinct routes.

It can reduce predictive connectivity between distant locations, degrading the quality of information available before a migrant reaches its destination.

It can also change the window over which correction remains possible—for example by compressing resource peaks, changing stopover conditions or altering the cost of speed and delay.

A species can therefore become more mismatched without losing its intrinsic ability to move or shift phenology. The problem can instead be that the forecast becomes reliable too late relative to the remaining control window.

### 4.9 Interactions convert controller differences into ecological mismatch

The pairwise mode decomposition clarifies why interaction mismatch need not
require different climate exposure. A common environmental displacement enters
both actors as a shared phase error, but differences in effective retention
\(\lambda_i=\phi_i(1-G_i g_iK_i)\) convert part of that common mode into a
differential mode.

This distinction changes comparative interpretation. A resident and a migrant,
or a plant and a pollinator, can experience the same regional warming yet
diverge because one has more informative cues, more remaining recourse or a
different feedback gain. The relevant comparative quantity is therefore not
taxonomic identity itself but the difference in the controllers through which
environmental information becomes timing correction.

Physical correction and strategic coordination should then be separated. The
controller theorem explains how mismatch is generated. The Paper-2 game theory
explains why a mismatched or obsolete timing configuration can remain difficult
to escape even after information improves. A physically feasible correction
can therefore remain strategically inaccessible.

### 4.10 Direct natural validation remains prospective

The current evidence supports complementary pieces of the mechanism across
different systems, but no natural PAYOFF-B dataset jointly identifies

\[
G,\quad K,\quad g,\quad \phi,\quad Q
\]

for the same focal transition.

Developmental and emergence systems provide strong prior support for
physiological/readiness timing. Mule deer provide unusually strong
individual-level evidence for signed downstream correction and a phase-variance
funnel. Migratory birds are the most natural hybrid target because endogenous
readiness and repeated route decisions can coexist within one individual.

The full prospective sequence is therefore

\[
\text{physiological readiness }G
\rightarrow
\text{checkpoint information }K
\rightarrow
\text{decision gain }g
\rightarrow
\text{signed correction}
\rightarrow
\text{downstream phase}.
\]

Mean and variance phase trajectories can identify \(K\) and effective
correction \(h=Gg\) under the declared Gaussian controller when \(\phi\) and
\(Q\) are independently known. They cannot separate \(G\) from \(g\) without
an additional physiological measure, readiness manipulation or independent
decision-gain calibration.

The strongest future test should therefore combine a readiness measurement with
checkpoint environmental information and movement decisions, and compare a
shared timing-programme model against a two-clock feedback model on held-out
downstream phase.

---

## 5. Conclusion

Seasonal migration should not be treated as a single departure date that determines a later arrival date.

Animals can move while learning. They can arrive at successive route stages with positive or negative seasonal phase error, update their estimate of the changing environment, and use speed, stopover duration, route and subsequent timing to reduce that error.

The resulting ecological problem has three coupled components:

\[
\boxed{
\text{infer the seasonal target}
\rightarrow
\text{correct current phase}
\rightarrow
\text{retain enough options to correct again}.
}
\]

Information generally becomes more accurate as the organism approaches the relevant future environment, but correction opportunities can disappear at the same time. The optimal information-use stage can therefore precede the stage of maximal cue accuracy.

For interacting species, differences in information, correction cost and remaining actionability create different phase trajectories even under the same external climate forcing. Seasonal mismatch can thus arise without a simple failure of adaptive capacity.

The strongest current interpretation is:

> **Climate adaptation can fail because organisms must control their seasonal phase toward a future target that becomes easier to infer only as the opportunities to correct toward it are disappearing.**

And the clearest prospective natural test is:

> **Do animals repeatedly re-estimate whether they are early or late at route checkpoints, and do those estimates predict the direction and magnitude of the correction made before the next checkpoint?**

---

## Post-freeze transparency statement

The stagewise recourse, continuous information-actionability balance and route-wise Bayesian phase-control extensions were formalized after the registered empirical gates and frozen GEB V2 package. They do not alter, reopen or retune any preregistered empirical outcome. The frozen V2 manuscript remains the audit and rollback source. This V3 document is a prospective integration draft for a later Paper-2 revision.
