# PAYOFF-B V5 novelty-collision resolution — 2026-10-05

Status: **PUBLICATION BRANCH STOPPED**

## Decision

PAYOFF-B V5 is stopped as an independent publication branch.

The reason is not lack of ecological importance or lack of data. The remaining
V5 biological claim is already occupied by Brlík et al.'s multi-species
annual-cycle analysis.

## Decisive prior evidence

The 2023 European Ornithologists' Union congress abstract by:

Brlík V, Procházka P, Hahn S & Norris DR

was titled:

**Time dependencies across stages of the annual cycle in migratory birds.**

The abstract reports:

- year-round movement data from **more than 2,000 individuals**;
- **62 passerine and near-passerine species**;
- the strongest timing link between non-breeding departure and breeding arrival;
- breeding departure also predicting non-breeding arrival;
- only a weak link between non-breeding arrival and subsequent non-breeding
  departure;
- the explicit conclusion that timing links are strong across migratory periods
  but **break down over the stationary non-breeding period**.

The same abstract states that a multi-species annual-cycle analysis had been
missing and explicitly hypothesizes weakening of timing links during prolonged
stationary non-breeding periods.

The accepted/in-press Nature Ecology & Evolution paper:

Brlík V, Procházka P, Rushing CS, Storch D, Schmaljohann H, et al.,
Norris DR. 2026.
**Temporal links in avian migration schedules across the annual cycle**

is the later publication lineage of that biological question.

## Collision with V5

V5 H1 was frozen as:

[
eta_{m stationary}<eta_{m active migration}.
]

The EOU abstract already reports the same biological contrast at a much larger
multi-species scale:

- strong temporal linkage across migratory periods;
- weak temporal linkage across the stationary non-breeding period.

Therefore H1 is not an independently novel ecological prediction.

The fact that V5 uses an unstandardized day-for-day `beta_AB` rather than the
exact implementation used by Brlík et al. is not enough to create biological
novelty.

## H2 does not rescue the paper

V5 H2 asked whether longer available stationary time predicts weaker
propagation.

This may remain a technically distinct moderator, but after H1 is occupied it
is not a sufficient standalone ecological contribution to justify continued
corpus accumulation as a separate PAYOFF-B paper.

H2 may be retained only as:
- a future secondary analysis;
- a replication/extension if the Brlík paper leaves the moderator unresolved;
- or a component of another biologically distinct study.

It does not reopen V5.

## Existing PAYOFF-B effects

The nine already opened source-faithful effects remain provenance.

They are not deleted, reclassified, or interpreted as support for H1/H2.

```text
OPENED_EFFECTS = 9
OPENED_BIOLOGICAL_COHORTS = 5
H1_MODEL_RUN = NO
H2_MODEL_RUN = NO
```

No additional primary V5 effect extraction should be performed solely to
complete the stopped meta-analysis.

## What this establishes about field position

The collision strongly supports the ecological importance of the user's
original question:

- annual-cycle timing stages are genuinely linked;
- flexibility differs among annual-cycle transitions;
- stationary periods can act as schedule-reset/buffering periods;
- this matters for vulnerability to environmental change.

These are not artificial PAYOFF-B constructions.

However, they are now active mainstream questions in migration ecology and are
already being addressed by a large international tracking consortium.

## Publication rule

```text
V5_PUBLICATION_BRANCH = STOPPED_PRIOR_ART_COLLISION
V5_H1 = CLOSED_PRIOR_ART
V5_H2 = DORMANT_SECONDARY_ONLY
V5_CORPUS_EXTRACTION = STOP
V5_EFFECTS = PROVENANCE_ONLY
```

A future PAYOFF-B publication must be biologically orthogonal to the general
question of where annual-cycle timing links strengthen or weaken.

A different statistical estimator, larger extracted corpus, or another
stationary-versus-active comparison does not qualify as an orthogonal
contribution.
