# PAYOFF-B V5 literature-search protocol

Date: 2026-10-03  
Status: **frozen before primary transition-effect extraction**

## Objective

Identify studies of migratory birds that quantify how timing at one annual-cycle
event propagates to the next event, with special attention to transitions that
buffer or reset earlier timing deviations.

## Core concepts

Search terms are built from three concept blocks.

**Annual-cycle timing**
- migration timing
- annual cycle
- phenology
- departure / arrival / laying / breeding

**Propagation**
- carry-over / carryover
- domino effect
- timing deviation
- delay
- sequential timing
- schedule adjustment

**Buffering / reset**
- buffer / buffering
- compensation
- reset / resetting
- stationary period
- stopover
- staging

## Search strings

Primary title/abstract searches:

1. (bird OR avian) AND migration AND ("annual cycle" OR year-round) AND ("carry-over" OR carryover) AND timing
2. (bird OR avian) AND migration AND ("domino effect" OR "sequential timing")
3. (bird OR avian) AND migration AND timing AND (buffering OR reset OR resetting OR compensation)
4. (bird OR avian) AND ("timing deviation" OR delay) AND migration AND (annual OR seasonal)
5. (bird OR avian) AND migration AND ("stationary period" OR stopover OR staging) AND timing

## Source-list searches

Reference lists and citing literature will be screened from:

- Senner et al. 2014;
- Briedis et al. 2018;
- Gow et al. 2019;
- Franklin et al. 2022 systematic review/meta-analysis;
- Carneiro et al. 2023;
- Weir & Phillimore 2024;
- Wang et al. 2024 global annual-cycle timing compilation.

Franklin et al. and Wang et al. are source corpora only. Their effect sizes are
not imported as timing-propagation coefficients.

## Screening stages

### Stage A — title/abstract

Include for full-text screening when the study:
- follows migratory birds;
- contains at least two annual-cycle timing events;
- discusses carry-over, domino effects, schedule adjustment, buffering or a
  directly equivalent sequential-timing relationship.

### Stage B — full text

Primary-effect eligibility requires:
- events A and B are temporally ordered;
- A and B are measured in the same individuals or an explicitly paired cohort;
- dates are in common time units;
- an unstandardized slope with uncertainty is reported, or raw individual data
  are publicly/author-accessible for prospective derivation.

### Stage C — fitness flag

Independently flag whether the study reports survival or reproduction after the
focal transition. Fitness reporting is not required for the primary buffering
synthesis.

## Screening decisions

Allowed statuses:
- INCLUDE_PRIMARY;
- INCLUDE_SECONDARY_CORRELATION_ONLY;
- INCLUDE_FITNESS_ONLY;
- FULLTEXT_REQUIRED;
- EXCLUDE_NO_SEQUENTIAL_TIMING;
- EXCLUDE_NO_PAIRED_UNIT;
- EXCLUDE_NO_RECOVERABLE_EFFECT;
- DUPLICATE_DATASET.

## Outcome-blind rule

Eligibility and transition class must be assigned without using the sign or
magnitude of the timing-propagation effect.

If a paper's narrative states 'reset', 'buffer' or 'domino effect', that wording
may be used to locate the paper but not to determine inclusion or transition
class. Inclusion depends on design and recoverable estimand.

## Search stop rule

Literature discovery stops only after:
1. all declared search strings have been screened;
2. reference lists of all included primary studies have been screened;
3. forward citations of the seven source-list anchors have been screened;
4. two consecutive snowball rounds yield no new primary-eligible study.

Only then may the project evaluate whether the corpus is large enough for
meta-regression versus a structured systematic synthesis.
