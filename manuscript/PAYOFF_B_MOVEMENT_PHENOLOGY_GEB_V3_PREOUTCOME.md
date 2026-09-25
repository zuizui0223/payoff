# No universal migration–phenology speed optimum: scale-dependent phase control across migratory systems

**Running title:** Scale-dependent phase control

## Abstract

**Aim:** We test whether migration follows one universal animal-to-environment speed optimum and, if not, whether phase control better describes timing correction.

**Location:** Eastern North America, western USA, North Atlantic–Arctic flyways and the Eurasian wigeon corridor.

**Time period:** Movement and phenology data from 2002–2020, with longer environmental baselines.

**Major taxa studied:** Migratory birds and ungulates; direct systems were mule deer, barnacle goose and Eurasian wigeon.

**Methods:** We tested the speed hypothesis in 5,816 observations from 55 bird species, then estimated phase retention, actuator responses and interval-standardized retained memory in three direct systems. A within-taxon development perturbation was preregistered separately.

**Results:** The 55-species analysis did not support one universal speed optimum: minima were shallow and species-level optima heterogeneous. Direct systems showed phase contraction through different mechanisms and interval scales. Typical seven-transition wigeon retained memory was 0.133 (POWER) or 0.231 (ERA5), versus 0.107 over whole-migration mule deer; conservative SIMEX allowed 0.627. <!-- AIKENS_LAMBDA_ABSTRACT_START -->
[AIKENS LAMBDA ABSTRACT PENDING — render from the registered result JSON before submission.]
<!-- AIKENS_LAMBDA_ABSTRACT_END -->

**Main conclusions:** Migration does not collapse onto one universal speed rule. Direct systems instead support scale-dependent phase feedback through different actuators. Phase control explains the broad failure without replacing it with a universal retention coefficient.

**Keywords:** animal tracking, biologging, environmental predictability, green wave, macroecology, migration, phenological mismatch, phase retention, plasticity, spring phenology

## Introduction

Seasonal migration is a tracking problem. Animals move through landscapes in which food availability, temperature, snowmelt, vegetation development, and breeding opportunity change in both space and time. A large literature shows that migrants can follow green-up, adjust migration timing, alter stopover behavior, and respond to spatial variation in the predictability of spring (Bischof et al., 2012; Kölzsch et al., 2015; Aikens et al., 2017; Bauer et al., 2020). The same literature also shows striking departures from continuous tracking: some migrants jump between seasonal ranges, some overtake a green wave near breeding sites, infrastructure can decouple movement from phenology, and large herbivores can modify the vegetation dynamics they appear to track (Bischof et al., 2012; van Toor et al., 2021; Aikens et al., 2022; Geremia et al., 2019).

These results are usually expressed with system-specific quantities: days from peak green-up, arrival relative to onset of spring, migration speed, stopover duration, a green-wave surfing score, or a reaction-norm slope (Aikens et al., 2017; Ortega et al., 2023; Laforge et al., 2025). Each is biologically meaningful, but they do not provide an obvious common response variable for comparing how strongly different movement systems preserve or correct phenological phase.

Our starting point was an exact theoretical result from PAYOFF-B. In a symmetric two-patch environment with exact anti-phase seasonal switching, a constant migration rate has one positive long-run growth optimum, and the optimum scales with the environmental switching timescale. That benchmark suggested an empirical hypothesis: animal movement and environmental phenology might show an order-one timescale match in nature. We tested the broad version of that prediction first.

The broad test failed. Across 55 migratory bird species, raw arrival–green-up mismatch was not minimized at a universal order-one animal-to-environment front-speed ratio. Local phase centering moved the flexible point minimum toward order-one values, but the minimum remained shallow and highly uncertain. This failure changed the empirical question. Rather than asking whether migrants share one optimal rate or zero lag, we ask how an existing phenological phase deviation is transformed after an animal has had an ecologically meaningful opportunity to move or wait.

We define signed phenological phase as

\[
E=T_a-T_e,
\]

where \(T_a\) is animal timing and \(T_e\) is environmental timing. Over one correction interval, we write

\[
E_{\rm next}
=
a+\lambda E_{\rm current}+\epsilon.
\]

The dimensionless coefficient \(\lambda\) is the fraction and sign of incoming phase deviation retained after the interval. We use

\[
R_\phi=|\lambda|
\]

as a segment-scale phase-retention coordinate **within each declared ecological
interval**. Values below one indicate phase contraction, values near zero
indicate near-complete reset, negative values indicate contraction with
overshoot, and magnitudes above one indicate local amplification. Importantly,
the same \(\lambda\) can arise through different mechanisms, and equal raw
\(\lambda\) values need not imply equal per-time correction when interval
durations differ. Cross-system magnitude comparison therefore uses the
pre-outcome interval standardization defined below.

A second distinction follows from environmental uncertainty. Let \(\xi\) denote the portion of downstream environmental timing that cannot be predicted from current conditions. A linearized phase map can be organized as

\[
e_{i+1}
=
\lambda_i e_i-\xi_i+\eta_i,
\]

where \(\eta_i\) is remaining behavioral and measurement variation. Under the declared approximation,

\[
V_{i+1}
=
\lambda_i^2V_i+\sigma_{\xi,i}^2+\sigma_{\eta,i}^2.
\]

The equation is standard control/AR algebra; our ecological question is whether separating environmental innovation from phase retention organizes migration systems better than treating both as a single “tracking ability.”

We therefore used a deliberately hierarchical design.

**Tier 1 was the primary macroecological test:** does one universal movement-to-phenology speed optimum organize migration across 55 bird species? A positive result would have supported a portable natural speed rule; a broad negative result would reject that simplification.

**Tier 2 was mechanistic decomposition:** if the universal speed rule fails, can direct migratory systems still be described as phase-error controllers, and do different movement architectures achieve correction on different interval scales? Mule deer, barnacle geese and wigeon are therefore not treated as three independent estimates of one universal coefficient. They are case studies of how a common feedback form is implemented differently.

**Tier 3 was perturbation:** does an independently observed movement constraint propagate into phase retention within a taxon under a preregistered forcing contrast?

This hierarchy separates the general macroecological conclusion from the smaller mechanistic panel. The 55-species test determines whether a universal speed rule survives; the direct systems explain what replaces that rule when it does not.

## Methods

### Broad bird test of a universal timescale optimum

We reanalyzed the published Amaral et al. (2025) migration-front dataset, containing spring migration and vegetation green-up estimates for 55 eastern North American migratory bird species across 2002–2017. After the registered completeness and velocity filters, the analysis contained 5,816 species-year-cell observations.

For each observation we defined

\[
u_{\rm macro}
=
\frac{c_{\rm animal}}
{c_{\rm environment}},
\]

where the two front speeds were estimated on matched spatial support, and directional alignment as the cosine of the difference between velocity directions. We modeled absolute bird-arrival minus vegetation-green-up lag as a flexible function of \(\log u_{\rm macro}\), latitude, range position, alignment, species, cell, and year. A second analysis subtracted each species-by-cell mean lag before fitting the same response. The PAYOFF-B interval was treated only as a theoretical reference; it was not an empirical acceptance interval.

### Direct phase-retention systems

We used a common inferential object across direct systems:

\[
E_{\rm next}
=
a+\lambda E_{\rm current}
+\text{registered route covariates}
+\epsilon.
\]

Observation intervals differed by movement architecture and were declared explicitly rather than forced onto one spatial or temporal grain.

Accordingly, raw \(\lambda\) is treated as a **segment-scale within-system
estimand**, not as a cross-system rate constant. A shared regression form does
not make the numerical coefficient invariant to interval length.

#### Mule deer

For Ortega et al. (2023) mule deer, we used the official Nature Communications source-data workbook. The dataset provided 152 animal-years from 72 individuals across eight years. Phase was expressed as days from peak instantaneous rate of green-up. Published movement-rate and stopover summaries were combined with annual green-wave propagation estimates. We quantified the association between initial phase and relative animal-to-environment movement speed, stopover duration, and phase at migration end. Individual-clustered uncertainty was used for repeated animals.

#### Barnacle geese

For Svalbard, Greenland, and Barents barnacle geese, we reconstructed spring stopovers from public Movebank GPS data from Kölzsch et al. (2015) using a common stay-region pipeline and independently reconstructed annual spring-onset anomalies from daily temperature. For fixed region-to-region transitions, unknown constant regional timing anchors shift intercepts but not the slope \(\lambda\), allowing anchor-invariant phase-transfer estimation.

For each eligible transition we estimated

\[
E_{i+1}
=
a+\lambda_iE_i+\epsilon
\]

and the stopover actuator

\[
g_{S,i}
=
-\frac{dS_i}{dE_i}.
\]

The three flyways were treated as repeated routes within one taxon, not as independent species-level replicates.

#### Eurasian wigeon

The wigeon analysis, based on the public tracking system of van Toor et al. (2021), was preregistered internally before promotion of a direct result. We reconstructed the original Movebank source, published four-state HMM parameters, track filtering, staging events, and the published 5 °C thermal-growing-season definition. The movement reconstruction was required to pass gates against reported trajectory counts, individual counts, endpoint distances, and migration speed. The independent environmental reconstruction was required to reproduce the published staging-event phase distribution within registered tolerance.

For consecutive staging events we modeled phase change as

\[
E_{i+1}-E_i
=
\beta_EE_i
+\text{route progress}
+\text{total migration distance}
+\text{year}
+\epsilon,
\]

with

\[
\lambda=1+\beta_E.
\]

The primary preregistered prediction was \(\lambda<1\). A stronger exploratory prediction, \(|\lambda|<0.75\), was frozen before the promoted result.

### Interval standardization of phase retention

Before the preregistered Aikens phase-retention outcome was opened, we froze a
secondary standardization that leaves every primary raw-\(\lambda\) analysis
unchanged.

For each system we define the retained magnitude

\[
R=|\lambda|.
\]

Using the median observed elapsed duration of the exact frozen pair sample as
the reference interval \(\Delta t_{\rm ref}\), we report the equivalent
decay constant

\[
k_{\rm eq}
=
-\frac{\log R}{\Delta t_{\rm ref}},
\]

with units d\(^{-1}\), and the corresponding daily retained magnitude

\[
R_{\rm day}=\exp(-k_{\rm eq}).
\]

Because several interval distributions are strongly skewed, especially for
wigeon, the 25th and 75th percentile durations are retained as a sensitivity
envelope. \(k_{\rm eq}\) is a reference-interval transformation, **not** a
direct fit of a continuous-time controller.

For repeated homogeneous transitions we additionally report the propagated
memory of the incoming phase deviation,

\[
R_{\rm path}(n)=R^n.
\]

This is not expected final phase error: intercepts, new environmental
innovations, route-stage heterogeneity and process noise can add new error
between transitions. For wigeon, \(n\) is taken from the observed
animal-year transition-count distribution, not from total transitions divided
by unique individuals. The 224 transitions comprise 32 animal-years from 28
unique individuals, with both mean and median \(n=7\). For mule deer the
original interval already spans the full spring migration. We do not construct
post-hoc whole-route products for the highlighted goose transitions because a
common preregistered full-route chain is absent.

Negative \(\lambda\) values retain their sign as overshoot/reversal cases;
the logarithmic transformation uses \(|\lambda|\) only for the magnitude
envelope. Wigeon SIMEX values are propagated as sensitivity scenarios, not as
corrected truth.

The prospective Aikens phase-retention contrast uses fixed 24-h pairs, so if it
is estimable its secondary standardization has
\(\Delta t_{\rm ref}=1\) d by construction. This standardization cannot
alter the frozen Aikens group contrast, support threshold, direction, or
significance rule.
### Environmental information and innovation

For fixed barnacle-goose region pairs we modeled destination spring anomaly from origin spring anomaly. The residual standard deviation

\[
\sigma_\xi
\]

was used as the environmental innovation scale. We compared this quantity descriptively with direct phase retention \(|\lambda|\). Transition rows share species, routes, and sometimes individuals, so they were not analyzed as independent studies.

### Measurement-error recovery and replicate environmental calibration

Because phase is reconstructed and appears on the predictor axis, ordinary
least-squares estimates of \(\lambda\) are vulnerable to regression dilution.
We therefore used the local PAYOFF-B tracking recurrence as a known-\(\lambda\)
generator and added an explicit observation layer. If latent incoming phase has
variance \(V_E\), predictor error variance \(V_u\), and covariance \(C_{uv}\)
between consecutive phase errors, the large-sample naive slope is

\[
E[\hat\lambda]
=
\frac{\lambda V_E+C_{uv}}
{V_E+V_u}.
\]

We verified this attenuation analytically and with seed-explicit Monte Carlo
simulation and event-structure-preserving SIMEX.

For wigeon, we first executed a preregistered POWER-versus-ERA5-Land replicate
calibration. That lane retained only 220 of 256 staging events and therefore
failed its frozen 90% coverage gate; its numerical disagreement summaries were
kept as incomplete-calibration diagnostics only.

We then froze a separate source-faithful follow-up before inspecting its
outcome. The original study used hourly ERA5 2-m temperature, so the follow-up
queried ERA5 rather than ERA5-Land, computed GMT daily means from exactly 24
finite hourly values, restricted each year to January--July, and applied the
same cumulative-minimum 5 C TGS rule. The same 256 staging events, 224
transitions, controller formula, clustering rule, published-phase validation
and 90% coverage threshold were retained. Replicate disagreement was used as a
sensitivity scale rather than treated as a gold-standard measurement-error
distribution.

For barnacle geese, we prospectively froze one highlighted fixed transition per
flyway before the corresponding ERA5 outcome was inspected: Greenland R2->R3,
Barents R1->R2 and Svalbard R2->R4. ERA5 hourly 2-m temperature was aggregated
to GMT daily means and passed through the identical latitude-dependent
GDD--logistic-jerk transform used for the POWER reconstruction. Greenland and
Barents used the frozen 1982--2013 baseline; Svalbard used its pre-existing
1982--2011 baseline. Annual onset anomalies were centered separately within
each environmental source. Because a region-specific constant onset offset
changes only the intercept in a fixed origin/destination regression, the
Svalbard reliability lane did not require the uncertain absolute regional
anchors. POWER refits had to reproduce the frozen transition lambda values and
sample sizes before ERA5 estimates were interpreted. POWER--ERA5 anomaly
differences were again treated only as replicate sensitivity scales.

Finally, using the complete ERA5 calibration, we froze a second SIMEX analysis
that assigned one shared error to each unique staging event, preserved
origin--destination error dependence within individual-year sequences, used
\(\zeta=0.5,1,1.5,2\) with 1000 replicates each, and quadratically
extrapolated the mean \(\hat\lambda\) curve to \(\zeta=-1\).

### Industrial-development actuation test

We reanalyzed the archived spring-migration GPS and development-footprint shapefiles from Aikens et al. (2022). Coordinates were transformed into the GPS reference system before calculating distances.

For each animal-year we defined a movement control-permeability proxy

\[
G
=
\frac{\operatorname{median}(\text{speed near development boundary})}
{\operatorname{median}(\text{speed far from development boundary})}.
\]

The primary contrast defined “near” as within 2 km and “far” as at least 10 km from the relevant footprint. Seven additional registered near/far combinations were used for sensitivity. We compared the small- and large-development populations and tested the stronger prediction that the difference became more negative through time. A second model used movement steps with individual-year fixed effects.

### Prospective within-taxon forcing test of phase retention

To test whether an independently observed actuation constraint propagates into
phase retention while holding taxon fixed, we preregistered a second analysis
of the Aikens et al. (2022) industrial-development system before reconstructing
the lambda outcome. The phase coordinate was signed days relative to local peak
instantaneous rate of green-up (IRG), with negative values indicating an animal
ahead of the local peak and positive values indicating an animal behind it.

The original study used MODIS Version 6.0 environmental products, but official
distribution of MODIS V6 land products ended before this analysis. Before
opening the outcome we therefore froze MOD09Q1.061 plus MOD10A2.061 as the
primary successor environmental lane while retaining the already frozen
64,539-GPS request geometry. This product amendment changed neither the
hypothesis nor the spatial request manifest.

We reconstructed local peak IRG with one common processing rule in both
development populations and formed consecutive phase pairs on a fixed 24 h
target grid with a predeclared ±3 h location-matching tolerance. Environmental
phase coverage was required for every retained GPS observation. The primary
model was

\[
E_{t+24h}
=
\beta_0
+
\lambda_{\rm small}E_t
+
\Delta\lambda_{\rm large}
E_t I_{\rm large}
+
\alpha_{\rm animal-year}
+
\epsilon,
\]

with uncertainty clustered by animal identity. The preregistered prediction was

\[
\Delta\lambda_{\rm large}>0
\]

with \(p\le0.05\), corresponding to greater retention of incoming phase error
under large-development forcing. Each population was required to contribute at
least 10 animals and 100 fixed-24 h transitions; otherwise the result was
classified as not estimable without changing the interval, tolerance, product
or support threshold. This within-taxon perturbation is kept separate from the
cross-taxon lambda synthesis.

### Cross-system synthesis and claim control

The broad 55-species speed-ratio analysis is the primary cross-system test. The three direct taxa are a mechanistic panel rather than a three-study meta-analysis.

We therefore reduced the direct registry to one descriptive record per taxon and did not estimate a pooled universal \(\lambda\). Barnacle-goose routes contribute an observed within-taxon range, not independent taxonomic weights. Interval-standardized quantities are used only to diagnose how much of the apparent between-system magnitude difference is attributable to correction scale; they are not promoted as a universal biological rate.

We separately audited prior literature. Green-wave surfing, surf-versus-jump strategies, migration-timing plasticity, predictability effects, compensatory movement, anthropogenic decoupling, ecosystem engineering, and generic negative-feedback mathematics were treated as prior art rather than novel claims.

## Results

### Broad bird data reject a universal natural speed-ratio optimum

The median observed animal-to-environment front-speed ratio across the registered bird dataset was 1.263 and median directional alignment was 0.948. However, the flexible minimum of raw absolute arrival–green-up mismatch occurred at

\[
u_{\rm macro}\approx0.405
\]

under median alignment, far from a universal PAYOFF-B-like order-one optimum.

After subtracting each species-by-cell mean phase offset, the flexible point minimum shifted to

\[
u_{\rm macro}\approx1.043
\]

at median alignment and approximately 1.397 under perfect alignment. These minima were shallow and highly uncertain. Species-level curvature and vertex diagnostics were heterogeneous, and no convincing moderator emerged from HWI, body mass, overwinter latitude, mean phenological sensitivity, route-direction concentration, directional alignment, or simple interannual timing variability.

The broad dataset therefore did not validate one natural movement constant. Instead, it indicated that preserving or transforming a characteristic local phase is more relevant than minimizing raw zero lag.

### Mule deer show strong distributed phase correction

Initial mule-deer phase strongly predicted relative migration speed:

\[
\kappa
=
0.01830\ {\rm d}^{-1},
\]

with individual-clustered SE 0.001223 and \(p=1.21\times10^{-50}\). Each additional day late relative to the forage wave was associated with approximately 1.85% higher relative movement speed.

Stopover duration changed in the compensatory direction:

\[
-0.492\ {\rm stopover\ days}
\]

per additional day late, with clustered \(p=6.07\times10^{-37}\).

Mean absolute phase error declined from 21.91 d at migration start to 11.12 d at migration end. The clustered mean reduction was 10.79 ± 1.41 d (\(p=2.28\times10^{-14}\)). The direct phase-transfer summary was approximately

\[
\lambda=0.107.
\]

Thus only about 11% of incoming phase deviation was retained over the registered spring-migration interval.

The fitted relative-speed controller crossed \(u=1\) at a nonzero phase of approximately 8.46 d, reinforcing that successful tracking need not imply zero phenological lag.

### Barnacle geese repeatedly transform phase through stopover control

For the Svalbard flyway, the primary southern-Norway-to-Svalbard transition included 16 transitions from 15 individuals. Flight pace showed no detectable response to phase error (\(p=0.421\)), whereas stopover duration declined by 0.589 d per additional day late (\(p=1.77\times10^{-11}\)). Direct phase transfer was

\[
\lambda=-0.106,
\]

and the no-correction null \(\lambda=1\) was rejected (\(p=2.01\times10^{-5}\)). The negative sign indicates correction with overshoot, consistent with the known shift toward arrival before local spring near the Arctic breeding grounds.

Independent flyway reconstructions showed the same general ability to contract phase error but different magnitudes. Greenland R2→R3 had

\[
\lambda=0.131
\]

with stopover slope -0.524 d/d, while Barents R1→R2 had

\[
\lambda=0.494
\]

with stopover slope -0.591 d/d. Other route stages included near-complete reset and local amplification, demonstrating that a single species-wide \(\lambda\) is not biologically adequate.

### Wigeon prospectively shows phase contraction; actuator inference is reconstruction-sensitive

A source-faithfulness audit changed the promoted wigeon result before this
manuscript was finalized. The published environmental code restricts daily
temperatures to January--July before applying the 5 C cumulative-minimum TGS
rule. Our original independent POWER reconstruction had used the full calendar
year, which allowed cold northern cell-years to return day 365/366 as apparent
TGS onset. We froze the correction rule before inspecting the corrected
coefficient.

The corrected POWER reconstruction retained all 256 staging events and closely
matched the published phase distribution. Across the same 224 consecutive
staging transitions from 28 individuals,

\[
\hat\lambda_{\rm POWER}=0.7498\pm0.0499,
\]

with a naive test against complete retention of
\(p=5.33\times10^{-7}\). The preregistered primary \(\lambda<1\) gate
therefore passed. The stronger frozen POWER point forecast
\(|\hat\lambda|<0.75\) also passed, but by only 0.00023.

Under the registered POWER phase surface, the directional W2 stopover
prediction also passed: stopover duration declined by 0.0629 d per additional
day late (clustered \(p=0.0317\)). No fixed p-value threshold was preregistered
for W2, and the secondary magnitude forecast \(0.3<g_S<0.8\) failed because
the observed gain was only 0.0629. Between-staging travel speed remained
unsupported.

The independently frozen source-faithful ERA5 reconstruction then provided a
stronger robustness test. It achieved 256/256 event coverage and passed the
published phase-validation and POWER identity gates. On exactly the same 224
transitions,

\[
\hat\lambda_{\rm ERA5}=0.8113\pm0.0448,
\]

with a naive \(p=2.51\times10^{-5}\) against one. Thus estimator-scale phase
contraction reproduced across the POWER and ERA5 environmental surfaces, even
though its magnitude shifted by 0.0615.

The actuator result was less stable. With ERA5 phase, the stopover slope was
-0.0242 d/d with \(p=0.310\), and travel speed again remained unsupported.
Accordingly, the preregistered POWER W2 result remains a valid source-specific
prospective outcome, but it is not independently replicated by the ERA5 phase
surface.

### Observation-error calibration changes correction magnitude more than the qualitative phase signal

The registered ERA5-Land replicate calibration remains a formal failure because
it reached only 220/256 events, below the frozen 90% coverage threshold. A
separate source-faithful ERA5 follow-up, frozen without relaxing that failed
gate, achieved complete 256/256 coverage.

Across the complete paired events, ERA5-minus-POWER phase disagreement had
median 1 d and SD 7.09 d. Treating two reconstructions as equal independent
replicates gives a sensitivity error scale of 5.01 d; consecutive discrepancy
correlation was 0.367. These quantities describe replicate disagreement and do
not uniquely identify either source's measurement error.

True-\(\lambda=1\) simulations showed strong assumption dependence. With the
5.01-d equal-independent-replicate scale, the lower-tail probability at the
observed POWER \(\hat\lambda=0.7498\) was 0.0099; incorporating the observed
discrepancy-correlation proxy reduced it to 0.00050. In a deliberately
conservative scenario that assigned the full 7.09-d disagreement SD to each
source, the lower-tail probability rose to 0.401.

The complete-calibration event-structure SIMEX gave the same qualitative
message. Extrapolated values were 0.8412 under equal independent replicate
error, 0.7979 with the discrepancy-correlation proxy, and 0.9354 under the
conservative full-disagreement scenario. Measurement error therefore materially
changes the inferred strength of correction and can bring the estimate close to
complete retention under an extreme allocation of replicate disagreement.
Nevertheless, all three frozen SIMEX extrapolations remained below one.

We therefore treat wigeon phase retention as a robust estimator-scale response
coordinate across two environmental reconstructions, while leaving the latent
biological correction magnitude interval- and assumption-dependent.

### Raw phase-retention magnitudes partly reflect interval scale

The source-faithful direct estimates use the same regression form but markedly
different ecological intervals. Median elapsed duration was 47.0 d for the
whole-migration mule-deer rows, 14.8--26.6 d for the three highlighted
barnacle-goose transitions, and only 1.06 d for consecutive wigeon staging
transitions.

At those reference durations, the equivalent magnitude-decay constants for the
primary reconstructions were approximately

~~~text
Mule deer whole migration:
  k_eq = 0.047 d^-1

Barnacle goose:
  Svalbard R2->R4  k_eq = 0.151 d^-1, with negative-lambda overshoot retained
  Greenland R2->R3 k_eq = 0.110 d^-1
  Barents R1->R2   k_eq = 0.026 d^-1

Eurasian wigeon:
  POWER k_eq = 0.273 d^-1
  ERA5  k_eq = 0.198 d^-1
~~~

Thus interval normalization does not create one universal rate. It does,
however, show why the raw contrast between mule-deer \(|\lambda|=0.107\)
and wigeon \(|\lambda|=0.750--0.811\) should not be read as a seven-fold
difference in whole-migration correction.

The wigeon source contains 32 animal-years from 28 unique individuals, with a
mean and median of seven consecutive staging transitions per animal-year.
Under the explicitly homogeneous-coefficient retained-memory summary,

\[
R_{\rm path}(7)=0.133
\]

for the registered POWER estimate and

\[
R_{\rm path}(7)=0.231
\]

for the independent ERA5 reconstruction. These values are the same order as
the retrospective whole-spring-migration mule-deer retention
\(R=0.107\).

This apparent convergence is not promoted as a universal controller
coefficient. Under the frozen wigeon SIMEX sensitivity range, the same
seven-transition retained-memory component spans approximately 0.206--0.627.
Measurement-error assumptions therefore remain large enough to prevent a claim
that all taxa remove a common 80--90% fraction of phase deviation over one
migration.

Mule deer show speed and stopover compensation, and highlighted barnacle-goose
transitions show strong stopover-mediated control. Wigeon remains diagnostic:
phase contraction replicated under POWER and ERA5, whereas the negative
stopover association was supported only on the registered POWER phase surface.

The shared object is therefore the **phase-retention estimator form**. Raw
cross-system \(\lambda\) magnitudes are segment-scale quantities;
interval-standardized retained-memory summaries are secondary comparison
coordinates, and actuator architecture remains system- and
reconstruction-dependent.

### Environmental predictability and feedback strength are separate channels

Five stable barnacle-goose transitions with matched environmental reconstructions occupied distinct combinations of environmental innovation and phase retention.

For example, Greenland R2→R3 combined relatively large environmental innovation (5.28 d) with strong phase reset (\(|\lambda|=0.131\)), whereas Barents R2→R3 combined lower innovation (3.59 d) with weaker correction (\(|\lambda|=0.538\)). A near-reset Barents transition (\(|\lambda|\approx0.009\)) still retained an environmental-innovation floor of about 6.08 d.

Across seven matched transition pairs, the initial prediction that higher phenological predictability should imply stronger behavioral correction was not supported:

\[
\rho_{\rm Spearman}
=
-0.464,\qquad p=0.294.
\]

The sample is small and non-independent, so the result does not imply a general negative relationship. It does show that environmental predictability cannot be equated with feedback gain.

### Industrial development attenuates movement control, but not with the predicted extra time trend

The industrial-mule-deer archive provided 64,539 GPS positions from 137 animals and 253 animal-years. The primary control-permeability comparison was estimable for 188 animal-years from 103 animals.

Median \(G\) was

~~~text
small-development population = 1.656
large-development population = 1.037
~~~

and the clustered large-development population shift in \(\log G\) was

\[
-0.476\pm0.197,\qquad p=0.017.
\]

The large-development population had lower median \(G\) under all eight registered near/far definitions. A step-level individual-year fixed-effect analysis likewise detected attenuation of the edge-associated movement response in the large-development population (\(p=0.038\)).

The stronger longitudinal prediction was not supported. The year-by-large-development interaction was

\[
0.0405\pm0.0411,\qquad p=0.327,
\]

and remained non-significant across the registered sensitivity grid. Thus the reanalysis supports an actuation contrast but not progressive temporal deterioration of the registered permeability metric.

### Industrial-development phase retention: preregistered within-taxon test

<!-- AIKENS_LAMBDA_RESULTS_START -->
[AIKENS LAMBDA RESULT PENDING — render from the registered result JSON before submission.]
<!-- AIKENS_LAMBDA_RESULTS_END -->

## Cross-taxon direct-controller summary

**Table 1. Registered primary direct phase-retention systems.** Raw \(\lambda\) is a segment-scale estimator. \(k_{\rm eq}\) is the frozen secondary equivalent decay constant using the median observed interval and is not a fitted continuous-time controller rate.

| Taxon / system | Interval | Median \(\Delta t\) (d) | \(\lambda\) | \(k_{\rm eq}\) (d\(^{-1}\)) | Detected actuator architecture |
| --- | --- | ---: | ---: | ---: | --- |
| Mule deer | Full spring migration | 47.0 | 0.107 | 0.047 | Movement speed + stopover |
| Barnacle goose, Svalbard | Southern Norway → Svalbard | 14.8 | −0.106 | 0.151 magnitude decay; overshoot sign retained | Stopover + overtake |
| Barnacle goose, Greenland | R2 → R3 | 18.5 | 0.131 | 0.110 | Stopover |
| Barnacle goose, Barents | R1 → R2 | 26.6 | 0.494 | 0.026 | Stopover |
| Eurasian wigeon | Consecutive staging transitions | 1.06 | 0.750 POWER; 0.811 ERA5 | 0.273 POWER; 0.198 ERA5 | Phase contraction replicates; POWER stopover association not replicated under ERA5 |

The three barnacle-goose rows are within-taxon route replications and are not
treated as independent taxonomic observations. Whole-route cumulative
retention is not constructed for these fixed goose transitions. For wigeon,
the typical observed seven-transition animal-year gives retained-memory
\(R_{\rm path}=0.133\) under POWER and 0.231 under ERA5.

## Discussion

### The broad result is the absence of a universal speed rule

The broad bird analysis is the strongest independent test in the empirical programme because it spans 55 species rather than a handful of reconstructed controller systems. It does not support a single natural animal-to-environment speed optimum. Raw mismatch favored a point well below one, local phase centering moved the point estimate toward one, but the surface remained shallow and species-level optima were heterogeneous. No measured moderator recovered a convincing universal rule.

That negative result is the macroecological conclusion, not a failed prelude. A single speed ratio is too coarse because migration systems differ in target phase, route structure, opportunities to wait, and the interval over which correction is expressed.

The direct systems are therefore used to explain the failure rather than to replace one universal constant with another. Mule deer, barnacle geese and wigeon all show phase transformation, but they do so through different actuator architectures and on markedly different segment scales. Phase retention provides a common mathematical language for those feedbacks; interval standardization makes clear that the raw coefficient itself is not the invariant.

### Direct controller systems explain how the universal rule breaks

Mule deer, barnacle geese and wigeon all admit direct phase-retention
representations, but unequal segment durations show why a common regression
form is not the same as a common biological rate. The interval-standardized
analysis narrows the comparison: wigeon transition-scale retention accumulates
to a migration-sequence memory component of the same order as whole-migration
mule-deer retention under the naive POWER and independent ERA5
reconstructions, while SIMEX sensitivity prevents a universal magnitude claim.
The wigeon replicate calibration also shows why the response coordinate and
actuator layer must remain separate.

Mule deer combine movement-speed acceleration and stopover shortening.
Barnacle geese show strong stopover-mediated STEP control with overtaking in
some route stages. Under the registered POWER reconstruction, wigeon also show
a negative stopover response, but this association weakens and is unsupported
when phase is reconstructed independently from source-faithful ERA5. By
contrast, \(\hat\lambda\) remains below one under both POWER and ERA5 on the
same 224 transitions.

The wigeon comparison therefore supplies a within-system robustness test of the
two-gate architecture: a phase-retention signal can replicate while one proposed
actuator does not. This is more informative than classifying an entire taxon as
having or lacking a common controller mechanism.

Preregistered POWER-to-ERA5 substitutions in the three highlighted
barnacle-goose flyways provide the complementary case. Greenland R2->R3 changed
only from \(\hat\lambda=0.131\) to 0.144, Barents R1->R2 from 0.494 to
0.515, and Svalbard R2->R4 retained a negative overshoot coefficient while
shifting from -0.106 to -0.287. Negative stopover slopes remained supported
under ERA5 in all three transitions. Response and actuator reliability therefore
need to be evaluated as separate system-by-estimand properties: both layers
were stable across the highlighted barnacle transitions, whereas only the
response coordinate was stable in wigeon.

### Information and feedback solve different parts of the same timing problem

The barnacle-goose multi-flyway analysis also falsified a tempting but overly simple prediction: more predictable environments did not show stronger direct feedback correction in the current transition screen.

This distinction matters mechanistically. Environmental predictability reduces uncertainty before the animal experiences the next condition, an information problem already emphasized in migration theory and stopover studies (Kölzsch et al., 2015; Bauer et al., 2020). Feedback alters error after mismatch exists. A highly predictable route can therefore maintain precise timing with relatively weak reactive correction, while an unpredictable route may require stronger correction after new error is introduced.

The variance decomposition

\[
V_{i+1}
=
\lambda_i^2V_i+\sigma_{\xi,i}^2+\sigma_{\eta,i}^2
\]

is not new mathematics, but it makes an important ecological distinction explicit: feedback can remove inherited error, whereas it cannot remove environmental innovation that has not yet entered the system.

### Actuation constraints are distinct from information constraints

The industrial-mule-deer analysis supplies a quantitative boundary case. Relative movement response near the development footprint was consistently lower in the large-development population, supporting the idea that movement control can be attenuated even when a corridor remains physically traversable.

At the same time, the stronger temporal-deterioration prediction failed. This prevents the perturbation system from becoming a post hoc confirmation exercise. The framework gains credibility only if its stronger extensions are allowed to fail.

### Does actuation attenuation propagate into phase retention?

<!-- AIKENS_LAMBDA_DISCUSSION_START -->
[AIKENS LAMBDA DISCUSSION PENDING — render from the registered result JSON before submission.]
<!-- AIKENS_LAMBDA_DISCUSSION_END -->

### There is no single axis of “tracking ability”

The combined results imply at least three separable sources of apparent phenological mismatch:

1. environmental innovation: the next seasonal state is difficult to predict;
2. phase retention: realized error is only weakly corrected;
3. actuation limitation: the animal cannot express the movement response available in less constrained settings.

A fourth boundary arises when the animal changes the resource wave itself, as in ecosystem-engineering systems such as bison. In that case the environment is not an external target and a one-way tracking model becomes inappropriate.

These mechanisms can produce similar observed arrival mismatch while implying different ecological processes and different responses to climate or landscape change.

### Limitations

The current comparison spans three directly reconstructed taxa, not a global
sample of migration strategies. Barnacle-goose flyways are repeated routes
within one species and are not independent taxonomic replicates. Observation
intervals differ among continuous and stopover-based systems, so raw
\(\lambda\) should be interpreted as phase retention over a declared
ecological correction interval rather than per unit time. We therefore froze
the secondary \(k_{\rm eq}\) and retained-memory standardization before the
Aikens outcome was opened. This removes an obvious scale ambiguity but does not
turn a pooled discrete regression into a fitted continuous-time controller:
interval distributions remain broad, route stages can differ, and innovations
enter between transitions.

Environmental reconstructions are heterogeneous. For wigeon, the initial
registered ERA5-Land error-calibration lane failed its 90% event-coverage gate
and remains a failure. A separately frozen source-faithful ERA5 hourly follow-up
achieved 256/256 coverage and reproduced the estimator-scale contraction on all
224 transitions. The two environmental surfaces nevertheless shifted
\(\hat\lambda\) from 0.750 to 0.811 and changed the stopover result from
supported under POWER to unsupported under ERA5. In the three
preregistered barnacle-goose fixed transitions, by contrast, POWER-to-ERA5
substitution preserved the qualitative phase response and supported negative
stopover slopes. Greenland and Barents \(\hat\lambda\) shifted by only
0.013--0.021, while the Svalbard overshoot remained negative
(-0.106 under POWER; -0.287 under ERA5). These replicate calibrations increase
confidence in reconstruction robustness for those specific rows, but do not
identify a gold-standard error distribution.

Errors-in-variables bias remains important. The complete POWER-versus-ERA5
replicate calibration and event-structure SIMEX show that plausible frozen
error allocations move wigeon \(\lambda\) upward, with SIMEX extrapolations
from 0.798 to 0.935. Replicate disagreement does not identify a gold-standard
error distribution, so these values are sensitivity diagnostics rather than
corrected truth. A common independent-classical-error stress calculation
identifies wigeon as the most error-fragile highlighted positive system, whereas
the strongest mule-deer and goose contractions would require error SDs
comparable to most of their observed predictor-phase variation under that
specific null. Cross-taxon magnitude differences nevertheless cannot yet be
attributed entirely to controller biology.

All direct results are observational. Phase contraction does not by itself
demonstrate that the measured controller maximizes lifetime fitness or evolved
specifically to minimize phenological error. Finally, the industrial-development
comparison cannot isolate development causally from all population and landscape
differences.

### Outlook

The immediate next step is neither a pooled universal \(\lambda\) nor mechanical
taxonomic expansion. The main macroecological result already comes from the
55-species test; adding more direct taxa would not strengthen that result by
simple counting.

The sharper next tests concern mechanism. First, the preregistered
industrial-mule-deer perturbation asks whether a forcing regime that
independently attenuates movement control also changes phase retention while
holding taxon fixed. Second, independent reliability calibration should be
added for the mule-deer phase coordinate before remaining cross-system
differences in standardized retention are interpreted biologically. The current reliability contrasts
already show two distinct cases: wigeon phase retention reproduces while one
proposed actuator does not, whereas the highlighted Greenland, Barents and
Svalbard goose transitions reproduce both phase transformation and stopover
response across POWER and ERA5.

Future taxa should therefore be added only when they test a new inferential
boundary--for example a preregistered approach to \(\lambda\approx1\), a sign
change or overshoot boundary, or a discriminating actuator prediction--rather
than simply increasing panel size. The organizing state now separates raw interval scale from the secondary
standardization:

\[
(\sigma_\xi,\ \hat\lambda,\ \Delta t,\ k_{\rm eq},
\ R_{\rm path},\ \text{actuator architecture},
\ \text{reliability state}).
\]

This framework yields testable predictions for climate change. Increasing
interannual or spatial innovation can worsen timing even if behavioral control
remains unchanged. Conversely, infrastructure can increase mismatch by
attenuating actuation even if environmental predictability is stable. Systems
with strong resource engineering require coupled animal--environment dynamics
rather than the exogenous-wave approximation.

PAYOFF-B1 and the empirical macro programme therefore remain distinct but
connected. PAYOFF-B1 gives an exact benchmark for fixed-rate timescale matching
in a periodic environment. The empirical programme tests which parts of that
temporal-control language survive source reconstruction, measurement error and
real ecological forcing.

## Conclusion

The primary empirical conclusion is negative but general: phenological migration does not collapse onto one natural animal-to-environment speed optimum. Across 55 bird species, the location of the apparent optimum depended on phase centering and remained shallow and heterogeneous rather than defining one portable speed rule.

The direct controller systems explain why. Incoming phase deviation can be transformed through movement speed, stopover and route-stage responses, but the resulting retention coefficient is conditional on the ecological interval over which correction is measured. Interval standardization shrinks some apparent between-system differences without producing a new universal migration-wide coefficient.

Separating phase retention from environmental innovation clarifies why precise migration timing can arise through predictable environments, strong realized correction, or both. Quantitative disturbance evidence further shows that actuation can be attenuated without supporting every stronger temporal prediction.

<!-- AIKENS_LAMBDA_CONCLUSION_START -->
[AIKENS LAMBDA CONCLUSION PENDING — render from the registered result JSON before submission.]
<!-- AIKENS_LAMBDA_CONCLUSION_END -->

The resulting picture is therefore not “one optimal speed” and not “one universal \(\lambda\).” It is a family of phase-control problems whose feedback architecture and correction scale differ among systems. The macroecological regularity is the failure of a universal speed rule; the mechanistic regularity is that migrants can actively transform phase error through system-specific feedback.

## Data and Code Availability Statement

All analyses use previously published public datasets or archived source data. Reproducible analysis code, registered claim boundaries, data-source receipts and derived non-sensitive outputs will be archived in an anonymized reviewer-access repository at submission. The blinded manuscript will use a private reviewer link so that repository ownership does not compromise double-anonymous review. Original datasets remain available from their cited source repositories and DOIs.

## Figure legends

**Figure 1. Phase is not the same as zero lag.** Conceptual geometry showing animal and environmental timing surfaces, a nonzero characteristic phase offset, continuous phase-error feedback, and the distinction between target phase and correction strength.

**Figure 2. Broad bird data do not support one universal natural speed-ratio optimum.** Raw and local-phase-centered arrival–green-up mismatch across the 55-species dataset, with species-level curvature/vertex diagnostics and the registered null moderator scan.

**Figure 3. Mule deer correct phenological phase through movement speed and stopover behavior.** Initial phase versus relative movement speed, initial phase versus stopover duration, start-to-end phase compression, and annual controller estimates.

**Figure 4. Segment-scale phase retention spans heterogeneous migration regimes.** (A) Raw taxon-level phase retention \(|\lambda|\) on each declared ecological interval. These coefficients share an estimator form but are not interpreted as directly comparable biological rates; interval-standardized retained-memory summaries are reported separately in the text and Table 1. The barnacle-goose point is the declared route median and the whisker is the observed route range, not a confidence interval. (B) Environmental innovation versus raw \(|\lambda|\) for stable barnacle-goose transitions. Transition points share species, routes, and individuals and are not independent study estimates.

**Figure 5. Industrial development attenuates relative movement control but does not show the predicted extra temporal decline.** (A) Median control permeability \(G\) for small- and large-development populations across all registered near/far distance definitions. (B) Year-by-large-development interaction estimates and 95% intervals across the same definitions; all intervals include zero.

## References

- Aikens, E. O., Kauffman, M. J., Merkle, J. A., Dwinnell, S. P. H., Fralick, G. L., & Monteith, K. L. (2017). The greenscape shapes surfing of resource waves in a large migratory herbivore. *Ecology Letters, 20*, 741–750. https://doi.org/10.1111/ele.12772
- Aikens, E. O., Wyckoff, T. B., Sawyer, H., & Kauffman, M. J. (2022). Industrial energy development decouples ungulate migration from the green wave. *Nature Ecology & Evolution, 6*, 1733–1741. https://doi.org/10.1038/s41559-022-01887-9
- Amaral, B. R., Youngflesh, C., Tingley, M., & Miller, D. A. W. (2025). Shifting gears in a shifting climate: Birds adjust migration speed in response to spring vegetation green-up. *Diversity and Distributions, 31*, e70033. https://doi.org/10.1111/ddi.70033
- Bauer, S., McNamara, J. M., & Barta, Z. (2020). Environmental variability, reliability of information and the timing of migration. *Proceedings of the Royal Society B: Biological Sciences, 287*, 20200622. https://doi.org/10.1098/rspb.2020.0622
- Bischof, R., Loe, L. E., Meisingset, E. L., Zimmermann, B., Van Moorter, B., & Mysterud, A. (2012). A migratory northern ungulate in the pursuit of spring: Jumping or surfing the green wave? *The American Naturalist, 180*, 407–424. https://doi.org/10.1086/667590
- Forchhammer, M. C., Post, E., & Stenseth, N. C. (2002). North Atlantic Oscillation timing of long- and short-distance migration. *Journal of Animal Ecology, 71*, 1002–1014. https://doi.org/10.1046/j.1365-2656.2002.00664.x
- Geremia, C., Merkle, J. A., Eacker, D. R., Wallen, R. L., White, P. J., Hebblewhite, M., & Kauffman, M. J. (2019). Migrating bison engineer the green wave. *Proceedings of the National Academy of Sciences, 116*, 25707–25713. https://doi.org/10.1073/pnas.1913783116
- Kölzsch, A., Bauer, S., de Boer, R., Griffin, L., Cabot, D., Exo, K.-M., van der Jeugd, H. P., & Nolet, B. A. (2015). Forecasting spring from afar? Timing of migration and predictability of phenology along different migration routes of an avian herbivore. *Journal of Animal Ecology, 84*, 272–283. https://doi.org/10.1111/1365-2656.12281
- Laforge, M. P., Vander Wal, E., Webber, Q. M. R., Geremia, C., Kauffman, M. J., McWhirter, D. E., Middleton, A., Mong, T. W., Monteith, K. L., Ortega, A. C., Sawyer, H., & Merkle, J. A. (2025). Consistent individual differences and plasticity in migration behaviour of three North American ungulates. *Ecology Letters, 28*, e70101. https://doi.org/10.1111/ele.70101
- Ortega, A. C., Aikens, E. O., Merkle, J. A., Monteith, K. L., & Kauffman, M. J. (2023). Migrating mule deer compensate en route for phenological mismatches. *Nature Communications, 14*, 2008. https://doi.org/10.1038/s41467-023-37750-z
- Post, E., Forchhammer, M. C., Stenseth, N. C., & Callaghan, T. V. (2001). The timing of life-history events in a changing climate. *Proceedings of the Royal Society B: Biological Sciences, 268*, 15–23. https://doi.org/10.1098/rspb.2000.1324
- Torstenson, M., & Shaw, A. K. (2025). Strength of seasonality and type of migratory cue determine the fitness consequences of changing phenology for migratory animals. *Oikos, 2025*, e10862. https://doi.org/10.1111/oik.10862
- van Toor, M. L., Kharitonov, S., Švažas, S., Dagys, M., Kleyheeg, E., Müskens, G., Ottosson, U., Žydelis, R., & Waldenström, J. (2021). Migration distance affects how closely Eurasian wigeons follow spring phenology during migration. *Movement Ecology, 9*, 61. https://doi.org/10.1186/s40462-021-00296-0

## Claim ceiling

This manuscript supports:

- **as the primary cross-system result**, failure of a universal natural speed-ratio optimum in the registered 55-species broad bird test;
- source-faithful naive phase-retention estimates in mule deer, barnacle goose and prospectively tested wigeon;
- a pre-Aikens observation-error recovery analysis showing that the wigeon estimator remains below true-lambda=1 null expectations across frozen replicate-disagreement sensitivities, while the registered ERA5-Land calibration itself fails its coverage gate;
- **as mechanistic decomposition rather than independent meta-analytic replication**, source-faithful phase-retention estimates in three direct taxa, including wigeon contraction reproduced under independent POWER and ERA5 environmental surfaces;
- a pre-Aikens interval-standardization contract separating raw segment-scale λ from equivalent daily magnitude decay and homogeneous path-memory retention;
- wigeon typical seven-transition retained-memory values of about 0.133 (POWER) and 0.231 (ERA5), while the conservative SIMEX sensitivity permits substantially greater retained memory;
- separation of environmental innovation from realized phase retention;
- a quantitative industrial-development actuation contrast with a falsified stronger longitudinal prediction.

It does not support:

- a universal phase-retention coefficient;
- treating the three direct taxa as three independent estimates of one universal biological controller;
- direct biological ranking of taxa by raw λ magnitude across incompatible interval definitions;
- a universal claim that migration removes 80–90% of phase deviation;
- a final measurement-error-corrected latent wigeon lambda or a completed cross-taxon reliability correction;
- one common reactive behavioral mechanism across taxa, or a robust wigeon stopover actuator across environmental reconstructions;
- a causal effect of predictability on feedback strength;
- an evolutionary fitness optimum for the empirical \(\lambda\) values;
- causal attribution of the industrial population contrast solely to development;
- a claim that the generic control/AR mathematics is novel.
