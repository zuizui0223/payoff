# PAYOFF-B V5 — 2026 Nature Ecology & Evolution novelty-collision hold

Date: **2026-10-04**  
Status: **FAIL-CLOSED NOVELTY HOLD; H1/H2 MUST REMAIN UNRUN**

## Trigger

A current-literature check identified the accepted/in-press paper:

**Brlík V, Procházka P, Rushing CS, Storch D, Schmaljohann H, et al.,
Norris DR. 2026. "Temporal links in avian migration schedules across the annual
cycle." Nature Ecology & Evolution. In press.**

The paper is listed as in press by multiple author/institutional publication
pages, including the Norris Lab and the SFB 1372 publication list.

A public dataset is also registered:

**Data for Temporal links in avian migration schedules across the annual cycle**
Zenodo master DOI: **10.5281/zenodo.18175801**

ORCID records list published versions including:
- 10.5281/zenodo.18175802
- 10.5281/zenodo.18433481
- 10.5281/zenodo.19821864

The dataset record is dated 2026-04-27 in the current ORCID index.

## Why this threatens V5 directly

V5 currently asks:

> Where in the annual cycle do migratory birds absorb temporal delays, and what
> predicts when those delays persist?

The only remaining V5 novelty after the 2026-10-03 audit was a
cross-transition comparative synthesis of temporal links/buffering across the
annual cycle.

The new in-press paper's title directly targets **temporal links in avian
migration schedules across the annual cycle**.

The public repository snippet begins by asking how tightly annual-cycle events
are linked and how much flexibility exists in migration schedules, explicitly
framing those links/flexibility as relevant to vulnerability under
environmental change.

The author list is a very large international tracking consortium and includes
many investigators/datasets that also appear in the V5 source literature.

Therefore this is not a peripheral citation. It is a **high-probability direct
novelty collision**.

## What is established now

```text
NEE_2026_TITLE = TEMPORAL_LINKS_IN_AVIAN_MIGRATION_SCHEDULES_ACROSS_THE_ANNUAL_CYCLE
NEE_2026_STATUS = IN_PRESS_NATURE_ECOLOGY_AND_EVOLUTION
NEE_2026_DATASET = ZENODO_10.5281/zenodo.18175801
NEE_2026_PROBLEM_FRAME = ANNUAL_CYCLE_LINKAGE_AND_SCHEDULE_FLEXIBILITY
V5_TOPIC_OVERLAP = VERY_HIGH
```

## What is not yet established

The currently accessible public indexes do **not yet safely expose** the full
accepted manuscript, complete abstract, analysis code, or Zenodo file contents
in this execution environment.

Therefore we have not yet verified whether Brlík et al. 2026:

1. uses unstandardized day-for-day slopes;
2. compares active migration with stationary transitions;
3. estimates transition-specific link strength across the full annual cycle;
4. tests interval duration as a moderator;
5. includes fitness/vital-rate endpoints;
6. uses exactly the same underlying cohorts as the current V5 corpus;
7. reports a common-estimand "buffer map" equivalent to V5.

No claim of exact duplication is licensed until those items are checked.

## Conservative decision

Because the only remaining V5 novelty is close to the explicit title and
problem statement of an accepted 2026 Nature Ecology & Evolution paper, the
burden of proof reverses.

V5 must now demonstrate a clear non-overlapping contribution **before** any
comparative model is opened.

```text
V5_NOVELTY_STATUS = HOLD_2026_NEE_COLLISION
V5_CORPUS_EXTRACTION = PAUSE_FOR_PUBLICATION_NOVELTY_AUDIT
V5_H1 = DO_NOT_RUN
V5_H2 = DO_NOT_RUN
V5_PUBLICATION_CLAIM = NONE_PENDING_COLLISION_RESOLUTION
```

The nine already opened source-faithful effects remain provenance. They are not
deleted, retuned, or interpreted.

## Reopening rule

V5 can reopen only if the accepted Brlík et al. paper / public code-data package
is inspected and one of the following is documented:

### Reopen A — distinct estimand

Brlík et al. do not quantify a common day-for-day transition propagation
estimand, while V5's raw `beta_AB` comparison answers a biologically distinct
question not recoverable from their analysis.

### Reopen B — distinct transition contrast

Brlík et al. quantify temporal links broadly but do not test the specific
stationary-versus-active transition contrast or another independently declared
V5 contrast that remains ecologically meaningful.

### Reopen C — distinct fitness/conservation question

Their study maps schedule linkage, while a predeclared PAYOFF-B analysis links
loss of a specific buffering transition to an independently measured vital
rate or disturbance response not analyzed by Brlík et al.

A difference in statistical implementation alone is **not** sufficient
novelty.

## Stop rule

If Brlík et al. already provide a broad cross-transition map of annual-cycle
temporal links/flexibility at comparable biological scale, V5 should stop as a
publication branch rather than search for a cosmetic distinction.

Possible retained uses would then be:
- provenance / independent reproduction;
- a methods note only if the raw day/day estimand materially changes ecological
  inference;
- a genuinely orthogonal fitness or conservation analysis with independent
  data.

## Current scientific interpretation

This collision is informative rather than a failure.

The repeated PAYOFF-B reframing has converged onto a question that a large
international migration-ecology consortium is independently treating as
important enough for Nature Ecology & Evolution. That strongly validates the
**ecological importance of the question**, while simultaneously threatening
PAYOFF-B's **publication novelty**.

The correct response is to protect the latter boundary rather than force a
difference.
