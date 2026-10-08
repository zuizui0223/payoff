# Environmental predictability is not enough for seasonal tracking: a timer–controller architecture for phenological mismatch

**PAYOFF-B Paper 2 — V4 post-V8 integration candidate**  
**Date:** 2026-10-05  
**Status:** New candidate manuscript built after the prospective V8 outcome. The V3 science-frozen manuscript remains unchanged as the rollback source.

## Abstract

**Aim:** Phenological mismatch is often attributed to inadequate environmental
information: if seasonal conditions become harder to predict, migrants and
their resources should decouple. We ask a more general question: **is better
environmental predictability sufficient for better realized tracking?**

**Location:** General theory, with empirical tests in migratory birds and
individual-level mechanism evidence from mule deer in North America.

**Time period:** The principal bird analysis compares 2002–2009 with
2010–2017; supporting natural systems are dataset-specific.

**Major taxa studied:** Migratory birds and mule deer, with other seasonal
interactions used as mechanistic benchmarks.

**Methods:** We separate environmental information quality from biological
actionability in a serial timer–controller model. A developmental or
physiological timer determines entry into a seasonal trajectory; a downstream
information-dependent controller determines whether phase error is corrected.
We combine the theory with a prospectively specified multi-species test of
source–destination spring predictive connectivity, a registered
connectivity-change to mismatch-change test, structural nulls, and
individual-level movement analyses.

**Results:** Across 166 unique source–destination spatial pairs used by 28
migratory bird species, detrended spring predictive connectivity increased
between periods (mean \(\Delta\rho=+0.369\), 95% pair-bootstrap CI
+0.298 to +0.436; 26/28 species means positive). Yet larger connectivity gains
did not predict larger reductions in arrival–green-up mismatch
(\(\beta=+0.062\), 95% CI -0.014 to +0.136); the apparent positive slope
was reproduced by fixed-arrival and within-window permutation nulls. In the
theory, information can become more accurate while opportunities to use it
decline. In mule deer, nutritional condition predicts migration-start timing,
whereas signed phase predicts downstream speed and stopover use.

**Main conclusions:** The range-based environmental correlation proxy does
not, by itself, predict the registered change in seasonal matching. That proxy
does not measure what birds perceived or how accurately their forecasts were
calibrated. A serial timer–controller model distinguishes readiness from
post-entry correction and clarifies how information, action constraints and
costs could jointly determine realized tracking. The empirical analyses do
not identify a single missing causal mechanism or reproductive fitness gain.

**Keywords:** phenological mismatch; seasonal timing; migration; information
ecology; environmental predictability; feedback control; recourse; climate
change

---

## 1. Introduction

Phenological mismatch is commonly explained as a failure to keep pace with a
moving seasonal target. For migrants, one particularly intuitive mechanism is
loss of environmental predictability: an earlier location becomes a poorer
guide to conditions that will be encountered later, so departure and movement
decisions are made from degraded information.

That explanation is plausible but incomplete. The observed correlation of
environmental states at two geographical points is not automatically a
predictive signal available to an animal at its decision time. In particular,
stronger within-period correlation can coexist with a changing cue-to-target
mean or slope, an outdated learned forecast, or no cue perception at all.
Better information has value only while useful actions remain available.
A migrant can acquire more accurate information as it approaches a breeding
destination, yet simultaneously lose
the ability to undo earlier departure, fuelling, route or stopover decisions.
Plants and developmentally committed insects represent the opposite extreme:
local information can be accurate, but the focal event can become difficult to
reverse once initiated. Environmental information quality and biological
actionability are therefore distinct axes.

An additional distinction is essential: a better match to a seasonal target
need not imply greater fitness once the costs of early arrival, travel,
competition or adjustment are considered. Torstenson and Shaw (2025, *Oikos*,
doi:10.1111/oik.10862) explicitly separate cue timing accuracy from cue
fitness efficacy and show that the relative benefit of temporal and
environmental migration cues can reverse across habitat-seasonality regimes.
Consequently PAYOFF-B does **not** claim novelty for cue-type reversal or the
general proposition that phenological matching differs from fitness.

Long-distance migration makes the distinction especially visible. Departure is
not the only decision. Speed, stopover duration, route, skipping behaviour and
post-arrival timing can be altered while new information is acquired. Seasonal
tracking is consequently better represented as repeated inference and
correction than as a single phenological response coefficient.

Here we separate two timing layers. A developmental or physiological entry
timer determines when a seasonal trajectory begins and with what initial phase
error. A downstream controller then estimates signed seasonal phase and uses
whatever actuators remain available to correct that error. The architecture
allows information quality to improve while retained actionability declines,
and it predicts that interacting actors can become mismatched even under shared
environmental forcing.

We also test the simpler external-information explanation prospectively. In a
broad migratory-bird dataset we ask whether source–destination spring
predictive connectivity deteriorated between two non-overlapping periods, and
whether routes showing larger changes in connectivity showed corresponding
changes in arrival–green-up mismatch. This provides a direct stress test of
the proposition that changing environmental predictability is sufficient to
explain changing tracking.

The empirical result is deliberately not used to retune the theory. The
registered degradation prediction fails in the opposite direction:
source–destination spring connectivity strengthens broadly. Yet larger gains
in connectivity do not produce the preregistered reduction in bird mismatch,
and structural nulls prevent interpreting the raw positive association as a
bird response. We therefore use the bird analysis to reject a simple
information-loss explanation, not to identify the missing mechanism.

We then derive the timer–controller architecture and evaluate its separate
components with independent natural evidence, using mule deer as the strongest
same-system example of distinct entry-state and downstream-control signals.
Our central claim is:

> **Environmental predictability is only one component of seasonal adaptation:
> realized tracking also depends on when information becomes actionable and on
> the downstream opportunities available to correct phase error.**

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

In the single-commitment limit, the downstream consequences of waiting can be
compressed into an effective deadline cost,
\[
D_{\rm eff}(\delta)
=
J(\delta)+\min_c\{K(c)+M(\delta-c)\}.
\]
This reduced bridge explains why raw elapsed delay need not rank deadline
severity. V3 does not infer natural \(D_{\rm eff}\) values from observed phase
retention or compensation.

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

**Ecological phase-coordinate boundary.** The model's \(e_t\) is defined
relative to its assumed *fitness-relevant target*, whereas GPS or remote
sensing often supplies only a resource-centred proxy. Define

\[
r_t=t_{\mathrm{event},t}-t_{\mathrm{resource},t},
\qquad
\delta_t=t_{\mathrm{fitness\ optimum},t}-t_{\mathrm{resource},t}.
\]

Then the fitness-centred phase is exactly

\[
e_t=r_t-\delta_t.
\]

The offset \(\delta_t\) need not be zero: it may depend on energetic reserves,
offspring developmental time, mortality risk, or subsequent life-history
events. If the measured forage-centred process obeys
\(r_{t+1}=\phi_t(r_t-u_t)+w_t\), the same process expressed in fitness-centred
coordinates obeys

\[
e_{t+1}=\phi_t(e_t-u_t)+
\left[w_t+\phi_t\delta_t-\delta_{t+1}\right].
\]

This is a coordinate identity, not a new theorem or a measured selection
gradient. Until \(\delta_t\) is estimated from independent fitness
observations, a reduction in \(|r_t|\) establishes closer alignment with
the resource marker, **not** a measured increase in fitness.

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

Let correction cost be quadratic and residual *fitness-centred phase*
mismatch costly:

\[
L(u)=\kappa u^2+\mu(e-u)^2.
\]

Here \(\mu(e-u)^2\) is an assumed local loss approximation; it is not a
regression-derived survival or reproductive cost. The resulting optimal
control direction is valid for this declared loss and a correctly defined
target, but need not hold if a field study substitutes the vegetation
green-up peak for the actual fitness optimum without estimating their
offset.

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

This gives an exact decomposition of segment-scale phase retention **for the
declared fitness-centred state under perfect phase estimation and no target
shift**. Its coefficient is not identified by fitting observed resource-centred
Days-From-Peak phase unless the resource-to-fitness offset in Section 2.2
has also been identified or appropriately constrained.

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

### 2.6 An entry timer and a decision controller operate sequentially by default

Seasonal timing can involve two mechanistically different control layers.

A **developmental/physiological entry timer** carries an internal state \(z_i(t)\)
and determines when the focal behavioral mode becomes available:

\[
\tau_i
=
\inf\{t:z_i(t)\ge\Theta_i\}.
\]

The actor enters that mode with signed ecological phase error \(e_{i,0}\).
This is a rate-to-threshold mechanism and need not require estimating whether
the organism is early or late relative to an ecological target.

After entry, an **inferential decision controller** estimates phase and chooses
correction:

\[
\hat e_{i,k}=E[e_{i,k}\mid I_{i,k}],
\qquad
u_{i,k}=\pi(\hat e_{i,k},A_{i,k}).
\]

Its reduced post-entry retention is

\[
\lambda_i
=
\phi_i(1-h_iK_i),
\]

where \(K_i\) is effective phase information and \(h_i\) is enacted correction.
For a serial entry gate, \(h_i=O_i g_i\): readiness has already been crossed,
while remaining opportunity \(O_i\) and decision gain \(g_i\) govern later
correction. Here \(O_i\) is the actuator-specific realization of the retained
actionability \(r(t)\) introduced in Section 2.1. The quantity \(r(t)\)
summarizes the fraction of the full state-contingent response still usable,
whereas \(O_i\) is the opportunity factor entering a particular phase-control
channel; they coincide only in the scalar one-opportunity case. A concurrent
physiological gate can instead enter \(h_i\) when readiness is independently
measured at the same decision stage.

Thus the ecological sequence is

\[
\boxed{
\text{become ready}
\rightarrow
\text{enter with }e_0
\rightarrow
\text{observe}
\rightarrow
\text{correct}
\rightarrow
\text{observe again}.
}
\]

The post-entry decision controller is mechanistically distinct from the
physiological entry timer even when physiological state persists after entry.

### 2.7 The entry timer and decision controller contribute separately to interaction mismatch

For two actors, define entry-state mean error and mismatch

\[
m_0=\frac{e_{1,0}+e_{2,0}}{2},
\qquad
\Delta_0=e_{1,0}-e_{2,0}.
\]

In the no-innovation witness,

\[
e_{i,n}=\lambda_i^n e_{i,0}.
\]

Therefore mismatch after \(n\) checkpoints is exactly

\[
\boxed{
\Delta_n
=
(\lambda_1^n-\lambda_2^n)m_0
+
\frac{\lambda_1^n+\lambda_2^n}{2}\Delta_0.
}
\]

The first term is **controller-generated mismatch**: different downstream
controllers convert a shared entry error into differential timing. The second
is **timer-propagated mismatch**: a phase difference already created by the
readiness timers survives downstream.

Two limiting cases separate the mechanisms. If both actors share the same
post-entry controller,

\[
\Delta_n=\lambda^n\Delta_0,
\]

so feedback can only retain or erase the mismatch inherited at entry. If entry
is synchronized, \(\Delta_0=0\), then

\[
\Delta_n=(\lambda_1^n-\lambda_2^n)m_0,
\]

so controller asymmetry alone creates mismatch.

For a weighted interaction network exposed to shared error \(m\), the
one-step continuous analogue is

\[
\mathcal M
=
m^2
\frac{\boldsymbol\lambda^\top L\boldsymbol\lambda}{W},
\]

where \(L\) is the interaction-network Laplacian and \(W\) total edge weight.
Thus community mismatch depends on where unlike controllers interact, with the
earlier binary network-cut result recovered as a special case.

This serial decomposition separates **where a seasonal trajectory starts**
from **what happens to its error afterward** *within the declared model*.
Empirical pairwise interactions need independently defined biological timing
targets, because different species can have different resource-to-fitness
offsets, and a pairwise calendar overlap is not itself a pairwise fitness
measure.

### 2.8 Information recovery can still fail to restore coordination

The route-wise controller describes within-actor correction. The earlier coordination game remains relevant after actors interact.

At perfect information, an obsolete timing convention and an informed convention can both be strict equilibria when the temporary interaction cost of moving first exceeds the individual gain from unilateral information use. Therefore two distinct barriers can prevent recovery.

First, **physical or developmental irreversibility**: accurate information arrives after useful actions have disappeared.

Second, **strategic irreversibility**: actions remain physically possible, but unilateral change is selected against because partners remain in the previous convention.

The first route is a control constraint. The second is a coordination constraint. They should not be conflated.

---

## 3. Natural evidence

### 3.1 Predictive connectivity strengthened without the predicted improvement in mismatch

We first tested the simplest information-loss explanation prospectively. The
V8 environmental analysis used a frozen range-based source–target mapping in
which each breeding-range target cell was paired with the nearest lower-latitude
migratory-range source cell for the same species. The primary inferential unit
was the unique spatial source–target pair, preventing species that shared the
same environmental relationship from duplicating the environmental outcome.

Across 166 finite unique spatial pairs used by 28 species, detrended
source–destination green-up correlation changed strongly in the direction
opposite to the registered degradation hypothesis. The unique-pair mean was

\[
\overline{\Delta\rho}=+0.369,
\]

with 95% pair-bootstrap CI (+0.298, +0.436). The equal-species exposure mean
was +0.336 (95% CI +0.263 to +0.431), and 26 of 28 species means were positive.
Fisher-z, exact-complete-window, alternative-window, raw-correlation and
leave-one-species-out sensitivities all retained the positive direction.
Thus broad degradation of this environmental predictive coordinate is not
supported in the sampled system.

We then tested whether larger gains in predictive connectivity were associated
with larger reductions in realized arrival–green-up mismatch over the same
period. The frozen transfer analysis retained 150 species-target rows, 72
unique spatial pairs and 22 species. Contrary to the registered negative
direction, the equal-species-weighted coefficient was

\[
\hat\beta_{\rm transfer}=+0.0624,
\]

with 95% unique-pair bootstrap CI (-0.0141, +0.1363). The sample also showed no
clear overall change in log mismatch: the equal-species mean late-minus-early
change was -0.0203 (95% CI -0.0900 to +0.0512).

The positive transfer point estimate is not interpreted as a biological
worsening response. Holding each species-target bird arrival date fixed while
allowing green-up to vary produced a positive null coefficient (+0.0474), and
the observed-minus-fixed-arrival increment was only +0.0150 (95% CI -0.0521 to
+0.1027). Within-window arrival permutations likewise reproduced positive
coefficients, with the observed value lying well inside the permutation
distribution. The apparent positive slope can therefore arise from shared
target-green-up geometry and the nonlinear mismatch transformation.

A stricter matched between–within decomposition also failed to recover a
negative information effect: the persistent between-route coefficient was
+0.0122 (95% CI -0.1111 to +0.0894), and the within-route coefficient was
+0.0518 (95% CI -0.0117 to +0.1131). The earlier pooled association between
pre-outcome connectivity and smaller mismatch is therefore retained only as a
dependence-sensitive supporting result, not as the central empirical claim.

The licensed conclusion is narrower but consequential: **environmental
predictive connectivity strengthened strongly, yet larger connectivity gains
did not translate into the predicted improvement in realized bird mismatch**.
Because the source–target links are range-based spatial proxies rather than
tracked individual routes, and because the analysis does not identify cue
perception or causality, this result is a sufficiency stress test rather than a
mechanistic estimate.

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
model. Crucially, the measured Days-From-Peak is a **forage-centred** timing
coordinate, not an observed individual fitness optimum. The signed
coefficients support a behavioral phase-tracking interpretation but do not
identify the fitness-gradient coefficient (mu) in Section 2.4.

Using the same verified Source Data, we tested both readiness and channel
separation. Of 93 animal-years with IFBFat and migration timing, 62
animal-years from 40 deer began after March 31, guaranteeing that March IFBFat
preceded departure. IFBFat predicted standardized migration start
(\(-3.97\) d/unit; animal-cluster 95% CI \(-6.31\) to \(-0.69\)); the
year-fixed-effect sensitivity crossed zero. In that same safe subset, models
including both IFBFat and signed starting phase showed that phase retained
associations with movement rate (\(+0.0742\), 95% CI \(+0.0387\) to
\(+0.1028\)) and stopover (\(-0.234\), \(-0.429\) to \(-0.0095\)), whereas
IFBFat intervals spanned zero in both downstream models.

The prespecified post-freeze proxy moderation analysis also failed to show
that March IFBFat gates the phase-to-actuator response. The starting-phase
by IFBFat interaction for movement rate was -0.0152 (animal-cluster 95% CI
-0.0542 to +0.0219), and the stopover interaction was +0.0481 (95% CI
-0.1539 to +0.2365). Neither was supported in the year-centred sensitivity
either. These negative results are retained as a **limit on H2**, not as
evidence that a different readiness state could never gate correction.

Taken together, these results provide a candidate same-population
timer–controller anchor and support channel dissociation: physiological
condition is associated with when migration begins, whereas ecological phase
is associated with how migration is subsequently paced. It does not establish causal independence, identify
IFBFat with the readiness gate \(G\), or demonstrate H2 readiness-gated
feedback. The primitive \(G,O,K,g,\phi,Q\) decomposition remains unresolved.

### 3.4 Bar-tailed godwits absorb early departure later in the route

In bar-tailed godwits migrating from New Zealand through the Yellow Sea to Alaska, departure advanced by about six days over 2008–2020, but Alaska arrival and breeding did not advance correspondingly. Longer later stopovers absorbed the earlier departure.

This supplies the opposite sign of recourse: being early can be corrected by delaying progress later in the route.

Together with mule deer, the two examples show why departure timing alone is not a sufficient measure of downstream seasonal phase.

The serial principle also extends beyond movement. In greater snow geese,
prelaying duration declines by 0.53 d for each day of later arrival, implying a
same-sample simple stage-retention coefficient of \(1-0.53=0.47\) from arrival
to laying. Because correlations among sequential timing variables need not
imply strategic control, we treat this as **descriptive buffering**, not a
feedback-gain estimate. In the pied-flycatcher tit-phenology experiment, the
manipulation did not alter arrival timing, whereas later female settlement
responded after the cue became observable. Together these systems show that
different mechanisms can govern successive seasonal stages.

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

A complementary reproductive anchor comes from Greenland white-fronted
geese (Schindler et al. 2024, *Proceedings of the Royal Society B*,
doi:10.1098/rspb.2023.2016). Across 108 observed breeding seasons
(28 successes, 73 failures and 7 deferrals), females spending more time
feeding and less energy during spring migration were more likely to breed
successfully. High energy expenditure coupled with little feeding was most
associated with breeding deferral; the authors did not find that the particular
spring sub-season in which feeding or expenditure occurred altered these
breeding associations. These are **published source-study results**, not new
PAYOFF-B estimates, and the associations are observational rather than causal.
They establish a different ecological margin from phenological matching:
migration may end at an apparently suitable time while the energetic state
carried into breeding remains unfavorable.

The state needed to interpret a timing correction is consequently not only
the residual phase error but also the energetic cost of reaching that phase.
For a conceptual augmented controller, let energetic reserve evolve through
intake minus movement and maintenance costs, while subsequent breeding payoff
depends jointly on residual phase and reserve. This **does not** identify a
fitness cost function from the existing V8 birds or the mule-deer source table:
the Greenland study lacks the same individual's registered incoming
phase-error-and-independent-recourse contrast required for that inference.

Two additional natural systems show why even the *direction* of the
fitness-optimal seasonal offset can differ. Aikens et al. (2021,
*Ecology*, doi:10.1002/ecy.3334) found that short-distance migratory
mule deer in western Wyoming generally gave birth earlier than
long-distance migrants and less closely matched summer green-up.
The authors proposed an ecological trade-off between immediate forage
availability and additional offspring growth time before winter.
They measured birth timing, fetal development and birth mass, **not a
causally identified lifetime survival advantage of that early-birth
strategy**. This is independent published prior art, not a newly
demonstrated PAYOFF-B strategy, and is not assumed to involve the
same individual sample as the Red Desert Ortega analysis.

The contrasting split-brood winter moth–oak experiment of van Dis et al.
(2023, *Proceedings B*, doi:10.1098/rspb.2023.0414) directly estimated
survival and a fecundity proxy under manipulated relative hatching times.
Its reported composite-fitness optimum was around **2 days after**
oak budburst; hatching before leaves were available sharply reduced
caterpillar survival. This demonstrates a nonzero, asymmetric
resource-to-fitness timing offset in a local consumer–resource
interaction. It is not evidence that migrants use this same offset.

Together with the goose energy–breeding results, these studies impose a
strict boundary on PAYOFF-B: phenological matching, a physiological
compensation cost, and later fitness are distinct ecological endpoints.
Their published findings already establish that boundary in individual
systems. What PAYOFF-B has *not* established is a new cross-system
causal rule predicting the sign or size of (delta_t) from information
and actionability alone.

### 3.7 Interaction-level asymmetry changes relative timing

Across 10 European nest-box schemes, resident tits were more temperature-sensitive than migratory flycatchers, and this differential response widened their laying-date interval by 0.94 days per decade. Published UK bird–caterpillar analyses likewise show incomplete temporal tracking by consumers.

These systems support the ecological step from heterogeneous response rules to changing interaction timing. They do not directly estimate the route-wise phase controller.

### 3.8 Negative evidence defines the boundary

Several prospective tests fail, and those failures delimit the claim rather
than being reinterpreted as confirmation.

First, V8 rejects the proposed broad degradation of cross-site spring
predictive connectivity: the environmental coordinate increases strongly.
Second, the registered connectivity-gain to mismatch-improvement transfer is
not supported, but structural nulls show that the opposite-sign point estimate
cannot be treated as a bird response. Third, a matched between–within panel
supports neither a negative persistent between-route association nor a
negative within-route transfer. The repeated-speed actuator bridge is
not estimable under its frozen admission rule (5 species-target rows, 4 unique
pairs, 4 species), and its threshold is not relaxed.

The registered Eurasian wigeon test likewise does not support the predicted
negative interaction between incoming phase error and predictive connectivity.
Predictive connectivity should therefore not be treated as a universal
amplifier of post-error correction.

Two preregistered long-term environmental reversal gates also failed before any
natural hysteresis analysis was opened. PAYOFF-B consequently does not claim a
natural degradation–recovery hysteresis sequence.

Together these results rule out a convenient but overly simple narrative in
which environmental information quality alone explains mismatch. They do not,
by themselves, identify actionability loss, timer structure or recourse as the
cause. Those mechanisms are supplied by the formal model and evaluated in
separate individual-level evidence.

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

The main conceptual change is to separate the quality of the environmental
signal from the organism's capacity to act on it. In the V8 stress test,
detrended source–destination spring *correlation* becomes stronger rather than
weaker, yet the preregistered improvement in bird mismatch is not detected.
This does not show that birds received more useful information: cue
availability, belief calibration, individual routes and actionability were not
observed in V8. It therefore fails the registered correlation-to-matching
transfer hypothesis without establishing a biological actionability
bottleneck.

Two organisms can also reach the same observed arrival shift for very
different reasons. One may predict the future accurately and require little
correction. Another may depart with large timing error but repeatedly
compensate en route. A third may receive accurate information only after useful
correction has become impossible.

These cases are not equivalent biologically, even if their final timing is
similar. The relevant object is therefore a sequence of inference,
commitment and correction rather than a single fast-versus-slow phenological
response rate.

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

### 4.3 Entry timing and downstream control leave different empirical signatures

A developmental or physiological timer should primarily predict **entry
timing**: emergence, flowering, migratory readiness or another threshold
event. Temperature, photoperiod, endocrine state and molecular clock pathways
can contribute, but PAYOFF-B does not treat all bee emergence as one molecular
oscillator.

A decision controller predicts **signed post-entry correction**: late actors
advance, early actors delay, and repeated correction can narrow the phase
distribution.

Mule deer now provide both signatures in one population. March scaled IFBFat
predicts later migration-start timing in a conservative predeparture subset,
whereas signed starting phase predicts speed and stopover after departure. A
prespecified DFP × IFBFat moderation test did not support stronger signed
feedback at higher IFBFat.

A second frozen downstream-phase test also rejected the **pure entry-only
Markov handoff** as a complete description: in
\(DFP_{end}\sim DFP_{start}+IFBFat\), the clustered interval for
\(DFP_{start}\) crossed zero while IFBFat retained a raw conditional
association; after within-year residualization both became unresolved.

The appropriate distinction is therefore mechanistic rather than temporally
absolute. The entry timer and the decision controller can remain different
mechanisms even if physiological or energetic state persists after entry. A
post-hoc nested model writes

\[
s_{k+1}=\rho s_k,
\qquad
e_{k+1}=\lambda e_k+\beta s_k+w_k.
\]

This possibility is motivated, not confirmed, by the mule-deer result. Greater
snow geese provide an independent natural anchor: premigration condition
predicts lay date after arrival is controlled, and an unplanned reduction in
prebreeding condition delayed laying.

### 4.4 A variance funnel identifies effective feedback, not controller primitives

Individualized post-entry feedback predicts more phase-variance contraction
than a common open-loop schedule. With incoming variance \(P_t\), information
weight \(K_t\), effective correction \(h_t\), passive retention \(\phi_t\) and
new process variance \(Q_t\),

\[
P_{t+1}
=
\phi_t^2P_t[1-K_th_t(2-h_t)]+Q_t.
\]

Mean retention is

\[
\lambda_t=\phi_t(1-h_tK_t).
\]

If \(\phi_t\) and \(Q_t\) are independently known, mean and variance retention
can separate \(K_t\) from \(h_t\). They cannot, by themselves, separate the
primitive biological sources of \(h_t\).

For a serial entry-gate system after entry, \(h_t=O_tg_t\). If physiological
readiness is concurrently active at the same decision, \(h_t=G_tO_tg_t\).
The latter must be measured rather than assumed.

This matters because final synchrony can hide different strategies. With no new
innovation,

\[
V_n=\lambda^{2n}V_0,
\]

so a noisier entry timer can be offset by stronger downstream correction.
Arrival precision alone therefore does not identify how that precision was
achieved.

### 4.5 The most informative checkpoint need not be the most important checkpoint

The actionability theorem predicts an intermediate-stage peak in behavioral cue responsiveness. Early in the route, the signal can be too poor to guide correction. Late in the route, the signal can be excellent but response options can be exhausted.

The ecologically important checkpoint is therefore where information gain and remaining correction capacity jointly make information most valuable.

This prediction differs from a simple “closer cues are better” model.

### 4.6 Phase retention is a useful coordinate but not a mechanism by itself

The empirical phase-retention coefficient \(\lambda\) quantifies how strongly
incoming seasonal error persists to a later stage. For a serial post-entry
controller,

\[
\lambda=\phi(1-OgK)
=
\phi(1-hK),
\qquad
h=Og.
\]

The same \(\lambda\) can therefore arise from different combinations of
passive persistence, information quality, remaining opportunity and active
decision gain. A physiological readiness term should be reintroduced only when
readiness is independently measured at the same downstream decision stage.

Negative retention can arise from overshoot, anticipation, target movement or
coordinate changes. Direct mechanistic inference therefore requires actuator
and environmental information in addition to \(\lambda\).

### 4.7 Prediction and downstream correction can substitute before new error appears

Let \(R(q)\) be mismatch risk remaining after pre-entry information of quality
\(q\), and let post-entry correction gain \(g\) reduce that inherited error at
quadratic cost \(cg^2/2\):

\[
L(g;q)
=
(1-g)^2R(q)
+
\frac{c}{2}g^2.
\]

The optimum is

\[
g^*(q)
=
\frac{2R(q)}
{c+2R(q)}.
\]

If better prediction lowers inherited mismatch while correction cost is fixed,
optimal downstream correction becomes weaker. Accurate entry timing and strong
post-entry correction are therefore partially substitutable.

That substitution is limited. Once new phase noise is generated after entry,

\[
V_{k+1}
=
\lambda^2V_k+Q,
\]

so

\[
V_n
=
\lambda^{2n}V_0
+
Q\sum_{j=0}^{n-1}\lambda^{2j}.
\]

Improving the entry timer reduces only the first term. Post-entry innovations
can only be suppressed by downstream control. Thus feedback has a distinct
value in long, stochastic journeys even when departure timing is precise.

The serial architecture also permits formal allocation models in which entry
precision and downstream correction substitute under historical conditions.
Timer–feedback portfolio optimization and opportunity-loss fragility are retained as
prospective supporting theory rather than as a co-equal main-text claim because
no current natural dataset directly identifies the required allocation and
opportunity-loss parameters.


### 4.8 Interactions convert controller differences into ecological mismatch

The pairwise mode decomposition clarifies why interaction mismatch need not
require different climate exposure. A common environmental displacement enters
both actors as a shared phase error, but differences in effective retention
\(\lambda_i=\phi_i(1-O_i g_iK_i)\) convert part of that common mode into a
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

### 4.9 Direct natural validation remains prospective

The evidence is no longer purely cross-system. Mule deer provide a candidate
same-population two-layer hybrid: March physiological condition predicts
migration-start timing, while signed phase predicts later speed/stopover
correction and phase convergence. The prespecified IFBFat moderation test does
not support concurrent readiness-gated feedback. A separate frozen handoff test
does not support the stronger claim that physiological state acts only at entry.
The readiness association is also not invariant to every sensitivity analysis.

The direct serial test should therefore measure:

\[
\text{physiological state}
\rightarrow
\tau
\rightarrow
e_0
\rightarrow
(\text{checkpoint information, action})
\rightarrow
\lambda
\rightarrow
e_n.
\]

For the post-entry controller, mean and variance trajectories can identify
information weight \(K\) and effective correction \(h\) when passive retention
and process innovation are independently known. In the serial architecture
\(h=Og\) after entry. Separating opportunity \(O\) from decision gain \(g\)
still requires additional data; a concurrent physiological gate \(G\) should
only be introduced when readiness is measured at the same decision stage.

The strongest future test is therefore to measure entry readiness and entry
phase, then estimate repeated downstream phase retention in the same
individuals and interacting partners.


---

## 5. Conclusion

Environmental correlation, calibrated forecast skill, cue perception,
phenological matching and demographic fitness are five different quantities.
The current V8 evidence directly measures the first and a spatial proxy for
the fourth, not the other three. Moreover, closeness to a green-up marker
is not equivalent to closeness to a life-history-specific fitness optimum.
Environmental predictability is therefore
not synonymous with adaptive tracking. In the prospective bird stress test, source–destination spring predictive
connectivity strengthens broadly, yet larger connectivity gains do not yield
the preregistered improvement in arrival–green-up mismatch. The analysis does
not identify why, but it rejects a simple broad information-degradation
explanation for this sampled system.

The timer–controller model supplies a **candidate** mechanistic decomposition,
not an empirically established explanation for the V8 null. Under its declared
assumptions, a developmental or physiological timer determines when an organism enters a
seasonal trajectory with some initial phase error. An information-dependent
controller then determines whether that error is erased, retained or
amplified. For interacting species, the model writes later phase mismatch as two
components, conditional on a correctly defined target and observed state:

\[
\boxed{
\text{entry-timer mismatch}
+
\text{controller-generated mismatch}.
}
\]

This architecture provides a possible account of why more precise information
need not translate into improved realized timing; the empirical data do not
identify the proposed control channels as its cause. Information can become
more accurate while response options disappear; conversely, strong downstream
feedback can rescue a poorly timed start.

The ecological question is therefore not only whether the environment is
predictable or whether phenology shifts, but **when relevant information
becomes available, when the organism becomes able to act, and what can still be
changed after commitment**.

The strongest prospective validation remains to measure physiological
readiness, signed phase information, available actuators and downstream phase
retention in the same individuals and interacting partners.

---

## Post-freeze transparency statement

The V3 manuscript was science-frozen on 2026-10-03 and remains unchanged as a
rollback source. V4 was created only after the prospectively specified V8
environmental outcome, transfer test, mandatory sensitivities and structural
nulls were frozen. The original V8 degradation hypothesis is reported as
rejected and is not relabelled as a successful prediction. The positive raw
transfer slope is explicitly treated as structurally explainable rather than
as a biological bird response. Earlier preregistered negative results remain
negative. V4 is therefore a new integration candidate, not a retroactive
retuning of the V8 support rule.
