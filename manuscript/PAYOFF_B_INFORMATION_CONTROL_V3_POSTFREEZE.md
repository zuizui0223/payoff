# Seasonal tracking is a sequential information-and-control problem

**PAYOFF-B Paper 2 — V3 post-freeze development draft**  
**Date:** 2026-10-03  
**Status:** post-freeze integration draft; the frozen GEB V2 manuscript and its registered empirical outcomes are unchanged.

## Abstract

**Aim:** We ask when seasonal information becomes useful, how timing error can be corrected after movement begins, and why interacting species can still desynchronize despite substantial adaptive capacity.

**Location:** General theory, with empirical modules from migratory birds and ungulates in North America and Europe.

**Time period:** Dataset-specific; principal reconstructed phenology records span approximately 1980–2020.

**Major taxa studied:** Migratory birds and mule deer, with plant–pollinator and resident–migrant interaction studies as independent benchmarks.

**Methods:** We combine Bayesian decision models, stagewise value-of-information theory, a route-wise signed phase controller, finite coordination games, preregistered macroecological analyses and source-backed natural systems.

**Results:** Information quality can improve while useful response options disappear. In the reduced model, usable information value is \(r(t)[Sq(t)-B]-C(t)\); with exponential learning and recourse loss the unique zero-cost optimum is \(t^*=\log(1+\alpha/\beta)/\alpha\), generally before maximal cue accuracy. Route-wise phase dynamics obey \(e_{t+1}=\phi_t(e_t-u_t)+w_t\). A post-freeze source-data reanalysis of 152 mule-deer animal-years shows that end-of-migration phase variance was 0.249 of start variance (95% animal-cluster bootstrap 0.167–0.362; 0.294 after year centering), while movement speed increased and stopover use decreased continuously with later starting phase. These observations quantify a natural phase funnel with signed compensation but do not identify the latent controller.

**Main conclusions:** Seasonal tracking combines physiological readiness timers with information-dependent decision control. Controller asymmetry can convert a shared seasonal error directly into interaction mismatch: organisms exposed to the same forcing can diverge because they differ in readiness, information, remaining actionability or phase correction. Restored information need not restore coordination after response options or coordinated conventions have been lost.

**Keywords:** phenological mismatch; migration; information ecology; feedback control; recourse; phase error; climate change

---

## 1. Introduction

Phenological mismatch is commonly summarized as a difference between the timing of consumers and resources, plants and pollinators, or migrants and the seasonal conditions they exploit. That description is useful but mechanistically incomplete. The same observed mismatch can arise because an organism cannot respond far enough, because it cannot predict the relevant future state, because useful information arrives only after important actions have been committed, because an earlier timing error can no longer be repaired, or because unilateral adjustment creates a temporary mismatch with interaction partners.

Long-distance migration makes these distinctions unusually visible. A migrant may have to leave a wintering site before it can directly observe spring conditions at the destination. Yet departure is not the only decision. Individuals can change travel speed, alter stopover duration, skip sites, choose routes and alter post-arrival timing. Migration is therefore neither a single irreversible departure decision nor a purely open-loop response to a distant cue. It can be a sequence of decisions in which new environmental information is acquired while the animal is already moving.

This suggests a control problem. Let (e_t) denote the signed difference between an animal's current seasonal phase and the locally relevant seasonal optimum at route stage (t). The animal does not necessarily know (e_t) exactly. Instead, it forms an internal estimate from the information available by that stage. It then chooses a correction through the actuators that remain available. The residual error is carried into the next stage, where it can be re-estimated and corrected again.

The central difficulty is that information and control change in opposite directions. Later in a journey, conditions nearer the destination may provide better information about the coming spring. At the same time, fewer opportunities remain to change speed, stopover allocation, route or breeding timing. Waiting can therefore increase cue accuracy while reducing the value of that accuracy.

The intuition can be stated without metaphor: an organism may know the future best only after it has become too late to act on that knowledge. In the motivating analogy used during model development, the migrant is a train travelling toward a destination whose seasonal timetable is not yet fully known—a “Shinkansen to Schrödinger's spring.” The formal theory, however, is standard sequential inference and feedback control applied to an ecological timing problem.

We develop the argument in four linked steps. First, we derive when improving information should be acted upon while response options are disappearing. Second, we introduce a signed route-wise phase controller that allows both late and early individuals to correct error at repeated checkpoints. Third, we show how actors exposed to the same improving information can desynchronize if their correction opportunities decay at different rates. Fourth, we retain the earlier coordination-game result showing that environmental information can recover before coordinated information use recovers.

The empirical evidence is deliberately layered rather than treated as one direct validation. Existing natural data support predictive connectivity, route-stage cue use, bidirectional timing compensation and compensation costs, but do not yet identify the complete latent-state controller in a single system. The direct route-wise test is therefore prospective.

Our revised ecological claim is:

> **Seasonal tracking depends not only on how accurately organisms can infer a future state, but on whether they can still correct their seasonal phase when that information becomes available.**

---

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

### 2.6 Migration as repeated infer–correct–propagate control

The route-wise model changes the interpretation of migration.

Rather than

\[
\text{departure decision}\rightarrow\text{arrival},
\]

the ecological sequence becomes

\[
\boxed{
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

Departure error can therefore be large while arrival error is small. Conversely, early departure need not produce early arrival if later stopovers absorb the advance.

This generates a distinction between two forms of tracking capacity:

1. **prediction capacity** — how accurately the organism can estimate the relevant future seasonal state;
2. **control capacity** — how strongly it can alter phase after that estimate changes.

### 2.7 Controller asymmetry converts shared seasonal error into interaction mismatch

For actor \(i\), the noisy-feedback representation gives effective
regression-scale mean phase retention

\[
\lambda_i=\phi_i(1-g_iK_i).
\]

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

This directly links individual tracking control to interaction mismatch.

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
actors retain or correct that error differently. No difference in external
climate exposure and no initial interaction mismatch are required.

Here (G_i) is the readiness gate generated by the developmental/physiological
clock. The previous decision-only controller is the special case (G_i=1).

With equal passive retention, information asymmetry alone is sufficient:

\[
\Delta_{t+1}
=
-\phi g(K_1-K_2)m_t,
\]

readiness-clock asymmetry alone is sufficient:

[
Delta_{t+1}
=
-phi gK(G_1-G_2)m_t,
]

and with equal readiness and information weight, control-gain asymmetry alone
is sufficient:

\[
\Delta_{t+1}
=
-\phi K(g_1-g_2)m_t.
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

Controller differences are therefore amplified when either actor approaches
weak restoring control \(\lambda\to1\). This is more specific than saying that
two species have different phenological sensitivities: the theory identifies
the information/control asymmetry that converts common environmental error
into differential ecological timing.


For a weighted interaction network with actor retentions
\(\boldsymbol\lambda\), graph Laplacian \(L\), total edge weight \(W\), and a
shared incoming error \(m_t\), the same result generalizes to mean squared
edge mismatch

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

Thus community mismatch depends on where controller differences sit in the
interaction network, not only on their marginal variance. If controller states
are binary, the expression reduces exactly to the earlier network-cut geometry:
only edges joining unlike controller states contribute. The discrete
asynchronous-uptake result is therefore a special case of continuous
controller discordance.

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

### 4.3 Seasonal timing contains two different clocks

The phrase “biological clock” can hide two distinct mechanisms.

A **developmental or physiological timer** progresses an internal state toward
a seasonal threshold. Emergence, diapause termination, flowering readiness and
circannual migratory disposition can be represented schematically as

\[
\dot z=v(E_t,z),
\qquad
\tau=\inf\{t:z(t)\ge\Theta\}.
\]

Environmental conditions can change the timer rate or threshold crossing
without requiring the organism to estimate whether it is currently early or
late relative to an ecological target. In insects, photoperiodic and circadian
clock pathways can contribute to this timer, but PAYOFF-B does not assume that
all bee emergence is governed by one molecular oscillator.

An **inferential decision clock** instead repeatedly estimates signed phase
error and chooses a correction:

\[
\hat e_t=E[e_t\mid I_t],
\qquad
u_t=\pi_t(\hat e_t,A_t).
\]

This is the functional “Mikawa-Anjo clock”: a route checkpoint at which an
animal behaves as if it assesses whether it is early or late and changes speed,
stopover duration, route or departure accordingly.

Migratory birds can contain **both layers**. Endogenous circannual and
photoperiodic programmes can create migratory readiness or a broad departure
window, while weather, fuel state and en-route information govern repeated
decisions after that gate opens. The developmental layer therefore helps
determine which actions are available; the decision layer determines which
available action is taken.

This distinction is empirically testable. A developmental timer predicts
cue-dependent threshold timing with little signed post-event correction. A
decision controller predicts opposite responses to early versus late phase
error and can generate a downstream phase-variance funnel. The same observed
phenological shift can therefore arise from different clock architectures.

### 4.4 A variance funnel distinguishes individualized feedback from a common schedule

Mean timing alone cannot distinguish a common timing programme from
individualized correction. If every individual receives the same open-loop
timing shift, that common shift changes the mean but does not selectively
reduce between-individual phase variance.

Under the Gaussian route-wise controller, incoming phase variance \(P_t\),
checkpoint observation variance \(R_t\), posterior weight
\(K_t=P_t/(P_t+R_t)\), feedback gain \(g_t\), passive retention \(\phi_t\) and
new process variance \(Q_t\) give

\[
P_{t+1}
=
\phi_t^2P_t[1-K_tg_t(2-g_t)]+Q_t.
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
information, the observed regression-scale phase retention is

\[
\lambda_t=\phi_t(1-g_tK_t),
\]

not \(\phi_t(1-g_t)\) unless phase information is perfect. Define

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
\\qquad
g_t=\frac{d_t}{K_t}.
\]

Thus, if passive retention \(\phi_t\) and process innovation \(Q_t\) are
identified independently, mean retention plus the variance funnel can
separate an effective checkpoint-information weight \(K_t\) from a feedback
gain \(g_t\). This is a prospective functional inverse, not evidence that
animals explicitly compute Bayesian weights.

### 4.5 The most informative checkpoint need not be the most important checkpoint

The actionability theorem predicts an intermediate-stage peak in behavioral cue responsiveness. Early in the route, the signal can be too poor to guide correction. Late in the route, the signal can be excellent but response options can be exhausted.

The ecologically important checkpoint is therefore where information gain and remaining correction capacity jointly make information most valuable.

This prediction differs from a simple “closer cues are better” model.

### 4.6 Phase retention is a useful coordinate but not a mechanism by itself

The empirical phase-retention coefficient \(\lambda\) is valuable because it
quantifies how strongly incoming seasonal error persists to a later stage.
Under perfect phase information,

\[
\lambda=\phi(1-g),
\]

whereas with noisy individualized phase estimation,

\[
\lambda=\phi(1-gK).
\]

Thus the same \(\lambda\) can arise from different combinations of passive
persistence, information quality and active feedback. Negative retention can
arise from overshoot, anticipation, target movement or coordinate changes.
Direct mechanistic inference therefore requires actuator and environmental
information in addition to \(\lambda\).

### 4.7 Prediction and reactive correction can be substitute control channels

The controller also changes how cross-route comparisons should be interpreted.
Let (R(q)) be mismatch risk remaining after the actor has used available
pre-commitment information, and let downstream reactive gain (g) reduce that
error at quadratic cost (c g^2/2):

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
\(\lambda_i=\phi_i(1-g_iK_i)\) convert part of that common mode into a
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

The current evidence supports pieces of the mechanism across different systems. It does not yet demonstrate, in one natural population, the full sequence

\[
\text{checkpoint cue}
\rightarrow
\text{updated phase estimate}
\rightarrow
\text{signed correction}
\rightarrow
\text{reduced next-stage phase error}.
\]

That is now the clearest empirical target.

The strongest future test would compare a departure-only model with a checkpoint-updating model on held-out downstream phase. It would separately measure cue quality and actuator availability, avoiding circular estimation of information from the same behavior being predicted.

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
