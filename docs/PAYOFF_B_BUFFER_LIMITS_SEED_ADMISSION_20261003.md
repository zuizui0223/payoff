# PAYOFF-B V5 seed-study admission ledger — 2026-10-03

Status: **eligibility screen only; focal comparative effect sizes not yet extracted**

This ledger applies the frozen V5 contract in
`data/payoff_b_buffer_limits_meta_contract_20261003.json` before numerical
`beta_AB` values are entered into the comparative corpus.

## Admission principle

The primary corpus requires an unstandardized day-for-day transition slope
between two ordered annual-cycle timing events, either reported directly with
uncertainty or estimable from individual-level data.

Correlation, repeatability and qualitative statements about "reset" are not
converted into `beta_AB`.

## SENNER2014 — Hudsonian godwit

Source:
Senner NR et al. 2014. *PLoS ONE* 9:e86588.
DOI 10.1371/journal.pone.0086588.

Design audit:
- 26 tracked adults; 43 complete and 13 partial tracks across 2009–2012;
- individual arrival/departure timing was expressed relative to year-specific
  population schedules;
- sequential mixed models were fitted to relative timing and to the change in
  timing deviation between stages;
- individual and year were random effects;
- breeding success and return were analysed separately.

Admission status:

```text
PRIMARY_STATUS = ADMIT_REPORTED_SLOPE
INDIVIDUAL_LEVEL_DESIGN = YES
COMMON_DAY_UNITS = YES
YEAR_ADJUSTMENT = YES
REPORTED_SEQUENTIAL_MODELS = YES
RAW_BETA_COMPATIBILITY = PASSED_FOR_TWO_CLEAN_TRANSITIONS
NUMERICAL_EXTRACTION = OPENED
```

Table 3 verification passed for two clean immediate transitions:

- Buenos Aires departure -> Chiloé arrival, active autumn migration:
  beta_AB = 0.97, SE = 0.07;
- Chiloé arrival -> Chiloé departure, non-breeding stationary period:
  beta_AB = 0.05, SE = 0.09.

The latter stationary interval averaged 192 +/- 2 d. Other Senner coefficients
that span multiple biological processes or use the authors' derived
rate-of-change response are not promoted automatically.

## GOW2019 — tree swallow

Source:
Gow EA et al. 2019. *Proc. R. Soc. B* 286:20181916.
DOI 10.1098/rspb.2018.1916.
Dryad 10.5061/dryad.5v5b124.

Design audit:
- 133 individuals from 12 North American breeding populations;
- each bird was tracked for one annual cycle;
- individual breeding, departure, stopover, non-breeding and spring-return
  timing variables were analysed;
- the individual-level timing dataset is publicly archived on Dryad;
- published models include geography and distance moderators, but the raw data
  permit V5 to estimate the prespecified transition slope on a common scale.

Admission status:

```text
PRIMARY_STATUS = ADMIT_REESTIMATE_FROM_PUBLIC_INDIVIDUAL_DATA
INDIVIDUAL_LEVEL_DESIGN = YES
COMMON_DAY_UNITS = YES
PUBLIC_RAW_DATA = YES
TRANSITIONS = MULTIPLE
NUMERICAL_EXTRACTION = NOT_YET_OPENED
```

The V5 reanalysis must use the frozen centering and transition-class rules; it
must not select only the published "domino" links.

## CARNEIRO2023 — Icelandic whimbrel

Source:
Carneiro C et al. 2023. *The American Naturalist* 201:353–362.
DOI 10.1086/722566.
Dryad 10.5061/dryad.vt4b8gtv9.

Design audit:
- 38 individuals tracked across seven years;
- public `dataStationary.csv` contains individual identifier, tracking years,
  autumn departure, winter arrival, spring departure, spring arrival and
  subsequent laying date;
- stopover duration, spring migration duration and breeding outcomes are also
  available;
- dates are reported in day-of-year units.

Admission status:

```text
PRIMARY_STATUS = ADMIT_REESTIMATE_FROM_PUBLIC_INDIVIDUAL_DATA
INDIVIDUAL_LEVEL_DESIGN = YES
COMMON_DAY_UNITS = YES
PUBLIC_RAW_DATA = YES
TRANSITIONS = MULTIPLE
FITNESS_LAYER = PARTIAL
NUMERICAL_EXTRACTION = NOT_YET_OPENED
```

This is currently the cleanest seed for estimating both active-migration and
stationary-period propagation from a common individual dataset.

## SAINO2017 — barn swallow

Source:
Saino N et al. 2017. *Journal of Animal Ecology* 86:239–249.
DOI 10.1111/1365-2656.12625.

Design audit:
- annual-cycle timing and fecundity are linked;
- the accessible primary results report Pearson correlation coefficients among
  focal phenological events;
- the frozen V5 contract explicitly forbids converting correlation
  coefficients into raw day-for-day propagation slopes.

Admission status:

```text
PRIMARY_STATUS = EXCLUDE_PRIMARY_CORRELATION_ONLY
INDIVIDUAL_LEVEL_BIOLOGY = YES
REPORTED_RAW_BETA = NO_CONFIRMED
SECONDARY_CORRELATION_SYNTHESIS = ELIGIBLE
FITNESS_LAYER = ELIGIBLE
NUMERICAL_PRIMARY_EXTRACTION = PROHIBITED
```

This study can enter the separately declared secondary standardized-correlation
or fitness layer, but not the primary `beta_AB` synthesis unless a public
individual dataset or reported unstandardized slope is independently located.

## BRIEDIS2018 — collared flycatcher

Source:
Briedis M et al. 2018. *Behavioral Ecology and Sociobiology* 72:93.
DOI 10.1007/s00265-018-2509-3.

Design audit:
- individual-based full annual-cycle tracking was combined with breeding and
  stable-isotope data;
- a brood-size manipulation was used to separate treatment effects from
  intrinsic quality;
- the paper explicitly identifies the non-breeding period as a buffer.

Admission status:

\`\`\`text
PRIMARY_STATUS = CONDITIONAL_REPORTED_OR_RAW_DATA
INDIVIDUAL_TRACKING = YES
SEQUENTIAL_TIMING = YES
PUBLIC_EVENT_LEVEL_DATA = NOT_LOCATED_IN_CURRENT_SCREEN
REPORTED_RAW_BETA = NOT_YET_VERIFIED
NUMERICAL_EXTRACTION = NOT_YET_OPENED
\`\`\`

The biological result is relevant, but "buffering" in the title is not an
admission criterion. A primary V5 effect requires either an unstandardized
event-to-event slope or recoverable individual event dates.

## LOPEZCALDERON2024 — barn swallow

Source:
López-Calderón C et al. 2024. *Ornithology* 141:ukae024.
Dryad 10.5061/dryad.ghx3ffbxj.

Design audit:
- 35 individuals (22 females, 13 males);
- public individual-level file contains departure from breeding colony, onset
  of autumn migration, winter arrival, spring migration onset and breeding
  arrival;
- the same individuals are linked to clutch number, total eggs and total
  fledglings where breeding data are available;
- dates are chronological event dates on a common scale.

Admission status:

\`\`\`text
PRIMARY_STATUS = ADMIT_REESTIMATE_FROM_PUBLIC_INDIVIDUAL_DATA
INDIVIDUAL_LEVEL_DESIGN = YES
COMMON_DATE_SCALE = YES
PUBLIC_RAW_DATA = YES
TRANSITIONS = MULTIPLE
FITNESS_LAYER = YES
NUMERICAL_EXTRACTION = NOT_YET_OPENED
\`\`\`

The published PLS path coefficients are not substituted for \`beta_AB\`; V5
will re-estimate the frozen raw day-for-day transition slopes from the public
event dates.

## ARCTIC_SKUA2024 — Arctic skua

Source:
Movement Ecology 2024, DOI 10.1186/s40462-024-00459-9.

Design audit:
- 276 migration cycles from 155 individuals across multiple breeding and
  wintering areas;
- six annual-cycle events are defined explicitly;
- processed analyses include timing and duration models with individual random
  effects;
- geolocator data are publicly listed by Movebank study ID;
- the article directly reports at least one day-for-day relationship:
  spring-arrival delay to clutch initiation.

Admission status:

\`\`\`text
PRIMARY_STATUS = EXCLUDE_PRIMARY_CURRENT_EVIDENCE
INDIVIDUAL_LEVEL_DESIGN = YES
MULTIPLE_POPULATIONS = YES
PUBLIC_GEOLOCATOR_DATA = YES
PROCESSED_EVENT_TABLE_PUBLIC = NOT_CONFIRMED
DIRECT_EVENT_TO_EVENT_BETA_WITH_UNCERTAINTY = NOT_CONFIRMED
DURATION_ONSET_SLOPES = DO_NOT_ALGEBRAICALLY_CONVERT_POST_HOC
NUMERICAL_PRIMARY_EXTRACTION = PROHIBITED_CURRENT_EVIDENCE
\`\`\`

Only coefficients already parameterized as event-B timing versus event-A
timing are eligible under the frozen primary definition. Duration-versus-onset
coefficients are not converted to \`beta_AB\` after seeing their results.

## BLACKTAILED2011 — Black-tailed godwit

Source:
Lourenço PM et al. 2011. *Journal of Ornithology* 152:1023–1032.
DOI 10.1007/s10336-011-0692-3.

Design audit:
- staging departure, breeding arrival and laying date were measured for the
  same colour-marked individuals;
- GLMs tested each timing event as a predictor of later timing events with year
  as a factor;
- repeatability was analysed separately and is not a V5 primary effect.

Admission status:

\`\`\`text
PRIMARY_STATUS = EXCLUDE_PRIMARY_INSUFFICIENT_EFFECT_REPORTING
INDIVIDUAL_LEVEL_DESIGN = YES
SEQUENTIAL_GLM = YES
REPEATABILITY_EFFECTS = EXCLUDE_PRIMARY
TABLE_2_REPORTS = F_P_R2_POWER_WITHOUT_RAW_BETA_SE
NUMERICAL_PRIMARY_EXTRACTION = PROHIBITED_CURRENT_EVIDENCE
\`\`\`

The paper's "no domino effects" conclusion is not coded as beta=0. Table 2
reports F statistics, P values, R-squared and power but not the unstandardized
day/day coefficient and its uncertainty. Unless individual-level data are
independently located, this study remains outside the primary beta synthesis.

## CATRY2013 — Cory's shearwater experiment

Source:
Catry P et al. 2013. *Ecology* 94:1230–1235.
DOI 10.1890/12-2177.1.

Design audit:
- parental investment was experimentally reduced;
- treatment shifted the timing and destination of later migration stages;
- the design is strong causal evidence for carry-over effects;
- the focal published contrast is treatment versus control rather than a
  day-for-day transition coefficient.

Admission status:

\`\`\`text
PRIMARY_STATUS = EXCLUDE_PRIMARY_INTERVENTION_CONTRAST
CAUSAL_CARRYOVER_ANCHOR = YES
SEQUENTIAL_TIMING = YES
RAW_EVENT_TO_EVENT_BETA = NOT_CONFIRMED
SECONDARY_MECHANISTIC_LAYER = ELIGIBLE
NUMERICAL_PRIMARY_EXTRACTION = PROHIBITED_UNLESS_RAW_DATES_LOCATED
\`\`\`

Experimental strength does not override the frozen estimand definition.

## CONKLIN2012 — bar-tailed godwit

Source:
Conklin JR & Battley PF 2012. *Journal of Avian Biology* 43:252–263.
DOI 10.1111/j.1600-048X.2012.05606.x.

Design audit:
- 77 individually colour-banded birds were followed across three non-breeding
  seasons;
- late arrival delayed wing moult;
- birds partially compensated by faster moult and shorter moult duration;
- delays of more than a month did not propagate to spring departure;
- subsequent return was also considered.

Admission status:

\`\`\`text
PRIMARY_STATUS = CONDITIONAL_REPORTED_SLOPE
INDIVIDUAL_LEVEL_DESIGN = YES
SEQUENTIAL_TIMING = YES
COMPENSATION_STAGE = MOULT_AND_NONBREEDING
PUBLIC_RAW_EVENT_DATA = NOT_LOCATED_IN_CURRENT_SCREEN
RAW_BETA_AND_UNCERTAINTY = VERIFY_FULL_TABLES
NUMERICAL_EXTRACTION = NOT_YET_OPENED
\`\`\`

This is biologically central to V5, but qualitative correction to the normal
departure schedule cannot be encoded as beta=0 without the admissible slope.

## Updated seed-screen tally

\`\`\`text
SCREENED = 10
PRIMARY_ADMIT_REESTIMATE = 3
PRIMARY_ADMIT_REPORTED = 1
PRIMARY_CONDITIONAL = 2
PRIMARY_EXCLUDE = 4
FOCAL_BETA_VALUES_OPENED = 2
\`\`\`

Admitted for re-estimation:
- GOW2019
- CARNEIRO2023
- LOPEZCALDERON2024

Admitted from reported coefficients:
- SENNER2014 — two clean primary transitions opened.

Conditional pending coefficient/data verification:
- BRIEDIS2018
- CONKLIN2012

Excluded from the primary beta synthesis under the current evidence state:
- SAINO2017 — accessible result is correlation, not raw propagation;
- CATRY2013 — experimental treatment contrast, not raw propagation;
- ARCTIC_SKUA2024 — no directly reported event-to-event beta with admissible uncertainty confirmed;
- BLACKTAILED2011 — Table 2 lacks raw beta and SE.

## Remaining seed screen

Before primary modelling, complete the same audit for any unreviewed seed or
newly discovered study. The screen must record exclusions as actively as
admissions, and no study is promoted because its verbal conclusion agrees with
V5.
