# Hidden tracking: why environmental mismatch does not reveal how organisms keep pace with changing environments

**Status:** integrated ecology manuscript v1, PREOUTCOME  
**Publication architecture:** combines the frozen synthetic tracking-theory programme with the movement–phenology macroecological programme; the exact anti-phase optimum theorem remains a separate PAYOFF-B1 paper.  
**Evidence boundary:** all synthetic quantitative claims are inherited from frozen 2026-09-20 tracking outputs; all empirical claims are inherited from registered and source-faithful receipts already on main. The preregistered Aikens industrial-development lambda outcome remains unopened.

## Abstract

Environmental mismatch is often treated as a direct measure of how well organisms track changing conditions. That interpretation is incomplete when tracking can be redistributed among movement, seasonal timing, environmental information and behavioral actuation. We combine theory, simulation and migration data to test whether a single tracking rule can explain low mismatch across systems. A local controller gives a deliberately strong null: movement and phenological feedback are interchangeable through their summed restoring gain, so the same mismatch trajectory can arise from different allocations between axes. Explicit moving landscapes break this equivalence. Finite phenological capacity delays but does not eliminate spatial tracking; timing reduces sampled fragmentation costs before movement re-enters; and partner dependence can make jointly beneficial reallocations inaccessible to unilateral change. We then test the corresponding one-dimensional empirical prediction across 5,816 observations from 55 migratory bird species. The data do not support one portable natural movement-speed/environmental-wave-speed optimum. Direct reconstructions in mule deer, barnacle geese and Eurasian wigeon instead show phase transformation on different ecological intervals and through different actuator architectures, with environmental reconstruction changing some actuator inferences while preserving phase-retention signals. These results support a common inference framework rather than a common coefficient: observed mismatch is an outcome of environmental innovation, retained phase error and actuation constraints. Low mismatch can therefore conceal substantial and shifting tracking effort, and similar mismatch among systems need not imply similar mechanisms or resilience.

**Keywords:** environmental tracking; phenological mismatch; migration; movement ecology; climate change; phase retention; habitat fragmentation; behavioral plasticity

---

## 1. Introduction

Organisms exposed to changing environments can respond by moving through space, changing seasonal timing, altering behavior, or combining these responses. Yet many ecological analyses compress this multidimensional process into a single endpoint: the difference between where or when an organism occurs and where or when conditions are favorable.

That endpoint is important, but it is not a mechanism. A small mismatch may reflect weak environmental forcing, high predictability, strong behavioral correction, large movement effort, substantial phenological adjustment, or several of these at once. Conversely, similar mismatch in two populations need not mean that they have similar capacity to continue tracking future change.

This creates an identification problem. If different tracking responses can close the same environmental gap, then endpoint mismatch alone cannot reveal which response is carrying the burden. The problem becomes ecologically important because those responses have different constraints. Movement must be realized through landscapes and corridors. Phenological adjustment has finite seasonal range. Behavioral responses depend on information. Interacting species may need to remain aligned while changing their tracking strategy.

PAYOFF-B begins from an intentionally simple benchmark. In a symmetric two-patch environment with exact anti-phase seasonal switching, a constant migration rate has one positive long-run growth optimum and that optimum scales with the environmental switching timescale. The exact theorem is developed separately in PAYOFF-B1. Here we use that result only as a benchmark for a broader question: **does environmental tracking remain effectively one-dimensional once organisms can redistribute correction between space and time, and does nature exhibit one portable movement-to-environment tracking rule?**

We answer this in three steps.

First, we construct the strongest possible substitution null. In a local controller, movement-mediated and timing-mediated feedback enter only through their summed restoring gain. Equal endpoint mismatch can therefore arise from different tracking architectures.

Second, we add constraints that should break this equivalence: finite phenological capacity, explicit spatial redistribution, fragmented movement routes and partner matching. These models generate testable failure modes in which timing temporarily substitutes for movement but later becomes complementary to it, and in which jointly favorable reallocations can be blocked by coordination barriers.

Third, we test the one-dimensional prediction empirically. A registered broad analysis of 5,816 observations from 55 migratory bird species asks whether migration naturally collapses onto one animal-speed/environment-speed optimum. It does not. We then use directly reconstructed mule-deer, barnacle-goose and Eurasian-wigeon systems to ask what replaces the failed universal rule. Rather than estimating one biological constant, we separate a common phase-retention estimator from system-specific actuator mechanisms and ecological interval scales.

The resulting hypothesis is not that movement or phenology is generally superior. It is that **mismatch is an outcome, not a tracking architecture**. Low mismatch can be maintained while the burden of tracking shifts among space, time, information and actuation, and the hidden architecture determines when apparent resilience will fail.

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

### 2.3 Three ways the null should fail

We distinguish three constraint classes.

**Capacity.** Phenological timing cannot shift indefinitely. If environmental displacement continues accumulating, temporal adjustment can delay but not permanently replace spatial redistribution.

**Geometry.** Movement must traverse actual landscapes. Two strategies producing similar endpoint mismatch can differ strongly in route cost and access to habitat.

**Coordination.** Interacting species can each track the abiotic environment while becoming mismatched with one another. A reallocation beneficial when both partners change together can be selected against when either changes alone.

These constraints yield a general expectation:

\[
\text{same mismatch} \not\Rightarrow \text{same resilience}.
\]

### 2.4 Empirical phase retention

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

### 3.2 Broad 55-species migration test

The primary cross-system empirical test uses 5,816 observations from 55 migratory bird species in the registered broad migration dataset. The analysis asks whether arrival mismatch is minimized at one portable ratio of animal migration speed to environmental-wave speed.

Raw and phase-centered versions are evaluated under the frozen analysis. Species-level curvature and optimum heterogeneity are retained rather than replaced with one pooled optimum when the surface is shallow.

### 3.3 Direct migration systems

Three directly reconstructed systems are used for mechanistic decomposition rather than formal meta-analysis.

**Mule deer.** Whole-spring-migration phase transformation is linked to movement-speed and stopover adjustment.

**Barnacle geese.** Route-stage transitions across multiple flyways estimate phase retention and stopover/overtake responses. POWER-to-ERA5 substitutions are retained as reconstruction-reliability tests for highlighted transitions.

**Eurasian wigeon.** Consecutive staging transitions estimate phase retention under source-faithful POWER and independent ERA5 environmental reconstructions. Actuator results are evaluated separately from the phase-retention response.

### 3.4 Interval standardization and measurement error

Before opening the Aikens lambda outcome, a secondary interval-standardization contract was frozen. Raw \(\lambda\) remains the primary segment-scale estimator; equivalent magnitude decay and homogeneous path-memory retention are reported only as scale-explicit secondary comparisons.

Wigeon POWER-versus-ERA5 disagreement and event-structure SIMEX are treated as sensitivity evidence, not as a gold-standard latent correction.

### 3.5 Industrial-development perturbation

Published industrial-development mule-deer data provide an independent actuation contrast. The registered control-permeability analysis asks whether movement response is attenuated in the large-development population and whether a stronger temporal deterioration prediction is supported.

A separate preregistered 24-hour phase-retention analysis asks whether this independently observed actuation contrast propagates into \(\lambda\) while holding taxon fixed.

**This lambda outcome remains unopened in the present PREOUTCOME manuscript.**

---

## 4. Results

### 4.1 The same mismatch can be produced by different tracking architectures

In the local controller, movement and timing feedback are exactly substitutable at fixed total gain \(K\). Endpoint mismatch therefore does not identify whether spatial movement, seasonal timing, or a mixture carries the corrective burden.

This is the baseline identification result for the integrated paper. All subsequent results ask which ecological constraints reveal differences hidden by this local equivalence.

### 4.2 Finite timing capacity delays spatial tracking but does not replace it

In the frozen one-dimensional moving landscape, increasing phenological capacity expanded the sampled persistence frontier. With \(z_{\max}=0\), the largest persisted forcing velocity was 0.030 and the first failed velocity was 0.035. At \(z_{\max}=5\), the corresponding bracket shifted to 0.065 and 0.070.

Near the persistence frontier, however, strategies remained migration-dominant. Timing therefore extends the operating envelope but does not remove the need for spatial redistribution under sustained directional forcing.

The two-dimensional zigzag landscape makes this temporal bypass visible. At \(z_{\max}=4\), phenology-only strategies were favored at forcing velocities 0.04 and 0.05. Migration re-entered at 0.06 and increased further at 0.07. The second-wall crossing fraction rose from effectively zero in the phenology-only regime to about 0.132 at 0.06 and 0.314 at 0.07.

Thus the same low mismatch can be maintained first by timing and later by renewed movement. Endpoint mismatch alone would not reveal this shift in burden.

### 4.3 Timing can buffer fragmentation costs before spatial demand re-enters

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

This is not treated as a failed prelude. It is the cross-system result the mechanistic theory predicts can occur when multiple tracking dimensions and constraints are compressed into one ratio.

### 4.6 Direct migration systems transform phase error, but not with one actuator or interval

The three directly reconstructed systems share an estimator form but not one biological coefficient.

Mule deer show strong phase-dependent movement-speed acceleration, compensatory stopover shortening and a whole-migration phase-retention estimate near \(\lambda=0.107\).

Barnacle-goose route stages show a wider range of phase transformations, including strong reset, partial retention and negative overshoot. Highlighted POWER-to-ERA5 substitutions preserve the qualitative response in Greenland R2→R3, Barents R1→R2 and Svalbard R2→R4. Negative stopover responses also reproduce for these highlighted transitions.

Eurasian wigeon provide a contrasting reliability pattern. On the same 224 transitions, phase retention remains below one under both POWER and source-faithful ERA5 reconstructions, while the proposed stopover actuator is supported under POWER but not under ERA5.

The shared object is therefore the response coordinate, not one actuator architecture.

### 4.7 Interval scale explains part, but not all, of apparent cross-system heterogeneity

Raw phase-retention coefficients describe different ecological intervals. The median elapsed duration is about 47 d for the mule-deer whole-migration interval and much shorter for route-stage or staging-transition systems.

The frozen secondary interval standardization makes this scale dependence explicit. It reduces the temptation to interpret the difference between mule-deer \(|\lambda|\approx0.107\) and wigeon \(|\lambda|\approx0.750\)–0.811 as a direct seven-fold difference in biological correction strength.

For wigeon, homogeneous propagation over a typical seven-transition migration gives retained-memory components of approximately 0.133 under POWER and 0.231 under ERA5. But the frozen SIMEX sensitivity allows substantially greater retained memory, reaching about 0.627 in the conservative scenario.

Interval normalization therefore clarifies comparison without producing a new universal controller constant.

### 4.8 Information and feedback are distinct routes to low mismatch

Barnacle-goose transitions occupy different combinations of environmental innovation and phase retention. The preregistered expectation that higher environmental predictability should mechanically imply stronger realized correction was not supported in the current screen.

This matters because prediction and correction solve different parts of the timing problem. Environmental information can reduce the error that appears at the next transition; behavioral feedback acts on error that already exists.

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

### 5.1 Mismatch is an outcome, not a tracking architecture

The theoretical and empirical results converge on an identification problem.

In the exact local controller,

\[
\text{same mismatch}
\neq
\text{same movement–timing allocation}.
\]

In the broad bird data,

\[
\text{similar migration mismatch}
\neq
\text{one universal speed rule}.
\]

And in the direct systems,

\[
\text{shared phase-retention estimator}
\neq
\text{shared actuator architecture or biological rate}.
\]

These are three levels of the same result. Endpoint mismatch is informative about realized alignment with the environment, but it does not by itself identify the effort, mechanism or remaining capacity that produced that alignment.

### 5.2 Why low mismatch can be fragile

The synthetic landscapes show three hidden liabilities.

First, timing has finite capacity. A population can maintain low mismatch while using phenological adjustment to postpone movement, yet directional forcing eventually forces spatial redistribution back into the solution.

Second, movement and timing experience different geometry. Timing can reduce the immediate cost of fragmented movement routes without repairing the route itself.

Third, partner dependence can convert a jointly beneficial response into an inaccessible one. Strong matching can synchronize partners and still make the next coordinated tracking architecture unreachable by unilateral change.

Low mismatch can therefore coexist with shrinking response options.

### 5.3 Why the 55-species falsification is expected under multidimensional tracking

The failure of a universal natural speed optimum is not surprising once tracking has multiple degrees of freedom.

A speed ratio compresses target phase, waiting opportunities, route geometry, information quality, actuator constraints and ecological interval into one scalar. Species can therefore achieve similar realized timing with different combinations of movement and waiting, or maintain different characteristic phase offsets despite comparable movement speeds.

The broad analysis is important precisely because it prevents the theory from becoming an unconstrained explanation after the fact. A simple portable optimum was testable and was not recovered.

### 5.4 What is portable across migration systems

The direct systems suggest a more modest portable object: the transformation of incoming phase error over a declared ecological interval.

Even this portability has limits. Raw \(\lambda\) depends on interval definition and is vulnerable to error in the reconstructed environmental phase. We therefore retain raw segment-scale estimates, interval-standardized secondary comparisons, and reconstruction reliability as separate dimensions.

Actuators are even less portable. Mule deer use movement speed and stopover. Barnacle geese show strong route-stage waiting and overtaking behavior. Wigeon phase transformation reproduces across environmental surfaces while one proposed stopover association does not.

The useful generalization is therefore a decomposition, not a constant.

### 5.5 Information, retention and actuation should not be collapsed into “tracking ability”

Observed mismatch can be organized into at least three distinct components:

1. **environmental innovation** — how much new error enters because the next condition is uncertain;
2. **phase retention** — how much incoming error remains after realized correction;
3. **actuation limitation** — whether the organism can express the movement or waiting response otherwise available.

A fourth boundary occurs when organisms change the resource wave itself, as in ecosystem engineering. In those systems the environmental target is partly endogenous and a one-way tracker model is insufficient.

This decomposition changes how climate responses should be interpreted. Increasing environmental innovation can worsen mismatch without any decline in behavioral control. Conversely, infrastructure can increase mismatch by reducing actuation even if environmental predictability is unchanged.

### 5.6 Within-taxon perturbation is the decisive next mechanism test

The industrial-development system is especially valuable because it changes the inferential structure. Cross-species differences can always reflect many unmeasured differences in life history, routes and observation scale. A preregistered within-taxon comparison can instead ask whether an independently observed actuation contrast is accompanied by a change in phase retention.

<!-- AIKENS_LAMBDA_DISCUSSION_START -->
[AIKENS LAMBDA DISCUSSION PENDING — the integrated narrative must remain valid if the contrast is supported, null, opposite-signed within uncertainty, or non-estimable under the frozen support gate.]
<!-- AIKENS_LAMBDA_DISCUSSION_END -->

The purpose of this test is not to rescue a universal lambda. It is to distinguish response-coordinate stability from a specific mechanistic perturbation.

### 5.7 Limitations

The synthetic landscapes are mechanism models, not calibrated forecasts. Their velocities, costs and corridor geometries should not be interpreted as natural thresholds.

The 55-species analysis tests a broad speed-ratio hypothesis but does not observe every behavioral decision available to each species.

The direct empirical panel contains three reconstructed taxa, with repeated barnacle-goose flyways sharing species and individuals. It is not a formal meta-analysis of independent taxa.

Raw phase-retention coefficients are conditional on ecological interval. Secondary standardization makes the scale explicit but does not turn the discrete regressions into continuous-time controller estimates.

Environmental phase is reconstructed with heterogeneous data products. POWER-to-ERA5 comparisons provide sensitivity and replication evidence but do not identify a uniquely correct error distribution.

All current direct phase-retention results are observational. They do not establish that the observed controller maximizes lifetime fitness or evolved specifically to minimize phenological error.

The industrial-development comparison does not by itself identify development as the sole causal difference among populations.

---

## 6. Conclusion

A small environmental mismatch is not a complete measure of adaptive tracking.

In a local system, movement and phenological adjustment can produce the same mismatch through different allocations of corrective effort. Explicit landscapes show why this hidden substitution becomes fragile: timing has finite capacity, movement pays geometric costs, and interacting partners can face coordination barriers. Consistent with that multidimensional view, 55 migratory bird species do not collapse onto one natural movement-to-environment speed optimum.

Direct migration systems reveal what replaces the failed universal rule. Incoming phase error can be transformed through movement, waiting and route-stage responses, but the correction interval and actuator architecture differ among systems. Environmental information, retained phase error and actuation constraints therefore represent distinct routes to the same observed endpoint.

<!-- AIKENS_LAMBDA_CONCLUSION_START -->
[AIKENS LAMBDA CONCLUSION PENDING — outcome-blind renderer insertion only.]
<!-- AIKENS_LAMBDA_CONCLUSION_END -->

The general lesson is not that one tracking mechanism dominates. It is that **mismatch is an outcome of a tracking system whose internal burden can shift before the endpoint visibly deteriorates**. Predicting resilience under continued environmental change therefore requires measuring not only mismatch, but also the mechanisms and remaining capacities that keep mismatch small.

---

## Figure architecture

**Figure 1 — One mismatch, multiple tracking architectures.**  
Conceptual panel linking the separate PAYOFF-B1 timescale benchmark to the local movement–timing substitution null and the phase-retention empirical coordinate.

**Figure 2 — Finite temporal buffering and spatial re-entry.**  
Synthetic one- and two-dimensional results: persistence frontier, zigzag temporal bypass and movement re-entry.

**Figure 3 — Interaction can block coordinated tracking reallocation.**  
Canonical one-step coordination gate plus compact 22/24 two-dimensional summary.

**Figure 4 — Broad natural test rejects one universal speed rule.**  
55-species raw and phase-centered movement/environment speed analysis with heterogeneity diagnostics.

**Figure 5 — Real systems transform phase error through different architectures.**  
Mule deer, barnacle goose and wigeon phase-retention and actuator summaries, with raw interval scale made explicit.

**Figure 6 — Information, retention and actuation are separable.**  
Environmental innovation versus phase retention, reconstruction reliability, and industrial-development actuation contrast; reserve one subpanel for the preregistered Aikens lambda outcome if estimable.

The integrated paper should use no more than six main figures. Extended simulation sweeps and direct-system diagnostics move to Supplementary Information.

---

## Claim ceiling

This integrated manuscript supports:

- failure of one universal natural movement-speed/environmental-wave-speed optimum in the registered 55-species broad bird analysis;
- exact movement–timing substitutability in the declared local controller;
- finite temporal buffering, spatial re-entry and fragmentation-cost buffering in the declared synthetic landscapes;
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
- extension of the PAYOFF-B1 anti-phase uniqueness theorem to the general moving-landscape or empirical systems.
