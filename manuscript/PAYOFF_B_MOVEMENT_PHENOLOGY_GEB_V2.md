# Migration timing as phase control: environmental information and phase retention across migratory taxa

**Running title:** Phase control of migration

## Abstract

**Aim:** Migratory phenology is usually compared using arrival mismatch, movement speed or resource-surfing scores. We test whether a common phase-retention coordinate can compare how realized animal–environment timing deviations are transformed during migration while separating this process from environmental predictability.

**Location:** Eastern North America, the western United States, North Atlantic–Arctic barnacle-goose flyways, and the Eurasian wigeon migration corridor.

**Time period:** Published movement and phenology datasets spanning 2002–2020, with longer environmental baselines used where required for phenology reconstruction.

**Major taxa studied:** Migratory birds and ungulates, with direct controller reconstructions for mule deer (*Odocoileus hemionus*), barnacle goose (*Branta leucopsis*) and Eurasian wigeon (*Mareca penelope*).

**Methods:** We first reanalysed 5,816 bird-year-cell observations from 55 migratory species to test a universal movement-to-phenology speed-ratio prediction. We then defined signed phenological phase, (E=T_a-T_e), and estimated phase retention, (lambda), from (E_{next}=a+lambda E_{current}+epsilon) over ecologically meaningful movement intervals. We reconstructed direct phase dynamics from public biologging and environmental data, estimated environmental timing innovation separately from retained phase error, and tested an industrial-development perturbation of movement control.

**Results:** Broad bird data did not support one universal natural speed optimum. Direct systems instead showed significant phase contraction with strongly heterogeneous retention: mule deer (|lambda|approx0.11), primary barnacle-goose transitions (|lambda|approx0.11)–0.49, and wigeon (|lambda|approx0.86). Behavioral implementation differed: mule deer used speed and stopover adjustments, barnacle geese used stage-specific stopover control and overtaking, whereas wigeon showed weak contraction without detected stopover or travel-speed responses. Environmental predictability did not map monotonically onto feedback strength. Industrial development reduced a registered movement-control permeability proxy, but the stronger predicted temporal deterioration was unsupported.

**Main conclusions:** Phenological migration is better compared through the fraction of incoming phase deviation retained after movement than through a universal migration rate or zero-lag target. Environmental information and realized phase correction are separable channels, and a common phase-retention coordinate can reveal generality while preserving taxon- and route-specific controller architecture.

**Keywords:** animal tracking, biologging, environmental predictability, green wave, macroecology, migration, phenological mismatch, phase retention, plasticity, spring phenology

## Introduction

Seasonal migration is a tracking problem. Animals move through landscapes in which food availability, temperature, snowmelt, vegetation development, and breeding opportunity change in both space and time. A large literature shows that migrants can follow green-up, adjust migration timing, alter stopover behavior, and respond to spatial variation in the predictability of spring. The same literature also shows striking departures from continuous tracking: some migrants jump between seasonal ranges, some overtake a green wave near breeding sites, infrastructure can decouple movement from phenology, and large herbivores can modify the vegetation dynamics they appear to track.

These results are usually expressed with system-specific quantities: days from peak green-up, arrival relative to onset of spring, migration speed, stopover duration, a green-wave surfing score, or a reaction-norm slope. Each is biologically meaningful, but they do not provide an obvious common response variable for comparing how strongly different movement systems preserve or correct phenological phase.

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

as a common phase-retention coordinate. Values below one indicate phase contraction, values near zero indicate near-complete reset, negative values indicate contraction with overshoot, and magnitudes above one indicate local amplification. Importantly, the same \(\lambda\) can arise through different mechanisms.

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

We therefore tested four linked predictions. First, a broad universal speed optimum should fail if systems differ in target phase and controller architecture. Second, direct phase contraction should nevertheless be measurable across taxonomically different migrants. Third, environmental predictability and realized phase correction should act as separable channels rather than necessarily covarying positively. Fourth, a perturbation that constrains movement should attenuate realized control even if the migration corridor remains spatially traversable.

## Methods

### Broad bird test of a universal timescale optimum

We reanalyzed the published Amaral et al. migration-front dataset, containing spring migration and vegetation green-up estimates for 55 eastern North American migratory bird species across 2002–2017. After the registered completeness and velocity filters, the analysis contained 5,816 species-year-cell observations.

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

#### Mule deer

For Ortega et al. mule deer, we used the official Nature Communications source-data workbook. The dataset provided 152 animal-years from 72 individuals across eight years. Phase was expressed as days from peak instantaneous rate of green-up. Published movement-rate and stopover summaries were combined with annual green-wave propagation estimates. We quantified the association between initial phase and relative animal-to-environment movement speed, stopover duration, and phase at migration end. Individual-clustered uncertainty was used for repeated animals.

#### Barnacle geese

For Svalbard, Greenland, and Barents barnacle geese, we reconstructed spring stopovers from public Movebank GPS data using a common stay-region pipeline and independently reconstructed annual spring-onset anomalies from daily temperature. For fixed region-to-region transitions, unknown constant regional timing anchors shift intercepts but not the slope \(\lambda\), allowing anchor-invariant phase-transfer estimation.

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

The wigeon analysis was preregistered internally before promotion of a direct result. We reconstructed the original Movebank source, published four-state HMM parameters, track filtering, staging events, and the published 5 °C thermal-growing-season definition. The movement reconstruction was required to pass gates against reported trajectory counts, individual counts, endpoint distances, and migration speed. The independent environmental reconstruction was required to reproduce the published staging-event phase distribution within registered tolerance.

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

### Environmental information and innovation

For fixed barnacle-goose region pairs we modeled destination spring anomaly from origin spring anomaly. The residual standard deviation

\[
\sigma_\xi
\]

was used as the environmental innovation scale. We compared this quantity descriptively with direct phase retention \(|\lambda|\). Transition rows share species, routes, and sometimes individuals, so they were not analyzed as independent studies.

### Industrial-development actuation test

We reanalyzed the archived spring-migration GPS and development-footprint shapefiles from Aikens et al. Coordinates were transformed into the GPS reference system before calculating distances.

For each animal-year we defined a movement control-permeability proxy

\[
G
=
\frac{\operatorname{median}(\text{speed near development boundary})}
{\operatorname{median}(\text{speed far from development boundary})}.
\]

The primary contrast defined “near” as within 2 km and “far” as at least 10 km from the relevant footprint. Seven additional registered near/far combinations were used for sensitivity. We compared the small- and large-development populations and tested the stronger prediction that the difference became more negative through time. A second model used movement steps with individual-year fixed effects.

### Cross-taxon synthesis and claim control

We reduced the direct registry to one descriptive record per taxon before cross-taxon presentation. Barnacle-goose routes contribute an observed within-taxon range, not independent meta-analytic weights. At three taxa we did not estimate a pooled universal \(\lambda\).

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

### Wigeon prospectively confirm weak phase contraction and falsify near-reset convergence

The wigeon movement reconstruction recovered 33 spring trajectories from 29 individuals, compared with 35 trajectories from 31 individuals in the published analysis. Median endpoint distance was 1,911 km versus 1,899 km published. The registered movement reconstruction gates all passed.

The independent thermal-growing-season reconstruction linked 256 staging events to local TGS. Median arrival phase was 20.93 d after TGS onset, compared with 22.5 d published, and the registered event-count, median-phase, and IQR-overlap gates passed.

Across 224 consecutive staging transitions from 28 individuals,

\[
\beta_E=-0.1401\pm0.0451,
\]

so

\[
\lambda=0.8599.
\]

The no-correction null \(\lambda=1\) was rejected (\(p=0.00190\)). Thus approximately 14% of incoming phase deviation was removed per reconstructed staging transition.

The stronger prospective forecast

\[
|\lambda|<0.75
\]

was not supported. Stopover duration showed essentially no phase response (\(p=0.972\)), and measured between-staging travel speed also lacked convincing phase dependence (\(p=0.197\)). Wigeon therefore validate a common phase-retention coordinate without reproducing the reactive speed/stopover mechanisms detected in mule deer and barnacle geese.

### Three taxa share a coordinate, not a universal controller

The direct taxon-level phase-retention summaries span a broad range:

~~~text
Mule deer:
  |lambda| ~ 0.107

Barnacle goose:
  median |lambda| ~ 0.131
  highlighted route range ~ 0.106–0.494

Eurasian wigeon:
  |lambda| ~ 0.860
~~~

All declared taxon-level primary examples show contraction, but correction strength ranges from approximately 0.14 to 0.89. The data therefore reject both a universal near-reset expectation and a universal actuator coefficient.

Instead, phase retention is portable as a measurement coordinate while controller architecture is heterogeneous.

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

## Cross-taxon direct-controller summary

**Table 1. Registered primary direct phase-retention systems.** The common coordinate is phase retention (|\lambda|); actuator coefficients are not assumed to be mechanistically interchangeable across taxa.

| Taxon / system | Interval | \(\lambda\) | \(|\lambda|\) | Correction strength \(1-|\lambda|\) | Detected actuator architecture |
| --- | --- | ---: | ---: | ---: | --- |
| Mule deer | Full spring migration | 0.107 | 0.107 | 0.893 | Movement speed + stopover |
| Barnacle goose, Svalbard | Southern Norway → Svalbard | −0.106 | 0.106 | 0.894 | Stopover + overtake |
| Barnacle goose, Greenland | R2 → R3 | 0.131 | 0.131 | 0.869 | Stopover |
| Barnacle goose, Barents | R1 → R2 | 0.494 | 0.494 | 0.506 | Stopover |
| Eurasian wigeon | Consecutive staging transitions | 0.860 | 0.860 | 0.140 | Net phase retention; no detected speed/stopover actuator |

The three barnacle-goose rows are within-taxon route replications and are not treated as independent taxonomic observations.

## Discussion

### A failed universal-optimum hypothesis reveals a more useful invariant

The broad bird analysis was designed as a direct transport test of the PAYOFF-B timescale idea. Its failure is therefore part of the result, not a nuisance. Raw animal-to-environment speed matching does not collapse heterogeneous migration systems onto one optimum. Once system-specific phase is recognized, however, a more transferable question appears: how much incoming phase deviation is retained after movement?

This reframing preserves the temporal core of PAYOFF-B without claiming that a two-patch fixed-rate optimum should appear literally in continuous natural migrations.

### Phase retention is more portable than behavioral gain

Mule deer, barnacle geese, and wigeon all admit a direct phase-retention representation, but their actuator architectures differ sharply.

Mule deer combine movement-speed acceleration and stopover shortening. Barnacle geese show strong stopover-mediated STEP control, with deliberate overtake in some route stages. Wigeon exhibit much weaker but significant phase contraction without a detected stopover or transit-speed response.

The third taxon is therefore more valuable than a simple replication. It falsifies the emerging stronger idea that successful tracking requires near-complete reactive reset. A common response variable survives while the common mechanism does not.

### Information and feedback solve different parts of the same timing problem

The barnacle-goose multi-flyway analysis also falsified a tempting but overly simple prediction: more predictable environments did not show stronger direct feedback correction in the current transition screen.

This distinction matters mechanistically. Environmental predictability reduces uncertainty before the animal experiences the next condition. Feedback alters error after mismatch exists. A highly predictable route can therefore maintain precise timing with relatively weak reactive correction, while an unpredictable route may require stronger correction after new error is introduced.

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

### There is no single axis of “tracking ability”

The combined results imply at least three separable sources of apparent phenological mismatch:

1. environmental innovation: the next seasonal state is difficult to predict;
2. phase retention: realized error is only weakly corrected;
3. actuation limitation: the animal cannot express the movement response available in less constrained settings.

A fourth boundary arises when the animal changes the resource wave itself, as in ecosystem-engineering systems such as bison. In that case the environment is not an external target and a one-way tracking model becomes inappropriate.

These mechanisms can produce similar observed arrival mismatch while implying different ecological processes and different responses to climate or landscape change.

### Limitations

The current comparison spans three directly reconstructed taxa, not a global sample of migration strategies. Barnacle-goose flyways are repeated routes within one species and are not independent taxonomic replicates. Observation intervals differ among continuous and stopover-based systems, so \(\lambda\) should be interpreted as phase retention over a declared ecological correction interval rather than per unit time.

Environmental reconstructions are also heterogeneous. Wigeon validation uses an independent NASA POWER reconstruction rather than the original ERA5 grid, and barnacle-goose analyses use independently reconstructed annual phenology anomalies rather than byte-identical historical climate inputs. These reconstructions were validated against available published timing summaries and were handled with explicit claim ceilings.

All direct results are observational. Phase contraction does not by itself demonstrate that the measured controller maximizes lifetime fitness or evolved specifically to minimize phenological error. Finally, the industrial-development comparison cannot isolate development causally from all population and landscape differences.

### Outlook

The immediate next step is not to estimate a pooled universal \(\lambda\). A more useful macroecological expansion would increase taxonomic coverage while retaining the two-channel structure:

\[
(\sigma_\xi,\ |\lambda|,\ \text{actuator architecture}).
\]

This framework yields testable predictions for climate change. Increasing interannual or spatial innovation can worsen timing even if behavioral control remains unchanged. Conversely, infrastructure can increase mismatch by attenuating actuation even if environmental predictability is stable. Systems with strong resource engineering require coupled animal–environment dynamics rather than the exogenous-wave approximation.

PAYOFF-B1 and the empirical macro programme therefore remain distinct but connected. PAYOFF-B1 gives an exact benchmark for fixed-rate timescale matching in a periodic environment. The empirical results show that natural migrants solve the broader temporal problem through heterogeneous, state- and route-dependent transformations of phenological phase.

## Conclusion

Phenological migration does not collapse onto one natural migration rate, zero-lag target, or universal behavioral feedback coefficient. Across three directly reconstructed taxa, however, incoming phase deviation can be placed on a common retention coordinate. That coordinate spans weak to near-complete correction and is generated by different movement architectures.

Separating phase retention from environmental innovation clarifies why precise migration timing can arise through predictable environments, strong realized correction, or both. Quantitative disturbance evidence further shows that actuation can be attenuated without supporting every stronger temporal prediction.

The resulting picture is not a universal controller. It is a common phase-control problem with multiple ecological solutions.

## Data and Code Availability Statement

All analyses use previously published public datasets or archived source data. Reproducible analysis code, registered claim boundaries, data-source receipts and derived non-sensitive outputs will be archived in an anonymized reviewer-access repository at submission. The blinded manuscript will use a private reviewer link so that repository ownership does not compromise double-anonymous review. Original datasets remain available from their cited source repositories and DOIs.

## Figure legends

**Figure 1. Phase is not the same as zero lag.** Conceptual geometry showing animal and environmental timing surfaces, a nonzero characteristic phase offset, continuous phase-error feedback, and the distinction between target phase and correction strength.

**Figure 2. Broad bird data do not support one universal natural speed-ratio optimum.** Raw and local-phase-centered arrival–green-up mismatch across the 55-species dataset, with species-level curvature/vertex diagnostics and the registered null moderator scan.

**Figure 3. Mule deer correct phenological phase through movement speed and stopover behavior.** Initial phase versus relative movement speed, initial phase versus stopover duration, start-to-end phase compression, and annual controller estimates.

**Figure 4. A common phase-retention coordinate spans heterogeneous migration regimes.** (A) Taxon-level phase retention \(|\lambda|\). The barnacle-goose point is the declared route median and the whisker is the observed route range, not a confidence interval. (B) Environmental innovation versus \(|\lambda|\) for stable barnacle-goose transitions. Transition points share species, routes, and individuals and are not independent study estimates.

**Figure 5. Industrial development attenuates relative movement control but does not show the predicted extra temporal decline.** (A) Median control permeability \(G\) for small- and large-development populations across all registered near/far distance definitions. (B) Year-by-large-development interaction estimates and 95% intervals across the same definitions; all intervals include zero.

## References currently central to the claim boundary

- Bischof et al. 2012. A migratory northern ungulate in the pursuit of spring: jumping or surfing the green wave? *The American Naturalist*. DOI 10.1086/667590.
- Kölzsch et al. 2015. Forecasting spring from winter: predicting phenology of a migrant across its route. *Journal of Animal Ecology*. DOI 10.1111/1365-2656.12281.
- Bauer, McNamara & Barta 2020. Environmental variability, reliability of information and the timing of migration. *Proceedings of the Royal Society B*. DOI 10.1098/rspb.2020.0622.
- van Toor et al. 2021. Migration distance affects how closely Eurasian wigeons follow spring phenology during migration. *Movement Ecology*. DOI 10.1186/s40462-021-00296-0.
- Aikens et al. 2022. Industrial energy development decouples ungulate migration from the green wave. *Nature Ecology & Evolution*. DOI 10.1038/s41559-022-01887-9.
- Ortega et al. 2023. Phenological mismatch with environmental conditions is mitigated by compensatory plasticity in a migratory large herbivore. *Nature Communications*. DOI 10.1038/s41467-023-37750-z.
- Geremia et al. 2019. Migrating bison engineer the green wave. *Proceedings of the National Academy of Sciences*. DOI 10.1073/pnas.1913783116.

## Claim ceiling

This manuscript supports:

- failure of a universal natural speed-ratio optimum in the registered broad bird test;
- direct phase-retention estimates across three taxa;
- strong heterogeneity in retention magnitude and actuator architecture;
- separation of environmental innovation from realized phase retention;
- a quantitative industrial-development actuation contrast with a falsified stronger longitudinal prediction.

It does not support:

- a universal phase-retention coefficient;
- one common reactive behavioral mechanism across taxa;
- a causal effect of predictability on feedback strength;
- an evolutionary fitness optimum for the empirical \(\lambda\) values;
- causal attribution of the industrial population contrast solely to development;
- a claim that the generic control/AR mathematics is novel.
