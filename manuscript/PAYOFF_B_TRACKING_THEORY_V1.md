# Tracking together or failing apart: space–time substitution, finite temporal buffering, and coordination barriers under moving environments

**Status:** synthetic theory manuscript v1  
**Programme boundary:** separate from the PAYOFF-B GEB empirical phase-retention paper and from the anti-phase Theoretical Ecology Brief.  
**Evidence boundary:** exact local controller results plus frozen synthetic landscape results dated 2026-09-20; no natural climate threshold, corridor threshold, or taxon-level calibration is claimed.

## Abstract

Organisms can track a moving environment by redistributing in space, shifting seasonal timing, or combining both responses. These axes are often discussed as alternative forms of climate tracking, but substitution at the level of environmental mismatch does not imply substitution at the level of evolutionary accessibility or population persistence. We develop a coupled migration–phenology model in which movement and timing close a common environmental mismatch while interacting species additionally pay for spatial and phenological separation. A local linear controller gives an exact null: movement and timing feedback are interchangeable through their summed restoring gain. Explicit moving landscapes break that equivalence. Phenological capacity extends persistence under faster environmental movement but only over a finite temporal-bypass window, after which spatial redistribution re-enters the optimal strategy. In two-dimensional fragmented landscapes, increasing phenological capacity reduced the sampled zigzag-route growth penalty by about 83%, yet movement again became necessary as forcing increased. Interactions introduce a second failure mode. With positive matching dependence and a fine unilateral mutation step, 22 of 24 sampled two-dimensional cells contained a coordination barrier and 21 of 24 converted local extinction into coordinated persistence. In a direct local audit, a coordinated timing shift increased joint low-density growth by 1.095, whereas the same shift by either partner alone decreased its payoff by 5.946 because the partners temporarily became mismatched. Finite-population drift can cross such barriers, but in the sampled regime the accompanying exploration load prevented a gain in long-run mean joint growth. The resulting hierarchy is therefore not simply movement versus phenology. Tracking capacity, locally accessible adaptation, coordinated value, demographic visibility, and stochastic barrier crossing are distinct ecological quantities. The model predicts that temporal adjustment can delay spatial tracking demands while interspecific matching can convert a technically available adaptive route into an evolutionarily inaccessible one.

**Keywords:** climate tracking; phenology; migration; coevolution; evolutionary accessibility; habitat fragmentation; persistence; coordination barrier

---

## 1. Introduction

Environmental change can be tracked along more than one biological axis. A population may move toward newly suitable locations, alter the timing of migration or reproduction, or combine smaller changes in both dimensions. At the level of abiotic mismatch, these responses can look substitutable: one unit of spatial displacement and an appropriately scaled shift in timing may close the same environmental gap.

That observation leaves three harder questions unresolved.

First, does temporal adjustment actually replace spatial tracking, or only postpone it? A seasonal schedule has finite room to shift, whereas directional environmental change can continue to accumulate. If timing saturates, movement should eventually re-enter even when phenological adjustment is initially cheaper.

Second, how does habitat connectivity change this substitution? A spatial response must be realized through actual movement across a landscape. Detours, bottlenecks, and anisotropic movement can make the spatial axis costly in ways that are absent from a one-dimensional moving-optimum model. Timing could therefore act as a temporary bypass of geometric route costs.

Third, what happens when successful tracking must remain coordinated with another species? Two interacting lineages may face the same moving environment but allocate adaptation differently between movement and timing. A coordinated change could improve both species while the same move by either species alone is deleterious because it transiently breaks spatial or phenological matching. In that case the global adaptive solution exists but is inaccessible to unilateral evolution.

Several components of this problem are already established. Climate responses in behaviour, phenology, and geographic range have been explicitly framed as related ways of realigning organisms with their niches (Muthukrishnan et al. 2025), and empirical work shows that combined range and phenology shifts can be associated with stronger population performance (Hällfors et al. 2021; Macgregor et al. 2019). Moving-habitat models already treat dispersal, multidimensional landscapes, and species interactions, while spatial eco-evolutionary models have shown that dispersal can alter adaptation of seasonal timing (Harsch et al. 2017; Pontarp et al. 2015). Likewise, phenological mismatch and the evolution of interacting phenologies under climate change are mature research areas (Visser & Gienapp 2019; Kharouba & Wolkovich 2020; Gilman et al. 2012). We therefore do not treat the coexistence of spatial and temporal responses, or climate-driven interaction mismatch, as the novelty here. The narrower question is whether interacting species that can allocate tracking between space and time can actually reach a jointly valuable alternative through unilateral adaptive changes.

Here we separate these questions explicitly. The framework combines five layers that are usually conflated: environmental tracking capacity, optimization over migration and phenology, unilateral evolutionary accessibility, demographic persistence, and finite-population barrier crossing. The central null is deliberately simple. In a local linear controller, movement and timing enter only through their summed restoring gain and are exactly substitutable before costs and constraints are added. We then restore the ingredients that break this null one by one: finite phenological capacity, explicit spatial redistribution, two-dimensional connectivity, interaction matching, demographic stochasticity, and finite-population evolutionary drift.

The resulting prediction is not that one axis is generally superior. Instead, space–time substitution is scale dependent. Timing can buffer spatial costs and delay movement, but finite capacity forces spatial tracking to re-enter. Interaction matching can synchronize partner responses under moderate forcing, yet the same synchronization can lock both partners into a maladaptive local attractor under stronger forcing. Adaptation can therefore fail even when a jointly persistent tracking architecture is present in the strategy space.

---

## 2. Model

### 2.1 A common tracking coordinate

Environmental demand moves directionally as

```text
D_t = v t
```

A lineage responds through spatial displacement `x` and phenological shift `z`. A conversion factor `s` puts the two responses on one climate-equivalent coordinate,

```text
y = g x + s z
```

where `g` converts spatial position into environmental units. Abiotic mismatch is

```text
e_t = D_t - g x_t - s z_t
```

This construction gives the strongest possible substitution null: movement and timing can close the same mismatch when measured in common units.

### 2.2 Fixed tracking rates

In the nonspatial benchmark, migration/spatial tracking rate `m` and phenological tracking rate `h` jointly close a fraction

```text
q = 1 - exp[-(m + h)]
```

of current mismatch per update. Correction is partitioned according to the relative rates. In the absence of costs, limits, and interactions, strategies with equal `m+h` therefore generate the same abiotic mismatch trajectory.

### 2.3 Explicit moving landscape

The spatial model replaces direct spatial displacement with local population dynamics on fixed patches. In patch `j`,

```text
e_j(t) = D_t - g x_j - s z_t
```

Low-density growth is

```text
g0_j = b - (A/2)e_j^2 - C_track - C_int
```

where `A` is abiotic mismatch strength. Realized demographic growth additionally contains local density regulation. Evolutionary optimization uses low-density growth; density regulation affects abundance only. This separation prevents costly tracking from appearing favorable merely because it depresses abundance and relaxes competition.

Offspring disperse conservatively among neighboring habitat cells. Movement is therefore an emergent shift of the abundance distribution rather than a direct push toward the environmental optimum.

Phenology responds to residual mismatch but is bounded by

```text
|z_t| <= z_max
```

This finite bound is the key mechanism that prevents unlimited replacement of movement by timing.

### 2.4 Interaction matching

For two interacting species, mismatch contains a partner term. In the explicit landscape the climate-equivalent interaction distance is

```text
M^2 = [g(xbar_A - xbar_B)]^2 + [s(z_A - z_B)]^2
```

Interaction strength `I` penalizes this separation. Both species can therefore track the abiotic environment while still failing because they track it on different axes.

### 2.5 Evolutionary accessibility

We distinguish the coordinated value of a strategy from its accessibility under unilateral evolution.

A deterministic rare-substitution walk alternates between species. At each step, one species evaluates local one-step mutants while the partner is held fixed. The best strictly improving mutant fixes. The process stops at a locally accessible endpoint.

Separately, the full matched-pair strategy grid is searched for the coordinated optimum. A coordination barrier is present when the coordinated matched solution has higher joint payoff than the local unilateral endpoint but cannot be reached through the declared sequence of individually improving substitutions.

### 2.6 Demographic persistence

Low-density growth is transported into integer abundance through density-regulated population dynamics with Poisson demographic sampling. Zero abundance is absorbing. For interacting pairs, persistence ends when either partner becomes extinct.

This creates a second distinction:

```text
accessibility gap != persistence consequence
```

A large payoff barrier need not matter demographically if both strategies are safely persistent or nearly doomed.

### 2.7 Finite-population evolutionary drift

For a monomorphic resident and one-step mutant with low-density growth difference `Delta g`, relative fitness is

```text
r = exp(beta * Delta g)
```

Under a frequency-independent Moran mapping with symmetric nearest-neighbor mutation proposals, the exact weak-mutation stationary distribution is

```text
Pi_i ∝ exp[beta (N - 1) g_i]
```

Small populations therefore explore broader regions of the strategy landscape, while large populations concentrate near high-payoff local states. This layer tests whether stochastic substitution can cross a deterministic coordination barrier.

### 2.8 Local closed-loop null

A separate local controller isolates the pure feedback geometry. Let `q_m` be movement-mediated restoring feedback and `q_h` timing-mediated feedback. Mismatch obeys

```text
e_(t+1) = (1 - q_m - q_h)e_t + r
```

Defining

```text
K = q_m + q_h
```

the local controller depends on movement and timing only through total restoring gain. Stability requires

```text
0 < K < 2
```

and equilibrium mismatch is

```text
e* = r / K
```

With quadratic feedback costs,

```text
C = 0.5 c_m q_m^2 + 0.5 c_h q_h^2
```

the minimum-cost allocation at fixed `K` is

```text
q_m* = K c_h / (c_m + c_h)
q_h* = K c_m / (c_m + c_h)
```

This exact substitutability is the analytic null against which the explicit landscape results are interpreted.

### 2.9 Parameter and design status

The complete submission-style parameter map is frozen in
`submission/PAYOFF_B_TRACKING_PARAMETER_TABLE.md`. It separates exact
mathematical definitions from synthetic design axes, robustness-only settings,
and reporting conventions. Numerical grid values are therefore treated as
declared model design choices rather than empirical estimates.

---

## 3. Results

### 3.1 Phenological capacity extends tracking but does not remove the need for movement

In the canonical one-dimensional moving landscape, increasing the allowed phenological shift expanded the sampled persistence frontier. With phenology limit `z_max=0`, the maximum persisted climate velocity was 0.030 and the first failed velocity was 0.035. At `z_max=5`, the corresponding bracket was 0.065 and 0.070.

The frontier was stable to refinement of the migration–phenology strategy grid from `7 x 7` to `11 x 11`. Importantly, every frontier strategy remained migration dominant. Phenological capacity therefore expanded the range of environmental velocities that could be tolerated, but did not replace spatial redistribution near the persistence boundary.

A simple finite-horizon capacity diagnostic reproduced the same trend. The available climate-equivalent tracking capacity increases with both the spatial leading edge and the phenological bound, yielding a near-linear increase in the sampled persistence frontier. The diagnostic is not a persistence theorem, but it captures why timing has a finite operating range.

### 3.2 Two-dimensional fragmentation reveals temporal bypass and spatial re-entry

Two-dimensional landscapes allow route geometry that cannot be represented in one dimension. We compared open habitat with straight and zigzag wall configurations while climate moved along a fixed axis.

At high phenological capacity, the optimal strategy showed a three-stage sequence. In the canonical zigzag design with `z_max=4`,

- at climate velocity 0.04, the optimum was phenology only;
- at 0.05, the optimum remained phenology only;
- at 0.06, migration re-entered and the optimum became mixed;
- at 0.07, the migration component increased further.

The second-wall crossing fraction rose from essentially zero in the phenology-only regime to about 0.132 at velocity 0.06 and 0.314 at velocity 0.07.

This is a finite temporal bypass. Timing can temporarily absorb environmental displacement and delay spatial corridor use, but sufficiently strong directional forcing exhausts the bypass and forces movement back into the solution.

### 3.3 Timing buffers route costs even when movement is anisotropic

In the canonical open-versus-zigzag comparison, the mean low-density growth penalty of the zigzag route was

```text
-0.0419
```

at phenology limit 0 and only

```text
-0.0070
```

at phenology limit 4, an approximately 83% reduction in penalty magnitude.

The same qualitative result survived strong directional anisotropy. Reducing transverse movement weight relative to the climate-axis direction from 1 to 0.1 made the no-phenology zigzag penalty increasingly negative, but phenology limit 4 still reduced penalty magnitude by about 75–76% across all sampled anisotropy levels.

The result is therefore temporal buffering of geometric movement cost, not a claim that timing eliminates fragmentation or rescues persistence in every route geometry.

### 3.4 Interaction matching creates coordination barriers

The strongest qualitative change appears once two interacting species must remain matched.

In the coarse one-dimensional explicit-landscape design, positive interaction produced 52 coordination barriers among 81 positive-interaction cells, with 24 persistence rescues. Refining the unilateral mutation step from 0.2 to 0.1 retained 57 barriers and 21 persistence rescues across 81 cells.

The two-dimensional result was stronger. At mutation step 0.1 and positive interaction, 22 of 24 sampled cells contained coordination barriers and 21 of 24 converted the local endpoint from extinction to coordinated persistence.

The barrier vanished in the no-interaction control. Thus it is not generated by route geometry alone: it arises because partners must remain spatially and phenologically matched while changing their tracking architecture.

### 3.5 The barrier is local, not an artifact of distant optima

A direct one-step audit isolates the mechanism in the canonical two-dimensional zigzag cell.

The resident matched strategy was

```text
(m, h) = (0.2, 0)
```

The coordinated neighboring strategy was

```text
(m, h) = (0.2, 0.2)
```

When both species made the timing shift together, joint low-density growth changed from approximately

```text
-0.840
```

to

```text
+0.255
```

for a coordinated gain of

```text
+1.095
```

Yet if either species made the same timing shift alone, its unilateral gain was approximately

```text
-5.946
```

The unilateral move created a climate-equivalent interaction mismatch of about 3.747.

The coordination barrier therefore exists at one mutation step. The jointly persistent alternative is not merely far away on the strategy surface; it is adjacent but individually disfavored.

### 3.6 Distribution-level overlap strengthens rather than removes the gate

The baseline interaction term uses spatial centroids plus phenological separation. To test whether the barrier was an artifact of centroid compression, we added a Bhattacharyya-overlap penalty based on the full spatial abundance distributions.

Across overlap-penalty scales 0, 0.5, 1, and 2, the canonical cell retained

- a coordination barrier,
- a persistence rescue, and
- the direct one-step sign gate.

The unilateral mutant and resident distributions had very low overlap, about 0.07. Increasing the overlap penalty made the unilateral move more deleterious, with the gain falling from approximately -5.946 at scale 0 to -7.804 at scale 2.

Explicit spatial segregation therefore strengthens the sampled gate rather than explaining it away.

### 3.7 Synchronization changes sign with forcing

Partner-specific tracking preferences were introduced by varying relative movement and phenology costs for the two species.

At moderate forcing, interaction acted as a synchronizer. Without interaction, opposed cost biases produced quantitatively different partner strategies. With interaction strength 0.5 or 1, strategy distance collapsed to zero, interaction mismatch became very small, and all sampled pairs persisted.

At stronger forcing the same synchronizing mechanism became maladaptive. Without interaction, all sampled partner pairs converged to a matched mixed strategy near `(0.2, 0.2)` and persisted. With interaction strength 0.5 or 1, all sampled pairs converged to the same locally accessible migration-only attractor and all went extinct.

Interaction-mediated synchronization is therefore not intrinsically beneficial or harmful. Its sign depends on whether the synchronized local attractor remains inside the persistence envelope.

### 3.8 Coordination barriers are demographically most visible near persistence transitions

The first 32-replicate demographic pilot suggested several large cell-level persistence gains, including a maximum of 0.1875. An independent 128-replicate rerun did not reproduce any gain at or above 0.10. The maximum fell to 0.09375.

The aggregate structure did replicate. Across 396 barrier cells, mean persistence gain was about 0.0055. Cells with local persistence between 0.3 and 0.7 had mean gain about 0.0197, whereas cells already in the 0.9–1 persistence range had mean gain only about 0.0011.

The retained interpretation is a demographic visibility window. Coordination barriers can be mechanistically real but demographically cryptic when both strategies are nearly doomed or nearly certain to persist. Their population consequences become most visible near the persistence transition.

### 3.9 Drift can cross the barrier without producing evolutionary rescue

Finite-population substitution simulations began at a deterministic local endpoint.

At `beta=5`, small populations frequently crossed the barrier: the escape-replicate fraction was 0.94 at `N=10` and 0.97 at `N=30`. At `N=100`, no retained high-payoff escape occurred in the sampled design, and at `N>=300` the local endpoint dominated.

However, stochastic exploration carried a load. The coordinated payoff gain in the representative barrier regime was small relative to the broader distribution of lower-payoff states explored by small populations. Mean long-run joint growth therefore did not exceed the deterministic local endpoint.

The correct conclusion is drift-assisted barrier crossing, not drift rescue.

### 3.10 Explicit feedback turns local substitutability into forcing-dependent complementarity

The local controller predicts exact equivalence of movement and timing feedback at fixed total gain `K`. The explicit landscape violates that equivalence because movement has route costs, finite movement-rate ceilings, and spatial population consequences, whereas timing has its own finite capacity and cost.

In the canonical state-dependent movement-feedback landscape, feedback was unnecessary under weak forcing. Under intermediate forcing, positive movement feedback improved mismatch and low-density growth.

Under stronger forcing, however, movement feedback alone was insufficient. At climate velocities 0.05 and 0.06, none of the seven sampled movement-feedback gains persisted when the independent timing rate was zero. By contrast, all seven persisted when timing rate was 0.25 or 0.5.

Timing also sharply reduced movement demand. At velocity 0.06 and the strongest sampled movement-feedback gain, increasing timing response from zero to 0.25 reduced mean effective movement by about 66%; a timing rate of 0.5 reduced it by about 76% and removed all movement-ceiling contact.

Thus local space–time substitutability becomes forcing-dependent complementarity in an explicit finite landscape.

---

## 4. Synthesis: five quantities that should not be collapsed

The model produces a nested hierarchy:

```text
tracking capacity
!= chosen tracking architecture
!= coordinated value
!= unilateral accessibility
!= population persistence
```

Finite populations add a sixth distinction:

```text
barrier crossing != long-run payoff improvement
```

This hierarchy explains why apparently simple questions such as “can phenology compensate for movement?” or “can drift rescue maladaptation?” do not have one-dimensional answers.

At the abiotic level, timing and movement can close the same mismatch. At the landscape level, they differ because movement must traverse geometry and timing has finite range. At the interaction level, both axes must remain aligned between partners. At the evolutionary level, coordinated changes may be unavailable to unilateral selection. At the demographic level, even a real accessibility barrier matters most near a persistence transition. Finally, stochastic exploration can cross a barrier while reducing mean performance.

---

## 5. Discussion

### 5.1 Temporal adjustment is a buffer, not an unlimited substitute for movement

The strongest recurring result across the landscape models is finite temporal bypass. Phenological adjustment can absorb environmental displacement and substantially reduce the cost of spatial detours. But directional environmental forcing accumulates while the timing axis is bounded. Movement therefore re-enters once the temporal buffer approaches its operating limit.

This distinction matters conceptually. A short-term empirical association in which populations adjust timing while moving little does not imply that temporal adjustment can replace redistribution indefinitely. The model predicts a regime shift: timing first delays spatial demand, then mixed tracking emerges, and movement dominates again near the boundary.

### 5.2 Connectivity changes the realized cost of an otherwise substitutable axis

In the local controller, one unit of restoring feedback has no memory of whether it came from movement or timing. In a landscape, the two axes have different mechanics. Spatial correction has to be realized through redistribution across habitat, while timing changes mismatch without physically crossing a barrier.

This gives phenology a special role under fragmentation: it can reduce the urgency of corridor traversal even when it cannot ultimately remove the need for spatial tracking. The persistence frontier can therefore be controlled by one axis while short-term movement burden is strongly modified by the other.

### 5.3 Mutual dependence can create maladaptive synchronization

Interaction matching adds a qualitatively different failure mode. Under moderate forcing, synchronization is useful because it keeps partners aligned despite intrinsic differences in preferred tracking allocation. Under strong forcing, the same matching pressure can trap both species on a locally accessible architecture that lies outside the persistence envelope.

This is not simply “coevolution slows adaptation.” The coordinated alternative can be adjacent in strategy space and strongly favorable when both partners move together. The obstruction is specifically unilateral accessibility: the transient mismatch cost of moving first is larger than the long-run benefit of reaching the joint alternative.

The result predicts that stronger dependence between partners can sometimes increase failure risk even when a jointly viable solution exists.

### 5.4 Evolutionary accessibility and demographic consequence are different scales

The higher-replication demographic rerun is important because it removes an initially tempting but unstable claim. Large cell-level persistence gains did not replicate. What did replicate was the location of demographic visibility: barriers matter most near persistence transitions.

This makes the theory more, not less, informative. It predicts where an accessibility barrier should become observable as a population effect. Far from demographic thresholds, evolutionary constraints can remain hidden in abundance data even when the underlying strategy landscape is strongly structured.

### 5.5 Drift is a barrier-crossing mechanism, not automatically a rescue mechanism

Small populations explore more broadly and can cross deterministic adaptive barriers. But broader exploration also spends time in low-payoff states. Whether stochastic escape improves long-run performance therefore depends on the payoff gain beyond the barrier relative to the exploration load required to reach and retain it.

In the sampled regime the latter dominated. This separates two ideas that are often rhetorically merged: stochastic barrier crossing and adaptive rescue.

---

## 6. Testable predictions

The synthetic model supports qualitative predictions that can be tested without treating its parameter values as natural thresholds.

1. **Spatial re-entry prediction.** Systems using strong timing adjustment under moderate directional environmental change should show increasing reliance on spatial redistribution as timing approaches an effective seasonal or physiological bound.

2. **Fragmentation-buffer prediction.** Greater timing flexibility should reduce short-term growth or performance penalties caused by spatial detours even when it does not eliminate long-run dependence on connectivity.

3. **Coordination-gate prediction.** In tightly interacting pairs, an individually induced shift in tracking axis should be more costly than the same shift performed by both partners, especially when interaction matching is strong.

4. **Forcing-dependent synchronization prediction.** Stronger partner matching should reduce between-partner tracking divergence under moderate forcing but can increase failure risk under stronger forcing if the synchronized local attractor lies outside the persistence envelope.

5. **Demographic-visibility prediction.** The population-level effect of an evolutionary coordination barrier should be largest near persistence boundaries and weak when both strategies are safely persistent.

6. **Drift-load prediction.** Small populations may show more frequent exploration across a coordination barrier without higher mean long-run performance unless the payoff gain beyond the barrier is large enough to compensate for stochastic occupancy of inferior states.

These are directional predictions. The present synthetic parameter values do not define empirical cutoffs.

---

## 7. Scope and limitations

The framework intentionally uses simplified ingredients to isolate mechanism. The current landscape is a regular grid with declared habitat barriers rather than an empirical resistance surface. Directional environmental change is imposed rather than estimated from a named climate variable. Interaction costs are phenomenological. Evolution proceeds through a specified local mutation neighborhood rather than a full quantitative-genetic process.

The finite horizon is also part of the model definition. Under indefinitely directional environmental change, mismatch and partner separation can accumulate, so the current landscape experiments should not be read as stationary-equilibrium theorems.

Most importantly, no number reported here is a natural prevalence estimate. The fraction of sampled cells containing barriers, the climate velocities defining persistence brackets, the 83% route-cost buffering effect, and the controller gains are properties of declared synthetic designs.

The empirical PAYOFF-B phase-retention programme is therefore kept separate. It asks whether a common response coordinate can be estimated across real migratory systems. The present paper asks a different question: what ecological and evolutionary failures become possible even when movement and timing can, in principle, close the same environmental mismatch?

---

## 8. Conclusion

Movement and phenological change are exactly substitutable only in the most local description of environmental correction. Once finite capacity, route geometry, partner matching, evolutionary accessibility, and demography are restored, that equivalence breaks in structured ways.

Timing can buffer connectivity costs and postpone movement, but it has a finite bypass range. Interaction can synchronize partner tracking, but synchronization can become maladaptive under stronger forcing. A jointly persistent alternative can be present one mutation step away while remaining inaccessible because either partner moving first is selected against. Drift can cross that barrier without guaranteeing a long-run fitness gain.

The central lesson is therefore not that organisms should move or change timing. It is that **adaptive capacity is not the same as adaptive accessibility**. Under a moving environment, persistence can fail because the viable tracking architecture cannot be reached by the sequence of individually favorable changes available to interacting populations.

---

## Prior-art boundary and core references

The full novelty audit is frozen in
`docs/PAYOFF_B_TRACKING_THEORY_PRIOR_ART_20260924.md`.

The manuscript does **not** claim novelty for combining dispersal and phenology, for modelling moving habitat, or for climate-driven mismatch between interacting species. Its candidate contribution is the estimand chain from exact local space-time substitutability to finite temporal bypass, spatial re-entry, a direct unilateral coordination gate, demographic visibility, and finite-N crossing without automatic rescue.

Core references:

- Gilman RT, Fabina NS, Abbott KC, Rafferty NE. 2012. Evolution of plant–pollinator mutualisms in response to climate change. *Evolutionary Applications* 5:2–16. DOI: 10.1111/j.1752-4571.2011.00202.x.
- Hällfors MH et al. 2021. Combining range and phenology shifts offers a winning strategy for boreal Lepidoptera. *Ecology Letters*. DOI: 10.1111/ele.13774.
- Harsch MA et al. 2017. Moving forward: insights and applications of moving-habitat models for climate change ecology. *Journal of Ecology*. DOI: 10.1111/1365-2745.12724.
- Kharouba HM, Wolkovich EM. 2020. Disconnects between ecological theory and data in phenological mismatch research. *Nature Climate Change* 10:406–415. DOI: 10.1038/s41558-020-0752-x.
- Macgregor CJ et al. 2019. Climate-induced phenology shifts linked to range expansions in species with multiple reproductive cycles per year. *Nature Communications* 10:4455.
- Muthukrishnan R, Smiley TM, Title PO, Fudickar AM, Jahn AE, Lau JA. 2025. Chasing the Niche: Escaping Climate Change Threats in Place, Time, and Space. *Global Change Biology*. DOI: 10.1111/gcb.70167.
- Pontarp M, Johansson J, Jonzén N, Lundberg P et al. 2015. Adaptation of timing of life history traits and population dynamic responses to climate change in spatially structured populations. *Evolutionary Ecology* 29:565–579. DOI: 10.1007/s10682-015-9759-6.
- Visser ME, Gienapp P. 2019. Evolutionary and demographic consequences of phenological mismatches. *Nature Ecology & Evolution* 3:879–885. DOI: 10.1038/s41559-019-0880-8.

---

## 9. Frozen result provenance

The numerical claims in this manuscript are restricted to the existing frozen receipts:

- `docs/PAYOFF_B_TRACKING_SYNTHETIC_RESULTS_20260920.md`
- `docs/PAYOFF_B_MOVING_LANDSCAPE_RESULTS_20260920.md`
- `docs/PAYOFF_B_2D_CONNECTIVITY_RESULTS_20260920.md`
- `docs/PAYOFF_B_CLOSED_LOOP_TRACKING_RESULTS_20260920.md`
- `docs/PAYOFF_B_MOVEMENT_FEEDBACK_LANDSCAPE_RESULTS_20260920.md`

The analytic and implementation definitions are in:

- `theory/MIGRATION_PHENOLOGY_TRACKING.md`
- `theory/CLOSED_LOOP_MOVEMENT_PHENOLOGY_TRACKING.md`

No post-2026-09-20 empirical phase-retention result is used as evidence for the synthetic claims in this manuscript.

---

## 10. Figure set

The complete vector figure set is rendered by:

```bash
python scripts/render_tracking_theory_figures.py \
  --output-dir submission/tracking_theory_figures
```

Full submission captions are frozen in
`submission/PAYOFF_B_TRACKING_FIGURE_CAPTIONS.md`.

- **Figure 1 — Conceptual hierarchy:** `PAYOFF_B_TRACKING_FIG1_CONCEPT.svg`
- **Figure 2 — Finite temporal bypass:** `PAYOFF_B_TRACKING_FIG2_TEMPORAL_BYPASS.svg`
- **Figure 3 — Coordination gate:** `PAYOFF_B_TRACKING_FIG3_COORDINATION_GATE.svg`
- **Figure 4 — Synchronization changes sign:** `PAYOFF_B_TRACKING_FIG4_SYNCHRONIZATION.svg`
- **Figure 5 — Demographic visibility and finite-N crossing:** `PAYOFF_B_TRACKING_FIG5_DEMOGRAPHY_DRIFT.svg`
- **Figure 6 — Local null versus explicit landscape:** `PAYOFF_B_TRACKING_FIG6_COMPLEMENTARITY.svg`

CI renders the same six figures from the frozen receipt chain and uploads them
as artifact `payoff-b-tracking-theory-figures`.
