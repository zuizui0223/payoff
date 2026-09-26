# Better information can transiently worsen seasonal coordination under unequal decision deadlines

**Status:** integrated ecology manuscript v2, PREOUTCOME  
**Relation to v1:** candidate replacement narrative for `PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md`; v1 remains retained for provenance.  
**Outcome boundary:** all Bayesian, information-timing, predictive-connectivity and temporal-buffering claims below are inherited from frozen receipts already in the repository. The preregistered Aikens phase-retention outcome remains unopened and is not required for the argument.

## Abstract

Seasonal organisms often act before the state they must match is observable. We ask how costly waiting for information changes coordination. An exact decision model shows that partners with different waiting costs begin using the same improving cue at different thresholds, producing synchronized ignorance, transient desynchronization and then informed resynchronization. In a three-player Bayesian game, transient information loss becomes strict lower-payoff hysteresis in complete and chain networks but not a migrant-star, separating shock transmission from ecological memory. Across 3,311 observations from 37 migratory bird species, stronger pre-outcome predictive connectivity is associated with smaller mismatch in a preregistered pooled analysis, although dependence-aware uncertainty is wider. A flycatcher experiment anchors timing-dependent information availability, whereas wigeon predictability does not strengthen post-error correction and a 31-year cue–driver series fails its preregistered reversal gate. Seasonal adaptation therefore depends on what organisms can know before a decision deadline and on which coordinated states remain historically accessible.

**Keywords:** phenology; migration; information; Bayesian game; social information; ecological memory; climate change; phenological mismatch

---

## 1. Introduction

Climate change is altering the seasonal timing of environments, resources and interacting species. Organisms can respond by shifting phenology, moving through space, changing behavior or combining these responses. Yet the response that would minimize mismatch is not always available at the moment a seasonal decision must be made.

This timing problem is especially acute for migrants. A resident plant or insect can respond directly to local spring conditions, whereas a long-distance migrant may initiate migration days or weeks before encountering the destination state it ultimately needs to match. Remote temperature, vegetation and photoperiod can provide predictive information, but cue reliability is imperfect and can change as spatial climate relationships change. Previous work has already established the key ingredients separately: migration timing depends on environmental predictability and the value of information (Bauer et al. 2020); environmental cues used by pied flycatchers can explain arrival without predicting the estimated annual fitness optimum (Tomotani et al. 2021); heterospecific phenology can provide social information after migrants arrive (Samplonius & Both 2017); and frequency-dependent selection can stabilize phenologies that differ from a simple fitness-maximizing date (Johansson & Jonzén 2012).

These results motivate a different question. If useful information exists but becomes available only after a costly decision deadline, **when should an organism act under uncertainty and when should it wait?** More importantly for interacting species, what happens when partners pay different costs of waiting and therefore begin using the same improving information at different thresholds?

The usual intuition is monotonic: better information should improve tracking. That intuition need not hold at the interaction level. At low cue quality, two partners may both ignore a cue and remain synchronized. As the cue improves, the lower-cost partner may begin waiting for and using it while the higher-cost partner still commits early. Better information then creates asymmetric information use and can increase mismatch. Only after the second partner also crosses its value-of-information threshold do the partners resynchronize.

A second problem follows once alternative timing strategies exist. A transient information shock can move an interaction network from one self-consistent timing regime to another. Even if information later recovers, unilateral incentives may prevent a return to the higher-payoff regime. The ecological consequence is history dependence: a short-lived informational perturbation can persist as a property of the interaction network.

We develop this argument in five steps. First, we derive an exact act-now versus wait-for-information threshold and show how interaction externalities create a private-versus-joint information-acquisition wedge. Second, we show that unequal decision deadlines generate a non-monotonic information-induced desynchronization window. Third, we embed asymmetric information in a three-player Bayesian timing game and ask which interaction topologies merely transmit an information shock and which store it as a strict lower-payoff equilibrium after information recovery. Fourth, we test separable pieces of the mechanism in natural systems: pre-commitment predictive connectivity across migratory birds, timing-dependent social information in a flycatcher experiment, and post-error phase correction in wigeon. Finally, we retain the earlier PAYOFF-B temporal-buffering result as a distinct **capacity barrier**, asking how information constraints interact conceptually with what organisms are physically able to do.

Our central prediction is not that information is generally beneficial or harmful. It is more specific:

> **Improving information can temporarily worsen phenological coordination when interacting species face different decision deadlines, and interaction topology can determine whether that transient desynchronization disappears or becomes ecological memory.**

---

## 2. Theory

### 2.1 Three barriers to seasonal adaptation

We distinguish three conceptually separate barriers.

**Capacity — cannot do it.** A response may be known but physiologically or spatially unavailable. In the retained movement–phenology model, finite timing capacity can delay but not indefinitely replace spatial redistribution.

**Information timing — cannot know it yet.** A future response may be physically available, but the state it should target is not yet observable. Waiting can improve information but carries opportunity costs.

**Strategic accessibility — cannot get there alone.** A jointly beneficial timing regime may exist, but an individual partner can lose by moving toward it unilaterally. Historical state therefore matters.

These barriers can coexist but should not be collapsed into one scalar “tracking ability.”

### 2.2 Act now or wait for information

Let the future seasonal state be (	hetain{0,1}), where state 1 is an early season, with prior probability (pi). The focal actor chooses an early or late action.

A false-early decision has cost (C_F); a missed-early decision has cost (C_M). Before observing a new cue, the minimum expected decision loss is

[
R_0 = min[(1-pi)C_F, pi C_M].
]

Suppose waiting reveals a symmetric binary cue with accuracy (q). After observing the cue, the actor chooses the lower-loss action for that posterior state. Let the resulting Bayes risk be (R_q). The private value of waiting for information is

[
V_{mathrm{private}}(q)=R_0-R_qge 0.
]

If delaying commitment costs (D), the actor waits only when

[
V_{mathrm{private}}(q)>D.
]

This produces an actionable-information threshold. A cue can become statistically more accurate without changing behavior if both cue outcomes still imply the same optimal action.

### 2.3 Interaction externalities create an information-acquisition wedge

A wrong timing decision can also harm partners through missed pollination, competition, resource mismatch or lost mutualistic overlap. Let (E_F) and (E_M) denote the partner losses associated with the two state errors. Replacing (C_F,C_M) with (C_F+E_F,C_M+E_M) gives the joint value of information,

[
V_{mathrm{joint}}(q).
]

Whenever

[
V_{mathrm{private}}(q)le D < V_{mathrm{joint}}(q),
]

the focal actor rationally commits before the cue while the interaction system would gain if it waited.

For the transparent witness

[
pi=0.40,quad C_F=2,quad C_M=1,quad q=0.90,
]

we obtain

[
V_{mathrm{private}}=0.24.
]

Adding one unit of partner loss to each error gives

[
V_{mathrm{joint}}=0.54.
]

Thus any delay cost between 0.24 and 0.54 creates a private-commit / joint-wait wedge.

### 2.4 Better information can transiently increase mismatch

Now consider two actors with the same future cue and the same state-loss function but different opportunity costs of waiting, (D_A>D_B).

With the canonical private information process and

[
D_A=0.30,qquad D_B=0.10,
]

actor B begins waiting when cue accuracy reaches approximately (q=0.82), whereas actor A does not wait until approximately (q=0.94).

Three regimes follow:

[
qle0.81:
quad
	ext{commit}mid	ext{commit},
]

[
0.82le qle0.93:
quad
	ext{commit}mid	ext{wait},
]

[
qge0.94:
quad
	ext{wait}mid	ext{wait}.
]

In the declared shared-cue model, expected action mismatch is therefore zero, then positive, then zero. It reaches 0.436 at the first threshold, (q=0.82).

The mechanism is **asynchronous information uptake**. Cue reliability improves monotonically; coordination does not.

### 2.5 Partial-information coordination and ecological memory

We next allow a flowering resource, a local pollinator and a migrant to choose cue-contingent timing policies. The migrant's cue can be less reliable than the local cues, and payoffs combine environmental timing error with interaction mismatch.

Sequential best response supplies an explicit historical accessibility rule. The initial high-information state is cue following by all three players. Migrant information is then degraded and subsequently restored.

We classify a recovered historical state as **strict lower-payoff hysteresis** only when:

1. the high-information baseline is all cue-following;
2. degrading migrant information changes at least one resident policy;
3. full recovery of migrant information does not restore the initial profile;
4. a higher-joint-payoff pure Bayesian equilibrium remains available; and
5. every player has a strictly positive unilateral best-response margin in the historical recovered state.

This excludes exact ties from the primary hysteresis claim.

---

## 3. Empirical tests and source-backed anchors

### 3.1 Broad predictive connectivity

The broad natural analysis uses the Amaral et al. migratory-bird dataset. For each species and breeding target cell, we identify the nearest southern migratory-range source cell using spatial metadata only.

For outcome year (t), predictive connectivity is estimated using the previous eight calendar years only. Source and destination green-up dates are detrended separately within the trailing window, and their signed residual correlation is retained as (ho). The focal outcome year is excluded.

The primary response is

[
log(1+|	ext{green-up day}-	ext{bird arrival day}|).
]

The preregistered prediction is a negative coefficient of predictive connectivity.

### 3.2 Timing-dependent social information

Samplonius & Both (2017) experimentally advanced or delayed resident tit hatching phenology and observed settlement by migratory pied flycatchers.

We use this study as a source-backed ecological anchor rather than a new reanalysis. The relevant contrast is temporal: most males settled before the manipulated hatching difference became apparent, whereas later female settlement occurred when heterospecific phenology was visible.

This system does not estimate the PAYOFF-B delay-cost parameters. It tests the narrower premise that information available to a later seasonal decision can be unavailable to an earlier one.

### 3.3 Post-error correction in Eurasian wigeon

The registered wigeon lane asks a different question. Using 224 consecutive staging transitions from 28 individuals, we estimate historical route-level predictive connectivity from 2000–2017 ERA5 seasonal-state reconstructions, before the 2018–2020 tracking outcomes.

The preregistered interaction asks whether higher predictive connectivity strengthens correction of phase error already present at a staging transition. This separates information available before commitment from feedback after error appears.

### 3.4 Long-term cue–driver reversal gate

Because cue–driver decoupling has already been proposed explicitly for pied flycatchers (Tomotani et al. 2021), we preregistered a stricter long-term question using 1980–2010 annual selection gradients from Visser et al. (2015).

A fixed Ivory Coast NCEP/NCAR temperature cue was reconstructed over a source-defined 20-day February window. Eight-year trailing cue–driver predictive connectivity was calculated without using the focal year.

A natural path-dependence analysis was licensed only if the information series first passed a frozen decline–recovery gate: a two-segment fit had to improve AICc by at least four, have a negative pre-break slope and positive post-break slope, and recover at least half of the predicted decline.

### 3.5 Capacity baseline

The retained PAYOFF-B moving-landscape models provide a separate capacity layer. Movement and timing are locally substitutable at fixed total restoring gain, but explicit landscapes impose finite phenological range, movement geometry and partner matching.

These models are not used to infer the information thresholds above. They ask what happens after a correct response is known but finite timing or spatial accessibility limits its expression.

---

## 4. Results

### 4.1 Waiting for information has a private and a joint threshold

Across the exact canonical phase map of cue accuracy 0.50–1.00 and delay cost 0–0.80, 2,848 of 4,131 cells produce commitment before the cue by both private and joint criteria, and 530 produce waiting under both criteria.

In **753 cells (18.2% of the declared design)**, however, the focal actor commits while the joint interaction system would benefit from waiting.

These grid fractions are design frequencies, not estimated natural prevalences. The exact qualitative result is the existence of a non-empty interval

[
V_{mathrm{private}}le D <V_{mathrm{joint}}.
]

### 4.2 Improving one shared cue can first desynchronize and then resynchronize partners

The unequal-delay witness generates a non-monotonic response to monotonically improving cue reliability.

Below (q=0.82), neither partner pays to wait. Between (q=0.82) and 0.93, only the lower-delay partner waits and uses the cue. Expected mismatch rises abruptly, reaching 0.436 at (q=0.82). At (qge0.94), both partners wait and mismatch returns to zero.

Thus:

[
	ext{shared ignorance}
ightarrow
	ext{asymmetric information use}
ightarrow
	ext{shared informed coordination}.
]

The surprising result is not that information can sometimes mislead. The information itself becomes more reliable throughout; mismatch appears because **partners begin using the same improving cue at different thresholds**.

### 4.3 Interaction topology determines whether an information shock is stored

The strict three-player phase diagram separates transient shock transmission from ecological memory.

Among eligible high-information cells:

| topology | eligible cells | resident cascade | strict lower-payoff hysteresis |
|---|---:|---:|---:|
| complete | 391 | 221 | **118** |
| chain | 364 | 194 | **52** |
| migrant-star | 404 | 367 | **0** |

The chain and migrant-star each contain two undirected edges, so the contrast is not interaction density alone.

The migrant-star readily transmits an information shock: resident cascades occur in 367/404 eligible cells. But no cell retains a strict lower-payoff historical state after information recovery.

By contrast, the chain

[
	ext{flower}--	ext{local pollinator}--	ext{migrant}
]

contains a substantial strict hysteresis region. Local coupling among destination partners can therefore store the historical consequence of a transient migrant information loss.

The primary interior witness uses local cue accuracy 0.875 and interaction strength 0.50. Under complete and chain topologies, migrant cue degradation leads from all-following to all-late timing, while full information recovery ends at late/late/follow. The historical state has strictly positive unilateral best-response margins, yet all-following is again a higher-joint-payoff equilibrium. Under the migrant-star, the same information recovery returns the system to all-following.

### 4.4 Broad natural data support a pooled predictive-information effect

The preregistered broad analysis contains 3,311 estimable observations from 37 species and 635 species–cell units.

Higher pre-outcome predictive connectivity is associated with smaller arrival–green-up mismatch:

[
hateta_{ho}=-0.0462,
]

with

[
95% mathrm{CI}=[-0.0870,-0.0054],
qquad p=0.0265.
]

The coefficient remains negative under the 10-year trailing-window sensitivity and under all leave-one-species-out and leave-one-year-out fits. Using raw, undetrended source–destination correlation instead produces essentially no effect ((etaapprox0.0043, p=0.831)), consistent with the distinction between interannual predictive information and a shared long-term climate trend.

The uncertainty is not uniformly strong across dependence structures. Cluster-robust intervals by species, cell-year and source–target pair include zero. Of 33 individually estimable species, 21 have negative coefficients and 12 positive; the inverse-variance species summary also includes zero.

We therefore treat this as **pooled directional support with dependence-sensitive uncertainty**, not a universal species-level coefficient.

### 4.5 Heterospecific phenology is informative only after it becomes visible

The flycatcher experiment provides an independent temporal anchor.

Male settlement among available boxes did not respond detectably to manipulated tit timing ((Z=0.854, p=0.393)); the study reports that almost all males had settled before the manipulated difference became apparent through tit hatching.

Later female settlement did respond. The published pairing model gives a tit-timing effect of −0.101 (SE 0.050, (p=0.042)), and the time-dependent Cox analysis gives −0.065 (SE 0.025, (p<0.009)). Treatment separation became stronger later in the settlement period.

This does not show that females deliberately delayed in order to collect information. It supports the narrower PAYOFF-B premise: **the same partner state can be unavailable to an early decision and behaviorally relevant to a later one.**

### 4.6 Predictive connectivity does not act as a universal post-error controller

In Eurasian wigeon, route predictive connectivity varied substantially among 17 staging-segment pairs, from approximately 0.21 to 0.91.

The preregistered interaction between incoming phase error and predictive connectivity was

[
hateta=+0.0202,
]

[
95% mathrm{CI}=[-0.1058,0.1461],
qquad p=0.756.
]

The registered negative prediction was therefore not supported.

This separates two informational roles:

[
	ext{information before commitment}

eq
	ext{correction after error appears}.
]

Predictive connectivity can matter for which timing decision is reached without necessarily increasing the strength of later corrective feedback.

### 4.7 The long-term cue–driver series fails the preregistered reversal gate

The 1980–2010 flycatcher cue–driver analysis yielded 25 estimable trailing-window correlations.

A single linear trend had slope −0.0174 per year. The best two-line fit changed near 2001 and improved AICc by 10.20, but its fitted slopes were both positive:

[
eta_{mathrm{pre}}=+0.00869,
qquad
eta_{mathrm{post}}=+0.04944.
]

The registered decline–recovery geometry therefore failed. Because there was no fitted pre-break decline, the recovery fraction was undefined and the path-dependence model was **not run**.

The series is visibly nonstationary, but it is not relabelled as natural hysteresis after inspection.

### 4.8 Capacity constraints remain distinct from information constraints

In the retained moving-landscape programme, finite phenological capacity expands persistence and delays movement, but movement re-enters under stronger sustained forcing.

With no phenological capacity, the largest persisted sampled forcing velocity was 0.030; with (z_{max}=5), it increased to 0.065. In the zigzag landscape with (z_{max}=4), phenology-only strategies were favored at forcing 0.04–0.05, while migration re-entered at 0.06 and increased further at 0.07.

Timing also reduced the immediate sampled growth penalty of a fragmented zigzag route from about −0.0419 at phenology limit 0 to −0.0070 at limit 4.

These results define a capacity boundary, not an information result. An organism can fail because it cannot perform a response even when the target state is known; the new theory shows that it can also fail earlier because the target state is not worth waiting to observe.

---

## 5. Discussion

### 5.1 Information quality and information use are different ecological variables

Ecological models often treat cue quality as a property of an environment–organism pair. Our results add a second coordinate: **whether the organism can afford to wait until that cue becomes useful**.

The same cue can therefore generate different effective information sets among partners without any difference in sensory physiology. An actor facing a large cost of delay commits early and remains prior-driven; another facing a smaller delay cost waits and becomes cue-responsive.

This distinction turns decision deadlines into a mechanism of ecological information asymmetry.

### 5.2 Better information can transiently worsen coordination

The non-monotonic information result is the central theoretical surprise.

At low cue quality, shared ignorance can be coordinating. At high cue quality, shared informed responses can also be coordinating. The vulnerable regime lies between them, when only part of the interaction system has crossed the value-of-information threshold.

This mechanism differs from an ecological trap caused by a misleading cue. Here the cue becomes **more accurate**, not less. Coordination worsens because adoption is asynchronous.

Climate change can plausibly move ecological systems through such intermediate regimes. It can alter cue reliability, seasonal predictability and the costs of delaying migration or breeding. The prediction is therefore not that improving forecasts harm organisms. It is that interacting species with different decision deadlines can respond non-monotonically to the same change in information quality.

### 5.3 Interaction networks can convert transient information asymmetry into memory

Asynchronous cue uptake becomes more consequential when timing decisions are strategically coupled.

The strict phase diagram shows that temporary information degradation can move a community into another self-consistent timing state. Whether that state disappears after information recovery depends on topology.

The migrant-star transmits shocks but does not retain strict lower-payoff hysteresis in the declared grid. A chain with the same number of edges can retain it. This separates two network properties:

[
	ext{shock transmission}

eq
	ext{shock storage}.
]

Ecological history can therefore reside not in a permanently degraded cue but in the interaction structure that remains after the cue recovers.

### 5.4 Natural data support the information axis, not the full hysteresis claim

No current natural dataset demonstrates the complete sequence

[
	ext{information loss}
ightarrow
	ext{partner timing shift}
ightarrow
	ext{information recovery}
ightarrow
	ext{persistent partner state}.
]

We retain that boundary deliberately.

The broad-bird analysis supports a pooled association between pre-outcome predictive connectivity and realized mismatch. The flycatcher experiment shows that partner phenology can become informative only after an early settlement decision has already occurred. Wigeon show that historical predictability does not simply translate into stronger correction once phase error exists. The 31-year cue–driver lane is nonstationary but fails its preregistered reversal gate.

Together these systems identify different edges of the proposed mechanism; none is treated as evidence for an unobserved natural network hysteresis event.

### 5.5 Cue–driver decoupling is motivation, not the novelty claim

Tomotani et al. (2021) already showed that environmental variables associated with pied-flycatcher arrival need not predict the estimated annual fitness optimum and explicitly proposed climate-driven disruption of cue–driver correlations.

PAYOFF-B therefore does not claim novelty for remote cues, predictive connectivity or cue–driver decoupling itself.

The contribution begins one step downstream:

[
	ext{changing cue quality}
	imes
	ext{unequal decision deadlines}
ightarrow
	ext{asynchronous information uptake}
ightarrow
	ext{transient desynchronization}
ightarrow
	ext{topology-dependent ecological memory}.
]

This sequence also distinguishes the new argument from generic “phenological mismatch” explanations.

### 5.6 Capacity, information and accessibility should not be collapsed into resilience

The older temporal-buffering result remains useful because it identifies a different reason for failure.

A seasonal response can fail because:

1. the organism **cannot do** the required response;
2. it **cannot know** the correct response before commitment;
3. it **cannot afford to wait** until the information becomes actionable; or
4. the interaction system **cannot reach** the higher-payoff regime through unilateral changes.

These mechanisms can produce similar endpoint mismatch but imply different interventions and different responses to future forcing.

### 5.7 Outcome-blind perturbation test

The registered Aikens within-taxon phase-retention result remains unopened.

<!-- AIKENS_LAMBDA_DISCUSSION_START -->
[AIKENS LAMBDA DISCUSSION PENDING — if retained in this manuscript, it is an actuation/capacity boundary test and must not alter the information-timing headline.]
<!-- AIKENS_LAMBDA_DISCUSSION_END -->

The information-deadline argument does not depend on its sign or estimability.

### 5.8 Limitations

The information-timing and Bayesian-network models are deliberately finite mechanism models. Cue accuracies, delay costs and payoff magnitudes are not fitted natural parameters.

The shared-cue desynchronization witness assumes two actors can eventually observe the same signal. Natural partners may instead receive correlated but non-identical signals.

Sequential best response is one explicit accessibility rule, not a universal evolutionary dynamic.

The broad-bird result is dependence-sensitive and should not be interpreted as 3,311 independent route replicates or as one common species coefficient.

The flycatcher manipulation anchors timing-dependent cue availability but does not identify whether females respond directly to heterospecific hatching or to correlated resource, predation or competition conditions.

The long-term cue–driver reconstruction uses a fixed coarse-grid Ivory Coast temperature proxy and published derived annual selection gradients. It is a bounded test of one prespecified information coordinate.

Most importantly, the topology-dependent hysteresis result remains synthetic. A direct natural test requires a sufficiently long system containing a pre-commitment cue, future destination/resource state, focal timing, partner timing and a genuine information degradation–recovery episode.

---

## 6. Conclusion

Seasonal adaptation is not limited only by response capacity.

Useful information can exist yet arrive after the decision that needs it. When waiting is costly, organisms can rationally commit under uncertainty. If interaction partners face different decision deadlines, they can begin using the same improving cue at different reliability thresholds.

This creates a counterintuitive ecological prediction:

> **Better information can temporarily worsen phenological coordination.**

In the exact model, shared ignorance gives way to asymmetric information use before shared informed coordination is restored.

Interaction structure determines what happens next. Some networks merely transmit the transient information shock; others can store it as a strict, lower-joint-payoff timing regime that persists after information recovers.

Natural systems currently support pieces rather than the full chain: pre-outcome predictive connectivity is associated with lower mismatch in a pooled migratory-bird analysis; heterospecific phenology affects later but not earlier flycatcher settlement decisions; predictive connectivity does not strengthen post-error correction in wigeon; and a preregistered 31-year flycatcher information series fails the required decline–recovery gate.

The resulting ecological framework is therefore:

[
	ext{capacity}
+
	ext{information before deadline}
+
	ext{cost of waiting}
+
	ext{strategic accessibility}
ightarrow
	ext{realized seasonal coordination}.
]

Mismatch is the endpoint of this system, not a direct measure of what organisms knew, what they could do or which alternative coordinated states were historically reachable.

---

## Prior-art boundary

This manuscript does not claim novelty for game-theoretic phenology (Johansson & Jonzén 2012), migration timing under variable information (Bauer et al. 2020), climate-driven informational mismatch, environmental predictive connectivity in migrants, social information use, or cue–driver decoupling in pied flycatchers (Tomotani et al. 2021).

The narrower contribution is the combination of:

1. endogenous information access through costly decision timing;
2. an exact private-versus-joint value-of-waiting wedge;
3. non-monotonic coordination under monotonically improving cue reliability;
4. strict topology-dependent storage of a transient information shock; and
5. outcome-bounded natural tests that separate pre-commitment information, information availability at settlement and post-error correction.

---

## Main-figure architecture

**Figure 1 — Information can arrive after the decision deadline.**  
Act-now versus wait-for-information decision, private and joint information value, and the flycatcher male/female information-availability anchor.

**Figure 2 — Better information can transiently worsen coordination.**  
Cue accuracy versus waiting decisions and expected interactor mismatch, highlighting the 0.82–0.93 desynchronization window.

**Figure 3 — Interaction topology determines ecological memory.**  
Complete, chain and migrant-star networks; strict phase-diagram counts and the interior 0.875/0.50 witness.

**Figure 4 — Natural predictive connectivity and mismatch.**  
Broad-bird registered coefficient, detrended versus raw comparison, leave-one-out sign stability and dependence-aware uncertainty.

**Figure 5 — Prediction, settlement information and correction are different axes.**  
Flycatcher source-backed manipulation, wigeon registered null, and the long-term cue–driver gate failure.

**Figure 6 — Capacity remains a separate barrier.**  
Finite temporal buffering, spatial re-entry and fragmentation-cost buffering from the retained moving-landscape programme.

Extended speed-ratio falsification, direct-system phase-retention comparisons, interval-standardization diagnostics and broader moving-landscape sweeps move to Supplementary Information unless required by journal format.

---

## References

- Amaral BR, Youngflesh C, Tingley M, Miller DAW (2025) Shifting gears in a shifting climate: Birds adjust migration speed in response to spring vegetation green-up. *Diversity and Distributions* 31:e70033. DOI: 10.1111/ddi.70033.
- Bauer S, McNamara JM, Barta Z (2020) Environmental variability, reliability of information and the timing of migration. *Proceedings of the Royal Society B* 287:20200622. DOI: 10.1098/rspb.2020.0622.
- Johansson J, Jonzén N (2012) Game theory sheds new light on ecological responses to current climate change when phenology is historically mismatched. *Ecology Letters* 15:881–888. DOI: 10.1111/j.1461-0248.2012.01812.x.
- Samplonius JM, Both C (2017) Competitor phenology as a social cue in breeding site selection. *Journal of Animal Ecology* 86:615–623. DOI: 10.1111/1365-2656.12640.
- Tomotani BM, Gienapp P, de la Hera I, Terpstra M, Pulido F, Visser ME (2021) Integrating Causal and Evolutionary Analysis of Life-History Evolution: Arrival Date in a Long-Distant Migrant. *Frontiers in Ecology and Evolution* 9:630823. DOI: 10.3389/fevo.2021.630823.
- Visser ME, Gienapp P, Husby A, Morrisey M, de la Hera I, Pulido F, Both C (2015) Effects of Spring Temperatures on the Strength of Selection on Timing of Reproduction in a Long-Distance Migratory Bird. *PLOS Biology* 13:e1002120. DOI: 10.1371/journal.pbio.1002120.
- van Toor ML et al. (2021) Migration distance affects how closely Eurasian wigeons follow spring phenology during migration. *Movement Ecology* 9:61. DOI: 10.1186/s40462-021-00296-0.
- Visser ME, Gienapp P (2019) Evolutionary and demographic consequences of phenological mismatches. *Nature Ecology & Evolution* 3:879–885. DOI: 10.1038/s41559-019-0880-8.
- Weir JC, Phillimore AB (2024) Buffering and phenological mismatch: a change of perspective. *Global Change Biology* 30:e17294. DOI: 10.1111/gcb.17294.

---

## Claim ceiling

This v2 manuscript supports:

- exact value-of-information and waiting-threshold results in the declared binary model;
- an exact private-versus-joint information-acquisition wedge;
- non-monotonic information-induced desynchronization in the declared shared-cue unequal-delay model;
- strict topology-dependent lower-payoff hysteresis in the declared three-player Bayesian game;
- pooled, dependence-sensitive association between pre-outcome predictive connectivity and lower natural migration mismatch;
- a source-backed experimental anchor for timing-dependent heterospecific information availability;
- a registered null for predictive-connectivity modulation of wigeon post-error phase correction;
- a registered negative long-term cue–driver reversal gate;
- finite temporal buffering and spatial re-entry as a distinct capacity mechanism.

It does not support:

- natural interaction-network hysteresis;
- universal harm or benefit of improved information;
- a universal predictive-connectivity coefficient across bird species;
- the claim that female flycatchers intentionally delay in order to collect tit information;
- the claim that the 1980–2010 cue–driver series contains a verified natural information recovery cycle;
- a universal phase-retention coefficient or actuator;
- a natural threshold inferred from synthetic cue accuracies, delay costs or interaction strengths.
