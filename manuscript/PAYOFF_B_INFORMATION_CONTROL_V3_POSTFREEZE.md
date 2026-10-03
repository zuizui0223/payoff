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

**Results:** Information quality can improve while useful response options disappear. In the reduced model, usable information value is (r(t)[Sq(t)-B]-C(t)); with exponential learning and recourse loss the unique zero-cost optimum is (t^*=\log(1+\alpha/\beta)/\alpha), generally before maximal cue accuracy. Route-wise phase dynamics obey (e_{t+1}=\phi_t(e_t-u_t)+w_t); under perfect estimation and proportional feedback, phase retention decomposes as (\lambda_t=\phi_t(1-g_t)). Thus early and late errors can be corrected in opposite directions and departure error need not equal arrival error. Natural evidence independently supports predictive connectivity, heterogeneous temperature responsiveness, route-stage compensation and compensation costs. The model additionally predicts a phase-variance funnel under individualized feedback, but the full controller is not yet identified in one system.

**Main conclusions:** Seasonal tracking is a sequential inference-and-control problem. Mismatch can arise because interacting organisms differ in when they can infer a future seasonal state, how long that information remains actionable and how strongly they can correct phase error after learning it. Restored information need not restore coordination after response options or coordinated conventions have been lost.

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

[
V_A(q)=Sq-B,
]

where (S) is the total state-dependent loss scale and (B) is the larger prior action loss.

Let (r(t)in[0,1]) represent retained actionability: the fraction of the full state-contingent response that remains usable at time or route stage (t). Let (C(t)) be cumulative direct cost of waiting. The reduced net value of using information at time (t) is

[
N(t)=r(t)[Sq(t)-B]-C(t).
]

For differentiable trajectories, an interior optimum satisfies

[
rSq'=-r'[Sq-B]+C'.
]

The left side is the marginal benefit of improving environmental information. The first term on the right is the loss of value as response options disappear; the second is the direct marginal cost of waiting.

When direct marginal waiting cost is zero,

[
rac{Sq'}{Sq-B}=-rac{r'}{r}.
]

Thus the optimum occurs when the relative gain in information value is exactly balanced by the relative loss of remaining actionability.

For exponential learning and exponential actionability loss,

[
q(t)=q_0+Delta q[1-exp(-alpha t)]
]

and

[
r(t)=exp(-eta t),
]

the unique zero-cost optimum is

[
t^*=rac{log(1+alpha/eta)}{alpha}.
]

The optimum moves earlier as (eta) increases. Two actors observing the same environmental-information trajectory can therefore commit at different stages solely because their remaining response options disappear at different rates.

A particularly important consequence is that perfect information can be too late. With (alpha=eta=1), the optimum is (t^*=log 2), where cue accuracy is only (q=0.75) in the symmetric witness even though (q	o1) later. Better information is not automatically more useful.

### 2.2 Route-wise phase state

The actionability model determines when information is worth using. It does not by itself describe what happens to the animal's timing error after the organism acts.

We therefore define signed phase error

[
e_t>0
]

for an actor that is late relative to the locally relevant seasonal optimum, and

[
e_t<0
]

for an actor that is early.

At route stage (t), the actor forms an estimate

[
hat e_t=E[e_tmid I_t],
]

where (I_t) is the information accumulated by that stage.

A signed correction (u_t) represents the combined timing effect of available actuators:

- (u_t>0): speed up, shorten stopover, skip delay or otherwise advance progress;
- (u_t<0): slow down, lengthen stopover, wait or otherwise delay progress.

The realized phase state then evolves as

[
oxed{
e_{t+1}=phi_t(e_t-u_t)+w_t
}
]

where (phi_t) is passive phase retention in the absence of active correction and (w_t) is change in the local seasonal target between checkpoints.

This matters because even a perfect correction at one checkpoint need not eliminate later mismatch. The resource wave itself can move.

### 2.3 The animal's internal phase estimate

For a transparent stochastic representation, suppose

[
e_tsim N(m_t,P_t)
]

and an intermediate environmental cue obeys

[
z_t=e_t+
u_t,qquad 
u_tsim N(0,R_t).
]

The posterior phase estimate is

[
K_t=rac{P_t}{P_t+R_t},
]

[
m_t^+=m_t+K_t(z_t-m_t),
]

[
P_t^+=(1-K_t)P_t.
]

The ecological interpretation is simple. An animal need not know its true phase error. It need only behave as if it repeatedly updates an estimate of whether it is too early or too late.

This filtering result is established control theory, not a claim of mathematical novelty.

### 2.4 Signed correction follows estimated phase error

Let correction cost be quadratic and residual phase mismatch costly:

[
L(u)=kappa u^2+mu(e-u)^2.
]

Conditional on the posterior phase belief,

[
E[L(u)mid I_t]
=
kappa u^2
+
mu[(m_t^+-u)^2+P_t^+].
]

Without actuator bounds, the optimal one-step correction is

[
u_t^*
=
g^*m_t^+,
]

where

[
g^*=rac{mu}{kappa+mu}.
]

Thus the sign of correction follows the sign of the estimated phase error. Late actors advance; early actors delay. Stronger residual mismatch costs increase the correction gain, whereas more expensive movement or stopover adjustment reduces it.

Finite speed, stopover or route flexibility clips this correction to the feasible interval. The organism can therefore remain mismatched even when it knows the direction of the required correction.

### 2.5 Phase retention decomposes into passive carry-over and active feedback

Under perfect estimation, proportional feedback

[
u_t=g_te_t,
]

no actuator clipping and no target shift,

[
e_{t+1}
=
phi_t(1-g_t)e_t.
]

Therefore

[
oxed{
lambda_t=phi_t(1-g_t).
}
]

This gives an exact decomposition of segment-scale phase retention.

If (g_t=0), the observed phase coefficient is passive carry-over (lambda_t=phi_t).

If (0<g_t<1), active correction reduces retained phase error.

If (g_t=1), the current phase error is reset at that checkpoint when the target does not move.

If (g_t>1), the controller overshoots and (lambda_t) can become negative.

The existing PAYOFF-B closed-loop model

[
e_{t+1}=(1-K)e_t+r
]

is recovered exactly by setting (phi_t=1), (g_t=K), (hat e_t=e_t) and (w_t=r). The route-wise model is therefore an extension of the existing phase controller rather than a separate theory.

The decomposition also establishes an important identification boundary: neither (1-|lambda|) nor (lambda) itself is a direct estimate of recourse, actionability or control gain without an independent estimate of passive retention and an explicit actuator model.

### 2.6 Migration as repeated infer–correct–propagate control

The route-wise model changes the interpretation of migration.

Rather than

[
	ext{departure decision}ightarrow	ext{arrival},
]

the ecological sequence becomes

[
oxed{
	ext{move}
ightarrow
	ext{observe}
ightarrow
	ext{update phase belief}
ightarrow
	ext{correct}
ightarrow
	ext{move again}.
}
]

Departure error can therefore be large while arrival error is small. Conversely, early departure need not produce early arrival if later stopovers absorb the advance.

This generates a distinction between two forms of tracking capacity:

1. **prediction capacity** — how accurately the organism can estimate the relevant future seasonal state;
2. **control capacity** — how strongly it can alter phase after that estimate changes.

### 2.7 Different controllers create interaction mismatch

For interacting actors (i), each can have its own information trajectory (q_i(t)), retained actionability (r_i(t)), phase-estimation reliability and correction gain (g_i(t)).

Even if two species experience the same external environmental change, they need not act on it at the same stage. Faster actionability loss shifts optimal commitment earlier. Greater correction cost reduces feedback gain. Poorer remote information weakens the phase estimate.

The result is a mechanistic route to seasonal mismatch:

[
	ext{different inference}
+
	ext{different remaining recourse}
+
	ext{different correction gain}
ightarrow
	ext{different phase trajectories}.
]

This is more specific than saying that two species differ in phenological sensitivity.

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

[
hateta_ho=-0.0462,
]

with 95% CI ([-0.0870,-0.0054]) and (p=0.0265). Stronger pre-existing predictive connectivity is therefore associated with smaller arrival–green-up mismatch in the declared pooled analysis.

The sign remains negative in all leave-one-species-out and leave-one-year-out fits, but dependence-aware intervals cross zero. The licensed conclusion is a pooled directional macroecological signal, not a universal species-level coefficient.

### 3.2 Long-distance migrants show weaker temperature responsiveness

A separate reconstruction of the Usui et al. source table retains 944 temperature-response effects from 28 studies and 279 species after restricting migration distance to short and long classes.

The adjusted long-minus-short contrast is

[
+0.421 mathrm{d}/^circmathrm C
]

with 95% CI (+0.121) to (+0.722) and (p=0.0077). Because negative slopes denote earlier timing in warmer years, long-distance migrants are less temperature-responsive than short-distance migrants in this reconstruction.

This pattern is not uniquely diagnostic of information distance; endogenous timing and photoperiodic control remain alternative explanations.

### 3.3 Mule deer show signed route compensation

Published tracking of 72 adult female mule deer over 152 animal-years provides a natural example of phase correction during movement. Early migrants began about 30 days ahead of peak instantaneous rate of green-up, whereas late migrants began about 20 days behind. Late migrants moved about 2.5 times faster and spent about 72% less time on stopovers than early migrants.

This is consistent with signed correction: late phase error is followed by advancement through speed and stopover compression. The source summaries do not identify the internal phase estimate, passive retention or feedback gain.

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

[
	ext{phase recovery}

eq
	ext{zero biological cost}.
]

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

[
e_{mathrm{in}}
ightarrow
	ext{actuator response}
ightarrow
e_{mathrm{out}}.
]

A route-wise analysis should estimate signed incoming error, the information available at the checkpoint, the subsequent speed/stopover/route response and the outgoing error at the next checkpoint.

### 4.3 A functional “phase sense” is testable without claiming neural calculation

The model does not require animals to compute probabilities, Kalman gains or explicit dates. The testable biological claim is functional:

> animals behave as if they update an internal estimate of seasonal phase and alter movement according to the sign and magnitude of that estimate.

This can be falsified. If independently estimated incoming phase error does not predict correction direction despite unused actuator capacity, the feedback interpretation is weakened.

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


The mean and variance signatures can also be combined. Under the same reduced
model,

\[
\rho_V=\frac{P_{t+1}-Q_t}{P_t}
=(1-K_t)\phi_t^2+K_t\lambda_t^2.
\]

If passive retention \(\phi_t\) and process innovation \(Q_t\) are identified
independently, then mean retention \(\lambda_t\) together with the variance
funnel identifies an effective checkpoint-information weight

\[
K_t=
\frac{\phi_t^2-\rho_V}
{\phi_t^2-\lambda_t^2}.
\]

This is a prospective functional estimate of phase information, not evidence
that animals explicitly compute Bayesian weights.

### 4.5 The most informative checkpoint need not be the most important checkpoint

The actionability theorem predicts an intermediate-stage peak in behavioral cue responsiveness. Early in the route, the signal can be too poor to guide correction. Late in the route, the signal can be excellent but response options can be exhausted.

The ecologically important checkpoint is therefore where information gain and remaining correction capacity jointly make information most valuable.

This prediction differs from a simple “closer cues are better” model.

### 4.6 Phase retention is a useful coordinate but not a mechanism by itself

The empirical phase-retention coefficient (lambda) is valuable because it quantifies how strongly incoming seasonal error persists to a later stage. But the decomposition

[
lambda=phi(1-g)
]

shows why the same (lambda) can arise from different mechanisms.

Low retention can reflect strong active feedback, low passive persistence, or both. Negative retention can arise from overshoot, anticipation, target movement or coordinate changes. Direct mechanistic inference therefore requires actuator and environmental information in addition to (lambda).

### 4.7 Prediction and reactive correction can be substitute control channels

The controller also changes how cross-route comparisons should be interpreted.
Let (R(q)) be mismatch risk remaining after the actor has used available
pre-commitment information, and let downstream reactive gain (g) reduce that
error at quadratic cost (c g^2/2):

[
L(g;q)=(1-g)^2R(q)+rac{c}{2}g^2.
]

The unique optimum is

[
g^*(q)=rac{2R(q)}{c+2R(q)},
qquad
lambda^*(q)=rac{c}{c+2R(q)}.
]

If better prediction lowers the mismatch reaching the feedback stage while
correction cost is fixed, optimal downstream correction becomes weaker. Strong
pre-commitment prediction and strong post-error correction are therefore
substitutes in this reduced model, not necessarily positively correlated
traits.

More generally, if cue quality also changes the effective cost of correction,
the sign is determined by

[
rac{d}{dq}lograc{g^*}{1-g^*}
=
rac{R'}{R}-rac{c'}{c}.
]

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

### 4.9 Interactions add a second layer of irreversibility

Physical correction and strategic coordination should be separated.

A migrant may still be capable of changing timing but face a partner that is not changing. A plant may have local environmental information but little developmental recourse after flowering begins. A consumer may have behavioral flexibility yet gain little from moving first if the resource or competitor remains on the previous schedule.

The Paper-2 game theory is most useful after the control theory, not before it: it explains why a physically feasible correction may remain strategically inaccessible.

### 4.10 Direct natural validation remains prospective

The current evidence supports pieces of the mechanism across different systems. It does not yet demonstrate, in one natural population, the full sequence

[
	ext{checkpoint cue}
ightarrow
	ext{updated phase estimate}
ightarrow
	ext{signed correction}
ightarrow
	ext{reduced next-stage phase error}.
]

That is now the clearest empirical target.

The strongest future test would compare a departure-only model with a checkpoint-updating model on held-out downstream phase. It would separately measure cue quality and actuator availability, avoiding circular estimation of information from the same behavior being predicted.

---

## 5. Conclusion

Seasonal migration should not be treated as a single departure date that determines a later arrival date.

Animals can move while learning. They can arrive at successive route stages with positive or negative seasonal phase error, update their estimate of the changing environment, and use speed, stopover duration, route and subsequent timing to reduce that error.

The resulting ecological problem has three coupled components:

[
oxed{
	ext{infer the seasonal target}
ightarrow
	ext{correct current phase}
ightarrow
	ext{retain enough options to correct again}.
}
]

Information generally becomes more accurate as the organism approaches the relevant future environment, but correction opportunities can disappear at the same time. The optimal information-use stage can therefore precede the stage of maximal cue accuracy.

For interacting species, differences in information, correction cost and remaining actionability create different phase trajectories even under the same external climate forcing. Seasonal mismatch can thus arise without a simple failure of adaptive capacity.

The strongest current interpretation is:

> **Climate adaptation can fail because organisms must control their seasonal phase toward a future target that becomes easier to infer only as the opportunities to correct toward it are disappearing.**

And the clearest prospective natural test is:

> **Do animals repeatedly re-estimate whether they are early or late at route checkpoints, and do those estimates predict the direction and magnitude of the correction made before the next checkpoint?**

---

## Post-freeze transparency statement

The stagewise recourse, continuous information-actionability balance and route-wise Bayesian phase-control extensions were formalized after the registered empirical gates and frozen GEB V2 package. They do not alter, reopen or retune any preregistered empirical outcome. The frozen V2 manuscript remains the audit and rollback source. This V3 document is a prospective integration draft for a later Paper-2 revision.
