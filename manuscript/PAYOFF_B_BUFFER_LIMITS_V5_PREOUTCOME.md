# Where does the annual cycle absorb delay?

## A comparative synthesis of temporal buffering in migratory birds

**PAYOFF-B Paper 2 — V5 PREOUTCOME comparative draft**  
**Date:** 2026-10-03  
**Status:** novelty hold as of 2026-10-04. Nine source-faithful effects from five biological cohorts are retained as provenance, but H1/H2 must not be run until the accepted 2026 Nature Ecology & Evolution paper `Temporal links in avian migration schedules across the annual cycle` is audited for overlap.

> **Novelty hold.** A current-literature check identified an accepted/in-press
> 2026 *Nature Ecology & Evolution* study, Brlík et al., *Temporal links in
> avian migration schedules across the annual cycle*, plus an associated public
> Zenodo dataset (10.5281/zenodo.18175801). Its title and indexed problem
> statement overlap directly with the candidate V5 contribution. The present
> draft is therefore not an active submission candidate until that collision is
> resolved. See `docs/PAYOFF_B_V5_NEE_2026_COLLISION_HOLD_20261004.md`.

## Abstract

**Aim:** Migratory birds experience annual cycles in which delays can either
propagate across successive stages or be absorbed before reaching
fitness-sensitive events. Individual and multi-species studies already quantify
domino effects, temporal reset and departure-to-arrival carry-over. We ask a
narrower comparative question: whether day-for-day timing propagation differs
systematically among annual-cycle transition types, and what predicts the
limits of buffering.

**Methods:** We synthesize sequential timing relationships from studies that
measure two annual-cycle events in the same individuals or cohorts. The primary
effect size is the unstandardized day-for-day timing-propagation coefficient
\(\beta_{AB}\), the change in timing at stage B associated with a one-day
timing deviation at the preceding stage A. A value of 1 denotes one-for-one
carry-over, values between 0 and 1 partial buffering, 0 statistical reset,
negative values reversal and values above 1 amplification. Repeatability and
correlation coefficients are not converted into propagation coefficients.

**Primary predictions:** Timing deviations should propagate less strongly
across adjustable stationary periods than across active migration segments.
Within stationary periods, longer available intervals should provide more
opportunity to absorb delay. A secondary fitness layer asks whether delays that
survive to the last pre-breeding transition are more likely to carry
reproductive or survival consequences.

**Status:** Nine individual transition effects have been opened under the frozen contract, but no H1/H2 comparative model has been run. Further corpus extraction and all comparative modelling are paused pending the 2026 Nature Ecology & Evolution novelty-collision audit.

---

## 1. Introduction

A bird can be late without remaining late.

A delay generated during breeding, departure or migration may be transmitted
to the next stage in a domino effect. It may also disappear if an individual
shortens a stationary period, changes stopover duration, migrates faster or
otherwise adjusts its annual schedule. Both outcomes are well documented.

Full-annual-cycle studies illustrate the contrast. Hudsonian godwits can accrue
timing deviations over several migratory stages and later erase them without
detectable breeding or survival penalties. Icelandic whimbrels use stationary
periods to absorb delays, while some spring transitions still transmit delay
toward laying. Tree swallows can show a domino effect from breeding through
autumn migration that is reset before spring migration. Barn swallow studies
identify specific premigration or winter intervals that buffer links between
breeding investment, migration timing and subsequent breeding success.

These examples establish that temporal buffering exists. They do not yet tell
us how general each type of transition is as a buffer.

This distinction matters because contemporary phenological-mismatch ecology is
increasingly concerned with buffering. Weir and Phillimore (2024) argued that
asynchrony may often be less damaging than assumed because organisms and
populations possess mechanisms that reduce asynchrony or its fitness
consequences. They explicitly called for identifying systems with fewer
buffers and, especially, the limits of those buffers.

Migration ecology provides a tractable case because annual-cycle events are
ordered and often measured in the same time units. A one-day departure delay
can be followed through stopover, arrival and breeding. Comparative work has already moved partway toward this question. Schmaljohann
(2019) estimated departure-to-arrival timing slopes across multiple migratory
bird species, showing that later starts generally remained later at arrival but
with partial compression. Van Bemmelen et al. (2024) explicitly used
stage-to-stage slopes to quantify compensation and carry-over in Arctic skuas.
Meta-analysis has separately quantified the repeatability of migration dates
across years, while global tracking compilations have examined mean annual-cycle
timing and broad carry-over paths. What we did not find is a synthesis that
places **different annual-cycle transition classes** on the same unstandardized
day-for-day propagation scale.

Our question is therefore deliberately simple:

> **Where in the annual cycle do migratory birds absorb temporal delays, and
> what predicts when those delays persist?**

We treat temporal buffering as a transition property, not a species label.
The same individual or species can transmit delay through one segment and
erase it during another. This shifts attention from whether a species is
'flexible' to where flexibility can actually change the annual schedule.

---

## 2. Effect-size definition

### 2.1 Timing propagation

For two sequential events A and B, let \(d_A\) and \(d_B\) be timing
deviations in days from the appropriate population/year reference.

We define

\[
d_B=a+\beta_{AB}d_A+\varepsilon.
\]

The unstandardized slope \(\beta_{AB}\) is the primary effect size.

- \(\beta_{AB}=1\): one day early or late at A remains one day early or late at B.
- \(0<\beta_{AB}<1\): the deviation is partly absorbed.
- \(\beta_{AB}=0\): no linear propagation remains at B.
- \(\beta_{AB}<0\): the deviation reverses sign.
- \(\beta_{AB}>1\): the deviation is amplified.

This coefficient is descriptive. It is not a direct estimate of a behavioral
controller, physiological clock or adaptive plasticity.

### 2.2 Why not use repeatability?

Repeatability asks whether individuals that are early in an event in one year
tend to be early in that same event in another year. Transition propagation
asks whether being one day late at an earlier event leaves a measurable delay
at the next event.

Both are useful, but they answer different biological questions.

Likewise, a correlation coefficient depends on the variance of both dates and
cannot be interpreted as the fraction of a delay that remains. The primary
synthesis therefore uses raw slopes in common time units.

---

## 3. Prospective synthesis

### 3.1 Study eligibility

The primary synthesis is restricted to migratory birds and sequential
annual-cycle timing events.

A study enters the primary effect-size corpus only if it supplies:

1. two temporally ordered annual-cycle events;
2. measurements on the same individuals, or an explicitly paired cohort;
3. timing in days or a directly convertible temporal unit;
4. an unstandardized transition slope with uncertainty, or individual-level
   data from which that slope can be estimated.

Studies reporting only repeatability, population mean dates or correlation
coefficients do not enter the primary slope synthesis.

### 3.2 Transition classes

Transitions are classified before effect-size modelling as:

- active spring migration;
- spring stopover or staging;
- non-breeding stationary period;
- arrival-to-breeding / pre-laying period;
- breeding / post-breeding interval;
- active autumn migration;
- autumn stopover or staging;
- other stationary period.

Ambiguous multi-process intervals are coded MIXED and excluded from the
primary class comparison.

### 3.3 Primary hypotheses

**H1: Stationary-period buffering.**

\[
\beta_{\rm stationary}<\beta_{\rm active}.
\]

If stationary periods are the principal opportunities to reset annual timing,
a one-day deviation should be transmitted less strongly across them than
across active migration segments.

**H2: Available-time hypothesis.**

Within stationary transitions, longer available intervals should be associated
with weaker delay propagation.

This variable is extracted only when interval duration is reported or
derivable from the same annual-cycle schedule. No species-average value is
inserted after observing an effect size.

### 3.4 Fitness layer

Timing recovery is not treated as fitness recovery.

For the subset of studies reporting vital-rate outcomes, we separately record
survival or return, breeding probability, nest initiation, hatching/fledging
success and seasonal fecundity.

An end-to-end fitness-rescue design requires the same individuals to provide:

\[
\text{incoming timing deviation}
\rightarrow
\text{buffering/correction}
\rightarrow
\text{outgoing timing deviation}
\rightarrow
\text{survival or reproduction}.
\]

Individual quality or physiological state is coded separately because
high-quality individuals can both buffer delays and achieve high fitness,
creating an apparent causal benefit of buffering.

---

## 4. Analysis plan

The primary analysis is a multilevel meta-regression of \(\beta_{AB}\) with
study, species and population/cohort as grouping levels.

The primary moderator is transition type: stationary versus active migration.
The second declared moderator is available interval duration among stationary
transitions.

Phylogenetic structure will be included only if the number and distribution of
species permit stable estimation; the non-phylogenetic multilevel model
remains the declared baseline.

Prespecified sensitivity analyses are:

- within-year or year-adjusted timing estimates only;
- individual-level estimates only;
- leave-one-study-out;
- leave-one-species-out;
- removal of MIXED transitions;
- removal of slopes reconstructed from figures.

A secondary synthesis may summarize standardized correlations, but those
effects remain separate and are not translated into day-for-day propagation.

---

## 5. Position relative to prior work

This study does not ask whether annual-cycle buffering exists. That question
has already been answered in multiple species.

It also does not ask whether migration timing is repeatable; a formal
meta-analysis already addresses that problem. Nor does it introduce the
stage-to-stage timing slope itself: departure-to-arrival slopes have already
been estimated across species, and carry-over strength has been expressed as a
day-for-day slope within annual-cycle studies.

The candidate contribution is narrower, comparative and transition-based:

> **How much of a temporal deviation survives each kind of annual-cycle
> transition?**

If the eligible corpus is large enough, a quantitative buffer map would make
existing evidence directly comparable across **biologically different
transitions**: active migration, stopover/staging, stationary non-breeding
periods and arrival-to-breeding intervals.
It would also provide a way to identify transitions where disturbances are
most likely to be transmitted into breeding or another fitness-sensitive
stage.

The intended ecological interpretation is concrete. A wintering site or
stopover can function not only as habitat or fuel supply, but also as temporal
slack. If such a period normally reduces a five-day delay to one day, loss of
that interval can expose downstream stages to timing variation that was
previously hidden.

That is a conservation question about where annual-cycle schedules have room
to recover, not a claim for a new generic control theory.

---

## 6. Fitness and interaction extensions

The fitness analysis remains secondary because vital-rate outcomes are likely
to be sparse and heterogeneous.

The first question is whether delays reach a fitness-sensitive stage. The
second is whether the remaining delay, or the behavior used to remove it,
changes survival or reproduction.

Interaction mismatch is retained only as a downstream extension. If partners
possess different buffer maps, a disturbance can be absorbed by one actor but
propagated by another. That possibility follows naturally once annual-cycle
buffering has been quantified, but it is not required for the primary V5
claim.

---

## 7. Current status

The study design and eligibility rules were fixed before focal comparative
outcomes were opened.

Current prior-art anchors include full-annual-cycle studies of Hudsonian
godwits, Icelandic whimbrels, tree swallows, barn swallows and other migrants;
the Franklin et al. migration-timing repeatability meta-analysis; the Wang et
al. macro-scale annual-cycle tracking compilation; and the Weir & Phillimore
phenological-buffering synthesis.

These sources define the question and the novelty boundary. They are not a
result of V5.

---

## 8. Conclusion

Migratory schedules do not simply shift as rigid blocks. A delay can persist
through one stage and disappear in the next.

The unresolved comparative question is whether the strength of propagation
shows a reproducible pattern across transition classes once studies are placed
on the same day-for-day scale.

PAYOFF-B V5 therefore treats each annual-cycle transition as a potential
buffer and asks how many days of an earlier timing deviation survive it.

If successful, the synthesis will identify the annual-cycle stages that act as
temporal safety margins—and the stages at which there is effectively nowhere
left to recover.