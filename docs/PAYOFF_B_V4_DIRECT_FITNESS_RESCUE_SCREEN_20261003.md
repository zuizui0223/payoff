# PAYOFF-B V4 direct fitness-rescue screen — 2026-10-03

Status: **FAIL-CLOSED NOVELTY AUDIT**

Purpose: test whether the V4 question

> *When does seasonal timing correction rescue fitness across the annual cycle?*

is both (i) directly testable with public data and (ii) still sufficiently
unresolved to carry PAYOFF-B novelty.

This screen was defined before opening any new PAYOFF-B analysis of candidate
datasets. It does not reopen V2/V3 preregistered outcomes.

## Admission requirements for a direct fitness-rescue test

A system qualifies for an end-to-end direct test only if the same biological
individuals provide, or can be linked to:

1. **incoming timing state** — a signed or experimentally imposed timing
   deviation before the focal correction stage;
2. **correction action** — speed, stopover, route, waiting, settlement or other
   behavior measured after that deviation;
3. **outgoing timing state** — a later timing coordinate allowing recovery or
   persistence of the deviation to be assessed;
4. **fitness endpoint** — survival and/or subsequent reproduction;
5. **individual identity linkage** across items 1–4;
6. **quality/state control** sufficient to distinguish correction from
   individual-quality confounding;
7. **data access** sufficient for independent analysis if PAYOFF-B is to claim a
   new empirical result.

A published result can be a strong natural anchor without satisfying all seven.

## Candidate A — American redstart, Dossman et al. 2023

Source:
- Dossman BC et al. 2023. *Ecology* 104:e3938.
- DOI: 10.1002/ecy.3938.
- Public code/data repository: Zenodo 10.5281/zenodo.7271787.

Published result:
- relatively late departure predicted faster migration;
- a 10-d delay corresponded to approximately 43% faster migration;
- later relative migration timing was associated with lower apparent annual
  survival.

Critical design boundary:
- the paper states that the low number of radio-tagged individuals **precluded a
  direct assessment of migration rate on survival**;
- migration-rate inference used tracking subsets;
- survival inference used the separate 2010–2019 color-band mark-resight
  dataset with relative departure timing as predictor.

Decision:

```text
INCOMING_TIMING = YES
CORRECTION_ACTION = YES
OUTGOING_TIMING = PARTIAL
FITNESS_ENDPOINT = YES
SAME_INDIVIDUAL_ACTION_TO_FITNESS = NO
DIRECT_FITNESS_RESCUE_TEST = FAIL
ROLE = COSTLY_COMPENSATION_ANCHOR
```

PAYOFF-B must not write that the same birds observed to accelerate migration
were shown to incur the 6.3% survival reduction.

## Candidate B — pied flycatcher, Bell et al. 2024

Source:
- Bell F et al. 2024. *Scientific Reports* 14:4075.
- DOI: 10.1038/s41598-024-53575-2.
- UK tracking archive: Movebank Data Repository 10.5441/001/1.1732qn7j.

Published design:
- 62 individuals had estimated non-breeding departure dates;
- 57 had complete spring migrations;
- tracking was linked to subsequent breeding phenology and performance;
- clutch size and fledgling number were measured in tracked individuals.

Published pattern:
- earlier departure was followed by longer spring migration and earlier
  breeding-ground arrival;
- departure order was largely maintained through arrival and breeding;
- longer spring migration was associated with larger clutch size and, in males,
  more fledglings.

Decision:

```text
INCOMING_TIMING = YES
TRAJECTORY = YES
OUTGOING_TIMING = YES
REPRODUCTION = YES
SAME_INDIVIDUAL_LINKAGE = YES
SIGNED_ERROR_CORRECTION = NO
DIRECT_FITNESS_RESCUE_TEST = FAIL
ROLE = TRAJECTORY_TO_REPRODUCTION_ANCHOR
```

This is a strong full-annual-cycle trajectory–fitness dataset, but it does not
represent late individuals correcting a signed error. It therefore cannot be
relabeled as a correction-rescue test.

## Candidate C — juvenile white stork delay experiment, Bontekoe et al. 2023

Source:
- Bontekoe ID et al. 2023. *Proc. R. Soc. B* 290:20231268.
- DOI: 10.1098/rspb.2023.1268.
- Public Movebank datasets and Zenodo analysis code.

Design:
- migration timing was experimentally delayed;
- nearly continuous GPS trajectories measured subsequent movement;
- delayed birds changed speed and stopover behavior;
- survival was measured in the same experimental cohorts.

Published outcome:
- delayed migrants moved faster and spent fewer days at stopovers;
- delayed birds had lower mortality than controls;
- they migrated shorter distances and wintered closer to the breeding area;
- none reached the traditional African wintering areas;
- migration choices remained altered in later life.

Decision:

```text
EXPERIMENTAL_TIMING_PERTURBATION = YES
CORRECTION_ACTION = YES
SURVIVAL = YES
SAME_INDIVIDUAL_COHORT = YES
RETURN_TO_ORIGINAL_PHASE_TARGET = NO
DIRECT_FITNESS_RESCUE_TEST = FAIL
ROLE = CAUSAL_STRATEGY_RESET_ANCHOR
```

The manipulation is unusually strong causal evidence, but the birds did not
simply restore the original seasonal trajectory. They adopted a different
migration strategy/destination. Calling this "phase rescue" would erase the
main biology of the experiment.

## Candidate D — Hudsonian godwit, Senner et al. 2014

Source:
- Senner NR et al. 2014. *PLoS ONE* 9:e86588.
- DOI: 10.1371/journal.pone.0086588.

Design:
- 26 individual godwits contributed annual-cycle tracking;
- three consecutive years of migration tracks were coupled to four years of
  breeding-success observations;
- stage-specific timing deviations from annual population schedules were
  quantified;
- stop number and stopover duration were measured during northward migration;
- breeding success and subsequent return were modeled.

Published result:
- timing deviations accumulated during some portions of migration but later
  dissipated;
- deviations disappeared during the long non-breeding period;
- breeding-ground arrival depended on stop number and stopover duration;
- accumulated lateness and breeding arrival date did not detectably reduce
  breeding success or return/survival.

Decision:

```text
INCOMING_TIMING_DEVIATION = YES
STAGEWISE_TIMING_CHANGE = YES
ACTION_PROXIES = YES
OUTGOING_TIMING = YES
BREEDING_SUCCESS = YES
RETURN_SURVIVAL = YES
SAME_INDIVIDUAL_LONGITUDINAL_DESIGN = YES
V4_CONCEPTUAL_QUESTION_ALREADY_TESTED = YES
ROLE = PRIOR_ART_SATURATING_V4_QUESTION
```

This is the decisive novelty result of the screen. The general question of
whether annual-cycle timing deviations persist, disappear and carry fitness
costs was already asked directly and answered in a longitudinal migration
study.

## Additional prior-art boundary

Paxton & Moore 2017 directly showed that late black-and-white warblers near
their breeding destination shortened stopover duration, consistent with
catch-up behavior.

Schmaljohann 2022 reviewed stopover functions in the full-annual-cycle context
and explicitly framed stop/continue decisions in terms of immediate and delayed
fitness costs.

Hahn, Cornelius & Watts 2025 explicitly proposed a trade-off between reducing
current timing mismatch through temporal flexibility and increasing later
carry-over effects.

Therefore none of the following can carry PAYOFF-B novelty:

- stopovers as timing-correction opportunities;
- late migrants shortening stopovers to catch up;
- timing correction carrying delayed fitness costs;
- annual-cycle timing deviations dissipating before breeding;
- asking in general whether timing recovery rescues fitness.

## Current direct-screen conclusion

```text
REDSTART = FAIL_SAME_INDIVIDUAL_ACTION_FITNESS_LINK
PIED_FLYCATCHER = FAIL_SIGNED_CORRECTION
WHITE_STORK = FAIL_PHASE_RESCUE_STRATEGY_RESET
HUDSONIAN_GODWIT = PRIOR_ART_ALREADY_TESTS_GENERAL_V4_QUESTION
DIRECT_NEW_FITNESS_RESCUE_DATASET = NONE_ADMITTED
V4_GENERAL_CONCEPTUAL_NOVELTY = NOT_ESTABLISHED
```

## What remains genuinely open in the field

The 2026 systematic review of migratory songbird ecology identifies concrete
gaps that are narrower than V4's general fitness-rescue question:

1. **where and when mortality occurs during migration**;
2. **what functional need causes a bird to land or remain at a stopover**;
3. **how migration distance changes migration decisions**;
4. **how predation danger changes decisions**;
5. **how stopover habitat quality changes migration decisions**.

These are empirical decision-and-consequence gaps.

## PAYOFF-B stop rule

Do not promote V4 as a new general theory or conceptual discovery.

Do not reanalyze any of the four screened systems merely to reproduce their
published central result.

A new PAYOFF-B paper must now do one of the following:

- test a narrower, predeclared empirical prediction not already answered in the
  source publication;
- combine multiple systems in a genuinely comparative analysis with a
  prespecified common estimand;
- obtain a new dataset that links an unresolved migration decision to a vital
  rate;
- or stop this publication branch.

Until one of those conditions is met:

```text
PAYOFF_B_V4_PUBLICATION_STATE = HOLD_NOVELTY_UNRESOLVED
```
