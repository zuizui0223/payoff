# Information deadlines can desynchronize seasonal interactions under environmental change

**Status:** PAYOFF-B Paper 2 canonical manuscript, V2 PREOUTCOME  
**Lineage:** absorbs the Paper 2 publication role from `PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md`; V1 is frozen as temporal-buffering provenance/rollback and is not a separate submission candidate while V2 is active.  
**Evidence boundary:** exact theoretical claims are restricted to declared finite games and frozen synthetic programmes. Natural-data claims retain their registered dependence and source boundaries. The preregistered Aikens industrial-development lambda outcome remains unopened.

## Abstract

**Aim:** We ask when improving environmental information can desynchronize interacting seasonal organisms and why restored information may fail to restore coordination.

**Location:** General theory, with empirical modules from eastern North America and European bird interaction systems.

**Time period:** Dataset-specific; principal reconstructed phenology records span approximately 1980–2020.

**Major taxa studied:** Migratory birds, with plants and insect pollinators as an independent benchmark.

**Methods:** We combine exact Bayesian decision theory and finite coordination games with preregistered comparative analyses, source-table reconstructions, published experiments and interaction-level phenology studies.

**Results:** Information becomes actionable only above an exact reliability threshold, but waiting is governed by an **effective deadline cost**: direct waiting loss plus the minimum cost of downstream compensation and residual delay. Raw waiting time therefore does not generally rank effective deadlines and can even reverse the predicted order of information-use thresholds. Heterogeneous effective deadlines create a finite asynchronous-uptake window, so improving the same cue can transiently increase mismatch. Perfect information can also support both obsolete uninformed and better informed strict equilibria; after cue degradation collapses coordinated information use, restoring perfect cue accuracy need not recover the informed state. Natural evidence supports successive links rather than the full hysteresis sequence: stronger predictive connectivity is associated with smaller mismatch across 37 bird species, a 944-effect reconstruction shows weaker temperature responses in long- than short-distance migrants, and differential climate sensitivity across 10 European nest-box schemes widened resident–migrant laying-date intervals by **0.94 d/decade**.

**Main conclusions:** Seasonal mismatch cannot be interpreted from cue quality or raw waiting time alone. Effective deadline costs determine when information is worth using, while strategic coordination can determine whether information use recovers at all. **Environmental information can recover before ecological coordination does.**

**Keywords:** phenological mismatch; migration; information ecology; Bayesian games; seasonal timing; predictive connectivity; ecological hysteresis; climate change

---

## 1. Introduction

Climate-change ecology often asks whether organisms can keep pace with changing environments. Species may move through space, shift seasonal timing, alter stopover behaviour or combine these responses. The usual endpoint is mismatch: the difference between when or where organisms occur and when or where favourable conditions occur.

Mismatch is important, but it compresses several different ecological problems. A species can be mismatched because it lacks response capacity, because the future state is difficult to predict, because useful information becomes available only after a decision deadline, or because an individually costly transition blocks a jointly beneficial response. These mechanisms make different predictions even when they produce the same observed timing error.

Migration makes the information problem especially clear. A resident organism can often sample local spring directly. A long-distance migrant must make some decisions before the destination state is observed. Environmental conditions at wintering or stopover sites can provide predictive information, but that information need not remain reliable under climate change. This general problem is established in migration theory and empirical work: migrants use remote environmental cues, environmental predictability changes optimal migration timing, and climate change can decouple cues from the later conditions that determine fitness (Kölzsch et al., 2015; Bauer et al., 2020; Tomotani et al., 2021). PAYOFF-B therefore does not treat cue–driver decoupling itself as a new idea.

The unresolved problem is what happens **after cue quality is allowed to vary among decision contexts**. Interacting species do not necessarily face the same cost of delaying action. Crucially, that cost is not the number of days delayed: organisms can compress migration or compensate later, and compensation can itself carry fitness costs. We therefore distinguish raw waiting time from an **effective deadline cost** that combines nonrecoverable waiting loss with the least costly feasible downstream compensation. Early arrival can affect rank, mating opportunities or territory acquisition; later decisions can use richer local information. Thus two species, or two demographic classes within a species, can observe the same future cue but rationally begin using it at different reliability thresholds.

Game-theoretic phenology already shows that individually selected timing can differ from a simple system-level optimum under climate change (Johansson & Jonzén, 2012). This immediately produces a counterintuitive possibility: better information need not improve ecological coordination monotonically. If one actor begins waiting for a cue before another, the first becomes informed while its partner remains committed to the previous timing convention. Coordination can worsen during the transition from shared ignorance to shared information.

Interaction adds a second problem. Once a seasonal network has coordinated on one timing convention, being the first actor to adopt a different information-dependent strategy can itself create partner mismatch. The network may therefore remain in an obsolete timing regime even after environmental information has fully recovered. In that case the constraint is neither uncertainty nor response capacity. It is strategic accessibility.

We develop this argument in four layers.

First, we derive an exact **information-deadline theorem** for a binary seasonal decision. It gives the cue reliability at which information becomes actionable, the actor-specific threshold at which waiting for that information becomes worthwhile, and the exact width of the information-induced desynchronization window between two actors with different effective deadline costs. Those costs need not preserve the ordering of raw waiting durations.

Second, we embed information acquisition in an interaction game. We show conditions under which an obsolete uninformed profile and a fully informed profile are both strict equilibria under perfect environmental information, even though the informed profile has higher joint payoff. We then perturb cue quality down and back up to ask whether environmental recovery restores information use, and derive the minimum voluntary coalition and temporary informed seed needed to restart recovery.

Third, we connect the theory to natural systems using deliberately separated empirical tests. A preregistered broad-bird analysis asks whether pre-outcome predictive connectivity is associated with realized phenological mismatch. A separate meta-analytic source-table reconstruction asks whether phenological temperature responsiveness weakens from short- to long-distance migration, with an independent local plant–pollinator dataset used as a non-migratory benchmark rather than pooled into a taxon contrast. A source-backed pied-flycatcher manipulation asks whether heterospecific phenology affects decisions made before versus after that information becomes visible. A registered wigeon analysis asks a different question: whether predictive connectivity strengthens correction after phase error has already appeared. These tests distinguish prediction, information distance, information timing and feedback rather than collapsing them into one “tracking ability.”

Fourth, we retain the earlier PAYOFF-B temporal-buffering result as a capacity layer. Timing can temporarily substitute for movement, but finite temporal capacity eventually forces spatial tracking to re-enter. Capacity, information and coordination are therefore complementary failure modes.

Our central theoretical conclusion is:

> **Seasonal adaptation can fail even when an adequate response exists and environmental information later becomes perfect, because interacting organisms can face different effective decision deadlines and information use can itself become a coordination state.**

---

## 2. Theory

### 2.1 The information-deadline problem

Let the future seasonal state be normal or early, with

[
P(early)=\pi.
]

An actor chooses an early or late seasonal action. Define

[
A=(1-\pi)C_F
]

as the prior expected loss of committing early and

[
L=\pi C_M
]

as the prior expected loss of committing late. Before observing a cue, the Bayes-optimal action has risk

[
R_0=\min(A,L).
]

A later binary cue has state-classification accuracy \(q\ge 1/2\). Waiting for it creates raw temporal delay \(\delta\), but elapsed delay is not itself the theorem input. Let \(J(\delta)\) be direct nonrecoverable waiting loss, let compensation \(c\) cost \(K(c)\), and let residual delay cost \(M(\delta-c)\). The relevant **effective deadline cost** is

[
D_{eff}(\delta)
=
J(\delta)+\min_c\{K(c)+M(\delta-c)\}.
]

The original fixed-cost theorem is recovered by setting \(D=D_{eff}\).

The cue becomes capable of changing the Bayes-optimal action at

[
q_0=\frac{\max(A,L)}{A+L}.
]

Its exact value is

[
V(q)=
\max\left[
0,;
q(A+L)-\max(A,L)
\right].
]

The actor waits only when \(V(q)>D_{eff}\). If \(D_{eff}<R_0\),

[
q_{wait}
=
\frac{\max(A,L)+D_{eff}}{A+L}.
]

If \(D_{eff}\ge R_0\), even perfect information is not worth waiting for.

This distinction is empirically consequential. Two actors can experience the same raw delay, or one can wait longer, yet the actor with greater downstream compensatory capacity can have the lower \(D_{eff}\) and therefore begin using information sooner. Raw waiting duration, migration distance and departure date therefore need not preserve the ordering of information-use thresholds.

If effective waiting cost depends on an unresolved future **deadline state** \(H\), let \(\mathcal I\) be the information available at commitment and write \(D(H)\equiv D_{eff}(H)\) for the state-specific effective cost. The decision-relevant quantity is

[
\bar D_{eff}(\mathcal I)=E[D(H)\mid\mathcal I].
]

Thus later harshness changes the rational threshold only insofar as it is predictable at commitment; an ex-ante optimal decision can still look wrong ex post.

### 2.2 Better information can transiently increase mismatch

Consider two actors facing the same future cue and state-dependent losses but different effective waiting costs,

[
D_{eff,1}<D_{eff,2}.
]

When both are below \(R_0\), their information-use thresholds satisfy \(q_1<q_2\). Three regimes follow:

[
q\le q_1:
\quad
commit\mid commit,
]

[
q_1<q\le q_2:
\quad
wait\mid commit,
]

[
q>q_2:
\quad
wait\mid wait.
]

The exact width of the asynchronous information-use interval is

[
\boxed{
\Delta q
=
\frac{D_{eff,2}-D_{eff,1}}{A+L}.
}
]

Thus cue quality can improve monotonically while ecological mismatch follows a zero–positive–zero trajectory. Crucially, this ordering is an ordering of effective costs, not waiting times: compensation can make \(\delta_1>\delta_2\) coexist with \(D_{eff,1}<D_{eff,2}\), reversing any threshold ranking inferred from raw delay.

In the transparent PAYOFF-B witness,

[
\pi=0.4,\quad C_F=2,\quad C_M=1,
]

with effective costs \(0.10\) and \(0.30\), the exact thresholds are

[
q_1=0.8125,\qquad q_2=0.9375.
]

On a 0.01 grid this appears as a mismatch window from \(q=0.82\) to \(0.93\). If the higher effective cost exceeds \(R_0\), that actor never waits even at \(q=1\), so information asymmetry persists under perfect cue reliability.

### 2.3 Perfect information does not guarantee information use

We next consider a shared-cue interaction network at

[
q=1.
]

For player (i), let (R_i) be its prior mismatch risk under the old timing convention, (D_i) its effective waiting cost, (I_i) its interaction-mismatch strength, and (p) the probability of the state in which informed action differs from the old action.

If all players retain the old action, player (i) receives

[
U_i^{old}=-R_i.
]

If it alone begins using perfect information while all neighbours remain old,

[
U_i^{first}=-D_i-pI_i.
]

The old profile is therefore stable when

[
D_i+pI_i\ge R_i.
]

If all players use perfect information, there is no state mismatch and no interaction mismatch:

[
U_i^{info}=-D_i.
]

The informed profile is stable when

[
D_i\le R_i+pI_i.
]

Both are strict equilibria when

[
\boxed{
|D_i-R_i|<pI_i.
}
]

Yet the informed profile has higher joint payoff whenever

[
\boxed{
\sum_i D_i<\sum_i R_i.
}
]

Thus perfect environmental information can coexist with a strictly stable obsolete timing regime and a strictly stable better-informed regime.

### 2.4 Temporary information degradation can create permanent behavioural lock-in

The canonical shared-cue network has three actors: flower, local pollinator and migrant. Their information costs are

[
(0.05,0.10,0.30),
]

their prior-late risks are

[
(0.10,0.10,0.40),
]

and interaction strength is (0.50).

At (q=1), the unilateral gains from being the first information user are

[
(-0.15,-0.20,-0.10).
]

No player wants to move first.

Nevertheless, the fully informed joint payoff is

[
-0.45,
]

compared with

[
-0.60
]

for the obsolete all-late profile.

The exact player-specific stability thresholds of the informed profile are approximately

[
0.583,quad 0.667,quad 0.800.
]

The migrant therefore defines the network boundary. Under path-preserving best response, the informed profile remains at the exact tie (q=0.80) and collapses at (q=0.79) on the 0.01 grid.

When cue quality is restored stepwise to (q=1), the network remains in the all-late profile. Environmental information recovers completely, but ecological information use does not.

### 2.5 In communities, asynchronous information use is a network cut

At cue quality \(q\), let \(S(q)\) be the actors using the cue, \(C(q)\) the interaction weight crossing from users to non-users, \(W\) total interaction weight, and \(M(q)\) the probability that cue-contingent action differs from the old action. Expected interaction mismatch is

    E(q) = M(q) C(q) / W.

In an unweighted complete network with \(N\) actors and \(k\) users,

    C/W = 2 k (N-k) / [N(N-1)],

so exposure to asynchronous uptake is greatest near the middle of adoption. Topology enters because the next adopter can create or repair mismatch edges:

    Delta C_i
      = weight(i, still-uninformed neighbours)
      - weight(i, already-informed neighbours).

The same effective-deadline distribution can therefore generate different mismatch trajectories depending on where those deadlines sit in the network.

### 2.6 Private and joint value of waiting can diverge

Let \(V_P(q)\) be the focal actor's private value of information and \(V_J(q)\) the joint value including partner losses. Whenever \(V_J(q)>V_P(q)\), the interval

[
D\in[V_P(q),V_J(q))
]

contains decisions for which the actor rationally commits under uncertainty although the interacting system would gain from waiting. Coordination failure can therefore begin as under-investment in information acquisition, before seasonal actions themselves diverge.

### 2.7 Recovery can be nucleated by a small informed seed

Failure of spontaneous recovery does not imply that all actors must shift simultaneously. Suppose a temporary informed seed \(S\) is maintained while other actors best respond. For uninformed actor \(i\), let \(a_i(S)\) be the fraction of its interaction weight attached to informed neighbours. Its gain from adopting is

[
\boxed{
H_i(S)
=
R_i-D_i+pI_i[2a_i(S)-1].
}
]

Actor \(i\) follows the informed state when

[
a_i(S)>
\frac12
\left[
1-\frac{R_i-D_i}{pI_i}
\right].
]

Because \(a_i(S)\) cannot decrease as adoption spreads on non-negative networks, recovery is a progressive threshold cascade. In the canonical three-species example spontaneous recovery fails in all tested connected networks, yet a temporary one-species seed can restore the informed equilibrium. Any single actor works in the complete graph and migrant-star; in the chain

[
flower-local pollinator-migrant,
]

only the central local pollinator is a singleton rescue seed. Thus trap existence and rescue leverage are different network properties, and the species best placed to **maintain** a timing convention need not be the species best placed to **rescue** it.

Threshold cascades are established in network science (Watts, 2002); here the node threshold is derived from seasonal mismatch risk, effective information cost and interaction mismatch rather than introduced as a free adoption parameter.

---

## 3. Empirical evidence hierarchy

### 3.1 Predictive connectivity and realized mismatch across migratory birds

The preregistered broad-bird analysis reanalyses the migration and green-up dataset of Amaral et al. (2025), retaining 3,311 observations from 37 species after requiring a trailing eight-year information window.

Predictive connectivity is defined as the signed correlation between source and destination green-up anomalies after the two locations are separately detrended within the pre-outcome window.

The registered pooled GAM gives

[
\hat\beta_{\rho}=-0.0462,
]

with

[
95\%\ CI=[-0.0870,-0.0054],
\quad
p=0.0265.
]

Thus stronger pre-existing predictive connectivity is associated with smaller arrival–green-up mismatch in the declared pooled analysis.

The sign remains negative in all leave-one-species-out and all leave-one-year-out fits. The 10-year trailing-window sensitivity is also negative with its interval below zero.

However, dependence-aware uncertainty is wider. Species-, cell-year- and source–target-pair clustered intervals cross zero, as does the species-level inverse-variance summary. The licensed interpretation is therefore a pooled directional macroecological signal, not a universal species-level coefficient.

Importantly, using raw undetrended source–destination correlation removes the effect. The signal is associated with interannual predictive information rather than a shared long-term warming trend.

#### Information distance is visible in an independent migration meta-analysis

A separate reconstruction of the Usui et al. (2017) effect-size table retains 944 temperature-response rows from 28 studies and 279 species after restricting the source-coded migration-distance moderator to short and long migrants. Inverse-variance meta-regression with two-way Study × Species clustered uncertainty gives an adjusted long-minus-short contrast of **+0.421 d / °C** (95% CI **+0.121 to +0.722**, p = 0.0077). Because negative slopes denote earlier migration in warmer years, long-distance migrants are less temperature-responsive than short-distance migrants. The result is stable to capping the largest inverse-variance weights (**+0.417**, 95% CI **+0.118 to +0.715**) and to an unweighted adjusted fit (**+0.538**, 95% CI **+0.190 to +0.887**). Leaving out each of the 28 studies in turn retains a positive contrast in every fit, and every 95% CI lower bound remains above zero (estimate range **+0.378 to +0.608 d / °C**; largest p = **0.0195**). This reconstructs a pattern already reported by Usui et al.; it is not a new PAYOFF-B discovery and does not reproduce the source paper's phylogenetic layer.

A non-exclusive alternative explanation is that long-distance migrants rely more strongly on endogenous circannual programmes and photoperiodic timing, which can weaken short-term temperature responsiveness even when remote environmental information is available (Åkesson et al., 2017; Helm & Liedvogel, 2024). E6 therefore does not identify information distance as the causal mechanism: endogenous or photoperiodic control is treated here as a possible mechanistic source or correlate of early commitment, not as evidence that the deadline pathway itself has been observed.

An independent local benchmark from Freimuth et al. (2022) reproduces all 1,763 archived species-level temperature slopes and the published group means: plants **−5.152 d / °C**, flies **−3.879**, bees **−2.024**, butterflies/moths **−1.848** and beetles **−1.706**. These sources are not pooled into a bird-versus-pollinator coefficient because taxon, geography, phenophase and study design are confounded. Their licensed role is triangulation: local partners can show large but unequal temperature responses, while within migratory birds responsiveness weakens with migration distance.

### 3.2 A manipulated heterospecific cue affects later but not earlier decisions

Samplonius and Both (2017) experimentally advanced and delayed resident tit hatching phenology while observing pied-flycatcher settlement.

Male flycatcher settlement was not detectably related to treatment

[
Z=0.854,
\quad
P=0.393,
]

and the authors note that almost all males settled before the manipulated hatching difference became apparent.

Later female settlement did respond to treatment. The published pairing model gives a tit-timing effect of approximately

[
-0.101
]

with

[
P=0.042,
]

and the time-dependent Cox analysis gives

[
-0.065,
\quad
P<0.009.
]

The experiment does not show that females deliberately delayed settlement in order to collect information, nor does it identify the exact sensory pathway. It does support the narrower timing claim required by the model: the same heterospecific seasonal state can be unavailable to an earlier decision and behaviourally relevant to a later decision.

### 3.3 Predictive connectivity does not strengthen post-error correction in wigeon

A registered wigeon analysis builds on the Eurasian wigeon migration system of van Toor et al. (2021), using historical 2000–2017 ERA5 timing relationships to define route-level predictive connectivity before analysing 2018–2020 staging transitions.

Across 224 transitions from 28 individuals, the preregistered interaction between incoming phase error and predictive connectivity is

[
\hat\beta=+0.0202,
]

with

[
95\%\ CI=[-0.1058,0.1461],
\quad
p=0.756.
]

The predicted negative interaction is not supported.

This null is informative because it separates two functions of information. Predictive connectivity may influence which action or timing regime is chosen before error appears without acting as a universal amplifier of correction after error has already appeared.

### 3.4 Two preregistered natural reversal gates did not license a hysteresis test

Two long-term gates were preregistered to ask whether a natural environmental-information coordinate first showed the decline→recovery geometry required before any network-history claim could be opened. The first, linking a fixed Ivory Coast temperature cue to annual pied-flycatcher selection gradients, returned \texttt{NO\_CUE\_DRIVER\_REVERSAL}. A second, closer same-system gate linked the same fixed cue to independently archived Hoge Veluwe caterpillar-peak dates over 24 registered predictive-connectivity years (1992–2015). That gate also failed the preregistered negative-then-positive reversal geometry and returned \texttt{NO\_CUE\_RESOURCE\_REVERSAL}.

Because the environmental prerequisite failed, the resident–migrant history test remained unopened: pied-flycatcher and great-tit timing were not joined into a hysteresis analysis. Full breakpoint, slope and source-provenance diagnostics are retained in Supporting Information and frozen receipts. PAYOFF-B therefore does not claim a natural information-recovery hysteresis event.

### 3.5 Capacity remains a distinct failure mode

The earlier moving-landscape programme supplies a separate capacity result. In a local controller, movement and phenological feedback can be exactly substitutable at fixed total restoring gain. Explicit landscapes break that equivalence.

Finite timing capacity extends persistence and reduces immediate route costs, but movement re-enters under stronger directional forcing. This capacity layer is motivated by empirical work showing green-wave tracking, compensation for phenological error and anthropogenic decoupling of movement from seasonal resources (Aikens et al., 2017, 2022; Ortega et al., 2023). In the canonical one-dimensional landscape, increasing phenological capacity shifts the persistence bracket substantially, yet frontier strategies remain migration-dominant. In a two-dimensional zigzag landscape, phenology-only tracking is favoured at moderate forcing before migration re-enters as forcing increases.

Timing therefore acts as a finite buffer, not a permanent substitute for spatial tracking.

---

## 4. Discussion

### 4.1 Cue quality and cue use are different ecological state variables

A central result of PAYOFF-B is that environmental information quality should not be equated with information use.

The information-deadline theorem gives actor-specific cue thresholds. Two species can experience the same external cue and nevertheless occupy different information states because they face different costs of waiting.

This distinction changes how phenological mismatch should be interpreted. A mismatch peak during a period of improving environmental predictability need not imply that organisms are becoming less responsive. It can arise because one partner has begun using a cue that the other partner still rationally ignores.

### 4.2 Better information can transiently worsen coordination

The exact desynchronization-width identity

[
\Delta q=
\frac{|D_{eff,2}-D_{eff,1}|}{A+L}
]

gives a direct comparative prediction: greater heterogeneity in effective deadline costs widens asynchronous cue uptake, whereas larger timing-error losses compress that interval because both actors value information sooner.

The key empirical warning is that **elapsed waiting time does not generally order this quantity**. An organism can wait longer yet face a lower \(D_{eff}\) if it can compress migration or compensate later; conversely, complete recovery of downstream timing can leave a positive direct cost \(J\). Migration distance, departure date and waiting duration are therefore unsafe proxies for information-use thresholds unless a cost-and-compensation model links them to \(D_{eff}\). In principle they can rank two actors in the wrong order. American redstarts give a concrete natural example of the underlying mechanism: birds departing about 10 days late migrated 43% faster, yet this compensatory pattern was associated with a reported 6.3% decrease in annual survival (Dossman et al., 2023). This supports compensation-with-cost, not an estimate of \(D_{eff}\) or cue-use thresholds.

The prediction is transitional, not that information is harmful: both actors ignore poor cues and use sufficiently reliable cues, with mismatch concentrated between those regimes.

A second predictability channel arises when the future effective cost of waiting is itself uncertain. The relevant term is \(E[D_{eff,i}(H)\mid\mathcal I_i]\), giving two-actor window width \(|E[D_{eff,2}\mid\mathcal I_2]-E[D_{eff,1}\mid\mathcal I_1]|/(A+L)\). Greater-snow-goose experiments motivate this hidden-deadline extension because perturbation costs vary among breeding contexts while southern conditions weakly predict later Arctic conditions; they do not estimate this conditional cost or an information-use threshold (Legagneux et al., 2012; Grandmont et al., 2023; Reséndiz-Infante & Gauthier, 2024).

### 4.3 Environmental recovery can precede ecological recovery

The shared-cue network produces a stronger path-dependent result.

Once coordinated information use collapses, restoring cue reliability is not sufficient to restore the informed state. At perfect information, the obsolete and informed timing profiles can both remain strict equilibria. The informed state has higher joint payoff, but each individual actor loses by moving first because it pays the information cost while temporarily mismatching partners.

Thus environmental recovery and behavioural recovery are not equivalent:

[
\text{information recovery}
\neq
\text{coordination recovery}.
]

This is a seasonal ecological version of a coordination trap. The contribution is not the generic existence of multiple equilibria, which is established in game theory, but the link from decision deadlines and information acquisition to a persistent ecological timing convention.

### 4.4 Acquisition memory and topological memory are distinct

The shared-cue recovery failure is topology-independent across the three canonical connected graphs because a lone information adopter mismatches all of its own neighbours.

The earlier private-cue game shows a different mechanism. There, displaced heterogeneous timing profiles are stored differently by different graph structures. Under the strict phase diagram, complete and chain networks retain lower-payoff hysteresis across nontrivial parameter regions, whereas the migrant-star does not.

PAYOFF-B therefore distinguishes:

1. **acquisition memory** — failure to restart a coordinated information-using convention;
2. **topological memory** — storage of heterogeneous timing states by network geometry.

The first concerns strategic accessibility of shared information use; the second concerns which mixed timing configurations a network can retain.

### 4.5 Recovery leverage is topology-dependent

The coordination trap is not the same as irreversible loss.

At perfect information the all-old profile can be strict, so no actor moves
first voluntarily. Yet temporary cue use by a sufficiently influential seed can
change the incentives facing its neighbours and initiate a recovery cascade.

The canonical chain makes this distinction concrete. The central local
pollinator is the unique singleton rescue seed, whereas either peripheral
species fails to restart the network alone. In the complete and migrant-star
topologies, any singleton seed is sufficient.

This creates a new comparative prediction: the species most important for
**maintaining** a timing convention need not be the same species that is most
effective at **rescuing** it after collapse.

The model therefore separates:

1. vulnerability to information degradation;
2. stability of the obsolete state;
3. rescue leverage of individual network positions.

A real ecosystem test would require observing or manipulating a temporary
change in information use or timing flexibility. PAYOFF-B does not infer such a
keystone rescue species from the current natural datasets.

### 4.6 Natural evidence currently supports the information axis, not natural network hysteresis

The empirical evidence is deliberately modular.

The broad-bird result supports an association between predictive information and realized mismatch, but dependence-aware uncertainty prevents a universal species-level claim. The independent migration-distance reconstruction adds a second natural gradient: long-distance migrants are less temperature-responsive than short-distance migrants under Study × Species clustered uncertainty. The Freimuth plant–pollinator reconstruction provides a local-system benchmark in which all five source group means reproduce but response magnitudes differ strongly. Together these results support an information-distance axis without licensing a causal bird-versus-pollinator comparison.

Two published interaction-level analyses narrow this gap further. In UK bird–caterpillar pairs, temporal tracking slopes are **0.510** for Blue Tit, **0.515** for Great Tit and **0.348** for Pied Flycatcher, all below perfect tracking, so earlier resource years increase consumer–resource mismatch (Burgess et al., 2018). Across 10 European nest-box schemes, resident tits were more temperature-sensitive than migratory flycatchers, and this differential response widened their laying-date interval by **0.94 d/decade**; tit phenology also explained flycatcher phenology after controlling for temperature (Samplonius et al., 2018).

These studies support **interaction-level response asymmetry → changing relative timing**. The exact, implementation-verified mapping \(D_{eff,2}-D_{eff,1} \rightarrow q_2-q_1 \rightarrow q_1<q\le q_2\) remains prospective in nature: neither study independently estimates the effective waiting-cost gap and actor-specific thresholds or observes the predicted asynchronous window in one system.

The flycatcher manipulation anchors the idea that the availability of heterospecific phenology depends on when a decision is made.

The wigeon null shows that predictive connectivity should not be treated as a universal post-error controller.

Two long-term preregistered reversal gates are negative. The second, more direct cue–resource gate failed before any resident–migrant history outcome was opened.

No current natural dataset therefore demonstrates the full degradation–recovery network hysteresis predicted by the shared-cue and private-cue games. That remains a prospective test.

### 4.7 Capacity, information and coordination are distinct but coupled constraints

The framework separates six barriers: **capacity** (how much delay can be
recovered), **prediction** (whether pre-commitment information forecasts the
later state), **information timing** (whether it arrives before commitment),
**strategic accessibility** (whether unilateral cue uptake is costly),
**network memory** (whether topology retains altered timing), and **recovery
leverage** (which temporary informed seed restarts coordination).

Capacity can lower \(D_{eff}\), while forecasts increase cue quality. Greater-snow-goose tracking illustrates the distinction because later departure can coincide with shorter migration, weakening departure–arrival coupling (Bêty et al., 2004). Neither mechanism necessarily resolves a coordination trap.

### 4.8 Relation to prior work

Remote environmental cues, information value in migration, climate-driven cue–driver decoupling, phenological games and ecological mismatch all have substantial prior literatures (Johansson & Jonzén, 2012; Kharouba & Wolkovich, 2020; Visser & Gienapp, 2019; Bauer et al., 2020).

The closest direct predecessor is the pied-flycatcher work showing that wintering- and breeding-ground environmental variables can explain arrival timing without predicting the annual fitness optimum, with climate-driven cue–driver decoupling proposed explicitly (Tomotani et al., 2021).

PAYOFF-B therefore begins one step later.

Its candidate contribution is the conjunction:

[
\text{changing cue reliability}
\times
\text{heterogeneous decision deadlines}
\rightarrow
\text{asynchronous cue uptake}
\rightarrow
\text{temporary mismatch}
\rightarrow
\text{coordination trap or network memory}.
]

The exact threshold and bistability conditions make that conjunction testable rather than metaphorical.

---

## 5. Conclusion

Seasonal adaptation is not limited only by how fast organisms can move or how far they can shift phenology.

An organism may possess an adequate response but face a decision before useful information becomes available. Interacting organisms can face different effective costs of waiting, even when raw delays suggest the opposite ordering, causing them to begin using the same improving cue at different reliability thresholds. Better information can therefore transiently worsen coordination.

The stronger result is historical. Once an information-using convention collapses, restoring environmental information can be insufficient. Under perfect cue accuracy, an obsolete timing convention and a better informed convention can both be strict equilibria. The informed state can have higher joint payoff while no actor benefits from adopting it first. But the trap need not require network-wide intervention: a temporary informed seed can change neighbour incentives and nucleate recovery, with the minimum rescue set determined by network position.

Natural data currently support pieces of this causal chain rather than the complete hysteresis process. Predictive connectivity is associated with smaller mismatch in a pooled broad-bird analysis; a dependence-aware reconstruction of a published migration meta-analysis shows weaker temperature responsiveness in long- than short-distance migrants, while an independent local plant–pollinator benchmark shows strong but unequal temperature responses; heterospecific phenology affects decisions made after, but not before, it becomes visible in a flycatcher manipulation; predictive connectivity does not strengthen post-error correction in wigeon; and two preregistered long-term natural reversal gates are negative, including a same-system cue–resource gate that failed before interaction history was opened.

The resulting theoretical predictions remain prospective at the full network-hysteresis level:

> **Theory predicts that environmental information can recover before ecological coordination does.**

and

> **The model further predicts that a community that cannot recover spontaneously may still be recoverable through a small, strategically placed information seed.**

The framework therefore predicts that climate adaptation can fail not only because organisms cannot respond or cannot predict the future, but because information use itself has become a historically contingent property of the interaction network.

---

## References

- Aikens EO, Kauffman MJ, Merkle JA, Dwinnell SPH, Fralick GL, Monteith KL (2017) The greenscape shapes surfing of resource waves in a large migratory herbivore. *Ecology Letters* 20:741–750. DOI: 10.1111/ele.12772.
- Aikens EO, Wyckoff TB, Sawyer H, Kauffman MJ (2022) Industrial energy development decouples ungulate migration from the green wave. *Nature Ecology & Evolution* 6:1733–1741. DOI: 10.1038/s41559-022-01887-9.
- Amaral BR, Youngflesh C, Tingley M, Miller DAW (2025) Shifting gears in a shifting climate: Birds adjust migration speed in response to spring vegetation green-up. *Diversity and Distributions* 31:e70033. DOI: 10.1111/ddi.70033.
- Åkesson S, Ilieva M, Karagicheva J, Rakhimberdiev E, Tomotani B, Helm B (2017) Timing avian long-distance migration: from internal clock mechanisms to global flights. *Philosophical Transactions of the Royal Society B* 372:20160252. DOI: 10.1098/rstb.2016.0252.
- Bauer S, McNamara JM, Barta Z (2020) Environmental variability, reliability of information and the timing of migration. *Proceedings of the Royal Society B* 287:20200622. DOI: 10.1098/rspb.2020.0622.
- Bêty J, Giroux J-F, Gauthier G (2004) Individual variation in timing of migration: causes and reproductive consequences in greater snow geese (*Anser caerulescens atlanticus*). *Behavioral Ecology and Sociobiology* 57:1–8. DOI: 10.1007/s00265-004-0840-3.
- Burgess MD, Smith KW, Evans KL, Leech D, Pearce-Higgins JW, Branston CJ, Briggs K, Clark JR, du Feu CR, Lewthwaite K, Nager RG, Sheldon BC, Smith JA, Whytock RC, Willis SG, Phillimore AB (2018) Tritrophic phenological match–mismatch in space and time. *Nature Ecology & Evolution* 2:970–975. DOI: 10.1038/s41559-018-0543-1.
- Dossman BC, Rodewald AD, Studds CE, Marra PP (2023) Migratory birds with delayed spring departure migrate faster but pay the costs. *Ecology* 104:e3938. DOI: 10.1002/ecy.3938.
- Freimuth J, Bossdorf O, Scheepens JF, Willems FM (2022) Climate warming changes synchrony of plants and pollinators. *Proceedings of the Royal Society B* 289:20212142. DOI: 10.1098/rspb.2021.2142.
- Grandmont T, Fast P, Grentzmann I, Gauthier G, Bêty J, Legagneux P (2023) Should I breed or should I go? Manipulating individual state during migration influences breeding decisions in a long-lived bird species. *Functional Ecology* 37:602–613. DOI: 10.1111/1365-2435.14256.
- Legagneux P, Fast PLF, Gauthier G, Bêty J (2012) Manipulating individual state during migration provides evidence for carry-over effects modulated by environmental conditions. *Proceedings of the Royal Society B* 279:876–883. DOI: 10.1098/rspb.2011.1351.
- Helm B, Liedvogel M (2024) Avian migration clocks in a changing world. *Journal of Comparative Physiology A* 210:691–716. DOI: 10.1007/s00359-023-01688-w.
- Johansson J, Jonzén N (2012) Game theory sheds new light on ecological responses to current climate change when phenology is historically mismatched. *Ecology Letters* 15:881–888. DOI: 10.1111/j.1461-0248.2012.01812.x.
- Kharouba HM, Wolkovich EM (2020) Disconnects between ecological theory and data in phenological mismatch research. *Nature Climate Change* 10:406–415. DOI: 10.1038/s41558-020-0752-x.
- Kölzsch A et al. (2015) Forecasting spring from afar? Timing of migration and predictability of phenology along different migration routes of an avian herbivore. *Journal of Animal Ecology* 84:272–283. DOI: 10.1111/1365-2656.12281.
- Ortega AC, Aikens EO, Merkle JA, Monteith KL, Kauffman MJ (2023) Migrating mule deer compensate en route for phenological mismatches. *Nature Communications* 14:2008. DOI: 10.1038/s41467-023-37750-z.
- Reséndiz-Infante C, Gauthier G (2024) Can arctic migrants adjust their phenology based on temperature encountered during the spring migration? The case of the greater snow goose. *Frontiers in Bird Science* 3:1307628. DOI: 10.3389/fbirs.2024.1307628.
- Samplonius JM, Both C (2017) Competitor phenology as a social cue in breeding site selection. *Journal of Animal Ecology* 86:615–623. DOI: 10.1111/1365-2656.12640.
- Samplonius JM, Bartošová L, Burgess MD, Bushuev AV, Eeva T, Ivankina EV, Kerimov AB, Krams I, Laaksonen T, Mägi M, Mänd R, Potti J, Török J, Trnka M, Visser ME, Zang H, Both C (2018) Phenological sensitivity to climate change is higher in resident than in migrant bird populations among European cavity breeders. *Global Change Biology* 24:3780–3790. DOI: 10.1111/gcb.14160.
- Tomotani BM, Gienapp P, de la Hera I, Terpstra M, Pulido F, Visser ME (2021) Integrating causal and evolutionary analysis of life-history evolution: Arrival date in a long-distant migrant. *Frontiers in Ecology and Evolution* 9:630823. DOI: 10.3389/fevo.2021.630823.
- Usui T, Butchart SHM, Phillimore AB (2017) Temporal shifts and temperature sensitivity of avian spring migratory phenology: a phylogenetic meta-analysis. *Journal of Animal Ecology* 86:250–261. DOI: 10.1111/1365-2656.12612.
- van Toor ML et al. (2021) Migration distance affects how closely Eurasian wigeons follow spring phenology during migration. *Movement Ecology* 9:61. DOI: 10.1186/s40462-021-00296-0.
- Visser ME, Gienapp P (2019) Evolutionary and demographic consequences of phenological mismatches. *Nature Ecology & Evolution* 3:879–885. DOI: 10.1038/s41559-019-0880-8.
- Visser ME, Lindner M, Gienapp P, Long M, Jenouvrier S (2021) Recent natural variability in global warming weakened phenological mismatch and selection on seasonal timing in great tits (*Parus major*). *Proceedings of the Royal Society B* 288:20211337. DOI: 10.1098/rspb.2021.1337.
- Watts DJ (2002) A simple model of global cascades on random networks. *Proceedings of the National Academy of Sciences USA* 99:5766–5771. DOI: 10.1073/pnas.082090499.

