# Seasonal tracking depends on information access and opportunities for correction

## Abstract

Environmental states can be forecastable to an analyst without providing
information that organisms can access at the relevant decision time. Seasonal
tracking therefore involves at least three distinct problems: environmental
forecastability, organismal information access, and opportunities for
downstream correction.

In migratory birds, a preregistered source–destination analysis showed
detrended spring correlation increasing from 0.284 to 0.653. Posthoc
cross-validation showed destination variability increasing from 2.41 to 4.66 d
while the squared-loss forecast value of adding nonlocal environmental
structure changed from -16.1 to +16.0 d^2. Yet in a restricted stage subset,
the realized source mid-green-up event occurred after the population front had
already reached the source cell in most annual observations, so the predictor
cannot be treated as an observed online cue. Target green-up advanced by 2.31 d
while estimated bird arrival shifted by only 0.19 d. Independent mule-deer data
showed strong phase convergence and signed downstream speed and stopover
adjustments.

We formalize seasonal tracking as a sequence from environmental forecastability
to accessible information, retained actionability, and correction.

**Keywords:** environmental forecastability; information access; phenological
mismatch; seasonal timing; migration; actionability; feedback control

---

## 1. Introduction

Phenological mismatch is usually described as a failure to keep biological
timing aligned with a moving seasonal target. For migrants, the problem begins
before the target environment is directly observable. Conditions at a wintering
or stopover site can carry information about spring farther along the route, and
chains of spatial environmental correlation have long been proposed as a basis
for migration timing (Kölzsch et al. 2015; Bauer et al. 2020).

But "predictability" contains several different ecological quantities.
Correlation measures how strongly two standardized anomalies move together. It
does not by itself measure how variable the destination is, how many days of
forecast error remain, or how much expected loss the cue removes relative to
acting without it. A cue can therefore become more informative in relative or
decision-theoretic terms while the environment simultaneously becomes more
variable in absolute units.

This decision-scale framing has strong prior foundations. McNamara et al.
(2011) explicitly showed that the consequences of seasonal cue use depend on
changes in cue–optimum correlation, slope, and the variance of the optimal
timing target, while Usinowicz and O'Connor (2023) developed a broader fitness
value-of-information framework for ecology. We therefore do not treat
decision-scale information value itself as new.

Empirical and theoretical migration work also distinguishes information
available in the environment from information actually used in movement
decisions (Shaw and Couzin 2013), and current environmental conditions from
climatological information. Robertson et al. (2024) found that many Western
Hemisphere migratory birds align more strongly with long-term average green-up
than with current green-up. We therefore do not treat environmental
availability versus biological use as a new distinction. Our analysis asks a
narrower temporal question: how the marginal out-of-sample value and calendar
timing of one reconstructed nonlocal environmental signal changed, and whether
population arrival changed with it.

A second distinction appears after information is acquired. Biological systems
combine anticipatory and feedback processes in fluctuating environments
(Bernhardt et al. 2020), and migration makes the separation especially visible.
An organism may forecast a future seasonal state before departure, then alter
speed, stopover duration, route, or later timing after observing new conditions.
The ecological value of information therefore depends not only on the forecast
problem but also on whether consequential actions remain available.

The distinction matters because seasonal decisions are not infinitely
reversible. A migrant can wait for better information, but waiting may consume
time needed for refuelling, route changes, stopovers, territorial arrival or
breeding. A flowering plant may experience highly informative local
temperature but have little ability to undo flowering once development has
passed a threshold. Conversely, an animal may commit early with poor
information yet retain several opportunities to compensate later. Information
quality and response opportunity can therefore move independently and even in
opposite directions.

We therefore separate three quantities. **Environmental forecastability**
describes how much an ideal observer can reduce prediction loss using external
environmental structure. **Organismal information value** describes the
decision loss an organism can reduce using information it can actually
encounter or infer at that stage. **Actionability** is the fraction of the
state-contingent response that remains biologically implementable. None is
equivalent to correlation, elapsed time or distance.

This distinction leads to a direct prediction. If organismally accessible
information value increases through a seasonal sequence while actionability
declines, the usable value of that information need not increase monotonically. It can be low
early because the future is poorly known, peak at an intermediate stage, and
decline again even while the environmental signal becomes more informative
because too little can still be changed. Two interacting organisms exposed to the same environmental
information can then optimally commit at different times solely because their
response opportunities disappear at different rates.

This leads to one ecological question: **what determines whether a
forecastable seasonal environment is converted into phenological adjustment?** We
treat the problem as a sequence. Before commitment, environmental structure can
reduce uncertainty about a future seasonal target. For that statistical value
to matter biologically, organisms must encounter or infer relevant information
and retain actions capable of altering residual timing error.

We develop this sequence in a reduced information–control model. We then use a
prospectively specified multi-species bird analysis to quantify temporal change
in cross-site environmental coupling, followed by explicitly posthoc
cross-validation and temporal-order audits that place the environmental signal
on decision-loss and calendar-time scales. Finally, we use individual-level
mule-deer data as an independent natural anchor for the downstream correction
layer.

Our central claim is that **environmental forecastability, biological access
to information, and realized adjustment are distinct stages of seasonal
tracking**. Standardized coupling
alone cannot rank forecast value, and even a valuable, temporally leading
environmental signal does not by itself establish cue use or correction.

---

## 2. Theory

### 2.1 Environmental forecastability is not organismal information

Let G_E(t) denote the expected reduction in prediction or decision loss
available to an ideal observer using a declared set of external environmental
variables. Let G_O(t) denote the corresponding reduction available to the
organism from information it can actually encounter or infer at stage t.

If the organism's information set is a subset of the ideal observer's set,
standard value-of-information monotonicity implies

[
0 <= G_O(t) <= G_E(t).
]

This inequality is established decision theory, not a new theorem, and assumes
the same loss function and that a decision maker receiving extra information is
free to ignore it. Its ecological role is to prevent analyst forecastability
from being silently relabelled as biological information.

The empirical cross-validation quantity used below is deliberately not
identified with this population value-of-information object. A finite-sample,
restricted source-informed forecasting model can predict worse than the
baseline and therefore produce a negative G_CV. We treat G_CV as an
**operational forecast-value proxy** for a declared model comparison, not as a
nonnegative theoretical value of information.

Figure 1 summarizes the resulting hierarchy from external forecastability to
organismal information access, retained actionability and downstream
correction.

Now let r(t) ∈ [0,1] denote retained actionability: the fraction of the fully
informed state-contingent response that remains implementable. Let C(t) be the
direct cost of waiting. We use the reduced form

[
N(t)=r(t)G_O(t)-C(t).
]

The multiplicative term r(t)G_O(t) is a transparent scalar specialization, not
a general identity for arbitrary action sets. Its purpose is to expose the
seasonal trade-off between accessible decision-relevant information and losing
response options.

An interior optimum satisfies

[
rG_O'=-r'G_O+C'.
]

Thus accessible information should be used where its marginal gain in
decision value is balanced by the loss of response opportunity and the direct
cost of waiting.

The environmental forecastability layer can be placed on a decision-loss
scale. For a Gaussian timing target Y and an analyst-observed environmental
predictor X under optimal linear prediction and squared loss,

[
R0=sigma_Y^2,
]

[
R1=sigma_Y^2(1-rho^2),
]

and

[
G=sigma_Y^2 rho^2.
]

Here R0 is baseline variance without the predictor, R1 is residual prediction
risk, and G_E is the variance reduction attributable to the predictor.
Increasing rho can therefore increase ideal-observer forecast value while
residual absolute uncertainty also increases if sigma_Y^2 grows sufficiently. Correlation,
forecast error, and information value need not have the same ordering.

The earlier binary seasonal-decision model is a special case for organismally
accessible information. Above the cue-action threshold, let

[
G_O(t)=S q(t)-B.
]

For an improving information trajectory

[
q(t)=q_0+Delta q[1-exp(-alpha t)]
]

and declining actionability

[
r(t)=exp(-beta t),
]

with no additional waiting cost,

[
N(t)=S Delta q exp(-beta t)[1-exp(-alpha t)].
]

This has a unique maximum at

[
t^*=log(1+alpha/beta)/alpha.
]

Faster actionability loss moves the optimum earlier. With a positive effective
deadline cost, information can be worth using only within a finite interval
t_- < t < t_+ even while q(t) continues to improve. Early in a seasonal
trajectory, the future can be too poorly known; late in the trajectory, the
future can be well known but too little remains changeable.

Generic value of information, cue–timing loss models,
feedforward/feedback control, and optimal stopping are established ideas. The
specific contribution sought here is narrower: connect a time-varying
decision-scale forecast value to declining biological actionability and then to
explicit post-entry phase correction, while testing the environmental
forecast-value component in a multi-species migration system.

### 2.2 Departure error need not become arrival error

Commitment does not necessarily end seasonal adjustment. A migrant can alter
speed, stopover duration or route after departure; other organisms can retain
different degrees of post-entry plasticity.

Let (e_t) be signed phase error relative to the local seasonal optimum.
Positive values denote a trajectory that is late and negative values one that
is early. Let (u_t) be the signed timing correction enacted at stage (t).
A minimal phase equation is

[
e_{t+1}
=
φ_t(e_t-u_t)+w_t,
]

where (φ_t) is passive phase retention and (w_t) is change in the
seasonal target between stages.

If the organism estimates current phase with effective information weight
(K_t) and enacts a fraction (h_t) of the indicated correction, write

[
u_t=h_tK_te_t.
]

Then, in the no-innovation local reduction,

[
e_{t+1}
=
λ_t e_t,
]

with

[
λ_t
=
φ_t(1-h_tK_t).
]

This decomposition makes the information–actionability distinction explicit
after commitment. The same observed phase retention can arise from poor phase
information, limited remaining opportunity, weak behavioral gain or strong
passive carry-over. Consequently, phase retention is an empirical coordinate,
not a direct estimate of any one mechanism.

The downstream controller also explains why raw departure delay need not rank
the biological severity of a deadline. If a delay (delta) can be partly
recovered by a later correction (c), the effective cost can be written

[
D_eff(delta)
=
J(delta)
+
min_c{K(c)+M(delta-c)},
]

where (J) is the direct nonrecoverable cost of waiting, (K(c)) the cost of
compensation and (M) the loss from residual phase error. Two migrants with
the same departure delay can therefore face very different effective
deadlines, and a migrant that departs later can still suffer less residual
timing loss if downstream recourse is larger.

### 2.3 Entry timing and downstream correction are separable

Seasonal trajectories can contain at least two mechanistically different
timing layers. A developmental or physiological process can determine when a
focal behavioral mode becomes available, whereas a later decision process can
map signed ecological error onto movement, waiting or other timing adjustments.

Represent entry by an internal state z_i(t) and threshold Theta_i,

[
tau_i = inf{t : z_i(t) >= Theta_i}.
]

The actor enters the focal trajectory at time tau_i with phase error e_(i,0).
After entry, it can repeatedly estimate ecological phase and use whatever
response options remain:

[
become ready
→
enter with e_0
→
observe
→
correct
→
observe again.
]

The distinction does not require physiology to disappear after entry. It only
requires that the process setting entry timing need not be identical to the
process mapping later ecological error onto correction. This separation makes
it possible for two organisms to have similar departure or onset dates but very
different downstream ability to repair error, or conversely to start at
different times yet converge later.

---

## 3. Methods

### 3.1 Migratory-bird environmental analysis

We used the public `final.rds` dataset from Amaral et al. (2025), fixed to
repository commit `62c58d77c2028bd863dfe3697b0d9cf29ceaeab0`. The analysis
period was divided prospectively into 2002–2009 and 2010–2017. For each
breeding-range target cell, we selected the nearest lower-latitude
migratory-range cell for the same species as the nonlocal environmental source,
following the operational range-flag semantics used in the source analysis
code. A source–target mapping was admitted when at least six years of finite
green-up observations were shared in both periods.

For the prospectively specified primary environmental analysis, source and
target mid-green-up dates were detrended separately against year within each
period. Pearson correlation was then calculated between the paired residual
anomalies. The primary estimand was the late-minus-early change in correlation
for each unique spatial source–target pair. The admitted primary sample
contained 166 unique spatial pairs used by 28 species. Uncertainty was estimated
with 10,000 bootstrap replicates over unique spatial pairs. Dependence
sensitivities clustered or resampled source cells, target cells, two-way
source–target structure, 5-degree and 10-degree spatial blocks, and global
calendar-year omissions; equal-species weighting and alternative window
definitions were also examined.

### 3.2 Posthoc forecastability and observability diagnostics

All analyses in this subsection were designed after the primary correlation
outcome was known and are treated as posthoc diagnostics. We first quantified
the day-scale target anomaly standard deviation, source-to-target regression
slope, explained variance and fitted residual error within each period.

We then evaluated held-out prediction with leave-one-year-out
cross-validation. For each held-out year, source and target linear trends were
estimated on the remaining years. A target-history-only forecast used the
target trend. The source-informed forecast additionally regressed detrended
target anomalies on detrended source anomalies in the training years and added
the predicted anomaly to the held-out target trend. We summarized the marginal
forecast value of the reconstructed source predictor as

[
G_CV
=
MSE(target-history only)
-
MSE(source-informed forecast).
]

Because these are estimated restricted forecasting models, G_CV can be
negative and is not identified with a nonnegative theoretical value of
information. We examined robustness to a target-climatology baseline, exact
8/8-year windows, global calendar-year omission, equal-species weighting, and
the first three nearest lower-latitude source ranks.

We separately audited temporal ordering. In the broader bird sample we compared
the reconstructed source mid-green-up date with target arrival. For a stricter
stagewise analysis, we required at least six annual arrival estimates at both
mapped source and target cells in both periods, yielding 56
species-source-target units, 31 unique spatial pairs and 14 species. Within this
subset we classified each annual source mid-green-up event as occurring before
source-front arrival, between source- and target-front arrival, or after
target-front arrival. This ordering analysis assesses whether the reconstructed
environmental event could have been online at the mapped stage; it does not
establish individual routes, perception or cue use.

### 3.3 Bird timing and stagewise phase geometry

To restore direction lost by absolute mismatch, we defined signed timing as

[
e = arrival - local\ mid\!\text{-}\!greenup.
]

Positive values indicate arrival after local mid-green-up and negative values
arrival before it. In the transfer sample, period means were estimated for
arrival date, target green-up, signed lag and absolute lag for 150
species-target rows, 72 unique spatial pairs and 22 species. Unique-pair
bootstraps preserved all species rows attached to each sampled environmental
pair; equal-species summaries were reported as sensitivities.

The same restricted 31-pair/14-species stage subset was used to describe
population-front phase transformation between mapped source and target cells:

[
\Delta e_{route}
=
e_{target}
-
e_{source}.
]

We decomposed this quantity into the source-to-target population-front interval
and the corresponding green-up interval. This is population-level geometry,
not an individual feedback estimator. Because reported arrival posterior
uncertainty differed strongly between periods, we propagated the published
arrival posterior standard deviations through 5,000 independent-Normal Monte
Carlo draws and also performed an inverse-variance weighted sensitivity. Raw
source-to-target phase-retention regressions were excluded from mechanistic
interpretation after an errors-in-variables audit showed that the early-period
latent slope was not identifiable under the reported predictor uncertainty.

To test whether environmental forecastability was associated with realized bird
timing, we related change in G_CV to change in absolute and log-transformed
arrival–green-up mismatch using equal total weight per species. A fixed-arrival
structural null held each species-target arrival date at its 2002–2017 mean
while allowing green-up to vary, and 2,000 within-period arrival permutations
destroyed year-specific bird–environment alignment while preserving each
period's arrival distribution.

### 3.4 Mule-deer phase correction

For the downstream-correction anchor, we reanalysed the public source-data
workbook accompanying Ortega et al. (2023). The paired phase table contained
152 animal-years from 72 adult female mule deer with signed Days-From-Peak at
migration start and end. We summarized phase variance contraction, the
whole-route start-to-end phase slope, the fraction of animal-years ending closer
to peak green-up, and mean absolute phase error.

A matched actuator table provided movement rate and stopover duration. We
estimated descriptive linear associations of starting signed phase with each
actuator and repeated the slopes after centering predictor and response within
year. Uncertainty was obtained with 10,000 cluster-bootstrap resamples of
individual animals. The phenomenon of bidirectional compensation and
resynchronization is prior work from Ortega et al.; our reanalysis places it on
the continuous signed-phase scale used by the present framework.

As a secondary channel-separation analysis, we used the subset with March body
fat information and migration beginning after 31 March so that the
physiological measurement preceded departure. We examined migration-start
timing versus standardized body fat and downstream actuator models containing
both body fat and starting ecological phase. These analyses are descriptive and
do not identify causal independence between physiological readiness and
downstream control.

### 3.5 Evidence status

The source–destination correlation contrast and its outcome-opening rules were
specified before the primary outcome was examined. The day-scale forecast
decomposition, G_CV, source-rank and baseline sensitivities, observability
audit, signed timing decomposition, forecast-value transfer analysis and
stagewise population-front analyses are explicitly posthoc. The theoretical
results are exact only for their declared reduced models. Throughout, we
separate preregistered evidence, posthoc diagnostics, published prior phenomena
and prospective predictions rather than reclassifying later analyses as
confirmatory.

---

## 4. Natural evidence

### 4.1 Environmental forecastability increased while bird arrival changed little

We first tested a prespecified environmental hypothesis in the eastern North
American migratory-bird dataset of Amaral et al. (2025). Each breeding-range
target cell was paired with the nearest lower-latitude migratory-range source
cell for the same species. Source and target green-up were detrended separately
within 2002–2009 and 2010–2017, and the preregistered environmental coordinate
was the Pearson correlation of annual residual anomalies.

A posthoc temporal-order audit confirmed that the environmental source was
usually earlier in calendar time as well as lower in latitude. Mean
source-to-target green-up lead was about **13.4 d**, and **158/166 (95.2%)**
pairs had positive mean source lead in both windows. The source can therefore be described as a target-preceding environmental
predictor, not as a cue known to have been encountered or perceived by birds.

The registered degradation prediction was not supported. Across 166 unique
source–destination pairs used by 28 species, mean detrended correlation
increased from

[
rho_early=0.284
]

to

[
rho_late=0.653,
]

giving mean delta-rho = +0.369. The pair-bootstrap 95% interval was +0.298 to
+0.436, and 26 of 28 species means were positive. The direction remained
positive under source-cell and target-cell clustering, two-way source–target
dependence, 5-degree and 10-degree spatial blocking, and global
leave-one-calendar-year-out analyses.

Because correlation is scale invariant, we subsequently performed an explicitly
posthoc metric-scale diagnostic. Destination green-up anomalies became much
more variable: mean target residual SD increased from **2.41 d to 4.66 d**
(change +2.25 d; pair-bootstrap 95% CI +1.95 to +2.55), with positive source-,
target-, and spatial-block intervals. Mean in-window R-squared increased from
**0.290 to 0.572**, and mean source-to-target slope increased from **0.399 to
0.640**.

We then evaluated held-out prediction. Source-informed leave-one-year-out RMSE
was essentially unchanged (**4.11 to 4.17 d**; change +0.055 d, 95% CI -0.59
to +0.63), whereas a target-history-only forecast worsened from **3.18 to 5.86
d** (change +2.68 d, 95% CI +2.34 to +3.01).

To place the environmental signal on the same squared-loss scale as the reduced
theory, we defined a posthoc **cross-validated forecast-value proxy**,

[
G_CV = MSE(no source) - MSE(source informed).
]

This is an environmental forecast value, not an organismal fitness value of
information. Mean G_CV changed from **-16.1 d^2 to +16.0 d^2**, a
late-minus-early increase of **+32.1 d^2**. The increase was widespread:
median delta G_CV was **+15.84 d^2**, the 10% trimmed mean was **+20.87 d^2**,
and **139/166 (83.7%)** spatial pairs were positive. Equal-species weighting
gave a change of **+20.87 d^2** with **25/28 species** positive. A
climatological-mean no-source baseline still gave a pair-mean increase of
**+22.37 d^2**, and the exact 8/8-year subset retained a **+28.30 d^2**
increase. In that subset, omission of every calendar year left all 16 mean
increases and all 16 bootstrap intervals positive.

The forecast-value increase was not unique to the frozen nearest-source choice.
On a common 223-row, 22-species sample, the first-, second- and third-nearest
lower-latitude sources all showed positive mean increases in G_CV (+37.2,
+33.5 and +29.1 d^2, respectively). The nearest-versus-third-nearest
equal-species contrast was +10.68 d^2 (95% CI +2.46 to +18.96), whereas the
nearest-versus-second contrast remained unresolved. We therefore interpret the
result as regional nonlocal forecast structure, not a uniquely identified cue
site.

That distinction matters because the predictor is reconstructed retrospectively.
In the restricted 31-pair/14-species stage subset, source mid-green-up occurred
before the population front reached the source cell in only **29.8%** of annual
observations in the early window and **45.8%** in the late window. It occurred
after target-front arrival in **41.6%** and **36.1%** of annual observations,
respectively. On average, source mid-green-up fell 4.21 d after source-front
arrival and 2.18 d before target-front arrival early, and 0.70 d after source
arrival and 3.83 d before target arrival late. Thus G_CV quantifies
ideal-observer forecastability of environmental structure, not an online cue
known to have been available to the birds.

The realized source event also occurred earlier relative to target arrival. In
the admitted bird sample, mean source-mid-green-up-to-arrival lead widened from
**5.47 to 7.95 d** (change **+2.48 d**, 95% CI +1.91 to +3.05), with
source-cell, target-cell, 5-degree and 10-degree intervals all positive. Equal
species weighting gave a **+2.37 d** change, and 21 of 22 species showed a
positive change. The wider lead arose primarily because source green-up
advanced by about **2.86 d**, whereas estimated bird arrival advanced by only
about **0.38 d** in that subset.

Restoring the sign of arrival relative to the target green-up revealed the
biological consequence more clearly. Across the 150 species-target rows of the
transfer sample, target green-up advanced by **2.31 d** (95% CI 2.08 to 2.58 d
earlier), whereas estimated bird arrival changed by only **0.19 d** (95% CI
-0.95 to +0.52 d). Signed lag, defined as arrival minus target green-up, shifted
from **-7.81 to -5.69 d**, a **+2.12 d** change (95% CI +1.41 to +2.77).
Equal-species weighting gave a +2.14 d change, and 20 of 22 species were
positive. Birds therefore became less early relative to mid-green-up because
the environmental target advanced while the estimated arrival schedule changed
little.

A restricted same-system stage analysis provided a population-level bridge
between environmental opportunity and downstream timing. Among **31
source–target pairs from 14 species** with at least six annual arrival estimates
at both mapped cells in both periods, the estimated migration front generally
reached the source first. The source-to-target front interval shortened from
**7.20 to 5.69 d** (change -1.51 d, 95% CI -2.32 to -0.70), whereas the
source-to-target green-up interval changed little. Consequently the
source-to-target phase transformation became more negative, from **-3.57 to
-4.95 d** (change -1.37 d, 95% CI -2.36 to -0.36); 23/31 pairs and 12/14
species changed in that direction. This shows that population-level relative
timing was transformed across migration stages rather than passively copied
from source to target. It does not identify individual feedback. The subset is
restricted, arrival posterior precision was much poorer in the early period,
and inverse-variance reweighting weakened the contrast to an interval spanning
zero, although posterior-normal propagation of the reported arrival
uncertainty retained a negative mean change in all 5,000 simulations.

This signed decomposition also changes the interpretation of the absolute
mismatch metric. Absolute arrival–green-up distance changed only modestly
(8.42 to 8.07 d unweighted; 9.04 to 8.42 d under equal-species weighting), but
that stability is not evidence of active tracking. Because birds were several
days earlier than mid-green-up in both periods, an advancing green-up moved
toward the largely unchanged arrival schedule.

Finally, larger route-level gains in forecast value did not produce a detected
bird-specific improvement. The posthoc delta-G_CV transfer had a raw positive
day-scale coefficient of +2.43 d per SD, but a fixed-arrival environmental null
produced +2.98 d. The observed-minus-null bird increment was -0.56 d (95% CI
-2.39 to +0.55), and within-window arrival permutations reproduced the raw
positive slope.

The licensed conclusion is therefore asymmetric but clear:

> **The reconstructed environment became more forecastable to an ideal
> observer while the estimated population arrival schedule remained
> comparatively rigid.**

These analyses establish changing environmental forecastability, not
organismal information access or cue use. The range-based source cells are environmental proxies, and the
data do not show that individuals passed through, perceived, learned, or acted
on the fitted source signal.

### 4.2 Mule deer provide an individual-level phase-correction anchor

Red Desert mule deer provide a complementary system because individuals begin
migration with large signed differences relative to the local green wave and
can alter their trajectories en route. Ortega et al. (2023) established that
early and late migrants resynchronize by changing movement speed and stopover
use. We use the public source data to quantify that published phenomenon on
the continuous phase scale required by the model.

Across 152 animal-years from 72 adult females, the standard deviation of signed
Days-From-Peak phase declined from 26.41 d at migration start to 13.17 d at
migration end. The end/start variance ratio was

[
0.249
]

with a 95% animal-cluster bootstrap interval of 0.167–0.362. After removing
year-specific start and end means, the ratio remained 0.294 (95% CI
0.206–0.405).

The whole-route phase-retention slope was

[
λ = 0.107
]

with 95% animal-cluster bootstrap CI 0.013–0.209. Of 152 animal-years, 107
(70.4%) ended closer to peak green-up than they started, and mean absolute phase
error declined from 21.91 d to 11.12 d.

The same source table shows the expected signed actuator geometry. Each
additional day of positive start-phase error was associated descriptively with
+0.0683 km d(^{-1}) higher movement rate (95% animal-cluster bootstrap
+0.0554 to +0.0800) and -0.492 d of stopover use (95% CI -0.569 to -0.412).
After centering within year, the corresponding slopes remained +0.0852 and
-0.614, with both intervals excluding zero. Late individuals therefore moved
faster and stopped less, whereas early individuals showed the opposite
adjustment.

We also examined whether a predeparture physiological state and downstream
phase carried separable signals. Of 93 animal-years with IFBFat and migration
timing, 62 animal-years from 40 deer began after 31 March, ensuring that March
IFBFat preceded departure. In that temporally conservative subset, IFBFat was
associated with migration-start timing (-3.97 d per standardized unit;
animal-cluster 95% CI -6.31 to -0.69), although a year-fixed-effect sensitivity
crossed zero.

Within the same safe subset, models including both IFBFat and signed starting
phase retained associations of phase with movement rate (+0.0742, 95% CI
+0.0387 to +0.1028) and stopover duration (-0.234, 95% CI -0.429 to -0.0095),
whereas IFBFat intervals spanned zero in both downstream models.

The mule-deer data therefore provide a candidate same-population
timer–controller anchor: predeparture condition is associated with when
migration begins, while ecological phase is associated with how migration is
subsequently paced. Figure 3 summarizes the individual-level phase contraction and signed
actuator responses. The evidence does not establish causal independence,
identify nutritional condition with a unique physiological readiness variable,
or separately estimate information weight, opportunity, behavioral gain,
passive retention and process noise.

---

## 5. Discussion

### 5.1 Forecastability is not biological information

The bird analysis separates quantities that are often compressed into the word
predictability. Earlier migration studies already distinguished correlation,
proportionality, environmental variability, information availability and cue
use (McNamara et al. 2011; Shaw and Couzin 2013; Kölzsch et al. 2015), and
increasing spatial synchrony of spring phenology is itself established (Koenig
and Liebhold 2016; Liu et al. 2019). Our contribution is narrower: within the
same sampled source–destination network, destination variability increased,
nonlocal forecast value increased, and the environmental signal became earlier
relative to arrival, yet population arrival timing changed little.

The forecasting problem therefore contains at least three distinct quantities.
Standardized coupling asks how strongly anomalies covary. Forecast value asks how much held-out prediction loss is removed by adding the
nonlocal predictor. Temporal ordering asks whether the reconstructed
environmental event precedes the focal outcome. Neither temporal ordering nor
forecast value establishes that an organism actually encountered or inferred
that information.

That distinction is visible here. The reconstructed source predictor gained substantial marginal forecast value
and its realized event moved earlier relative to target arrival, so the absence
of a route-level transfer cannot be attributed simply to weaker spatial
predictive structure.
Yet target green-up advanced by about 2.3 d while estimated arrival changed
little. This is consistent with the original Amaral et al. (2025) result that
migration speed responds to green-up but does not fully compensate for
phenological change.

The missing step lies between environmental opportunity and realized
adjustment. Individuals must encounter or infer the relevant signal, integrate
it with other cues and internal state, and retain an actuator capable of
changing timing. In the reduced framework, the sequence is

[
environmental forecastability
→
organismal accessibility / inference
→
retained correction opportunity
→
realized adjustment.
]

The first quantity describes the external forecasting problem. The remaining
stages describe organismal information access, use and control. The bird data identify external forecastability and population-level timing
geometry, but not organismal information access, the internal decision process,
or correction capacity.

### 5.2 Seasonal trajectories, not endpoint dates, reveal control

The mule-deer result illustrates why final timing alone is insufficient.
Individuals begin migration across a broad signed range around peak green-up,
yet the phase distribution contracts strongly en route. The sign of initial
phase predicts the direction of later speed and stopover adjustment.

An endpoint-only analysis could describe the resulting arrival distribution as
precise phenology without revealing whether precision arose from accurate
initial timing or from strong downstream correction. Conversely, an analysis
of departure timing alone could classify early or late starts as mismatch even
when later stages substantially repair that error.

The empirically useful unit is therefore a transition:

[
e_in
→
available information
→
actuator response
→
e_out.
]

Repeated transitions can estimate how much phase error is retained and where
along the trajectory correction occurs. They can also distinguish a system
with accurate entry and weak downstream recourse from one with imprecise entry
but strong correction, even when both end at the same date.

### 5.3 The strongest prediction is an intermediate information-use window

The most distinctive empirical prediction is not simply that later cues are
better or that constraints matter. It is that cue responsiveness should peak
at an intermediate stage when independently measured **organismally accessible
information value** and remaining actionability move in opposite directions.

A direct test requires at least three ordered stages of the same decision
problem. At each stage, investigators should estimate independently:

1. the external environmental variables that are forecastable at that stage;
2. which of those variables the organism can actually encounter or infer;
3. loss with and without that accessible information, and therefore G_O(t);
4. the remaining set or value of feasible timing responses r(t);
5. the behavioral response to the cue on a common scale.

The focal comparison is then between models based on standardized coupling,
forecast error or G_O(t) alone and a model that allows G_O(t) to be discounted
by remaining actionability. The strongest support would be a reproducible
entry–peak–exit pattern in cue use while raw cue accuracy or correlation
continues to improve.

Recent GPS work on spring-departing Brent geese provides a useful boundary
case: the effect of tailwind assistance on departure was strongest early in the
season and weakened to near unity late in the departure window as migratory
urgency increased (Theurich et al. 2026). That result is consistent with
late-stage loss of cue selectivity, but it does not test the predicted hump
because future-state information quality and retained actionability were not
independently measured across the same stages.

Migration is a particularly useful system because departure, route choice,
stopover departure, speed, settlement and breeding provide repeated decisions.
But the logic is broader. Flowering, emergence, reproduction, diapause and
other seasonal transitions differ in how information accumulates and how
quickly commitment removes later options.

### 5.4 Limits

The bird source–destination links are range-based spatial proxies, not tracked
individual routes. Although source green-up preceded target green-up by about 13 d on average, the
realized source mid-green-up event was not consistently available before the
population front reached the mapped cells. In the restricted stage subset,
source mid-green-up occurred before source-front arrival in only 29.8% of
annual observations early and 45.8% late, and after target-front arrival in
41.6% and 36.1%, respectively. The mapping therefore quantifies retrospective
environmental forecastability, not a cue demonstrated to be available,
perceived or learned by birds. Likewise, G_CV is the marginal held-out predictive value of adding that
reconstructed environmental variable to a declared analyst forecast. Because
it compares estimated, restricted forecasting models, G_CV can be negative and
is not identical to the nonnegative population value of information G_E. It is
an operational forecastability proxy, not organismally accessible information
and not the expected fitness value of information to an organism.

The increase in standardized coupling is the preregistered result. The
day-scale forecast decomposition, cross-validated forecast value, temporal-order
audits, signed timing decomposition and stagewise analyses were constructed
after that outcome was known and are therefore explicitly posthoc. They reveal
structure hidden by rho but cannot be relabelled as confirmatory. The analysis
also does not identify anthropogenic climate change as the cause of any
two-window difference.

The stagewise bird bridge is also restricted to 31 source–target pairs from
14 species with sufficiently complete arrival estimates at both stages. This
subset is selected toward shorter source–target distances (mean 495 versus
911 km outside the subset) and stronger late environmental coupling (mean rho
0.847 versus 0.608), although its increase in cross-validated forecast value is
similar to the excluded pairs. Arrival posterior SD was substantially larger in
the early period. Propagating
the reported posterior uncertainty around the arrival means retained a negative
late-minus-early phase-transformation change in all 5,000 simulations, but an
inverse-variance weighted sensitivity retained a negative point estimate with a
95% interval spanning zero. Exploratory source-to-target phase-retention
regressions were not interpreted mechanistically: in the early period the
reported source-arrival uncertainty exceeds the residual source-phase variance
needed to identify a classical errors-in-variables corrected slope, and in the
late period the corrected slope is approximately the fixed-arrival
environmental null. The stagewise result is therefore supporting
population-level geometry, not a measurement-error-invariant causal estimate.

The modest stability of absolute arrival–green-up distance should not be read
as successful active tracking. Signed timing shows that target green-up
advanced by about 2.3 d while estimated arrival changed little, so the
environmental target moved toward an arrival schedule that was already several
days early relative to mid-green-up. The arrival estimates describe a
population migration front rather than tracked individual decisions. Other
cues, route changes, selection, population turnover and unmeasured behavioral
adjustments remain possible.

The mule-deer analyses independently establish phase convergence and signed
downstream adjustment, but they do not estimate the bird mechanism and do not
jointly identify G_O(t) and r(t). The association of predeparture nutritional
condition with migration start is also sensitive to a year-fixed-effect
specification and should be treated as a candidate entry-timing signal rather
than a fully identified physiological timer.

The evidence is therefore layered rather than causal across systems. The bird analysis demonstrates that standardized coupling, absolute
environmental variability and ideal-observer forecastability can move
differently through time. The theory then inserts an organismal-access layer
before retained actionability. The mule-deer system establishes that signed
post-entry correction is biologically real. A direct natural test of the full
architecture still requires accessible information value G_O(t), r(t) and
behavior to be measured along the same seasonal trajectory.

---

## 6. Conclusion

Environmental forecastability and phenological adjustment are not the same
thing. In the sampled eastern North American bird system, destination spring
became more variable while reconstructed nonlocal environmental structure
gained substantial cross-validated forecast value. Yet target green-up advanced by about 2.3 d while
estimated bird arrival changed little, and larger route-level gains in forecast
value did not produce detectable bird-specific improvement beyond structural
nulls.

The bird result therefore identifies an unresolved conversion chain rather
than a simple shortage of environmental predictive structure. A predictor can be
statistically valuable and target-preceding without being known to have been
encountered, perceived, integrated or translated into a timing response. In the restricted same-species stage subset, population-level relative timing
was nevertheless transformed between source and target rather than passively
retained, providing a same-system bridge from external forecast structure to
downstream timing without identifying individual feedback.

Mule-deer trajectories illustrate the individual-level downstream side of this
problem.
Individuals entering migration at different signed phases alter movement speed
and stopover use in opposite directions and strongly compress phase variation
before the end of migration. Forecasting future conditions and correcting
residual error after commitment are therefore distinct routes through which
seasonal timing can change.

The resulting framework replaces a single predictability or phenological
response coefficient with a sequence:

[
environmental forecastability
→
organismal information access
→
retained actionability
→
phase re-estimation
→
correction.
]

The central comparative question is therefore **not only how informative the
environment is, but whether organisms can access that information in time and
still convert it into correction**.


---

## Literature Cited

Amaral, B. R., C. Youngflesh, M. W. Tingley, and D. A. W. Miller. 2025.
Shifting gears in a shifting climate: birds adjust migration speed in response
to spring vegetation green-up. Diversity and Distributions 31:e70033.
doi:10.1111/ddi.70033.

Bauer, S., J. M. McNamara, and Z. Barta. 2020. Environmental variability,
reliability of information and the timing of migration. Proceedings of the
Royal Society B 287:20200622. doi:10.1098/rspb.2020.0622.

Ortega, A. C., E. O. Aikens, J. A. Merkle, K. L. Monteith, and M. J. Kauffman.
2023. Migrating mule deer compensate en route for phenological mismatches.
Nature Communications 14:2008. doi:10.1038/s41467-023-37750-z.

Theurich, N., S. Garthe, F. Jiguet, P. Bocher, and P. Schwemmer. 2026.
Departing with the wind: spring migration timing in Brent geese from their most
important staging and wintering site, the Wadden Sea World Heritage Site.
Ecology and Evolution 16:e74119. doi:10.1002/ece3.74119.

Kölzsch, A., G. J. D. M. Müskens, H. Kruckenberg, P. Glazov, R. Weinzierl,
B. A. Nolet, and M. Wikelski. 2015. Forecasting spring from afar? Timing of
migration and predictability of phenology along different migration routes of
an avian herbivore. Journal of Animal Ecology 84:272–283.
doi:10.1111/1365-2656.12281.

Bernhardt, J. R., M. I. O'Connor, J. M. Sunday, and A. Gonzalez. 2020. Life in
fluctuating environments. Philosophical Transactions of the Royal Society B
375:20190454. doi:10.1098/rstb.2019.0454.


Koenig, W. D., and A. M. Liebhold. 2016. Temporally increasing spatial
synchrony of North American temperature and bird populations. Nature Climate
Change 6:614–617. doi:10.1038/nclimate2933.

Liu, Q., S. Piao, Y. H. Fu, M. Gao, J. Peñuelas, and I. A. Janssens. 2019.
Climatic warming increases spatial synchrony in spring vegetation phenology
across the Northern Hemisphere. Geophysical Research Letters 46:1641–1650.
doi:10.1029/2018GL081370.


McNamara, J. M., Z. Barta, M. Klaassen, and S. Bauer. 2011. Cues and the
optimal timing of activities under environmental changes. Ecology Letters
14:1183–1190. doi:10.1111/j.1461-0248.2011.01686.x.

Usinowicz, J., and M. I. O'Connor. 2023. The fitness value of ecological
information in a variable world. Ecology Letters 26:621–639.
doi:10.1111/ele.14166.


Robertson, E. P., F. A. La Sorte, J. D. Mays, P. J. Taillie, O. J. Robinson,
R. J. Ansley, T. J. O'Connell, C. A. Davis, and S. R. Loss. 2024. Decoupling
of bird migration from the changing phenology of spring green-up. Proceedings
of the National Academy of Sciences USA 121:e2308433121.
doi:10.1073/pnas.2308433121.


Shaw, A. K., and I. D. Couzin. 2013. Migration or residency? The evolution of
movement behavior and information usage in seasonal environments. The American
Naturalist 181:114–124. doi:10.1086/668600.
