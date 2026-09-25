# Temporal buffering delays but does not replace spatial tracking under environmental change

**Status:** integrated ecology manuscript v1, PREOUTCOME  
**Publication architecture:** combines the frozen synthetic tracking-theory programme with the movement–phenology macroecological programme; the exact anti-phase optimum theorem remains a separate PAYOFF-B1 paper.  
**Evidence boundary:** all synthetic quantitative claims are inherited from frozen 2026-09-20 tracking outputs; all empirical claims are inherited from registered and source-faithful receipts already on main. The preregistered Aikens industrial-development lambda outcome remains unopened.

## Abstract

Organisms can track changing environments by moving through space or adjusting seasonal timing, but whether temporal adjustment can replace movement under sustained change is unresolved. We combine theory, moving-landscape simulations and migration data to test temporal buffering of spatial tracking demand. A local controller provides an exact substitution null, whereas explicit landscapes show that finite phenological capacity expands persistence and reduces sampled fragmentation costs before movement re-enters under stronger directional forcing. Across 5,816 observations from 55 migratory bird species, one portable movement-speed/environmental-wave-speed optimum is not supported. We then tested temporal substitution directly with a response-blind chronological split: 2002–2009 estimated species timing responsiveness and 2010–2017 formed the holdout. Among 39 species and 3,268 holdout observations, stronger historical timing responsiveness did not flatten the later mismatch-versus-speed curve; the registered quadratic interaction was opposite-signed (+0.035 ± 0.029, p=0.225). In the same frozen model, timing responsiveness was associated with lower average holdout mismatch (secondary descriptive effect −0.300 ± 0.105), so better timing did not make movement-speed dependence dispensable. Direct reconstructions in mule deer, barnacle geese and Eurasian wigeon likewise show phase correction through different actuator architectures and ecological intervals.
<!-- AIKENS_LAMBDA_ABSTRACT_START -->
[AIKENS LAMBDA ABSTRACT PENDING — outcome-blind renderer insertion only.]
<!-- AIKENS_LAMBDA_ABSTRACT_END -->
Together, these results identify temporal adjustment as a buffer rather than a substitute for spatial tracking. Low mismatch can therefore conceal continued dependence on movement and movement-permitting landscapes.

**Keywords:** environmental tracking; phenological mismatch; migration; movement ecology; climate change; phase retention; habitat fragmentation; behavioral plasticity

---

## 1. Introduction

Organisms exposed to changing environments can respond by moving through space, changing seasonal timing, altering behavior, or combining these responses (Hällfors et al. 2021; Fredston et al. 2025). Yet many ecological analyses compress this multidimensional process into a single endpoint: the difference between where or when an organism occurs and where or when conditions are favorable.

That endpoint is important, but it is not a mechanism. Phenological-mismatch research already emphasizes that apparent alignment can be buffered and that theory and observed mismatch are not interchangeable descriptions of process (Kharouba & Wolkovich 2020; Weir & Phillimore 2024). A small mismatch may reflect weak environmental forcing, high predictability, strong behavioral correction, large movement effort, substantial phenological adjustment, or several of these at once. Conversely, similar mismatch in two populations need not mean that they have similar capacity to continue tracking future change.

The central ecological question is therefore not only how small mismatch becomes, but **how long temporal adjustment can postpone the need for spatial tracking**. Movement must be realized through landscapes and corridors, whereas phenological adjustment has finite seasonal range. A population can therefore remain well aligned while using timing to defer movement, even as the spatial response required under continued environmental displacement is pushed into the future. We refer to that deferred requirement descriptively as **latent spatial tracking demand**. Behavioral information and interaction partners can further determine whether the required reallocation remains accessible.

PAYOFF-B begins from an intentionally simple benchmark. In a symmetric two-patch environment with exact anti-phase seasonal switching, a constant migration rate has one positive long-run growth optimum and that optimum scales with the environmental switching timescale. The exact theorem is developed separately in PAYOFF-B1. Here we use that result only as a benchmark for a broader question: **can seasonal timing replace spatial tracking under sustained directional environmental change, or does it only buffer and postpone the need to move?** We then ask whether natural migration nevertheless collapses onto one portable movement-to-environment tracking rule.

We answer this in three steps.

First, we construct the strongest possible substitution null. In a local controller, movement-mediated and timing-mediated feedback enter only through their summed restoring gain. Timing can therefore absorb the same local corrective burden as movement while endpoint mismatch remains unchanged.

Second, we add the ecological constraints that turn substitution into finite buffering: bounded phenological capacity, explicit spatial redistribution, fragmented movement routes and partner matching. These models ask whether a temporal bypass merely delays spatial response, when movement must re-enter, and whether the required reallocation remains accessible.

Third, we test the corresponding one-dimensional natural prediction empirically. A registered broad analysis of 5,816 observations from 55 migratory bird species derived from Amaral et al. (2025) asks whether migration collapses onto one animal-speed/environment-speed optimum. It does not. We then test substitution itself using a fresh chronological split of the same archived dataset: early years estimate species-level timing responsiveness to green-up, and later years ask whether stronger historical timing responsiveness weakens the dependence of phase mismatch on movement speed. Finally, we use directly reconstructed mule-deer, barnacle-goose and Eurasian-wigeon systems to ask how real migrants transform phase error (Ortega et al. 2023; Kölzsch et al. 2015; van Toor et al. 2021), separating a common response coordinate from system-specific actuator mechanisms and ecological interval scales.

Our central prediction is therefore directional and mechanistic: **temporal adjustment can buffer spatial tracking demand, but it cannot replace movement indefinitely under sustained environmental change**. A true natural substitute should make later mismatch less dependent on movement speed. The split-sample test therefore provides a direct empirical attempt to falsify the substitution component while keeping the synthetic buffering mechanism and the broad speed-rule test distinct.

---

## 2. Conceptual framework

### 2.1 A common environmental-error coordinate

Let directional environmental demand be \(D_t\). A lineage can reduce error through spatial displacement \(x_t\) and phenological shift \(z_t\). With conversion factors \(g\) and \(s\), both responses can be represented in common environmental units:

\[
e_t = D_t - g x_t - s z_t.
\]

The observed mismatch \(e_t\) is therefore compatible with many combinations of spatial and temporal response.

### 2.2 The exact local substitution null

Let \(q_m\) be movement-mediated restoring feedback and \(q_h\) timing-mediated feedback. A local error controller has

\[
e_{t+1}=(1-q_m-q_h)e_t+r,
\]

where \(r\) is new forcing between updates. Only the total restoring gain

\[
K=q_m+q_h
\]

determines the local error dynamics. At this level,

\[
(q_m,q_h)=(K,0)
\]

and

\[
(q_m,q_h)=(0,K)
\]

are observationally equivalent from mismatch alone.

This is deliberately stronger than we expect in nature. It supplies a null against which ecological constraints can be added one at a time.

### 2.3 Phase and velocity are different control channels

Following the registered bird holdout readout, we use a minimal moving-front identity as a **post-readout mechanistic interpretation**, not as a preregistered prediction. Let an environmental front move as

\[
E(t)=E_0+v_E t,
\]

and let the organism's spatial front move at speed \(v_A\) with a seasonal timing shift \(z\),

\[
A(t;z)=A_0+v_A(t+z).
\]

The signed spatial mismatch is

\[
e(t;z)=(E_0-A_0)-v_A z+(v_E-v_A)t.
\]

Timing therefore changes the phase offset,

\[
\frac{\partial e}{\partial z}=-v_A,
\]

whereas movement-speed matching determines the rate at which mismatch drifts,

\[
\frac{\partial e}{\partial t}=v_E-v_A.
\]

A fixed timing shift can remove mismatch at one instant but cannot keep mismatch zero over a sustained interval when \(v_E\neq v_A\). If timing adjustment is bounded by \(|z|\le z_{\max}\), the maximum extra time it can buy before the same mismatch threshold is reached is

\[
T_{\rm buffer}=\frac{v_A z_{\max}}{|v_E-v_A|}
=\frac{u z_{\max}}{|1-u|},
\]

with \(u=v_A/v_E\). This is elementary kinematics rather than a claim of mathematical novelty. It clarifies the ecological asymmetry: timing can shift **when** a tracker meets the environmental wave, whereas movement speed determines whether it can keep pace with the wave once tracking continues.

### 2.4 Temporal buffering, latent spatial demand and three failure modes

We use **latent spatial tracking demand** descriptively to mean the spatial redistribution that becomes necessary to maintain tracking once finite temporal adjustment is exhausted; it is not a separately fitted empirical parameter. Temporal buffering can keep mismatch low while this future spatial requirement remains unexpressed. We distinguish three ways that buffer can fail.

**Capacity.** Phenological timing cannot shift indefinitely. If environmental displacement continues accumulating, temporal adjustment can delay but not permanently replace spatial redistribution.

**Geometry.** Movement must traverse actual landscapes. Two strategies producing similar endpoint mismatch can differ strongly in route cost and access to habitat.

**Coordination.** Interacting species can each track the abiotic environment while becoming mismatched with one another. A reallocation beneficial when both partners change together can be selected against when either changes alone.

These constraints yield a general expectation:

\[
\text{low current mismatch} \not\Rightarrow \text{low future spatial demand}.
\]

The same endpoint can therefore conceal different amounts of remaining temporal capacity and different exposure to spatial constraints.

### 2.5 Empirical phase retention

For a realized migration system, let \(E_i\) denote phase error entering an ecological correction interval and \(E_{i+1}\) the error after the interval. We use

\[
E_{i+1}=a+\lambda E_i+\epsilon_i.
\]

Here \(\lambda\) is a phase-retention estimator over the declared interval. Values near zero describe strong reset of incoming error, positive values below one describe partial retention, and negative values retain an overshoot/sign-reversal interpretation.

Raw \(\lambda\) is not assumed to be a universal biological rate. Different systems use different ecological intervals. Secondary interval-standardized quantities are therefore used only as comparison coordinates.

A variance decomposition separates inherited error from new forcing:

\[
V_{i+1}
=
\lambda_i^2V_i+\sigma_{\xi,i}^2+\sigma_{\eta,i}^2,
\]

where \(\sigma_{\xi,i}^2\) represents environmental innovation and \(\sigma_{\eta,i}^2\) remaining behavioral and measurement variation.

This gives an empirical counterpart to the theoretical identification problem: precise realized timing can arise from predictable forcing, strong correction after error appears, or both.

---

## 3. Methods overview

### 3.1 Synthetic moving-environment programme

The synthetic programme retains the frozen PAYOFF-B tracking design. Populations occupy explicit one- or two-dimensional landscapes under directional environmental forcing. Spatial redistribution emerges from local population growth and dispersal rather than direct displacement. Phenological response is bounded by a finite \(z_{\max}\).

We compare open landscapes with straight and zigzag barriers, vary directional movement anisotropy, and add partner-matching costs for interacting species. Coordinated strategy value is separated from accessibility under unilateral rare substitutions.

The synthetic parameter values are mechanism probes, not estimates of natural climate velocity or corridor thresholds.

### 3.2 Broad 55-species migration and split-sample substitution tests

The primary cross-system empirical test uses 5,816 observations from 55 migratory bird species in the registered broad migration dataset. The analysis asks whether arrival mismatch is minimized at one portable ratio of animal migration speed to environmental-wave speed.

Raw and phase-centered versions are evaluated under the frozen analysis. Species-level curvature and optimum heterogeneity are retained rather than replaced with one pooled optimum when the surface is shallow.

A fresh response-blind secondary registration then tested temporal substitution directly. Unique years were split chronologically, with 2002–2009 used only to estimate each species' responsiveness of arrival-date anomalies to green-up anomalies and 2010–2017 reserved as holdout. Species required at least 60 calibration observations, five cells and five calibration years. Calibration years also defined each species-by-cell baseline phase. In holdout years, absolute deviation from that baseline was modelled as a quadratic function of log animal/environment speed ratio, timing responsiveness and their interactions, with speed scale, alignment, latitude, green-up anomaly, migration/breeding flags and species, species-by-cell and year random effects. The registered primary term was the interaction between squared log speed ratio and standardized timing responsiveness. Temporal substitution predicted a negative coefficient; support required the registered direction and p<0.05. No alternate split, timing-gain definition, response or moderator model was licensed after readout.

### 3.3 Direct migration systems

Three directly reconstructed systems are used for mechanistic decomposition rather than formal meta-analysis.

**Mule deer.** Whole-spring-migration phase transformation is linked to movement-speed and stopover adjustment.

**Barnacle geese.** Route-stage transitions across multiple flyways estimate phase retention and stopover/overtake responses. POWER-to-ERA5 substitutions are retained as reconstruction-reliability tests for highlighted transitions.

**Eurasian wigeon.** Consecutive staging transitions estimate phase retention under source-faithful POWER and independent ERA5 environmental reconstructions. Actuator results are evaluated separately from the phase-retention response.

### 3.4 Interval standardization and measurement error

Before opening the Aikens lambda outcome, a secondary interval-standardization contract was frozen. Raw \(\lambda\) remains the primary segment-scale estimator; equivalent magnitude decay and homogeneous path-memory retention are reported only as scale-explicit secondary comparisons.

Wigeon POWER-versus-ERA5 disagreement and event-structure SIMEX are treated as sensitivity evidence, not as a gold-standard latent correction.

### 3.5 Industrial-development perturbation

Published industrial-development mule-deer data provide an independent actuation contrast (Aikens et al. 2022). The registered control-permeability analysis asks whether movement response is attenuated in the large-development population and whether a stronger temporal deterioration prediction is supported.

A separate preregistered 24-hour phase-retention analysis asks whether this independently observed actuation contrast propagates into \(\lambda\) while holding taxon fixed.

**This lambda outcome remains unopened in the present PREOUTCOME manuscript.**

---

## 4. Results

### 4.1 Movement and timing are locally substitutable

In the local controller, movement and timing feedback are exactly substitutable at fixed total gain \(K\). Endpoint mismatch therefore does not identify whether spatial movement, seasonal timing, or a mixture carries the corrective burden.

This is the baseline identification result for the integrated paper. All subsequent results ask which ecological constraints reveal differences hidden by this local equivalence.

### 4.2 Finite timing creates a temporal bypass followed by spatial re-entry

In the frozen one-dimensional moving landscape, increasing phenological capacity expanded the sampled persistence frontier. With \(z_{\max}=0\), the largest persisted forcing velocity was 0.030 and the first failed velocity was 0.035. At \(z_{\max}=5\), the corresponding bracket shifted to 0.065 and 0.070.

Near the persistence frontier, however, strategies remained migration-dominant. Timing therefore extends the operating envelope but does not remove the need for spatial redistribution under sustained directional forcing.

The two-dimensional zigzag landscape makes this temporal bypass visible. At \(z_{\max}=4\), phenology-only strategies were favored at forcing velocities 0.04 and 0.05. Migration re-entered at 0.06 and increased further at 0.07. The second-wall crossing fraction rose from effectively zero in the phenology-only regime to about 0.132 at 0.06 and 0.314 at 0.07.

Thus the same low mismatch can be maintained first by timing and later by renewed movement. Endpoint mismatch alone would not reveal this shift in burden.

### 4.3 Temporal buffering can hide fragmentation costs until spatial demand re-enters

In the canonical open-versus-zigzag comparison, the mean low-density growth penalty associated with the zigzag route changed from approximately -0.0419 at phenology limit 0 to -0.0070 at phenology limit 4, an approximately 83% reduction in penalty magnitude.

The qualitative effect persisted under strong directional anisotropy, where phenological capacity reduced the sampled route penalty by roughly 75–76% across the declared anisotropy levels.

This is buffering, not elimination of fragmentation. Timing reduces the immediate cost of spatial geometry, but continued environmental displacement eventually restores movement demand.

### 4.4 Partner dependence can make beneficial reallocations inaccessible

With positive partner matching dependence, coordination barriers were common in the sampled interacting landscapes. In the two-dimensional design, 22 of 24 sampled positive-interaction cells contained a coordination barrier and 21 of 24 changed the local endpoint from extinction to coordinated persistence.

The canonical one-step gate shows why. A matched resident at

\[
(m,h)=(0.2,0)
\]

had joint low-density growth near -0.840. If both partners shifted together to

\[
(m,h)=(0.2,0.2),
\]

joint growth rose to approximately +0.255, a gain of +1.095. Yet the same one-step timing shift made by either species alone had a strongly negative unilateral gain of approximately -5.946.

The high-value alternative was therefore adjacent but individually inaccessible. Interaction matching can preserve synchronization under moderate forcing while blocking the coordinated reallocation required under stronger forcing.

### 4.5 The broad natural test rejects one universal speed rule

The simple benchmark motivates a natural empirical question: do migrants organize around one portable animal-speed/environmental-wave-speed optimum?

Across 5,816 observations from 55 migratory bird species, the registered broad analysis does not support that prediction.

Raw arrival mismatch favored an apparent optimum away from one. Local phase centering moved the flexible point estimate toward order one, but the surface remained shallow and species-level optima were heterogeneous. Registered moderator scans did not recover a convincing universal rule.

The primary macroecological result is therefore a falsification:

> phenological migration does not collapse onto one natural movement-to-environment speed optimum.

This is not treated as a failed prelude. It is the cross-system result expected when temporal buffering, waiting, route geometry and other tracking dimensions redistribute demand away from movement speed alone. A single speed ratio cannot remain portable if the amount of spatial response currently expressed depends on how much tracking burden is being absorbed elsewhere.

The chronological holdout then tested the stronger substitution prediction. Calibration years produced timing-responsiveness estimates for 39 eligible species; the holdout contained 3,268 observations from the same 39 species across eight years. The registered interaction between squared log speed ratio and timing responsiveness was **+0.0351 ± 0.0289** (p=0.225), opposite to the predicted negative direction. The registered test therefore failed in direction: historically stronger timing responsiveness did not flatten later dependence of mismatch on movement speed. In the same frozen model, timing responsiveness had a negative main association with holdout mismatch (−0.300 ± 0.105, p=0.0043), but this was not the registered primary test and is retained only as a secondary descriptive result.

Thus the natural bird data provide no evidence that greater timing responsiveness makes movement-speed matching less relevant. Better temporal tracking can coexist with, rather than replace, dependence on the spatial movement axis.

### 4.6 Direct migration systems transform phase error, but not with one actuator or interval

The three directly reconstructed systems share an estimator form but not one biological coefficient.

Mule deer show strong phase-dependent movement-speed acceleration, compensatory stopover shortening and a whole-migration phase-retention estimate near \(\lambda=0.107\).

Barnacle-goose route stages show a wider range of phase transformations, including strong reset, partial retention and negative overshoot. Highlighted POWER-to-ERA5 substitutions preserve the qualitative response in Greenland R2→R3, Barents R1→R2 and Svalbard R2→R4. Negative stopover responses also reproduce for these highlighted transitions.

Eurasian wigeon provide a contrasting reliability pattern. On the same 224 transitions, phase retention remains below one under both POWER and source-faithful ERA5 reconstructions, while the proposed stopover actuator is supported under POWER but not under ERA5.

The shared object is therefore the response coordinate, not one actuator architecture. Natural migrants correct phase error through multiple routes, consistent with tracking burden being redistributed among movement, waiting and route-stage responses rather than expressed as one universal movement speed.

### 4.7 Interval scale explains part, but not all, of apparent cross-system heterogeneity

Raw phase-retention coefficients describe different ecological intervals. The median elapsed duration is about 47 d for the mule-deer whole-migration interval and much shorter for route-stage or staging-transition systems.

The frozen secondary interval standardization makes this scale dependence explicit. It reduces the temptation to interpret the difference between mule-deer \(|\lambda|\approx0.107\) and wigeon \(|\lambda|\approx0.750\)–0.811 as a direct seven-fold difference in biological correction strength.

For wigeon, homogeneous propagation over a typical seven-transition migration gives retained-memory components of approximately 0.133 under POWER and 0.231 under ERA5. But the frozen SIMEX sensitivity allows substantially greater retained memory, reaching about 0.627 in the conservative scenario.

Interval normalization therefore clarifies comparison without producing a new universal controller constant.

### 4.8 Information and feedback are distinct routes to low mismatch

Barnacle-goose transitions occupy different combinations of environmental innovation and phase retention. The preregistered expectation that higher environmental predictability should mechanically imply stronger realized correction was not supported in the current screen.

This matters because prediction and correction solve different parts of the timing problem, a distinction already central to migration-information theory (Bauer et al. 2020; Kölzsch et al. 2015). Environmental information can reduce the error that appears at the next transition; behavioral feedback acts on error that already exists.

Low realized mismatch can therefore arise from low innovation, strong phase transformation, or both.

### 4.9 Actuation can be attenuated without supporting every stronger prediction

The industrial-development mule-deer analysis used 64,539 GPS positions from 137 animals and 253 animal-years. The primary control-permeability comparison was estimable for 188 animal-years from 103 animals.

Movement control was lower in the large-development population, with the registered direction stable across all eight near/far definitions. The clustered large-development shift in log control permeability was negative and supported in the frozen primary analysis.

The stronger prediction of additional temporal deterioration was not supported.

This separates an actuation constraint from a general decline in every timing metric and provides a discriminating setting for the preregistered within-taxon phase-retention test.

### 4.10 Does actuation attenuation propagate into phase retention?

<!-- AIKENS_LAMBDA_RESULTS_START -->
[AIKENS LAMBDA RESULT PENDING — render only from the registered result JSON after the frozen environmental reconstruction executes.]
<!-- AIKENS_LAMBDA_RESULTS_END -->

---

## 5. Discussion

### 5.1 Temporal buffering delays rather than removes spatial tracking

The strongest mechanistic result is not merely that movement and timing are difficult to identify from the same mismatch. In explicit moving landscapes, finite timing capacity acts as a **temporal bypass**: it expands the persistence envelope, reduces the immediate cost of fragmented routes and can support phenology-only tracking over part of the forcing range. Under stronger sustained directional forcing, however, movement re-enters and remains necessary near the persistence frontier.

This distinguishes buffering from permanent substitution. The local controller permits exact substitution at fixed total feedback, but the explicit landscape does not because timing has finite range while the environmental target continues to move. Temporal adjustment therefore changes **when** spatial tracking becomes necessary; it does not abolish spatial demand.

### 5.2 Low mismatch can conceal latent spatial tracking demand

The ecological consequence is that current alignment can remain good while the future requirement for movement grows. A population can maintain low mismatch by spending finite timing capacity, yet once that capacity is exhausted the deferred spatial response becomes explicit. We call that deferred requirement latent spatial tracking demand.

Two additional constraints make this hidden demand consequential. First, temporal adjustment can reduce the immediate cost of fragmented movement routes without repairing those routes, so fragmentation can become important precisely when movement re-enters. Second, partner dependence can make a jointly beneficial reallocation inaccessible to unilateral change.

Hence,

\[
\text{low current mismatch}
\neq
\text{low future spatial demand},
\]

and

\[
\text{same mismatch}
\neq
\text{same remaining response capacity}.
\]

This is where the identification result becomes biologically important: mismatch is an outcome of the tracking system, not a direct readout of the mechanism or reserve capacity that keeps it small.

### 5.3 Natural data reject both a universal speed rule and simple temporal substitution

The failure of a universal natural speed optimum is not surprising once tracking has multiple degrees of freedom. A speed ratio compresses target phase, waiting opportunities, route geometry, information quality, actuator constraints and ecological interval into one scalar. The broad analysis is important precisely because it prevents the theory from becoming an unconstrained explanation after the fact: a simple portable optimum was testable and was not recovered.

The chronological holdout provides a sharper boundary. If timing responsiveness simply substituted for movement-speed matching, species that historically tracked green-up more strongly should have shown a flatter later mismatch-speed curve. They did not. The registered moderation coefficient was opposite-signed and unsupported, so the natural data reject that simple substitution prediction as well.

The secondary negative timing-responsiveness main effect suggests that historically more timing-responsive species can maintain lower mismatch overall while still retaining movement-speed dependence. Because that main effect was not the registered primary target, we treat it descriptively. The licensed inference is narrower: temporal responsiveness may improve tracking without making spatial tracking dispensable. This distinction aligns with the explicit landscapes, where timing buffers environmental change but movement re-enters once temporal capacity or geometry becomes limiting.

### 5.4 Phase–velocity division of labor explains the failed substitution test

The registered holdout result sharpens the mechanism. Species with stronger historical timing responsiveness had lower holdout mismatch on average, yet that responsiveness did not weaken the mismatch dependence on movement-speed ratio. The predicted negative moderation therefore failed even though timing responsiveness itself was associated with improved alignment.

The phase–velocity identity explains this combination. A timing shift changes the phase intercept of the tracking problem, whereas a speed difference changes how mismatch accumulates along a moving environmental wave. Better timing can therefore lower the whole mismatch surface without flattening its dependence on movement speed. In control terms, timing and speed are not redundant actuators acting on one scalar gain; they can regulate different components of the forcing.

This interpretation is also consistent with the Amaral source analysis, which independently modelled bird migration speed as responding to green-up date and green-up speed. Its species-sensitivity term in the migration-speed model was not negative. We treat that source result as prior consistency rather than a new PAYOFF confirmatory test.

The deeper ecological distinction is therefore between **phase control** and **propagation control**. Phenological responsiveness helps determine when the organism enters the moving environmental wave; movement speed helps determine whether it keeps pace with the spatial propagation of that wave. Timing can improve tracking without making transport dispensable.

### 5.5 What is portable across migration systems

The direct systems suggest a more modest portable object: the transformation of incoming phase error over a declared ecological interval.

Even this portability has limits. Raw \(\lambda\) depends on interval definition and is vulnerable to error in the reconstructed environmental phase. We therefore retain raw segment-scale estimates, interval-standardized secondary comparisons, and reconstruction reliability as separate dimensions.

Actuators are even less portable. Mule deer use movement speed and stopover. Barnacle geese show strong route-stage waiting and overtaking behavior. Wigeon phase transformation reproduces across environmental surfaces while one proposed stopover association does not.

The useful generalization is therefore a decomposition, not a constant.

### 5.6 Information, retention and actuation should not be collapsed into “tracking ability”

Observed mismatch can be organized into at least three distinct components:

1. **environmental innovation** — how much new error enters because the next condition is uncertain;
2. **phase retention** — how much incoming error remains after realized correction;
3. **actuation limitation** — whether the organism can express the movement or waiting response otherwise available.

A fourth boundary occurs when organisms change the resource wave itself, as in ecosystem engineering. In those systems the environmental target is partly endogenous and a one-way tracker model is insufficient.

This decomposition changes how climate responses should be interpreted. Increasing environmental innovation can worsen mismatch without any decline in behavioral control. Conversely, infrastructure can increase mismatch by reducing actuation even if environmental predictability is unchanged.

### 5.7 Within-taxon perturbation is the decisive next mechanism test

The industrial-development system is especially valuable because it changes the inferential structure. Cross-species differences can always reflect many unmeasured differences in life history, routes and observation scale. A preregistered within-taxon comparison can instead ask whether an independently observed actuation contrast is accompanied by a change in phase retention.

<!-- AIKENS_LAMBDA_DISCUSSION_START -->
[AIKENS LAMBDA DISCUSSION PENDING — the integrated narrative must remain valid if the contrast is supported, null, opposite-signed within uncertainty, or non-estimable under the frozen support gate.]
<!-- AIKENS_LAMBDA_DISCUSSION_END -->

The purpose of this test is not to rescue a universal lambda. It is to distinguish response-coordinate stability from a specific mechanistic perturbation.

### 5.8 Limitations

The synthetic landscapes are mechanism models, not calibrated forecasts. Their velocities, costs and corridor geometries should not be interpreted as natural thresholds.

The 55-species analysis tests a broad speed-ratio hypothesis but does not observe every behavioral decision available to each species. The chronological holdout directly tests one substitution prediction but does not measure remaining phenological capacity; its timing-responsiveness slope is a realized phase-response metric, not the synthetic \(z_{\max}\).

The direct empirical panel contains three reconstructed taxa, with repeated barnacle-goose flyways sharing species and individuals. It is not a formal meta-analysis of independent taxa.

Raw phase-retention coefficients are conditional on ecological interval. Secondary standardization makes the scale explicit but does not turn the discrete regressions into continuous-time controller estimates.

Environmental phase is reconstructed with heterogeneous data products. POWER-to-ERA5 comparisons provide sensitivity and replication evidence but do not identify a uniquely correct error distribution.

All current direct phase-retention results are observational. They do not establish that the observed controller maximizes lifetime fitness or evolved specifically to minimize phenological error.

The industrial-development comparison does not by itself identify development as the sole causal difference among populations.

---

## 6. Conclusion

Temporal adjustment can postpone movement, but it cannot replace spatial tracking indefinitely under sustained directional environmental change.

In the explicit landscapes, finite timing capacity expands persistence and buffers fragmentation costs before movement re-enters as forcing strengthens. Low mismatch can therefore hide latent spatial tracking demand until temporal capacity is exhausted, while interaction constraints can further block the reallocation required to keep tracking.

Natural migration also rejects a simple substitution interpretation. Across 55 bird species, migration does not collapse onto one portable movement-to-environment speed optimum. In the independent chronological holdout, stronger historical timing responsiveness did not weaken later movement-speed dependence; the registered moderation test failed in the opposite direction. Direct systems instead transform phase error through different combinations of movement, waiting and route-stage responses over different ecological intervals.

<!-- AIKENS_LAMBDA_CONCLUSION_START -->
[AIKENS LAMBDA CONCLUSION PENDING — outcome-blind renderer insertion only.]
<!-- AIKENS_LAMBDA_CONCLUSION_END -->

The general ecological conclusion is therefore **temporal buffering, not temporal replacement**. Timing can delay when spatial tracking becomes necessary, and that delay can make current mismatch underestimate future dependence on movement and movement-permitting landscapes. The methodological consequence follows from the ecology: mismatch is an outcome, not a direct measure of tracking architecture or remaining resilience.

---

## Prior-art boundary

This paper does not claim novelty for recognizing phenological mismatch or
climate-driven shifts in seasonal timing (Post et al. 2001; Visser & Gienapp
2019; Kharouba & Wolkovich 2020; Weir & Phillimore 2024), for combining spatial
and temporal responses to environmental change (Harsch et al. 2017; Macgregor
et al. 2019; Hällfors et al. 2021; Muthukrishnan et al. 2025; Fredston et al.
2025), or for earlier theory linking timing adaptation to spatial structure
(Pontarp et al. 2015).

Nor do we claim novelty for green-wave surfing, surf-versus-jump migration or
compensatory tracking behavior (Bischof et al. 2012; Aikens et al. 2017;
Ortega et al. 2023; Amaral et al. 2025; van Toor et al. 2021), for migration
timing under variable or predictable information (Kölzsch et al. 2015; Bauer
et al. 2020; Torstenson & Shaw 2025), for climate-driven interaction mismatch
(Gilman et al. 2012), for resource-wave engineering (Geremia et al. 2019), or
for anthropogenic decoupling of migration from the green wave (Aikens et al.
2022). Generic negative-feedback mathematics is likewise not claimed as new.

The narrower contribution is to show that temporal adjustment can act as a
finite buffer of spatial tracking demand in explicit moving landscapes: timing
delays spatial response and reduces immediate route costs, but movement re-enters
under sustained forcing, while geometry and coordination can constrain that
reallocation. The broad 55-species test rejects a one-dimensional universal
speed rule, and a fresh chronological holdout additionally rejects the simple
prediction that historically stronger timing responsiveness should weaken later
movement-speed dependence. Direct migration systems show that natural phase
correction is implemented through different actuators and ecological intervals.
The identification result is a consequence of this mechanism: low mismatch can
conceal continued dependence on spatial tracking and does not directly measure
remaining response capacity.

## References

- Aikens EO, Kauffman MJ, Merkle JA, Dwinnell SPH, Fralick GL, Monteith KL (2017) The greenscape shapes surfing of resource waves in a large migratory herbivore. *Ecology Letters* 20:741–750. DOI: 10.1111/ele.12772.
- Aikens EO, Wyckoff TB, Sawyer H, Kauffman MJ (2022) Industrial energy development decouples ungulate migration from the green wave. *Nature Ecology & Evolution* 6:1733–1741. DOI: 10.1038/s41559-022-01887-9.
- Amaral BR, Youngflesh C, Tingley M, Miller DAW (2025) Shifting gears in a shifting climate: Birds adjust migration speed in response to spring vegetation green-up. *Diversity and Distributions* 31:e70033. DOI: 10.1111/ddi.70033.
- Bauer S, McNamara JM, Barta Z (2020) Environmental variability, reliability of information and the timing of migration. *Proceedings of the Royal Society B* 287:20200622. DOI: 10.1098/rspb.2020.0622.
- Bischof R, Loe LE, Meisingset EL, Zimmermann B, Van Moorter B, Mysterud A (2012) A migratory northern ungulate in the pursuit of spring: Jumping or surfing the green wave? *The American Naturalist* 180:407–424. DOI: 10.1086/667590.
- Fredston AL et al. (2025) Reimagining species on the move across space and time. *Trends in Ecology & Evolution* 40:629–638. DOI: 10.1016/j.tree.2025.03.015.
- Geremia C, Merkle JA, Eacker DR, Wallen RL, White PJ, Hebblewhite M, Kauffman MJ (2019) Migrating bison engineer the green wave. *Proceedings of the National Academy of Sciences* 116:25707–25713. DOI: 10.1073/pnas.1913783116.
- Gilman RT, Fabina NS, Abbott KC, Rafferty NE (2012) Evolution of plant–pollinator mutualisms in response to climate change. *Evolutionary Applications* 5:2–16. DOI: 10.1111/j.1752-4571.2011.00202.x.
- Hällfors MH et al. (2021) Combining range and phenology shifts offers a winning strategy for boreal Lepidoptera. *Ecology Letters* 24:1619–1632. DOI: 10.1111/ele.13774.
- Harsch MA et al. (2017) Moving forward: insights and applications of moving-habitat models for climate change ecology. *Journal of Ecology* 105:1169–1181. DOI: 10.1111/1365-2745.12724.
- Kharouba HM, Wolkovich EM (2020) Disconnects between ecological theory and data in phenological mismatch research. *Nature Climate Change* 10:406–415. DOI: 10.1038/s41558-020-0752-x.
- Kölzsch A et al. (2015) Forecasting spring from afar? Timing of migration and predictability of phenology along different migration routes of an avian herbivore. *Journal of Animal Ecology* 84:272–283. DOI: 10.1111/1365-2656.12281.
- Macgregor CJ et al. (2019) Climate-induced phenology shifts linked to range expansions in species with multiple reproductive cycles per year. *Nature Communications* 10:4455. DOI: 10.1038/s41467-019-12479-w.
- Muthukrishnan R et al. (2025) Chasing the Niche: Escaping Climate Change Threats in Place, Time, and Space. *Global Change Biology* 31:e70167. DOI: 10.1111/gcb.70167.
- Ortega AC, Aikens EO, Merkle JA, Monteith KL, Kauffman MJ (2023) Migrating mule deer compensate en route for phenological mismatches. *Nature Communications* 14:2008. DOI: 10.1038/s41467-023-37750-z.
- Pontarp M, Johansson J, Jonzén N, Lundberg P (2015) Adaptation of timing of life history traits and population dynamic responses to climate change in spatially structured populations. *Evolutionary Ecology* 29:565–579. DOI: 10.1007/s10682-015-9759-6.
- Post E, Forchhammer MC, Stenseth NC, Callaghan TV (2001) The timing of life-history events in a changing climate. *Proceedings of the Royal Society B* 268:15–23. DOI: 10.1098/rspb.2000.1324.
- Torstenson M, Shaw AK (2025) Strength of seasonality and type of migratory cue determine the fitness consequences of changing phenology for migratory animals. *Oikos* 2025:e10862. DOI: 10.1111/oik.10862.
- van Toor ML et al. (2021) Migration distance affects how closely Eurasian wigeons follow spring phenology during migration. *Movement Ecology* 9:61. DOI: 10.1186/s40462-021-00296-0.
- Visser ME, Gienapp P (2019) Evolutionary and demographic consequences of phenological mismatches. *Nature Ecology & Evolution* 3:879–885. DOI: 10.1038/s41559-019-0880-8.
- Weir JC, Phillimore AB (2024) Buffering and phenological mismatch: a change of perspective. *Global Change Biology* 30:e17294. DOI: 10.1111/gcb.17294.

---

## Figure architecture

**Figure 1 — Temporal buffering and latent spatial tracking demand.**  
Conceptual panel linking the PAYOFF-B1 timescale benchmark to local movement–timing substitution, finite temporal buffering, spatial re-entry, the broad speed-rule test and direct phase-control systems.

**Figure 2 — Finite temporal buffering and spatial re-entry.**  
Synthetic one- and two-dimensional results: persistence frontier, zigzag temporal bypass and movement re-entry.

**Figure 3 — Interaction can block coordinated tracking reallocation.**  
Canonical one-step coordination gate plus compact 22/24 two-dimensional summary.

**Figure 4 — Broad natural data reject a universal speed rule and simple temporal substitution.**  
The 55-species raw and phase-centered movement/environment speed analysis is paired with the registered 2002–2009 / 2010–2017 timing-responsiveness holdout test.

**Figure 5 — Real systems transform phase error through different architectures.**  
Mule deer, barnacle goose and wigeon phase-retention and actuator summaries, with raw interval scale made explicit.

**Figure 6 — Information, retention and actuation are separable.**  
Environmental innovation versus phase retention, reconstruction reliability, and industrial-development actuation contrast; reserve one subpanel for the preregistered Aikens lambda outcome if estimable.

The integrated paper should use no more than six main figures. Extended simulation sweeps and direct-system diagnostics move to Supplementary Information.

---

## Claim ceiling

This integrated manuscript supports:

- failure of one universal natural movement-speed/environmental-wave-speed optimum in the registered 55-species broad bird analysis;
- failure, in the registered chronological holdout, of the prediction that stronger historical timing responsiveness weakens later movement-speed dependence;
- exact movement–timing substitutability in the declared local controller;
- finite temporal buffering that delays but does not permanently replace spatial tracking in the declared synthetic landscapes;
- low mismatch concealing latent spatial tracking demand within those declared synthetic landscapes;
- spatial re-entry and fragmentation-cost buffering in the declared synthetic landscapes;
- interaction-generated coordination barriers in the declared sampled systems;
- source-faithful phase transformation in mule deer, barnacle goose and wigeon;
- separation of response coordinate from actuator architecture;
- scale-explicit interval standardization without promotion of a universal biological lambda;
- separation of environmental innovation, realized phase retention and actuation constraints;
- the frozen industrial-development actuation contrast and its falsified stronger time-trend prediction.

It does not support:

- a universal lambda or universal actuator;
- a formal cross-taxon meta-analytic controller coefficient;
- a natural threshold inferred from synthetic velocity or corridor values;
- direct ranking of taxa by raw lambda magnitude;
- a universal claim that migrants remove a fixed fraction of phase error;
- a final latent measurement-error-corrected wigeon lambda;
- causal attribution of the industrial population contrast solely to development;
- an evolutionary fitness optimum for the empirical lambda values;
- direct empirical measurement of latent spatial tracking demand across the 55-species or three-system datasets;
- a claim that all natural phenological adjustment necessarily produces hidden spatial demand;
- promotion of the secondary timing-responsiveness main effect to the registered primary holdout result;
- a positive empirical claim that timing and movement are complementary based on the unsupported positive holdout interaction;
- extension of the PAYOFF-B1 anti-phase uniqueness theorem to the general moving-landscape or empirical systems.
