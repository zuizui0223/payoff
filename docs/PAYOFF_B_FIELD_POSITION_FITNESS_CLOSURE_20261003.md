# PAYOFF-B field position and fitness closure — 2026-10-03

Status: **conceptual correction after V3 science freeze**

## 1. Primary ecological field

PAYOFF-B belongs primarily to **full-annual-cycle migration ecology / movement
ecology**, with **carry-over effects and life-history fitness** as the fitness
framework and **global-change phenology** as the environmental context.

It is not primarily a generic phenological-mismatch paper, a chronobiology
paper, or a new control-theory paper.

The field already asks how migrants integrate local cues and internal state,
make movement decisions, transform those decisions into realized trajectories,
and ultimately pay survival or reproductive consequences across the annual
cycle.

Key anchors:
- Winkler et al. 2014, *Movement Ecology*, "Cues, strategies, and outcomes:
  how migrating vertebrates track environmental change".
- Harrison et al. 2011, *Journal of Animal Ecology*, carry-over effects as
  drivers of fitness differences.
- Kharouba & Wolkovich 2020, *Nature Climate Change*, theory-data disconnects
  in phenological mismatch research.
- Hahn et al. 2025, *Journal of Neuroendocrinology*, timing mismatch versus
  carry-over trade-offs.
- Léandri-Breton et al. 2024, *Journal of Animal Ecology*, individual quality
  versus carry-over effects across the annual cycle.
- 2026 migration-ecology systematic review identifying individual migration
  decisions, mortality and habitat-quality consequences as major knowledge
  gaps.

## 2. What is already known and must not be claimed as PAYOFF-B novelty

The following are prior art:

1. Migrants often decide using cues separated in space and time from the
   fitness-decisive environment.
2. Stopovers can provide new environmental information.
3. Departure timing is not equivalent to arrival timing.
4. Migrants can compensate en route by changing speed, stopover duration or
   route.
5. Such compensation can be costly.
6. Timing deviations can carry over across annual-cycle stages.
7. Carry-over effects can alter survival or reproduction.
8. Timing flexibility can reduce a current mismatch while increasing costs at
   a later annual-cycle stage.
9. Phenological shifts can have demographic consequences, but those
   consequences depend strongly on life history and annual-cycle stage.

These ideas are central to migration ecology and full-annual-cycle ecology, not
new PAYOFF-B discoveries.

## 3. The real unresolved ecological question

The field-level question PAYOFF-B should address is:

> **When does correcting a seasonal timing error actually rescue fitness,
> rather than merely restore calendar timing or move the cost to another stage
> of the annual cycle?**

This is a real unresolved problem because phase recovery, survival,
reproduction and population consequences are not interchangeable endpoints.

## 4. Fitness closure

Let an individual enter a focal stage with timing error e_in and choose a
correction action u. Let the action yield e_out and alter survival and later
reproductive value.

For a one-cycle representation,

[
W(u)=S(u)R(e_{out}),
]

where:
- S(u) is survival through the correction / migration stage;
- R(e_out) is expected subsequent reproductive output or reproductive value
  given residual timing error.

Correction is a **fitness rescue** only if

[
oxed{
W(u)>W(0)
}
]

or equivalently

[
oxed{
Delta log S
+
Delta log R
>0.
}
]

Thus

[
	ext{phase recovery}

otRightarrow
	ext{fitness recovery}.
]

For long-lived or multi-stage organisms, R is replaced by the appropriate
continuation reproductive value / future-state value. This is standard
life-history bookkeeping, not a claimed new theorem.

The existing quadratic controller loss,

[
L(u)=kappa u^2+mu(e-u)^2,
]

is therefore only a reduced approximation to the biological fitness problem.
The first term corresponds to correction costs; the second to residual
mistiming costs. Natural interpretation requires mapping these terms to actual
vital rates.

## 5. Natural systems already show different regimes

### A. Timing rescue with a detectable survival cost — American redstart

Dossman et al. 2023:
- approximately 10-d delayed departure;
- approximately 43% faster migration;
- approximately 6.3% lower apparent annual survival.

This demonstrates that calendar compensation can carry a fitness cost.
The study does not by itself estimate net lifetime fitness rescue because the
reproductive benefit recovered by acceleration and the survival effect were not
jointly measured as a complete lifetime-fitness contrast in the same tracked
individuals.

### B. Timing deviations erased without detected survival/reproductive penalty — Hudsonian godwit

Senner et al. 2014:
- timing deviations arose and dissipated across the full annual cycle;
- large arrival variation at the nonbreeding site contracted strongly by
  subsequent departure;
- timing deviations were not associated with detected breeding-success or
  survival penalties.

This is a natural example in which timing recovery is consistent with
demographic buffering rather than detectable fitness debt.

### C. Delay creates reproductive fitness loss — greater snow goose

Legagneux / Bêty experimental work:
- experimentally imposed staging delay carried over to reproduction;
- reproductive success was reduced strongly in two years, with effects
  buffered in a favourable breeding year.

Recent follow-up work also shows migration-stage stress can carry over to
survival.

This demonstrates that failure to absorb a timing/state perturbation can
produce actual vital-rate consequences.

### D. Phase correction without a direct fitness endpoint — mule deer

Ortega et al. 2023 and the PAYOFF-B source-data reanalysis quantify strong
en-route phase convergence and signed speed/stopover compensation.

They are a strong **phase-rescue** example but do not close the
**fitness-rescue** question.

## 6. What ecologists actually want to know

The practical questions are:

1. At which annual-cycle stage is a timing deviation still reversible?
2. Which action removes it: speed, stopover, route, settlement or breeding
   delay?
3. What survival, energetic or reproductive cost is paid for that correction?
4. Does correction improve net annual-cycle fitness?
5. Which life histories can tolerate aggressive correction?
6. Which habitats or stopovers are necessary to preserve correction capacity?
7. At the population level, which vital rate converts phenological adjustment
   into population persistence?

These questions matter for conservation because final arrival synchrony can
hide costly trajectories, while temporary timing deviations can be harmless if
later stages absorb them without vital-rate loss.

## 7. Novelty boundary after literature audit

The following should **not** be the main novelty claim:
- "migrants update information";
- "migrants compensate timing error";
- "compensation has costs";
- "timing stages are linked";
- "shared climate forcing can produce different phenological shifts";
- "carry-over effects matter";
- "timer and controller are different mechanisms".

The current pairwise mismatch identity remains a valid mathematical result, but
its ecological headline is too close to the established idea that interacting
species differ in phenological responses.

The defensible PAYOFF-B contribution is narrower:

> **a common stagewise framework that keeps timing-state recovery and
> full-annual-cycle fitness recovery as separate estimands, so that the same
> final phenological date can represent successful adaptation, costly
> compensation or unresolved fitness debt.**

This is primarily a **conceptual / identification contribution**, not a claim
that PAYOFF-B discovered en-route compensation or carry-over effects.

## 8. Consequence for paper positioning

Recommended primary question:

> **When does seasonal timing correction rescue fitness across the annual
> cycle?**

Recommended biological message:

> **Final synchrony is not sufficient evidence of climate adaptation. To know
> whether an organism has recovered, we must reconstruct the timing trajectory
> and measure the survival and reproductive consequences of the actions used to
> correct it.**

The interaction-mismatch result should remain a downstream extension:
different correction trajectories can also alter synchrony between partners,
but this should not carry the main novelty claim.

## 9. What would directly close the empirical gap

The decisive design follows the same individuals through:

[
e_{in}
ightarrow
u
ightarrow
e_{out}
ightarrow
survival
ightarrow
reproduction.
]

It must measure:
- incoming signed timing error;
- correction action(s);
- outgoing timing error;
- survival during/after correction;
- subsequent reproduction;
- individual quality / state to separate compensation from quality effects.

This is the direct natural test of **fitness rescue**.

Until such a dataset is analysed, PAYOFF-B can close the fitness logic
theoretically and triangulate it with natural systems, but must not claim
end-to-end empirical identification of net fitness rescue.
