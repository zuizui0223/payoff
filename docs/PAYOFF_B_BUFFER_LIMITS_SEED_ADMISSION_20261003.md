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

## Prior-art correction after the first six effects were opened

A subsequent novelty audit identified two papers that narrow the V5 claim
without changing the six already extracted effects:

- Schmaljohann (2019) already reports species-specific departure-to-arrival
  day-for-day relationships across 17 spring and 21 autumn migrant species.
- van Bemmelen et al. (2024) already treats stage-to-stage timing relationships
  as compensation/carry-over strength across the annual cycle of Arctic skuas.

Therefore the slope concept, partial compression, and species variation in a
departure-to-arrival slope are prior art. The remaining candidate contribution
is a **cross-transition-class synthesis**.

This correction was made after the first six V5 effects were visible. It is a
novelty-boundary correction, not a new outcome hypothesis.


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
PRIMARY_STATUS = ADMIT_REESTIMATE_FROM_PUBLIC_INDIVIDUAL_DATA
INDIVIDUAL_LEVEL_BIOLOGY = YES
PUBLIC_RAW_DATA = YES
DRYAD_DOI = 10.5061/dryad.12n6v
REPORTED_RAW_BETA = NO_CONFIRMED
FITNESS_LAYER = ELIGIBLE
NUMERICAL_PRIMARY_EXTRACTION = NOT_YET_OPENED
```

The published correlation and path coefficients remain ineligible as primary
effects. The admission is instead based on the public individual-level Dryad
dataset, from which only directly observed day-scale event transitions may be
re-estimated under the frozen V5 definition.

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
PRIMARY_STATUS = ADMIT_REPORTED_SLOPE
INDIVIDUAL_LEVEL_DESIGN = YES
SEQUENTIAL_TIMING = YES
COMPENSATION_STAGE = MOULT_AND_NONBREEDING
PUBLIC_RAW_EVENT_DATA = NOT_LOCATED_IN_CURRENT_SCREEN
RAW_BETA_AND_UNCERTAINTY = PASSED_FOR_TWO_WITHIN_SUBJECT_TRANSITIONS
NUMERICAL_EXTRACTION = OPENED
\`\`\`

Table 3 supplies two admissible within-subject timing-to-timing effects:

- New Zealand arrival -> start of primary moult:
  beta_AB = 1.00, SE = 0.10;
- end of pre-basic moult -> start of primary moult:
  beta_AB = 0.23, SE = 0.10.

Both are coded NONBREEDING_STATIONARY. The reported non-significant
arrival -> spring-departure result is **not** coded as beta=0 because the
unstandardized coefficient was not reported. Duration responses are likewise
kept out of the primary timing-to-timing synthesis.

## BRIEDIS_SPRINT2018 — collared flycatcher sprint migration

Source:
Briedis M et al. 2018. *Ecology and Evolution* 8:11179–11191.
DOI 10.1002/ece3.4206.
Dryad 10.5061/dryad.v51p331.

Design audit:
- individually tracked collared flycatchers were followed across complete
  autumn and spring migration;
- departure and arrival dates were analysed directly on the same day scale;
- the authors also measured migration speed and documented stronger catch-up
  in spring.

Admission status:

\`\`\`text
PRIMARY_STATUS = ADMIT_REPORTED_SLOPE
INDIVIDUAL_LEVEL_DESIGN = YES
COMMON_DAY_UNITS = YES
DIRECT_EVENT_TO_EVENT_BETA = YES
NUMERICAL_EXTRACTION = OPENED
\`\`\`

Two direct departure-to-arrival effects are admissible:

- autumn departure -> autumn arrival:
  beta_AB = 0.49, SE = 0.13;
- spring departure -> spring arrival:
  beta_AB = 0.20, SE = 0.12.

The migration-speed regressions are mechanistic anchors but are not themselves
primary timing-propagation effects.

## VANWIJK2017 — Eurasian hoopoe

Source:
van Wijk RE, Schaub M & Bauer S. 2017. *Behavioral Ecology and
Sociobiology* 71:73.
DOI 10.1007/s00265-017-2305-5.

Design audit:
- 57 unique first annual-cycle tracks were retained from a five-year hoopoe
  study;
- timing and duration of successive breeding, migration and non-breeding
  activities were analyzed in days;
- breeding phenology, territory quality and fledgling production were linked to
  the tracked individuals;
- the paper explicitly interprets timing coefficients below one as weakening
  carry-over through the annual cycle;
- the focal dependency analysis uses model-averaged coefficients conditional
  on multiple preceding activities rather than the simple pairwise V5 slope by
  default;
- the 2025 public Swiss-hoopoe geolocator package
  (Zenodo 10.5281/zenodo.15260024) provides tracks and tag data, but a matching
  public table of all breeding-event dates needed for direct V5 re-estimation
  was not confirmed in the present audit.

Admission status:

```text
PRIMARY_STATUS = CONDITIONAL_REPORTED_OR_RAW_DATA
INDIVIDUAL_LEVEL_DESIGN = YES
COMMON_DAY_UNITS = YES
FITNESS_LAYER = YES
PUBLISHED_COEFFICIENTS = MODEL_AVERAGED_CONDITIONAL
PUBLIC_GEOLOCATOR_PACKAGE = YES
PUBLIC_MATCHED_BREEDING_EVENT_TABLE = NOT_CONFIRMED
NUMERICAL_PRIMARY_EXTRACTION = NOT_YET_OPENED
```

Do not treat the dependency matrix or a conditional model-averaged coefficient
as the primary pairwise `beta_AB` without demonstrating that the estimand
matches the frozen V5 definition.

## MEIER2020 — alpine swift

Source:
Meier CM et al. 2020. *Journal of Avian Biology*.
DOI 10.1111/jav.02515.

Design audit:
- 215 individuals from four populations were tracked with geolocators;
- four major annual-cycle event dates were modeled;
- previous-stage timing was included to test carry-over;
- all variables were z-transformed before the reported models, so the published
  previous-stage effects are standardized rather than day-for-day slopes.

Admission status:

```text
PRIMARY_STATUS = EXCLUDE_PRIMARY_CURRENT_EVIDENCE
INDIVIDUAL_LEVEL_DESIGN = YES
SEQUENTIAL_TIMING = YES
REPORTED_PREVIOUS_STAGE_EFFECT = YES
REPORTED_RAW_DAY_DAY_BETA = NO
STANDARDIZED_EFFECT_ONLY = YES
NUMERICAL_PRIMARY_EXTRACTION = PROHIBITED_CURRENT_EVIDENCE
```

The standardized carry-over coefficients must not be converted into raw
propagation coefficients. This system can reopen only if individual event dates
are independently located.

## BRIEDIS_MULTI2019 — 14-species Afro-Palearctic synthesis

Source:
Briedis M et al. 2019. *Proceedings of the Royal Society B*
286:20182821.
DOI 10.1098/rspb.2018.2821.
Dryad 10.5061/dryad.t78400r.

Design audit:
- more than 350 migration tracks across 14 long-distance migrant species;
- departure and arrival timing were linked within autumn and spring;
- the public database is a useful source map for underlying cohorts;
- the dataset combines cohorts that also appear in primary species/population
  papers and therefore is not an independent biological dataset for V5.

Admission status:

```text
ROLE = HIGH_PRIORITY_PRIOR_ART_AND_SOURCE_MAP
MULTISPECIES_CARRYOVER = YES
PUBLIC_DATABASE = YES
PRIMARY_INDEPENDENCE_UNIT = NO
COUNT_AS_NEW_DATASET = NO
DOUBLE_COUNT_WITH_PRIMARY_STUDIES = PROHIBITED
```

This study further closes any claim that multi-species departure-to-arrival
carry-over is new. Its value for V5 is discovery and deduplication of source
cohorts.

## FAYET2016 — Manx shearwater experiment

Source:
Fayet AL et al. 2016. *Journal of Animal Ecology* 85:1516–1527.
DOI 10.1111/1365-2656.12580.
Dryad 10.5061/dryad.32kc7.

Design audit:
- reproductive effort was manipulated experimentally by cross-fostering chicks;
- adults were followed through migration and wintering with geolocators;
- later breeding phenology and breeding success were measured;
- public Dryad data include full annual-cycle geolocator and metadata files;
- the central causal estimand is treatment contrast / carry-over from
  reproductive effort rather than an upstream-date to downstream-date
  day-for-day slope.

Admission status:

```text
PRIMARY_STATUS = EXCLUDE_PRIMARY_INTERVENTION_CONTRAST
EXPERIMENTAL_CARRYOVER = YES
FULL_ANNUAL_CYCLE_TRACKING = YES
FITNESS_LAYER = YES
RAW_PAIRWISE_BETA = NOT_CONFIRMED
SECONDARY_MECHANISTIC_LAYER = ELIGIBLE
```

The strong experimental design does not override the common-estimand rule.

## OUWEHAND2017 — Dutch pied flycatcher

Source:
Ouwehand J & Both C. 2017. *Journal of Animal Ecology* 86:88–97.
DOI 10.1111/1365-2656.12599.
Dryad 10.5061/dryad.k6q68.

Design audit:
- individual light-level geolocators were used to infer wintering-ground
  departure and breeding-ground arrival;
- spring migration duration was available for the same tracked birds;
- the paper reports a strong positive departure-to-arrival relationship and
  concludes that variation in spring arrival was caused by variation in
  African departure rather than migration speed;
- the public Dryad repository contains the timing/geolocator data used in the
  analysis;
- the currently retrieved article text does not expose a verified
  unstandardized pairwise slope with uncertainty, so no numerical V5 effect is
  copied from prose or figure appearance.

Admission status:

```text
PRIMARY_STATUS = ADMIT_REESTIMATE_FROM_PUBLIC_INDIVIDUAL_DATA
TRANSITION_CLASS = ACTIVE_SPRING_MIGRATION
INDIVIDUAL_LEVEL_DESIGN = YES
COMMON_DAY_UNITS = YES
PUBLIC_RAW_DATA = YES
DRYAD_DOI = 10.5061/dryad.k6q68
REPORTED_RAW_BETA_SE = NOT_VERIFIED
NUMERICAL_EXTRACTION = NOT_YET_OPENED
```

This cohort is an independent active-migration candidate, subject to the V5
duplicate-data check against multi-species syntheses that later reused the same
tracking records.

## LEMKE2013 — great reed warbler

Source:
Lemke HW et al. 2013. *PLoS ONE* 8:e79209.
DOI 10.1371/journal.pone.0079209.

Design audit:
- complete annual-cycle geolocator data were available for six males, with
  additional partial autumn data;
- spring departure from the final wintering site and breeding-ground arrival
  were both measured for the same individuals;
- the article reports only a Spearman correlation for the spring
  departure-to-arrival relationship (r_s=0.94, n=6), which is ineligible as a
  V5 primary effect;
- public Supplementary Table S3 is an XLSX containing individual annual-cycle
  geolocator event data, so the raw day-for-day slope can be re-estimated
  without converting the correlation.

Admission status:

```text
PRIMARY_STATUS = ADMIT_REESTIMATE_FROM_PUBLIC_INDIVIDUAL_DATA
TRANSITION_CLASS = ACTIVE_SPRING_MIGRATION
INDIVIDUAL_LEVEL_DESIGN = YES
COMMON_DAY_UNITS = YES
PUBLIC_INDIVIDUAL_EVENT_TABLE = YES
REPORTED_PRIMARY_EFFECT = CORRELATION_ONLY_INELIGIBLE
NUMERICAL_EXTRACTION = NOT_YET_OPENED
```

The autumn breeding-departure to first-winter-arrival transition may also be
estimable from Table S3 but must be screened separately for biological
comparability and missingness.

## CALLO2013 — red-eyed vireo

Source:
Callo PA, Morton ES & Stutchbury BJM. 2013. *The Auk* 130:240–246.
DOI 10.1525/auk.2013.12213.

Design audit:
- ten males returned with usable geolocator data;
- departure from South America and breeding-ground arrival were measured on the
  same birds;
- the paper reports a strong spring departure-to-arrival correlation
  (r=0.81, p=0.002) despite long and variable stopovers;
- no verified raw unstandardized beta with uncertainty or public individual
  timing table was located in the current screen.

Admission status:

```text
PRIMARY_STATUS = CONDITIONAL_RAW_DATA_OR_COMPATIBLE_BETA_REQUIRED
INDIVIDUAL_LEVEL_DESIGN = YES
TRANSITION_CLASS = ACTIVE_SPRING_MIGRATION
REPORTED_CORRELATION = YES_INELIGIBLE
REPORTED_RAW_BETA_SE = NO_CONFIRMED
PUBLIC_INDIVIDUAL_TABLE = NOT_CONFIRMED
NUMERICAL_PRIMARY_EXTRACTION = PROHIBITED_CURRENT_EVIDENCE
```

Correlation is not converted into `beta_AB`.

## JAHN2013 — Tyrannus flycatchers

Source:
Jahn AE et al. 2013. *The Auk* 130:247–257.
DOI 10.1525/auk.2013.13010.

Design audit:
- the paper tracks Eastern Kingbirds, Western Kingbirds and Scissor-tailed
  Flycatchers from distinct breeding cohorts;
- published Table 1 lists individual fall departure, winter arrival, spring
  departure and breeding arrival dates;
- spring sample sizes include at least seven Eastern Kingbird records and six
  Western Kingbird records with sufficient timing data;
- the article reports only correlations for the spring relationships
  (Eastern Kingbird r=0.55; Western Kingbird r=0.94), not the V5 raw slope;
- because the individual dates are published, species-specific day-for-day
  slopes can in principle be re-estimated directly from Table 1.

Admission status:

```text
PRIMARY_STATUS = PARTIALLY_OPENED_FROM_PUBLISHED_INDIVIDUAL_TABLE
MULTISPECIES = YES
INDEPENDENCE_UNIT = SPECIES_BY_BREEDING_COHORT
COMMON_DAY_UNITS = YES
PUBLISHED_INDIVIDUAL_EVENT_DATES = YES
REPORTED_PRIMARY_EFFECT = CORRELATION_ONLY_INELIGIBLE
WESTERN_KINGBIRD_SPRING = OPENED
WESTERN_KINGBIRD_AUTUMN = OPENED
SCISSOR_TAILED_AUTUMN = OPENED
SCISSOR_TAILED_SPRING = INSUFFICIENT_COMPLETE_PAIRS
EASTERN_KINGBIRD = HOLD_RECORD_STRUCTURE_AMBIGUITY
```

The opened effects are recorded in
`docs/PAYOFF_B_V5_JAHN2013_EFFECT_RECEIPT_20261004.md` and the cumulative
effect file `data/payoff_b_buffer_limits_effects_v0_2_20261004.csv`.

Western Kingbird spring provides a source-faithfulness check: the six complete
pairs reproduce the published departure-arrival correlation (r≈0.94) before
the raw V5 slope is estimated.

Eastern Kingbird is held because one bird contributes two years and the table
also includes an Oklahoma individual among the primarily Nebraska cohort.
No post-hoc choice of repeated year, averaging rule or population pooling is
made.

## Updated seed-screen tally

```text
SCREENED = 19
PRIMARY_ADMIT_REESTIMATE = 7
PRIMARY_ADMIT_REPORTED = 3
PRIMARY_CONDITIONAL = 3
PRIMARY_EXCLUDE = 5
PRIOR_ART_NONINDEPENDENT = 1
FOCAL_BETA_VALUES_OPENED = 9
```

Admitted for re-estimation:
- GOW2019
- LEMKE2013
- JAHN2013
- OUWEHAND2017
- SAINO2017
- CARNEIRO2023
- LOPEZCALDERON2024

Admitted from reported coefficients:
- SENNER2014 — two clean primary transitions opened;
- CONKLIN2012 — two clean within-subject stationary transitions opened;
- BRIEDIS_SPRINT2018 — autumn and spring departure-to-arrival slopes opened.

Conditional pending coefficient/data verification:
- BRIEDIS2018
- CALLO2013
- VANWIJK2017

Excluded from the primary beta synthesis under the current evidence state:
- CATRY2013 — experimental treatment contrast, not raw propagation;
- ARCTIC_SKUA2024 — no directly reported event-to-event beta with admissible uncertainty confirmed;
- BLACKTAILED2011 — Table 2 lacks raw beta and SE;
- MEIER2020 — reported previous-stage effects are standardized;
- FAYET2016 — experimental treatment contrast rather than raw timing propagation.

Prior-art/source-map only:
- BRIEDIS_MULTI2019 — multi-species carry-over using overlapping source cohorts; do not count as an independent dataset.

## Remaining seed screen

Before primary modelling, complete the same audit for any unreviewed seed or
newly discovered study. The screen must record exclusions as actively as
admissions, and no study is promoted because its verbal conclusion agrees with
V5.
